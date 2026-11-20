# Set 7 — Performance Analysis, Asymptotic Notation and Recurrences

**41 questions** — High: 18, Medium: 22, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Notation): A. f(n) = O(g(n))  B. f(n) = Ω(g(n))  C. f(n) = Θ(g(n))  D. f(n) = o(g(n))  
List II (Meaning): I. g is both an upper and a lower bound for f (up to constants)  II. g is an asymptotic upper bound for f  III. f grows strictly slower than g  IV. g is an asymptotic lower bound for f

(1) A-II, B-I, C-IV, D-III  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — Big-O, Big-Omega, Theta and little-o.

</details>

**Q2.** `High`  
Arrange the following functions in increasing order of growth rate.  
A. n log n  B. 2^n  C. √n  D. n!  E. log n

(1) C, E, A, B, D  
(2) E, A, C, B, D  
(3) E, C, A, D, B  
(4) E, C, A, B, D  

<details><summary>Answer</summary>

**(4)** — log n < √n < n log n < 2^n < n!.

</details>

**Q3.** `High`  
Which of the following is true?

(1) n^2 = O(n log n)  
(2) 2^(n+1) = O(2^n)  
(3) 2^(2n) = O(2^n)  
(4) n! = O(2^n)  

<details><summary>Answer</summary>

**(2)** — 2^(n+1) = 2 × 2^n, but 2^(2n) = 4^n grows faster than 2^n.

</details>

**Q4.** `High`  
log(n!) is

(1) Θ(n)  
(2) Θ(n log n)  
(3) Θ(log n)  
(4) Θ(n²)  

<details><summary>Answer</summary>

**(2)** — By Stirling's approximation, log(n!) ≈ n log n − n log e.

</details>

**Q5.** `High`  
Using the master theorem, the solution of T(n) = 2T(n/2) + n is

(1) Θ(n²)  
(2) Θ(log n)  
(3) Θ(n)  
(4) Θ(n log n)  

<details><summary>Answer</summary>

**(4)** — n^(log2 2) = n matches f(n), so case 2 gives Θ(n log n).

</details>

**Q6.** `High`  
Using the master theorem, the solution of T(n) = 4T(n/2) + n is

(1) Θ(n²)  
(2) Θ(n)  
(3) Θ(n² log n)  
(4) Θ(n log n)  

<details><summary>Answer</summary>

**(1)** — n^(log2 4) = n² dominates f(n) = n (case 1).

</details>

**Q7.** `High`  
Using the master theorem, the solution of T(n) = 4T(n/2) + n² is

(1) Θ(n log n)  
(2) Θ(n²)  
(3) Θ(n² log n)  
(4) Θ(n³)  

<details><summary>Answer</summary>

**(3)** — f(n) = n² equals n^(log2 4), so case 2 adds a log factor.

</details>

**Q8.** `High`  
Using the master theorem, the solution of T(n) = 4T(n/2) + n³ is

(1) Θ(n² log n)  
(2) Θ(n³ log n)  
(3) Θ(n³)  
(4) Θ(n²)  

<details><summary>Answer</summary>

**(3)** — f(n) = n³ dominates n², and the regularity condition holds (case 3).

</details>

**Q9.** `High`  
The recurrence of Strassen's matrix multiplication, T(n) = 7T(n/2) + Θ(n²), has the solution

(1) Θ(n³)  
(2) Θ(n² log n)  
(3) Θ(n²)  
(4) Θ(n^(log2 7)) ≈ Θ(n^(2.81))  

<details><summary>Answer</summary>

**(4)** — n^(log2 7) dominates n² (case 1).

</details>

**Q10.** `High`  
The solution of T(n) = T(n/2) + 1 (binary search) is

(1) Θ(1)  
(2) Θ(n log n)  
(3) Θ(log n)  
(4) Θ(n)  

<details><summary>Answer</summary>

**(3)** — Case 2 of the master theorem with a = 1, b = 2.

</details>

**Q11.** `High`  
The solution of T(n) = T(n − 1) + n, with T(1) = 1, is

(1) Θ(2^n)  
(2) Θ(n log n)  
(3) Θ(n)  
(4) Θ(n²)  

<details><summary>Answer</summary>

**(4)** — T(n) = 1 + 2 + ... + n = n(n + 1)/2.

</details>

**Q12.** `High`  
The solution of T(n) = 2T(n − 1) + 1, with T(1) = 1, is

(1) Θ(n)  
(2) Θ(n!)  
(3) Θ(2^n)  
(4) Θ(n²)  

<details><summary>Answer</summary>

**(3)** — This is the Tower of Hanoi recurrence: T(n) = 2^n − 1.

</details>

**Q13.** `High`  
The solution of T(n) = 2T(√n) + log n is

(1) Θ(log n)  
(2) Θ(log n log log n)  
(3) Θ(√n)  
(4) Θ(n)  

