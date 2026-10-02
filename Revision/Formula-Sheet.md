# Exam-Day Formula & Facts Sheet (UGC NET CS)

Read this the evening before and the morning of the exam. Every line here has appeared in past papers.

## Paper 1
| Topic | Must-remember |
|-------|---------------|
| Levels of teaching | Memory–Herbart · Understanding–Morrison · Reflective–Hunt |
| Bloom (revised) | Remember → Understand → Apply → Analyse → Evaluate → Create |
| Evaluation | Formative (during) · Summative (end) · Diagnostic (difficulties) · Placement (before) |
| Research | Type I = reject true H₀ · Type II = accept false H₀ · NOIR scales |
| Plagiarism (UGC 2018) | L0 ≤10% · L1 10–40 · L2 40–60 · L3 >60 |
| Communication | Lasswell 5Ws · Shannon–Weaver noise · Schramm field of experience · Berlo SMCR |
| Logic | A(S) E(S,P) I(–) O(P) distribution · contradictory A–O, E–I |
| Pramanas | Charvaka 1 · Buddhist/Vaisheshika 2 · Samkhya 3 · Nyaya 4 · Prabhakara 5 · Bhatta/Advaita 6 |
| Hetvabhasa | Savyabhichara, Viruddha, Satpratipaksha, Asiddha, Badhita |
| Maths | Net % = a + b + ab/100 · CI − SI (2y) = P(R/100)² · avg speed 2xy/(x+y) |
| DI | 1% = 3.6° · Mode = 3 Median − 2 Mean |
| Environment | SDG 17/169 · EPA 1986 · NAPCC 8 missions · Kyoto 1997 · Paris 2015 · ISA Gurugram · Net zero 2070 |
| Higher Ed | Nalanda–Kumaragupta I · Vikramashila–Dharmapala · Wood 1854 · Radhakrishnan 1948 · Kothari 1964–66 · NEP 2020 (GER 50% by 2035) |

## Discrete Mathematics
```
p → q ≡ ¬p ∨ q ≡ ¬q → ¬p           Boolean functions on n vars: 2^(2ⁿ)
Relations on n: 2^(n²) · reflexive 2^(n²−n) · symmetric 2^(n(n+1)/2) · antisymmetric 2ⁿ·3^(n(n−1)/2)
Onto functions m→n: Σ(−1)ᵏ C(n,k)(n−k)ᵐ        Derangements D4 = 9, D5 = 44
Bell: 1, 1, 2, 5, 15, 52, 203     Catalan: 1, 1, 2, 5, 14, 42, 132
Handshake Σdeg = 2E · V − E + F = 2 · E ≤ 3V − 6 · Cayley nⁿ⁻² · Kₙ edges n(n−1)/2
Lagrange: |H| divides |G| · generators of cyclic Zₙ = φ(n) · Zₙ field ⇔ n prime
Transportation BFS = m + n − 1 · PERT tₑ = (a + 4m + b)/6, σ² = ((b − a)/6)²
```

## Computer Architecture
```
2's complement range: −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1      IEEE single 1|8|23 bias 127 ; double 1|11|52 bias 1023
Hamming parity bits: 2ʳ ≥ m + r + 1
Pipeline: T = (k + n − 1)·t ; speedup → k ; Amdahl S = 1/((1 − f) + f/s)
Cache: hierarchical T = h·tc + (1 − h)(tc + tm) ; parallel T = h·tc + (1 − h)·tm
Address split: direct TAG|LINE|OFFSET · k-way TAG|SET|OFFSET (sets = lines/k)
Disk: avg rotational latency = ½ × 60/RPM
NAND-only XOR = 4 gates · Johnson counter n FF → 2n states · ring n FF → n states
```

## Programming & Graphics
```
Bresenham p0 = 2Δy − Δx ; pk<0 → pk + 2Δy ; else pk + 2Δy − 2Δx
Midpoint circle p0 = 1 − r ; 8-way symmetry ; ellipse 4-way
Frame buffer = W × H × bpp / 8 bytes
Rotation about P: T(P)·R(θ)·T(−P) ; Cohen–Sutherland TBRL ; AND ≠ 0 → reject
Bezier n control points → degree n − 1, global control ; B-spline local control
Gouraud → intensities ; Phong → normals ; Z-buffer → image space
Non-overloadable C++: ::  .  .*  ?:  sizeof
```

## DBMS
```
Super keys with 1 CK of 1 attr among n: 2ⁿ⁻¹ ; two single-attr CKs: 3·2ⁿ⁻²
2NF: no partial dep · 3NF: X superkey OR A prime · BCNF: X superkey
Lossless: (R1 ∩ R2) → R1 or R2 · 3NF lossless + dep-preserving ; BCNF lossless only
Conflict serializable ⇔ precedence graph acyclic · serial schedules = n!
Wait–Die: old waits, young dies · Wound–Wait: old wounds, young waits
B+ internal: p·Pb + (p−1)·K ≤ B · leaf: q(K + Pr) + Pb ≤ B
Support = n(A∪B)/N · Confidence = sup(A∪B)/sup(A) · cuboids 2ⁿ
CAP: choose 2 · HDFS block 128 MB, replication 3
```

