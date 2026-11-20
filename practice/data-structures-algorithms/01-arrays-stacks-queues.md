# Set 1 — Arrays, Sparse Matrices, Stacks and Queues

**40 questions** — High: 13, Medium: 26, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
An array A[1..10][1..15] of 2-byte elements is stored in row-major order starting at address 100. The address of A[5][7] is

(1) 232  
(2) 240  
(3) 228  
(4) 234  

<details><summary>Answer</summary>

**(1)** — 100 + 2 × ((5 − 1) × 15 + (7 − 1)) = 100 + 2 × 66 = 232.

</details>

**Q2.** `High`  
An array A[1..10][1..15] of 2-byte elements is stored in column-major order starting at address 100. The address of A[5][7] is

(1) 236  
(2) 228  
(3) 244  
(4) 232  

<details><summary>Answer</summary>

**(2)** — 100 + 2 × ((7 − 1) × 10 + (5 − 1)) = 100 + 2 × 64 = 228.

</details>

**Q3.** `High`  
An array A[−5..5][2..10] of 4-byte elements is stored in row-major order starting at address 1000. The address of A[0][5] is

(1) 1180  
(2) 1216  
(3) 1192  
(4) 1200  

<details><summary>Answer</summary>

**(3)** — Each row has 9 elements: 1000 + 4 × ((0 − (−5)) × 9 + (5 − 2)) = 1000 + 4 × 48 = 1192.

</details>

**Q4.** `Medium`  
A lower-triangular 10 × 10 matrix is stored row by row, keeping only the elements on and below the diagonal. The number of elements stored is

(1) 50  
(2) 45  
(3) 55  
(4) 100  

<details><summary>Answer</summary>

**(3)** — n(n + 1)/2 = 10 × 11 / 2 = 55.

</details>

**Q5.** `Medium`  
Elements on and below the diagonal of a lower-triangular matrix A[1..n][1..n] are stored row by row in a one-dimensional array starting at index 0. The index of A[5][3] is

(1) 13  
(2) 15  
(3) 10  
(4) 12  

<details><summary>Answer</summary>

**(4)** — Rows 1 to 4 hold 1 + 2 + 3 + 4 = 10 elements, so A[5][3] is at 10 + (3 − 1) = 12.

</details>

**Q6.** `Medium`  
In the triplet (row, column, value) representation of a sparse matrix with t non-zero elements, including one header triplet for the dimensions, the number of values stored is

(1) 3t  
(2) t + 3  
(3) 2t + 1  
(4) 3(t + 1)  

<details><summary>Answer</summary>

**(4)** — The header stores the number of rows, columns and non-zero elements.

</details>

**Q7.** `High`  
The value of the postfix expression 6 2 3 + − 3 8 2 / + * 2 ^ 3 + is

(1) 55  
(2) 52  
(3) 64  
(4) 49  

<details><summary>Answer</summary>

**(2)** — 6 − 5 = 1; 8/2 + 3 = 7; 1 × 7 = 7; 7^2 = 49; 49 + 3 = 52.

</details>

**Q8.** `High`  
The value of the postfix expression 5 6 2 + * 12 4 / − is

(1) 43  
(2) 37  
(3) 46  
(4) 40  

<details><summary>Answer</summary>

**(2)** — 5 × (6 + 2) = 40; 12/4 = 3; 40 − 3 = 37.

</details>

**Q9.** `High`  
The postfix form of the infix expression A + B * C − D / E is

(1) ABC+*DE/−  
(2) AB+C*DE/−  
(3) ABC*+DE−/  
(4) ABC*+DE/−  

<details><summary>Answer</summary>

**(4)** — * and / are applied before + and −, and operators of equal precedence associate left to right.

</details>

**Q10.** `High`  
The postfix form of A + B * (C ^ D − E) ^ (F + G * H) − I is

(1) ABCDE^−FGH*+^*+I−  
(2) ABCD^E−FGH*+^+*I−  
(3) ABCD^E−FGH*+^*+I−  
(4) AB+CD^E−*FGH*+^I−  

<details><summary>Answer</summary>

**(3)** — ^ has the highest precedence and is right-associative.

</details>

**Q11.** `High`  
The prefix form of the infix expression A + B * C − D / E is

(1) −+A*BC/DE  
(2) +−A*BC/DE  
(3) +A−*BC/DE  
(4) −+*ABC/DE  

<details><summary>Answer</summary>

**(1)** — The last operator applied is −, whose operands are A + B * C and D / E.

</details>

**Q12.** `Medium`  
Since ^ is right-associative, the postfix form of A ^ B ^ C is

