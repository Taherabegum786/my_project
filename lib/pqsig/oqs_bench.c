/* liboqs signature benchmark. Enumerates every enabled signature scheme.
 * Build: cc -O2 -I$PREFIX/include oqs_bench.c -L$PREFIX/lib -loqs -lm -o oqs_bench
 * Run:   oqs_bench ITER MACHINE DATE GIT_COMMIT [alg ...] >> out.csv   (header via oqs_bench --header)
 * Timings in microseconds, clock_gettime(CLOCK_MONOTONIC). Schema matches classical_bench.py. */
#include <oqs/oqs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

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
    printf("machine,date,git_commit,backend,scheme,family,iterations,msg_bytes,pk_bytes,sk_bytes,sig_bytes_max,sig_bytes_mean");
    for (int o = 0; o < 3; o++)
        printf(",%s_mean_us,%s_median_us,%s_p95_us,%s_p99_us,%s_std_us,%s_frac_gt3ms,%s_frac_gt100ms",
               HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o], HDR_OPS[o]);
    printf("\n");
}
static int bench(const char *alg, size_t n, const char *mach, const char *date, const char *commit) {
    OQS_SIG *sig = OQS_SIG_new(alg);
    if (!sig) { fprintf(stderr, "skip %s (not enabled)\n", alg); return 0; }
    uint8_t msg[64]; memset(msg, 0x5a, sizeof msg);
    uint8_t *pk = malloc(sig->length_public_key), *sk = malloc(sig->length_secret_key);
    uint8_t *sg = malloc(sig->length_signature);
    double *kg = malloc(n * sizeof(double)), *sn = malloc(n * sizeof(double)), *vf = malloc(n * sizeof(double));
    size_t maxl = 0; double suml = 0, t;
    for (size_t i = 0; i < n; i++) {
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
    printf("%s,%s,%s,liboqs-%s,%s,pq,%zu,%zu,%zu,%zu,%zu,%.2f", mach, date, commit, OQS_version(), alg, n,
           sizeof msg, sig->length_public_key, sig->length_secret_key, maxl, suml / n);
    emit(kg, n, 0, 0); emit(sn, n, 0, 0); emit(vf, n, 0, 0);
    printf("\n");
    OQS_SIG_free(sig); free(pk); free(sk); free(sg); free(kg); free(sn); free(vf);
    return 0;
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
    if (argc >= 2 && !strcmp(argv[1], "--list")) {
        OQS_init();
        for (size_t i = 0; i < OQS_SIG_algs_length; i++) {
            const char *a = OQS_SIG_alg_identifier(i);
            if (OQS_SIG_alg_is_enabled(a)) printf("%s\n", a);
        }
        return 0;
    }
    if (argc < 5) { fprintf(stderr, "usage: %s ITER MACHINE DATE COMMIT [alg...]\n", argv[0]); return 2; }
    size_t n = strtoul(argv[1], 0, 10);
    OQS_init();
    if (argc > 5) { for (int i = 5; i < argc; i++) if (bench(argv[i], n, argv[2], argv[3], argv[4])) return 1; }
    else for (size_t i = 0; i < OQS_SIG_algs_length; i++) {
        const char *a = OQS_SIG_alg_identifier(i);
        if (OQS_SIG_alg_is_enabled(a) && bench(a, n, argv[2], argv[3], argv[4])) return 1;
    }
    return 0;
}