<details><summary>Answer</summary>

**(2)** — Substituting n = 2^m gives S(m) = 2S(m/2) + m, so S(m) = Θ(m log m).

</details>

**Q14.** `Medium`  
The solution of T(n) = T(√n) + 1 is

(1) Θ(log n)  
(2) Θ(log log n)  
(3) Θ(1)  
(4) Θ(√n)  

<details><summary>Answer</summary>

**(2)** — With n = 2^m: S(m) = S(m/2) + 1 = Θ(log m).

</details>

**Q15.** `Medium`  
The solution of T(n) = 3T(n/4) + n log n is

(1) Θ(n^(log4 3))  
(2) Θ(n)  
(3) Θ(n log² n)  
(4) Θ(n log n)  

<details><summary>Answer</summary>

**(4)** — n^(log4 3) ≈ n^(0.79) is dominated by n log n (case 3).

</details>

**Q16.** `Medium`  
The solution of T(n) = T(n/3) + T(2n/3) + n is

(1) Θ(n log n)  
(2) Θ(n)  
(3) Θ(n²)  
(4) Θ(n^(1.5))  

<details><summary>Answer</summary>

**(1)** — A recursion tree has about log_(3/2) n levels, each doing O(n) work.

</details>

**Q17.** `Medium`  
The solution of T(n) = 2T(n/2) + n log n is

(1) Θ(n²)  
(2) Θ(n log n)  
(3) Θ(n log² n)  
(4) Θ(n log log n)  

<details><summary>Answer</summary>

**(3)** — This falls between the master theorem cases; the extended case 2 gives Θ(n log² n).

</details>

**Q18.** `High`  
What is the time complexity of the following code?  
for (i = 1; i < n; i = i * 2) count++;

(1) Θ(n)  
(2) Θ(√n)  
(3) Θ(n log n)  
(4) Θ(log n)  

<details><summary>Answer</summary>

**(4)** — i doubles each iteration, so the loop runs about log2 n times.

</details>

**Q19.** `High`  
What is the time complexity of the following code?  
for (i = 1; i <= n; i++) for (j = 1; j <= n; j = j + i) count++;

(1) Θ(n)  
(2) Θ(n√n)  
(3) Θ(n²)  
(4) Θ(n log n)  

<details><summary>Answer</summary>

**(4)** — The inner loop runs n/i times: n(1 + 1/2 + ... + 1/n) = Θ(n log n).

</details>

**Q20.** `High`  
What is the time complexity of the following code?  
for (i = n; i > 0; i = i / 2) for (j = 0; j < i; j++) count++;

(1) Θ(log n)  
(2) Θ(n log n)  
(3) Θ(n²)  
(4) Θ(n)  

<details><summary>Answer</summary>

**(4)** — n + n/2 + n/4 + ... ≤ 2n.

</details>

**Q21.** `High`  
What is the time complexity of the following code?  
for (i = 0; i < n; i++) for (j = 0; j < i; j++) count++;

(1) Θ(n³)  
(2) Θ(n²)  
(3) Θ(n)  
(4) Θ(n log n)  

<details><summary>Answer</summary>

**(2)** — The total is 0 + 1 + ... + (n − 1) = n(n − 1)/2.

</details>

**Q22.** `Medium`  
What is the time complexity of the following code?  
for (i = 1; i * i <= n; i++) count++;

(1) Θ(√n)  
(2) Θ(n²)  
(3) Θ(n)  
(4) Θ(log n)  

<details><summary>Answer</summary>

**(1)** — The loop stops when i exceeds √n.

</details>

**Q23.** `Medium`  
The naive recursive Fibonacci function fib(n) = fib(n − 1) + fib(n − 2) runs in

(1) Θ(n²)  
(2) exponential time Θ(φ^n), where φ ≈ 1.618  
(3) Θ(n)  
(4) Θ(log n)  

<details><summary>Answer</summary>

**(2)** — Its call tree grows like the Fibonacci numbers themselves.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: The space complexity of naive recursive Fibonacci is O(n).  
Statement II: The time complexity of the iterative (or memoized) Fibonacci is O(n).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The recursion depth is n even though the number of calls is exponential.

</details>

**Q25.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Appending to a dynamic array that doubles its capacity when full takes O(1) amortized time.  
Reason R: Every individual append takes O(1) time in the worst case.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — An append that triggers resizing copies all elements and takes O(n); only the amortized cost is O(1).

</details>

**Q26.** `Medium`  
Match List I with List II.  
List I (Amortized analysis method): A. Aggregate method  B. Accounting method  C. Potential method  
List II (Idea): I. Assigns a potential function to the data structure state  II. Computes the total cost of n operations and divides by n  III. Charges some operations more than their cost and stores credit for later operations

(1) A-II, B-III, C-I  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — The three methods of amortized analysis.

</details>

