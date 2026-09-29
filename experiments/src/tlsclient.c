/*
 * tlsclient: TLS 1.3 client and load generator with optional DAPV.
 *
 * DAPV is implemented by exporting dapv_submit(), which the patched
 * oqs-provider calls after the classical component of a hybrid signature
 * has verified.  When DAPV is enabled, the PQ component (message, signature
 * and PQ public key) is copied into a job and verified by a background
 * worker; the provider returns success so that the handshake proceeds.
 * This applies to every hybrid verification the client performs: the
 * certificate signatures of the chain and CertificateVerify.  A session is
 * "fully authenticated" when all jobs submitted during its handshake have
 * completed successfully.
 *
 * Worker models:  none    synchronous verification (baseline)
 *                 thread  one new thread per job (as in the original prototype)
 *                 pool:M  M pre-started workers with a FIFO queue
 *
 * Modes:
 *   seq  <n>            n sequential handshakes; per-handshake latency and
 *                       per-job timings are written as CSV.
 *   load <conns> <warmup_s> <measure_s>
 *                       closed loop with <conns> concurrent connections;
 *                       reports completed handshakes per second.
 *
 * usage: tlsclient <host> <port> <cafile> <groups> <worker-model> <outprefix>
 *                  seq <n> | load <conns> <warmup_s> <measure_s>
 * env:   DAPV_CORRUPT=1 flips one byte of each deferred PQ signature
 *        (to check that failures are detected).
 */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <oqs/oqs.h>
#include <openssl/err.h>
#include <openssl/provider.h>
#include <openssl/ssl.h>
#include <pthread.h>
#include <signal.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

/* ------------------------------------------------------------------ */
static inline uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

#define MAXHS (1u << 21)
#define MAXJOBS (1u << 23)

typedef struct {
    uint64_t t_tcp, t_hello, t_done; /* connect start, ClientHello, hs done */
    int njobs;
    _Atomic int jobs_done, jobs_failed;
    _Atomic uint64_t t_last_job;
} hsrec_t;

typedef struct {
    uint32_t serial;
    uint64_t t_submit, t_start, t_end;
    uint32_t crypto_ns;
    int ok;
} joblog_t;

typedef struct job {
    struct job *next;
    uint32_t serial;
    uint64_t t_submit;
    const char *alg;
    unsigned char *pk, *msg, *sig;
    size_t pklen, msglen, siglen;
} job_t;

static hsrec_t *hs;
static joblog_t *jl;
static _Atomic uint32_t njl;
static int model = 0; /* 0 none, 1 thread, 2 pool */
static int corrupt = 0;
static __thread uint32_t cur_serial;

static pthread_mutex_t qmu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t qcv = PTHREAD_COND_INITIALIZER;
static job_t *qhead, *qtail;

static pthread_mutex_t dmu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t dcv = PTHREAD_COND_INITIALIZER;

/* ------------------------------------------------------------------ */
static OQS_SIG *sig_for(const char *alg) {
    static __thread OQS_SIG *cache[8];
    static __thread const char *names[8];
    for (int i = 0; i < 8; i++) {
        if (names[i] && strcmp(names[i], alg) == 0) return cache[i];
        if (!names[i]) {
            cache[i] = OQS_SIG_new(alg);
            names[i] = cache[i] ? alg : NULL;
            return cache[i];
        }
    }
    return OQS_SIG_new(alg);
}

static void run_job(job_t *j) {
    uint64_t t0 = now_ns();
    OQS_SIG *s = sig_for(j->alg);
    uint64_t c0 = now_ns();
    int ok = s && OQS_SIG_verify(s, j->msg, j->msglen, j->sig, j->siglen,
                                 j->pk) == OQS_SUCCESS;
    uint64_t c1 = now_ns();
    uint32_t k = atomic_fetch_add(&njl, 1);
    if (k < MAXJOBS)
        jl[k] = (joblog_t){j->serial, j->t_submit, t0, c1, (uint32_t)(c1 - c0), ok};
    hsrec_t *h = &hs[j->serial % MAXHS];
    uint64_t prev = atomic_load(&h->t_last_job);
    while (prev < c1 && !atomic_compare_exchange_weak(&h->t_last_job, &prev, c1)) {}
    if (!ok) atomic_fetch_add(&h->jobs_failed, 1);
    pthread_mutex_lock(&dmu);
    atomic_fetch_add(&h->jobs_done, 1);
    pthread_cond_broadcast(&dcv);
    pthread_mutex_unlock(&dmu);
    free(j->pk);
    free(j->msg);
    free(j->sig);
    free(j);
}

static void *thread_job(void *a) {
    run_job(a);
    return NULL;
}

