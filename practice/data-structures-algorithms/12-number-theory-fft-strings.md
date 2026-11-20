# Set 12 — Selected Topics: Number-Theoretic Algorithms, Polynomial Arithmetic, FFT and String Matching

**35 questions** — High: 17, Medium: 17, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
gcd(252, 198) computed by Euclid's algorithm is

(1) 6  
(2) 18  
(3) 36  
(4) 9  

<details><summary>Answer</summary>

**(2)** — 252 = 1 × 198 + 54; 198 = 3 × 54 + 36; 54 = 1 × 36 + 18; 36 = 2 × 18.

</details>

**Q2.** `High`  
The extended Euclidean algorithm applied to 99 and 78 gives gcd = 3 = 99x + 78y with

(1) x = 14, y = −11  
(2) x = −11, y = 14  
(3) x = −3, y = 4  
(4) x = 3, y = −4  

<details><summary>Answer</summary>

**(2)** — 99 × (−11) + 78 × 14 = −1089 + 1092 = 3.

</details>

**Q3.** `High`  
The multiplicative inverse of 7 modulo 26 is

(1) 3  
(2) 11  
(3) 15  
(4) 19  

<details><summary>Answer</summary>

**(3)** — 7 × 15 = 105 = 4 × 26 + 1.

</details>

**Q4.** `Medium`  
The multiplicative inverse of 17 modulo 43 is

(1) 38  
(2) 5  
(3) 41  
(4) 23  

<details><summary>Answer</summary>

**(1)** — 17 × 38 = 646 = 15 × 43 + 1.

</details>

**Q5.** `High`  
The value of 7^222 mod 11 is

(1) 3  
(2) 7  
(3) 1  
(4) 5  

<details><summary>Answer</summary>

**(4)** — By Fermat, 7^10 ≡ 1 (mod 11); 7^222 = (7^10)^22 × 7^2 ≡ 49 ≡ 5.

</details>

**Q6.** `High`  
The value of 2^100 mod 7 is

(1) 2  
(2) 4  
(3) 1  
(4) 6  

<details><summary>Answer</summary>

**(1)** — 2^3 ≡ 1 (mod 7); 100 = 3 × 33 + 1, so 2^100 ≡ 2.

</details>

**Q7.** `Medium`  
The value of 3^200 mod 13 is

(1) 9  
(2) 12  
(3) 1  
(4) 3  

<details><summary>Answer</summary>

**(1)** — 3^3 = 27 ≡ 1 (mod 13); 200 = 3 × 66 + 2, so 3^200 ≡ 9.

</details>

**Q8.** `High`  
The smallest non-negative x satisfying x ≡ 2 (mod 3), x ≡ 3 (mod 5) and x ≡ 2 (mod 7) is

(1) 23  
(2) 53  
(3) 38  
(4) 8  

<details><summary>Answer</summary>

**(1)** — By the Chinese remainder theorem the solution is unique modulo 105; 23 satisfies all three.

</details>

**Q9.** `High`  
Euler's totient φ(100) is

(1) 20  
(2) 40  
(3) 50  
(4) 60  

<details><summary>Answer</summary>

**(2)** — φ(100) = 100 × (1 − 1/2) × (1 − 1/5) = 40.

</details>

**Q10.** `High`  
Given below are two statements.  
Statement I: Euclid's algorithm takes O(log min(a, b)) division steps.  
Statement II: The worst case of Euclid's algorithm occurs for consecutive Fibonacci numbers.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This is Lamé's theorem.

</details>

**Q11.** `Medium`  
The number of division steps that Euclid's algorithm takes to compute gcd(55, 34) is

(1) 5  
(2) 8  
(3) 7  
(4) 6  

<details><summary>Answer</summary>

**(2)** — 55 and 34 are consecutive Fibonacci numbers, giving the maximum number of steps for their size: 8.

</details>

**Q12.** `High`  
Computing a^b mod n by repeated squaring requires

