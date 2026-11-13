"""Real broadcast-authentication protocols (sender/receiver, byte framing) over a seeded slot channel.
Crypto: liboqs through ctypes (pqshim.c), Ed25519 and HMAC/SHA-256 through OpenSSL (python-cryptography / hashlib),
erasure code: zfec (systematic Reed-Solomon over GF(256), MDS)."""