static void *pool_worker(void *a) {
    (void)a;
    for (;;) {
        pthread_mutex_lock(&qmu);
        while (!qhead) pthread_cond_wait(&qcv, &qmu);
        job_t *j = qhead;
        qhead = j->next;
        if (!qhead) qtail = NULL;
        pthread_mutex_unlock(&qmu);
        run_job(j);
    }
    return NULL;
}

static unsigned char *memdup_(const unsigned char *p, size_t n) {
    unsigned char *d = malloc(n ? n : 1);
    memcpy(d, p, n);
    return d;
}

/* Called by the patched oqs-provider. Return 1 = deferred. */
__attribute__((visibility("default"))) int
dapv_submit(const char *alg, const unsigned char *pk, size_t pklen,
            const unsigned char *msg, size_t msglen, const unsigned char *sig,
            size_t siglen) {
    if (model == 0) return 0;
    job_t *j = calloc(1, sizeof *j);
    j->serial = cur_serial;
    j->alg = alg; /* static string owned by liboqs */
    j->pk = memdup_(pk, pklen); j->pklen = pklen;
    j->msg = memdup_(msg, msglen); j->msglen = msglen;
    j->sig = memdup_(sig, siglen); j->siglen = siglen;
    if (corrupt) j->sig[siglen / 2] ^= 0x01;
    hs[cur_serial % MAXHS].njobs++;
    j->t_submit = now_ns();
    if (model == 1) {
        pthread_t t;
        pthread_attr_t at;
        pthread_attr_init(&at);
        pthread_attr_setdetachstate(&at, PTHREAD_CREATE_DETACHED);
        pthread_create(&t, &at, thread_job, j);
        pthread_attr_destroy(&at);
    } else {
        pthread_mutex_lock(&qmu);
        if (qtail) qtail->next = j; else qhead = j;
        qtail = j;
        pthread_cond_signal(&qcv);
        pthread_mutex_unlock(&qmu);
    }
    return 1;
}

static void wait_full(uint32_t serial) {
    hsrec_t *h = &hs[serial % MAXHS];
    pthread_mutex_lock(&dmu);
    while (atomic_load(&h->jobs_done) < h->njobs) pthread_cond_wait(&dcv, &dmu);
    pthread_mutex_unlock(&dmu);
}

/* ------------------------------------------------------------------ */
static SSL_CTX *ctx;
static struct sockaddr_in srv;

static int tcp_socket(int nonblock) {
    int s = socket(AF_INET, SOCK_STREAM | (nonblock ? SOCK_NONBLOCK : 0), 0);
    int one = 1;
    setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
    struct linger lg = {1, 0}; /* RST on close: avoid TIME_WAIT exhaustion */
    setsockopt(s, SOL_SOCKET, SO_LINGER, &lg, sizeof lg);
    return s;
}

static int run_seq(int n, const char *prefix) {
    char fn[512];
    snprintf(fn, sizeof fn, "%s_hs.csv", prefix);
    FILE *fh = fopen(fn, "w");
    fprintf(fh, "serial,tcp_ms,hs_ms,full_ms,njobs,failed\n");
    unsigned char buf[64] = "GET", rbuf[64];
    int errors = 0, detected = 0;
    for (int i = 0; i < n; i++) {
        uint32_t serial = (uint32_t)i;
        hsrec_t *h = &hs[serial];
        cur_serial = serial;
        int s = tcp_socket(0);
        h->t_tcp = now_ns();
        if (connect(s, (struct sockaddr *)&srv, sizeof srv)) { perror("connect"); return 1; }
        SSL *ssl = SSL_new(ctx);
        SSL_set_fd(ssl, s);
        h->t_hello = now_ns();
        int r = SSL_connect(ssl);
        h->t_done = now_ns();
        if (r != 1) { errors++; ERR_print_errors_fp(stderr); SSL_free(ssl); close(s); continue; }
        if (SSL_write(ssl, buf, 32) <= 0 || SSL_read(ssl, rbuf, sizeof rbuf) <= 0) errors++;
        wait_full(serial);
        int failed = atomic_load(&h->jobs_failed);
        if (failed) detected++;
        uint64_t tfull = h->njobs ? atomic_load(&h->t_last_job) : h->t_done;
        if (tfull < h->t_done) tfull = h->t_done;
        fprintf(fh, "%u,%.4f,%.4f,%.4f,%d,%d\n", serial,
                (h->t_hello - h->t_tcp) / 1e6, (h->t_done - h->t_hello) / 1e6,
                (tfull - h->t_hello) / 1e6, h->njobs, failed);
        SSL_free(ssl);
        close(s);
    }
    fclose(fh);
    snprintf(fn, sizeof fn, "%s_jobs.csv", prefix);
    FILE *fj = fopen(fn, "w");
    fprintf(fj, "serial,queue_us,crypto_us,dt_us,ok\n");
    uint32_t m = atomic_load(&njl);
    for (uint32_t k = 0; k < m && k < MAXJOBS; k++)
        fprintf(fj, "%u,%.2f,%.2f,%.2f,%d\n", jl[k].serial,
                (jl[k].t_start - jl[k].t_submit) / 1e3, jl[k].crypto_ns / 1e3,
                (jl[k].t_end - jl[k].t_submit) / 1e3, jl[k].ok);
    fclose(fj);
    fprintf(stderr, "seq: %d handshakes, %d errors, %d sessions with PQ failure detected\n",
            n, errors, detected);
    return errors ? 1 : 0;
}

