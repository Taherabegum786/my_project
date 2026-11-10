# Set 5 — Network Security (malware, cryptography, steganography, digital signatures, VPNs, firewalls)

**55 questions** — High: 27, Medium: 27, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
In RSA, p = 3, q = 11 and the public exponent e = 7. The private exponent d is

(1) 7  
(2) 3  
(3) 17  
(4) 13  

<details><summary>Answer</summary>

**(2)** — φ(n) = 2 × 10 = 20; 7 × 3 = 21 ≡ 1 (mod 20), so d = 3.

</details>

**Q2.** `High`  
Using RSA with p = 3, q = 11 and e = 7, the ciphertext for plaintext M = 2 is

(1) 29  
(2) 8  
(3) 17  
(4) 31  

<details><summary>Answer</summary>

**(1)** — C = 2^7 mod 33 = 128 mod 33 = 29.

</details>

**Q3.** `High`  
In an RSA system p = 7, q = 11 and e = 13. The value of d is

(1) 17  
(2) 37  
(3) 43  
(4) 23  

<details><summary>Answer</summary>

**(2)** — φ(n) = 60; 13 × 37 = 481 = 8 × 60 + 1.

</details>

**Q4.** `High`  
In RSA with p = 5 and q = 11, the public key is (e, n) = (3, 55). The private key d is

(1) 27  
(2) 7  
(3) 37  
(4) 13  

<details><summary>Answer</summary>

**(1)** — φ(n) = 40; 3 × 27 = 81 ≡ 1 (mod 40).

</details>

**Q5.** `High`  
In the Diffie-Hellman key exchange the prime is q = 23 and the primitive root is α = 5. If user A selects the private key 6, A's public key is

(1) 2  
(2) 15  
(3) 19  
(4) 8  

<details><summary>Answer</summary>

**(4)** — 5^6 mod 23: 5^2 = 2, 5^4 = 4, so 5^6 = 8.

</details>

**Q6.** `High`  
In a Diffie-Hellman exchange with q = 23 and α = 5, A's private key is 6 and B's private key is 15. The shared secret key is

(1) 8  
(2) 19  
(3) 2  
(4) 13  

<details><summary>Answer</summary>

**(3)** — B's public key is 5^15 mod 23 = 19; K = 19^6 mod 23 = 2.

</details>

**Q7.** `High`  
How many keys are required for 10 users to communicate pairwise using symmetric-key cryptography and using public-key cryptography respectively?

(1) 45 and 10  
(2) 100 and 20  
(3) 90 and 10  
(4) 45 and 20  

<details><summary>Answer</summary>

**(4)** — Symmetric: n(n − 1)/2 = 45 shared keys; asymmetric: one key pair per user = 20 keys.

</details>

**Q8.** `High`  
To create a digital signature the sender signs the message digest with

(1) the sender's private key  
(2) the sender's public key  
(3) the receiver's private key  
(4) the receiver's public key  

<details><summary>Answer</summary>

**(1)** — Anyone can verify it with the sender's public key.

</details>

**Q9.** `High`  
To ensure confidentiality in public-key cryptography, the sender encrypts the message with

(1) the sender's private key  
(2) the receiver's public key  
(3) the sender's public key  
(4) the receiver's private key  

<details><summary>Answer</summary>

**(2)** — Only the receiver's private key can decrypt it.

</details>

**Q10.** `High`  
A digital signature provides which of the following services?  
A. Message authentication  B. Message integrity  C. Non-repudiation  D. Confidentiality  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A, B and C only  
(3) A, B, C and D  
(4) A and D only  

<details><summary>Answer</summary>

**(2)** — A signature alone does not hide the message; confidentiality needs encryption.

</details>

**Q11.** `High`  
Match List I with List II.  
List I (Parameter of DES): A. Block size  B. Effective key size  C. Number of rounds  D. Round key size  
List II (Value): I. 16  II. 48 bits  III. 64 bits  IV. 56 bits

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-I, C-IV, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — DES: 64-bit block, 56-bit key, 16 Feistel rounds, 48-bit round keys.

