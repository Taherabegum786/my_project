# Set 8 — Software Testing (V&V, white-box and black-box testing, basis path testing, test levels)

**29 questions** — High: 12, Medium: 16, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A program's control flow graph has 9 edges and 7 nodes. Its cyclomatic complexity is

(1) 4  
(2) 3  
(3) 2  
(4) 5  

<details><summary>Answer</summary>

**(1)** — V(G) = E − N + 2 = 9 − 7 + 2 = 4.

</details>

**Q2.** `High`  
The code if (a &gt; b) { if (b &gt; c) x = 1; else x = 2; } else x = 3; while (i &lt; n) i++; has cyclomatic complexity

(1) 2  
(2) 5  
(3) 3  
(4) 4  

<details><summary>Answer</summary>

**(4)** — There are three decisions (two ifs and one while): V(G) = 3 + 1 = 4.

</details>

**Q3.** `High`  
Which of the following are valid ways to compute cyclomatic complexity V(G) of a flow graph?  
A. E − N + 2  B. Number of predicate nodes + 1  C. Number of regions of the planar flow graph  D. Number of nodes − 1  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) B, C and D only  
(3) A, B, C and D  
(4) A and D only  

<details><summary>Answer</summary>

**(1)** — All three give the same value for a connected flow graph.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: Cyclomatic complexity gives an upper bound on the number of tests needed to execute every independent path at least once.  
Statement II: Cyclomatic complexity gives the total number of possible paths through the program.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — It counts linearly independent (basis) paths; the number of complete paths can be far larger, or infinite with loops.

</details>

**Q5.** `High`  
Match List I with List II.  
List I (Term): A. Error  B. Fault (defect, bug)  C. Failure  D. Test oracle  
List II (Meaning): I. A mechanism to decide whether a test passed  II. A human mistake  III. The manifestation of a fault as incorrect behaviour during execution  IV. An incorrect step or data definition in the program

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(4)** — An error leads to a fault, which may cause a failure.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: Verification asks "Are we building the product right?"  
Statement II: Validation asks "Are we building the right product?"

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Boehm's well-known distinction.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Testing technique): A. Equivalence partitioning  B. Boundary value analysis  C. Basis path testing  D. Cause-effect graphing  
List II (Type and idea): I. White-box; uses cyclomatic complexity to derive independent paths  II. Black-box; tests values at the edges of input domains  III. Black-box; maps combinations of input conditions to actions via a decision table  IV. Black-box; divides inputs into classes that are treated alike

(1) A-IV, B-II, C-III, D-I  
(2) A-IV, B-II, C-I, D-III  
(3) A-IV, B-I, C-II, D-III  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(2)** — Black-box techniques use the specification; white-box techniques use the code.

</details>

**Q8.** `High`  
For a function with 2 independent input variables, the number of test cases needed by basic boundary value analysis (min, min+, nominal, max−, max for each variable, holding the others at nominal) is

(1) 9  
(2) 13  
(3) 5  
(4) 25  

<details><summary>Answer</summary>

**(1)** — 4n + 1 = 9; robustness testing needs 6n + 1 = 13 and worst-case testing 5^n = 25.

</details>

**Q9.** `Medium`  
For a function with 3 input variables, worst-case boundary value testing needs how many test cases?

(1) 125  
(2) 13  
(3) 343  
(4) 19  

<details><summary>Answer</summary>

**(1)** — 5^n = 5³ = 125 (robust worst case needs 7³ = 343).

</details>

**Q10.** `High`  
Arrange the levels of testing in the order in which they are normally performed.  
A. System testing  B. Unit testing  C. Acceptance testing  D. Integration testing

(1) B, D, A, C  
(2) B, A, D, C  
(3) D, B, A, C  
(4) B, D, C, A  

<details><summary>Answer</summary>

**(1)** — Each level tests larger units of the system.

</details>

**Q11.** `High`  
Match List I with List II.  
List I (Test type): A. Alpha testing  B. Beta testing  C. Regression testing  D. Stress testing  
List II (Description): I. Re-running tests after changes to ensure nothing else broke  II. Conducted at the developer's site by end users  III. Executing the system under abnormal quantities, frequencies or volumes of resources  IV. Conducted at one or more customer sites, without the developer present

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — Types of testing from Pressman.

</details>

**Q12.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In top-down integration testing, drivers are needed to call the top-level module.  
Reason R: Lower-level modules called by the module under test may not yet be ready.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Top-down integration needs stubs for missing lower-level modules (as R implies); drivers are needed in bottom-up integration.

</details>

**Q13.** `Medium`  
In bottom-up integration testing, the components that simulate higher-level modules calling the module under test are called

(1) oracles  
(2) drivers  
(3) stubs  
(4) mocks only  

<details><summary>Answer</summary>