/* ------------------------------------------------------------------ */
enum { ST_CONNECT, ST_HS, ST_WRITE, ST_READ };
typedef struct {
    int fd, st;
    SSL *ssl;
    uint32_t serial;
} conn_t;

static uint32_t next_serial = 0;

static void conn_start(int ep, conn_t *c) {
    c->serial = next_serial++;
    hsrec_t *h = &hs[c->serial % MAXHS];
    h->njobs = 0;
    atomic_store(&h->jobs_done, 0);
    atomic_store(&h->jobs_failed, 0);
    atomic_store(&h->t_last_job, 0);
    c->fd = tcp_socket(1);
    h->t_tcp = now_ns();
    int r = connect(c->fd, (struct sockaddr *)&srv, sizeof srv);
    c->st = ST_CONNECT;
    c->ssl = NULL;
    struct epoll_event ev = {.events = EPOLLOUT, .data.ptr = c};
    epoll_ctl(ep, EPOLL_CTL_ADD, c->fd, &ev);
    (void)r;
}

static void conn_end(int ep, conn_t *c) {
    epoll_ctl(ep, EPOLL_CTL_DEL, c->fd, NULL);
    if (c->ssl) SSL_free(c->ssl);
    close(c->fd);
}

static void want(int ep, conn_t *c, int err) {
    struct epoll_event ev = {.events = err == SSL_ERROR_WANT_WRITE ? EPOLLOUT : EPOLLIN,
                             .data.ptr = c};
    epoll_ctl(ep, EPOLL_CTL_MOD, c->fd, &ev);
}

static int run_load(int nconn, double warm, double meas, const char *prefix) {
    int ep = epoll_create1(0);
    conn_t *cs = calloc(nconn, sizeof *cs);
    uint64_t t0 = now_ns(), tw = t0 + (uint64_t)(warm * 1e9),
             te = tw + (uint64_t)(meas * 1e9);
    for (int i = 0; i < nconn; i++) conn_start(ep, &cs[i]);
    uint64_t done = 0, errors = 0;
    double lat_sum = 0;
    struct epoll_event evs[1024];
    struct rusage ru0, ru1;
    int started = 0;
    char fn[512];
    snprintf(fn, sizeof fn, "%s_loadlat.csv", prefix);
    FILE *fl = fopen(fn, "w");
    fprintf(fl, "hs_ms\n");
    unsigned char buf[64] = "GET";
    for (;;) {
        uint64_t t = now_ns();
        if (!started && t >= tw) { started = 1; getrusage(RUSAGE_SELF, &ru0); }
        if (t >= te) break;
        int n = epoll_wait(ep, evs, 1024, 10);
        for (int k = 0; k < n; k++) {
            conn_t *c = evs[k].data.ptr;
            hsrec_t *h = &hs[c->serial % MAXHS];
            int r, e;
            if (c->st == ST_CONNECT) {
                int soerr = 0;
                socklen_t sl = sizeof soerr;
                getsockopt(c->fd, SOL_SOCKET, SO_ERROR, &soerr, &sl);
                if (soerr) { errors++; conn_end(ep, c); conn_start(ep, c); continue; }
                c->ssl = SSL_new(ctx);
                SSL_set_fd(c->ssl, c->fd);
                c->st = ST_HS;
                h->t_hello = now_ns();
            }
            if (c->st == ST_HS) {
                cur_serial = c->serial;
                r = SSL_do_handshake(c->ssl);
                if (r != 1) {
                    e = SSL_get_error(c->ssl, r);
                    if (e == SSL_ERROR_WANT_READ || e == SSL_ERROR_WANT_WRITE) { want(ep, c, e); continue; }
                    errors++; ERR_clear_error(); conn_end(ep, c); conn_start(ep, c); continue;
                }
                h->t_done = now_ns();
                c->st = ST_WRITE;
            }
            if (c->st == ST_WRITE) {
                r = SSL_write(c->ssl, buf, 32);
                if (r <= 0) {
                    e = SSL_get_error(c->ssl, r);
                    if (e == SSL_ERROR_WANT_READ || e == SSL_ERROR_WANT_WRITE) { want(ep, c, e); continue; }
                    errors++; conn_end(ep, c); conn_start(ep, c); continue;
                }
                c->st = ST_READ;
                want(ep, c, SSL_ERROR_WANT_READ);
                continue;
            }
            if (c->st == ST_READ) {
                unsigned char rb[64];
                r = SSL_read(c->ssl, rb, sizeof rb);
                if (r <= 0) {
                    e = SSL_get_error(c->ssl, r);
                    if (e == SSL_ERROR_WANT_READ || e == SSL_ERROR_WANT_WRITE) { want(ep, c, e); continue; }
                    errors++; conn_end(ep, c); conn_start(ep, c); continue;
                }
                uint64_t tn = now_ns();
                if (started && tn < te) {
                    done++;
                    double l = (h->t_done - h->t_hello) / 1e6;
                    lat_sum += l;
                    fprintf(fl, "%.4f\n", l);
                }
                conn_end(ep, c);
                conn_start(ep, c);
            }
        }
    }
    getrusage(RUSAGE_SELF, &ru1);
    fclose(fl);
    double cpu = (ru1.ru_utime.tv_sec - ru0.ru_utime.tv_sec) +
                 (ru1.ru_utime.tv_usec - ru0.ru_utime.tv_usec) / 1e6 +
                 (ru1.ru_stime.tv_sec - ru0.ru_stime.tv_sec) +
                 (ru1.ru_stime.tv_usec - ru0.ru_stime.tv_usec) / 1e6;
    uint32_t m = atomic_load(&njl), bad = 0;
    snprintf(fn, sizeof fn, "%s_loadjobs.csv", prefix);
    FILE *fj = fopen(fn, "w");
    fprintf(fj, "queue_us,crypto_us,dt_us,ok\n");
    for (uint32_t k = 0; k < m && k < MAXJOBS; k++) {
        bad += !jl[k].ok;
        if (jl[k].t_submit >= tw && jl[k].t_submit < te)
            fprintf(fj, "%.2f,%.2f,%.2f,%d\n", (jl[k].t_start - jl[k].t_submit) / 1e3,
                    jl[k].crypto_ns / 1e3, (jl[k].t_end - jl[k].t_submit) / 1e3, jl[k].ok);
    }
    fclose(fj);
    printf("conns=%d handshakes=%llu rate=%.1f mean_hs_ms=%.3f errors=%llu "
           "client_cpu_cores=%.3f pq_jobs=%u pq_failures=%u\n",
           nconn, (unsigned long long)done, done / meas, done ? lat_sum / done : 0,
           (unsigned long long)errors, cpu / meas, m, bad);
    return 0;
}

