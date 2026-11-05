/* evp_sigbench.c - PRIMARY native timing source (OpenSSL 3.5.4 EVP API).
 *
 * usage: evp_sigbench <scheme> <op> <iters> <warmup> [raw_out.bin]
 *   scheme: ML-DSA-44 ML-DSA-65 ML-DSA-87 SLH-DSA-SHA2-128s SLH-DSA-SHA2-128f ED25519 ECDSA-P256 RSA-2048 ML-KEM-768
 *   op:     keygen sign verify   (ML-KEM-768: keygen encaps decaps)
 * Prints one CSV line: scheme,op,iters,median_us,p99_us,mean_us,sig_bytes,pk_bytes
 * Message: 200-byte claim string; ML-DSA/SLH-DSA use the FIPS 204/205 context string "EMBER-root".
 * Raw per-iteration samples (double, microseconds) are optionally written to raw_out.bin.
 */
#include <openssl/core_names.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/params.h>
#include <openssl/x509.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static double now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    return ts.tv_sec * 1e9 + ts.tv_nsec;
}
static int cmpd(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}
static void die(const char *m) {
    fprintf(stderr, "error: %s\n", m);
    ERR_print_errors_fp(stderr);
    exit(1);
}

static unsigned char MSG[200];
static const char *CTXSTR = "EMBER-root";

static EVP_PKEY *keygen(const char *scheme) {
    if (!strcmp(scheme, "ECDSA-P256")) return EVP_PKEY_Q_keygen(NULL, NULL, "EC", "P-256");
    if (!strcmp(scheme, "RSA-2048")) return EVP_PKEY_Q_keygen(NULL, NULL, "RSA", (size_t)2048);
    return EVP_PKEY_Q_keygen(NULL, NULL, scheme);
}
static int is_pq_sig(const char *s) { return !strncmp(s, "ML-DSA", 6) || !strncmp(s, "SLH-DSA", 7); }
static const char *mdname(const char *s) {
    return (!strcmp(s, "ECDSA-P256") || !strcmp(s, "RSA-2048")) ? "SHA256" : NULL;
}

static size_t do_sign(EVP_PKEY *k, const char *scheme, unsigned char *sig, size_t cap) {
    EVP_MD_CTX *m = EVP_MD_CTX_new();
    OSSL_PARAM p[2] = {OSSL_PARAM_END, OSSL_PARAM_END};
    if (is_pq_sig(scheme))
        p[0] = OSSL_PARAM_construct_octet_string(OSSL_SIGNATURE_PARAM_CONTEXT_STRING, (void *)CTXSTR, strlen(CTXSTR));
    if (EVP_DigestSignInit_ex(m, NULL, mdname(scheme), NULL, NULL, k, p) <= 0) die("signinit");
    size_t L = cap;
    if (EVP_DigestSign(m, sig, &L, MSG, sizeof MSG) <= 0) die("sign");
    EVP_MD_CTX_free(m);
    return L;
}
static int do_verify(EVP_PKEY *k, const char *scheme, const unsigned char *sig, size_t L) {
    EVP_MD_CTX *m = EVP_MD_CTX_new();
    OSSL_PARAM p[2] = {OSSL_PARAM_END, OSSL_PARAM_END};
    if (is_pq_sig(scheme))
        p[0] = OSSL_PARAM_construct_octet_string(OSSL_SIGNATURE_PARAM_CONTEXT_STRING, (void *)CTXSTR, strlen(CTXSTR));
    if (EVP_DigestVerifyInit_ex(m, NULL, mdname(scheme), NULL, NULL, k, p) <= 0) die("verifyinit");
    int r = EVP_DigestVerify(m, sig, L, MSG, sizeof MSG);
    EVP_MD_CTX_free(m);
    return r;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "usage: %s scheme op iters warmup [raw.bin]\n", argv[0]);
        return 2;
    }
    const char *scheme = argv[1], *op = argv[2];
    int iters = atoi(argv[3]), warm = atoi(argv[4]);
    for (size_t i = 0; i < sizeof MSG; i++) MSG[i] = 'a' + (i % 26);
    double *t = malloc(sizeof(double) * iters);
    EVP_PKEY *k = keygen(scheme);
    if (!k) die("keygen");
    size_t pklen = 0;
    EVP_PKEY_get_raw_public_key(k, NULL, &pklen);
    if (!pklen) pklen = i2d_PUBKEY(k, NULL); /* DER SPKI for EC/RSA */
    static unsigned char sig[65536], ct[4096], ss[64];
    size_t siglen = 0;
    int kem = !strcmp(scheme, "ML-KEM-768");
    EVP_PKEY_CTX *pc = EVP_PKEY_CTX_new_from_pkey(NULL, k, NULL);
    size_t ctlen = sizeof ct, sslen = sizeof ss;
    if (kem) {
        if (EVP_PKEY_encapsulate_init(pc, NULL) <= 0 || EVP_PKEY_encapsulate(pc, ct, &ctlen, ss, &sslen) <= 0) die("encaps");
        siglen = ctlen;
    } else {
        siglen = do_sign(k, scheme, sig, sizeof sig);
        if (do_verify(k, scheme, sig, siglen) != 1) die("selftest verify");
        sig[siglen / 2] ^= 1;
        if (do_verify(k, scheme, sig, siglen) == 1) die("selftest: tampered sig accepted");
        sig[siglen / 2] ^= 1;
    }
    for (int r = -warm; r < iters; r++) {
        double t0 = now_ns();
        if (!strcmp(op, "keygen")) {
            EVP_PKEY *kk = keygen(scheme);
            EVP_PKEY_free(kk);
        } else if (!strcmp(op, "sign")) {
            do_sign(k, scheme, sig, sizeof sig);
        } else if (!strcmp(op, "verify")) {
            if (do_verify(k, scheme, sig, siglen) != 1) die("verify");
        } else if (!strcmp(op, "encaps")) {
            EVP_PKEY_CTX *c = EVP_PKEY_CTX_new_from_pkey(NULL, k, NULL);
            size_t a = sizeof ct, b = sizeof ss;
            if (EVP_PKEY_encapsulate_init(c, NULL) <= 0 || EVP_PKEY_encapsulate(c, ct, &a, ss, &b) <= 0) die("encaps");
            EVP_PKEY_CTX_free(c);
        } else if (!strcmp(op, "decaps")) {
            EVP_PKEY_CTX *c = EVP_PKEY_CTX_new_from_pkey(NULL, k, NULL);
            size_t b = sizeof ss;
            if (EVP_PKEY_decapsulate_init(c, NULL) <= 0 || EVP_PKEY_decapsulate(c, ss, &b, ct, ctlen) <= 0) die("decaps");
            EVP_PKEY_CTX_free(c);
        } else
            die("bad op");
        double dt = (now_ns() - t0) / 1000.0;
        if (r >= 0) t[r] = dt;
    }
    if (argc > 5) {
        FILE *f = fopen(argv[5], "wb");
        fwrite(t, sizeof(double), iters, f);
        fclose(f);
    }
    double mean = 0;
    for (int i = 0; i < iters; i++) mean += t[i];
    mean /= iters;
    qsort(t, iters, sizeof(double), cmpd);
    double med = iters % 2 ? t[iters / 2] : 0.5 * (t[iters / 2 - 1] + t[iters / 2]);
    int i99 = (int)(0.99 * (iters - 1) + 0.5);
    printf("%s,%s,%d,%.3f,%.3f,%.3f,%zu,%zu\n", scheme, op, iters, med, t[i99], mean, siglen, pklen);
    return 0;
}
