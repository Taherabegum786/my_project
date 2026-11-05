// loadgen: E8 load generator.
//
//   -mode p1   closed loop, -conns keep-alive connections, sessions of K requests per token
//   -mode p2   open loop Poisson at -rate req/s over -conns connections (latency from the
//              scheduled arrival time, so queueing in the generator is counted)
//   -mode p3   token sessions: Poisson token issuance at -lambda per pipeline, Zipf(alpha) virtual
//              edge choice, first request after lognormal delay, then K~geom(mean) segments
//   -mode rtt  keep-alive GET /ping samples
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"math"
	"math/rand"
	"net"
	"net/http"
	"net/url"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"emberproto/tokens"
)

var (
	mode     = flag.String("mode", "p1", "p1|p2|p3|rtt")
	target   = flag.String("target", "127.0.0.1:8080", "edge host:port")
	scheme   = flag.String("scheme", "b1", "scheme path component")
	conns    = flag.Int("conns", 64, "connections")
	warm     = flag.Duration("warm", 5*time.Second, "warm-up")
	dur      = flag.Duration("dur", 20*time.Second, "measurement duration")
	K        = flag.Int("K", 150, "p1/p2: requests per token (session)")
	sessions = flag.Int("sessions", 8000, "p1/p2: pre-generated tokens")
	edgePid  = flag.Int("edgepid", 0, "edge pid for CPU accounting")
	out      = flag.String("out", "", "CSV to append a row to")
	run      = flag.Int("run", 0, "run index")
	seed     = flag.Int64("seed", 20261105, "seed")
	rate     = flag.Float64("rate", 1000, "p2 req/s")
	loadFrac = flag.Float64("loadfrac", 0, "p2 label")
	netLabel = flag.String("net", "netns-tapbridge", "net label")
	// p3
	issuerURL = flag.String("issuer", "http://10.72.0.2:9090", "issuer base URL")
	pipes     = flag.String("pipes", "pull:200:1", "mode:lambda:kid,...")
	V         = flag.Int("V", 10, "virtual edges")
	alpha     = flag.Float64("alpha", 0.8, "Zipf exponent of edge shares")
	kmean     = flag.Float64("kmean", 20, "mean segments per session (geometric)")
	segIv     = flag.Duration("seg", 200*time.Millisecond, "segment interval")
	firstMed  = flag.Float64("first-med-ms", 120, "token receipt -> first request lognormal median (ms)")
	firstSig  = flag.Float64("first-sigma", 0.5, "lognormal sigma")
	deltaS    = flag.Float64("delta", 1, "p3 label: epoch Δ (s)")
	reqOut    = flag.String("reqout", "", "p3: per-request CSV (optional)")
	n         = flag.Int("n", 500, "rtt samples")
)

// ------------------------------------------------------------------ raw HTTP/1.1 client

type hconn struct {
	c  net.Conn
	br *bufio.Reader
}

func dial(addr string) (*hconn, error) {
	c, err := net.DialTimeout("tcp", addr, 5*time.Second)
	if err != nil {
		return nil, err
	}
	c.(*net.TCPConn).SetNoDelay(true)
	return &hconn{c: c, br: bufio.NewReaderSize(c, 16384)}, nil
}

// do sends one request and returns status and selected headers.
func (h *hconn) do(req []byte) (int, map[string]string, error) {
	if _, err := h.c.Write(req); err != nil {
		return 0, nil, err
	}
	line, err := h.br.ReadSlice('\n')
	if err != nil {
		return 0, nil, err
	}
	if len(line) < 12 {
		return 0, nil, fmt.Errorf("bad status line")
	}
	status, _ := strconv.Atoi(string(line[9:12]))
	hdr := map[string]string{}
	cl := 0
	for {
		l, err := h.br.ReadSlice('\n')
		if err != nil {
			return 0, nil, err
		}
		if len(l) <= 2 {
			break
		}
		i := bytes.IndexByte(l, ':')
		if i < 0 {
			continue
		}
		k := string(bytes.ToLower(l[:i]))
		v := string(bytes.TrimSpace(l[i+1:]))
		if k == "content-length" {
			cl, _ = strconv.Atoi(v)
		} else if strings.HasPrefix(k, "x-") {
			hdr[k] = v
		}
	}
	if _, err := h.br.Discard(cl); err != nil {
		return 0, nil, err
	}
	return status, hdr, nil
}

