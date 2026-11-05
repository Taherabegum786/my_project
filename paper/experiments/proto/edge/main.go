// edge: HTTP edge verifier for EMBER tokens and per-token baselines (E8).
//
// Request:  GET /<scheme>/<path...>?Token=<token>   (or Cookie: Edge-Token=<token>)
// Optional: X-VEdge: <int>  (virtual edge id; each has its own root cache)
//           X-EMBER-Root: <b64url SR>  (stapled signed root)
// Response headers: X-Root-Event (none|hit|fetch|coalesced|staple), X-Root-Wait-Us.
//
// Root cache: per (vedge, kid, epoch); singleflight (coalescing) per key; negative cache for
// failed fetches (TTL -negttl). Pull-on-miss fetches GET <origin>/root/<kid>/<epoch>.
package main

import (
	"crypto/sha256"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"emberproto/tokens"
)

var (
	listen   = flag.String("listen", ":8080", "listen address")
	origin   = flag.String("origin", "http://10.72.0.2:9090", "root service base URL")
	seed     = flag.Uint64("seed", 20261105, "key derivation seed")
	vmax     = flag.Int64("vmax", 3600, "V_max seconds")
	negTTL   = flag.Duration("negttl", 2*time.Second, "negative-cache TTL")
	reverify = flag.Int("reverify-every", 1000, "o1a: re-verify the root signature every N EMBER requests")
	bodyLen  = flag.Int("body", 64, "response body bytes")
	kidAlg   = flag.String("kidalg", "4:5", "kid:signer_id for root algorithms other than ML-DSA-44 (id 1); 5 = hybrid Ed25519+ML-DSA-44")
	tau      = flag.Int64("tau", 5, "clock-skew tolerance (s)")
	prewarm  = flag.Int("prewarm", 0, "open N keep-alive connections to the origin at start (persistent edge->origin connections)")
)

type rootKey struct {
	v     int
	kid   uint32
	epoch uint32
}

type rootEntry struct {
	done     chan struct{}
	sr       *tokens.SignedRoot
	err      error
	negUntil time.Time
}

type kidStats struct {
	Fetches        int64 `json:"fetches"`
	FetchBytes     int64 `json:"fetch_bytes"`
	FetchErrors    int64 `json:"fetch_errors"`
	StapleInstalls int64 `json:"staple_installs"`
	StapleBytes    int64 `json:"staple_bytes"`
	Coalesced      int64 `json:"coalesced"`
	SigVerifs      int64 `json:"sig_verifs"`
	Requests       int64 `json:"requests"`
}

type server struct {
	keys     *tokens.Keys
	ver      *tokens.Verifier
	mu       sync.Mutex
	roots    map[rootKey]*rootEntry
	vcacheMu sync.Mutex
	vcache   map[[32]byte]int64
	statsMu  sync.Mutex
	stats    map[uint32]*kidStats
	reqs     atomic.Int64
	rejects  atomic.Int64
	vhits    atomic.Int64
	vmiss    atomic.Int64
	emberCtr atomic.Int64
	client   *http.Client
	body     []byte
}

func (s *server) ks(kid uint32) *kidStats {
	s.statsMu.Lock()
	defer s.statsMu.Unlock()
	st := s.stats[kid]
	if st == nil {
		st = &kidStats{}
		s.stats[kid] = st
	}
	return st
}

var kidAlgs = map[uint32]uint8{}

func algFor(kid uint32) uint8 {
	if a, ok := kidAlgs[kid]; ok {
		return a
	}
	return tokens.AlgMLDSA44
}

func (s *server) fetchRoot(kid, e uint32) (*tokens.SignedRoot, int, error) {
	resp, err := s.client.Get(fmt.Sprintf("%s/root/%d/%d", *origin, kid, e))
	if err != nil {
		return nil, 0, err
	}
	defer resp.Body.Close()
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, 0, err
	}
	if resp.StatusCode != 200 {
		return nil, len(b), fmt.Errorf("root status %d", resp.StatusCode)
	}
	sr, err := tokens.UnmarshalRoot(b, algFor(kid))
	return sr, len(b), err
}