(1) ABC^ ^ (with A^B first)  
(2) ABC^^  
(3) AB^C^  
(4) A^BC^  

<details><summary>Answer</summary>

**(2)** — A ^ B ^ C means A ^ (B ^ C), giving ABC^^.

</details>

**Q13.** `Medium`  
The postfix form of (A − B) / C * D + E is

(1) AB−CD*/E+  
(2) AB−C/D*E+  
(3) ABC−/D*E+  
(4) AB−C/DE*+  

<details><summary>Answer</summary>

**(2)** — / and * are left-associative: ((A − B) / C) * D, then + E.

</details>

**Q14.** `Medium`  
During the evaluation of the postfix expression 2 3 4 * + 5 − using a stack, the maximum number of elements on the stack at any time is

(1) 3  
(2) 2  
(3) 5  
(4) 4  

<details><summary>Answer</summary>

**(1)** — 2, 3 and 4 are pushed before the first operator is applied.

</details>

**Q15.** `High`  
The numbers 1, 2, 3, 4, 5 are pushed onto a stack in that order, and pops may occur at any time. Which output sequence is NOT possible?

(1) 5, 4, 3, 2, 1  
(2) 4, 5, 3, 1, 2  
(3) 3, 2, 4, 1, 5  
(4) 2, 1, 5, 4, 3  

<details><summary>Answer</summary>

**(2)** — After 4, 5 and 3 are popped, 2 is above 1 on the stack, so 1 cannot come out before 2.

</details>

**Q16.** `High`  
The number of different output permutations obtainable by passing 1, 2, 3, 4 through a stack (pushing in order, popping at any time) is

(1) 42  
(2) 14  
(3) 24  
(4) 16  

<details><summary>Answer</summary>

**(2)** — It is the Catalan number C(4) = (1/5) × C(8, 4) = 14.

</details>

**Q17.** `High`  
Given below are two statements.  
Statement I: A stack is used to implement function calls and recursion.  
Statement II: A queue is used for breadth-first search of a graph.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Depth-first search, in contrast, uses a stack (explicitly or through recursion).

</details>

**Q18.** `High`  
In a circular queue of size n implemented with front and rear indices, where one slot is kept empty, the queue is full when

(1) (rear + 1) % n == front  
(2) (front + 1) % n == rear  
(3) rear == front  
(4) rear == n − 1  

<details><summary>Answer</summary>

**(1)** — Keeping one slot empty distinguishes "full" from "empty" (front == rear); the queue holds at most n − 1 elements.

</details>

**Q19.** `Medium`  
A queue is implemented using two stacks, where dequeue moves all elements from the input stack to the output stack only when the output stack is empty. The amortized cost per operation is

(1) O(1)  
(2) O(n)  
(3) O(n²)  
(4) O(log n)  

<details><summary>Answer</summary>

**(1)** — Each element is pushed and popped at most twice in total.

</details>

**Q20.** `Medium`  
Match List I with List II.  
List I (Data structure): A. Stack  B. Queue  C. Deque  D. Priority queue  
List II (Removal rule): I. From either end  II. Element with the highest priority  III. Last in, first out  IV. First in, first out

(1) A-III, B-IV, C-I, D-II  
(2) A-IV, B-III, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(1)** — Basic linear data structures.

</details>

**Q21.** `Medium`  
An input-restricted deque allows

(1) insertion and deletion at one end only  
(2) no deletions  
(3) insertion at both ends but deletion at one end  
(4) insertion at one end but deletion at both ends  

<details><summary>Answer</summary>

**(4)** — An output-restricted deque allows deletion at one end and insertion at both ends.

</details>

**Q22.** `High`  
The minimum number of moves needed to solve the Tower of Hanoi with 6 disks is

(1) 63  
(2) 36  
(3) 64  
(4) 127  

<details><summary>Answer</summary>

**(1)** — 2^n − 1 = 64 − 1 = 63.

</details>

**Q23.** `Medium`  
Which data structure is most suitable for checking whether the parentheses in an expression are balanced?

(1) Queue  
(2) Stack  
(3) Binary search tree  
(4) Hash table  

<details><summary>Answer</summary>

**(2)** — Each opening bracket is pushed and matched with the next closing bracket.

</details>

**Q24.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Accessing the element at index i of an array takes constant time.  
Reason R: An array stores its elements in contiguous memory, so the address can be computed as base + i × size.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This direct address computation is what gives arrays random access.

</details>

**Q25.** `Medium`  
Inserting an element at the beginning of an array of n elements requires, in the worst case,

(1) O(1) time  
(2) O(n²) time  
(3) O(log n) time  
(4) O(n) time  