**Q27.** `Medium`  
Incrementing a binary counter n times, starting from 0, takes total time

(1) Θ(n²)  
(2) Θ(n)  
(3) Θ(log n)  
(4) Θ(n log n)  

<details><summary>Answer</summary>

**(2)** — Bit i flips n/2^i times, so the total is less than 2n.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: If f(n) = O(g(n)), then g(n) = O(f(n)).  
Statement II: If f(n) = O(g(n)) and g(n) = O(h(n)), then f(n) = O(h(n)).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Big-O is transitive but not symmetric (n = O(n²), but n² ≠ O(n)).

</details>

**Q29.** `Medium`  
The value of n^(1/log2 n) is

(1) log n  
(2) 1  
(3) n  
(4) 2  

<details><summary>Answer</summary>

**(4)** — n^(1/log2 n) = 2^(log2 n / log2 n) = 2.

</details>

**Q30.** `Medium`  
Which of the following is NOT O(n²)?

(1) n log n  
(2) n  
(3) 100n² + 5  
(4) n^(2.5)  

<details><summary>Answer</summary>

**(4)** — n^(2.5) grows faster than n².

</details>

**Q31.** `Medium`  
The master theorem cannot be applied directly to

(1) T(n) = 2^n T(n/2) + n  
(2) T(n) = 9T(n/3) + n  
(3) T(n) = 2T(n/2) + n  
(4) T(n) = T(2n/3) + 1  

<details><summary>Answer</summary>

**(1)** — The number of subproblems a must be a constant.

</details>

**Q32.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: An algorithm that is O(n²) can never be faster in practice than an O(n log n) algorithm.  
Reason R: Asymptotic notation ignores constant factors and lower-order terms.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — For small n or large constant factors an O(n²) algorithm can be faster; R is exactly why A is false.

</details>

**Q33.** `Medium`  
The time complexity of the following recursive function is  
void f(int n) { if (n <= 1) return; f(n/2); f(n/2); }

(1) Θ(n²)  
(2) Θ(n log n)  
(3) Θ(log n)  
(4) Θ(n)  

<details><summary>Answer</summary>

**(4)** — T(n) = 2T(n/2) + 1 = Θ(n).

</details>

**Q34.** `Medium`  
The best-case time complexity of an algorithm is

(1) always O(1)  
(2) an upper bound on its running time for every input  
(3) its running time on the input of size n that takes the least time  
(4) the same as its average case  

<details><summary>Answer</summary>

**(3)** — Worst case gives an upper bound over all inputs of size n.

</details>

**Q35.** `Medium`  
Space complexity measures

(1) disk usage only  
(2) the number of comparisons  
(3) the total memory an algorithm needs as a function of input size  
(4) the number of instructions  

<details><summary>Answer</summary>

**(3)** — Auxiliary space excludes the input itself.

</details>

**Q36.** `Medium`  
Which of the following methods are used to solve recurrences?  
A. Substitution method  B. Recursion-tree method  C. Master method  D. Greedy method  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A and D only  
(3) A, B, C and D  
(4) A, B and C only  

<details><summary>Answer</summary>

**(4)** — The greedy method is an algorithm design technique.

</details>

**Q37.** `Medium`  
The solution of T(n) = 8T(n/2) + n² is

(1) Θ(n³)  
(2) Θ(n² log n)  
(3) Θ(n²)  
(4) Θ(n^(2.81))  

<details><summary>Answer</summary>

**(1)** — n^(log2 8) = n³ dominates n² (case 1). This is the recurrence of standard divide-and-conquer matrix multiplication.

</details>

**Q38.** `Medium`  
The solution of T(n) = 3T(n/2) + n (Karatsuba multiplication) is

(1) Θ(n log n)  
(2) Θ(n^(log2 3)) ≈ Θ(n^(1.585))  
(3) Θ(n^(1.5))  
(4) Θ(n²)  

<details><summary>Answer</summary>

**(2)** — n^(log2 3) dominates n (case 1).

</details>

**Q39.** `Medium`  
Given below are two statements.  
Statement I: n log n = O(n^(1.001)).  
Statement II: (log n)^100 = O(n^(0.01)).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Any power of log n grows more slowly than any positive power of n.

</details>

**Q40.** `Low`  
The term "asymptotic" in complexity analysis refers to behaviour as

(1) n grows without bound  
(2) n approaches 0  
(3) n equals 1  
(4) n is negative  

<details><summary>Answer</summary>

**(1)** — Constants and lower-order terms become irrelevant for large n.

</details>

**Q41.** `Medium`  
What is the time complexity of the following code?  
int i = n; while (i > 1) { i = i / 3; }

(1) Θ(√n)  
(2) Θ(n)  
(3) Θ(log n)  
(4) Θ(n/3)  

<details><summary>Answer</summary>

**(3)** — i is divided by 3 each time: about log3 n iterations.

</details>
