# Set 6 — Sorting and Searching

**40 questions** — High: 16, Medium: 23, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Sorting algorithm): A. Quick sort  B. Merge sort  C. Insertion sort  D. Heap sort  
List II (Worst-case time): I. O(n log n), but not in place  II. O(n²), but O(n log n) on average  III. O(n log n) and in place  IV. O(n²), but O(n) on already sorted input

(1) A-II, B-IV, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-I, C-III, D-IV  
(4) A-I, B-II, C-IV, D-III  

<details><summary>Answer</summary>

**(2)** — Standard complexities of comparison sorts.

</details>

**Q2.** `High`  
Which of the following sorting algorithms are stable in their standard implementations?  
A. Insertion sort  B. Merge sort  C. Quick sort  D. Heap sort  E. Counting sort  
Choose the correct answer from the options given below:

(1) A, B and E only  
(2) B, C and E only  
(3) A, C and D only  
(4) A, B, C and E only  

<details><summary>Answer</summary>

**(1)** — Quick sort and heap sort can change the relative order of equal keys.

</details>

**Q3.** `High`  
The lower bound on the number of comparisons needed by any comparison-based sorting algorithm in the worst case is

(1) Ω(log n)  
(2) Ω(n log n)  
(3) Ω(n²)  
(4) Ω(n)  

<details><summary>Answer</summary>

**(2)** — A decision tree must have at least n! leaves, so its height is at least log2(n!) = Θ(n log n).

</details>

**Q4.** `High`  
The minimum number of comparisons needed in the worst case to sort 5 elements is at least

(1) 10  
(2) 5  
(3) 7  
(4) 8  

<details><summary>Answer</summary>

**(3)** — ⌈log2 5!⌉ = ⌈log2 120⌉ = 7, and 7 comparisons are achievable.

</details>

**Q5.** `High`  
Quick sort, using the first or last element as the pivot, takes O(n²) time when the input is

(1) already sorted  
(2) random  
(3) all distinct  
(4) of even length  

<details><summary>Answer</summary>

**(1)** — Each partition splits off only one element.

</details>

**Q6.** `High`  
The CLRS (Lomuto) PARTITION procedure, using the last element as the pivot, is applied to [2, 8, 7, 1, 3, 5, 6, 4]. The resulting array is

(1) [1, 2, 3, 4, 5, 6, 7, 8]  
(2) [2, 1, 3, 4, 7, 5, 6, 8]  
(3) [3, 1, 2, 4, 7, 5, 6, 8]  
(4) [2, 1, 3, 4, 8, 7, 5, 6]  

<details><summary>Answer</summary>

**(2)** — The pivot 4 ends at index 3 with 2, 1, 3 before it and 7, 5, 6, 8 after it.

</details>

**Q7.** `High`  
After the first pass of bubble sort (ascending) on [5, 1, 4, 2, 8], the array is

(1) [1, 5, 4, 2, 8]  
(2) [1, 2, 4, 5, 8]  
(3) [1, 4, 2, 5, 8]  
(4) [5, 1, 2, 4, 8]  

<details><summary>Answer</summary>

**(3)** — The largest element bubbles to the end: 5 is swapped past 1, 4 and 2.

</details>

**Q8.** `High`  
After two passes of selection sort (ascending) on [64, 25, 12, 22, 11], the array is

(1) [11, 12, 25, 22, 64]  
(2) [11, 25, 12, 22, 64]  
(3) [12, 11, 25, 22, 64]  
(4) [11, 12, 22, 25, 64]  

<details><summary>Answer</summary>

**(1)** — Pass 1 swaps 11 with 64; pass 2 swaps 12 with 25.

</details>

**Q9.** `High`  
The number of element shifts performed by insertion sort on [8, 4, 3, 7, 6, 5, 2, 1] equals the number of inversions, which is

(1) 22  
(2) 28  
(3) 20  
(4) 18  

<details><summary>Answer</summary>

**(1)** — Count pairs out of order: 7 + 3 + 2 + 4 + 3 + 2 + 1 = 22.

</details>

**Q10.** `High`  
Given below are two statements.  
Statement I: Selection sort performs O(n) comparisons in the best case.  
Statement II: Selection sort performs O(n) swaps in the worst case.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Selection sort always makes n(n − 1)/2 comparisons, even on sorted input.

</details>

**Q11.** `High`  
In LSD radix sort of [170, 45, 75, 90, 802, 24, 2, 66], the array after sorting on the units digit is

(1) [170, 90, 2, 802, 24, 45, 75, 66]  
(2) [2, 24, 45, 66, 75, 90, 170, 802]  
(3) [802, 2, 24, 45, 66, 170, 75, 90]  
(4) [170, 90, 802, 2, 24, 45, 75, 66]  

