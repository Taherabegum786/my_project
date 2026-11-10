# Set 1 — Data Communication (signals, channel capacity, encoding, multiplexing, media, error handling)

**67 questions** — High: 23, Medium: 40, Low: 4

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A noiseless channel of bandwidth 3000 Hz transmits a signal with two signal levels. The maximum bit rate of the channel is

(1) 1500 bps  
(2) 3000 bps  
(3) 6000 bps  
(4) 12000 bps  

<details><summary>Answer</summary>

**(3)** — Nyquist: C = 2B log2 L = 2 × 3000 × 1 = 6000 bps.

</details>

**Q2.** `High`  
A channel has a bandwidth of 4 kHz and a signal-to-noise ratio of 15. The maximum achievable data rate is

(1) 8 kbps  
(2) 12 kbps  
(3) 16 kbps  
(4) 60 kbps  

<details><summary>Answer</summary>

**(3)** — Shannon: C = B log2(1 + SNR) = 4000 × log2 16 = 16 kbps.

</details>

**Q3.** `High`  
What is the approximate capacity of a telephone line with a bandwidth of 3 kHz and a signal-to-noise ratio of 30 dB?

(1) 90 kbps  
(2) 10 kbps  
(3) 30 kbps  
(4) 3 kbps  

<details><summary>Answer</summary>

**(3)** — 30 dB = 1000; C = 3000 × log2(1001) ≈ 3000 × 9.97 ≈ 30 kbps.

</details>

**Q4.** `Medium`  
A signal-to-noise ratio of 20 dB corresponds to a power ratio of

(1) 20  
(2) 10  
(3) 100  
(4) 200  

<details><summary>Answer</summary>

**(3)** — SNR(dB) = 10 log10(S/N), so S/N = 10^2 = 100.

</details>

**Q5.** `High`  
A modem uses 16-QAM and transmits at a bit rate of 4800 bps. The baud rate is

(1) 19200 baud  
(2) 300 baud  
(3) 4800 baud  
(4) 1200 baud  

<details><summary>Answer</summary>

**(4)** — 16 = 2^4, so 4 bits per signal element; baud = 4800 / 4 = 1200.

</details>

**Q6.** `High`  
What is the baud rate of standard 10 Mbps Ethernet that uses Manchester encoding?

(1) 40 Mbaud  
(2) 10 Mbaud  
(3) 20 Mbaud  
(4) 5 Mbaud  

<details><summary>Answer</summary>

**(3)** — Manchester uses two signal elements per bit, so the baud rate is twice the bit rate.

</details>

**Q7.** `Medium`  
The propagation delay of a 2000 km link in which the signal travels at 2 × 10^8 m/s is

(1) 100 ms  
(2) 1 ms  
(3) 10 ms  
(4) 4 ms  

<details><summary>Answer</summary>

**(3)** — Tp = distance / speed = 2 × 10^6 / 2 × 10^8 = 10 ms.

</details>

**Q8.** `Medium`  
The transmission time of a 1000-byte frame over a 1 Mbps link is

(1) 1 s  
(2) 8 ms  
(3) 125 µs  
(4) 1 ms  

<details><summary>Answer</summary>

**(2)** — Tt = 8000 bits / 10^6 bps = 8 ms.

</details>

**Q9.** `High`  
A block code has a minimum Hamming distance of 5. It can

(1) detect up to 5 errors and correct up to 2 errors  
(2) detect up to 4 errors and correct up to 2 errors  
(3) detect up to 4 errors and correct up to 4 errors  
(4) detect up to 2 errors and correct up to 1 error  

<details><summary>Answer</summary>

**(2)** — Detection of s errors needs dmin = s + 1; correction of t errors needs dmin = 2t + 1.

</details>

**Q10.** `High`  
How many redundant bits are needed in a Hamming code to correct a single-bit error in a 7-bit data word?

(1) 2  
(2) 4  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(2)** — Need 2^r ≥ m + r + 1; r = 4 gives 16 ≥ 12, while r = 3 gives 8 < 11.

</details>

**Q11.** `High`  
A bit stream 1101011011 is transmitted using the CRC method with generator polynomial x^4 + x + 1. The CRC bits appended to the message are

(1) 0111  
(2) 1001  
(3) 1011  
(4) 1110  

