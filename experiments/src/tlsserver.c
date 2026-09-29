/*
 * tlsserver: multi-threaded TLS 1.3 server for the DAPV experiments.
 *
 * T threads accept from one shared listening socket; each serves one
 * connection at a time: full handshake (no session tickets), read a
 * small request, write a small response, close.  The server is unmodified
 * with respect to DAPV; it only signs.
 *
 * usage: tlsserver <port> <threads> <chain.pem> <key.pem> <groups>
 */
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <openssl/err.h>
#include <openssl/provider.h>
#include <openssl/ssl.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static SSL_CTX *ctx;
static int port;
static int lsock; /* shared listening socket */

static int listen_socket(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0), one = 1;
    setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    setsockopt(s, SOL_SOCKET, SO_REUSEPORT, &one, sizeof one);
    struct sockaddr_in a = {.sin_family = AF_INET, .sin_port = htons(port),
                            .sin_addr.s_addr = htonl(INADDR_ANY)};
    if (bind(s, (struct sockaddr *)&a, sizeof a) || listen(s, 4096)) {
        perror("bind/listen");
        exit(1);
    }
    return s;
}

static void *serve(void *arg) {
    (void)arg;
    int ls = lsock;
    unsigned char buf[256];
    for (;;) {
        int c = accept(ls, NULL, NULL);
        if (c < 0) continue;
        int one = 1;
        setsockopt(c, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
        SSL *ssl = SSL_new(ctx);
        SSL_set_fd(ssl, c);
        if (SSL_accept(ssl) == 1) {
            int n = SSL_read(ssl, buf, sizeof buf);
            if (n > 0) SSL_write(ssl, buf, n);
        }
        SSL_free(ssl); /* no close_notify wait: client closes first */
        close(c);
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 6) {
        fprintf(stderr, "usage: %s port threads chain key groups\n", argv[0]);
        return 2;
    }
    signal(SIGPIPE, SIG_IGN);
    port = atoi(argv[1]);
    int threads = atoi(argv[2]);
    if (!OSSL_PROVIDER_load(NULL, "default") ||
        !OSSL_PROVIDER_load(NULL, "oqsprovider")) {
        ERR_print_errors_fp(stderr);
        return 1;
    }
    ctx = SSL_CTX_new(TLS_server_method());
    SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
    SSL_CTX_set_options(ctx, SSL_OP_NO_TICKET);
    SSL_CTX_set_num_tickets(ctx, 0);
    SSL_CTX_set_session_cache_mode(ctx, SSL_SESS_CACHE_OFF);
    if (SSL_CTX_use_certificate_chain_file(ctx, argv[3]) != 1 ||
        SSL_CTX_use_PrivateKey_file(ctx, argv[4], SSL_FILETYPE_PEM) != 1 ||
        SSL_CTX_set1_groups_list(ctx, argv[5]) != 1) {
        ERR_print_errors_fp(stderr);
        return 1;
    }
    lsock = listen_socket();
    pthread_t t;
    pthread_attr_t at;
    pthread_attr_init(&at);
    pthread_attr_setstacksize(&at, 256 * 1024);
    for (int i = 0; i < threads - 1; i++) pthread_create(&t, &at, serve, NULL);
    fprintf(stderr, "tlsserver: listening on %d with %d threads\n", port, threads);
    serve(NULL);
    return 0;
}
