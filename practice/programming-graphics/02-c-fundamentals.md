# Set 2 — Programming in C: Tokens, Data Types, Operators and Control Statements (with output questions)

**36 questions** — High: 16, Medium: 19, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
What is the output of the following C code?  
int a = 10, b = 3; printf("%d %d %d", a / b, a % b, -a % b);

(1) 3 -1 -1  
(2) 3.33 1 -1  
(3) 3 1 -1  
(4) 3 1 1  

<details><summary>Answer</summary>

**(3)** — Integer division truncates towards zero, and the remainder takes the sign of the dividend (C99).

</details>

**Q2.** `High`  
What is the output of the following C code?  
printf("%d", 5 &gt; 3 &gt; 1);

(1) 0  
(2) Compilation error  
(3) 5  
(4) 1  

<details><summary>Answer</summary>

**(1)** — Relational operators associate left to right: (5 &gt; 3) is 1, and 1 &gt; 1 is 0.

</details>

**Q3.** `High`  
What is the output of the following C code?  
int i = 0; while (i++ &lt; 3); printf("%d", i);

(1) 3  
(2) 0  
(3) Infinite loop  
(4) 4  

<details><summary>Answer</summary>

**(4)** — The loop body is the empty statement; the test is evaluated with i = 0, 1, 2, 3, and i is incremented each time, ending at 4.

</details>

**Q4.** `High`  
What is the output of the following C code?  
int x = 2; switch (x) { case 1: printf("A"); case 2: printf("B"); case 3: printf("C"); break; default: printf("D"); }

(1) B  
(2) BCD  
(3) BC  
(4) ABC  

<details><summary>Answer</summary>

**(3)** — Control falls through from case 2 into case 3 until the break.

</details>

**Q5.** `High`  
What is the output of the following C code?  
int i; for (i = 0; i &lt; 5; i++) { if (i == 3) continue; printf("%d", i); }

(1) 01234  
(2) 0123  
(3) 012  
(4) 0124  

<details><summary>Answer</summary>

**(4)** — continue skips the printf only when i is 3.

</details>

**Q6.** `High`  
What is the output of the following C code?  
int x = 2, y = 5; x = x ^ y; y = x ^ y; x = x ^ y; printf("%d %d", x, y);

(1) 5 2  
(2) 7 7  
(3) 2 5  
(4) 0 0  

<details><summary>Answer</summary>

**(1)** — The three XOR assignments swap x and y without a temporary variable.

</details>

**Q7.** `High`  
What is the output of the following C code?  
printf("%d %d %d %d", 5 & 3, 5 | 3, 5 ^ 3, 1 &lt;&lt; 4);

(1) 1 6 7 16  
(2) 1 7 6 16  
(3) 7 1 6 16  
(4) 1 7 6 8  

<details><summary>Answer</summary>

**(2)** — 101 & 011 = 001, 101 | 011 = 111, 101 ^ 011 = 110, and 1 &lt;&lt; 4 = 16.

</details>

**Q8.** `High`  
What is the output of the following C code?  
int i = 0, j = 0; if (i++ || j++) ; printf("%d %d", i, j);

(1) 1 1  
(2) 0 0  
(3) 0 1  
(4) 1 0  

<details><summary>Answer</summary>

**(1)** — i++ yields 0 (false), so the right operand j++ is also evaluated.

</details>

**Q9.** `High`  
What is the output of the following C code?  
int i = 0, j = 0; if (++i || ++j) ; printf("%d %d", i, j);

(1) 1 1  
(2) 0 0  
(3) 1 0  
(4) 0 1  

<details><summary>Answer</summary>

**(3)** — ++i yields 1 (true), so ++j is not evaluated (short-circuit evaluation).

</details>

**Q10.** `Medium`  
What is the output of the following C code?  
int i = 0, j = 0; if (i++ && j++) ; printf("%d %d", i, j);

(1) 0 0  
(2) 1 0  
(3) 1 1  
(4) 0 1  

<details><summary>Answer</summary>

**(2)** — i++ yields 0, so the && short-circuits and j++ is skipped.

</details>

**Q11.** `High`  
What is the output of the following C code?  
int x = -1; unsigned int y = 1; printf("%d", x &lt; y);

