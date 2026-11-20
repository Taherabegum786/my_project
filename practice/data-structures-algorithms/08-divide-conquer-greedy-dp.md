# Set 8 — Design Techniques: Divide and Conquer, Greedy Algorithms and Dynamic Programming

**38 questions** — High: 17, Medium: 20, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Problem): A. Merge sort  B. Huffman coding  C. Matrix-chain multiplication  D. N-queens  
List II (Design technique): I. Dynamic programming  II. Greedy method  III. Divide and conquer  IV. Backtracking

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-I, C-II, D-IV  
(3) A-II, B-III, C-I, D-IV  
(4) A-III, B-II, C-I, D-IV  

<details><summary>Answer</summary>

**(4)** — Standard classification of algorithms by design technique.

</details>

**Q2.** `High`  
Strassen's algorithm multiplies two 2 × 2 block matrices using

(1) 8 multiplications  
(2) 7 multiplications  
(3) 4 multiplications  
(4) 6 multiplications  

<details><summary>Answer</summary>

**(2)** — It trades one multiplication for extra additions, giving Θ(n^(2.81)).

</details>

**Q3.** `Medium`  
Karatsuba's algorithm multiplies two n-digit numbers using

(1) three half-size multiplications, giving Θ(n^(1.585))  
(2) two half-size multiplications  
(3) four half-size multiplications  
(4) n multiplications  

<details><summary>Answer</summary>

**(1)** — T(n) = 3T(n/2) + O(n).

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: Dynamic programming is applicable when a problem has optimal substructure and overlapping subproblems.  
Statement II: Divide and conquer is most efficient when the subproblems overlap heavily.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Divide and conquer suits independent subproblems; overlapping subproblems are what DP exploits.

</details>

**Q5.** `High`  
The minimum number of scalar multiplications needed to compute the product of matrices with dimensions 10 × 100, 100 × 5 and 5 × 50 is

(1) 25,000  
(2) 5,000  
(3) 75,000  
(4) 7,500  

<details><summary>Answer</summary>

**(4)** — (A1 A2) A3 costs 10·100·5 + 10·5·50 = 5000 + 2500 = 7500; A1 (A2 A3) costs 75,000.

</details>

**Q6.** `High`  
For the matrix chain with dimensions p = (30, 35, 15, 5, 10, 20, 25), the minimum number of scalar multiplications is

(1) 18,000  
(2) 15,125  
(3) 15,000  
(4) 11,875  

<details><summary>Answer</summary>

**(2)** — This is the CLRS example; the optimal parenthesization is ((A1 (A2 A3)) ((A4 A5) A6)).

</details>

**Q7.** `Medium`  
For three matrices of dimensions 10 × 20, 20 × 30 and 30 × 40, the minimum number of scalar multiplications is

(1) 30,000  
(2) 24,000  
(3) 18,000  
(4) 32,000  

<details><summary>Answer</summary>

**(3)** — (A1 A2) A3: 6000 + 12000 = 18,000; A1 (A2 A3): 24000 + 8000 = 32,000.

</details>

**Q8.** `Medium`  
The number of ways to fully parenthesize a product of 4 matrices is

(1) 4  
(2) 6  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(3)** — It is the Catalan number C(n − 1) = C(3) = 5.

</details>

**Q9.** `High`  
The length of the longest common subsequence of "ABCBDAB" and "BDCABA" is

(1) 6  
(2) 5  
(3) 4  
(4) 3  

<details><summary>Answer</summary>

**(3)** — One LCS is BCBA.

</details>

**Q10.** `Medium`  
The length of the longest common subsequence of "AGGTAB" and "GXTXAYB" is

(1) 6  
(2) 3  
(3) 4  
(4) 5  

<details><summary>Answer</summary>

**(3)** — GTAB is a common subsequence of length 4.

</details>

**Q11.** `High`  
The time complexity of the dynamic-programming algorithm for the LCS of strings of lengths m and n is

(1) O(m + n)  
(2) O(mn)  
(3) O(m log n)  
(4) O(2^(m+n))  

<details><summary>Answer</summary>

**(2)** — It fills an (m + 1) × (n + 1) table.

</details>

**Q12.** `High`  
The edit (Levenshtein) distance between "kitten" and "sitting" is

(1) 2  
(2) 4  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(4)** — Substitute k → s, substitute e → i, and insert g.

</details>

**Q13.** `High`  
For the 0/1 knapsack with capacity 50 and items (weight, value) = (10, 60), (20, 100), (30, 120), the maximum value is

(1) 220  
(2) 240  
(3) 160  
(4) 180  