</details>

**Q12.** `High`  
The number of rounds in AES for key sizes of 128, 192 and 256 bits are respectively

(1) 10, 12 and 14  
(2) 12, 14 and 16  
(3) 16, 16 and 16  
(4) 8, 10 and 12  

<details><summary>Answer</summary>

**(1)** — AES always has a 128-bit block; the rounds depend on the key size.

</details>

**Q13.** `High`  
Which of the following is NOT a transformation in a round of AES?

(1) ShiftRows  
(2) SubBytes  
(3) MixColumns  
(4) Initial permutation  

<details><summary>Answer</summary>

**(4)** — AES rounds use SubBytes, ShiftRows, MixColumns and AddRoundKey; the initial permutation belongs to DES.

</details>

**Q14.** `Medium`  
Given below are two statements.  
Statement I: DES is based on the Feistel cipher structure.  
Statement II: AES is also based on the Feistel cipher structure.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — AES (Rijndael) is a substitution-permutation network, not a Feistel cipher.

</details>

**Q15.** `High`  
Which of the following are asymmetric-key algorithms?  
A. RSA  B. AES  C. ElGamal  D. Blowfish  E. Elliptic curve cryptography  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) A, C, D and E only  
(3) A, C and E only  
(4) B and D only  

<details><summary>Answer</summary>

**(3)** — AES and Blowfish are symmetric block ciphers.

</details>

**Q16.** `High`  
The security of RSA and of Diffie-Hellman rests respectively on the difficulty of

(1) sorting and searching  
(2) the knapsack problem and factoring  
(3) factoring large integers and computing discrete logarithms  
(4) computing discrete logarithms and factoring large integers  

<details><summary>Answer</summary>

**(3)** — RSA: integer factorisation; Diffie-Hellman and ElGamal: discrete logarithm.

</details>

**Q17.** `High`  
The basic Diffie-Hellman key exchange is vulnerable to

(1) a SQL injection attack  
(2) a brute-force attack on DES  
(3) a man-in-the-middle attack  
(4) a birthday attack  

<details><summary>Answer</summary>

**(3)** — It does not authenticate the two parties, so an attacker can sit between them.

</details>

**Q18.** `High`  
Using the Caesar cipher with a key of 3, the plaintext HELLO is encrypted as

(1) IFMMP  
(2) KHOOS  
(3) KHOOR  
(4) EBIIL  

<details><summary>Answer</summary>

**(3)** — Each letter is shifted forward by three positions.

</details>

**Q19.** `Medium`  
Match List I with List II.  
List I (Cipher): A. Caesar cipher  B. Rail fence cipher  C. Vigenère cipher  D. Playfair cipher  
List II (Type): I. Polyalphabetic substitution  II. Digram substitution using a 5 × 5 matrix  III. Monoalphabetic substitution  IV. Transposition

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-I, B-IV, C-III, D-II  

<details><summary>Answer</summary>

**(2)** — Caesar is monoalphabetic, rail fence rearranges letters, Vigenère is polyalphabetic, Playfair encrypts letter pairs.

</details>

**Q20.** `Medium`  
Which cipher is theoretically unbreakable when the key is random, as long as the message and used only once?

(1) Playfair cipher  
(2) Vigenère cipher  
(3) DES  
(4) One-time pad  

<details><summary>Answer</summary>

**(4)** — The one-time pad (Vernam cipher) offers perfect secrecy.

</details>

**Q21.** `High`  
Match List I with List II.  
List I (Hash function): A. MD5  B. SHA-1  C. SHA-256  D. SHA-512  
List II (Digest size): I. 160 bits  II. 512 bits  III. 128 bits  IV. 256 bits

(1) A-III, B-I, C-II, D-IV  
(2) A-III, B-IV, C-I, D-II  
(3) A-I, B-III, C-IV, D-II  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(4)** — MD5 128, SHA-1 160, SHA-256 256, SHA-512 512 bits.

</details>

