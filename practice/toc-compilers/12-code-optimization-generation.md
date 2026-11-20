# Set 12 — Code Optimization and Code Generation (basic blocks, flow graphs, data-flow analysis, local, global, loop and peephole optimization, instruction scheduling)

**28 questions** — High: 12, Medium: 15, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Consider the three-address code: (1) a = 0  (2) i = 1  (3) t = a + i  (4) a = t  (5) i = i + 1  (6) if i <= 10 goto (3)  (7) print a. The number of basic blocks is

(1) 2  
(2) 4  
(3) 7  
(4) 3  

<details><summary>Answer</summary>

**(4)** — Leaders are (1) (first instruction), (3) (a jump target) and (7) (after a jump): blocks {1, 2}, {3–6} and {7}.

</details>

**Q2.** `High`  
Which of the following instructions are leaders when partitioning three-address code into basic blocks?  
A. The first instruction  B. Any target of a conditional or unconditional jump  C. Any instruction immediately following a jump  D. Every assignment instruction  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A and D only  
(3) A, B, C and D  
(4) A, B and C only  

<details><summary>Answer</summary>

**(4)** — Each basic block runs from a leader up to (but not including) the next leader.

</details>

**Q3.** `High`  
For the basic block a = b + c; b = a − d; c = b + c; d = a − d, the DAG has how many nodes?

(1) 8  
(2) 6  
(3) 7  
(4) 5  

<details><summary>Answer</summary>

**(2)** — Leaves b0, c0, d0 and interior nodes + (a), − (b and d share it) and + (c): 3 + 3 = 6.

</details>

**Q4.** `High`  
In the basic block a = b + c; b = a − d; c = b + c; d = a − d, which optimization is possible?

(1) The statement d = a − d can be replaced by d = b, since a − d was already computed into b  
(2) Loop unrolling  
(3) Removing the first statement  
(4) Constant folding of b + c  

<details><summary>Answer</summary>

**(1)** — This is common subexpression elimination; d has not changed between the two computations of a − d.

</details>

**Q5.** `High`  
For the block (1) a = b + c  (2) d = a − e  (3) b = d + f  (4) return b, the set of variables live at the entry of the block is

(1) {b, c, d, e, f}  
(2) {a, d, e, f}  
(3) {b, c, e, f}  
(4) {a, b, c}  

<details><summary>Answer</summary>

**(3)** — a and d are defined before they are used; b is used in (1) before it is redefined in (3).

</details>

**Q6.** `High`  
Match List I with List II.  
List I (Data-flow problem): A. Reaching definitions  B. Live variables  C. Available expressions  D. Very busy expressions  
List II (Direction and meet operator): I. Backward, intersection  II. Forward, intersection  III. Backward, union  IV. Forward, union

(1) A-III, B-IV, C-II, D-I  
(2) A-IV, B-III, C-I, D-II  
(3) A-IV, B-II, C-III, D-I  
(4) A-IV, B-III, C-II, D-I  

<details><summary>Answer</summary>

**(4)** — "May" problems use union; "must" problems use intersection.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Optimization): A. Constant folding  B. Copy propagation  C. Dead-code elimination  D. Strength reduction  
List II (Example): I. Replacing i × 4 inside a loop by repeated addition of 4  II. Replacing x = 2 × 3.14 by x = 6.28  III. Removing an assignment whose result is never used  IV. After y = x, replacing later uses of y by x

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — Common machine-independent optimizations.

</details>

**Q8.** `High`  
Moving a computation whose value does not change inside a loop to just before the loop is called

(1) loop fusion  
(2) code motion (loop-invariant code motion)  
(3) strength reduction  
(4) loop unrolling  

<details><summary>Answer</summary>

**(2)** — The computation is placed in a preheader block.

</details>

**Q9.** `High`  
Given below are two statements.  
Statement I: Induction-variable elimination increases the number of variables used in a loop.  
Statement II: Loop unrolling increases the number of iterations of a loop.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Induction-variable elimination removes redundant variables, and unrolling reduces the number of iterations.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Loop optimization): A. Loop unrolling  B. Loop fusion (jamming)  C. Loop-invariant code motion  D. Loop fission  
List II (Description): I. Moving computations that do not change inside the loop to outside it  II. Splitting one loop into several loops over the same range  III. Replicating the loop body to reduce loop-control overhead  IV. Combining adjacent loops over the same range into one

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(2)** — Loop transformations improve speed and locality.

</details>

**Q11.** `High`  
Peephole optimization

(1) is done only on the source program  
(2) examines a small window of target (or intermediate) instructions and replaces them with shorter or faster sequences  
(3) builds the symbol table  
(4) examines the whole program at once  

<details><summary>Answer</summary>

**(2)** — Examples: removing redundant loads and stores, unreachable code, jumps to jumps, algebraic simplifications and using machine idioms.

</details>

**Q12.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The instruction sequence MOV R0, a followed immediately by MOV a, R0 can be reduced to the first instruction alone.  
Reason R: The second instruction loads a value different from the one just stored.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Provided the second instruction is not a jump target, it reloads exactly the value already in R0.

