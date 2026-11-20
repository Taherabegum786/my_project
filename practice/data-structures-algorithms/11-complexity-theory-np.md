# Set 11 — Complexity Theory (P, NP, NP-completeness, NP-hardness and reductions)

**27 questions** — High: 10, Medium: 16, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A problem is NP-complete if

(1) it is in P  
(2) it is in NP and every problem in NP is polynomial-time reducible to it  
(3) it cannot be solved by any algorithm  
(4) it is NP-hard but not in NP  

<details><summary>Answer</summary>

**(2)** — NP-hard problems need not be in NP; NP-complete problems are NP-hard and in NP.

</details>

**Q2.** `High`  
The first problem proved to be NP-complete (by Cook and Levin) is

(1) graph colouring  
(2) Boolean satisfiability (SAT)  
(3) subset sum  
(4) the travelling salesman problem  

<details><summary>Answer</summary>

**(2)** — Cook (1971) and Levin independently proved SAT NP-complete.

</details>

**Q3.** `High`  
Which of the following problems is in P?

(1) Vertex cover  
(2) Hamiltonian cycle  
(3) 2-SAT  
(4) 3-SAT  

<details><summary>Answer</summary>

**(3)** — 2-SAT is solvable in linear time using strongly connected components of the implication graph.

</details>

**Q4.** `High`  
Which of the following problems are NP-complete?  
A. Clique  B. Vertex cover  C. Shortest path between two vertices  D. Subset sum  E. Minimum spanning tree  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A, B and D only  
(3) A, B, C, D and E  
(4) A, C and E only  

<details><summary>Answer</summary>

**(2)** — Shortest path and MST have polynomial-time algorithms.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: If an NP-complete problem can be solved in polynomial time, then P = NP.  
Statement II: If P = NP, then every NP-hard problem can be solved in polynomial time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Some NP-hard problems, such as the halting problem, are undecidable regardless of whether P = NP.

</details>

**Q6.** `High`  
Problem A is NP-complete, and A is polynomial-time reducible to problem B (A ≤p B). Which statement is correct?

(1) B is NP-hard  
(2) B is in P  
(3) A is in P  
(4) B is NP-complete in all cases  

<details><summary>Answer</summary>

**(1)** — B is at least as hard as A; it is NP-complete only if it is also in NP.

</details>

**Q7.** `High`  
If problem A ≤p B and B is in P, then

(1) A is in P  
(2) A is NP-complete  
(3) B is NP-hard  
(4) nothing can be concluded  

<details><summary>Answer</summary>

**(1)** — A can be solved by transforming it to B in polynomial time and solving B.

</details>

**Q8.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The halting problem is NP-hard.  
Reason R: The halting problem is in NP.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Every NP problem reduces to the halting problem, but the halting problem is undecidable, so it is not in NP.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Problem): A. 2-SAT  B. 3-SAT  C. Halting problem  D. Primality testing  
List II (Class): I. Undecidable  II. In P (AKS algorithm, 2002)  III. NP-complete  IV. In P (linear time via SCCs)

(1) A-IV, B-I, C-III, D-II  
(2) A-IV, B-III, C-II, D-I  
(3) A-III, B-IV, C-I, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — Primality testing was shown to be in P by Agrawal, Kayal and Saxena.

</details>

**Q10.** `Medium`  
The 0/1 knapsack problem can be solved in O(nW) time, yet its decision version is NP-complete because

(1) O(nW) is polynomial in the input size  
(2) W can be exponential in the number of bits used to represent it, so O(nW) is pseudo-polynomial  
(3) the problem is undecidable  
(4) knapsack is not in NP  

<details><summary>Answer</summary>

**(2)** — It is weakly NP-complete.

</details>

**Q11.** `High`  
Given below are two statements.  
Statement I: A graph G has a clique of size k if and only if its complement has an independent set of size k.  
Statement II: A set S is a vertex cover of G if and only if V − S is an independent set of G.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — These relationships give simple reductions among clique, independent set and vertex cover.

</details>

**Q12.** `Medium`  
Which of the following is NOT known to be NP-complete?

(1) Set cover (decision version)  
(2) Hamiltonian path  
(3) Graph 3-colouring  
(4) Integer factorization (decision version)  

<details><summary>Answer</summary>

**(4)** — Factoring is in NP ∩ co-NP and is not believed to be NP-complete.

</details>

**Q13.** `Medium`  
The class NP consists of decision problems

(1) that are undecidable  
(2) that cannot be solved in polynomial time  
(3) that are solvable in polynomial time on a deterministic machine  
(4) whose "yes" instances have certificates that can be verified in polynomial time  

<details><summary>Answer</summary>

**(4)** — Equivalently, problems solvable in polynomial time by a non-deterministic Turing machine.

</details>

