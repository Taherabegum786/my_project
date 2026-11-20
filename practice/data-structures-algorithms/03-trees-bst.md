# Set 3 — Trees, Binary Trees, Traversals, Threaded Binary Trees and Binary Search Trees

**40 questions** — High: 16, Medium: 23, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A binary tree has preorder traversal A B D E G C F H and inorder traversal D B G E A C H F. Its postorder traversal is

(1) D E G B H F C A  
(2) G E D B H F C A  
(3) D G E B H F C A  
(4) D G E B F H C A  

<details><summary>Answer</summary>

**(3)** — A is the root; the left subtree (D B G E) has root B; the right subtree (C H F) has root C with right child F whose left child is H.

</details>

**Q2.** `Medium`  
A binary tree has preorder A B D H E I C F G and inorder H D B I E A F C G. Its postorder traversal is

(1) H D I E B F G C A  
(2) H I D E B F G C A  
(3) H D I E B G F C A  
(4) D H I E B F G C A  

<details><summary>Answer</summary>

**(1)** — A is the root; B has left child D (with left child H) and right child E (with left child I); C has children F and G.

</details>

**Q3.** `Medium`  
A binary tree has preorder F B A D C E G I H and inorder A B C D E F G H I. Its level-order traversal is

(1) F B A D C E G I H  
(2) F B G A I D C E H  
(3) F G B I A D H C E  
(4) F B G A D I C E H  

<details><summary>Answer</summary>

**(4)** — F is the root with children B and G; B has A and D; D has C and E; G has right child I, which has left child H.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: The preorder and postorder traversals together always uniquely determine a binary tree.  
Statement II: The preorder and inorder traversals together uniquely determine a binary tree with distinct keys.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Preorder and postorder cannot distinguish a single left child from a single right child, unless the tree is full.

</details>

**Q5.** `High`  
A binary tree has 20 leaves. The number of nodes with exactly two children is

(1) 20  
(2) 21  
(3) 19  
(4) 10  

<details><summary>Answer</summary>

**(3)** — In any binary tree, n0 = n2 + 1, so n2 = 19.

</details>

**Q6.** `High`  
The maximum number of nodes in a binary tree of height h (the root at height 0) is

(1) 2^h  
(2) 2^(h+1) − 1  
(3) 2^h − 1  
(4) 2^(h+1)  

<details><summary>Answer</summary>

**(2)** — Level i has at most 2^i nodes: 1 + 2 + ... + 2^h = 2^(h+1) − 1.

</details>

**Q7.** `High`  
The number of structurally different binary trees with 4 nodes is

(1) 16  
(2) 10  
(3) 14  
(4) 12  

<details><summary>Answer</summary>

**(3)** — It is the Catalan number C(4) = 14.

</details>

**Q8.** `High`  
The number of different binary search trees that can be built from the keys 1, 2, 3, 4, 5 is

(1) 120  
(2) 60  
(3) 42  
(4) 24  

<details><summary>Answer</summary>

**(3)** — It is the Catalan number C(5) = 42.

</details>

**Q9.** `Medium`  
The number of different binary trees that can be formed with 3 distinct labelled nodes is

(1) 6  
(2) 15  
(3) 5  
(4) 30  

<details><summary>Answer</summary>

**(4)** — n! × C(n) = 6 × 5 = 30 (5 shapes, each labelled in 3! ways).

</details>

**Q10.** `High`  
A full (strictly) binary tree has 15 internal nodes. Its total number of nodes is

(1) 30  
(2) 31  
(3) 32  
(4) 29  

<details><summary>Answer</summary>

**(2)** — A full binary tree with i internal nodes has i + 1 leaves: 15 + 16 = 31.

</details>

**Q11.** `High`  
In a complete ternary tree (every internal node has exactly 3 children) with 10 internal nodes, the number of leaves is

(1) 31  
(2) 21  
(3) 30  
(4) 20  

<details><summary>Answer</summary>

**(2)** — For a full k-ary tree, leaves = (k − 1) × i + 1 = 2 × 10 + 1 = 21.

</details>

**Q12.** `Medium`  
A binary tree with n nodes has how many NULL child pointers when represented with left and right pointers?

(1) n − 1  
(2) n + 1  
(3) 2n  
(4) n  

<details><summary>Answer</summary>

**(2)** — 2n pointer fields, of which n − 1 point to children.

</details>

**Q13.** `High`  
In a threaded binary tree, the NULL left and right pointers are replaced by pointers to the

(1) inorder predecessor and inorder successor  
(2) leftmost and rightmost leaves  
(3) parent and root  
(4) preorder predecessor and successor  

<details><summary>Answer</summary>

**(1)** — Threads allow inorder traversal without a stack or recursion.