func mkReq(path, tok string, extra string) []byte {
	return []byte("GET " + path + "?Token=" + tok + " HTTP/1.1\r\nHost: cdn.example.com\r\n" + extra + "\r\n")
}

// ------------------------------------------------------------------ helpers

func pct(x []float64, p float64) float64 {
	if len(x) == 0 {
		return math.NaN()
	}
	s := append([]float64{}, x...)
	sort.Float64s(s)
	i := int(math.Ceil(p/100*float64(len(s)))) - 1
	if i < 0 {
		i = 0
	}
	return s[i]
}

func mean(x []float64) float64 {
	if len(x) == 0 {
		return math.NaN()
	}
	t := 0.0
	for _, v := range x {
		t += v
	}
	return t / float64(len(x))
}

func cpuTicks(pid int) float64 {
	b, err := os.ReadFile(fmt.Sprintf("/proc/%d/stat", pid))
	if err != nil {
		return math.NaN()
	}
	s := string(b)
	f := strings.Fields(s[strings.LastIndexByte(s, ')')+2:])
	u, _ := strconv.ParseFloat(f[11], 64)
	st, _ := strconv.ParseFloat(f[12], 64)
	return u + st // clock ticks (100/s)
}

func appendCSV(path, header, row string) {
	if path == "" {
		fmt.Println(header)
		fmt.Println(row)
		return
	}
	_, err := os.Stat(path)
	f, e2 := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if e2 != nil {
		log.Fatal(e2)
	}
	defer f.Close()
	if os.IsNotExist(err) {
		fmt.Fprintln(f, header)
	}
	fmt.Fprintln(f, row)
	fmt.Println(row)
}

// ------------------------------------------------------------------ token pools (p1/p2)

type pool struct {
	toks   []string
	prefix []string
}

func post(addr, path string, body []byte) {
	resp, err := http.Post("http://"+addr+path, "application/octet-stream", bytes.NewReader(body))
	if err != nil {
		log.Fatal(err)
	}
	b, _ := io.ReadAll(resp.Body)
	resp.Body.Close()
	if resp.StatusCode != 200 {
		log.Fatalf("admin %s: %s", path, b)
	}
}

// buildPool makes S session tokens for the scheme and installs edge state (roots/certs/keys).
func buildPool(S int) *pool {
	k := tokens.DeriveKeys(20261105)
	p := &pool{}
	exp := time.Now().Unix() + 7200
	cl := func(i int) tokens.Claims {
		pre := fmt.Sprintf("/%s/t1/s%d/", *scheme, i)
		p.prefix = append(p.prefix, pre)
		return tokens.Claims{URLPrefix: pre, Expires: exp, Tenant: 1}
	}
	switch *scheme {
	case "o1", "o1a", "o4":
		alg := uint8(tokens.AlgMLDSA44)
		if *scheme == "o4" {
			alg = tokens.AlgHybrid
		}
		const per = 1024
		tnow := uint64(time.Now().UnixMilli())
		for e := 0; e*per < S; e++ {
			var cs []tokens.Claims
			for i := e * per; i < (e+1)*per && i < S; i++ {
				cs = append(cs, cl(i))
			}
			for i := range cs {
				cs[i].Expires = int64(tnow/1000) + 3000
			}
			kid := uint32(1)
			if *scheme == "o4" {
				kid = 4
			}
			sr, toks := tokens.IssueEpoch(k, alg, kid, uint32(e+1), tnow, 1000, cs, tokens.RandFill)
			post(*target, fmt.Sprintf("/admin/root?v=0&kid=%d", kid), sr.Marshal())
			p.toks = append(p.toks, toks...)
		}
	default:
		aux := 1
		switch *scheme {
		case tokens.B11:
			post(*target, "/admin/deleg", tokens.MakeDelegCert(k, 1, exp))
		case tokens.B12:
			post(*target, "/admin/kem", tokens.WrapEpochKey(k.EdgeKEM.EncapsulationKey(), 1, tokens.EpochKey(k, 1)))
		}
		for i := 0; i < S; i++ {
			t, err := tokens.SignPerToken(k, *scheme, cl(i), aux)
			if err != nil {
				log.Fatal(err)
			}
			p.toks = append(p.toks, t)
		}
	}
	return p
}

