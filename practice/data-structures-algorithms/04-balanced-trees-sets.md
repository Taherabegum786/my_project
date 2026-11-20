# Set 4 — Balanced Search Trees (AVL, red-black, B, B+, B* trees) and Data Structures for Sets

**33 questions** — High: 15, Medium: 17, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The keys 1, 2, 3, 4, 5, 6, 7 are inserted in that order into an empty AVL tree. The root of the final tree is

(1) 3  
(2) 7  
(3) 4  
(4) 1  

<details><summary>Answer</summary>

**(3)** — Rotations keep the tree balanced, and the result is the perfect tree with root 4.

</details>

**Q2.** `High`  
The keys 10, 20, 30, 40, 50, 25 are inserted in that order into an empty AVL tree. The preorder traversal of the result is

(1) 40 20 10 30 25 50  
(2) 20 10 30 25 40 50  
(3) 30 20 10 25 40 50  
(4) 30 20 25 10 40 50  

<details><summary>Answer</summary>

**(3)** — Inserting 25 unbalances 20 (or the root), and a double (right-left) rotation makes 30 the root.

</details>

**Q3.** `Medium`  
The keys 50, 20, 60, 10, 8, 15, 32, 46, 11, 48 are inserted in that order into an empty AVL tree. The root of the final tree is

(1) 10  
(2) 20  
(3) 50  
(4) 46  

<details><summary>Answer</summary>

**(2)** — After several rotations, 20 becomes the root, with left subtree 10 and right subtree 50.

</details>

**Q4.** `High`  
The minimum number of nodes in an AVL tree of height 4 (a single node has height 0) is

(1) 15  
(2) 12  
(3) 20  
(4) 7  

<details><summary>Answer</summary>

**(2)** — N(h) = N(h − 1) + N(h − 2) + 1 with N(0) = 1 and N(1) = 2: N(2) = 4, N(3) = 7, N(4) = 12.

</details>

**Q5.** `High`  
The minimum number of nodes in an AVL tree of height 5 (a single node has height 0) is

(1) 16  
(2) 33  
(3) 20  
(4) 12  

<details><summary>Answer</summary>

**(3)** — N(5) = N(4) + N(3) + 1 = 12 + 7 + 1 = 20.

</details>

**Q6.** `High`  
The balance factor of every node in an AVL tree must be

(1) −2 to +2  
(2) positive  
(3) 0  
(4) −1, 0 or +1  

<details><summary>Answer</summary>

**(4)** — Balance factor = height of the left subtree − height of the right subtree.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Imbalance case at node z after insertion): A. Left-Left  B. Right-Right  C. Left-Right  D. Right-Left  
List II (Fix): I. Single left rotation at z  II. Single right rotation at z  III. Right rotation at z's right child, then left rotation at z  IV. Left rotation at z's left child, then right rotation at z

(1) A-II, B-I, C-III, D-IV  
(2) A-I, B-II, C-IV, D-III  
(3) A-II, B-I, C-IV, D-III  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — Single rotations fix outside cases; double rotations fix inside cases.

</details>

**Q8.** `High`  
Given below are two statements.  
Statement I: The height of an AVL tree with n nodes is O(log n).  
Statement II: Insertion into an AVL tree may require O(log n) rotations.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Insertion needs at most one single or double rotation; deletion may need O(log n) rotations.

</details>

**Q9.** `Medium`  
The maximum height of an AVL tree with n nodes is approximately

(1) 1.44 log2 n  
(2) 2 log2 n  
(3) log2 n  
(4) n/2  

<details><summary>Answer</summary>

**(1)** — The minimum-node AVL trees are Fibonacci trees, giving about 1.44 log2(n + 2).

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Red-black tree property): A. Root property  B. Red property  C. Black-height property  D. Leaf property  
List II (Statement): I. Every NIL leaf is black  II. Every path from a node to its descendant NIL leaves has the same number of black nodes  III. The root is black  IV. The children of a red node are black

(1) A-IV, B-III, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(3)** — These properties keep the tree approximately balanced.

</details>

