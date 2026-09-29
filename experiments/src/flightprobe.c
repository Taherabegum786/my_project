/*
 * flightprobe: measure the size of the server's first flight.
 *
 * Performs one TLS 1.3 handshake and prints the number of TCP payload bytes
 * received from the server when SSL_connect returns (tcpi_bytes_received),
 * i.e. ServerHello .. server Finished including record overhead, and the
 * number of data segments received (tcpi_data_segs_in).
 *
 * usage: flightprobe <host> <port> <cafile> <groups>
 */
#include <arpa/inet.h>
#include <linux/tcp.h>
#include <netinet/in.h>
#include <openssl/err.h>
#include <openssl/provider.h>
#include <openssl/ssl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s host port cafile groups\n", argv[0]); return 2; }
    OSSL_PROVIDER_load(NULL, "default");
    OSSL_PROVIDER_load(NULL, "oqsprovider");
    SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
    SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
    if (SSL_CTX_load_verify_locations(ctx, argv[3], NULL) != 1 ||
        SSL_CTX_set1_groups_list(ctx, argv[4]) != 1 ||
        SSL_CTX_set1_sigalgs_list(ctx, "p256_mldsa44:p256_falcon512:p384_mldsa65:"
                                       "p256_sphincssha2128fsimple:ecdsa_secp256r1_sha256:"
                                       "ecdsa_secp384r1_sha384") != 1) {
        ERR_print_errors_fp(stderr);
        return 1;
    }
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a = {.sin_family = AF_INET, .sin_port = htons(atoi(argv[2]))};
    inet_pton(AF_INET, argv[1], &a.sin_addr);
    if (connect(s, (struct sockaddr *)&a, sizeof a)) { perror("connect"); return 1; }
    SSL *ssl = SSL_new(ctx);
    SSL_set_fd(ssl, s);
    if (SSL_connect(ssl) != 1) { ERR_print_errors_fp(stderr); return 1; }
    struct tcp_info ti;
    socklen_t l = sizeof ti;
    getsockopt(s, IPPROTO_TCP, TCP_INFO, &ti, &l);
    printf("%llu %u\n", (unsigned long long)ti.tcpi_bytes_received, ti.tcpi_data_segs_in);
    return 0;
}
