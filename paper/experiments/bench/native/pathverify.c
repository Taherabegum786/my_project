/* pathverify.c - native EMBER edge verification cost (OpenSSL 3.5.4 libcrypto, EVP SHA-256, prefetched).
 *
 * usage: pathverify <iters_per_point> <batch>
 * For every d in 0..24 and n in {16,32}: times full path verification
 *   leaf = Th(tweak26, r16 || claims200) ; d x node = Th(tweak26, left||right) ; constant-time compare to root.
 * Also: HMAC-SHA256 over the 200-B claims (EVP_MAC, key set once, re-init per op), and one Th call
 * on 64-B and 200-B inputs.
 * usage: pathverify <iters> <batch> [impl]   impl = evp (EVP_Digest*, prefetched MD; default) or
 *        ll (low-level SHA256_Init/Update/Final; HMAC with precomputed ipad/opad SHA256 states).
 * Output CSV (stdout): impl,op,d,n,iters,ns_per_op_median,ns_per_op_p99   (distribution over per-batch means)
 */
#include <openssl/core_names.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>
#include <openssl/params.h>
#include <openssl/sha.h>
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

static EVP_MD *SHA;
static EVP_MD_CTX *MC;
static int LL = 0;
static const char *IMPL = "evp";

static void tw(unsigned char *t, unsigned kid, unsigned ep, unsigned char typ, unsigned char lvl, unsigned idx, unsigned ten) {
    memcpy(t, "EMBERv1\0", 8);
    unsigned v[2] = {kid, ep};
    for (int k = 0; k < 2; k++) {
        t[8 + 4 * k] = v[k] >> 24; t[9 + 4 * k] = v[k] >> 16; t[10 + 4 * k] = v[k] >> 8; t[11 + 4 * k] = v[k];
    }
    t[16] = typ; t[17] = lvl;
    t[18] = idx >> 24; t[19] = idx >> 16; t[20] = idx >> 8; t[21] = idx;
    t[22] = ten >> 24; t[23] = ten >> 16; t[24] = ten >> 8; t[25] = ten;
}
static inline void th(const unsigned char *t, const unsigned char *a, size_t al, const unsigned char *b, size_t bl,
                      unsigned char *out, int n) {
    unsigned char d[32];
    if (LL) {
        SHA256_CTX c;
        SHA256_Init(&c);
        SHA256_Update(&c, t, 26);
        SHA256_Update(&c, a, al);
        if (bl) SHA256_Update(&c, b, bl);
        SHA256_Final(d, &c);
        memcpy(out, d, n);
        return;
    }
    EVP_DigestInit_ex2(MC, SHA, NULL);
    EVP_DigestUpdate(MC, t, 26);
    EVP_DigestUpdate(MC, a, al);
    if (bl) EVP_DigestUpdate(MC, b, bl);
    EVP_DigestFinal_ex(MC, d, NULL);
    memcpy(out, d, n);
}

static unsigned char CLAIMS[200], R[16], PATH[24][32], ROOT[32];
static volatile int sink;

/* verify with the same structure as ember/edge.py (power-of-two tree, leaf index idx) */
static int verify(int d, int n, unsigned idx) {
    unsigned char t[26], x[32], buf[64];
    tw(t, 1, 5, 0, 0, idx, 7);
    th(t, R, 16, CLAIMS, 200, x, n);
    unsigned i = idx;
    for (int l = 0; l < d; l++) {
        tw(t, 1, 5, 1, l + 1, i >> 1, 0);
        if (i & 1) { memcpy(buf, PATH[l], n); memcpy(buf + n, x, n); }
        else { memcpy(buf, x, n); memcpy(buf + n, PATH[l], n); }
        th(t, buf, 2 * n, NULL, 0, x, n);
        i >>= 1;
    }
    return CRYPTO_memcmp(x, ROOT, n) == 0;
}

static void report(const char *op, int d, int n, long iters, double *bt, int nb) {
    qsort(bt, nb, sizeof(double), cmpd);
    double med = nb % 2 ? bt[nb / 2] : 0.5 * (bt[nb / 2 - 1] + bt[nb / 2]);
    int i99 = (int)(0.99 * (nb - 1) + 0.5);
    printf("%s,%s,%d,%d,%ld,%.2f,%.2f\n", IMPL, op, d, n, iters, med, bt[i99]);
    fflush(stdout);
}