**Q22.** `Medium`  
A hash function produces an n-bit digest. The effort needed to find a collision using a birthday attack is of the order of

(1) 2^n  
(2) 2^(n/2)  
(3) n^2  
(4) 2n  

<details><summary>Answer</summary>

**(2)** — The birthday paradox halves the exponent for collision search.

</details>

**Q23.** `Medium`  
Which property of a cryptographic hash function states that it is infeasible to find two different messages with the same digest?

(1) Collision resistance  
(2) Preimage resistance  
(3) Second preimage resistance  
(4) Avalanche effect  

<details><summary>Answer</summary>

**(1)** — Collision resistance is also called strong collision resistance.

</details>

**Q24.** `High`  
Match List I with List II.  
List I (Security protocol): A. IPSec  B. SSL/TLS  C. PGP  D. WPA2  
List II (Where it is applied): I. E-mail security  II. Wireless LAN security  III. Network layer  IV. Between the transport and application layers

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-I, C-IV, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(1)** — IPSec secures IP, TLS secures transport connections, PGP secures mail, WPA2 secures Wi-Fi.

</details>

**Q25.** `High`  
Given below are two statements.  
Statement I: The Authentication Header (AH) protocol of IPSec provides source authentication and data integrity but not confidentiality.  
Statement II: The Encapsulating Security Payload (ESP) protocol of IPSec provides confidentiality.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — ESP can provide encryption as well as authentication; AH cannot encrypt.

</details>

**Q26.** `Medium`  
In which IPSec mode is the entire original IP packet, including its header, protected and encapsulated in a new IP packet?

(1) Tunnel mode  
(2) Aggressive mode  
(3) Main mode  
(4) Transport mode  

<details><summary>Answer</summary>

**(1)** — Tunnel mode is used between gateways, e.g. in VPNs; transport mode protects only the payload.

</details>

**Q27.** `High`  
A virtual private network (VPN) is

(1) a physically separate leased-line network  
(2) a private network built over a public network using tunnelling and encryption  
(3) a network without any firewall  
(4) a LAN that uses only private IP addresses  

<details><summary>Answer</summary>

**(2)** — VPNs give privacy over the Internet using protocols such as IPSec, L2TP and PPTP.

</details>

**Q28.** `High`  
Match List I with List II.  
List I (Malware): A. Virus  B. Worm  C. Trojan horse  D. Ransomware  
List II (Characteristic): I. Encrypts the victim's files and demands payment  II. Appears to be a useful program but hides a malicious function  III. Attaches itself to a host program and needs it to spread  IV. Self-replicating, spreads across the network without a host program

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-II, C-IV, D-I  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-II, D-I  

<details><summary>Answer</summary>

**(3)** — Standard definitions of the four malware types.

</details>

**Q29.** `Medium`  
A piece of malicious code that lies dormant until a specific date or condition occurs is called a

(1) keylogger  
(2) logic bomb  
(3) rootkit  
(4) worm  

<details><summary>Answer</summary>

**(2)** — A logic bomb is triggered by an event such as a date or the deletion of a record.

</details>

**Q30.** `Medium`  
Which type of malware hides its presence by modifying the operating system so that it retains privileged access?

(1) Adware  
(2) Rootkit  
(3) Spyware  
(4) Worm  

<details><summary>Answer</summary>

**(2)** — A rootkit conceals itself and other malware at the kernel or system level.

</details>

**Q31.** `High`  
Which of the following are passive attacks?  
A. Traffic analysis  B. Masquerade  C. Release of message contents (eavesdropping)  D. Replay  E. Denial of service  
Choose the correct answer from the options given below:

(1) C and D only  
(2) B, D and E only  
(3) A, B and C only  
(4) A and C only  

<details><summary>Answer</summary>

**(4)** — Passive attacks only observe; masquerade, replay, modification and denial of service are active.

</details>

**Q32.** `High`  
Match List I with List II.  
List I (Attack): A. Eavesdropping  B. Modification of messages  C. Denial of service  D. Masquerade  
List II (Security goal threatened): I. Availability  II. Authentication  III. Confidentiality  IV. Integrity