// getRoot returns the verified root for (v,kid,e) plus event and wait time.
func (s *server) getRoot(v int, kid, e uint32, staple string) (*tokens.SignedRoot, string, time.Duration, error) {
	t0 := time.Now()
	k := rootKey{v, kid, e}
	s.mu.Lock()
	ent := s.roots[k]
	if ent != nil {
		s.mu.Unlock()
		select {
		case <-ent.done:
			if ent.err == nil {
				return ent.sr, "hit", 0, nil
			}
			if time.Now().Before(ent.negUntil) {
				return nil, "neg", 0, ent.err
			}
			s.mu.Lock()
			if s.roots[k] == ent {
				delete(s.roots, k)
			}
			s.mu.Unlock()
			return s.getRoot(v, kid, e, staple)
		default:
			<-ent.done
			atomic.AddInt64(&s.ks(kid).Coalesced, 1)
			return ent.sr, "coalesced", time.Since(t0), ent.err
		}
	}
	ent = &rootEntry{done: make(chan struct{})}
	s.roots[k] = ent
	s.mu.Unlock()
	st := s.ks(kid)
	event := "fetch"
	var sr *tokens.SignedRoot
	var err error
	if staple != "" {
		event = "staple"
		var raw []byte
		raw, err = tokens.B64.DecodeString(staple)
		if err == nil {
			sr, err = tokens.UnmarshalRoot(raw, algFor(kid))
		}
		atomic.AddInt64(&st.StapleInstalls, 1)
		atomic.AddInt64(&st.StapleBytes, int64(len(raw)))
	} else {
		var n int
		sr, n, err = s.fetchRoot(kid, e)
		atomic.AddInt64(&st.Fetches, 1)
		atomic.AddInt64(&st.FetchBytes, int64(n))
		if err != nil {
			atomic.AddInt64(&st.FetchErrors, 1)
		}
	}
	if err == nil {
		if sr.Kid != kid || sr.Epoch != e {
			err = fmt.Errorf("root kid/epoch mismatch")
		} else {
			atomic.AddInt64(&st.SigVerifs, 1)
			if !tokens.VerifyRoot(s.keys, sr) {
				err = fmt.Errorf("root signature invalid")
			}
		}
	}
	if err != nil {
		ent.err = err
		ent.negUntil = time.Now().Add(*negTTL)
	} else {
		ent.sr = sr
	}
	close(ent.done)
	return sr, event, time.Since(t0), err
}

func (s *server) installRoot(v int, sr *tokens.SignedRoot) error {
	if !tokens.VerifyRoot(s.keys, sr) {
		return fmt.Errorf("bad root sig")
	}
	ent := &rootEntry{done: make(chan struct{}), sr: sr}
	close(ent.done)
	s.mu.Lock()
	s.roots[rootKey{v, sr.Kid, sr.Epoch}] = ent
	s.mu.Unlock()
	return nil
}

func (s *server) deny(w http.ResponseWriter, why string) {
	s.rejects.Add(1)
	w.Header().Set("X-Reject", why)
	w.WriteHeader(403)
}

func (s *server) handle(w http.ResponseWriter, r *http.Request) {
	s.reqs.Add(1)
	path := r.URL.Path
	if len(path) < 2 {
		w.WriteHeader(404)
		return
	}
	sl := strings.IndexByte(path[1:], '/')
	if sl < 0 {
		w.WriteHeader(404)
		return
	}
	scheme := path[1 : 1+sl]
	tok := r.URL.Query().Get("Token")
	if tok == "" {
		if c, err := r.Cookie("Edge-Token"); err == nil {
			tok = c.Value
		}
	}
	if tok == "" {
		s.deny(w, "no token")
		return
	}
	now := time.Now()
	event, wait := "none", time.Duration(0)
	var c tokens.Claims
	switch scheme {
	case "o1", "o1a", "o4":
		var enc string
		var b tokens.EmberBlob
		var err error
		c, enc, b, err = tokens.ParseEmber(tok)
		if err != nil {
			s.deny(w, "parse")
			return
		}
		v := 0
		if hv := r.Header.Get("X-VEdge"); hv != "" {
			v, _ = strconv.Atoi(hv)
		}
		if b.Alg&^tokens.AlgN32 != algFor(b.Kid) {
			s.deny(w, "alg")
			return
		}
		st := s.ks(b.Kid)
		atomic.AddInt64(&st.Requests, 1)
		var sr *tokens.SignedRoot
		sr, event, wait, err = s.getRoot(v, b.Kid, b.Epoch, r.Header.Get("X-EMBER-Root"))
		if err != nil {
			s.deny(w, "root:"+err.Error())
			return
		}
		if c.Expires*1000 > int64(sr.TStartMs)+int64(sr.DeltaMs)+(*vmax+*tau)*1000 {
			s.deny(w, "expires beyond epoch window")
			return
		}
		if !tokens.VerifyEmberPath(c, enc, b, sr) {
			s.deny(w, "path")
			return
		}
		if scheme == "o1a" && s.emberCtr.Add(1)%int64(*reverify) == 0 {
			// amortised cold-cache cost: one root-signature verification per N requests
			if !tokens.VerifyRoot(s.keys, sr) {
				s.deny(w, "root")
				return
			}
		}
	case tokens.B5v:
		h := sha256.Sum256([]byte(tok))
		s.vcacheMu.Lock()
		exp, ok := s.vcache[h]
		s.vcacheMu.Unlock()
		if ok && exp >= now.Unix() {
			s.vhits.Add(1)
			var err error
			c, _, _, err = tokens.SplitToken(tok[:strings.LastIndex(tok, ":Sig=")])
			if err != nil {
				s.deny(w, "parse")
				return
			}
			event = "vcache-hit"
			break
		}
		s.vmiss.Add(1)
		var err error
		c, err = s.ver.VerifyPerToken(scheme, tok)
		if err != nil {
			s.deny(w, err.Error())
			return
		}
		s.vcacheMu.Lock()
		if len(s.vcache) > 1<<21 {
			s.vcache = map[[32]byte]int64{}
		}
		s.vcache[h] = c.Expires
		s.vcacheMu.Unlock()
	default:
		var err error
		c, err = s.ver.VerifyPerToken(scheme, tok)
		if err != nil {
			s.deny(w, err.Error())
			return
		}
	}
	if now.Unix() > c.Expires+*tau {
		s.deny(w, "expired")
		return
	}
	if !strings.HasPrefix(path, c.URLPrefix) {
		s.deny(w, "prefix")
		return
	}
	h := w.Header()
	h.Set("X-Root-Event", event)
	h.Set("X-Root-Wait-Us", strconv.FormatInt(wait.Microseconds(), 10))
	h.Set("Content-Length", strconv.Itoa(len(s.body)))
	w.Write(s.body)
}