/* ------------------------------------------------------------------ */
int main(int argc, char **argv) {
    if (argc < 9) {
        fprintf(stderr, "see source header for usage\n");
        return 2;
    }
    signal(SIGPIPE, SIG_IGN);
    hs = calloc(MAXHS, sizeof *hs);
    jl = calloc(MAXJOBS, sizeof *jl);
    corrupt = getenv("DAPV_CORRUPT") && atoi(getenv("DAPV_CORRUPT"));
    OQS_init();

    srv.sin_family = AF_INET;
    srv.sin_port = htons(atoi(argv[2]));
    inet_pton(AF_INET, argv[1], &srv.sin_addr);

    const char *wm = argv[5];
    if (!strcmp(wm, "none")) model = 0;
    else if (!strcmp(wm, "thread")) model = 1;
    else if (!strncmp(wm, "pool:", 5)) {
        model = 2;
        int m = atoi(wm + 5);
        for (int i = 0; i < m; i++) {
            pthread_t t;
            pthread_create(&t, NULL, pool_worker, NULL);
        }
    } else { fprintf(stderr, "bad worker model\n"); return 2; }

    if (!OSSL_PROVIDER_load(NULL, "default") || !OSSL_PROVIDER_load(NULL, "oqsprovider")) {
        ERR_print_errors_fp(stderr);
        return 1;
    }
    ctx = SSL_CTX_new(TLS_client_method());
    SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
    SSL_CTX_set_session_cache_mode(ctx, SSL_SESS_CACHE_OFF);
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
    if (SSL_CTX_load_verify_locations(ctx, argv[3], NULL) != 1 ||
        SSL_CTX_set1_groups_list(ctx, argv[4]) != 1 ||
        SSL_CTX_set1_sigalgs_list(ctx, "p256_mldsa44:p256_falcon512:p384_mldsa65:p256_sphincssha2128fsimple:"
                                       "ecdsa_secp256r1_sha256:ecdsa_secp384r1_sha384") != 1) {
        ERR_print_errors_fp(stderr);
        return 1;
    }
    if (!strcmp(argv[7], "seq")) return run_seq(atoi(argv[8]), argv[6]);
    if (!strcmp(argv[7], "load") && argc >= 11)
        return run_load(atoi(argv[8]), atof(argv[9]), atof(argv[10]), argv[6]);
    fprintf(stderr, "bad mode\n");
    return 2;
}
