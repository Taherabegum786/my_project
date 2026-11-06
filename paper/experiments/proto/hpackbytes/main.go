// hpackbytes (E3b): upstream request-header bytes per session for each token scheme, measured with
// the real HTTP/2 HPACK encoder (golang.org/x/net/http2/hpack, 4096-B dynamic table, the encoder's
// default indexing policy) and as raw HTTP/1.1 bytes.
//
// Session = 1 manifest + K segment requests on one connection (fresh encoder per session).
// Placements: url (token in ?Token=, so :path changes every request), cookie (one Cookie header,
// same value every request), cookie2 (token split into two cookie crumbs, B5c/B6c-style; in
// HTTP/1.1 the crumbs are joined into one Cookie header).  EMBER also with the stapled root
// (X-EMBER-Root) on the first request.
//
//   hpackbytes -dump slh_in.json           # messages that need SLH-DSA signatures (python helper)
//   hpackbytes -slh slh_out.json -out wire_bytes.csv
package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"emberproto/tokens"

	"golang.org/x/net/http2/hpack"
)

var (
	dump   = flag.String("dump", "", "write SLH-DSA signing inputs to this JSON and exit")
	slhIn  = flag.String("slh", "", "JSON with SLH-DSA signatures (from gen_slh.py)")
	outCSV = flag.String("out", "wire_bytes.csv", "output CSV")
	K      = flag.Int("K", 150, "segment requests per session")
)

const prefix = "/v/t42/vod/8f3a2c91d0e4/1080p/" // 30 chars; segment paths ~48-60 chars

var claims = tokens.Claims{URLPrefix: prefix, Expires: 1893456000, Tenant: 42}

// Realistic browser-like request headers (besides :path / cookie / token).
var common = [][2]string{
	{"user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"},
	{"accept", "*/*"},
	{"accept-encoding", "gzip, deflate, br, zstd"},
	{"accept-language", "en-US,en;q=0.9"},
	{"origin", "https://www.example-video.com"},
	{"referer", "https://www.example-video.com/watch?v=8f3a2c91d0e4"},
	{"sec-fetch-dest", "empty"},
	{"sec-fetch-mode", "cors"},
	{"sec-fetch-site", "cross-site"},
	{"sec-ch-ua", "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\""},
	{"sec-ch-ua-mobile", "?0"},
	{"sec-ch-ua-platform", "\"Windows\""},
}

const authority = "cdn.example.com"

func segPath(j int) string {
	if j == 0 {
		return prefix + "master.m3u8"
	}
	return fmt.Sprintf("%sseg_%05d.m4s", prefix, j)
}

type tokCase struct {
	scheme     string
	token      string
	placements []string
	staple     string // b64url SR for the first request (EMBER only)
	stapleHdr  string // header name for the staple (default x-ember-root; R1 b5s: x-token-sig)
}

// request returns the header list of request j.
func request(tc tokCase, placement string, j int, withStaple bool) [][2]string {
	path := segPath(j)
	var h [][2]string
	if placement == "url" && tc.token != "" {
		path += "?Token=" + tc.token
	}
	h = append(h, [2]string{":method", "GET"}, [2]string{":scheme", "https"}, [2]string{":authority", authority}, [2]string{":path", path})
	h = append(h, common...)
	switch placement {
	case "cookie":
		h = append(h, [2]string{"cookie", "Edge-Token=" + tc.token})
	case "cookie2":
		half := len(tc.token) / 2
		h = append(h, [2]string{"cookie", "Edge-Token-1=" + tc.token[:half]}, [2]string{"cookie", "Edge-Token-2=" + tc.token[half:]})
	}
	if withStaple && j == 0 && tc.staple != "" {
		hn := "x-ember-root"
		if tc.stapleHdr != "" {
			hn = tc.stapleHdr
		}
		h = append(h, [2]string{hn, tc.staple})
	}
	return h
}

