// h2probe (R1, reviewer M3/Q3): which HPACK dynamic-table size do real HTTP/2 clients use for REQUEST headers
// when the server (the HPACK decoder for requests) advertises SETTINGS_HEADER_TABLE_SIZE = -table?
//
// Minimal HTTP/2 server on raw frames (golang.org/x/net/http2 Framer): sends SETTINGS with HEADER_TABLE_SIZE,
// records for every request the HPACK header-block length (HEADERS + CONTINUATION payload bytes) and any
// dynamic-table-size update the client emits, decodes it with a decoder of the advertised size, and answers.
//   GET /           -> HTML page that sets a cookie of -cookie bytes and fetch()es /seg/<i> -n times sequentially
//   GET /seg/<i>    -> 204-like tiny 200 response
//   GET /done       -> writes the CSV row summary and exits
// TLS (self-signed) with ALPN h2 for browsers; -h2c for prior-knowledge cleartext clients (curl, Go).
package main

import (
	"bufio"
	"bytes"
	"context"
	"net/http"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"flag"
	"fmt"
	"io"
	"log"
	"math/big"
	"net"
	"os"
	"strings"
	"sync"
	"time"

	"golang.org/x/net/http2"
	"golang.org/x/net/http2/hpack"
)

var (
	addr    = flag.String("addr", "127.0.0.1:8443", "listen")
	table   = flag.Uint("table", 65536, "advertised SETTINGS_HEADER_TABLE_SIZE")
	h2c     = flag.Bool("h2c", false, "cleartext prior-knowledge HTTP/2 instead of TLS")
	n       = flag.Int("n", 150, "segment fetches the page performs")
	cookieN = flag.Int("cookie", 3311, "cookie value bytes set by the page")
	client  = flag.String("client", "", "client label for the CSV")
	out     = flag.String("out", "", "append CSV rows here")
	rawOut  = flag.String("raw", "", "append per-request rows here")
	goCli   = flag.Bool("goclient", false, "also run a Go x/net/http2 client (default Transport settings) against -h2c")
)

type rec struct {
	path       string
	blockBytes int
	sizeUpd    []uint32
	cookieLen  int
}

var (
	mu   sync.Mutex
	recs []rec
	done = make(chan struct{})
)

func page() []byte {
	val := strings.Repeat("A", *cookieN)
	// pseudo-random base64url-like content so Huffman behaves like a real token
	b := []byte(val)
	const al = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
	rb := make([]byte, len(b))
	rand.Read(rb)
	for i := range b {
		b[i] = al[int(rb[i])%64]
	}
	return []byte(fmt.Sprintf(`<!doctype html><html><body><script>
document.cookie = "Edge-Token=%s; path=/; Secure";
(async () => { for (let i = 0; i < %d; i++) { await fetch("/seg/" + i, {cache: "no-store"}); }
  await fetch("/done", {cache: "no-store"}); document.title = "done"; })();
</script></body></html>`, string(b), *n))
}

func serve(c net.Conn) {
	defer c.Close()
	br := bufio.NewReader(c)
	pre := make([]byte, len(http2.ClientPreface))
	if _, err := io.ReadFull(br, pre); err != nil || string(pre) != http2.ClientPreface {
		return
	}
	fr := http2.NewFramer(c, br)
	fr.WriteSettings(http2.Setting{ID: http2.SettingHeaderTableSize, Val: uint32(*table)},
		http2.Setting{ID: http2.SettingMaxConcurrentStreams, Val: 100})
	var cur *rec
	var sizes []uint32
	dec := hpack.NewDecoder(uint32(*table), nil)
	dec.SetEmitFunc(func(f hpack.HeaderField) {
		if f.Name == ":path" {
			cur.path = f.Value
		}
		if f.Name == "cookie" {
			cur.cookieLen += len(f.Value)
		}
	})
	var block bytes.Buffer
	var encBuf bytes.Buffer
	enc := hpack.NewEncoder(&encBuf)
	pg := page()
	for {
		f, err := fr.ReadFrame()
		if err != nil {
			return
		}
		switch f := f.(type) {
		case *http2.SettingsFrame:
			if !f.IsAck() {
				fr.WriteSettingsAck()
			}
		case *http2.PingFrame:
			if !f.IsAck() {
				fr.WritePing(true, f.Data)
			}
		case *http2.HeadersFrame, *http2.ContinuationFrame:
			var frag []byte
			var end bool
			var sid uint32
			if h, ok := f.(*http2.HeadersFrame); ok {
				frag, end, sid = h.HeaderBlockFragment(), h.HeadersEnded(), h.StreamID
				block.Reset()
				cur = &rec{}
				sizes = nil
			} else {
				cf := f.(*http2.ContinuationFrame)
				frag, end, sid = cf.HeaderBlockFragment(), cf.HeadersEnded(), cf.StreamID
			}
			block.Write(frag)
			if !end {
				continue
			}
			// detect dynamic table size updates at the start of the block (RFC 7541 §6.3: 001xxxxx)
			bb := block.Bytes()
			for len(bb) > 0 && bb[0]&0xe0 == 0x20 {
				v, rest := readInt(bb, 5)
				sizes = append(sizes, v)
				bb = rest
			}
			cur.blockBytes = block.Len()
			cur.sizeUpd = sizes
			if _, err := dec.Write(block.Bytes()); err != nil {
				log.Printf("hpack decode error: %v", err)
				return
			}
			if err := dec.Close(); err != nil {
				log.Printf("hpack close error: %v", err)
				return
			}
			mu.Lock()
			recs = append(recs, *cur)
			mu.Unlock()
			body := []byte("ok")
			ct := "text/plain"
			if cur.path == "/" {
				body, ct = pg, "text/html"
			}
			encBuf.Reset()
			enc.WriteField(hpack.HeaderField{Name: ":status", Value: "200"})
			enc.WriteField(hpack.HeaderField{Name: "content-type", Value: ct})
			enc.WriteField(hpack.HeaderField{Name: "cache-control", Value: "no-store"})
			fr.WriteHeaders(http2.HeadersFrameParam{StreamID: sid, BlockFragment: encBuf.Bytes(), EndHeaders: true})
			fr.WriteData(sid, true, body)
			if strings.HasPrefix(cur.path, "/done") {
				go func() { time.Sleep(200 * time.Millisecond); close(done) }()
			}
		}
	}
}

