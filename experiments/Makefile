# Builds the experiment tools against OpenSSL 3.5 (/opt/ossl) and liboqs (/opt/liboqs).
OSSL ?= /opt/ossl
OQS  ?= /opt/liboqs
CFLAGS = -O2 -Wall -Wextra -I$(OSSL)/include -I$(OQS)/include
LDFLAGS = -L$(OSSL)/lib -L$(OQS)/lib -Wl,-rpath,$(OSSL)/lib -Wl,-rpath,$(OQS)/lib

all: bin/tapbridge bin/tlsserver bin/tlsclient bin/flightprobe

bin/tapbridge: src/tapbridge.c
	@mkdir -p bin; $(CC) -O2 -Wall -o $@ $<
bin/tlsserver: src/tlsserver.c
	@mkdir -p bin; $(CC) $(CFLAGS) -o $@ $< $(LDFLAGS) -lssl -lcrypto -lpthread
# -rdynamic exports dapv_submit so that the provider can find it with dlsym.
bin/tlsclient: src/tlsclient.c
	@mkdir -p bin; $(CC) $(CFLAGS) -rdynamic -o $@ $< $(LDFLAGS) -lssl -lcrypto -loqs -lpthread
clean:
	rm -rf bin
bin/flightprobe: src/flightprobe.c
	@mkdir -p bin; $(CC) $(CFLAGS) -o $@ $< $(LDFLAGS) -lssl -lcrypto