**Q11.** `High`  
The height of a red-black tree with n internal nodes is at most

(1) 1.44 log2 n  
(2) 2 log2(n + 1)  
(3) log2 n  
(4) n  

<details><summary>Answer</summary>

**(2)** — The longest path is at most twice the shortest because red nodes cannot be consecutive.

</details>

**Q12.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Red-black trees usually need fewer rotations on insertion and deletion than AVL trees.  
Reason R: Red-black trees are more strictly balanced than AVL trees.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Red-black trees are less strictly balanced, which is why they rebalance less often.

</details>

**Q13.** `High`  
In a B-tree of order m (maximum m children per node), every internal node other than the root has at least

(1) m/4 children  
(2) m − 1 children  
(3) ⌈m/2⌉ children  
(4) 2 children  

<details><summary>Answer</summary>

**(3)** — It therefore has at least ⌈m/2⌉ − 1 keys; the root needs at least 2 children unless it is a leaf.

</details>

**Q14.** `High`  
In a B-tree of order 5, the maximum and minimum numbers of keys in a non-root node are

(1) 4 and 1  
(2) 5 and 3  
(3) 4 and 2  
(4) 5 and 2  

<details><summary>Answer</summary>

**(3)** — At most m − 1 = 4 keys, and at least ⌈5/2⌉ − 1 = 2 keys.

</details>

**Q15.** `High`  
Given below are two statements.  
Statement I: In a B-tree, all leaves are at the same level.  
Statement II: A B-tree grows in height when the root splits.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — B-trees grow upward from the root, which keeps them perfectly height-balanced.

</details>

**Q16.** `High`  
Match List I with List II.  
List I (Tree): A. B tree  B. B+ tree  C. B\* tree  D. 2-3 tree  
List II (Feature): I. Nodes are kept at least two-thirds full by redistributing with siblings before splitting  II. Keys and data may be in any node  III. A B-tree of order 3  IV. All data is in the leaves, which are linked for sequential access

(1) A-II, B-I, C-IV, D-III  
(2) A-IV, B-II, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — Variants of the B-tree.

</details>

**Q17.** `Medium`  
The keys 1, 2, 3, 4, 5 are inserted in that order into an initially empty B-tree of order 3 (2-3 tree). The root of the final tree contains

(1) 2 and 4  
(2) 3  
(3) 4  
(4) 2  

<details><summary>Answer</summary>

**(1)** — Inserting 3 splits [1, 2, 3] with 2 going up; inserting 5 splits [3, 4, 5] with 4 going up.

</details>

**Q18.** `Medium`  
A splay tree performs all of the following operations in O(log n) amortized time. What does a splay operation do?

(1) Moves the accessed node to the root using rotations  
(2) Rebalances the tree using colours  
(3) Deletes the accessed node  
(4) Converts the tree to a heap  

<details><summary>Answer</summary>

**(1)** — Frequently accessed items stay near the root.

</details>

**Q19.** `High`  
In the disjoint-set (union-find) data structure with union by rank and path compression, the amortized time per operation is

(1) O(log log n)  
(2) O(1)  
(3) O(log n)  
(4) O(α(n)), where α is the inverse Ackermann function  

<details><summary>Answer</summary>

**(4)** — α(n) ≤ 4 for all practical values of n.

</details>

**Q20.** `High`  
Match List I with List II.  
List I (Union-find heuristic): A. Union by rank  B. Path compression  C. Linked-list representation with weighted union  
List II (Effect): I. A sequence of m operations on n elements takes O(m + n log n)  II. Makes every node on the find path point directly to the root  III. Attaches the root of the shorter tree under the root of the taller tree

(1) A-II, B-III, C-I  
(2) A-III, B-I, C-II  
(3) A-III, B-II, C-I  
(4) A-I, B-II, C-III  

<details><summary>Answer</summary>

**(3)** — Together, union by rank and path compression give the inverse-Ackermann bound.

</details>

**Q21.** `Medium`  
Union-find is used in Kruskal's algorithm to

(1) check whether two vertices are already in the same component  
(2) sort the edges  
(3) find shortest paths  
(4) store the adjacency list  