<details><summary>Answer</summary>

**(4)** — Dividing 11010110110000 by 10011 (modulo-2) leaves remainder 1110.

</details>

**Q12.** `High`  
The message 100100 is to be transmitted using CRC with generator 1101. The transmitted frame is

(1) 100100000  
(2) 100100001  
(3) 100100110  
(4) 100100011  

<details><summary>Answer</summary>

**(2)** — 100100000 divided by 1101 (modulo-2) gives remainder 001, which is appended to the data.

</details>

**Q13.** `Medium`  
Using even parity, the parity bit appended to the data unit 1011001 is

(1) 0  
(2) either 0 or 1  
(3) cannot be determined  
(4) 1  

<details><summary>Answer</summary>

**(1)** — The data already has four 1s (an even number), so the parity bit is 0.

</details>

**Q14.** `High`  
Five channels, each with a 100 kHz bandwidth, are to be frequency-division multiplexed with guard bands of 10 kHz between adjacent channels. The minimum bandwidth of the link is

(1) 550 kHz  
(2) 600 kHz  
(3) 540 kHz  
(4) 500 kHz  

<details><summary>Answer</summary>

**(3)** — 5 × 100 + 4 guard bands × 10 = 540 kHz.

</details>

**Q15.** `High`  
In bit-oriented framing with flag 01111110, the data 0111111011111 is transmitted after bit stuffing as

(1) 011111101111101  
(2) 011111011011111  
(3) 01111101011111  
(4) 011111010111110  

<details><summary>Answer</summary>

**(4)** — A 0 is stuffed after every run of five consecutive 1s: 011111 0 10 11111 0.

</details>

**Q16.** `High`  
A voice channel is band-limited to 4 kHz and digitised using PCM with 256 quantisation levels. The bit rate produced is

(1) 56 kbps  
(2) 32 kbps  
(3) 128 kbps  
(4) 64 kbps  

<details><summary>Answer</summary>

**(4)** — Sampling at 2 × 4000 = 8000 samples/s with 8 bits per sample gives 64 kbps.

</details>

**Q17.** `Medium`  
A signal loses half its power while travelling through a medium. The attenuation is approximately

(1) −10 dB  
(2) −1 dB  
(3) −3 dB  
(4) −2 dB  

<details><summary>Answer</summary>

**(3)** — 10 log10(0.5) ≈ −3 dB.

</details>

**Q18.** `Medium`  
The T1 carrier multiplexes 24 voice channels and has a data rate of

(1) 2.048 Mbps  
(2) 1.544 Mbps  
(3) 6.312 Mbps  
(4) 64 kbps  

<details><summary>Answer</summary>

**(2)** — T1 = 24 × 8 bits + 1 framing bit = 193 bits per 125 µs = 1.544 Mbps. E1 is 2.048 Mbps.

</details>

**Q19.** `Medium`  
Light is guided through an optical fibre by the principle of

(1) total internal reflection  
(2) refraction at the core  
(3) dispersion  
(4) diffraction  

<details><summary>Answer</summary>

**(1)** — The core has a higher refractive index than the cladding, so light striking beyond the critical angle is totally reflected.

</details>

**Q20.** `High`  
Match List I with List II.  
List I (Line coding scheme): A. NRZ-I  B. Manchester  C. AMI  D. Differential Manchester  
List II (Property): I. Bipolar; alternate 1s take opposite polarity  II. Transition at the middle of every bit; the direction of the transition encodes the bit  III. Inversion at the start of a bit denotes 1  IV. Mid-bit transition always present; presence or absence of a transition at the start of the bit encodes the bit

(1) A-III, B-IV, C-I, D-II  
(2) A-II, B-III, C-I, D-IV  
(3) A-III, B-II, C-I, D-IV  
(4) A-I, B-II, C-III, D-IV  

<details><summary>Answer</summary>

**(3)** — NRZ-I inverts on 1; Manchester encodes by direction of the mid-bit transition; AMI is bipolar; differential Manchester uses the transition at the bit boundary.

</details>

**Q21.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Manchester encoding provides self-synchronisation between sender and receiver.  
Reason R: In Manchester encoding there is a transition in the middle of every bit interval.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The guaranteed mid-bit transition lets the receiver recover the clock, which is exactly why the code is self-clocking.