<details><summary>Answer</summary>

**(4)** — All n elements must be shifted one position.

</details>

**Q26.** `Medium`  
A stack implemented with an array of size n overflows when

(1) top == 0  
(2) the stack is empty and a pop is attempted  
(3) top == n − 1 and a push is attempted  
(4) top == −1  

<details><summary>Answer</summary>

**(3)** — Popping from an empty stack (top == −1) is underflow.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: A queue can be implemented using two stacks.  
Statement II: A stack can be implemented using two queues.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are possible, with different costs for push and pop.

</details>

**Q28.** `Medium`  
A queue implemented as a singly linked list with pointers to the front and rear nodes supports

(1) enqueue and dequeue in O(1)  
(2) enqueue in O(n) and dequeue in O(1)  
(3) enqueue in O(1) and dequeue in O(n)  
(4) both in O(n)  

<details><summary>Answer</summary>

**(1)** — Insert at the rear and delete at the front.

</details>

**Q29.** `Medium`  
Which of the following applications does NOT normally use a stack?

(1) CPU scheduling with round robin  
(2) Undo operation in an editor  
(3) Evaluating postfix expressions  
(4) Backtracking  

<details><summary>Answer</summary>

**(1)** — Round-robin scheduling uses a circular queue.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: Converting an infix expression to postfix requires a queue of operators.  
Statement II: A postfix expression needs parentheses to specify the order of evaluation.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Infix-to-postfix conversion uses a stack of operators, and postfix expressions need no parentheses.

</details>

**Q31.** `Medium`  
The number of push operations needed to evaluate the postfix expression 2 3 + 4 5 * − (counting the pushes of results as well) is

(1) 4  
(2) 5  
(3) 9  
(4) 7  

<details><summary>Answer</summary>

**(4)** — Four operands are pushed, plus three results (for +, * and −): 7 pushes.

</details>

**Q32.** `Medium`  
Match List I with List II.  
List I (Operation on an array of n elements): A. Access by index  B. Linear search  C. Binary search (sorted)  D. Insertion at a given position  
List II (Worst-case time): I. O(log n)  II. O(n) due to shifting  III. O(1)  IV. O(n)

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(2)** — Basic array operation costs.

</details>

**Q33.** `Medium`  
A recursive function calls itself n times before reaching the base case. The space used on the call stack is

(1) O(n²)  
(2) O(1)  
(3) O(log n)  
(4) O(n)  

<details><summary>Answer</summary>

**(4)** — Each pending call keeps its own activation record.

</details>

**Q34.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In a circular queue, the space freed by dequeued elements can be reused.  
Reason R: A queue follows the first-in, first-out principle.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but reuse comes from the indices wrapping around modulo the array size.

</details>

**Q35.** `Medium`  
Given below are two statements.  
Statement I: A sparse matrix is one in which most of the elements are non-zero.  
Statement II: Storing a sparse matrix as a linked list or as triplets saves memory compared with a two-dimensional array.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A sparse matrix has mostly zero elements, which is why compact representations save space.

</details>

**Q36.** `Medium`  
Which of the following expressions is in prefix (Polish) notation?

(1) AB+C*  
(2) +*ABC  
(3) A B C + *  
(4) A+B*C  

<details><summary>Answer</summary>

**(2)** — In prefix notation the operator precedes its operands.

</details>

**Q37.** `Medium`  
The value of the prefix expression − + 4 * 2 3 / 8 4 is

(1) 8  
(2) 12  
(3) 10  
(4) 14  

<details><summary>Answer</summary>

**(1)** — * 2 3 = 6; + 4 6 = 10; / 8 4 = 2; − 10 2 = 8.

</details>

**Q38.** `Low`  
Which data structure is used by the operating system for buffering keystrokes and print jobs?

(1) Stack  
(2) Tree  
(3) Queue  
(4) Graph  

<details><summary>Answer</summary>

**(3)** — Requests are served in arrival order.

</details>

**Q39.** `Medium`  
A double-ended queue (deque) supports insertion and deletion at both ends. Which of the following can it simulate directly?

(1) Only a stack  
(2) Only a queue  
(3) Both a stack and a queue  
(4) Neither a stack nor a queue  

<details><summary>Answer</summary>

**(3)** — Using one end only gives a stack; inserting at one end and deleting at the other gives a queue.

</details>

**Q40.** `Medium`  
Given below are two statements.  
Statement I: FORTRAN stores arrays in row-major order.  
Statement II: In row-major order, the elements of each row are stored contiguously.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — FORTRAN uses column-major order; C uses row-major order.

</details>