<details><summary>Answer</summary>

**(1)** — An edge is added only if its endpoints are in different sets.

</details>

**Q22.** `Medium`  
With union by rank alone (no path compression), the height of any tree in a disjoint-set forest of n elements is at most

(1) log2 n  
(2) n/2  
(3) √n  
(4) 1  

<details><summary>Answer</summary>

**(1)** — A tree of rank r has at least 2^r nodes.

</details>

**Q23.** `Medium`  
Given below are two statements.  
Statement I: Testing membership in a bit-vector set takes O(n) time.  
Statement II: A set over a small universe {0, ..., n − 1} can be represented as a bit vector, with union and intersection done by bitwise OR and AND.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Membership is a single bit test, O(1).

</details>

**Q24.** `Medium`  
In a B+ tree, range queries are efficient because

(1) the tree has height 1  
(2) all internal nodes store data records  
(3) keys are stored in the root  
(4) leaf nodes are linked in key order, so the range is scanned sequentially after one search  

<details><summary>Answer</summary>

**(4)** — This is a key advantage over B-trees for database indexes.

</details>

**Q25.** `Medium`  
The keys 3, 2, 1, 4, 5, 6, 7, 16, 15, 14 are inserted in that order into an empty AVL tree. The root of the resulting tree is

(1) 4  
(2) 3  
(3) 15  
(4) 7  

<details><summary>Answer</summary>

**(1)** — After inserting 14, a double rotation at 6 makes 7 the right child of root 4.

</details>

**Q26.** `Medium`  
The number of rotations needed in the worst case to delete a node from an AVL tree with n nodes is

(1) 1  
(2) O(n)  
(3) O(log n)  
(4) 2  

<details><summary>Answer</summary>

**(3)** — Rebalancing may propagate up to the root.

</details>

**Q27.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: B-trees are preferred for indexes stored on disk.  
Reason R: B-trees were introduced by Bayer and McCreight.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but B-trees suit disks because a node with many keys fills a disk block and keeps the tree shallow.

</details>

**Q28.** `Medium`  
Which of the following trees guarantees O(log n) worst-case time for search, insert and delete?  
A. AVL tree  B. Red-black tree  C. Binary search tree  D. B-tree  
Choose the correct answer from the options given below:

(1) B and C only  
(2) A and C only  
(3) A, B, C and D  
(4) A, B and D only  

<details><summary>Answer</summary>

**(4)** — An unbalanced BST can degenerate into a list.

</details>

**Q29.** `Medium`  
A trie (prefix tree) is most suitable for

(1) implementing priority queues  
(2) sorting integers  
(3) graph traversal  
(4) storing strings for fast prefix search and dictionary look-up  

<details><summary>Answer</summary>

**(4)** — Search time depends on the key length, not the number of keys.

</details>

**Q30.** `Medium`  
A segment tree over an array of n elements supports range-sum queries and point updates each in

(1) O(n log n)  
(2) O(n)  
(3) O(log n)  
(4) O(1)  

<details><summary>Answer</summary>

**(3)** — It needs O(n) space.

</details>

**Q31.** `Low`  
AVL trees are named after

(1) Adelson-Velsky and Landis  
(2) Aho, Vazquez and Lam  
(3) Adams, Venn and Lee  
(4) Allen, Valiant and Lin  

<details><summary>Answer</summary>

**(1)** — They were proposed in 1962 as the first self-balancing BSTs.

</details>

**Q32.** `Medium`  
Given below are two statements.  
Statement I: Every red-black tree is an AVL tree.  
Statement II: The height of a red-black tree with n nodes can be Θ(n).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Red-black trees are less strictly balanced than AVL trees, but their height is still at most 2 log2(n + 1).

</details>

**Q33.** `Medium`  
In a B-tree of order m with n keys, the height is

(1) O(m log n)  
(2) O(n)  
(3) O(log\_m n)  
(4) O(n/m)  

<details><summary>Answer</summary>

**(3)** — Each level multiplies the number of keys by at least about m/2.

</details>