**Q14.** `Medium`  
Given below are two statements.  
Statement I: It has been proved that P = NP.  
Statement II: It has been proved that P ≠ NP.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — The question is open; it is one of the Clay Millennium Prize Problems.

</details>

**Q15.** `Medium`  
co-NP is the class of problems

(1) that are in P  
(2) that are NP-hard  
(3) whose complements are in NP  
(4) that are not in NP  

<details><summary>Answer</summary>

**(3)** — Tautology (is every assignment satisfying?) is co-NP-complete.

</details>

**Q16.** `Medium`  
If P = NP, then

(1) nothing follows about co-NP  
(2) NP ≠ co-NP  
(3) NP = co-NP  
(4) P ≠ co-NP  

<details><summary>Answer</summary>

**(3)** — P is closed under complement, so P = NP implies NP = co-NP.

</details>

**Q17.** `Medium`  
To prove that a new problem X is NP-complete, it is sufficient to show that

(1) X is in NP and some known NP-complete problem reduces to X in polynomial time  
(2) X is in P  
(3) X has an exponential algorithm  
(4) X reduces to SAT  

<details><summary>Answer</summary>

**(1)** — The reduction must go from the known problem to X.

</details>

**Q18.** `Medium`  
Match List I with List II.  
List I (Problem): A. Travelling salesman (decision)  B. Euler circuit  C. Minimum cut in a network  D. Graph isomorphism  
List II (Status): I. In P by checking that every vertex has even degree (and connectivity)  II. In P via max-flow min-cut  III. NP-complete  IV. In NP, not known to be in P or NP-complete

(1) A-III, B-I, C-II, D-IV  
(2) A-I, B-III, C-II, D-IV  
(3) A-III, B-II, C-I, D-IV  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(1)** — Babai's 2015 result puts graph isomorphism in quasi-polynomial time.

</details>

**Q19.** `Medium`  
A problem is strongly NP-complete if

(1) it has a pseudo-polynomial algorithm  
(2) it is in P  
(3) it is undecidable  
(4) it remains NP-complete even when all numbers in its input are bounded by a polynomial in the input length  

<details><summary>Answer</summary>

**(4)** — Such problems (e.g. 3-partition, TSP) have no pseudo-polynomial algorithm unless P = NP.

</details>

**Q20.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: 3-SAT is NP-complete.  
Reason R: SAT can be reduced to 3-SAT in polynomial time by splitting long clauses using new variables.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — 3-SAT is in NP, and the reduction from SAT shows that it is NP-hard.

</details>

**Q21.** `Medium`  
The decision version of the travelling salesman problem asks whether

(1) there is a tour of total cost at most k  
(2) the graph is connected  
(3) all edges have equal weight  
(4) the graph has an Euler circuit  

<details><summary>Answer</summary>

**(1)** — Optimization versions are NP-hard; decision versions with a bound k are in NP.

</details>

**Q22.** `Medium`  
Which of the following problems can be solved in polynomial time?  
A. Linear programming  B. Integer linear programming  C. Maximum bipartite matching  D. 2-colouring of a graph  
Choose the correct answer from the options given below:

(1) A, B, C and D  
(2) A, C and D only  
(3) A, B and C only  
(4) B and D only  

<details><summary>Answer</summary>

**(2)** — Integer linear programming is NP-hard.

</details>

**Q23.** `Medium`  
Polynomial-time reductions are transitive. This means that

(1) if A ≤p B and B ≤p C, then A ≤p C  
(2) A ≤p B implies A = B  
(3) if A ≤p B then B ≤p A  
(4) every problem reduces to itself in exponential time  

<details><summary>Answer</summary>

**(1)** — Composing two polynomial-time transformations gives a polynomial-time transformation.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: Every problem in P is also in co-NP.  
Statement II: Every NP-complete problem is NP-hard.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — P ⊆ NP ∩ co-NP, and NP-complete problems are NP-hard by definition.

</details>

**Q25.** `Low`  
The question of whether P = NP was formally introduced in 1971 by

(1) Stephen Cook  
(2) Alan Turing  
(3) Donald Knuth  
(4) Edsger Dijkstra  

<details><summary>Answer</summary>

**(1)** — It is one of the Clay Millennium Prize Problems.

</details>

**Q26.** `Medium`  
Which of the following is NP-hard but not known to be in NP?

(1) 3-SAT  
(2) Vertex cover (decision)  
(3) The optimization version of TSP (finding the minimum-cost tour)  
(4) Clique (decision)  

<details><summary>Answer</summary>

**(3)** — An optimization problem is not a decision problem, so it is not in NP as stated.

</details>

**Q27.** `Medium`  
Karp's 1972 paper showed NP-completeness of how many combinatorial problems?

(1) 7  
(2) 50  
(3) 21  
(4) 100  

<details><summary>Answer</summary>

**(3)** — Karp's 21 NP-complete problems include clique, vertex cover, Hamiltonian cycle and knapsack.

</details>
