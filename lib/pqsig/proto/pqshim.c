/* Flat C wrapper around liboqs signatures for ctypes (no struct layouts exposed to Python).
 * Build (run.sh): cc -O2 -shared -fPIC pqshim.c -I$PREFIX/include -Wl,--whole-archive $PREFIX/lib/liboqs.a
 *                 -Wl,--no-whole-archive -lcrypto -lpthread -o libpqshim.so                                  */
#include <oqs/oqs.h>
#include <stdint.h>
#include <stddef.h>

void pq_init(void) { OQS_init(); }
const char *pq_version(void) { return OQS_version(); }
int pq_enabled(const char *name) { return OQS_SIG_alg_is_enabled(name); }
void *pq_new(const char *name) { return OQS_SIG_new(name); }
void pq_free(void *s) { OQS_SIG_free((OQS_SIG *)s); }
size_t pq_pk_len(void *s) { return ((OQS_SIG *)s)->length_public_key; }
size_t pq_sk_len(void *s) { return ((OQS_SIG *)s)->length_secret_key; }
size_t pq_sig_len(void *s) { return ((OQS_SIG *)s)->length_signature; }
int pq_level(void *s) { return (int)((OQS_SIG *)s)->claimed_nist_level; }
int pq_keypair(void *s, uint8_t *pk, uint8_t *sk) { return OQS_SIG_keypair((OQS_SIG *)s, pk, sk) == OQS_SUCCESS; }
int pq_sign(void *s, uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk) {
    return OQS_SIG_sign((OQS_SIG *)s, sig, siglen, m, mlen, sk) == OQS_SUCCESS;
}
int pq_verify(void *s, const uint8_t *m, size_t mlen, const uint8_t *sig, size_t siglen, const uint8_t *pk) {
    return OQS_SIG_verify((OQS_SIG *)s, m, mlen, sig, siglen, pk) == OQS_SUCCESS;
}
