# Set 2 — Linked Lists, Priority Queues and Heaps

**35 questions** — High: 11, Medium: 23, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Operation on a singly linked list of n nodes with only a head pointer): A. Insert at the beginning  B. Search for a key  C. Access the kth node  D. Sort the list with merge sort  
List II (Time): I. O(1)  II. O(n)  III. O(k)  IV. O(n log n)

(1) A-I, B-III, C-II, D-IV  
(2) A-I, B-II, C-IV, D-III  
(3) A-I, B-II, C-III, D-IV  
(4) A-II, B-I, C-III, D-IV  

<details><summary>Answer</summary>

**(3)** — Merge sort suits linked lists because it needs only sequential access.

</details>

**Q2.** `High`  
In a doubly linked list, given a pointer p to a node to be deleted (not the first or last node), which statements delete it?

(1) p-&gt;prev = p-&gt;next; p-&gt;next = p-&gt;prev;  
(2) p-&gt;prev-&gt;next = p-&gt;next; p-&gt;next-&gt;prev = p-&gt;prev;  
(3) p-&gt;next-&gt;next = p-&gt;prev; p-&gt;prev-&gt;prev = p-&gt;next;  
(4) p-&gt;next = NULL; p-&gt;prev = NULL;  

<details><summary>Answer</summary>

**(2)** — The neighbours are linked to each other, bypassing p; deletion takes O(1).

</details>

**Q3.** `High`  
Given below are two statements.  
Statement I: Binary search can be applied efficiently to a sorted singly linked list.  
Statement II: Finding the middle element of a singly linked list requires random access.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — A linked list has no random access, so binary search is inefficient; the middle is found by walking with slow and fast pointers.

</details>

**Q4.** `High`  
Floyd's cycle-finding algorithm detects a loop in a linked list using

(1) sorting the nodes  
(2) a hash table of visited nodes  
(3) two pointers moving at different speeds  
(4) recursion only  

<details><summary>Answer</summary>

**(3)** — The fast pointer moves two steps and the slow pointer one; they meet if and only if there is a cycle.

</details>

**Q5.** `Medium`  
Reversing a singly linked list of n nodes in place requires

(1) O(n) time and O(1) extra space  
(2) O(log n) time  
(3) O(n²) time  
(4) O(1) time  

<details><summary>Answer</summary>

**(1)** — Three pointers (previous, current, next) are moved along the list.

</details>

**Q6.** `Medium`  
In a circular singly linked list with a pointer only to the last node, which operations take O(1) time?  
A. Insert at the beginning  B. Insert at the end  C. Delete the first node  D. Delete the last node  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) A, B, C and D  
(3) C and D only  
(4) A and B only  

<details><summary>Answer</summary>

**(1)** — Deleting the last node needs its predecessor, which requires a traversal.

</details>

**Q7.** `Medium`  
What does the following function print for a linked list 1 → 2 → 3 → 4?  
void f(Node \*h) { if (h == NULL) return; f(h-&gt;next); printf("%d ", h-&gt;data); }

(1) 1 2 3 4  
(2) 4 2  
(3) 1 3  
(4) 4 3 2 1  

<details><summary>Answer</summary>

**(4)** — The recursive call is made before printing, so the values are printed in reverse order.

</details>

**Q8.** `Medium`  
An XOR linked list stores in each node

(1) the XOR of the addresses of the previous and next nodes  
(2) two pointers  
(3) the address of the next node only  
(4) the XOR of the data values  

<details><summary>Answer</summary>

**(1)** — It gives a doubly linked list with one pointer field per node.

</details>

**Q9.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A linked list uses memory more flexibly than an array when the number of elements varies.  
Reason R: Linked list nodes must be stored in consecutive memory locations.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Nodes are allocated individually and need not be contiguous, which is exactly why lists are flexible.

</details>

**Q10.** `High`  
In a max-heap stored in a 1-indexed array, the parent and children of the node at index i are at

(1) i/2, 2i and 2i + 1  
(2) 2i, i/2 and i/2 + 1  
(3) i − 1, i + 1 and i + 2  
(4) i/2, i and i + 1  

<details><summary>Answer</summary>

**(1)** — With 0-based indexing they are (i − 1)/2, 2i + 1 and 2i + 2.

</details>

**Q11.** `High`  
Building a max-heap from the array [4, 1, 3, 2, 16, 9, 10, 14, 8, 7] using the bottom-up BUILD-MAX-HEAP procedure gives