// sessionReqs: global request counter -> (session, segment); a token is used for K consecutive
// requests on one connection.
type sess struct {
	p    *pool
	next atomic.Int64
	wrap atomic.Int64
}

func (s *sess) get() int {
	i := int(s.next.Add(1) - 1)
	if i >= len(s.p.toks) {
		s.wrap.Add(1)
		i %= len(s.p.toks)
	}
	return i
}

// ------------------------------------------------------------------ P1

func p1() {
	p := buildPool(*sessions)
	ss := &sess{p: p}
	var measuring atomic.Bool
	var stop atomic.Bool
	lat := make([][]float64, *conns)
	var errs atomic.Int64
	var wg sync.WaitGroup
	for c := 0; c < *conns; c++ {
		wg.Add(1)
		go func(c int) {
			defer wg.Done()
			h, err := dial(*target)
			if err != nil {
				log.Fatal(err)
			}
			for !stop.Load() {
				si := ss.get()
				for j := 0; j < *K && !stop.Load(); j++ {
					path := fmt.Sprintf("%sseg%05d.m4s", p.prefix[si], j)
					t0 := time.Now()
					st, _, err := h.do(mkReq(path, p.toks[si], ""))
					if err != nil || st != 200 {
						errs.Add(1)
						if err != nil {
							h.c.Close()
							h, _ = dial(*target)
						}
						continue
					}
					if measuring.Load() {
						lat[c] = append(lat[c], float64(time.Since(t0).Microseconds())/1000)
					}
				}
			}
		}(c)
	}
	time.Sleep(*warm)
	c0 := cpuTicks(*edgePid)
	e0 := errs.Load()
	t0 := time.Now()
	measuring.Store(true)
	time.Sleep(*dur)
	measuring.Store(false)
	el := time.Since(t0).Seconds()
	c1 := cpuTicks(*edgePid)
	stop.Store(true)
	wg.Wait()
	var all []float64
	for _, l := range lat {
		all = append(all, l...)
	}
	cpu := (c1 - c0) / 100 / el
	if ss.wrap.Load() > 0 || errs.Load()-e0 > 0 {
		log.Printf("WARNING scheme=%s wraps=%d errors=%d", *scheme, ss.wrap.Load(), errs.Load()-e0)
	}
	appendCSV(*out, "scheme,run,req_per_s,cpu_util_edge,p50_ms,p99_ms,n_req,errors,token_bytes,net,impl",
		fmt.Sprintf("%s,%d,%.1f,%.3f,%.3f,%.3f,%d,%d,%d,%s,go-1.24.7+circl-1.6.1", *scheme, *run, float64(len(all))/el, cpu,
			pct(all, 50), pct(all, 99), len(all), errs.Load()-e0, len(p.toks[0]), *netLabel))
}

// ------------------------------------------------------------------ P2