int main(int argc, char **argv) {
    long iters = argc > 1 ? atol(argv[1]) : 1000000;
    int batch = argc > 2 ? atoi(argv[2]) : 1000;
    if (argc > 3 && !strcmp(argv[3], "ll")) { LL = 1; IMPL = "ll"; }
    int nb = iters / batch;
    double *bt = malloc(sizeof(double) * nb);
    SHA = EVP_MD_fetch(NULL, "SHA256", NULL);
    MC = EVP_MD_CTX_new();
    for (int i = 0; i < 200; i++) CLAIMS[i] = 'a' + i % 26;
    for (int i = 0; i < 16; i++) R[i] = i * 7;
    int ds[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    int ns[] = {16, 32};
    printf("impl,op,d,n,iters,ns_per_op_median,ns_per_op_p99\n");
    for (int a = 0; a < 2; a++) {
        int n = ns[a];
        for (int b = 0; b < (int)(sizeof ds / sizeof ds[0]); b++) {
            int d = ds[b];
            unsigned idx = d ? (0x5A5A5A5Au & ((1u << d) - 1)) : 0;
            /* build PATH and the matching ROOT */
            unsigned char t[26], x[32], buf[64];
            for (int l = 0; l < d; l++) for (int k = 0; k < 32; k++) PATH[l][k] = (unsigned char)(l * 31 + k);
            tw(t, 1, 5, 0, 0, idx, 7);
            th(t, R, 16, CLAIMS, 200, x, n);
            unsigned i = idx;
            for (int l = 0; l < d; l++) {
                tw(t, 1, 5, 1, l + 1, i >> 1, 0);
                if (i & 1) { memcpy(buf, PATH[l], n); memcpy(buf + n, x, n); }
                else { memcpy(buf, x, n); memcpy(buf + n, PATH[l], n); }
                th(t, buf, 2 * n, NULL, 0, x, n);
                i >>= 1;
            }
            memcpy(ROOT, x, n);
            if (!verify(d, n, idx)) { fprintf(stderr, "selftest failed\n"); return 1; }
            PATH[0][0] ^= d ? 1 : 0; CLAIMS[0] ^= d ? 0 : 1;
            if (verify(d, n, idx)) { fprintf(stderr, "tamper selftest failed\n"); return 1; }
            PATH[0][0] ^= d ? 1 : 0; CLAIMS[0] ^= d ? 0 : 1;
            for (int w = 0; w < 2000; w++) sink += verify(d, n, idx);
            for (int k = 0; k < nb; k++) {
                double t0 = now_ns();
                for (int j = 0; j < batch; j++) sink += verify(d, n, idx);
                bt[k] = (now_ns() - t0) / batch;
            }
            report("pathverify", d, n, iters, bt, nb);
        }
    }
    /* single Th calls */
    unsigned char t[26], x[32], in[200];
    memset(in, 3, sizeof in);
    tw(t, 1, 2, 1, 1, 0, 0);
    int lens[] = {64, 200};
    for (int a = 0; a < 2; a++)
        for (int b = 0; b < 2; b++) {
            for (int k = 0; k < nb; k++) {
                double t0 = now_ns();
                for (int j = 0; j < batch; j++) { th(t, in, lens[b], NULL, 0, x, ns[a]); sink += x[0]; }
                bt[k] = (now_ns() - t0) / batch;
            }
            char nm[32];
            snprintf(nm, sizeof nm, "th_%dB", lens[b]);
            report(nm, 0, ns[a], iters, bt, nb);
        }
    /* SHA-256 over whole tokens (verified-token cache key, B5v/B6v/O1v): 400 B (EMBER), 3500 B (B5), 4700 B (B6) */
    {
        static unsigned char big[4800];
        unsigned char dg[32];
        memset(big, 'x', sizeof big);
        int tl[] = {400, 3500, 4700};
        for (int a = 0; a < 3; a++) {
            for (int k = 0; k < nb; k++) {
                double t0 = now_ns();
                for (int j = 0; j < batch; j++) {
                    if (LL) { SHA256_CTX c; SHA256_Init(&c); SHA256_Update(&c, big, tl[a]); SHA256_Final(dg, &c); }
                    else { EVP_DigestInit_ex2(MC, SHA, NULL); EVP_DigestUpdate(MC, big, tl[a]); EVP_DigestFinal_ex(MC, dg, NULL); }
                    sink += dg[0];
                }
                bt[k] = (now_ns() - t0) / batch;
            }
            char nm[32];
            snprintf(nm, sizeof nm, "sha256_%dB", tl[a]);
            report(nm, 0, 32, iters, bt, nb);
        }
    }
    /* HMAC-SHA256 over 200-B claims */
    EVP_MAC *mac = EVP_MAC_fetch(NULL, "HMAC", NULL);
    EVP_MAC_CTX *mc = EVP_MAC_CTX_new(mac);
    unsigned char key[32] = {1}, tag[32], ref[32];
    OSSL_PARAM p[2] = {OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_DIGEST, "SHA256", 0), OSSL_PARAM_END};
    EVP_MAC_init(mc, key, 32, p);
    size_t L;
    EVP_MAC_update(mc, CLAIMS, 200);
    EVP_MAC_final(mc, ref, &L, 32);
    for (int k = 0; k < nb; k++) {
        double t0 = now_ns();
        for (int j = 0; j < batch; j++) {
            EVP_MAC_init(mc, NULL, 0, NULL);
            EVP_MAC_update(mc, CLAIMS, 200);
            EVP_MAC_final(mc, tag, &L, 32);
            sink += CRYPTO_memcmp(tag, ref, 32);
        }
        bt[k] = (now_ns() - t0) / batch;
    }
    if (LL) { /* precomputed inner/outer states, as an optimised edge would keep per key */
        unsigned char ip[64], op_[64];
        memset(ip, 0x36, 64); memset(op_, 0x5c, 64);
        for (int i = 0; i < 32; i++) { ip[i] ^= key[i]; op_[i] ^= key[i]; }
        SHA256_CTX ci, co, c;
        SHA256_Init(&ci); SHA256_Update(&ci, ip, 64);
        SHA256_Init(&co); SHA256_Update(&co, op_, 64);
        unsigned char in_[32];
        c = ci; SHA256_Update(&c, CLAIMS, 200); SHA256_Final(in_, &c);
        c = co; SHA256_Update(&c, in_, 32); SHA256_Final(tag, &c);
        if (CRYPTO_memcmp(tag, ref, 32)) { fprintf(stderr, "hmac ll mismatch\n"); return 1; }
        for (int k = 0; k < nb; k++) {
            double t0 = now_ns();
            for (int j = 0; j < batch; j++) {
                c = ci; SHA256_Update(&c, CLAIMS, 200); SHA256_Final(in_, &c);
                c = co; SHA256_Update(&c, in_, 32); SHA256_Final(tag, &c);
                sink += CRYPTO_memcmp(tag, ref, 32);
            }
            bt[k] = (now_ns() - t0) / batch;
        }
    }
    report("hmac_sha256_200B", 0, 32, iters, bt, nb);
    return 0;
}