(1) A-III, B-IV, C-II, D-I  
(2) A-IV, B-III, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — The CIA triad plus authentication.

</details>

**Q33.** `High`  
Match List I with List II.  
List I (Firewall type): A. Packet-filtering firewall  B. Stateful inspection firewall  C. Application-level gateway  D. Circuit-level gateway  
List II (Characteristic): I. Acts as a proxy and inspects application data  II. Relays TCP connections without examining their contents  III. Filters each packet on IP addresses and port numbers  IV. Keeps track of the state of active connections

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-I, B-IV, C-III, D-II  

<details><summary>Answer</summary>

**(2)** — Standard classification of firewalls.

</details>

**Q34.** `Medium`  
A packet-filtering firewall typically makes its decisions using

(1) digital signatures  
(2) the contents of e-mail messages  
(3) source and destination IP addresses, port numbers and protocol type  
(4) user passwords  

<details><summary>Answer</summary>

**(3)** — It examines network- and transport-layer headers only.

</details>

**Q35.** `Medium`  
A perimeter network that hosts an organisation's public servers, separated from both the Internet and the internal network, is called a

(1) demilitarised zone (DMZ)  
(2) virtual LAN  
(3) honeypot  
(4) extranet  

<details><summary>Answer</summary>

**(1)** — The DMZ limits the damage if a public-facing server is compromised.

</details>

**Q36.** `Medium`  
A decoy system designed to attract attackers and study their behaviour is called a

(1) bastion host  
(2) firewall  
(3) proxy  
(4) honeypot  

<details><summary>Answer</summary>

**(4)** — A honeypot diverts attackers from real systems and gathers information about them.

</details>

**Q37.** `High`  
Steganography is the technique of

(1) converting plaintext to ciphertext using a key  
(2) hiding the very existence of a message inside another medium such as an image  
(3) compressing data before transmission  
(4) verifying the identity of the sender  

<details><summary>Answer</summary>

**(2)** — Cryptography hides the meaning of a message; steganography hides its existence.

</details>

**Q38.** `Medium`  
A common technique for image steganography is

(1) increasing the image resolution  
(2) encrypting the image with RSA  
(3) modifying the least significant bits of pixel values  
(4) changing the image file name  

<details><summary>Answer</summary>

**(3)** — LSB substitution changes the image imperceptibly.

</details>

**Q39.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In practice public-key algorithms are used to exchange a session key rather than to encrypt bulk data.  
Reason R: Public-key algorithms are computationally much slower than symmetric-key algorithms.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Hybrid cryptosystems combine the convenience of public-key distribution with the speed of symmetric encryption.

</details>

**Q40.** `Medium`  
Which of the following binds a public key to the identity of its owner and is signed by a certification authority?

(1) Message digest  
(2) Session key  
(3) X.509 digital certificate  
(4) Nonce  

<details><summary>Answer</summary>

**(3)** — X.509 certificates are the basis of public-key infrastructure.

</details>

**Q41.** `Medium`  
Kerberos is

(1) a hashing algorithm  
(2) a firewall architecture  
(3) a public-key encryption algorithm  
(4) an authentication protocol based on symmetric keys, tickets and a key distribution centre  

<details><summary>Answer</summary>

**(4)** — Kerberos uses an authentication server and a ticket-granting server.

</details>

**Q42.** `Medium`  
A nonce (a number used only once) or a timestamp in an authentication protocol protects against

(1) traffic analysis  
(2) dictionary attacks  
(3) replay attacks  
(4) brute-force attacks  

<details><summary>Answer</summary>

**(3)** — An old captured message cannot be reused because its nonce is no longer fresh.

</details>

**Q43.** `Medium`  
The value of Euler's totient function φ(35) is

(1) 24  
(2) 35  
(3) 12  
(4) 34  

<details><summary>Answer</summary>

**(1)** — 35 = 5 × 7, so φ = 4 × 6 = 24.

