# Set 9 — Backtracking, Branch and Bound, and Lower Bound Theory

**27 questions** — High: 10, Medium: 16, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The number of distinct solutions of the 4-queens problem is

(1) 2  
(2) 4  
(3) 1  
(4) 8  

<details><summary>Answer</summary>

**(1)** — The two solutions are mirror images: (2, 4, 1, 3) and (3, 1, 4, 2).

</details>

**Q2.** `High`  
The number of distinct solutions of the 8-queens problem is

(1) 12  
(2) 92  
(3) 64  
(4) 96  

<details><summary>Answer</summary>

**(2)** — There are 92 solutions, of which 12 are distinct up to rotation and reflection.

</details>

**Q3.** `High`  
For the sum-of-subsets problem with w = {5, 10, 12, 13, 15, 18} and target M = 30, the number of solutions is

(1) 4  
(2) 5  
(3) 2  
(4) 3  

<details><summary>Answer</summary>

**(4)** — {5, 10, 15}, {5, 12, 13} and {12, 18}.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: Backtracking explores the state-space tree in depth-first order and abandons a partial solution as soon as it cannot lead to a valid solution.  
Statement II: Branch and bound typically explores the state-space tree using breadth-first or least-cost search and uses bounds to prune nodes.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard descriptions of the two techniques.

</details>

**Q5.** `High`  
Match List I with List II.  
List I (Branch-and-bound strategy): A. FIFO branch and bound  B. LIFO branch and bound  C. Least-cost (LC) branch and bound  
List II (Order in which live nodes are expanded): I. The node with the best estimated cost is expanded next  II. Live nodes are kept in a queue  III. Live nodes are kept in a stack

(1) A-II, B-I, C-III  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — LC search uses a priority queue ordered by a cost function.

</details>

**Q6.** `Medium`  
In backtracking, a function that decides whether a node of the state-space tree can possibly lead to a solution is called a

(1) objective function  
(2) cost function  
(3) bounding function  
(4) hash function  

<details><summary>Answer</summary>

**(3)** — Nodes failing the bounding function are pruned.

</details>

**Q7.** `Medium`  
Which of the following problems is commonly solved by backtracking?  
A. Graph m-colouring  B. Hamiltonian cycle  C. Sum of subsets  D. Minimum spanning tree  
Choose the correct answer from the options given below:

(1) A and D only  
(2) A, B, C and D  
(3) A, B and C only  
(4) B, C and D only  

<details><summary>Answer</summary>

**(3)** — The minimum spanning tree has efficient greedy algorithms.

</details>

**Q8.** `Medium`  
In the m-colouring decision problem solved by backtracking, a vertex is given a colour only if

(1) it has the highest degree  
(2) no adjacent vertex already has that colour  
(3) the graph is a tree  
(4) all vertices are uncoloured  

<details><summary>Answer</summary>

**(2)** — The algorithm backtracks when no colour is valid for the current vertex.

</details>

**Q9.** `Medium`  
In the state-space tree of the n-queens problem with one queen per row, the number of leaf nodes before pruning is

(1) n  
(2) n²  
(3) n^n (or n! if each column is used once)  
(4) 2^n  

<details><summary>Answer</summary>

**(3)** — Backtracking prunes most of these.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Branch and bound is suited to optimization problems such as the travelling salesman problem.  
Reason R: Branch and bound compares the bound at each node with the best solution found so far and discards nodes that cannot do better.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Backtracking, in contrast, is mainly used for decision and enumeration problems.

</details>

**Q11.** `Medium`  
The 15-puzzle is typically solved using

(1) Huffman coding  
(2) Kruskal's algorithm  
(3) LC branch and bound with a cost estimate such as the number of misplaced tiles  
(4) merge sort  

<details><summary>Answer</summary>

**(3)** — Not all initial arrangements are solvable; a parity test decides solvability.

</details>

**Q12.** `High`  
The decision tree for any comparison-based algorithm that sorts n elements must have at least

(1) 2^n leaves  
(2) n² leaves  
(3) n! leaves  
(4) n leaves  

<details><summary>Answer</summary>

**(3)** — Each permutation of the input must lead to a different leaf.

</details>

**Q13.** `High`  
The lower bound on the worst-case number of comparisons for searching a sorted array of n elements by comparisons is

(1) Ω(1)  
(2) Ω(n)  
(3) Ω(n log n)  
(4) Ω(log n)  

<details><summary>Answer</summary>

**(4)** — The decision tree must have at least n + 1 leaves.

</details>

**Q14.** `High`  
Finding the maximum of n elements by comparisons requires at least