(1) O(log b) multiplications  
(2) O(b²) multiplications  
(3) O(√b) multiplications  
(4) O(b) multiplications  

<details><summary>Answer</summary>

**(1)** — The exponent is processed bit by bit.

</details>

**Q13.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Fermat's little theorem states that a^(p − 1) ≡ 1 (mod p) for a prime p not dividing a.  
Reason R: The multiplicative group of integers modulo a prime p has order p − 1.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Lagrange's theorem then gives a^(p − 1) ≡ 1.

</details>

**Q14.** `Medium`  
The multiplicative inverse of a modulo n exists if and only if

(1) a is odd  
(2) n is prime  
(3) a &lt; n  
(4) gcd(a, n) = 1  

<details><summary>Answer</summary>

**(4)** — It is computed with the extended Euclidean algorithm.

</details>

**Q15.** `High`  
Evaluating a polynomial of degree n at a point using Horner's rule requires

(1) n(n + 1)/2 multiplications  
(2) 2n multiplications and n additions  
(3) n multiplications and n additions  
(4) n² multiplications  

<details><summary>Answer</summary>

**(3)** — a0 + x(a1 + x(a2 + ... + x an)).

</details>

**Q16.** `High`  
Multiplying two polynomials of degree n using the fast Fourier transform takes

(1) O(n log² n)  
(2) O(n²)  
(3) O(n^(1.58))  
(4) O(n log n)  

<details><summary>Answer</summary>

**(4)** — Evaluate at 2n roots of unity with FFT, multiply pointwise, and interpolate with inverse FFT.

</details>

**Q17.** `High`  
Given below are two statements.  
Statement I: The FFT evaluates a polynomial at the complex nth roots of unity in O(n log n) time.  
Statement II: The naive evaluation of a degree-(n − 1) polynomial at n points takes O(n log n) time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Naive evaluation at n points with Horner's rule takes O(n²).

</details>

**Q18.** `Medium`  
The FFT algorithm is based on which technique?

(1) Greedy  
(2) Divide and conquer  
(3) Backtracking  
(4) Dynamic programming  

<details><summary>Answer</summary>

**(2)** — A(x) = A\_even(x²) + x A\_odd(x²) splits the problem into two halves.

</details>

**Q19.** `Medium`  
The FFT requires the number of evaluation points n to be

(1) a power of 2 (in the basic radix-2 version)  
(2) odd  
(3) prime  
(4) a multiple of 10  

<details><summary>Answer</summary>

**(1)** — The polynomial is padded with zero coefficients if needed.

</details>

**Q20.** `High`  
Match List I with List II.  
List I (String-matching algorithm): A. Naive  B. Rabin-Karp  C. Knuth-Morris-Pratt  D. Finite-automaton matcher  
List II (Matching time, text length n, pattern length m): I. O((n − m + 1)m) worst case, O(n + m) expected  II. O(n) after O(m |Σ|) preprocessing  III. O((n − m + 1)m)  IV. O(n) after O(m) preprocessing

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-I, B-III, C-IV, D-II  
(4) A-III, B-I, C-II, D-IV  

<details><summary>Answer</summary>

**(1)** — Standard complexities from CLRS.

</details>

**Q21.** `High`  
The KMP prefix function π for the pattern "ababaca" is

(1) 0 1 2 3 0 1 0  
(2) 0 0 1 2 0 0 1  
(3) 0 0 0 1 2 3 0  
(4) 0 0 1 2 3 0 1  

<details><summary>Answer</summary>

**(4)** — π[q] is the length of the longest proper prefix of P[1..q] that is also its suffix.

</details>

**Q22.** `Medium`  
The KMP prefix function π for the pattern "aabaaab" is

(1) 0 0 1 1 2 2 3  
(2) 0 1 0 1 2 3 3  
(3) 0 1 0 1 2 2 3  
(4) 0 1 0 0 1 2 3  

<details><summary>Answer</summary>

**(3)** — For example, "aabaa" has border "aa" (2), and "aabaaab" has border "aab" (3).