<details><summary>Answer</summary>

**(4)** — A stable sort on the last digit keeps 802 before 2 and 45 before 75.

</details>

**Q12.** `High`  
Counting sort sorts n integers in the range 0 to k in

(1) O(nk)  
(2) O(n + k)  
(3) O(k log n)  
(4) O(n log n)  

<details><summary>Answer</summary>

**(2)** — It is linear when k = O(n), and it is stable.

</details>

**Q13.** `Medium`  
Radix sort on n numbers of d digits in base b, using counting sort for each digit, takes

(1) O(d(n + b))  
(2) O(b^d)  
(3) O(n log n)  
(4) O(n^d)  

<details><summary>Answer</summary>

**(1)** — It is linear when d is constant and b = O(n).

</details>

**Q14.** `Medium`  
Bucket sort runs in linear expected time when

(1) there is one bucket  
(2) the input is sorted in reverse  
(3) the input is uniformly distributed over a range  
(4) all keys are equal  

<details><summary>Answer</summary>

**(3)** — Each bucket then holds O(1) elements on average.

</details>

**Q15.** `High`  
The maximum number of comparisons made by binary search on a sorted array of 1000 elements is

(1) 9  
(2) 500  
(3) 10  
(4) 11  

<details><summary>Answer</summary>

**(3)** — ⌊log2 1000⌋ + 1 = 10.

</details>

**Q16.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Binary search cannot be applied directly to an unsorted array.  
Reason R: Binary search discards half of the elements based on a comparison with the middle element, which is valid only if the array is ordered.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Unsorted data must be sorted first or searched linearly.

</details>

**Q17.** `Medium`  
Interpolation search on uniformly distributed sorted data takes, on average,

(1) O(n)  
(2) O(log n)  
(3) O(1)  
(4) O(log log n)  

<details><summary>Answer</summary>

**(4)** — In the worst case it degrades to O(n).

</details>

**Q18.** `High`  
Merging two sorted lists of m and n elements requires at most how many comparisons?

(1) m + n  
(2) max(m, n)  
(3) m × n  
(4) m + n − 1  

<details><summary>Answer</summary>

**(4)** — Each comparison outputs one element, and the last element needs no comparison.

</details>

**Q19.** `Medium`  
The minimum number of comparisons needed to find both the maximum and minimum of 100 elements is

(1) 150  
(2) 148  
(3) 99  
(4) 198  

<details><summary>Answer</summary>

**(2)** — Process elements in pairs: ⌈3n/2⌉ − 2 = 148.

</details>

**Q20.** `Medium`  
The minimum number of comparisons needed to find the second largest of 64 elements is

(1) 126  
(2) 70  
(3) 68  
(4) 63  

<details><summary>Answer</summary>

**(3)** — A tournament needs n − 1 comparisons for the largest and ⌈log2 n⌉ − 1 more: 63 + 5 = 68.

</details>

**Q21.** `High`  
The kth smallest element of an unsorted array can be found in worst-case linear time using

(1) heap sort  
(2) binary search  
(3) the median-of-medians selection algorithm  
(4) quick sort  

<details><summary>Answer</summary>

**(3)** — Randomized quickselect runs in expected linear time.

</details>

**Q22.** `Medium`  
Match List I with List II.  
List I (Sorting algorithm): A. Bubble sort  B. Selection sort  C. Merge sort  D. Shell sort  
List II (Idea): I. Repeatedly picks the minimum of the unsorted part  II. Repeatedly swaps adjacent out-of-order elements  III. Insertion sort on elements a gap apart, with decreasing gaps  IV. Divides the array, sorts the halves and merges them

(1) A-II, B-I, C-III, D-IV  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-I, C-IV, D-III  
(4) A-I, B-II, C-IV, D-III  

<details><summary>Answer</summary>

**(3)** — Basic ideas of common sorting algorithms.

</details>

**Q23.** `Medium`  
Which sorting algorithm makes the minimum number of swaps in the worst case?

(1) Selection sort  
(2) Insertion sort  
(3) Quick sort  
(4) Bubble sort  

<details><summary>Answer</summary>

**(1)** — It makes at most n − 1 swaps.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: Merge sort needs O(n) extra space for arrays.  
Statement II: Merge sort is well suited to sorting linked lists.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Linked lists can be merged by relinking nodes, and merge sort needs only sequential access.

</details>

**Q25.** `Medium`  
Insertion sort is efficient when the input is

(1) random  
(2) nearly sorted  
(3) very large  
(4) reverse sorted  

<details><summary>Answer</summary>

**(2)** — Its running time is O(n + d), where d is the number of inversions.

</details>