func goClient() {
	tr := &http2.Transport{AllowHTTP: true, DialTLSContext: func(ctx context.Context, network, a string, _ *tls.Config) (net.Conn, error) {
		return net.Dial(network, a)
	}}
	cl := &http.Client{Transport: tr}
	ck := string(page()[len("<!doctype html><html><body><script>\ndocument.cookie = \"Edge-Token="):])
	ck = ck[:*cookieN]
	get := func(p string) {
		req, _ := http.NewRequest("GET", "http://"+*addr+p, nil)
		req.Header.Set("Cookie", "Edge-Token="+ck)
		resp, err := cl.Do(req)
		if err != nil {
			log.Fatal(err)
		}
		io.ReadAll(resp.Body)
		resp.Body.Close()
	}
	for i := 0; i < *n; i++ {
		get(fmt.Sprintf("/seg/%d", i))
	}
	get("/done")
}

func readInt(b []byte, nbits uint) (uint32, []byte) {
	m := uint32(1)<<nbits - 1
	v := uint32(b[0]) & m
	b = b[1:]
	if v < m {
		return v, b
	}
	var s uint
	for len(b) > 0 {
		c := b[0]
		b = b[1:]
		v += uint32(c&0x7f) << s
		s += 7
		if c&0x80 == 0 {
			break
		}
	}
	return v, b
}

func selfSigned() tls.Certificate {
	k, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	t := &x509.Certificate{SerialNumber: big.NewInt(1), Subject: pkix.Name{CommonName: "localhost"},
		DNSNames: []string{"localhost"}, IPAddresses: []net.IP{net.ParseIP("127.0.0.1")},
		NotBefore: time.Now().Add(-time.Hour), NotAfter: time.Now().Add(24 * time.Hour)}
	der, _ := x509.CreateCertificate(rand.Reader, t, t, &k.PublicKey, k)
	return tls.Certificate{Certificate: [][]byte{der}, PrivateKey: k}
}

func main() {
	flag.Parse()
	var ln net.Listener
	var err error
	if *h2c {
		ln, err = net.Listen("tcp", *addr)
	} else {
		ln, err = tls.Listen("tcp", *addr, &tls.Config{Certificates: []tls.Certificate{selfSigned()}, NextProtos: []string{"h2"}})
	}
	if err != nil {
		log.Fatal(err)
	}
	go func() {
		for {
			c, err := ln.Accept()
			if err != nil {
				return
			}
			go serve(c)
		}
	}()
	if *goCli {
		go goClient()
	}
	select {
	case <-done:
	case <-time.After(120 * time.Second):
		log.Print("timeout")
	}
	mu.Lock()
	defer mu.Unlock()
	var segs []rec
	var upd []string
	for _, r := range recs {
		if len(r.sizeUpd) > 0 {
			upd = append(upd, fmt.Sprint(r.sizeUpd))
		}
		if strings.HasPrefix(r.path, "/seg/") {
			segs = append(segs, r)
		}
	}
	if len(segs) == 0 {
		log.Fatal("no segment requests seen")
	}
	first, sum := segs[0].blockBytes, 0
	for _, r := range segs {
		sum += r.blockBytes
	}
	steady := 0
	for _, r := range segs[len(segs)/2:] {
		steady += r.blockBytes
	}
	steadyMean := float64(steady) / float64(len(segs)-len(segs)/2)
	row := fmt.Sprintf("%s,%d,%d,%d,%d,%d,%.1f,%d,%s", *client, *table, *cookieN, len(segs), first, sum, steadyMean,
		segs[len(segs)-1].cookieLen, strings.Join(upd, "|"))
	fmt.Println("client,advertised_table,cookie_value_bytes,seg_requests,first_seg_block_bytes,seg_block_bytes_total,steady_block_bytes_mean,cookie_len_seen,table_size_updates")
	fmt.Println(row)
	if *out != "" {
		newf := false
		if _, err := os.Stat(*out); err != nil {
			newf = true
		}
		f, _ := os.OpenFile(*out, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if newf {
			fmt.Fprintln(f, "client,advertised_table,cookie_value_bytes,seg_requests,first_seg_block_bytes,seg_block_bytes_total,steady_block_bytes_mean,cookie_len_seen,table_size_updates")
		}
		fmt.Fprintln(f, row)
		f.Close()
	}
	if *rawOut != "" {
		f, _ := os.OpenFile(*rawOut, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		for i, r := range segs {
			fmt.Fprintf(f, "%s,%d,%d,%d,%d\n", *client, *table, i, r.blockBytes, r.cookieLen)
		}
		f.Close()
	}
}
