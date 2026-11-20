# Set 13 — Advanced Algorithms: Parallel, Approximation and Randomized Algorithms

**31 questions** — High: 9, Medium: 21, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (PRAM model): A. EREW  B. CREW  C. CRCW  
List II (Memory access rule): I. Several processors may read and write the same cell at the same time, with a rule to resolve write conflicts  II. No two processors may read or write the same cell at the same time  III. Several processors may read the same cell at the same time, but writes must be exclusive

(1) A-II, B-I, C-III  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — CRCW variants include common, arbitrary and priority write rules.

</details>

**Q2.** `High`  
The sum of n numbers can be computed on a PRAM with n/2 processors in

(1) O(1) time  
(2) O(log n) time  
(3) O(n log n) time  
(4) O(n) time  

<details><summary>Answer</summary>

**(2)** — Numbers are added in pairs in a balanced binary tree of depth log2 n.

</details>

**Q3.** `High`  
The speedup and efficiency of a parallel algorithm using p processors are defined as

(1) T1 × Tp and T1/p  
(2) T1/Tp and (T1/Tp)/p  
(3) Tp/T1 and p/Tp  
(4) p/T1 and T1/p  

<details><summary>Answer</summary>

**(2)** — T1 is the best sequential time and Tp the parallel time on p processors.

</details>

**Q4.** `Medium`  
A parallel algorithm takes 100 s on 1 processor and 20 s on 8 processors. Its speedup and efficiency are

(1) 8 and 100%  
(2) 5 and 62.5%  
(3) 20 and 250%  
(4) 5 and 80%  

<details><summary>Answer</summary>

**(2)** — Speedup = 100/20 = 5; efficiency = 5/8 = 62.5%.

</details>

**Q5.** `Medium`  
Brent's theorem states that a computation with total work W and depth (span) D can be executed on p processors in time

(1) W + D × p  
(2) W/p + D  
(3) W × p  
(4) D/p  

<details><summary>Answer</summary>

**(2)** — More precisely, T_p ≤ W/p + D.

</details>

**Q6.** `High`  
Bitonic sort on n elements, as a sorting network, has depth

(1) O(n log n)  
(2) O(log² n)  
(3) O(log n)  
(4) O(n)  

<details><summary>Answer</summary>

**(2)** — It performs O(n log² n) comparisons in total.

</details>

**Q7.** `Medium`  
Odd-even transposition sort on a linear array of n processors sorts n elements in

(1) √n phases  
(2) n phases  
(3) n² phases  
(4) log n phases  

<details><summary>Answer</summary>

**(2)** — Odd and even pairs are compared alternately.

</details>

**Q8.** `Medium`  
The parallel prefix-sum (scan) of n elements can be computed in

(1) O(1) time  
(2) O(log n) time with O(n) work  
(3) O(n) time  
(4) O(n log n) time with O(n²) work  

<details><summary>Answer</summary>

**(2)** — Up-sweep and down-sweep phases each take log n steps.

</details>

