package main

// R2 mode p4: recovery behaviour of staple-per-connection schemes.
//   pipelines (-p4pipes "m2:200:11,ember:200:12"): M2 = stapled per-token ML-DSA-44 (b5s),
//   ember = EMBER staple-all (pooled tree, root stapled on the first request of every connection).
// Client: one connection per (session, edge); the first request of every connection carries the staple;
// with probability -pmove per request the session re-routes to another edge (new connection, staple again).
// Recovery: on 401 Staple-Required the client retries the same request with the staple on the same
// connection; on a broken connection (edge restart) it reconnects (every 20 ms, up to 10 s) and re-sends
// with the staple.  -event flush calls <edge>/admin/flush at -event-at (state loss, connections kept).

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"math"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

var (
	p4pipes  = flag.String("p4pipes", "m2:200:11,ember:200:12", "p4: scheme:lambda:kid,...  (scheme m2|ember)")
	pmove    = flag.Float64("pmove", 0.01, "p4: per-request probability of a mid-session re-route")
	tcut     = flag.Duration("tcut", 8*time.Second, "p4: stop sending requests this long after the issuance window")
	event    = flag.String("event", "none", "p4: none|flush|restart (restart is done by the run script; label only)")
	eventAt  = flag.Duration("event-at", 15*time.Second, "p4: time of the flush event (and label for restart)")
	scenario = flag.String("scenario", "cold", "p4: scenario label")
	reqLog   = flag.String("reqlog", "", "p4: per-request CSV")
)

type p4rec struct {
	pipe     int
	tok, seq int
	vedge    int
	tOffMs   float64
	latMs    float64
	extraMs  float64
	kind     string
	status   int
	staple   bool
	newConn  bool
}

// redial retries for up to 10 s (the edge may be restarting).
func redial() (*hconn, error) {
	t0 := time.Now()
	for {
		h, err := dial(*target)
		if err == nil || time.Since(t0) > 10*time.Second {
			return h, err
		}
		time.Sleep(20 * time.Millisecond)
	}
}