</details>

**Q14.** `High`  
The keys 50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24 are inserted in that order into an empty BST. Its postorder traversal is

(1) 3 8 5 20 24 37 15 58 60 91 62 50  
(2) 3 5 8 15 20 24 37 50 58 60 62 91  
(3) 3 8 5 24 37 20 15 60 58 91 62 50  
(4) 50 15 5 3 8 20 37 24 62 58 60 91  

<details><summary>Answer</summary>

**(3)** — Option 2 is the inorder and option 3 the preorder of the same tree.

</details>

**Q15.** `Medium`  
The keys 50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24 are inserted in that order into an empty BST. The height of the tree (the root at height 0) is

(1) 3  
(2) 4  
(3) 6  
(4) 5  

<details><summary>Answer</summary>

**(2)** — The longest path is 50 → 15 → 20 → 37 → 24.

</details>

**Q16.** `High`  
The preorder traversal of a BST is 30 20 10 15 25 23 39 35 42. Its postorder traversal is

(1) 15 10 23 25 20 35 42 39 30  
(2) 15 23 10 25 20 35 42 39 30  
(3) 15 10 25 23 20 42 35 39 30  
(4) 10 15 20 23 25 30 35 39 42  

<details><summary>Answer</summary>

**(1)** — Rebuild the BST from the preorder sequence: 30 has left subtree 20 (10 → 15, 25 → 23) and right subtree 39 (35, 42).

</details>

**Q17.** `High`  
The inorder traversal of a binary search tree gives

(1) the keys in reverse insertion order  
(2) the keys in sorted (non-decreasing) order  
(3) the keys in random order  
(4) the keys in level order  

<details><summary>Answer</summary>

**(2)** — This is why the inorder traversal of a BST can be used for sorting.

</details>

**Q18.** `High`  
Given below are two statements.  
Statement I: Searching a BST with n nodes takes O(log n) time in the worst case.  
Statement II: Inserting the keys in sorted order into an empty BST produces a tree of height n − 1.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — The worst case for search is O(n), which occurs exactly when the tree degenerates into a chain, as in Statement II.

</details>

**Q19.** `High`  
When deleting a node with two children from a BST, the node is replaced by its

(1) left child always  
(2) root  
(3) inorder successor (or inorder predecessor)  
(4) parent  

<details><summary>Answer</summary>

**(3)** — The successor is the minimum of the right subtree and has at most one child.

</details>

**Q20.** `Medium`  
The keys 7, 5, 1, 8, 3, 6, 0, 9, 4, 2 are inserted in that order into an empty BST. The number of leaf nodes is

(1) 5  
(2) 7  
(3) 6  
(4) 4  

<details><summary>Answer</summary>

**(1)** — The leaves are 0, 2, 4, 6 and 9.

</details>

**Q21.** `High`  
Match List I with List II.  
List I (Traversal): A. Preorder  B. Inorder  C. Postorder  D. Level order  
List II (Order of visiting): I. Left, right, root  II. Root, left, right  III. Level by level, left to right, using a queue  IV. Left, root, right

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(3)** — Depth-first traversals use a stack (or recursion); level order uses a queue.

</details>

**Q22.** `Medium`  
For an expression tree of (a + b) \* (c − d), the postorder traversal gives

(1) a b + c d − \*  
(2) a + b \* c − d  
(3) + a b \* − c d  
(4) \* + a b − c d  

<details><summary>Answer</summary>

**(1)** — Postorder gives the postfix form; preorder gives the prefix form.

</details>

**Q23.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Recursive traversal of a binary tree of height h needs only O(1) extra space.  
Reason R: The recursion stack holds one frame per level along the current path.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Because of R, recursive traversal needs O(h) space; Morris traversal achieves O(1).

</details>

**Q24.** `Medium`  
The minimum height of a binary tree with n nodes (the root at height 0) is

(1) n − 1  
(2) log2 n squared  
(3) ⌈log2(n + 1)⌉ − 1  
(4) ⌊n/2⌋  

<details><summary>Answer</summary>

**(3)** — A tree of height h holds at most 2^(h+1) − 1 nodes.

</details>

**Q25.** `High`  
Match List I with List II.  
List I (Binary tree type): A. Full binary tree  B. Complete binary tree  C. Perfect binary tree  D. Skewed binary tree  
List II (Property): I. All levels filled except possibly the last, which is filled from the left  II. Every node has 0 or 2 children  III. Every internal node has two children and all leaves are at the same level  IV. Every node has only one child, except the single leaf

(1) A-II, B-I, C-III, D-IV  
(2) A-II, B-III, C-I, D-IV  
(3) A-II, B-I, C-IV, D-III  
(4) A-I, B-II, C-III, D-IV  