</details>

**Q22.** `High`  
Given below are two statements.  
Statement I: The Nyquist bit rate formula gives the theoretical maximum bit rate of a noiseless channel.  
Statement II: According to the Shannon capacity formula, the capacity of a noisy channel can be increased without limit by increasing the number of signal levels.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Shannon capacity depends only on bandwidth and SNR; the number of levels does not appear in it.

</details>

**Q23.** `Medium`  
Match List I with List II.  
List I (Device/system): A. Keyboard to CPU  B. Walkie-talkie  C. Telephone network  
List II (Transmission mode): I. Full-duplex  II. Simplex  III. Half-duplex

(1) A-I, B-III, C-II  
(2) A-II, B-III, C-I  
(3) A-III, B-II, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(2)** — Keyboard input is one-way (simplex), a walkie-talkie alternates direction (half-duplex), telephony is simultaneous both ways (full-duplex).

</details>

**Q24.** `Medium`  
Which of the following is NOT one of the five components of a data communication system?

(1) Transmission medium  
(2) Message  
(3) Protocol  
(4) Topology  

<details><summary>Answer</summary>

**(4)** — The five components are message, sender, receiver, transmission medium and protocol.

</details>

**Q25.** `Medium`  
How many bits are carried by each signal element in QPSK?

(1) 3  
(2) 1  
(3) 4  
(4) 2  

<details><summary>Answer</summary>

**(4)** — QPSK uses four phases, and log2 4 = 2 bits per signal element.

</details>

**Q26.** `Medium`  
A digital signal has eight levels. How many bits are needed per level?

(1) 3  
(2) 8  
(3) 2  
(4) 4  

<details><summary>Answer</summary>

**(1)** — log2 8 = 3 bits per level.

</details>

**Q27.** `Medium`  
A periodic signal is decomposed into five sine waves with frequencies of 100, 300, 500, 700 and 900 Hz. Its bandwidth is

(1) 500 Hz  
(2) 900 Hz  
(3) 800 Hz  
(4) 2500 Hz  

<details><summary>Answer</summary>

**(3)** — Bandwidth = highest − lowest frequency = 900 − 100 = 800 Hz.

</details>

**Q28.** `Low`  
A sine wave has a period of 1 ms. Its frequency is

(1) 1 Hz  
(2) 1 MHz  
(3) 100 Hz  
(4) 1 kHz  

<details><summary>Answer</summary>

**(4)** — f = 1/T = 1 / 10^-3 = 1000 Hz.

</details>

**Q29.** `High`  
A channel has a bandwidth of 1 MHz and a signal-to-noise ratio of 63. The appropriate upper limit on the bit rate is

(1) 1 Mbps  
(2) 6 Mbps  
(3) 4 Mbps  
(4) 63 Mbps  

<details><summary>Answer</summary>

**(2)** — C = 10^6 × log2(64) = 6 Mbps.

</details>

**Q30.** `Medium`  
In which multiplexing technique are time slots allocated dynamically, on demand, so that no slot is wasted on an idle source?

(1) Statistical TDM  
(2) Synchronous TDM  
(3) FDM  
(4) WDM  

<details><summary>Answer</summary>

**(1)** — Statistical (asynchronous) TDM allocates slots only to sources that have data, so each slot carries an address.

</details>

**Q31.** `Medium`  
A two-dimensional parity check can

(1) detect only single-bit errors  
(2) detect and correct all 2-bit errors  
(3) detect all errors of up to 3 bits and correct single-bit errors  
(4) correct all burst errors  

<details><summary>Answer</summary>

**(3)** — Row and column parity locates a single-bit error (so it can be corrected) and detects any 1-, 2- or 3-bit error.

</details>

**Q32.** `Medium`  
In asynchronous serial transmission each 8-bit character is sent with one start bit and one stop bit. The transmission efficiency is

(1) 70%  
(2) 100%  
(3) 88.9%  
(4) 80%  

<details><summary>Answer</summary>

**(4)** — 8 data bits out of 10 transmitted bits = 80%.

</details>

**Q33.** `Medium`  
In a 7-bit Hamming code (4 data bits), the parity bits are placed at positions

(1) 1, 2 and 3  
(2) 1, 3 and 5  
(3) 5, 6 and 7  
(4) 1, 2 and 4  

