package main

// R2 additions: bounded LRU caches per virtual edge, 401 Staple-Required recovery hint,
// EMBER miss policy (pull or 401), and /admin/flush (state loss with connections kept open).

import (
	"container/list"
	"flag"
	"net/http"
	"sync/atomic"
)

var (
	scacheCap    = flag.Int("scache-cap", 0, "M2/b5s verified-entry cache capacity per virtual edge (LRU); 0 = unbounded")
	rcacheCap    = flag.Int("rcache-cap", 0, "EMBER verified-root cache capacity per virtual edge (LRU); 0 = unbounded")
	emberMiss    = flag.String("ember-miss", "pull", "EMBER root miss without a staple: pull (fetch from origin) or 401 (Staple-Required)")
	stapleStatus = flag.Int("staple-status", 401, "status for a missing staple: 401 (R2) or 403 (R1 behaviour)")
)

type lru[K comparable] struct {
	cap int
	ll  *list.List
	m   map[K]*list.Element
}

func newLRU[K comparable](c int) *lru[K] { return &lru[K]{cap: c, ll: list.New(), m: map[K]*list.Element{}} }

// touch marks k most recently used (inserting it) and returns the evicted keys.
func (l *lru[K]) touch(k K) []K {
	if e, ok := l.m[k]; ok {
		l.ll.MoveToFront(e)
		return nil
	}
	l.m[k] = l.ll.PushFront(k)
	var ev []K
	for l.cap > 0 && l.ll.Len() > l.cap {
		b := l.ll.Back()
		kk := b.Value.(K)
		l.ll.Remove(b)
		delete(l.m, kk)
		ev = append(ev, kk)
	}
	return ev
}

type skey struct {
	v int
	k [16]byte
}

type r2state struct {
	s401      atomic.Int64 // Staple-Required answers
	sEvict    atomic.Int64 // M2 entries evicted by the LRU
	rEvict    atomic.Int64 // EMBER roots evicted by the LRU
	flushes   atomic.Int64
	scacheLRU map[int]*lru[[16]byte] // guarded by scacheMu
	rootLRU   map[int]*lru[rootKey]  // guarded by mu
}

type errStapleRequired struct{}

func (errStapleRequired) Error() string { return "staple required" }

func (s *server) stapleRequired(w http.ResponseWriter, kind string) {
	s.r2.s401.Add(1)
	s.rejects.Add(1)
	w.Header().Set("X-Reject", "staple required")
	w.Header().Set("Staple-Required", kind)
	w.Header().Set("Content-Length", "0")
	w.WriteHeader(*stapleStatus)
}

// rootTouch records a verified root for LRU purposes; caller holds s.mu.
func (s *server) rootTouchLocked(k rootKey) {
	if *rcacheCap <= 0 {
		return
	}
	l := s.r2.rootLRU[k.v]
	if l == nil {
		l = newLRU[rootKey](*rcacheCap)
		s.r2.rootLRU[k.v] = l
	}
	for _, ev := range l.touch(k) {
		delete(s.roots, ev)
		s.r2.rEvict.Add(1)
	}
}

// scacheGet / scachePut: M2 verified-entry cache per virtual edge.
func (s *server) scacheGet(v int, key [16]byte, now int64) bool {
	s.scacheMu.Lock()
	defer s.scacheMu.Unlock()
	exp, ok := s.scache[skey{v, key}]
	if ok && exp >= now {
		if *scacheCap > 0 {
			s.r2.scacheLRU[v].touch(key)
		}
		return true
	}
	return false
}

func (s *server) scachePut(v int, key [16]byte, exp int64) {
	s.scacheMu.Lock()
	defer s.scacheMu.Unlock()
	if *scacheCap <= 0 && len(s.scache) > 1<<21 {
		s.scache = map[skey]int64{}
	}
	s.scache[skey{v, key}] = exp
	if *scacheCap > 0 {
		l := s.r2.scacheLRU[v]
		if l == nil {
			l = newLRU[[16]byte](*scacheCap)
			s.r2.scacheLRU[v] = l
		}
		for _, ev := range l.touch(key) {
			delete(s.scache, skey{v, ev})
			s.r2.sEvict.Add(1)
		}
	}
}

func (s *server) flush(w http.ResponseWriter, r *http.Request) {
	s.mu.Lock()
	s.roots = map[rootKey]*rootEntry{}
	s.r2.rootLRU = map[int]*lru[rootKey]{}
	s.mu.Unlock()
	s.scacheMu.Lock()
	s.scache = map[skey]int64{}
	s.r2.scacheLRU = map[int]*lru[[16]byte]{}
	s.scacheMu.Unlock()
	s.vcacheMu.Lock()
	s.vcache = map[[32]byte]int64{}
	s.vcacheMu.Unlock()
	s.r2.flushes.Add(1)
	w.Write([]byte("flushed\n"))
}