func (s *server) admin(w http.ResponseWriter, r *http.Request) {
	b, _ := io.ReadAll(r.Body)
	var err error
	switch r.URL.Path {
	case "/admin/root":
		var sr *tokens.SignedRoot
		kid, _ := strconv.Atoi(r.URL.Query().Get("kid"))
		sr, err = tokens.UnmarshalRoot(b, algFor(uint32(kid)))
		if err == nil {
			v, _ := strconv.Atoi(r.URL.Query().Get("v"))
			err = s.installRoot(v, sr)
		}
	case "/admin/deleg":
		id, pk, _, e := tokens.VerifyDelegCert(s.keys.M44Pub, b)
		err = e
		if err == nil {
			s.ver.DelegPub[id] = pk
		}
	case "/admin/kem":
		e, ke, e2 := tokens.UnwrapEpochKey(s.keys.EdgeKEM, b)
		err = e2
		if err == nil {
			s.ver.EpochK[e] = ke
		}
	default:
		err = fmt.Errorf("unknown admin")
	}
	if err != nil {
		w.WriteHeader(400)
		fmt.Fprintln(w, err)
		return
	}
	fmt.Fprintln(w, "ok")
}

func (s *server) statsH(w http.ResponseWriter, r *http.Request) {
	s.statsMu.Lock()
	out := map[string]interface{}{"requests": s.reqs.Load(), "rejects": s.rejects.Load(),
		"vcache_hits": s.vhits.Load(), "vcache_miss": s.vmiss.Load()}
	kids := map[string]kidStats{}
	for k, v := range s.stats {
		kids[strconv.Itoa(int(k))] = kidStats{atomic.LoadInt64(&v.Fetches), atomic.LoadInt64(&v.FetchBytes),
			atomic.LoadInt64(&v.FetchErrors), atomic.LoadInt64(&v.StapleInstalls), atomic.LoadInt64(&v.StapleBytes),
			atomic.LoadInt64(&v.Coalesced), atomic.LoadInt64(&v.SigVerifs), atomic.LoadInt64(&v.Requests)}
	}
	s.statsMu.Unlock()
	out["kids"] = kids
	json.NewEncoder(w).Encode(out)
}

func main() {
	flag.Parse()
	for _, kv := range strings.Split(*kidAlg, ",") {
		if f := strings.Split(kv, ":"); len(f) == 2 {
			kd, _ := strconv.Atoi(f[0])
			a, _ := strconv.Atoi(f[1])
			kidAlgs[uint32(kd)] = uint8(a << 4)
		}
	}
	k := tokens.DeriveKeys(*seed)
	s := &server{keys: k, ver: tokens.NewVerifier(k), roots: map[rootKey]*rootEntry{},
		vcache: map[[32]byte]int64{}, stats: map[uint32]*kidStats{}, body: make([]byte, *bodyLen)}
	s.client = &http.Client{Timeout: 5 * time.Second, Transport: &http.Transport{
		MaxIdleConns: 256, MaxIdleConnsPerHost: 256, IdleConnTimeout: 600 * time.Second,
		DialContext: (&net.Dialer{Timeout: 3 * time.Second, KeepAlive: 30 * time.Second}).DialContext}}
	if *prewarm > 0 {
		var wg sync.WaitGroup
		for i := 0; i < *prewarm; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				if resp, err := s.client.Get(*origin + "/ping"); err == nil {
					io.ReadAll(resp.Body)
					resp.Body.Close()
				}
			}()
		}
		wg.Wait()
		log.Printf("prewarmed %d origin connections", *prewarm)
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) { w.Write([]byte("pong")) })
	mux.HandleFunc("/stats", s.statsH)
	mux.HandleFunc("/admin/", s.admin)
	mux.HandleFunc("/", s.handle)
	srv := &http.Server{Addr: *listen, Handler: mux, MaxHeaderBytes: 1 << 16, ReadHeaderTimeout: 30 * time.Second,
		IdleTimeout: 600 * time.Second}
	log.Printf("edge listening on %s origin=%s", *listen, *origin)
	log.Fatal(srv.ListenAndServe())
}
