package tokens

import (
	"crypto/mlkem"
	"strings"
	"testing"
)

func claims(i int) Claims {
	return Claims{URLPrefix: "/v/t7/video" + string(rune('a'+i%26)) + "/", Expires: 1893456000, Tenant: 7}
}

func flip(s string, pos int) string {
	b := []byte(s)
	if b[pos] == 'A' {
		b[pos] = 'B'
	} else {
		b[pos] = 'A'
	}
	return string(b)
}

func TestEmberRoundTripAndNegatives(t *testing.T) {
	k := DeriveKeys(20261105)
	for _, alg := range []uint8{AlgMLDSA44, AlgMLDSA44 | AlgN32, AlgHybrid} {
		for _, N := range []int{1, 2, 3, 5, 8, 1000, 1025} {
			cs := make([]Claims, N)
			for i := range cs {
				cs[i] = claims(i)
			}
			sr, toks := IssueEpoch(k, alg, 42, 9, 1000, 1000, cs, RandFill)
			sr2, err := UnmarshalRoot(sr.Marshal(), alg)
			if err != nil || !VerifyRoot(k, sr2) {
				t.Fatalf("root verify N=%d", N)
			}
			for i, tok := range toks {
				c, enc, b, err := ParseEmber(tok)
				if err != nil || !VerifyEmberPath(c, enc, b, sr2) {
					t.Fatalf("verify N=%d i=%d", N, i)
				}
			}
			// negatives on the last token
			tok := toks[N-1]
			c, enc, b, _ := ParseEmber(tok)
			bad := b
			bad.Idx = b.Idx ^ 1
			if N > 1 && VerifyEmberPath(c, enc, bad, sr2) {
				t.Fatal("index flip accepted")
			}
			bad = b
			bad.Idx = uint32(N)
			if VerifyEmberPath(c, enc, bad, sr2) {
				t.Fatal("idx>=N accepted")
			}
			bad = b
			bad.R = append([]byte{}, b.R...)
			bad.R[0] ^= 1
			if VerifyEmberPath(c, enc, bad, sr2) {
				t.Fatal("salt flip accepted")
			}
			if len(b.Path) > 0 {
				bad = b
				bad.Path = append([]byte{}, b.Path...)
				bad.Path[len(bad.Path)-1] ^= 1
				if VerifyEmberPath(c, enc, bad, sr2) {
					t.Fatal("path flip accepted")
				}
			}
			c8 := c
			c8.Tenant = 8
			if VerifyEmberPath(c8, c8.Enc(), b, sr2) || VerifyEmberPath(c8, enc, b, sr2) {
				t.Fatal("cross-tenant accepted")
			}
			bad = b
			bad.Epoch = 10
			if VerifyEmberPath(c, enc, bad, sr2) {
				t.Fatal("epoch swap accepted")
			}
			bad = b
			bad.Kid = 43
			if VerifyEmberPath(c, enc, bad, sr2) {
				t.Fatal("kid swap accepted")
			}
			sr3 := *sr2
			sr3.Kid = 43
			if VerifyRoot(k, &sr3) {
				t.Fatal("root under other kid accepted")
			}
			sr3 = *sr2
			sr3.Sig = append([]byte{}, sr2.Sig...)
			sr3.Sig[len(sr3.Sig)-1] ^= 1
			if VerifyRoot(k, &sr3) {
				t.Fatal("tampered root sig accepted")
			}
			if alg == AlgHybrid {
				sr3.Sig = append([]byte{}, sr2.Sig...)
				sr3.Sig[0] ^= 1
				if VerifyRoot(k, &sr3) {
					t.Fatal("hybrid ed half tampered accepted")
				}
			}
		}
	}
}

func TestPerToken(t *testing.T) {
	k := DeriveKeys(20261105)
	v := NewVerifier(k)
	_, pk, _, err := VerifyDelegCert(k.M44Pub, MakeDelegCert(k, 3, 1893456000))
	if err != nil {
		t.Fatal(err)
	}
	v.DelegPub[3] = pk
	ek := k.EdgeKEM.EncapsulationKey()
	e, ke, err := UnwrapEpochKey(k.EdgeKEM, WrapEpochKey(ek, 11, EpochKey(k, 11)))
	if err != nil || e != 11 {
		t.Fatal("unwrap", err)
	}
	v.EpochK[11] = ke
	_ = mlkem.CiphertextSize768
	for _, s := range []string{B1, B2, B3, B5, B6, B9, B10, B11, B12} {
		aux := 3
		if s == B12 {
			aux = 11
		}
		tok, err := SignPerToken(k, s, claims(1), aux)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := v.VerifyPerToken(s, tok); err != nil {
			t.Fatalf("%s valid rejected: %v", s, err)
		}
		if _, err := v.VerifyPerToken(s, strings.Replace(tok, "Tenant=7", "Tenant=8", 1)); err == nil {
			t.Fatalf("%s tampered claims accepted", s)
		}
		i := strings.LastIndex(tok, ":Sig=") + 8
		if _, err := v.VerifyPerToken(s, flip(tok, i)); err == nil {
			t.Fatalf("%s tampered sig accepted", s)
		}
	}
	// B12 wrong epoch key
	tok, _ := SignPerToken(k, B12, claims(1), 12)
	if _, err := v.VerifyPerToken(B12, tok); err == nil {
		t.Fatal("B12 unknown epoch accepted")
	}
	// B11 non-certified key
	tok, _ = SignPerToken(k, B11, claims(1), 4)
	if _, err := v.VerifyPerToken(B11, tok); err == nil {
		t.Fatal("B11 uncertified accepted")
	}
}

