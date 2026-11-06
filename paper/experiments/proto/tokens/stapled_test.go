package tokens

import "testing"

func TestStapled(t *testing.T) {
	k := DeriveKeys(20261105)
	c := Claims{URLPrefix: "/v/t1/", Expires: 2000000000, Tenant: 1}
	tok, st, err := SignStapled(k, c, 1, RandFill)
	if err != nil {
		t.Fatal(err)
	}
	c2, enc, ref, _, err := ParseStapled(tok)
	if err != nil || c2 != c {
		t.Fatal("parse", err)
	}
	if !VerifyStapled(k, ref, enc, st) {
		t.Fatal("valid staple rejected")
	}
	tok2, st2, _ := SignStapled(k, c, 1, RandFill)
	_, enc2, ref2, _, _ := ParseStapled(tok2)
	if VerifyStapled(k, ref2, enc2, st) || !VerifyStapled(k, ref2, enc2, st2) {
		t.Fatal("cross-token staple accepted")
	}
	c3 := c
	c3.Expires++
	if VerifyStapled(k, ref, c3.Enc(), st) {
		t.Fatal("modified claims accepted")
	}
}