<details><summary>Answer</summary>

**(1)** — Take the items of weight 20 and 30; 240 is the fractional-knapsack optimum.

</details>

**Q14.** `High`  
For the fractional knapsack with capacity 50 and items (weight, value) = (10, 60), (20, 100), (30, 120), the maximum value is

(1) 220  
(2) 280  
(3) 230  
(4) 240  

<details><summary>Answer</summary>

**(4)** — Take items 1 and 2 fully (value 160) and 20/30 of item 3 (value 80).

</details>

**Q15.** `Medium`  
For the 0/1 knapsack with capacity 7 and items (weight, value) = (1, 1), (3, 4), (4, 5), (5, 7), the maximum value is

(1) 10  
(2) 11  
(3) 9  
(4) 8  

<details><summary>Answer</summary>

**(3)** — Items of weight 3 and 4 give value 9.

</details>

**Q16.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The greedy method of choosing items by value-to-weight ratio is optimal for the fractional knapsack problem but not for the 0/1 knapsack problem.  
Reason R: In the 0/1 knapsack, an item cannot be split, so filling the remaining capacity exactly may require a different selection.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — 0/1 knapsack needs dynamic programming (O(nW), pseudo-polynomial).

</details>

**Q17.** `High`  
The dynamic-programming algorithm for 0/1 knapsack with n items and capacity W runs in

(1) O(n log n)  
(2) O(n + W)  
(3) O(nW), which is pseudo-polynomial  
(4) O(2^n) always  

<details><summary>Answer</summary>

**(3)** — It is exponential in the number of bits of W.

</details>

**Q18.** `High`  
Huffman coding for characters with frequencies a: 45, b: 13, c: 12, d: 16, e: 9, f: 5 (per 100 characters) gives an average code length of

(1) 2.5 bits  
(2) 2.24 bits  
(3) 3 bits  
(4) 2.0 bits  

<details><summary>Answer</summary>

**(2)** — Code lengths are a: 1, b, c, d: 3, e, f: 4; total 224 bits per 100 characters.

</details>

**Q19.** `Medium`  
Huffman coding for symbols with probabilities 0.4, 0.2, 0.2, 0.1, 0.1 gives an average code length of

(1) 2.4 bits  
(2) 2.2 bits  
(3) 2.0 bits  
(4) 3.0 bits  

<details><summary>Answer</summary>

**(2)** — One optimal set of lengths is 2, 2, 2, 3, 3: 0.8 + 0.4 + 0.4 + 0.3 + 0.3 = 2.2.

</details>

**Q20.** `High`  
In the activity-selection problem with activities (start, finish): (1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16), the maximum number of compatible activities is

(1) 3  
(2) 5  
(3) 6  
(4) 4  

<details><summary>Answer</summary>

**(4)** — Greedy by earliest finish: (1, 4), (5, 7), (8, 11), (12, 16).

</details>

**Q21.** `High`  
Jobs J1 to J5 have (deadline, profit): (2, 100), (1, 19), (2, 27), (1, 25), (3, 15), and each takes one unit of time. The maximum total profit using greedy job sequencing is

(1) 140  
(2) 152  
(3) 142  
(4) 167  

<details><summary>Answer</summary>

**(3)** — Schedule J3 in slot 1, J1 in slot 2 and J5 in slot 3: 27 + 100 + 15 = 142.

</details>

**Q22.** `Medium`  
Using the optimal merge pattern, sorted files of sizes 20, 30, 10, 5 and 30 records are merged two at a time. The minimum total number of record moves is

(1) 95  
(2) 165  
(3) 240  
(4) 205  

<details><summary>Answer</summary>

**(4)** — Merge 5 + 10 = 15, 15 + 20 = 35, 30 + 30 = 60, 35 + 60 = 95: 15 + 35 + 60 + 95 = 205.

</details>

**Q23.** `High`  
With coin denominations {1, 3, 4} and amount 6, which statement is correct?

(1) Greedy gives 2 coins, which is optimal  
(2) Greedy gives 3 coins (4 + 1 + 1), but the optimum is 2 coins (3 + 3)  
(3) Both give 3 coins  
(4) No solution exists  

<details><summary>Answer</summary>

**(2)** — Greedy coin change is optimal only for special (canonical) coin systems.

</details>

**Q24.** `Medium`  
The number of ways to make change for 5 using coins {1, 2, 5} (unlimited supply, order ignored) is

(1) 6  
(2) 5  
(3) 4  
(4) 3  

<details><summary>Answer</summary>

**(3)** — 5; 2 + 2 + 1; 2 + 1 + 1 + 1; 1 + 1 + 1 + 1 + 1.

