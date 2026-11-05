// Feasibility probe: Go 1.24 stdlib crypto/mlkem timings and a loopback
// TLS 1.3 handshake negotiating X25519MLKEM768 (ECDSA P-256 certificate;
// Go 1.24 stdlib has no ML-DSA certificates).
// Usage: go run . [iterations]
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/mlkem"
	"crypto/rand"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"fmt"
	"math/big"
	"net"
	"os"
	"sort"
	"strconv"
	"time"
)

func median(d []time.Duration) float64 {
	sort.Slice(d, func(i, j int) bool { return d[i] < d[j] })
	return float64(d[len(d)/2].Nanoseconds()) / 1000.0
}

func main() {
	n := 2000
	if len(os.Args) > 1 {
		n, _ = strconv.Atoi(os.Args[1])
	}
	// ML-KEM-768 / 1024 timings
	kg, en, de := make([]time.Duration, n), make([]time.Duration, n), make([]time.Duration, n)
	for i := 0; i < n; i++ {
		t := time.Now()
		dk, _ := mlkem.GenerateKey768()
		kg[i] = time.Since(t)
		ek := dk.EncapsulationKey()
		t = time.Now()
		_, ct := ek.Encapsulate()
		en[i] = time.Since(t)
		t = time.Now()
		dk.Decapsulate(ct)
		de[i] = time.Since(t)
	}
	fmt.Printf("go,ML-KEM-768,keygen,%d,%.2f\n", n, median(kg))
	fmt.Printf("go,ML-KEM-768,encaps,%d,%.2f\n", n, median(en))
	fmt.Printf("go,ML-KEM-768,decaps,%d,%.2f\n", n, median(de))
	for i := 0; i < n; i++ {
		t := time.Now()
		dk, _ := mlkem.GenerateKey1024()
		kg[i] = time.Since(t)
		ek := dk.EncapsulationKey()
		t = time.Now()
		_, ct := ek.Encapsulate()
		en[i] = time.Since(t)
		t = time.Now()
		dk.Decapsulate(ct)
		de[i] = time.Since(t)
	}
	fmt.Printf("go,ML-KEM-1024,keygen,%d,%.2f\n", n, median(kg))
	fmt.Printf("go,ML-KEM-1024,encaps,%d,%.2f\n", n, median(en))
	fmt.Printf("go,ML-KEM-1024,decaps,%d,%.2f\n", n, median(de))

	// Self-signed ECDSA cert
	key, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	tmpl := &x509.Certificate{SerialNumber: big.NewInt(1), Subject: pkix.Name{CommonName: "localhost"},
		DNSNames: []string{"localhost"}, NotBefore: time.Now().Add(-time.Hour), NotAfter: time.Now().Add(time.Hour)}
	der, _ := x509.CreateCertificate(rand.Reader, tmpl, tmpl, &key.PublicKey, key)
	cert := tls.Certificate{Certificate: [][]byte{der}, PrivateKey: key}
	ln, err := tls.Listen("tcp", "127.0.0.1:0", &tls.Config{Certificates: []tls.Certificate{cert}, MinVersion: tls.VersionTLS13})
	if err != nil {
		panic(err)
	}
	go func() {
		for {
			c, err := ln.Accept()
			if err != nil {
				return
			}
			go func(c net.Conn) { c.(*tls.Conn).Handshake(); c.Close() }(c)
		}
	}()
	pool := x509.NewCertPool()
	pc, _ := x509.ParseCertificate(der)
	pool.AddCert(pc)
	for _, g := range []struct {
		name string
		cp   []tls.CurveID
	}{{"X25519MLKEM768", []tls.CurveID{tls.X25519MLKEM768}}, {"X25519", []tls.CurveID{tls.X25519}}} {
		m := 300
		hs := make([]time.Duration, m)
		for i := 0; i < m; i++ {
			t := time.Now()
			c, err := tls.Dial("tcp", ln.Addr().String(), &tls.Config{RootCAs: pool, ServerName: "localhost", CurvePreferences: g.cp, MinVersion: tls.VersionTLS13})
			if err != nil {
				panic(err)
			}
			hs[i] = time.Since(t)
			c.Close()
		}
		fmt.Printf("go-tls,%s,handshake_loopback,%d,%.2f,only_group_offered\n", g.name, m, median(hs))
	}
}
