# Set 11 — Intermediate Code Generation (syntax trees, DAGs, three-address code, quadruples, triples, SSA, backpatching)

**21 questions** — High: 8, Medium: 12, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The three-address code for a = b \* −c + b \* −c, generated without detecting common subexpressions, has how many instructions (including the final assignment)?

(1) 6  
(2) 7  
(3) 4  
(4) 5  

<details><summary>Answer</summary>

**(1)** — t1 = minus c; t2 = b \* t1; t3 = minus c; t4 = b \* t3; t5 = t2 + t4; a = t5.

</details>

**Q2.** `High`  
If common subexpressions are detected using a DAG, the three-address code for a = b \* −c + b \* −c can be reduced to how many instructions?

(1) 4  
(2) 6  
(3) 3  
(4) 5  

<details><summary>Answer</summary>

**(1)** — t1 = minus c; t2 = b \* t1; t3 = t2 + t2; a = t3.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (Representation): A. Quadruples  B. Triples  C. Indirect triples  D. Static single-assignment form  
List II (Feature): I. Each variable is assigned exactly once; φ-functions merge values at join points  II. Fields op, arg1, arg2 and result; temporaries are named explicitly  III. A separate list of pointers to triples, so instructions can be reordered easily  IV. Results are referred to by the position of the instruction that computes them

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Common implementations of three-address code.

</details>

**Q4.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Moving an instruction is harder in a triple representation than in a quadruple representation.  
Reason R: In triples, other instructions refer to a result by its position, so moving it requires changing all references.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Indirect triples avoid this by reordering a list of pointers.

</details>

**Q5.** `High`  
The syntax tree for a + a \* (b − c) + (b − c) \* d has 13 nodes. The corresponding DAG has

(1) 11 nodes  
(2) 9 nodes  
(3) 10 nodes  
(4) 7 nodes  

<details><summary>Answer</summary>

**(2)** — The leaves a, b, c, d appear once each, and b − c is shared: 4 leaves + 5 interior nodes.

</details>

**Q6.** `Medium`  
The minimum number of temporary variables needed to compute (a + b) \* (c + d) in three-address code, if temporaries may be reused, is

(1) 2  
(2) 3  
(3) 1  
(4) 4  

<details><summary>Answer</summary>

**(1)** — t1 = a + b; t2 = c + d; t1 = t1 \* t2.

</details>

**Q7.** `High`  
In static single-assignment form, the code x = a; x = x + 1; y = x \* 2 becomes

(1) x = a; x = x + 1; y = x \* 2  
(2) x1 = a; x2 = x1 + 1; y1 = x2 \* 2  
(3) x1 = a; x1 = x1 + 1; y1 = x1 \* 2  
(4) x = a + 1; y = x \* 2  

<details><summary>Answer</summary>

**(2)** — Each assignment defines a new version of the variable.

</details>

**Q8.** `Medium`  
A φ-function in SSA form is placed

(1) at the start of every basic block  
(2) only in loops without branches  
(3) after every assignment  
(4) at a join point where different definitions of a variable reach along different control-flow paths  

<details><summary>Answer</summary>

**(4)** — x3 = φ(x1, x2) selects the value according to the path taken.

</details>

**Q9.** `High`  
For an integer array A[10][20] (4 bytes per element, indices from 0) stored in row-major order with base address B, the address of A[i][j] is

(1) B + (i + j) × 4  
(2) B + (i × 20 + j) × 4  
(3) B + (j × 10 + i) × 4  
(4) B + (i × 10 + j) × 4  

<details><summary>Answer</summary>

**(2)** — Each row has 20 elements; the compiler generates this computation in the intermediate code.

</details>

**Q10.** `High`  
Backpatching is used in intermediate code generation to

(1) allocate registers  
(2) build the symbol table  
(3) optimize loops  
(4) fill in jump targets of conditional and unconditional jumps that are not yet known when the jumps are generated  

<details><summary>Answer</summary>

**(4)** — Lists of jumps (truelist, falselist, nextlist) are patched once the target labels are known.

</details>

**Q11.** `Medium`  
With short-circuit (jumping) code for the boolean expression a &lt; b or c &lt; d, if a &lt; b is true,

(1) the expression evaluates to false  
(2) c &lt; d is still evaluated  
(3) control jumps directly to the true exit without evaluating c &lt; d  
(4) an error occurs  

<details><summary>Answer</summary>

**(3)** — This is the semantics of || in C and "or else" in other languages.

</details>

**Q12.** `Medium`  
Given below are two statements.  
Statement I: Three-address code has at most one operator on the right side of each instruction.  
Statement II: Postfix notation is a form of intermediate representation.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Syntax trees, DAGs, postfix and three-address code are all intermediate representations.

</details>

**Q13.** `Medium`  
The postfix form of the expression a + b \* c is

(1) a+bc\*  
(2) ab+c\*  
(3) abc\*+  
(4) +a\*bc  

<details><summary>Answer</summary>

**(3)** — \* has higher precedence than +.

</details>

**Q14.** `Medium`  
A procedure call p(x1, x2, x3) is translated into three-address code as

(1) p = x1 + x2 + x3  
(2) param x1; param x2; param x3; call p, 3  
(3) goto p  
(4) call p, 3  

<details><summary>Answer</summary>

**(2)** — The second argument of call is the number of parameters.

</details>

**Q15.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Generating intermediate code makes it easier to apply machine-independent optimizations.  
Reason R: Intermediate code is independent of the target machine and simpler than the source program.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The same optimizer can be reused for many front ends and back ends.

</details>

**Q16.** `Medium`  
A switch statement with many dense case values is efficiently translated using

(1) recursion  
(2) a jump table indexed by the case value  
(3) a hash table always  
(4) a sequence of conditional jumps only  

<details><summary>Answer</summary>

**(2)** — For sparse values, a sequence of tests or a hash table is used instead.

</details>

**Q17.** `Medium`  
Which of the following is NOT a form of three-address instruction?

(1) x = y op z  
(2) goto L  
(3) x = op y  
(4) x = y op z op w  

<details><summary>Answer</summary>

**(4)** — Three-address code has at most three addresses and one operator per instruction.

</details>

**Q18.** `Medium`  
The triple representation of a = b \* −c + b \* −c needs

(1) 6 entries  
(2) 5 entries  
(3) 7 entries  
(4) 4 entries  

<details><summary>Answer</summary>

**(1)** — (0) minus c; (1) \* b, (0); (2) minus c; (3) \* b, (2); (4) + (1), (3); (5) = a, (4).

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: A syntax tree for an expression always has fewer nodes than the corresponding DAG.  
Statement II: A DAG for an expression identifies common subexpressions.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A DAG never has more nodes than the syntax tree, because it shares repeated subtrees.

</details>

**Q20.** `Low`  
Three-address code is called so because each instruction has

(1) three temporaries  
(2) exactly three operators  
(3) at most three addresses (two operands and one result)  
(4) three labels  

<details><summary>Answer</summary>

**(3)** — For example t1 = b \* c.

</details>

**Q21.** `Medium`  
In translating the statement while (a &lt; b) a = a + 1;, the intermediate code needs

(1) a call instruction  
(2) only one label  
(3) no jumps  
(4) a conditional jump out of the loop and an unconditional jump back to the test  

<details><summary>Answer</summary>

**(4)** — L1: if a &gt;= b goto L2; a = a + 1; goto L1; L2:.

</details>