(1) 1  
(2) -1  
(3) Compilation error  
(4) 0  

<details><summary>Answer</summary>

**(4)** — x is converted to unsigned int, becoming a very large value, so x &lt; y is false.

</details>

**Q12.** `High`  
What is the output of the following C code?  
float f = 0.1; if (f == 0.1) printf("Yes"); else printf("No");

(1) No  
(2) Yes  
(3) Compilation error  
(4) 0.1  

<details><summary>Answer</summary>

**(1)** — 0.1 cannot be represented exactly; the float value differs from the double constant 0.1.

</details>

**Q13.** `High`  
What is the output of the following C code?  
enum { A, B = 5, C, D = 2, E }; printf("%d %d %d", A, C, E);

(1) 0 2 3  
(2) 0 6 2  
(3) 0 6 3  
(4) 1 6 3  

<details><summary>Answer</summary>

**(3)** — Enumerators take the previous value plus one unless explicitly assigned.

</details>

**Q14.** `Medium`  
What is the output of the following C code?  
int i = 10; do { printf("%d", i); i++; } while (i &lt; 5);

(1) 10  
(2) Nothing  
(3) Infinite loop  
(4) 10111213  

<details><summary>Answer</summary>

**(1)** — A do-while loop executes its body at least once.

</details>

**Q15.** `High`  
What is the output of the following C code?  
printf("%d %d", -7 / 2, -7 % 2);

(1) -3 1  
(2) -3 -1  
(3) -4 -1  
(4) -4 1  

<details><summary>Answer</summary>

**(2)** — C99 truncates towards zero, so a = (a / b) × b + a % b gives -7 = -3 × 2 + (-1).

</details>

**Q16.** `Medium`  
What is the output of the following C code?  
int a = (1, 2, 3); printf("%d", a);

(1) Compilation error  
(2) 6  
(3) 3  
(4) 1  

<details><summary>Answer</summary>

**(3)** — The comma operator evaluates its operands left to right and yields the value of the last one.

</details>

**Q17.** `High`  
What is the output of the following C code?  
printf("%d", printf("Hello"));

(1) Hello6  
(2) Hello  
(3) Hello5  
(4) 5Hello  

<details><summary>Answer</summary>

**(3)** — The inner printf prints Hello and returns the number of characters printed, 5.

</details>

**Q18.** `Medium`  
In C, the value of sizeof('A') on a system with 4-byte int is

(1) 8  
(2) 2  
(3) 1  
(4) 4  

<details><summary>Answer</summary>

**(4)** — A character constant has type int in C (in C++ it has type char, so the size is 1).

</details>

**Q19.** `Medium`  
What is the output of the following C code?  
int i, c = 0; for (i = 1; i &lt;= 10; i \*= 2) c++; printf("%d", c);

(1) 4  
(2) 10  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(1)** — i takes the values 1, 2, 4 and 8.

</details>

**Q20.** `Medium`  
What is the output of the following C code?  
int i = 5, j; j = i++ \* 2; printf("%d %d", i, j);

(1) 5 10  
(2) 6 12  
(3) 6 10  
(4) 5 12  

<details><summary>Answer</summary>

**(3)** — Post-increment uses the old value 5 in the expression and then increments i.

</details>

**Q21.** `Medium`  
What is the output of the following C code?  
int a = 5, b = 10, c = 3; printf("%d", a &gt; b ? a : b &gt; c ? b : c);

(1) 1  
(2) 3  
(3) 5  
(4) 10  

<details><summary>Answer</summary>

**(4)** — ?: is right-associative: a &gt; b is false, so b &gt; c ? b : c gives 10.

</details>

**Q22.** `Medium`  
What is the output of the following C code?  
int x = 2 + 3 \* 4 % 5 - 6 / 4; printf("%d", x);

(1) 4  
(2) 3  
(3) 1  
(4) 5  

<details><summary>Answer</summary>

**(2)** — \* , % and / have equal precedence and are left-associative: 3 × 4 = 12, 12 % 5 = 2, 6 / 4 = 1; 2 + 2 − 1 = 3.

</details>

**Q23.** `Medium`  
What is the output of the following C code?  
int x = 0; if (x = 5) printf("T%d", x); else printf("F%d", x);