**Q26.** `Medium`  
The worst-case recursion depth of quick sort on n elements is

(1) O(n)  
(2) O(1)  
(3) O(n log n)  
(4) O(log n)  

<details><summary>Answer</summary>

**(1)** — Recursing on the smaller part first limits the stack depth to O(log n).

</details>

**Q27.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Randomized quick sort takes O(n log n) time in the worst case on every input.  
Reason R: A random pivot makes highly unbalanced partitions unlikely regardless of the input order.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — The O(n log n) bound is on the expected time; with very bad luck the worst case is still O(n²).

</details>

**Q28.** `Medium`  
External sorting is used when

(1) the data is already sorted  
(2) the data is very small  
(3) the data has only integers  
(4) the data does not fit in main memory  

<details><summary>Answer</summary>

**(4)** — Sorted runs are created in memory and then merged, often with a k-way merge.

</details>

**Q29.** `Medium`  
The number of passes of a 2-way external merge sort on 64 initial runs is

(1) 8  
(2) 6  
(3) 7  
(4) 5  

<details><summary>Answer</summary>

**(2)** — 64 → 32 → 16 → 8 → 4 → 2 → 1: log2 64 = 6 passes.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: Heap sort has O(n log n) worst-case time.  
Statement II: Quick sort is usually faster than heap sort in practice despite its O(n²) worst case.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Quick sort has better cache behaviour and smaller constants.

</details>

**Q31.** `Medium`  
In the best case, bubble sort with an early-exit flag (stop if no swap in a pass) takes

(1) O(n)  
(2) O(1)  
(3) O(n log n)  
(4) O(n²)  

<details><summary>Answer</summary>

**(1)** — On sorted input, one pass with no swaps suffices.

</details>

**Q32.** `Medium`  
Linear search on an unsorted array of n elements takes, on average for a successful search,

(1) n² comparisons  
(2) log2 n comparisons  
(3) (n + 1)/2 comparisons  
(4) 1 comparison  

<details><summary>Answer</summary>

**(3)** — Each position is equally likely.

</details>

**Q33.** `Low`  
Which sorting algorithm is used by the Unix sort command and many libraries for stable sorting of objects (for example Java's object sort and Python's sort)?

(1) Counting sort  
(2) Heap sort  
(3) A merge-sort variant (Timsort)  
(4) Selection sort  

<details><summary>Answer</summary>

**(3)** — Timsort combines merge sort with insertion sort on runs.

</details>

**Q34.** `Medium`  
Given below are two statements.  
Statement I: Counting sort is a comparison-based algorithm.  
Statement II: Radix sort can sort in linear time because it does not compare keys.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Counting sort uses key values as indices rather than comparing them.

</details>

**Q35.** `Medium`  
The number of comparisons made by merge sort on 8 elements already in ascending order (top-down merge sort) is

(1) 24  
(2) 17  
(3) 12  
(4) 7  

<details><summary>Answer</summary>

**(3)** — Merges of sizes 1+1 (×4), 2+2 (×2) and 4+4 (×1) need 4 × 1 + 2 × 2 + 1 × 4 = 12 comparisons.

</details>

**Q36.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The worst-case time of any comparison sort on n elements is at least log2(n!).  
Reason R: log2(n!) = Θ(n log n) by Stirling's approximation.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but A follows from the decision-tree argument; R only gives the asymptotic size of the bound.

</details>

**Q37.** `Medium`  
Which of the following is an in-place sorting algorithm with O(n log n) worst-case time?

(1) Heap sort  
(2) Counting sort  
(3) Quick sort  
(4) Merge sort  

<details><summary>Answer</summary>

**(1)** — Merge sort needs O(n) extra space; quick sort is O(n²) in the worst case.

</details>

**Q38.** `Medium`  
For which input does insertion sort perform the maximum number of comparisons?

(1) Sorted ascending  
(2) Sorted descending  
(3) All equal  
(4) Random  

<details><summary>Answer</summary>

**(2)** — Every new element must be compared with all previous elements.

</details>

**Q39.** `Medium`  
Sentinel linear search improves performance by

(1) sorting the array  
(2) eliminating the index bound check in each iteration  
(3) using binary search  
(4) reducing memory  

<details><summary>Answer</summary>

**(2)** — The key is placed at the end so the loop is guaranteed to stop.

</details>

**Q40.** `Medium`  
Ternary search on a sorted array of n elements makes about how many comparisons in the worst case compared with binary search?

(1) Exactly the same  
(2) More (about 2 log3 n versus log2 n)  
(3) n/3  
(4) Fewer  

<details><summary>Answer</summary>

**(2)** — 2 log3 n = 1.26 log2 n, so it is slightly worse.

</details>