<details><summary>Answer</summary>

**(1)** — Definitions vary slightly between textbooks; these are the common ones.

</details>

**Q26.** `Medium`  
A general tree is converted to a binary tree using the left-child, right-sibling representation. In the resulting binary tree, the root

(1) has no right child  
(2) has no left child  
(3) is a leaf  
(4) has two children  

<details><summary>Answer</summary>

**(1)** — The root of a tree has no siblings.

</details>

**Q27.** `Medium`  
A forest of trees can be represented as a single binary tree by

(1) it cannot be done  
(2) joining the trees through their leaves  
(3) deleting all leaves  
(4) connecting the roots of the trees as siblings in the left-child, right-sibling representation  

<details><summary>Answer</summary>

**(4)** — The roots of successive trees become right siblings.

</details>

**Q28.** `Medium`  
The number of edges in a tree with n nodes is

(1) n − 1  
(2) n  
(3) n + 1  
(4) 2n  

<details><summary>Answer</summary>

**(1)** — A tree is connected and acyclic.

</details>

**Q29.** `Medium`  
A tree has 4 nodes of degree 3 and 3 nodes of degree 2; all other nodes are leaves (degree 1). The number of leaves is

(1) 5  
(2) 7  
(3) 6  
(4) 4  

<details><summary>Answer</summary>

**(3)** — Sum of degrees = 2(n − 1): 12 + 6 + L = 2(7 + L − 1), giving L = 6.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: Every binary search tree is a heap.  
Statement II: A heap stores the keys so that an inorder traversal yields them in sorted order.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — A BST orders keys left-to-right; a heap orders them only along root-to-leaf paths.

</details>

**Q31.** `Medium`  
Which traversal of a binary tree can be used to delete (free) all its nodes safely?

(1) Level order  
(2) Preorder  
(3) Inorder  
(4) Postorder  

<details><summary>Answer</summary>

**(4)** — Children are freed before their parent.

</details>

**Q32.** `Medium`  
The time complexity of finding the height of a binary tree with n nodes is

(1) O(n)  
(2) O(n²)  
(3) O(log n)  
(4) O(1)  

<details><summary>Answer</summary>

**(1)** — Every node is visited once.

</details>

**Q33.** `Medium`  
What does the following function return for a binary tree?  
int f(Node \*t) { if (t == NULL) return 0; if (t-&gt;left == NULL && t-&gt;right == NULL) return 1; return f(t-&gt;left) + f(t-&gt;right); }

(1) The number of internal nodes  
(2) The number of nodes  
(3) The height  
(4) The number of leaves  

<details><summary>Answer</summary>

**(4)** — It returns 1 for each node with no children and adds the counts of the subtrees.

</details>

**Q34.** `Medium`  
In a binary search tree, the minimum key is found by

(1) following right pointers from the root  
(2) following left pointers from the root until a node with no left child  
(3) checking all leaves  
(4) a level-order traversal  

<details><summary>Answer</summary>

**(2)** — The maximum is found by following right pointers.

</details>

**Q35.** `Medium`  
The inorder successor of a node with a right child in a BST is

(1) its parent  
(2) the root  
(3) the leftmost node of its right subtree  
(4) its right child always  

<details><summary>Answer</summary>

**(3)** — If there is no right child, the successor is the lowest ancestor whose left subtree contains the node.

</details>

**Q36.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A threaded binary tree can be traversed in inorder without a stack.  
Reason R: Threads point to the parent of each node.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Threads point to the inorder predecessor and successor, not to the parent.

</details>

**Q37.** `Medium`  
An expression tree for an arithmetic expression has operators at

(1) the internal nodes  
(2) no nodes  
(3) only the root  
(4) the leaves  

<details><summary>Answer</summary>

**(1)** — Operands are at the leaves.

</details>

**Q38.** `Medium`  
In a complete binary tree with n nodes stored in an array (1-indexed), node i is a leaf if

(1) i = 1  
(2) i &gt; n/2  
(3) i &lt; n/2  
(4) i is even  

<details><summary>Answer</summary>

**(2)** — Its children 2i and 2i + 1 would be beyond n.

</details>

**Q39.** `Low`  
The maximum number of nodes at level k of a binary tree (the root at level 0) is

(1) 2k  
(2) k²  
(3) k  
(4) 2^k  

<details><summary>Answer</summary>

**(4)** — Each level can at most double the number of nodes.

</details>

**Q40.** `Medium`  
Given below are two statements.  
Statement I: The level-order traversal of a binary tree uses a stack.  
Statement II: The postorder traversal of a binary tree visits the root last.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Level-order traversal uses a queue.

</details>
