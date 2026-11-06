package tokens

// R1 baseline M2 / B5s: stapled per-token ML-DSA-44 (mirrors experiments/baselines/stapled.py).
//   URL token  = claims ":S=" b64url(kid[4] | nonce[16])
//   staple     = b64url(ML-DSA-44 sig over "CDN-token-staple" | kid | nonce | claims), sent once per edge
//                connection in the X-Token-Sig header
// The edge caches H(ref | claims) (16 B) as verified until the claims expire.

import (
	"crypto/sha256"
	"encoding/binary"
	"errors"
	"strings"

	"github.com/cloudflare/circl/sign/mldsa/mldsa44"
)

const B5s = "b5s"

var ctxStaple = []byte("CDN-token-staple")

func stapleMsg(ref []byte, enc string) []byte {
	m := append(append([]byte{}, ctxStaple...), ref...)
	return append(m, enc...)
}

// SignStapled returns the URL token and the b64url staple (signature).
func SignStapled(k *Keys, c Claims, kid uint32, rnd func([]byte)) (string, string, error) {
	enc := c.Enc()
	ref := binary.BigEndian.AppendUint32(nil, kid)
	nonce := make([]byte, 16)
	rnd(nonce)
	ref = append(ref, nonce...)
	sig := make([]byte, mldsa44.SignatureSize)
	if err := mldsa44.SignTo(k.M44, stapleMsg(ref, enc), nil, true, sig); err != nil {
		return "", "", err
	}
	return enc + ":S=" + B64.EncodeToString(ref), B64.EncodeToString(sig), nil
}

// ParseStapled splits a B5s URL token into claims, encoded claims, the 20-B reference and the cache key.
func ParseStapled(tok string) (Claims, string, []byte, [16]byte, error) {
	var key [16]byte
	i := strings.LastIndex(tok, ":S=")
	if i < 0 {
		return Claims{}, "", nil, key, errors.New("no ref")
	}
	c, enc, extra, err := SplitToken(tok[:i])
	if err != nil || len(extra) != 0 {
		return c, "", nil, key, errors.New("bad claims")
	}
	ref, err := B64.DecodeString(tok[i+3:])
	if err != nil || len(ref) != 20 {
		return c, "", nil, key, errors.New("bad ref")
	}
	h := sha256.New()
	h.Write(ref)
	h.Write([]byte(enc))
	copy(key[:], h.Sum(nil))
	return c, enc, ref, key, nil
}

// VerifyStapled checks the stapled signature for (ref, enc).
func VerifyStapled(k *Keys, ref []byte, enc string, staple string) bool {
	sig, err := B64.DecodeString(staple)
	if err != nil || len(sig) != mldsa44.SignatureSize {
		return false
	}
	return mldsa44.Verify(k.M44Pub, stapleMsg(ref, enc), nil, sig)
}