<details><summary>Answer</summary>

**(4)** — Parity bits occupy the positions that are powers of two: 1, 2, 4.

</details>

**Q34.** `High`  
According to the Nyquist sampling theorem, an analog signal whose highest frequency is f must be sampled at a rate of at least

(1) f / 2  
(2) f  
(3) 2f  
(4) 4f  

<details><summary>Answer</summary>

**(3)** — Sampling at least twice the highest frequency allows exact reconstruction.

</details>

**Q35.** `Medium`  
The wires in a twisted-pair cable are twisted together in order to

(1) increase the tensile strength of the cable  
(2) reduce crosstalk and electromagnetic interference  
(3) increase the data rate by doubling the conductors  
(4) reduce the cost of the cable  

<details><summary>Answer</summary>

**(2)** — Twisting makes both wires pick up nearly equal noise, which cancels at the receiver.

</details>

**Q36.** `Medium`  
A geostationary satellite orbits at an altitude of approximately

(1) 20,200 km  
(2) 2,000 km  
(3) 72,000 km  
(4) 35,786 km  

<details><summary>Answer</summary>

**(4)** — GEO satellites orbit at about 35,786 km above the equator with a 24-hour period.

</details>

**Q37.** `Medium`  
Given below are two statements.  
Statement I: In frequency hopping spread spectrum (FHSS) the carrier frequency hops according to a pseudo-random sequence known to both sender and receiver.  
Statement II: In direct sequence spread spectrum (DSSS) each data bit is replaced by a sequence of chips.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are the defining properties of the two spread-spectrum techniques.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: Baseband transmission sends a digital signal over the channel without changing it to an analog signal.  
Statement II: Broadband transmission requires a low-pass channel starting at zero frequency.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Broadband transmission uses modulation and therefore a band-pass channel; baseband needs the low-pass channel.

</details>

**Q39.** `Medium`  
Wavelength-division multiplexing is conceptually the same as

(1) TDM applied to optical signals  
(2) FDM applied to optical signals  
(3) statistical TDM  
(4) CDM applied to optical signals  

<details><summary>Answer</summary>

**(2)** — WDM combines light sources of different wavelengths (frequencies) on one fibre, i.e. FDM at optical frequencies.

</details>

**Q40.** `High`  
A CRC generator polynomial of degree r detects

(1) only burst errors of length exactly r  
(2) all burst errors of length less than or equal to r  
(3) all burst errors of any length  
(4) only single-bit errors  

<details><summary>Answer</summary>

**(2)** — All bursts of length ≤ r are detected; longer bursts are detected with high probability.

</details>

**Q41.** `Medium`  
Arrange the following guided media in increasing order of bandwidth.  
A. Coaxial cable  B. Optical fibre  C. Twisted-pair cable

(1) C, B, A  
(2) C, A, B  
(3) A, C, B  
(4) B, A, C  

<details><summary>Answer</summary>

**(2)** — Twisted pair < coaxial cable < optical fibre.

</details>

**Q42.** `Medium`  
Which of the following digital-to-analog modulation techniques is the most susceptible to noise?

(1) FSK  
(2) PSK  
(3) ASK  
(4) QPSK  

<details><summary>Answer</summary>

**(3)** — Noise mostly affects amplitude, and ASK carries its information in the amplitude.

</details>

**Q43.** `High`  
Quadrature amplitude modulation (QAM) is a combination of

(1) ASK and FSK  
(2) PSK and PCM  
(3) ASK and PSK  
(4) FSK and PSK  

<details><summary>Answer</summary>

**(3)** — QAM varies both the amplitude and the phase of the carrier.

</details>

**Q44.** `Medium`  
How many bits per sample are transmitted in delta modulation?

(1) 8  
(2) 2  
(3) 1  
(4) It depends on the number of quantisation levels  

<details><summary>Answer</summary>

**(3)** — Delta modulation sends a single bit indicating whether the signal rose or fell since the previous sample.

</details>

**Q45.** `Medium`  
Block coding scheme 4B/5B is used before NRZ-I in 100Base-TX mainly to

(1) double the data rate  
(2) ensure enough transitions for synchronisation  
(3) correct single-bit errors  
(4) compress the data  