func p2() {
	p := buildPool(*sessions)
	type job struct{ t time.Time }
	jobs := make(chan job, 1<<20)
	var mu sync.Mutex
	var lat []float64
	var errs, sent atomic.Int64
	measureFrom := time.Now().Add(*warm)
	measureTo := measureFrom.Add(*dur)
	// sessions: each connection owns a session token for K requests
	ss := &sess{p: p}
	var wg sync.WaitGroup
	for c := 0; c < *conns; c++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			h, err := dial(*target)
			if err != nil {
				log.Fatal(err)
			}
			si, j := ss.get(), 0
			var local []float64
			for jb := range jobs {
				if j == *K {
					si, j = ss.get(), 0
				}
				path := fmt.Sprintf("%sseg%05d.m4s", p.prefix[si], j)
				j++
				st, _, err := h.do(mkReq(path, p.toks[si], ""))
				done := time.Now()
				if err != nil || st != 200 {
					errs.Add(1)
					if err != nil {
						h.c.Close()
						h, _ = dial(*target)
					}
					continue
				}
				if jb.t.After(measureFrom) && jb.t.Before(measureTo) {
					local = append(local, float64(done.Sub(jb.t).Microseconds())/1000)
				}
			}
			mu.Lock()
			lat = append(lat, local...)
			mu.Unlock()
		}()
	}
	rng := rand.New(rand.NewSource(*seed + int64(1000**run)))
	start := time.Now()
	next := start
	end := measureTo
	for next.Before(end) {
		next = next.Add(time.Duration(rng.ExpFloat64() / *rate * 1e9))
		if d := time.Until(next); d > 0 {
			time.Sleep(d)
		}
		jobs <- job{next}
		sent.Add(1)
	}
	close(jobs)
	wg.Wait()
	achieved := float64(len(lat)) / dur.Seconds()
	appendCSV(*out, "scheme,load_frac,run,rate_target,rate_achieved,p50_ms,p99_ms,n_req,errors,net,impl",
		fmt.Sprintf("%s,%.2f,%d,%.1f,%.1f,%.3f,%.3f,%d,%d,%s,go-1.24.7+circl-1.6.1", *scheme, *loadFrac, *run, *rate, achieved,
			pct(lat, 50), pct(lat, 99), len(lat), errs.Load(), *netLabel))
}

// ------------------------------------------------------------------ P3

type reqRec struct {
	pipe    int
	tok     int
	vedge   int
	seq     int
	latMs   float64
	waitMs  float64
	event   string
	status  int
	issueMs float64
}

func zipfCDF(V int, a float64) []float64 {
	w := make([]float64, V)
	t := 0.0
	for v := range w {
		w[v] = 1 / math.Pow(float64(v+1), a)
		t += w[v]
	}
	c := make([]float64, V)
	acc := 0.0
	for v := range w {
		acc += w[v] / t
		c[v] = acc
	}
	return c
}

