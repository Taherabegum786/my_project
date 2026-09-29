/*
 * tapbridge: userspace layer-2 link emulator between two TAP devices.
 *
 * Replaces tc-netem (not available in the evaluation kernel).  Every
 * Ethernet frame read from one TAP device is written to the other after a
 * fixed one-way delay, serialised at a configurable link rate, so TCP runs
 * end to end between the two network namespaces with a real 1500-byte MTU
 * and its own congestion control.  Frames in each direction leave in FIFO
 * order.
 *
 * usage: tapbridge <tapA> <tapB> <one_way_delay_us> <rate_mbit> [ready_file]
 * The TAP devices are created by this process; a script then moves them
 * into namespaces (the file descriptors stay attached).  SIGHUP re-reads
 * the delay from /run/tapbridge.delay_us so that the RTT can be changed
 * without restarting the link.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <poll.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <time.h>
#include <unistd.h>

#define MAXF 2048
#define QLEN 65536

typedef struct {
    uint64_t release_ns;
    uint16_t len;
    unsigned char buf[MAXF];
} frame_t;

typedef struct {
    frame_t *q;
    size_t head, tail;
    uint64_t link_free_ns; /* when the emulated link finishes the last frame */
    uint64_t drops;
} dirq_t;

static volatile sig_atomic_t reload = 0;
static uint64_t delay_ns;
static uint32_t loss_ppm = 0;
static uint64_t rng = 0x9e3779b97f4a7c15ull;

static uint32_t rnd_ppm(void) { /* xorshift64* */
    rng ^= rng >> 12; rng ^= rng << 25; rng ^= rng >> 27;
    return (uint32_t)((rng * 0x2545F4914F6CDD1Dull) >> 32) % 1000000u;
}
static double ns_per_byte;

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static int tap_open(const char *name) {
    int fd = open("/dev/net/tun", O_RDWR | O_NONBLOCK);
    if (fd < 0) { perror("open /dev/net/tun"); exit(1); }
    struct ifreq ifr;
    memset(&ifr, 0, sizeof ifr);
    ifr.ifr_flags = IFF_TAP | IFF_NO_PI;
    strncpy(ifr.ifr_name, name, IFNAMSIZ - 1);
    if (ioctl(fd, TUNSETIFF, &ifr) < 0) { perror("TUNSETIFF"); exit(1); }
    return fd;
}

static void on_hup(int sig) { (void)sig; reload = 1; }

static void read_delay_file(void) {
    FILE *f = fopen("/run/tapbridge.delay_us", "r");
    if (!f) return;
    unsigned long long us;
    if (fscanf(f, "%llu", &us) == 1) delay_ns = us * 1000ull;
    fclose(f);
    f = fopen("/run/tapbridge.loss_ppm", "r");
    if (!f) return;
    unsigned int ppm;
    if (fscanf(f, "%u", &ppm) == 1) loss_ppm = ppm;
    fclose(f);
}

/* Read all pending frames from fd into q. */
static void ingest(int fd, dirq_t *d) {
    for (;;) {
        size_t next = (d->tail + 1) % QLEN;
        frame_t *f = &d->q[d->tail];
        ssize_t n = read(fd, f->buf, MAXF);
        if (n <= 0) return;
        if (next == d->head) { d->drops++; continue; }
        if (loss_ppm && rnd_ppm() < loss_ppm) { d->drops++; continue; }
        uint64_t t = now_ns();
        uint64_t start = d->link_free_ns > t ? d->link_free_ns : t;
        uint64_t tx_done = start + (uint64_t)(n * ns_per_byte);
        d->link_free_ns = tx_done;
        f->len = (uint16_t)n;
        f->release_ns = tx_done + delay_ns;
        d->tail = next;
    }
}

/* Write all due frames; return ns until the next frame is due (or -1). */
static int64_t flush(int fd, dirq_t *d) {
    uint64_t t = now_ns();
    while (d->head != d->tail) {
        frame_t *f = &d->q[d->head];
        if (f->release_ns > t) return (int64_t)(f->release_ns - t);
        if (write(fd, f->buf, f->len) < 0 && errno == EAGAIN) return 20000;
        d->head = (d->head + 1) % QLEN;
    }
    return -1;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "usage: %s tapA tapB delay_us rate_mbit [ready_file]\n", argv[0]);
        return 2;
    }
    int fa = tap_open(argv[1]), fb = tap_open(argv[2]);
    delay_ns = strtoull(argv[3], NULL, 10) * 1000ull;
    ns_per_byte = 8000.0 / atof(argv[4]); /* ns per byte at rate Mbit/s */
    signal(SIGHUP, on_hup);
    dirq_t ab = {calloc(QLEN, sizeof(frame_t)), 0, 0, 0, 0};
    dirq_t ba = {calloc(QLEN, sizeof(frame_t)), 0, 0, 0, 0};
    if (argc > 5) { FILE *r = fopen(argv[5], "w"); if (r) fclose(r); }

    struct pollfd p[2] = {{fa, POLLIN, 0}, {fb, POLLIN, 0}};
    for (;;) {
        if (reload) { reload = 0; read_delay_file(); }
        int64_t w1 = flush(fb, &ab), w2 = flush(fa, &ba);
        int64_t w = -1;
        if (w1 >= 0) w = w1;
        if (w2 >= 0 && (w < 0 || w2 < w)) w = w2;
        struct timespec ts, *tp = NULL;
        if (w >= 0) {
            /* Sleep coarsely, then spin for the last 50 us for precision. */
            if (w > 60000) { ts.tv_sec = 0; ts.tv_nsec = w - 50000; tp = &ts; }
            else { ts.tv_sec = 0; ts.tv_nsec = 0; tp = &ts; }
        }
        int r = ppoll(p, 2, tp, NULL);
        if (r < 0 && errno != EINTR) { perror("ppoll"); return 1; }
        if (p[0].revents & POLLIN) ingest(fa, &ab);
        if (p[1].revents & POLLIN) ingest(fb, &ba);
    }
}