</details>

**Q25.** `High`  
Match List I with List II.  
List I (Algorithm): A. Floyd-Warshall  B. Bellman-Ford  C. Kruskal  D. Dijkstra  
List II (Technique): I. Greedy, single-source shortest paths with non-negative weights  II. Dynamic programming, single-source shortest paths with negative weights allowed  III. Dynamic programming, all-pairs shortest paths  IV. Greedy, minimum spanning tree

(1) A-III, B-IV, C-II, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-III, B-II, C-IV, D-I  
(4) A-III, B-II, C-I, D-IV  

<details><summary>Answer</summary>

**(3)** — Techniques behind common graph algorithms.

</details>

**Q26.** `Medium`  
The dynamic-programming solution of the travelling salesman problem (Held-Karp) runs in

(1) O(n³)  
(2) O(n!)  
(3) O(n² 2^n)  
(4) O(2^n)  

<details><summary>Answer</summary>

**(3)** — It is still exponential but much faster than trying all n! tours.

</details>

**Q27.** `Medium`  
The dynamic-programming algorithm for constructing an optimal binary search tree on n keys runs in

(1) O(n³), or O(n²) with Knuth's optimization  
(2) O(2^n)  
(3) O(n²)  
(4) O(n log n)  

<details><summary>Answer</summary>

**(1)** — It fills a table of costs for every range of keys.

</details>

**Q28.** `Medium`  
The longest increasing subsequence of a sequence of n numbers can be found in

(1) O(n^(1.5))  
(2) O(n log n)  
(3) O(n³)  
(4) O(2^n)  

<details><summary>Answer</summary>

**(2)** — The simple DP takes O(n²); patience sorting with binary search takes O(n log n).

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: Memoization is a top-down approach that stores the results of recursive calls.  
Statement II: Tabulation is a bottom-up approach that fills a table iteratively.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are ways of implementing dynamic programming.

</details>

**Q30.** `Medium`  
The principle of optimality states that

(1) an optimal solution contains optimal solutions to its subproblems  
(2) a greedy choice is always optimal  
(3) the optimal solution is unique  
(4) every problem can be solved by divide and conquer  

<details><summary>Answer</summary>

**(1)** — It is the basis of dynamic programming (Bellman).

</details>

**Q31.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A greedy algorithm always produces an optimal solution.  
Reason R: A greedy algorithm makes the locally best choice at each step.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Greedy algorithms are optimal only for problems with the greedy-choice property and optimal substructure.

</details>

**Q32.** `Medium`  
The maximum subarray problem can be solved in linear time by

(1) Huffman coding  
(2) binary search  
(3) Kadane's algorithm  
(4) merge sort  

<details><summary>Answer</summary>

**(3)** — The divide-and-conquer solution takes O(n log n).

</details>

**Q33.** `Medium`  
The closest pair of points among n points in the plane can be found by divide and conquer in

(1) O(n³)  
(2) O(n log n)  
(3) O(n)  
(4) O(n²)  

<details><summary>Answer</summary>

**(2)** — The brute-force method takes O(n²).

</details>

**Q34.** `Medium`  
Given below are two statements.  
Statement I: Dijkstra's algorithm uses dynamic programming with backtracking.  
Statement II: Prim's and Kruskal's algorithms are both greedy.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Dijkstra's algorithm is a greedy algorithm.

</details>

**Q35.** `Medium`  
The number of subproblems solved by the dynamic-programming algorithm for matrix-chain multiplication of n matrices is

(1) O(2^n)  
(2) O(n)  
(3) O(n²)  
(4) O(n³)  

<details><summary>Answer</summary>

**(3)** — One subproblem per pair (i, j) with i ≤ j, each solved in O(n) time, giving O(n³) total.

</details>

**Q36.** `Medium`  
The edit distance between "sunday" and "saturday" is

(1) 4  
(2) 5  
(3) 3  
(4) 2  

<details><summary>Answer</summary>

**(3)** — Insert a, insert t, substitute n → r.

</details>

**Q37.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Huffman coding produces a prefix code.  
Reason R: Huffman's algorithm repeatedly merges the two least frequent nodes using a priority queue.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but the prefix property comes from characters being stored only at the leaves of the tree.

</details>

**Q38.** `Low`  
Binary search is an example of which design technique?

(1) Backtracking  
(2) Divide and conquer (decrease and conquer)  
(3) Greedy  
(4) Dynamic programming  

<details><summary>Answer</summary>

**(2)** — It reduces the problem to one subproblem of half the size.

</details>
