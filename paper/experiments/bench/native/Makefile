# Builds native benchmarks against the scratchpad OpenSSL 3.5.4 (override OSSL=...).
OSSL ?= /tmp/claude-0/-home-user-my-project/4a27d5c9-46a1-5d35-98ec-9a4e85dfb968/scratchpad/opt/ossl35
CFLAGS = -O2 -march=native -Wall -Wno-deprecated-declarations -I$(OSSL)/include
LDFLAGS = -L$(OSSL)/lib -Wl,-rpath,$(OSSL)/lib -lcrypto
BIN ?= build
all: $(BIN)/evp_sigbench $(BIN)/pathverify $(BIN)/issuerbench
$(BIN)/%: %.c
	mkdir -p $(BIN) && $(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)
clean:
	rm -rf $(BIN)