<details><summary>Answer</summary>

**(2)** — 4B/5B guarantees no long run of zeros, giving NRZ-I enough transitions; it adds 25% overhead.

</details>

**Q46.** `Medium`  
B8ZS and HDB3 are techniques used for

(1) scrambling long runs of zeros in AMI  
(2) multiplexing  
(3) analog-to-digital conversion  
(4) error correction  

<details><summary>Answer</summary>

**(1)** — Both substitute a run of zeros (8 and 4 respectively) with a pattern containing violations to keep synchronisation.

</details>

**Q47.** `High`  
The 8-bit one's-complement checksum of the two data words 10101001 and 00111001 is

(1) 00011101  
(2) 11100011  
(3) 00011110  
(4) 11100010  

<details><summary>Answer</summary>

**(1)** — The sum is 11100010; its one's complement is 00011101.

</details>

**Q48.** `Medium`  
Given below are two statements.  
Statement I: Throughput of a link can never be greater than its bandwidth in bits per second.  
Statement II: Latency of a network is the sum of propagation time, transmission time, queuing time and processing delay.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Bandwidth is the potential rate, throughput is the achieved rate; latency is the sum of the four delay components.

</details>

**Q49.** `Medium`  
Match List I with List II.  
List I (Impairment): A. Attenuation  B. Distortion  C. Crosstalk  D. Thermal noise  
List II (Description): I. Signal components travel at different speeds and arrive out of phase  II. Random motion of electrons in the conductor  III. Loss of signal energy with distance  IV. Coupling of a signal from one wire onto another

(1) A-I, B-III, C-IV, D-II  
(2) A-II, B-I, C-IV, D-III  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(3)** — Attenuation is energy loss, distortion is change of shape, crosstalk is coupling between wires, thermal noise is from electron motion.

</details>

**Q50.** `Medium`  
A signal is transmitted at 1000 baud using 8-PSK. The bit rate is

(1) 1000 bps  
(2) 125 bps  
(3) 3000 bps  
(4) 8000 bps  

<details><summary>Answer</summary>

**(3)** — 8-PSK carries log2 8 = 3 bits per baud, so 3000 bps.

</details>

**Q51.** `High`  
A noiseless 3 kHz channel has to carry 24 kbps. The minimum number of signal levels required is

(1) 256  
(2) 4  
(3) 16  
(4) 8  

<details><summary>Answer</summary>

**(3)** — 24000 = 2 × 3000 × log2 L gives log2 L = 4, so L = 16.

</details>

**Q52.** `Medium`  
Four sources, each producing 1 kbps, are combined using synchronous TDM with one bit from each source per frame. The duration of a bit on the multiplexed link is

(1) 4 ms  
(2) 250 µs  
(3) 500 µs  
(4) 1 ms  

<details><summary>Answer</summary>

**(2)** — The link carries 4 kbps, so each bit lasts 1/4000 s = 250 µs.

</details>

**Q53.** `Medium`  
Given below are two statements.  
Statement I: Single-mode fibre has a much smaller core diameter than multimode fibre.  
Statement II: Single-mode fibre suffers from greater modal dispersion than multimode fibre.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Single-mode fibre carries one mode, so it has essentially no modal dispersion and supports longer distances.

</details>

**Q54.** `Medium`  
Match List I with List II.  
List I (Unguided medium): A. Radio waves  B. Microwaves  C. Infrared  
List II (Characteristic): I. Cannot penetrate walls; short-range communication  II. Omnidirectional propagation  III. Unidirectional, line-of-sight propagation

(1) A-III, B-II, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-III, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(3)** — Radio waves are omnidirectional, microwaves need line of sight, infrared is confined to a room.

</details>

**Q55.** `Medium`  
In forward error correction (FEC)

(1) the receiver corrects errors using redundant bits without retransmission  
(2) the receiver asks the sender to retransmit corrupted frames  
(3) errors are ignored  
(4) only error detection is possible  

<details><summary>Answer</summary>

**(1)** — FEC adds enough redundancy for the receiver to correct errors itself; ARQ uses retransmission.

</details>

**Q56.** `High`  
A 7-bit Hamming code word (even parity, bit positions numbered 1 to 7 from left to right, parity bits at positions 1, 2 and 4) is received as 1011011. The bit in error is at position