**Q9.** `Medium`  
Given below are two statements.  
Statement I: A parallel algorithm is work-optimal if its total work matches the best sequential running time.  
Statement II: Adding more processors always reduces the running time of a parallel algorithm.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The span and communication overhead limit the speedup (see Amdahl's law).

</details>

**Q10.** `Medium`  
On a CREW PRAM with p processors, searching a sorted array of n elements takes

(1) O(log n / log(p + 1))  
(2) O(n/p)  
(3) O(log n)  
(4) O(1)  

<details><summary>Answer</summary>

**(1)** — Each step splits the array into p + 1 parts, so p = 1 gives binary search.

</details>

**Q11.** `High`  
The approximation ratio of the simple maximal-matching algorithm for the minimum vertex-cover problem is

(1) 2  
(2) 1  
(3) 1.5  
(4) log n  

<details><summary>Answer</summary>

**(1)** — Taking both endpoints of every edge in a maximal matching gives a cover at most twice the optimum.

</details>

**Q12.** `High`  
For the travelling salesman problem with the triangle inequality, the MST-based (double-tree) algorithm gives an approximation ratio of

(1) 1.5  
(2) log n  
(3) 1  
(4) 2  

<details><summary>Answer</summary>

**(4)** — Christofides' algorithm improves this to 1.5.

</details>

**Q13.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The general travelling salesman problem (without the triangle inequality) has no polynomial-time constant-factor approximation unless P = NP.  
Reason R: Such an approximation could be used to decide the Hamiltonian-cycle problem in polynomial time.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Give non-graph edges a huge weight; a good approximation would reveal whether a Hamiltonian cycle exists.

</details>

**Q14.** `Medium`  
The greedy algorithm for set cover has an approximation ratio of

(1) H(n) ≈ ln n  
(2) 2  
(3) 1.5  
(4) n  

<details><summary>Answer</summary>

**(1)** — It repeatedly picks the set covering the most uncovered elements.

</details>

**Q15.** `Medium`  
Match List I with List II.  
List I (Term): A. PTAS  B. FPTAS  C. Approximation ratio ρ(n)  
List II (Meaning): I. For every ε > 0, a (1 + ε)-approximation in time polynomial in n and 1/ε  II. For every ε > 0, a (1 + ε)-approximation in time polynomial in n for each fixed ε  III. Bound on the ratio between the cost of the produced solution and the optimal cost

(1) A-II, B-III, C-I  
(2) A-III, B-I, C-II  
(3) A-II, B-I, C-III  
(4) A-I, B-II, C-III  

<details><summary>Answer</summary>

**(3)** — 0/1 knapsack has an FPTAS.

</details>

**Q16.** `Medium`  
The first-fit decreasing heuristic for bin packing uses at most about

(1) 11/9 OPT + constant bins  
(2) 2 OPT bins  
(3) OPT bins  
(4) log n × OPT bins  

<details><summary>Answer</summary>

**(1)** — Simple first fit uses at most about 1.7 OPT bins.

</details>

**Q17.** `High`  
Match List I with List II.  
List I (Randomized algorithm type): A. Las Vegas  B. Monte Carlo  
List II (Property): I. Always gives the correct answer; running time is random  II. Running time is bounded; the answer may be wrong with small probability

(1) A-I, B-II  
(2) A-II, B-I  
(3) Both I  
(4) Both II  

<details><summary>Answer</summary>

**(1)** — Randomized quick sort is Las Vegas; Miller-Rabin is Monte Carlo.

</details>

**Q18.** `High`  
The expected running time of randomized quick sort on any input of n distinct elements is

(1) O(n)  
(2) O(n log n)  
(3) O(log n)  
(4) O(n²)  

<details><summary>Answer</summary>

**(2)** — The expected number of comparisons is about 2n ln n ≈ 1.39 n log2 n.

</details>

**Q19.** `Medium`  
Karger's randomized contraction algorithm finds a minimum cut of a graph with n vertices in one run with probability at least

(1) 2/(n(n − 1))  
(2) 1/n  
(3) 1/2  
(4) 1 − 1/n  

<details><summary>Answer</summary>

**(1)** — Repeating it about n² ln n times makes failure unlikely.

</details>

**Q20.** `Medium`  
Given below are two statements.  
Statement I: Freivalds' algorithm checks whether AB = C for n × n matrices in O(n²) time per trial.  
Statement II: Freivalds' algorithm can wrongly report that AB = C, with probability at most 1/2 per trial when AB ≠ C.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Repeating k trials reduces the error probability to 2^(−k).

</details>

**Q21.** `Medium`  
In the hiring problem with n candidates in random order, the expected number of times a new best candidate is hired is

(1) 1  
(2) n  
(3) n/2  
(4) H(n) ≈ ln n  

<details><summary>Answer</summary>

**(4)** — Candidate i is the best so far with probability 1/i.

</details>

**Q22.** `Medium`  
Match List I with List II.  
List I (Complexity class): A. RP  B. ZPP  C. BPP  
List II (Definition): I. Bounded two-sided error, probability of error at most 1/3  II. One-sided error: never accepts a "no" instance and accepts a "yes" instance with probability at least 1/2  III. Zero error in expected polynomial time (Las Vegas)

(1) A-II, B-III, C-I  
(2) A-II, B-I, C-III  
(3) A-I, B-III, C-II  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(1)** — ZPP = RP ∩ co-RP.

</details>

**Q23.** `Medium`  
The expected search time in a skip list with n elements is

(1) O(1)  
(2) O(√n)  
(3) O(log n)  
(4) O(n)  

<details><summary>Answer</summary>

**(3)** — Each element is promoted to the next level with probability 1/2.

</details>

**Q24.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Randomized algorithms can avoid worst-case inputs that are designed against a deterministic algorithm.  
Reason R: The behaviour of a randomized algorithm depends on random choices made at run time, not only on the input.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — An adversary cannot predict the random pivot of randomized quick sort.

</details>

**Q25.** `Medium`  
The Fisher-Yates algorithm generates a uniformly random permutation of n elements in

(1) O(n) time  
(2) O(n log n) time  
(3) O(n²) time  
(4) O(2^n) time  

<details><summary>Answer</summary>

**(1)** — For i from n down to 2, swap A[i] with A[random(1, i)].

</details>

**Q26.** `Medium`  
Randomized selection (quickselect with random pivots) finds the kth smallest of n elements in

(1) O(log n) expected time  
(2) O(1) time  
(3) O(n) expected time  
(4) O(n log n) worst-case time  

<details><summary>Answer</summary>

**(3)** — Its worst case is O(n²), unlike median of medians.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: An approximation algorithm always finds the optimal solution.  
Statement II: An approximation algorithm runs in polynomial time and returns a solution within a guaranteed factor of the optimum.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Approximation algorithms trade optimality for efficiency.

</details>

**Q28.** `Medium`  
For the MAX-CUT problem, the Goemans-Williamson algorithm based on semidefinite programming achieves an approximation ratio of about

(1) 0.5  
(2) 0.878  
(3) 1  
(4) 0.95  

<details><summary>Answer</summary>

**(2)** — A random cut already achieves 0.5 in expectation.

</details>

**Q29.** `Low`  
In parallel computing, the span (critical path length) of a computation is

(1) the number of processors  
(2) the length of the longest chain of dependent operations  
(3) the memory used  
(4) the total number of operations  

<details><summary>Answer</summary>

**(2)** — It is the running time with infinitely many processors.

</details>

**Q30.** `Medium`  
A Bloom filter with m bits, k hash functions and n inserted elements has a false-positive probability of about

(1) e^(−k)  
(2) (1 − e^(−kn/m))^k  
(3) 1/m  
(4) kn/m  

<details><summary>Answer</summary>

**(2)** — The best k is about (m/n) ln 2.

</details>

**Q31.** `Medium`  
Given below are two statements.  
Statement I: A Monte Carlo algorithm for a decision problem can be converted into one with smaller error probability by repeating it independently.  
Statement II: A Las Vegas algorithm may return an incorrect answer.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A Las Vegas algorithm is always correct; only its running time varies.

</details>
