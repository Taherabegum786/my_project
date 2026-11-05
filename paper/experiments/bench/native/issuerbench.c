/* issuerbench.c - native EMBER issuer cost per epoch (OpenSSL 3.5.4): leaf hashing, tree build,
 * one root signature (EVP), token encoding (path extraction + base64url + claims string).
 * usage: issuerbench <root_alg> <N> <reps> [n]
 * root_alg: ML-DSA-44 | ML-DSA-65 | SLH-DSA-SHA2-128s | SLH-DSA-SHA2-128f | ED25519
 * prints: alg,N,n,reps,t_leaf_us,t_tree_us,t_sign_us,t_encode_us,t_epoch_us,tokens_per_s  (medians over reps)
 */
#include <openssl/core_names.h>
#include <openssl/evp.h>
#include <openssl/params.h>
#include <openssl/rand.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static double now_us(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC_RAW, &t); return t.tv_sec * 1e6 + t.tv_nsec / 1e3; }
static int cmpd(const void *a, const void *b) { double x = *(double *)a, y = *(double *)b; return (x > y) - (x < y); }
static EVP_MD *SHA; static EVP_MD_CTX *MC;
static void tw(unsigned char *t, unsigned ep, int typ, int lvl, unsigned idx, unsigned ten) {
    memcpy(t, "EMBERv1\0", 8);
    unsigned v[4] = {1, ep, idx, ten};
    t[8] = 0; t[9] = 0; t[10] = 0; t[11] = 1;
    t[12] = ep >> 24; t[13] = ep >> 16; t[14] = ep >> 8; t[15] = ep;
    t[16] = typ; t[17] = lvl;
    t[18] = idx >> 24; t[19] = idx >> 16; t[20] = idx >> 8; t[21] = idx;
    t[22] = ten >> 24; t[23] = ten >> 16; t[24] = ten >> 8; t[25] = ten; (void)v;
}
static void th(const unsigned char *t, const unsigned char *a, size_t al, const unsigned char *b, size_t bl, unsigned char *o, int n) {
    unsigned char d[32];
    EVP_DigestInit_ex2(MC, SHA, NULL); EVP_DigestUpdate(MC, t, 26); EVP_DigestUpdate(MC, a, al);
    if (bl) EVP_DigestUpdate(MC, b, bl);
    EVP_DigestFinal_ex(MC, d, NULL); memcpy(o, d, n);
}
static int b64url(const unsigned char *in, int len, char *out) {
    int L = EVP_EncodeBlock((unsigned char *)out, in, len);
    while (L && out[L - 1] == '=') L--;
    for (int i = 0; i < L; i++) { if (out[i] == '+') out[i] = '-'; else if (out[i] == '/') out[i] = '_'; }
    out[L] = 0; return L;
}
int main(int argc, char **argv) {
    const char *alg = argv[1]; int N = atoi(argv[2]), reps = atoi(argv[3]), n = argc > 4 ? atoi(argv[4]) : 16;
    SHA = EVP_MD_fetch(NULL, "SHA256", NULL); MC = EVP_MD_CTX_new();
    EVP_PKEY *k = EVP_PKEY_Q_keygen(NULL, NULL, alg);
    const char *ctxs = "EMBER-root";
    int pq = strncmp(alg, "ED", 2) != 0;
    char claims[] = "URLPrefix=L3YvdDcvbTAwMDAwMC94eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg:Expires=1800001800:Tenant=7";
    int cl = strlen(claims);
    int levels = 0; while ((1 << levels) < N) levels++;
    /* level arrays */
    unsigned char **lv = calloc(levels + 1, sizeof(void *)); int *cnt = calloc(levels + 1, sizeof(int));
    cnt[0] = N; for (int l = 1; l <= levels; l++) cnt[l] = (cnt[l - 1] + 1) / 2;
    for (int l = 0; l <= levels; l++) lv[l] = malloc((size_t)cnt[l] * n);
    unsigned char *R = malloc((size_t)N * 16); RAND_bytes(R, N * 16);
    double *tl = malloc(sizeof(double) * reps), *tt = malloc(sizeof(double) * reps), *ts = malloc(sizeof(double) * reps),
           *te = malloc(sizeof(double) * reps), *tx = malloc(sizeof(double) * reps);
    static unsigned char sig[65536], blob[30 + 32 * 32], tok[8192]; size_t sl;
    volatile size_t sink = 0;
    for (int r = -1; r < reps; r++) {
        double t0 = now_us(); unsigned char t[26];
        for (int i = 0; i < N; i++) { tw(t, 5, 0, 0, i, 7); th(t, R + 16 * i, 16, (unsigned char *)claims, cl, lv[0] + (size_t)i * n, n); }
        double t1 = now_us();
        for (int l = 1; l <= levels; l++) {
            int m = cnt[l - 1];
            for (int j = 0; j < m / 2; j++) { tw(t, 5, 1, l, j, 0); th(t, lv[l - 1] + (size_t)2 * j * n, 2 * n, NULL, 0, lv[l] + (size_t)j * n, n); }
            if (m & 1) memcpy(lv[l] + (size_t)(m / 2) * n, lv[l - 1] + (size_t)(m - 1) * n, n);
        }
        double t2 = now_us();
        unsigned char msg[128]; memcpy(msg, "EMBER-root", 10); memset(msg + 10, 1, 24); memcpy(msg + 34, lv[levels], n);
        EVP_MD_CTX *m = EVP_MD_CTX_new(); OSSL_PARAM p[2] = {OSSL_PARAM_END, OSSL_PARAM_END};
        if (pq) p[0] = OSSL_PARAM_construct_octet_string(OSSL_SIGNATURE_PARAM_CONTEXT_STRING, (void *)ctxs, 10);
        EVP_DigestSignInit_ex(m, NULL, NULL, NULL, NULL, k, p); sl = sizeof sig;
        if (EVP_DigestSign(m, sig, &sl, msg, 34 + n) <= 0) { fprintf(stderr, "sign fail\n"); return 1; }
        EVP_MD_CTX_free(m);
        double t3 = now_us();
        for (int i = 0; i < N; i++) {
            memset(blob, 0, 14); blob[0] = 1; blob[10] = i >> 24; blob[11] = i >> 16; blob[12] = i >> 8; blob[13] = i;
            memcpy(blob + 14, R + 16 * i, 16); int L = 30, ii = i;
            for (int l = 0; l < levels; l++) { int s = ii ^ 1; if (s < cnt[l]) { memcpy(blob + L, lv[l] + (size_t)s * n, n); L += n; } ii >>= 1; }
            memcpy(tok, claims, cl); memcpy(tok + cl, ":E=", 3);
            sink += b64url(blob, L, (char *)tok + cl + 3);
        }
        double t4 = now_us();
        if (r >= 0) { tl[r] = t1 - t0; tt[r] = t2 - t1; ts[r] = t3 - t2; te[r] = t4 - t3; tx[r] = t4 - t0; }
    }
    qsort(tl, reps, 8, cmpd); qsort(tt, reps, 8, cmpd); qsort(ts, reps, 8, cmpd); qsort(te, reps, 8, cmpd); qsort(tx, reps, 8, cmpd);
    int h = reps / 2;
    printf("%s,%d,%d,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.1f\n", alg, N, n, reps, tl[h], tt[h], ts[h], te[h], tx[h], N / (tx[h] / 1e6));
    return 0;
}
