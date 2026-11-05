// issuer: EMBER issuer + root service (E8).
//
//   GET /issue?kid=K&tenant=T&prefix=/p/  -> body: token; header X-EMBER-Root: b64url(SR_e)
//        (held until the timer-Δ epoch containing the request closes)
//   GET /root/<kid>/<epoch>               -> SR_e bytes (immutable)
//   GET /ping, GET /stats
//
// -kids "kid:delta_ms[:alg],..." configures one timer-Δ epoch stream per kid (alg 1=ML-DSA-44,
// 5=hybrid Ed25519+ML-DSA-44; n=16). Empty epochs produce no root (and no epoch id).
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	"emberproto/tokens"
)

var (
	listen = flag.String("listen", ":9090", "listen address")
	seed   = flag.Uint64("seed", 20261105, "key seed")
	kids   = flag.String("kids", "1:1000", "kid:delta_ms[:alg],...")
	vmax   = flag.Int64("vmax", 3600, "V_max seconds")
)

type req struct {
	c    tokens.Claims
	t0   time.Time
	done chan result
}
type result struct {
	tok  string
	root string
}

type stream struct {
	kid     uint32
	deltaMs uint32
	alg     uint8
	mu      sync.Mutex
	q       []*req
	tStart  time.Time
	epoch   uint32
	signUs  []int64
	sizes   []int
}

type issuer struct {
	keys    *tokens.Keys
	streams map[uint32]*stream
	rmu     sync.RWMutex
	roots   map[[2]uint32][]byte
}

func (is *issuer) run(s *stream) {
	tick := time.NewTicker(time.Duration(s.deltaMs) * time.Millisecond)
	for now := range tick.C {
		s.mu.Lock()
		batch := s.q
		s.q = nil
		tStart := s.tStart
		s.tStart = now
		s.mu.Unlock()
		if len(batch) == 0 {
			continue
		}
		s.epoch++
		cs := make([]tokens.Claims, len(batch))
		exp := (tStart.UnixMilli()+int64(s.deltaMs))/1000 + *vmax
		for i, r := range batch {
			r.c.Expires = exp
			cs[i] = r.c
		}
		t1 := time.Now()
		sr, toks := tokens.IssueEpoch(is.keys, s.alg, s.kid, s.epoch, uint64(tStart.UnixMilli()), s.deltaMs, cs, tokens.RandFill)
		srb := sr.Marshal()
		el := time.Since(t1).Microseconds()
		is.rmu.Lock()
		is.roots[[2]uint32{s.kid, s.epoch}] = srb
		is.rmu.Unlock()
		s.mu.Lock()
		s.signUs = append(s.signUs, el)
		s.sizes = append(s.sizes, len(batch))
		s.mu.Unlock()
		rb := tokens.B64.EncodeToString(srb)
		for i, r := range batch {
			r.done <- result{toks[i], rb}
		}
	}
}

func (is *issuer) issue(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	kid, _ := strconv.Atoi(q.Get("kid"))
	s := is.streams[uint32(kid)]
	if s == nil {
		w.WriteHeader(404)
		return
	}
	ten, _ := strconv.Atoi(q.Get("tenant"))
	rq := &req{c: tokens.Claims{URLPrefix: q.Get("prefix"), Tenant: uint32(ten)}, t0: time.Now(), done: make(chan result, 1)}
	s.mu.Lock()
	s.q = append(s.q, rq)
	s.mu.Unlock()
	res := <-rq.done
	w.Header().Set("X-EMBER-Root", res.root)
	w.Header().Set("X-Issue-Wait-Us", strconv.FormatInt(time.Since(rq.t0).Microseconds(), 10))
	w.Write([]byte(res.tok))
}

func (is *issuer) root(w http.ResponseWriter, r *http.Request) {
	p := strings.Split(strings.TrimPrefix(r.URL.Path, "/root/"), "/")
	if len(p) != 2 {
		w.WriteHeader(400)
		return
	}
	k, _ := strconv.Atoi(p[0])
	e, _ := strconv.Atoi(p[1])
	is.rmu.RLock()
	b := is.roots[[2]uint32{uint32(k), uint32(e)}]
	is.rmu.RUnlock()
	if b == nil {
		w.WriteHeader(404)
		return
	}
	w.Header().Set("Cache-Control", fmt.Sprintf("public, max-age=%d, immutable", *vmax))
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Write(b)
}

func main() {
	flag.Parse()
	is := &issuer{keys: tokens.DeriveKeys(*seed), streams: map[uint32]*stream{}, roots: map[[2]uint32][]byte{}}
	for _, spec := range strings.Split(*kids, ",") {
		f := strings.Split(spec, ":")
		kid, _ := strconv.Atoi(f[0])
		d, _ := strconv.Atoi(f[1])
		alg := uint8(tokens.AlgMLDSA44)
		if len(f) > 2 { // signer id (1 = ML-DSA-44, 5 = hybrid)
			a, _ := strconv.Atoi(f[2])
			alg = uint8(a << 4)
		}
		s := &stream{kid: uint32(kid), deltaMs: uint32(d), alg: alg, tStart: time.Now()}
		is.streams[uint32(kid)] = s
		go is.run(s)
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/issue", is.issue)
	mux.HandleFunc("/root/", is.root)
	mux.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) { w.Write([]byte("pong")) })
	mux.HandleFunc("/stats", func(w http.ResponseWriter, r *http.Request) {
		out := map[string]interface{}{}
		for k, s := range is.streams {
			s.mu.Lock()
			out[strconv.Itoa(int(k))] = map[string]interface{}{"epochs": s.epoch, "epoch_us": s.signUs, "sizes": s.sizes}
			s.mu.Unlock()
		}
		json.NewEncoder(w).Encode(out)
	})
	srv := &http.Server{Addr: *listen, Handler: mux, IdleTimeout: 600 * time.Second}
	log.Printf("issuer on %s kids=%s", *listen, *kids)
	log.Fatal(srv.ListenAndServe())
}