**(2)** — Stubs replace lower-level modules called by the unit under test.

</details>

**Q14.** `High`  
Given below are two statements.  
Statement I: Statement coverage subsumes branch coverage.  
Statement II: Branch (decision) coverage subsumes statement coverage.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Covering every branch executes every statement, but not the other way round (for example an if with no else).

</details>

**Q15.** `Medium`  
Arrange the following coverage criteria from the weakest to the strongest.  
A. Path coverage  B. Statement coverage  C. Branch coverage

(1) B, A, C  
(2) C, B, A  
(3) A, C, B  
(4) B, C, A  

<details><summary>Answer</summary>

**(4)** — Full path coverage is usually infeasible with loops.

</details>

**Q16.** `Medium`  
The statement "Program testing can be used to show the presence of bugs, but never to show their absence" is due to

(1) Edsger Dijkstra  
(2) Watts Humphrey  
(3) Barry Boehm  
(4) Glenford Myers  

<details><summary>Answer</summary>

**(1)** — Exhaustive testing is impossible for any non-trivial program.

</details>

**Q17.** `Medium`  
In mutation testing, 50 mutants are generated, 5 of them are equivalent to the original program, and the test suite kills 40. The mutation score is about

(1) 85%  
(2) 80%  
(3) 89%  
(4) 90%  

<details><summary>Answer</summary>

**(3)** — Mutation score = killed / (total − equivalent) = 40 / 45 ≈ 0.89.

</details>

**Q18.** `Medium`  
Smoke testing is

(1) testing done by customers  
(2) a preliminary integration test, often daily, to check that the build's critical functions work  
(3) a test of the system under extreme heat  
(4) testing only the user interface  

<details><summary>Answer</summary>

**(2)** — It is common in projects using daily builds.

</details>

**Q19.** `Medium`  
Data-flow testing selects test paths according to

(1) the user interface  
(2) the number of loops  
(3) the locations of definitions and uses of variables (DU chains)  
(4) equivalence classes  

<details><summary>Answer</summary>

**(3)** — It is a white-box control-structure testing technique.

</details>

**Q20.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Black-box testing can detect missing functionality.  
Reason R: Black-box tests are derived from the code structure.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Black-box tests come from the specification, which is exactly why they can reveal functions the code omits.

</details>

**Q21.** `Medium`  
Loop testing distinguishes among

(1) infinite and finite loops  
(2) recursive and iterative loops  
(3) simple, nested, concatenated and unstructured loops  
(4) for, while and do-while loops only  

<details><summary>Answer</summary>

**(3)** — Unstructured loops should be redesigned before testing.

</details>

**Q22.** `Medium`  
Recovery testing checks

(1) how well the system recovers from crashes, hardware failures and similar problems  
(2) the speed of the system  
(3) the user interface  
(4) the documentation  

<details><summary>Answer</summary>

**(1)** — It forces the software to fail and verifies that recovery is performed properly.

</details>

**Q23.** `Medium`  
Given below are two statements.  
Statement I: Static testing, such as reviews and inspections, finds defects without executing the program.  
Statement II: Dynamic testing requires executing the program.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are forms of verification.

</details>

**Q24.** `Medium`  
A flow graph has 12 edges, 10 nodes and 2 connected components. Its cyclomatic complexity is

(1) 8  
(2) 2  
(3) 4  
(4) 6  

<details><summary>Answer</summary>

**(4)** — V(G) = E − N + 2P = 12 − 10 + 4 = 6.

</details>

**Q25.** `Medium`  
The debugging approach that works backwards from the place where a symptom appears to the cause is called

(1) backtracking  
(2) cause elimination  
(3) regression  
(4) brute force  

<details><summary>Answer</summary>

**(1)** — Cause elimination uses induction or deduction with binary partitioning.

</details>

**Q26.** `Medium`  
Given below are two statements.  
Statement I: Performance testing measures run-time performance in the context of an integrated system.  
Statement II: Security testing verifies that protection mechanisms built into a system protect it from improper penetration.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are kinds of system testing.

</details>

**Q27.** `Low`  
Unit testing is usually performed by

(1) the end users  
(2) the developers of the module  
(3) the customers at their site  
(4) the marketing team  

<details><summary>Answer</summary>

**(2)** — It focuses on the smallest unit of design, such as a component or class.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: Exhaustive testing of all inputs is practical for most programs.  
Statement II: White-box testing alone can guarantee that a program meets its specification.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Exhaustive testing is infeasible, and white-box testing cannot detect missing functions required by the specification.

</details>

**Q29.** `Medium`  
A decision table with 3 independent Boolean conditions has at most how many rules (columns)?

(1) 6  
(2) 9  
(3) 8  
(4) 3  

<details><summary>Answer</summary>

**(3)** — Each condition can be true or false: 2³ = 8 combinations.

</details>