## Operating Systems
```
n fork() → 2ⁿ processes · TAT = CT − AT · WT = TAT − BT
Deadlock-free: R ≥ n(k − 1) + 1 · semaphore final = initial − P + V
EAT(TLB) = h(t + m) + (1 − h)(t + 2m) · EAT(page fault) = (1 − p)·ma + p·service
Page table size = (2^LA / page size) × PTE
RM bound n(2^(1/n) − 1) → 0.69 · EDF U ≤ 1
Belady: FIFO only · RAID 5 distributed parity, min 3 disks · RAID 6 two parities, min 4
Inode max ≈ (12 + k + k² + k³) × block, k = block/pointer size
```

## Software Engineering
```
FP = UFP × (0.65 + 0.01 ΣFᵢ), 14 GSCs, VAF 0.65–1.35
EI 3/4/6 · EO 4/5/7 · EQ 3/4/6 · ILF 7/10/15 · EIF 5/7/10
COCOMO basic: organic 2.4,1.05,2.5,0.38 · semi 3.0,1.12,2.5,0.35 · embedded 3.6,1.20,2.5,0.32
V(G) = E − N + 2P = decisions + 1 = regions
Availability = MTTF/(MTTF + MTTR) · RE = P × C · BVA 4n + 1 · paths n(n−1)/2
Cohesion best Functional → worst Coincidental · Coupling best Data → worst Content
```

## Algorithms
```
Master: compare f(n) with n^(log_b a)
Binary tree: n₀ = n₂ + 1 · max nodes height h = 2^(h+1) − 1 · null links n + 1
AVL min nodes: 1, 2, 4, 7, 12, 20, 33 · RB height ≤ 2log(n+1)
Build-heap O(n) · comparison sort Ω(n log n) · min+max 3n/2 − 2
Dijkstra O((V+E)log V) no negative · Bellman–Ford O(VE) · Floyd O(V³) · Kruskal O(E log E)
Matrix chain O(n³) · LCS O(mn) · 0/1 knapsack O(nW) · KMP O(n + m)
SAT first NPC (Cook) · 2-SAT ∈ P · halting NP-hard not NP
```

## TOC & Compilers
```
NFA n → DFA ≤ 2ⁿ · nth-from-end DFA 2ⁿ states
CNF derivation 2n − 1 · GNF n · CYK O(n³)
Regular: closed under all · CFL: not ∩, not complement · DCFL: complement ✔ · RE: complement ✘
L and L̄ RE ⇒ recursive · Halting RE not recursive · Rice: non-trivial language props undecidable
Undecidable for CFG: ambiguity, equivalence, L = Σ*, intersection emptiness
LR(0) ⊂ SLR ⊂ LALR ⊂ CLR · #states LR(0) = SLR = LALR ≤ CLR · LALR merge → only R/R
S-attributed ⊂ L-attributed · live variables backward · reaching defs forward · avail. exprs forward ∩
```

## Networks
```
Nyquist 2B log₂L · Shannon B log₂(1 + SNR) · dB = 10 log₁₀
a = Tp/Tt · η_SW = 1/(1 + 2a) · η = W/(1 + 2a) · GBN 2ⁿ − 1 · SR 2ⁿ⁻¹
Pure ALOHA 18.4% (G = 0.5) · slotted 36.8% (G = 1) · CSMA/CD L_min = 2·Tp·B
Hosts /n = 2^(32−n) − 2 · d_min detect d+1, correct 2t+1
Mesh links n(n−1)/2 · symmetric keys n(n−1)/2 · asymmetric 2n
Token bucket burst = C/(M − ρ) · T1 1.544 Mbps · E1 2.048 Mbps
RIP DV hop 15 UDP 520 · OSPF LS IP 89 · BGP PV TCP 179
DES 64/56/16 · AES 128, keys 128/192/256 → rounds 10/12/14
Ports 20/21 FTP · 22 SSH · 23 Telnet · 25 SMTP · 53 DNS · 67/68 DHCP · 80 HTTP · 110 POP3 · 143 IMAP · 161 SNMP · 443 HTTPS
```

## AI
```
BFS time/space O(b^d) · DFS space O(bm) · IDDFS O(b^d) time, O(bd) space
A*: f = g + h, admissible ⇒ optimal ; h = 0 ⇒ UCS
α–β prune when α ≥ β ; best case O(b^(m/2))
Fuzzy: ∪ max · ∩ min · complement 1 − μ · very = μ² · somewhat = √μ
Perceptron Δw = η(t − y)x · no XOR · sigmoid′ = σ(1 − σ)
Hopfield capacity 0.138N · CF combine CF1 + CF2(1 − CF1) · schemata 3ˡ
```