(1) 6  
(2) 5  
(3) 7  
(4) 3  

<details><summary>Answer</summary>

**(3)** — c1 = b1⊕b3⊕b5⊕b7 = 1, c2 = b2⊕b3⊕b6⊕b7 = 1, c4 = b4⊕b5⊕b6⊕b7 = 1; syndrome 111 = 7.

</details>

**Q57.** `Low`  
A device that converts digital data to an analog signal and back is called a

(1) multiplexer  
(2) codec  
(3) modem  
(4) repeater  

<details><summary>Answer</summary>

**(3)** — A modem (modulator-demodulator) does digital-to-analog conversion; a codec converts an analog signal to digital form.

</details>

**Q58.** `Medium`  
Which of the following multiplexing techniques is used for digital signals?

(1) FDM  
(2) WDM  
(3) TDM  
(4) Both FDM and WDM  

<details><summary>Answer</summary>

**(3)** — FDM and WDM are analog techniques; TDM is a digital multiplexing technique.

</details>

**Q59.** `Medium`  
In CDMA, the chip sequences assigned to different stations are

(1) orthogonal to each other  
(2) identical  
(3) random and unknown to the receiver  
(4) complements of each other  

<details><summary>Answer</summary>

**(1)** — The inner product of two different chip sequences is 0, which lets the receiver separate the stations.

</details>

**Q60.** `Medium`  
The maximum data rate of a channel with bandwidth B and a signal-to-noise ratio of 0 is

(1) 2B  
(2) infinite  
(3) B  
(4) 0  

<details><summary>Answer</summary>

**(4)** — C = B log2(1 + 0) = 0; nothing can be received when the signal is completely lost in noise.

</details>

**Q61.** `Medium`  
The E1 carrier has a data rate of

(1) 2.048 Mbps  
(2) 44.736 Mbps  
(3) 8.448 Mbps  
(4) 1.544 Mbps  

<details><summary>Answer</summary>

**(1)** — E1 has 32 slots of 64 kbps each (30 for voice) = 2.048 Mbps.

</details>

**Q62.** `Low`  
Which connector is used with unshielded twisted-pair cable in Ethernet LANs?

(1) RJ-45  
(2) SC  
(3) RJ-11  
(4) BNC  

<details><summary>Answer</summary>

**(1)** — UTP Ethernet uses the 8-pin RJ-45 connector; BNC is used with coaxial cable and SC with fibre.

</details>

**Q63.** `Medium`  
Which of the following statements about a repeater and an amplifier is correct?

(1) A repeater amplifies the signal together with the noise  
(2) An amplifier regenerates the original bit pattern  
(3) A repeater regenerates the signal while an amplifier amplifies both signal and noise  
(4) Both operate at the data link layer  

<details><summary>Answer</summary>

**(3)** — A repeater is a regenerator at the physical layer; an amplifier cannot distinguish signal from noise.

</details>

**Q64.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A cyclic redundancy check can correct single-bit errors in a frame.  
Reason R: CRC is based on modulo-2 binary division.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — CRC is an error-detecting code only; it is indeed computed by modulo-2 division.

</details>

**Q65.** `Medium`  
Which of the following is an example of a polar line coding scheme with no DC-component problem and self-synchronisation?

(1) Manchester  
(2) NRZ-I  
(3) Unipolar NRZ  
(4) NRZ-L  

<details><summary>Answer</summary>

**(1)** — Manchester has a transition in every bit, so there is no baseline wandering or DC component.

</details>

**Q66.** `Medium`  
The minimum bandwidth required for an ASK signal transmitting at 2000 bps (with d = 0, i.e. ideal filtering) in half-duplex mode is

(1) 4000 Hz  
(2) 1000 Hz  
(3) 2000 Hz  
(4) 8000 Hz  

<details><summary>Answer</summary>

**(3)** — For binary ASK, B = (1 + d) × S, with S = 2000 baud, so B = 2000 Hz.

</details>

**Q67.** `Low`  
In data communication, jitter refers to

(1) variation in packet delay  
(2) loss of packets  
(3) the average delay of packets  
(4) corruption of bits  

<details><summary>Answer</summary>

**(1)** — Jitter is the variation in the arrival delay of packets belonging to the same stream.

</details>
