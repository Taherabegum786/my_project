"""Real SLH-DSA signatures for hpackbytes (circl v1.6.1 has no SLH-DSA).
usage: python gen_slh.py slh_in.json slh_out.json   (pqcrypto 1.0.0)"""
import json, sys
from pqcrypto.sign import slh_dsa_sha2_128s, slh_dsa_sha2_128f

inp = json.load(open(sys.argv[1]))
claims = inp["claims"].encode()
root_msg = bytes.fromhex(inp["root_msg_hex"])
pk_s, sk_s = slh_dsa_sha2_128s.keygen()
pk_f, sk_f = slh_dsa_sha2_128f.keygen()
out = {
    "sig_128s_claims": slh_dsa_sha2_128s.sign(sk_s, claims, context=b"CDN-token").hex(),
    "sig_128f_claims": slh_dsa_sha2_128f.sign(sk_f, claims, context=b"CDN-token").hex(),
    "sig_128s_root": slh_dsa_sha2_128s.sign(sk_s, root_msg, context=b"EMBER-root").hex(),
}
for k, v in out.items():
    print(k, len(v) // 2, "bytes")
json.dump(out, open(sys.argv[2], "w"))