(1) F0  
(2) T5  
(3) T0  
(4) F5  

<details><summary>Answer</summary>

**(2)** — x = 5 is an assignment, whose value 5 is true.

</details>

**Q24.** `Medium`  
What is the output of the following C code?  
int n = 0; while (1) { n += 3; if (n &gt; 10) break; } printf("%d", n);

(1) 10  
(2) 9  
(3) Infinite loop  
(4) 12  

<details><summary>Answer</summary>

**(4)** — n takes the values 3, 6, 9 and 12, and the loop exits when n exceeds 10.

</details>

**Q25.** `Medium`  
What is the output of the following C code?  
int i, j, c = 0; for (i = 0; i &lt; 4; i++) for (j = i; j &lt; 4; j++) c++; printf("%d", c);

(1) 12  
(2) 8  
(3) 10  
(4) 16  

<details><summary>Answer</summary>

**(3)** — 4 + 3 + 2 + 1 = 10.

</details>

**Q26.** `Medium`  
What is the output of the following C code?  
char c = 'A' + 2; printf("%c %d", c, c);

(1) C 67  
(2) B 66  
(3) C 65  
(4) A 65  

<details><summary>Answer</summary>

**(1)** — Characters are small integers; 'A' is 65 in ASCII.

</details>

**Q27.** `High`  
Given below are two statements.  
Statement I: In C, the expression i = i++ + ++i has undefined behaviour.  
Statement II: In C, the order of evaluation of function arguments is unspecified.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Modifying a variable twice without an intervening sequence point is undefined behaviour.

</details>

**Q28.** `High`  
Match List I with List II.  
List I (C operator): A. ++ (postfix)  B. \* (multiplication)  C. && (logical AND)  D. = (assignment)  
List II (Associativity / relative precedence): I. Lower precedence than relational operators, left to right  II. Highest of these, postfix  III. Lowest of these, right to left  IV. Higher than + and −, left to right

(1) A-II, B-IV, C-III, D-I  
(2) A-IV, B-II, C-I, D-III  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(3)** — Assignment operators have very low precedence and associate right to left.

</details>

**Q29.** `Medium`  
Which of the following is NOT a valid C identifier?

(1) \_count  
(2) count2  
(3) Count\_2  
(4) 2count  

<details><summary>Answer</summary>

**(4)** — Identifiers cannot begin with a digit.

</details>

**Q30.** `Medium`  
Which of the following are C keywords?  
A. auto  B. register  C. volatile  D. include  E. typedef  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) C, D and E only  
(3) A, B and D only  
(4) A, B, C and E only  

<details><summary>Answer</summary>

**(4)** — include is a preprocessor directive name, not a keyword.

</details>

**Q31.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The break statement exits only the innermost loop or switch that contains it.  
Reason R: C has no labelled break; goto must be used to exit several nested loops at once.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Java, in contrast, provides labelled break statements.

</details>

**Q32.** `Medium`  
The goto statement in C transfers control to

(1) any function  
(2) a labelled statement within the same function  
(3) the beginning of the program  
(4) the operating system  

<details><summary>Answer</summary>

**(2)** — Structured programming discourages goto, but it is occasionally used for error handling.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: In C, a switch expression can be of type float.  
Statement II: Case labels in a C switch statement must be integer constant expressions.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — The switch expression must have integer type (including char and enum).

</details>

**Q34.** `Medium`  
The range of values of a signed 8-bit char in two's complement representation is

(1) −127 to 127  
(2) −256 to 255  
(3) −128 to 127  
(4) 0 to 255  

<details><summary>Answer</summary>

**(3)** — An n-bit two's complement integer ranges from −2^(n−1) to 2^(n−1) − 1.

</details>

**Q35.** `Low`  
Which format specifier prints an unsigned integer in hexadecimal in C?

(1) %o  
(2) %d  
(3) %f  
(4) %x  

<details><summary>Answer</summary>

**(4)** — %o prints octal and %u unsigned decimal.

</details>

**Q36.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The expression 5 / 2 in C evaluates to 2.5.  
Reason R: When both operands are integers, C performs integer division.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Because of R, 5 / 2 evaluates to 2.

</details>