func h1Bytes(h [][2]string) int {
	var b strings.Builder
	var cookies []string
	for _, f := range h {
		switch f[0] {
		case ":method", ":scheme":
		case ":path":
			b.WriteString("GET " + f[1] + " HTTP/1.1\r\n")
		case ":authority":
			b.WriteString("Host: " + f[1] + "\r\n")
		case "cookie":
			cookies = append(cookies, f[1])
		default:
			b.WriteString(f[0] + ": " + f[1] + "\r\n")
		}
	}
	if len(cookies) > 0 {
		b.WriteString("cookie: " + strings.Join(cookies, "; ") + "\r\n")
	}
	b.WriteString("\r\n")
	return b.Len()
}

type row struct {
	scheme, placement, proto  string
	first, session, tokenLen int
}

func measure(tc tokCase, placement string, withStaple bool) []row {
	rs := measure1(tc, placement, withStaple, false, 4096)
	rs = append(rs, measure1(tc, placement, withStaple, true, 4096)[0])
	return append(rs, measure1(tc, placement, withStaple, false, 65536)[0])
}

// measure1: pathNoIndex=true marks :path as never-indexed (encoder-policy sensitivity variant).
func measure1(tc tokCase, placement string, withStaple bool, pathNoIndex bool, table uint32) []row {
	var buf bytes.Buffer
	enc := hpack.NewEncoder(&buf) // default 4096-byte dynamic table
	if table != 4096 {
		enc.SetMaxDynamicTableSizeLimit(table)
		enc.SetMaxDynamicTableSize(table)
	}
	var h2first, h2sum, h1first, h1sum int
	for j := 0; j <= *K; j++ {
		h := request(tc, placement, j, withStaple)
		buf.Reset()
		for _, f := range h {
			if err := enc.WriteField(hpack.HeaderField{Name: f[0], Value: f[1], Sensitive: pathNoIndex && f[0] == ":path"}); err != nil {
				log.Fatal(err)
			}
		}
		n1 := h1Bytes(h)
		if j == 0 {
			h2first, h1first = buf.Len(), n1
		}
		h2sum += buf.Len()
		h1sum += n1
	}
	name := tc.scheme
	if withStaple {
		name += "+staple"
	}
	if table != 4096 {
		return []row{{name, placement, "h2-hpack-t64k", h2first, h2sum, len(tc.token)}}
	}
	if pathNoIndex {
		return []row{{name, placement, "h2-hpack-pathnoindex", h2first, h2sum, len(tc.token)}}
	}
	return []row{{name, placement, "h2-hpack", h2first, h2sum, len(tc.token)}, {name, placement, "http1.1", h1first, h1sum, len(tc.token)}}
}