(1) log2 n comparisons  
(2) n log n comparisons  
(3) n/2 comparisons  
(4) n − 1 comparisons  

<details><summary>Answer</summary>

**(4)** — Every element except the maximum must lose at least one comparison.

</details>

**Q15.** `Medium`  
The minimum height of a comparison tree that sorts 8 elements is

(1) 24  
(2) 15  
(3) 28  
(4) 16  

<details><summary>Answer</summary>

**(4)** — ⌈log2 8!⌉ = ⌈log2 40320⌉ = ⌈15.3⌉ = 16.

</details>

**Q16.** `Medium`  
Merging two sorted lists of n elements each needs, in the worst case, at least

(1) n log n comparisons  
(2) log n comparisons  
(3) n comparisons  
(4) 2n − 1 comparisons  

<details><summary>Answer</summary>

**(4)** — An adversary argument shows that every adjacent pair in the output must be compared.

</details>

**Q17.** `High`  
Given below are two statements.  
Statement I: The element-uniqueness problem has an Ω(n log n) lower bound in the algebraic decision-tree model.  
Statement II: Computing the convex hull of n points has an Ω(n log n) lower bound, shown by reduction from sorting.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — If convex hull could be found faster, sorting could be done faster by mapping x to (x, x²).

</details>

**Q18.** `Medium`  
Proving a lower bound for problem B by reduction means showing that

(1) B is in P  
(2) B can be solved quickly  
(3) B has no solution  
(4) a problem A with a known lower bound can be transformed into B efficiently, so B must be at least as hard  

<details><summary>Answer</summary>

**(4)** — If B were faster, A could be solved faster too, contradicting A's lower bound.

</details>

**Q19.** `Medium`  
In an adversary argument for a lower bound, the adversary

(1) always gives random answers  
(2) solves the problem  
(3) answers the algorithm's queries so as to force it to do as much work as possible, while staying consistent  
(4) chooses the input in advance  

<details><summary>Answer</summary>

**(3)** — The adversary builds a worst-case input on the fly.

</details>

**Q20.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Merge sort is asymptotically optimal among comparison sorts.  
Reason R: Merge sort uses O(n) extra memory.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but A holds because merge sort's O(n log n) matches the Ω(n log n) lower bound; its memory use is unrelated.

</details>

**Q21.** `Medium`  
Counting sort beats the Ω(n log n) lower bound because

(1) it does not compare keys, using them as array indices instead  
(2) it uses recursion  
(3) its input is always small  
(4) it is a comparison sort  

<details><summary>Answer</summary>

**(1)** — The decision-tree lower bound applies only to comparison sorts.

</details>

**Q22.** `Medium`  
Hamiltonian-cycle backtracking adds a vertex to the path only if

(1) it is adjacent to the last vertex of the path and not yet on the path  
(2) it has the smallest label  
(3) it has been visited before  
(4) it is a leaf  

<details><summary>Answer</summary>

**(1)** — At the end the last vertex must also be adjacent to the start.

</details>

**Q23.** `Medium`  
In the 0/1 knapsack branch-and-bound method, the upper bound at a node is usually computed by

(1) solving the fractional knapsack on the remaining items  
(2) the value of items already chosen  
(3) counting the remaining items  
(4) dynamic programming on all items  

<details><summary>Answer</summary>

**(1)** — The fractional relaxation gives an optimistic bound.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: Backtracking always runs in polynomial time.  
Statement II: Branch and bound always runs in polynomial time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Both can take exponential time in the worst case; pruning helps only in practice.

</details>

**Q25.** `Low`  
The term "state-space tree" refers to

(1) a tree representing all possible partial and complete solutions examined by the algorithm  
(2) the call stack  
(3) a binary search tree  
(4) a heap  

<details><summary>Answer</summary>

**(1)** — Its nodes are problem states and its edges are choices.

</details>

**Q26.** `Medium`  
In a game tree, alpha-beta pruning

(1) explores every node  
(2) skips branches that cannot affect the final minimax decision  
(3) only works for single-player games  
(4) changes the minimax value  

<details><summary>Answer</summary>

**(2)** — With best move ordering it searches about O(b^(d/2)) nodes.

</details>

**Q27.** `Medium`  
The graph m-colouring problem for a graph with n vertices solved by backtracking has a worst-case time of

(1) O(n²)  
(2) O(nm)  
(3) O(m^n × n)  
(4) O(n log m)  

<details><summary>Answer</summary>

**(3)** — There are m^n possible colourings, each checked in O(n) or more.

</details>