func p4() {
	type pipe struct {
		name   string
		lambda float64
		kid    int
	}
	var ps []pipe
	for _, f := range strings.Split(*p4pipes, ",") {
		x := strings.Split(f, ":")
		l, _ := strconv.ParseFloat(x[1], 64)
		k, _ := strconv.Atoi(x[2])
		ps = append(ps, pipe{x[0], l, k})
	}
	cdf := zipfCDF(*V, *alpha)
	ic := &http.Client{Timeout: 60 * time.Second, Transport: &http.Transport{MaxIdleConnsPerHost: 4096, MaxIdleConns: 4096, IdleConnTimeout: 600 * time.Second}}
	var mu sync.Mutex
	var recs []p4rec
	ntok := make([]int, len(ps))
	moves := make([]int64, len(ps))
	stapleBytes := make([]int64, len(ps))
	var issueErr, fails atomic.Int64
	start := time.Now()
	stopAt := start.Add(*dur + *tcut)
	if *event == "flush" {
		go func() {
			time.Sleep(time.Until(start.Add(*eventAt)))
			if resp, err := http.Get("http://" + *target + "/admin/flush"); err == nil {
				io.ReadAll(resp.Body)
				resp.Body.Close()
			}
		}()
	}
	var wg sync.WaitGroup
	for pi, pp := range ps {
		wg.Add(1)
		go func(pi int, pp pipe) {
			defer wg.Done()
			rng := rand.New(rand.NewSource(*seed + int64(1000**run) + int64(pi)))
			pathScheme := "b5s"
			if pp.name == "ember" {
				pathScheme = "o1"
			}
			next := start
			var tw sync.WaitGroup
			for id := 0; ; id++ {
				next = next.Add(time.Duration(rng.ExpFloat64() / pp.lambda * 1e9))
				if next.Sub(start) > *dur {
					break
				}
				time.Sleep(time.Until(next))
				vedge := sort.SearchFloat64s(cdf, rng.Float64())
				if vedge >= *V {
					vedge = *V - 1
				}
				firstDelay := time.Duration(*firstMed * math.Exp(*firstSig*rng.NormFloat64()) * 1e6)
				k := 1 + int(math.Floor(math.Log(1-rng.Float64())/math.Log(1-1 / *kmean)))
				srng := rand.New(rand.NewSource(rng.Int63()))
				tenant := 1 + rng.Intn(100)
				tw.Add(1)
				go func(id int) {
					defer tw.Done()
					q := url.Values{"kid": {strconv.Itoa(pp.kid)}, "tenant": {strconv.Itoa(tenant)},
						"prefix": {fmt.Sprintf("/%s/t%d/s%d/", pathScheme, pp.kid, id)}}
					resp, err := ic.Get(*issuerURL + "/issue?" + q.Encode())
					if err != nil {
						issueErr.Add(1)
						return
					}
					tb, _ := io.ReadAll(resp.Body)
					resp.Body.Close()
					tok := string(tb)
					var stapleHdr string
					if pp.name == "m2" {
						stapleHdr = "X-Token-Sig: " + resp.Header.Get("X-Token-Sig") + "\r\n"
					} else {
						stapleHdr = "X-EMBER-Root: " + resp.Header.Get("X-EMBER-Root") + "\r\n"
					}
					mu.Lock()
					ntok[pi]++
					mu.Unlock()
					time.Sleep(firstDelay)
					h, err := redial()
					if err != nil {
						fails.Add(1)
						return
					}
					defer func() {
						if h != nil {
							h.c.Close()
						}
					}()
					newConn := true
					seqStart := time.Now()
					var local []p4rec
					for j := 0; j <= k; j++ {
						if j > 0 {
							time.Sleep(time.Until(seqStart.Add(time.Duration(j) * *segIv)))
						}
						if time.Now().After(stopAt) {
							break
						}
						if j > 0 && srng.Float64() < *pmove { // mid-session re-route to another edge
							nv := vedge
							for nv == vedge && *V > 1 {
								nv = sort.SearchFloat64s(cdf, srng.Float64())
								if nv >= *V {
									nv = *V - 1
								}
							}
							vedge = nv
							h.c.Close()
							if h, err = redial(); err != nil {
								h = nil
								fails.Add(1)
								return
							}
							newConn = true
							atomic.AddInt64(&moves[pi], 1)
						}
						path := fmt.Sprintf("/%s/t%d/s%d/seg%05d.m4s", pathScheme, pp.kid, id, j)
						vh := fmt.Sprintf("X-VEdge: %d\r\n", pi*1000+vedge)
						extra := vh
						stapled := newConn
						if newConn {
							extra += stapleHdr
							atomic.AddInt64(&stapleBytes[pi], int64(len(stapleHdr)))
						}
						t1 := time.Now()
						st, _, err := h.do(mkReq(path, tok, extra))
						kind, extraMs := "ok", 0.0
						if err != nil { // connection broken (edge restart): reconnect, re-send with staple
							kind = "reconnect"
							tr := time.Now()
							h.c.Close()
							ok := false
							for time.Since(tr) < 10*time.Second {
								if h2, e2 := dial(*target); e2 == nil {
									h = h2
									atomic.AddInt64(&stapleBytes[pi], int64(len(stapleHdr)))
									if st, _, err = h.do(mkReq(path, tok, vh+stapleHdr)); err == nil {
										ok = true
										break
									}
									h.c.Close()
								}
								time.Sleep(20 * time.Millisecond)
							}
							if !ok {
								kind = "fail"
								fails.Add(1)
							}
							extraMs = float64(time.Since(tr).Microseconds()) / 1000
							stapled = true
						} else if st == 401 { // Staple-Required: retry on the same connection
							kind = "retry"
							tr := time.Now()
							atomic.AddInt64(&stapleBytes[pi], int64(len(stapleHdr)))
							st, _, err = h.do(mkReq(path, tok, vh+stapleHdr))
							extraMs = float64(time.Since(tr).Microseconds()) / 1000
							if err != nil || st != 200 {
								kind = "fail"
								fails.Add(1)
							}
							stapled = true
						}
						local = append(local, p4rec{pi, id, j, vedge, float64(t1.Sub(start).Microseconds()) / 1000,
							float64(time.Since(t1).Microseconds()) / 1000, extraMs, kind, st, stapled, newConn})
						if kind == "fail" {
							break
						}
						newConn = false
					}
					mu.Lock()
					recs = append(recs, local...)
					mu.Unlock()
				}(id)
			}
			tw.Wait()
		}(pi, pp)
	}
	wg.Wait()
	wall := time.Since(start).Seconds()
	var stats map[string]interface{}
	if resp, err := http.Get("http://" + *target + "/stats"); err == nil {
		dec := json.NewDecoder(resp.Body)
		dec.Decode(&stats)
		resp.Body.Close()
	}
	num := func(k string) float64 {
		if v, ok := stats[k].(float64); ok {
			return v
		}
		return math.NaN()
	}
	kidStaple := func(kid int) float64 {
		if ks, ok := stats["kids"].(map[string]interface{}); ok {
			if m, ok := ks[strconv.Itoa(kid)].(map[string]interface{}); ok {
				return m["staple_installs"].(float64)
			}
		}
		return math.NaN()
	}
	if *reqLog != "" {
		f, _ := os.Create(*reqLog)
		fmt.Fprintln(f, "pipe,tok,seq,vedge,t_off_ms,lat_ms,extra_ms,kind,status,stapled,new_conn")
		for _, r := range recs {
			fmt.Fprintf(f, "%s,%d,%d,%d,%.1f,%.3f,%.3f,%s,%d,%t,%t\n", ps[r.pipe].name, r.tok, r.seq, r.vedge, r.tOffMs, r.latMs, r.extraMs, r.kind, r.status, r.staple, r.newConn)
		}
		f.Close()
	}
	header := "scenario,scheme,V,lambda,run,pmove,tokens,requests,moves,new_conns,staple_hdr_bytes_per_token,retries,retries_per_1k_req,retry_extra_mean_ms,retry_extra_p99_ms,reconnects,reconnect_extra_mean_ms,reconnect_extra_p99_ms,fails,affected_frac,req_lat_p50_ms,req_lat_p99_ms,retried_req_lat_mean_ms,edge_verifs,edge_staple_required,edge_m2_evictions,edge_root_evictions,issue_errors,wall_s,net"
	for pi, pp := range ps {
		var n, nc, retr, reco, fl int
		var lat, rex, cex, rlat []float64
		for _, r := range recs {
			if r.pipe != pi {
				continue
			}
			n++
			lat = append(lat, r.latMs)
			if r.newConn {
				nc++
			}
			switch r.kind {
			case "retry":
				retr++
				rex = append(rex, r.extraMs)
				rlat = append(rlat, r.latMs)
			case "reconnect":
				reco++
				cex = append(cex, r.extraMs)
			case "fail":
				fl++
			}
		}
		ev := num("b5s_staple_verifs")
		if pp.name == "ember" {
			ev = kidStaple(pp.kid)
		}
		nt := float64(ntok[pi])
		appendCSV(*out, header, fmt.Sprintf("%s,%s,%d,%g,%d,%g,%d,%d,%d,%d,%.1f,%d,%.4f,%.3f,%.3f,%d,%.3f,%.3f,%d,%.6f,%.3f,%.3f,%.3f,%.0f,%.0f,%.0f,%.0f,%d,%.1f,%s",
			*scenario, pp.name, *V, pp.lambda, *run, *pmove, ntok[pi], n, moves[pi], nc, float64(stapleBytes[pi])/nt,
			retr, 1000*float64(retr)/float64(n), mean(rex), pct(rex, 99), reco, mean(cex), pct(cex, 99), fl,
			float64(retr+reco)/float64(n), pct(lat, 50), pct(lat, 99), mean(rlat), ev, num("staple_required"),
			num("m2_evictions"), num("root_evictions"), issueErr.Load(), wall, *netLabel))
	}
}