func main() {
	flag.Parse()
	k := tokens.DeriveKeys(20261105)
	enc := claims.Enc()
	// SR template for an EMBER root (message for SLH-DSA-128s root signature)
	srTmpl := &tokens.SignedRoot{Alg: tokens.AlgSLH128s, Kid: 1, Epoch: 7, TStartMs: 1893452400000, DeltaMs: 1000, N: 1 << 14}
	// NOTE: the O3 staple's tree root differs from srTmpl.R; only the SR length matters for header bytes,
	// and the SLH-DSA-128s signature is real (7856 B).
	srTmpl.R = make([]byte, 16)
	if *dump != "" {
		b, _ := json.MarshalIndent(map[string]string{"claims": enc, "root_msg_hex": hex.EncodeToString(srTmpl.Msg())}, "", " ")
		os.WriteFile(*dump, b, 0644)
		return
	}
	var slh map[string]string
	if *slhIn != "" {
		raw, err := os.ReadFile(*slhIn)
		if err != nil {
			log.Fatal(err)
		}
		json.Unmarshal(raw, &slh)
	}
	var cases []tokCase
	all := []string{"url", "cookie"}
	add := func(s, t string, pl []string) { cases = append(cases, tokCase{scheme: s, token: t, placements: pl}) }
	cases = append(cases, tokCase{scheme: "none", token: "", placements: []string{"url"}})
	for _, s := range []string{tokens.B1, tokens.B2, tokens.B3, tokens.B5, tokens.B6, tokens.B9, tokens.B11, tokens.B12} {
		t, err := tokens.SignPerToken(k, s, claims, 1)
		if err != nil {
			log.Fatal(err)
		}
		pl := all
		if s == tokens.B5 || s == tokens.B6 {
			add(s+"c", t, []string{"cookie2"})
		}
		add(s, t, pl)
	}
	for _, kk := range []int{1, 3, 10} {
		t, _ := tokens.SignPerToken(k, tokens.B10, claims, kk)
		add(fmt.Sprintf("b10k%d", kk), t, all)
	}
	if slh != nil {
		for _, s := range []struct{ name, key string }{{"b7", "sig_128s_claims"}, {"b8", "sig_128f_claims"}} {
			sig, err := hex.DecodeString(slh[s.key])
			if err != nil || len(sig) == 0 {
				log.Fatal("missing ", s.key)
			}
			add(s.name, enc+":Sig="+tokens.B64.EncodeToString(sig), all)
			if s.name == "b7" || s.name == "b8" {
				add(s.name+"c", enc+":Sig="+tokens.B64.EncodeToString(sig), []string{"cookie2"})
			}
		}
	}
	// EMBER tokens from real trees: O1 (ML-DSA-44 root, n=16), O2 (n=32), O3 (SLH-128s root), O4 (hybrid root)
	for _, cfg := range []struct {
		name  string
		alg   uint8
		log2N int
	}{{"o1_N2^0", tokens.AlgMLDSA44, 0}, {"o1_N2^5", tokens.AlgMLDSA44, 5}, {"o1_N2^8", tokens.AlgMLDSA44, 8},
		{"o1_N2^10", tokens.AlgMLDSA44, 10}, {"o1_N2^14", tokens.AlgMLDSA44, 14}, {"o1_N2^20", tokens.AlgMLDSA44, 20},
		{"o2_N2^14", tokens.AlgMLDSA44 | tokens.AlgN32, 14}, {"o4_N2^14", tokens.AlgHybrid, 14}, {"o3_N2^14", tokens.AlgSLH128s, 14}} {
		N := 1 << cfg.log2N
		cs := make([]tokens.Claims, N)
		for i := range cs {
			cs[i] = claims
		}
		signAlg := cfg.alg
		if cfg.alg == tokens.AlgSLH128s {
			signAlg = tokens.AlgMLDSA44 // tree/tokens identical; root signature replaced below by a real SLH-DSA-128s sig
		}
		sr, toks := tokens.IssueEpoch(k, signAlg, 1, 7, 1893452400000, 1000, cs, tokens.RandFill)
		t := toks[N/3]
		if cfg.alg == tokens.AlgSLH128s {
			if slh == nil {
				continue
			}
			// patch alg byte in the token blob (tree is independent of the root signer)
			_, _, b, _ := tokens.ParseEmber(t)
			b.Alg = tokens.AlgSLH128s
			t = tokens.EncodeEmber(claims, b)
			sr.Alg = tokens.AlgSLH128s
			sr.Sig, _ = hex.DecodeString(slh["sig_128s_root"])
		}
		tc := tokCase{scheme: cfg.name, token: t, placements: all, staple: tokens.B64.EncodeToString(sr.Marshal())}
		cases = append(cases, tc)
	}
	// R1 M2/B5s: stapled per-token ML-DSA-44 (short URL token; signature once per session in x-token-sig)
	if t, st, err := tokens.SignStapled(k, claims, 1, tokens.RandFill); err == nil {
		cases = append(cases, tokCase{scheme: tokens.B5s, token: t, placements: all, staple: st, stapleHdr: "x-token-sig"})
	} else {
		log.Fatal(err)
	}
	f, err := os.Create(*outCSV)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	fmt.Fprintln(f, "scheme,placement,proto,K,first_req_bytes,session_bytes,bytes_per_req_mean,token_bytes,encoder")
	emit := func(rs []row) {
		for _, r := range rs {
			fmt.Fprintf(f, "%s,%s,%s,%d,%d,%d,%.2f,%d,x/net-hpack-v0.38.0\n", r.scheme, r.placement, r.proto, *K, r.first, r.session,
				float64(r.session)/float64(*K+1), r.tokenLen)
		}
	}
	for _, tc := range cases {
		for _, pl := range tc.placements {
			emit(measure(tc, pl, false))
			if tc.staple != "" {
				emit(measure(tc, pl, true))
			}
		}
	}
	log.Printf("wrote %s (%d cases)", *outCSV, len(cases))
}