func p3() {
	type pipe struct {
		mode   string
		lambda float64
		kid    int
	}
	var ps []pipe
	for _, s := range strings.Split(*pipes, ",") {
		f := strings.Split(s, ":")
		l, _ := strconv.ParseFloat(f[1], 64)
		k, _ := strconv.Atoi(f[2])
		ps = append(ps, pipe{f[0], l, k})
	}
	cdf := zipfCDF(*V, *alpha)
	issueClient := &http.Client{Timeout: 60 * time.Second, Transport: &http.Transport{MaxIdleConnsPerHost: 4096, MaxIdleConns: 4096, IdleConnTimeout: 600 * time.Second}}
	var mu sync.Mutex
	var recs []reqRec
	var issueWait [][]float64 = make([][]float64, len(ps))
	ntok := make([]int, len(ps))
	stapleUp := make([]int64, len(ps))
	var errs atomic.Int64
	var wg sync.WaitGroup
	start := time.Now()
	for pi, pp := range ps {
		wg.Add(1)
		go func(pi int, pp pipe) {
			defer wg.Done()
			rng := rand.New(rand.NewSource(*seed + int64(1000**run) + int64(pi)))
			next := start
			ti := 0
			var tw sync.WaitGroup
			for {
				next = next.Add(time.Duration(rng.ExpFloat64() / pp.lambda * 1e9))
				if next.Sub(start) > *dur {
					break
				}
				time.Sleep(time.Until(next))
				// per-token randomness drawn up-front from the pipe RNG
				u := rng.Float64()
				vedge := sort.SearchFloat64s(cdf, u)
				if vedge >= *V {
					vedge = *V - 1
				}
				firstDelay := time.Duration(*firstMed * math.Exp(*firstSig*rng.NormFloat64()) * 1e6)
				k := 1 + int(math.Floor(math.Log(1-rng.Float64())/math.Log(1-1 / *kmean)))
				id := ti
				ti++
				tw.Add(1)
				go func() {
					defer tw.Done()
					t0 := time.Now()
					q := url.Values{"kid": {strconv.Itoa(pp.kid)}, "tenant": {strconv.Itoa(pp.kid)},
						"prefix": {fmt.Sprintf("/o1/t%d/s%d/", pp.kid, id)}}
					resp, err := issueClient.Get(*issuerURL + "/issue?" + q.Encode())
					if err != nil {
						errs.Add(1)
						return
					}
					tb, _ := io.ReadAll(resp.Body)
					resp.Body.Close()
					root := resp.Header.Get("X-EMBER-Root")
					iw := float64(time.Since(t0).Microseconds()) / 1000
					tok := string(tb)
					mu.Lock()
					issueWait[pi] = append(issueWait[pi], iw)
					ntok[pi]++
					mu.Unlock()
					time.Sleep(firstDelay)
					h, err := dial(*target)
					if err != nil {
						errs.Add(1)
						return
					}
					defer h.c.Close()
					seqStart := time.Now()
					for j := 0; j <= k; j++ { // manifest (j=0) + k segments
						if j > 0 {
							time.Sleep(time.Until(seqStart.Add(time.Duration(j) * *segIv)))
						}
						extra := fmt.Sprintf("X-VEdge: %d\r\n", pi*1000+vedge)
						if j == 0 && pp.mode == "pull_staple" {
							extra += "X-EMBER-Root: " + root + "\r\n"
							atomic.AddInt64(&stapleUp[pi], int64(len("X-EMBER-Root: ")+len(root)+2))
						}
						path := fmt.Sprintf("/o1/t%d/s%d/seg%05d.m4s", pp.kid, id, j)
						t1 := time.Now()
						st, hd, err := h.do(mkReq(path, tok, extra))
						if err != nil {
							errs.Add(1)
							return
						}
						wus, _ := strconv.ParseFloat(hd["x-root-wait-us"], 64)
						mu.Lock()
						recs = append(recs, reqRec{pi, id, vedge, j, float64(time.Since(t1).Microseconds()) / 1000, wus / 1000, hd["x-root-event"], st, iw})
						mu.Unlock()
					}
				}()
			}
			tw.Wait()
		}(pi, pp)
	}
	wg.Wait()
	wall := time.Since(start).Seconds()
	// edge stats
	var stats struct {
		Kids map[string]struct {
			Fetches        int64 `json:"fetches"`
			FetchBytes     int64 `json:"fetch_bytes"`
			StapleInstalls int64 `json:"staple_installs"`
			StapleBytes    int64 `json:"staple_bytes"`
			Coalesced      int64 `json:"coalesced"`
			SigVerifs      int64 `json:"sig_verifs"`
		} `json:"kids"`
	}
	if resp, err := http.Get("http://" + *target + "/stats"); err == nil {
		json.NewDecoder(resp.Body).Decode(&stats)
		resp.Body.Close()
	}
	if *reqOut != "" {
		f, _ := os.Create(*reqOut)
		fmt.Fprintln(f, "pipe,mode,lambda,tok,vedge,seq,lat_ms,root_wait_ms,event,status,issue_ms")
		for _, r := range recs {
			fmt.Fprintf(f, "%d,%s,%g,%d,%d,%d,%.3f,%.3f,%s,%d,%.3f\n", r.pipe, ps[r.pipe].mode, ps[r.pipe].lambda, r.tok, r.vedge, r.seq, r.latMs, r.waitMs, r.event, r.status, r.issueMs)
		}
		f.Close()
	}
	header := "mode,V,delta_s,lambda,run,tokens,requests,rejects,misses,coalesced_waits,miss_per_token,miss_lat_mean_ms,miss_lat_p99_ms,wait_all_mean_ms,wait_all_p99_ms,root_bytes,root_bytes_per_token,edge_sig_verifs,staple_upstream_bytes_per_token,issue_wait_mean_ms,issue_wait_p99_ms,req_lat_p50_ms,req_lat_p99_ms,errors,wall_s,net"
	for pi, pp := range ps {
		var nreq, rej, miss, coal int
		var missLat, waitAll, lat []float64
		for _, r := range recs {
			if r.pipe != pi {
				continue
			}
			nreq++
			if r.status != 200 {
				rej++
			}
			lat = append(lat, r.latMs)
			switch r.event {
			case "fetch", "staple":
				miss++
				missLat = append(missLat, r.waitMs)
				waitAll = append(waitAll, r.waitMs)
			case "coalesced":
				coal++
				waitAll = append(waitAll, r.waitMs)
			}
		}
		ks := stats.Kids[strconv.Itoa(pp.kid)]
		rb := ks.FetchBytes
		if pp.mode == "pull_staple" {
			rb = ks.StapleBytes
		}
		nt := ntok[pi]
		appendCSV(*out, header, fmt.Sprintf("%s,%d,%g,%g,%d,%d,%d,%d,%d,%d,%.5f,%.3f,%.3f,%.3f,%.3f,%d,%.1f,%d,%.1f,%.1f,%.1f,%.3f,%.3f,%d,%.1f,%s",
			pp.mode, *V, *deltaS, pp.lambda, *run, nt, nreq, rej, miss, coal, float64(miss)/float64(nt),
			mean(missLat), pct(missLat, 99), mean(waitAll), pct(waitAll, 99), rb, float64(rb)/float64(nt), ks.SigVerifs, float64(stapleUp[pi])/float64(nt),
			mean(issueWait[pi]), pct(issueWait[pi], 99), pct(lat, 50), pct(lat, 99), errs.Load(), wall, *netLabel))
	}
}

