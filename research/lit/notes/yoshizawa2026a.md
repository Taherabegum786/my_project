# A Zero-Knowledge Signature Framework for Efficient Post-Quantum Message Authentication in Cooperative Automated Driving (arXiv 2026)
url: https://arxiv.org/abs/2610.11490
read: full
problem: Large PQ public keys and signatures inflate certificate-based V2X authentication, especially for CAMs broadcast at up to 10 Hz on a 20 MHz channel.
method: ZKS-PQC: replace the PQ public key and signature in each message with a compact Bulletproofs zero-knowledge proof, keeping certificate-based trust and ECDSA backward compatibility. Implemented with liboqs and Bulletproofs; evaluated for NIST PQC and additional-round signature candidates.
numbers: message size reduction exceeding 95% for most algorithms; ML-DSA and Falcon reduction 40 to 86%; overhead on the order of milliseconds at sender and receiver in many algorithms; CAM minimum interval 100 ms; tested on Intel Core i7-6600 @2.60GHz (16 GB) laptop and Cohda MK6C OBU (Qualcomm MDM 9150); SPHINCS+ about 10 times slower on MK6C than on the laptop.
limits: Compares PQ signatures within ONE broadcast domain only (V2X CAM); no drone or grid. Handshake-free broadcast is the setting (one-way CAM broadcast, no session setup), but it is not studied as a cross-domain topic. Single OBU vendor; does not establish trust of downstream sensor fusion; some algorithms exceed millisecond overhead.
use-for: v2x