</details>

**Q44.** `Medium`  
Which block cipher mode of operation encrypts identical plaintext blocks into identical ciphertext blocks?

(1) CBC  
(2) ECB  
(3) CFB  
(4) CTR  

<details><summary>Answer</summary>

**(2)** — Electronic codebook mode encrypts each block independently, so patterns leak.

</details>

**Q45.** `Medium`  
Triple DES with three independent keys has a key length of

(1) 56 bits  
(2) 112 bits  
(3) 128 bits  
(4) 168 bits  

<details><summary>Answer</summary>

**(4)** — 3 × 56 = 168 bits (112 bits with two keys).

</details>

**Q46.** `Medium`  
Which of the following is a stream cipher?

(1) IDEA  
(2) AES  
(3) RC4  
(4) DES  

<details><summary>Answer</summary>

**(3)** — RC4 generates a key stream that is XORed with the plaintext; the others are block ciphers.

</details>

**Q47.** `Medium`  
According to Shannon, the two properties that a good cipher should have are

(1) authentication and integrity  
(2) speed and simplicity  
(3) substitution and compression  
(4) confusion and diffusion  

<details><summary>Answer</summary>

**(4)** — Confusion hides the key-ciphertext relationship; diffusion spreads plaintext statistics.

</details>

**Q48.** `Medium`  
Kerckhoffs's principle states that the security of a cryptosystem should depend on

(1) the secrecy of the algorithm  
(2) the length of the plaintext  
(3) the speed of encryption  
(4) the secrecy of the key only  

<details><summary>Answer</summary>

**(4)** — The algorithm is assumed to be public.

</details>

**Q49.** `Medium`  
An attack in which fraudulent e-mails or websites trick users into revealing passwords or card details is called

(1) war driving  
(2) sniffing  
(3) spoofing of MAC addresses  
(4) phishing  

<details><summary>Answer</summary>

**(4)** — Phishing is a social-engineering attack.

</details>

**Q50.** `Medium`  
Which of the following combines a secret key with a hash function to provide message authentication?

(1) Base64  
(2) HMAC  
(3) MD5 alone  
(4) CRC  

<details><summary>Answer</summary>

**(2)** — An HMAC proves both integrity and that the sender knows the shared key.

</details>

**Q51.** `Medium`  
In a distributed denial-of-service attack

(1) one attacker guesses passwords of many users  
(2) data is silently copied from a server  
(3) many compromised machines flood a target to make it unavailable  
(4) a certificate is forged  

<details><summary>Answer</summary>

**(3)** — A botnet of zombies overwhelms the victim's resources.

</details>

**Q52.** `Medium`  
Given below are two statements.  
Statement I: An intrusion detection system (IDS) monitors traffic and raises alerts on suspicious activity.  
Statement II: An intrusion prevention system (IPS) is placed in-line and can block malicious traffic.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Detection versus active prevention.

</details>

**Q53.** `Medium`  
Which wireless security protocol uses AES-based CCMP for encryption?

(1) WEP  
(2) WPA (TKIP)  
(3) WPA2  
(4) None of these  

<details><summary>Answer</summary>

**(3)** — WEP and TKIP use RC4; WPA2 mandates AES-CCMP.

</details>

**Q54.** `Low`  
An attack that tries every possible key until the correct one is found is a

(1) side-channel attack  
(2) chosen-plaintext attack  
(3) replay attack  
(4) brute-force attack  

<details><summary>Answer</summary>

**(4)** — For DES this needs at most 2^56 trials.

</details>

**Q55.** `Medium`  
In which cryptanalytic attack does the attacker have access to pairs of plaintext and the corresponding ciphertext, but cannot choose them?

(1) Ciphertext-only attack  
(2) Chosen-ciphertext attack  
(3) Known-plaintext attack  
(4) Chosen-plaintext attack  

<details><summary>Answer</summary>

**(3)** — In a chosen-plaintext attack the analyst additionally selects the plaintexts.

</details>