(1) [16, 10, 14, 8, 7, 9, 3, 2, 4, 1]  
(2) [16, 14, 10, 4, 7, 9, 3, 2, 8, 1]  
(3) [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]  
(4) [16, 14, 9, 8, 7, 10, 3, 2, 4, 1]  

<details><summary>Answer</summary>

**(3)** — This is the CLRS example of BUILD-MAX-HEAP.

</details>

**Q12.** `High`  
From the max-heap [16, 14, 10, 8, 7, 9, 3, 2, 4, 1], the maximum is deleted (the last element is moved to the root and sifted down). The resulting heap is

(1) [14, 8, 10, 2, 7, 9, 3, 4, 1]  
(2) [10, 14, 8, 4, 7, 9, 3, 2, 1]  
(3) [14, 10, 8, 7, 4, 9, 3, 2, 1]  
(4) [14, 8, 10, 4, 7, 9, 3, 2, 1]  

<details><summary>Answer</summary>

**(4)** — 1 is moved to the root and swapped with 14, then 8, then 4.

</details>

**Q13.** `High`  
The keys 10, 20, 15, 30, 40 are inserted one by one into an initially empty max-heap. The resulting array is

(1) [40, 30, 20, 15, 10]  
(2) [40, 30, 15, 20, 10]  
(3) [40, 30, 15, 10, 20]  
(4) [40, 20, 30, 10, 15]  

<details><summary>Answer</summary>

**(3)** — After inserting 30: [30, 20, 15, 10]; 40 is added at index 5 and sifts up past 20 and 30.

</details>

**Q14.** `High`  
The time complexity of building a binary heap from n arbitrary elements using the bottom-up method is

(1) O(n)  
(2) O(n log n)  
(3) O(n²)  
(4) O(log n)  

<details><summary>Answer</summary>

**(1)** — Most nodes are near the bottom and need little sifting; the total work is bounded by a convergent series.

</details>

**Q15.** `High`  
Match List I with List II.  
List I (Operation on a binary max-heap): A. Find maximum  B. Insert one element  C. Build a heap from n elements  D. Heap sort of n elements  
List II (Worst-case time): I. O(n log n)  II. O(log n)  III. O(1)  IV. O(n)

(1) A-II, B-III, C-IV, D-I  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-II, C-I, D-IV  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(4)** — Bottom-up heap construction is linear; heap sort performs n delete-max operations.

</details>

**Q16.** `Medium`  
In a max-heap of n distinct elements, the minimum element is found in

(1) the last level only at index n  
(2) one of the leaves, which requires examining about n/2 elements  
(3) the root  
(4) the left child of the root  

<details><summary>Answer</summary>

**(2)** — The minimum must be a leaf, and a heap has ⌈n/2⌉ leaves.

</details>

**Q17.** `Medium`  
The number of leaves in a binary heap with n elements is

(1) ⌊n/2⌋  
(2) n − 1  
(3) ⌈n/2⌉  
(4) log2 n  

<details><summary>Answer</summary>

**(3)** — Nodes ⌊n/2⌋ + 1 to n are leaves.

</details>

**Q18.** `High`  
The number of distinct max-heaps that can be built from the keys 1, 2, 3, 4, 5 is

(1) 16  
(2) 5  
(3) 8  
(4) 20  

<details><summary>Answer</summary>

**(3)** — 5 is the root; the left subtree has 3 nodes and the right 1: C(4, 3) × 2 × 1 = 8.

</details>

**Q19.** `Medium`  
The number of distinct max-heaps that can be built from 7 distinct keys is

(1) 48  
(2) 120  
(3) 80  
(4) 42  

<details><summary>Answer</summary>

**(3)** — C(6, 3) × 2 × 2 = 80 (each 3-node subheap can be arranged in 2 ways).

</details>

**Q20.** `Medium`  
The height of a binary heap with n elements is

(1) n/2  
(2) log2 n squared  
(3) √n  
(4) ⌊log2 n⌋  

<details><summary>Answer</summary>

**(4)** — A heap is a complete binary tree.

</details>

**Q21.** `Medium`  
Given below are two statements.  
Statement I: Heap sort is a stable sorting algorithm.  
Statement II: Heap sort runs in O(n log n) time in the worst case and sorts in place.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Heap sort is not stable, because the swaps move equal keys past each other.

</details>

**Q22.** `Medium`  
k sorted lists containing n elements in total are merged into one sorted list using a min-heap of size k. The time required is

(1) O(n log k)  
(2) O(k log n)  
(3) O(n)  
(4) O(nk)  

<details><summary>Answer</summary>

**(1)** — Each of the n extractions and insertions costs O(log k).

</details>