</details>

**Q13.** `Medium`  
Replacing a jump to an unconditional jump (goto L1 where L1: goto L2) by goto L2 is an example of

(1) flow-of-control optimization  
(2) constant folding  
(3) register allocation  
(4) algebraic simplification  

<details><summary>Answer</summary>

**(1)** — It may also make L1 unreachable, enabling dead-code removal.

</details>

**Q14.** `Medium`  
Register allocation is often modelled as

(1) a network-flow problem  
(2) sorting  
(3) a shortest-path problem  
(4) graph colouring of the interference graph, with k colours for k registers  

<details><summary>Answer</summary>

**(4)** — Optimal graph colouring is NP-complete, so heuristics are used, and spilling handles failures.

</details>

**Q15.** `Medium`  
Two variables interfere in the interference graph if

(1) they are declared in the same block  
(2) they have the same type  
(3) they are live at the same time  
(4) they are never used  

<details><summary>Answer</summary>

**(3)** — Interfering variables cannot share a register.

</details>

**Q16.** `Medium`  
Given below are two statements.  
Statement I: Local optimization works within a single basic block.  
Statement II: Global optimization works across basic blocks, using data-flow analysis on the flow graph.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Loop optimizations are a major part of global optimization.

</details>

**Q17.** `Medium`  
Instruction scheduling is performed to

(1) build parse trees  
(2) allocate memory  
(3) reorder instructions to avoid pipeline stalls and exploit instruction-level parallelism, while preserving dependences  
(4) reduce program size  

<details><summary>Answer</summary>

**(3)** — List scheduling on the data-dependence graph is a common technique.

</details>

**Q18.** `Medium`  
Which of the following is a machine-dependent optimization?

(1) Common subexpression elimination  
(2) Peephole optimization using a special increment instruction  
(3) Dead-code elimination  
(4) Constant folding  

<details><summary>Answer</summary>

**(2)** — Using machine idioms such as INC depends on the target instruction set.

</details>

**Q19.** `Medium`  
In the flow graph of the code (1) a = 0  (2) i = 1  (3) t = a + i  (4) a = t  (5) i = i + 1  (6) if i <= 10 goto (3)  (7) print a, the number of edges between basic blocks is

(1) 2  
(2) 4  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(4)** — B1 → B2, B2 → B2 (the loop back edge) and B2 → B3.

</details>

**Q20.** `Medium`  
A natural loop in a flow graph is identified by

(1) an edge to the entry node  
(2) a back edge n → d, where d dominates n  
(3) a basic block with one instruction  
(4) any cycle  

<details><summary>Answer</summary>

**(2)** — The loop consists of d plus all nodes that can reach n without passing through d.

</details>

**Q21.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Dead-code elimination can remove the assignment x = y + z if x is not live after it.  
Reason R: Every variable is live at the end of a basic block.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — R is false; liveness analysis computes which variables are live, which is what makes A safe.

</details>

**Q22.** `Medium`  
Algebraic simplification can replace

(1) x = y by x = y + 0  
(2) constants by variables  
(3) loops by recursion  
(4) x = x + 0 and x = x × 1 by nothing, and x × 2 by x + x or a shift  

<details><summary>Answer</summary>

**(4)** — These identities are applied during local optimization or peephole optimization.

</details>

**Q23.** `Medium`  
Next-use information in code generation is used to

(1) decide which values to keep in registers and when a register can be freed  
(2) parse the program  
(3) detect lexical errors  
(4) build the symbol table  

<details><summary>Answer</summary>

**(1)** — It is computed by a backward scan over each basic block.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: Using Ershov numbers with every leaf labelled 1, the expression tree for (a + b) × (c + d) needs 3 registers to be evaluated without storing intermediate values in memory.  
Statement II: Evaluating the subtree that needs more registers first can reduce the number of registers needed.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Each of a + b and c + d is labelled 2; equal labels give the parent 2 + 1 = 3.

</details>

**Q25.** `Medium`  
Which of the following problems are faced by the code generator?  
A. Instruction selection  B. Register allocation  C. Evaluation order  D. Lexical analysis  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) A, B, C and D  
(3) B, C and D only  
(4) A and D only  

<details><summary>Answer</summary>

**(1)** — Lexical analysis is a front-end phase.

</details>

**Q26.** `Medium`  
Common subexpression elimination across basic blocks requires knowing which expressions are

(1) live  
(2) available  
(3) very busy  
(4) dead  

<details><summary>Answer</summary>

**(2)** — An expression is available at a point if it has been computed on every path to it without later changes to its operands.

</details>

**Q27.** `Low`  
Unreachable code is code that

(1) has no variables  
(2) can never be executed on any path  
(3) is executed most often  
(4) is inside loops  

<details><summary>Answer</summary>

**(2)** — For example, statements after an unconditional return or jump with no label.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: An optimization must preserve the meaning (observable behaviour) of the program.  
Statement II: Every optimization always makes a program both faster and smaller.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Some optimizations, such as loop unrolling and inlining, trade size for speed.

</details>