</details>

**Q23.** `Medium`  
The KMP prefix function π for the pattern "abcdabd" is

(1) 0 0 0 0 1 2 0  
(2) 0 1 2 3 0 0 0  
(3) 0 0 0 0 1 2 3  
(4) 0 0 0 1 2 0 0  

<details><summary>Answer</summary>

**(1)** — "abcdab" has border "ab"; "abcdabd" has no non-empty border.

</details>

**Q24.** `High`  
In the Rabin-Karp example with text 2359023141526739921, pattern 31415 and modulus 13, the number of spurious hits is

(1) 0  
(2) 1  
(3) 2  
(4) 3  

<details><summary>Answer</summary>

**(2)** — The valid match is at shift 6; the window 67399 at shift 12 also has hash 7 but does not match.

</details>

**Q25.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Rabin-Karp must verify each hash match character by character.  
Reason R: Different strings can have the same hash value modulo q.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Such false matches are called spurious hits.

</details>

**Q26.** `Medium`  
The naive string-matching algorithm, comparing characters left to right and stopping at the first mismatch, makes how many character comparisons to search for "aaab" in "aaaaaaaaab"?

(1) 10  
(2) 7  
(3) 28  
(4) 40  

<details><summary>Answer</summary>

**(3)** — Each of the 7 shifts compares 4 characters.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: The Boyer-Moore algorithm scans the pattern from right to left.  
Statement II: Boyer-Moore can skip parts of the text, so it is often sublinear in practice.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — It uses the bad-character and good-suffix heuristics.

</details>

**Q28.** `Medium`  
The KMP algorithm never

(1) moves backwards in the text  
(2) preprocesses the pattern  
(3) matches in linear time  
(4) uses the prefix function  

<details><summary>Answer</summary>

**(1)** — The text pointer only advances; the pattern pointer falls back using π.

</details>

**Q29.** `Medium`  
The Rabin-Karp algorithm is especially useful for

(1) compressing text  
(2) sorting strings  
(3) searching for many patterns at once, and for 2-D pattern matching  
(4) single-character search  

<details><summary>Answer</summary>

**(3)** — The hashes of all patterns can be stored in a set.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: The Miller-Rabin primality test is a deterministic polynomial-time algorithm that never errs.  
Statement II: Modular exponentiation is used in the RSA cryptosystem.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Miller-Rabin is a randomized (Monte Carlo) test with a small probability of error for composites.

</details>

**Q31.** `Medium`  
The value of 5^117 mod 19 is

(1) 1  
(2) 7  
(3) 11  
(4) 5  

<details><summary>Answer</summary>

**(1)** — 5 has order 9 modulo 19 (5^9 ≡ 1), and 117 = 9 × 13.

</details>

**Q32.** `Medium`  
The number of operations needed to multiply two n-digit integers with the schoolbook method is

(1) O(n²)  
(2) O(n)  
(3) O(2^n)  
(4) O(n log n)  

<details><summary>Answer</summary>

**(1)** — Karatsuba reduces it to O(n^(1.585)), and FFT-based methods to about O(n log n).

</details>

**Q33.** `Medium`  
A suffix tree for a text of length n can be built in

(1) O(n) time  
(2) O(n²) time only  
(3) O(2^n) time  
(4) O(n³) time  

<details><summary>Answer</summary>

**(1)** — Ukkonen's and McCreight's algorithms are linear for a constant alphabet.

</details>

**Q34.** `Low`  
The greatest common divisor of two consecutive integers is always

(1) the smaller integer  
(2) 1  
(3) 2  
(4) 0  

<details><summary>Answer</summary>

**(2)** — Any common divisor would also divide their difference, 1.

</details>

**Q35.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The inverse DFT can be computed with the same FFT algorithm.  
Reason R: The inverse DFT requires Θ(n²) time.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — The inverse DFT uses conjugate roots of unity and division by n, so it also takes O(n log n).

</details>
