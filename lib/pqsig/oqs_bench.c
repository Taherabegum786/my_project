/* liboqs signature benchmark (+ Ed25519 / ECDSA P-256 through OpenSSL EVP, same C harness).
 * Build: cc -O2 -I$PREFIX/include oqs_bench.c -L$PREFIX/lib -loqs -lm -lcrypto -o oqs_bench
 * Run:   oqs_bench ITER MACHINE DATE GIT_COMMIT GIT_DIRTY [alg ...] >> out.csv   (header via oqs_bench --header)
 *        oqs_bench --classical ITER MACHINE DATE GIT_COMMIT GIT_DIRTY >> classical.csv   (OpenSSL baselines)
 *        oqs_bench --list        default scheme set: ML-DSA, Falcon, MAYO, UOV, SNOVA (all levels), only the pure SLH-DSA sets,
 *                                and the lowest claimed NIST level of every other family (CROSS, MQOM)
 *        oqs_bench --list-all    every enabled scheme (the full list)
 * Timings in microseconds, clock_gettime(CLOCK_MONOTONIC). Schema matches classical_bench.py. */
#include <oqs/oqs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <openssl/evp.h>
#include <openssl/obj_mac.h>
#include <openssl/ec.h>
#include <openssl/opensslv.h>

#define KG_MAX 200
static double now_us(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e6 + t.tv_nsec / 1e3;
}
static int cmpd(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y);
}
static void emit(const double *v, size_t n, double *fg3, double *fg100) {
    double *s = malloc(n * sizeof *s); memcpy(s, v, n * sizeof *s);
    qsort(s, n, sizeof *s, cmpd);
    double mean = 0, var = 0; size_t g3 = 0, g100 = 0;
    for (size_t i = 0; i < n; i++) { mean += v[i]; g3 += v[i] > 3000; g100 += v[i] > 100000; }
    mean /= n;
    for (size_t i = 0; i < n; i++) var += (v[i] - mean) * (v[i] - mean);
    double sd = n > 1 ? sqrt(var / (n - 1)) : 0;
    double med = (n % 2) ? s[n / 2] : 0.5 * (s[n / 2 - 1] + s[n / 2]);
    size_t i95 = (size_t)ceil(0.95 * n) - 1, i99 = (size_t)ceil(0.99 * n) - 1;
    printf(",%.3f,%.3f,%.3f,%.3f,%.3f,%.6f,%.6f", mean, med, s[i95], s[i99], sd, (double)g3 / n, (double)g100 / n);
    (void)fg3; (void)fg100; free(s);
}
static const char *HDR_OPS[] = {"keygen", "sign", "verify"};
static void header(void) {
    printf("machine,date,git_commit,git_dirty,backend,scheme,family,iterations,keygen_iterations,msg_bytes,pk_bytes,sk_bytes,sig_bytes_max,sig_bytes_mean");
    for (int o = 0; o < 3; o++)
        printf(",%s_mean_us,%s_median_us,%s_p95_us,%s_p99_us,%s_std_us,%s_frac_gt3ms,%s_frac_gt100ms",
               HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o]);
    printf("\n");
}
static int bench(const char *alg, size_t n, const char *mach, const char *date, const char *commit, const char *dirty) {
    OQS_SIG *sig = OQS_SIG_new(alg);
    if (!sig) { fprintf(stderr, "skip %s (not enabled)\n", alg); return 0; }
    uint8_t msg[64]; memset(msg, 0x5a, sizeof msg);
    uint8_t *pk = malloc(sig->length_public_key), *sk = malloc(sig->length_secret_key);
    uint8_t *sg = malloc(sig->length_signature);
    size_t nk = n < KG_MAX ? n : KG_MAX;   /* key generation is repeated at most KG_MAX times (it is not a per-message cost) */
    double *kg = malloc(nk * sizeof(double)), *sn = malloc(n * sizeof(double)), *vf = malloc(n * sizeof(double));
    size_t maxl = 0; double suml = 0, t;
    for (size_t i = 0; i < nk; i++) {
        t = now_us();
        if (OQS_SIG_keypair(sig, pk, sk) != OQS_SUCCESS) { fprintf(stderr, "keypair fail %s\n", alg); return 1; }
        kg[i] = now_us() - t;
    }
    for (size_t i = 0; i < n; i++) {
        size_t l = 0;
        t = now_us();
        if (OQS_SIG_sign(sig, sg, &l, msg, sizeof msg, sk) != OQS_SUCCESS) { fprintf(stderr, "sign fail %s\n", alg); return 1; }
        sn[i] = now_us() - t;
        if (l > maxl) maxl = l;
        suml += l;
        t = now_us();
        if (OQS_SIG_verify(sig, msg, sizeof msg, sg, l, pk) != OQS_SUCCESS) { fprintf(stderr, "verify fail %s\n", alg); return 1; }
        vf[i] = now_us() - t;
    }
    printf("%s,%s,%s,%s,liboqs-%s,%s,pq,%zu,%zu,%zu,%zu,%zu,%zu,%.2f", mach, date, commit, dirty, OQS_version(), alg, n, nk,
           sizeof msg, sig->length_public_key, sig->length_secret_key, maxl, suml / n);
    emit(kg, nk, 0, 0); emit(sn, n, 0, 0); emit(vf, n, 0, 0);
    printf("\n");
    OQS_SIG_free(sig); free(pk); free(sk); free(sg); free(kg); free(sn); free(vf);
    return 0;
}
/* ---- classical baselines through OpenSSL EVP (same timing harness) ---- */
static EVP_PKEY *cl_keygen(int ed) {
    EVP_PKEY_CTX *c = EVP_PKEY_CTX_new_id(ed ? EVP_PKEY_ED25519 : EVP_PKEY_EC, NULL);
    EVP_PKEY *k = NULL; EVP_PKEY_keygen_init(c);
    if (!ed) EVP_PKEY_CTX_set_ec_paramgen_curve_nid(c, NID_X9_62_prime256v1);
    if (EVP_PKEY_keygen(c, &k) != 1) { fprintf(stderr, "openssl keygen failed\n"); exit(1); }
    EVP_PKEY_CTX_free(c); return k;
}
static size_t cl_sign(EVP_PKEY *k, int ed, const uint8_t *m, size_t ml, uint8_t *sig) {
    EVP_MD_CTX *c = EVP_MD_CTX_new(); size_t l = 80;
    if (EVP_DigestSignInit(c, NULL, ed ? NULL : EVP_sha256(), NULL, k) != 1 || EVP_DigestSign(c, sig, &l, m, ml) != 1) { fprintf(stderr, "openssl sign failed\n"); exit(1); }
    EVP_MD_CTX_free(c); return l;
}
static int cl_verify(EVP_PKEY *k, int ed, const uint8_t *m, size_t ml, const uint8_t *sig, size_t sl) {
    EVP_MD_CTX *c = EVP_MD_CTX_new();
    int ok = EVP_DigestVerifyInit(c, NULL, ed ? NULL : EVP_sha256(), NULL, k) == 1 && EVP_DigestVerify(c, sig, sl, m, ml) == 1;
    EVP_MD_CTX_free(c); return ok;
}
static int bench_classical(int ed, size_t n, const char *mach, const char *date, const char *commit, const char *dirty) {
    uint8_t msg[64]; memset(msg, 0x5a, sizeof msg); uint8_t sg[128];
    size_t nk = n < KG_MAX ? n : KG_MAX;
    double *kg = malloc(nk * sizeof(double)), *sn = malloc(n * sizeof(double)), *vf = malloc(n * sizeof(double));
    double t; EVP_PKEY *k = NULL; size_t maxl = 0; double suml = 0, l;
    for (size_t i = 0; i < nk; i++) { t = now_us(); EVP_PKEY *x = cl_keygen(ed); kg[i] = now_us() - t; if (i + 1 < nk) EVP_PKEY_free(x); else k = x; }
    size_t sl = 0;
    for (size_t i = 0; i < n; i++) {
        t = now_us(); sl = cl_sign(k, ed, msg, sizeof msg, sg); sn[i] = now_us() - t;
        if (sl > maxl) { maxl = sl; } suml += sl;
        t = now_us(); if (!cl_verify(k, ed, msg, sizeof msg, sg, sl)) { fprintf(stderr, "openssl verify failed\n"); return 1; } vf[i] = now_us() - t;
    }
    l = suml / n;
    printf("%s,%s,%s,%s,openssl-%s,%s,classical,%zu,%zu,%zu,%d,32,%zu,%.2f", mach, date, commit, dirty, OPENSSL_VERSION_TEXT, ed ? "Ed25519" : "ECDSA-P256", n, nk, sizeof msg, ed ? 32 : 65, maxl, l);
    emit(kg, nk, 0, 0); emit(sn, n, 0, 0); emit(vf, n, 0, 0); printf("\n");
    EVP_PKEY_free(k); free(kg); free(sn); free(vf); return 0;
}
/* ---- default scheme filter ---- */
static int starts(const char *a, const char *p) { return strncmp(a, p, strlen(p)) == 0; }
static int is_all_levels_family(const char *a) {
    return starts(a, "ML-DSA") || starts(a, "Falcon") || starts(a, "MAYO") || starts(a, "OV") || starts(a, "SNOVA");
}
static const char *other_family(const char *a) {      /* families kept at their lowest claimed NIST level only */
    if (starts(a, "cross")) return "cross";
    if (starts(a, "mqom")) return "mqom";
    return NULL;
}
static int selected_by_default(const char *a) {
    if (is_all_levels_family(a)) return 1;
    if (starts(a, "SLH_DSA")) return starts(a, "SLH_DSA_PURE");
    const char *fam = other_family(a);
    if (!fam) return 1;
    int lo = 99, mine = 99;
    for (size_t i = 0; i < OQS_SIG_algs_length; i++) {
        const char *b = OQS_SIG_alg_identifier(i);
        if (!OQS_SIG_alg_is_enabled(b) || !starts(b, fam)) continue;
        OQS_SIG *s = OQS_SIG_new(b); if (!s) continue;
        int lv = (int)s->claimed_nist_level; if (lv < lo) lo = lv; if (!strcmp(a, b)) mine = lv; OQS_SIG_free(s);
    }
    return mine == lo;
}
int main(int argc, char **argv) {
    if (argc >= 2 && !strcmp(argv[1], "--header")) { header(); return 0; }
    if (argc >= 2 && !strcmp(argv[1], "--list-sizes")) {
        /* declared (library-level) sizes: OQS_SIG length_* fields, no timing */
        OQS_init();
        printf("scheme,claimed_nist_level,euf_cma,length_public_key,length_secret_key,length_signature_declared,liboqs_version\n");
        for (size_t i = 0; i < OQS_SIG_algs_length; i++) {
            const char *a = OQS_SIG_alg_identifier(i);
            if (!OQS_SIG_alg_is_enabled(a)) continue;
            OQS_SIG *sg = OQS_SIG_new(a);
            if (!sg) continue;
            printf("%s,%d,%d,%zu,%zu,%zu,%s\n", a, (int)sg->claimed_nist_level, (int)sg->euf_cma,
                   sg->length_public_key, sg->length_secret_key, sg->length_signature, OQS_version());
            OQS_SIG_free(sg);
        }
        return 0;
    }
    if (argc >= 2 && (!strcmp(argv[1], "--list") || !strcmp(argv[1], "--list-all"))) {
        int all = !strcmp(argv[1], "--list-all");
        OQS_init();
        for (size_t i = 0; i < OQS_SIG_algs_length; i++) {
            const char *a = OQS_SIG_alg_identifier(i);
            if (OQS_SIG_alg_is_enabled(a) && (all || selected_by_default(a))) printf("%s\n", a);
        }
        return 0;
    }
    if (argc >= 7 && !strcmp(argv[1], "--classical")) {
        size_t n = strtoul(argv[2], 0, 10);
        return bench_classical(1, n, argv[3], argv[4], argv[5], argv[6]) || bench_classical(0, n, argv[3], argv[4], argv[5], argv[6]);
    }
    if (argc < 6) { fprintf(stderr, "usage: %s ITER MACHINE DATE COMMIT DIRTY [alg...]\n", argv[0]); return 2; }
    size_t n = strtoul(argv[1], 0, 10);
    OQS_init();
    if (argc > 6) { for (int i = 6; i < argc; i++) if (bench(argv[i], n, argv[2], argv[3], argv[4], argv[5])) return 1; }
    else for (size_t i = 0; i < OQS_SIG_algs_length; i++) {
        const char *a = OQS_SIG_alg_identifier(i);
        if (OQS_SIG_alg_is_enabled(a) && selected_by_default(a) && bench(a, n, argv[2], argv[3], argv[4], argv[5])) return 1;
    }
    return 0;
}