**Q23.** `Medium`  
The kth smallest element in a binary min-heap of n elements can be found, using an auxiliary heap, in

(1) O(k²)  
(2) O(k log k)  
(3) O(n)  
(4) O(n log n)  

<details><summary>Answer</summary>

**(2)** — Explore only candidates adjacent to removed nodes, keeping at most O(k) items in the auxiliary heap.

</details>

**Q24.** `Medium`  
Match List I with List II.  
List I (Heap variant): A. Binomial heap  B. Fibonacci heap  C. d-ary heap  
List II (Feature): I. Height O(log\_d n), cheaper decrease-key and more expensive delete-min  II. O(1) amortized decrease-key, used to speed up Dijkstra and Prim  III. Collection of binomial trees supporting union in O(log n)

(1) A-III, B-II, C-I  
(2) A-II, B-III, C-I  
(3) A-I, B-II, C-III  
(4) A-III, B-I, C-II  

<details><summary>Answer</summary>

**(1)** — Mergeable heap variants.

</details>

**Q25.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A binary heap is usually stored in an array without pointers.  
Reason R: A heap is a complete binary tree, so the positions of the parent and children can be computed from the index.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Completeness leaves no gaps in the array.

</details>

**Q26.** `Medium`  
In a min-heap stored in an array, which of the following arrays is a valid min-heap?

(1) [2, 1, 3, 4, 5, 6]  
(2) [1, 5, 2, 4, 7, 3]  
(3) [1, 2, 3, 0, 4, 5]  
(4) [1, 3, 2, 7, 4, 5]  

<details><summary>Answer</summary>

**(4)** — In option 2, 5 &gt; 4 (its child); in option 3, 2 &gt; 1; in option 4, 2 &gt; 0.

</details>

**Q27.** `Medium`  
Which of the following is a valid max-heap?

(1) [25, 14, 13, 16, 10, 8, 12]  
(2) [25, 14, 16, 13, 10, 8, 12]  
(3) [25, 14, 12, 13, 10, 8, 16]  
(4) [25, 12, 16, 13, 10, 8, 14]  

<details><summary>Answer</summary>

**(2)** — In option 2, 12 &lt; 13 (its child); in option 3, 12 &lt; 16; in option 4, 14 &lt; 16.

</details>

**Q28.** `Medium`  
A priority queue is most efficiently implemented with

(1) a stack  
(2) a sorted linked list  
(3) a binary heap  
(4) an unsorted array  

<details><summary>Answer</summary>

**(3)** — A heap gives O(log n) insertion and deletion of the maximum.

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: Deleting the maximum from an unsorted array priority queue takes O(1) time.  
Statement II: Inserting into a sorted linked list priority queue takes O(n) time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Deleting the maximum from an unsorted array requires a linear scan to find it.

</details>

**Q30.** `Medium`  
A header node in a linked list is

(1) a node that stores the list length only  
(2) the last node  
(3) a dummy node at the beginning that simplifies insertion and deletion at the front  
(4) the first data node  

<details><summary>Answer</summary>

**(3)** — It removes special cases for an empty list.

</details>

**Q31.** `Medium`  
Polynomials are commonly represented with linked lists in which each node stores

(1) a coefficient, an exponent and a pointer to the next term  
(2) two exponents  
(3) the value of the polynomial at a point  
(4) only the coefficient  

<details><summary>Answer</summary>

**(1)** — Only non-zero terms are stored.

</details>

**Q32.** `Medium`  
In the Josephus problem with n = 7 people in a circle and every 3rd person eliminated, starting the count from person 1, the survivor is

(1) 4  
(2) 7  
(3) 3  
(4) 5  

<details><summary>Answer</summary>

**(1)** — Order of elimination: 3, 6, 2, 7, 5, 1; person 4 survives.

</details>

**Q33.** `Low`  
Which pointer of the last node of a singly linked list is NULL?

(1) head  
(2) prev  
(3) next  
(4) data  

<details><summary>Answer</summary>

**(3)** — In a circular list it points back to the first node instead.

</details>

**Q34.** `Medium`  
The number of pointer fields that must be changed to insert a node between two nodes of a doubly linked list is

(1) 2  
(2) 6  
(3) 3  
(4) 4  

<details><summary>Answer</summary>

**(4)** — The new node's prev and next, the predecessor's next, and the successor's prev.

</details>

**Q35.** `Medium`  
Given below are two statements.  
Statement I: Arrays have better cache locality than linked lists.  
Statement II: Linked lists support O(1) access to the ith element.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Linked list access by position takes O(i).

</details>