// ------------------------------------------------------------------ RTT probe

func rtt() {
	h, err := dial(*target)
	if err != nil {
		log.Fatal(err)
	}
	req := []byte("GET /ping HTTP/1.1\r\nHost: x\r\n\r\n")
	h.do(req)
	var xs []float64
	for i := 0; i < *n; i++ {
		t0 := time.Now()
		if _, _, err := h.do(req); err != nil {
			log.Fatal(err)
		}
		xs = append(xs, float64(time.Since(t0).Microseconds())/1000)
		time.Sleep(10 * time.Millisecond)
	}
	f, _ := os.OpenFile(*out, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	st, _ := f.Stat()
	if st.Size() == 0 {
		fmt.Fprintln(f, "path,run,sample,rtt_ms")
	}
	for i, x := range xs {
		fmt.Fprintf(f, "%s,%d,%d,%.3f\n", *scheme, *run, i, x)
	}
	f.Close()
	fmt.Printf("%s rtt p50=%.3f mean=%.3f p99=%.3f ms\n", *scheme, pct(xs, 50), mean(xs), pct(xs, 99))
}

func main() {
	flag.Parse()
	switch *mode {
	case "p1":
		p1()
	case "p2":
		p2()
	case "p3":
		p3()
	case "rtt":
		rtt()
	}
}
