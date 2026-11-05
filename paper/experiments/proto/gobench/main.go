// gobench: per-operation cost of the Go prototype's crypto (go-1.24.7 stdlib + circl-1.6.1), one process
// per run; run pinned (taskset -c 1).  Appends rows op,impl,run,n_iter,median_us,p99_us,mean_us.
package main

import (
	"flag"
	"fmt"
	"os"
	"sort"
	"time"

	"emberproto/tokens"
)

var (
	run   = flag.Int("run", 1, "run index")
	iters = flag.Int("n", 2000, "iterations")
	out   = flag.String("out", "proto_go_verify.csv", "CSV")
)

func timeit(name string, n int, f func(i int)) {
	for i := 0; i < 200; i++ {
		f(i)
	}
	xs := make([]float64, n)
	for i := 0; i < n; i++ {
		t0 := time.Now()
		f(i)
		xs[i] = float64(time.Since(t0).Nanoseconds()) / 1000
	}
	m := 0.0
	for _, x := range xs {
		m += x
	}
	m /= float64(n)
	sort.Float64s(xs)
	_, err := os.Stat(*out)
	fh, _ := os.OpenFile(*out, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if os.IsNotExist(err) {
		fmt.Fprintln(fh, "op,impl,run,n_iter,median_us,p99_us,mean_us")
	}
	fmt.Fprintf(fh, "%s,go-1.24.7+circl-1.6.1,%d,%d,%.3f,%.3f,%.3f\n", name, *run, n, xs[n/2], xs[n*99/100], m)
	fh.Close()
}

func main() {
	flag.Parse()
	k := tokens.DeriveKeys(20261105)
	v := tokens.NewVerifier(k)
	_, pk, _, _ := tokens.VerifyDelegCert(k.M44Pub, tokens.MakeDelegCert(k, 1, 1893456000))
	v.DelegPub[1] = pk
	_, ke, _ := tokens.UnwrapEpochKey(k.EdgeKEM, tokens.WrapEpochKey(k.EdgeKEM.EncapsulationKey(), 1, tokens.EpochKey(k, 1)))
	v.EpochK[1] = ke
	c := tokens.Claims{URLPrefix: "/v/t42/vod/8f3a2c91d0e4/1080p/", Expires: 1893456000, Tenant: 42}
	for _, s := range []string{"b1", "b2", "b3", "b5", "b6", "b9", "b11", "b12"} {
		tok, _ := tokens.SignPerToken(k, s, c, 1)
		timeit("verify_token_"+s, *iters, func(int) {
			if _, err := v.VerifyPerToken(s, tok); err != nil {
				panic(err)
			}
		})
	}
	for _, alg := range []struct {
		name string
		a    uint8
	}{{"mldsa44", tokens.AlgMLDSA44}, {"hybrid", tokens.AlgHybrid}} {
		cs := make([]tokens.Claims, 1<<14)
		for i := range cs {
			cs[i] = c
		}
		sr, toks := tokens.IssueEpoch(k, alg.a, 1, 7, 1893452400000, 1000, cs, tokens.RandFill)
		srb := sr.Marshal()
		timeit("verify_root_"+alg.name, *iters, func(int) {
			s2, _ := tokens.UnmarshalRoot(srb, alg.a)
			if !tokens.VerifyRoot(k, s2) {
				panic("root")
			}
		})
		if alg.a == tokens.AlgMLDSA44 {
			timeit("sign_root_mldsa44", *iters/4, func(int) { tokens.SignRoot(k, sr) })
			timeit("ember_verify_token_N2^14", *iters, func(i int) {
				cl, enc, b, err := tokens.ParseEmber(toks[i%len(toks)])
				if err != nil || !tokens.VerifyEmberPath(cl, enc, b, sr) {
					panic("path")
				}
			})
			for _, N := range []int{1024, 16384} {
				timeit(fmt.Sprintf("issue_epoch_N%d", N), 20, func(int) {
					tokens.IssueEpoch(k, alg.a, 1, 8, 0, 1000, cs[:N], tokens.RandFill)
				})
			}
		}
	}
	for _, s := range []string{"b5", "b2", "b3"} {
		timeit("sign_token_"+s, *iters/4, func(int) { tokens.SignPerToken(k, s, c, 1) })
	}
}
