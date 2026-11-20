# Set 4 — Pushdown Automata and Properties of Context-Free Languages

**28 questions** — High: 11, Medium: 16, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Language class): A. Regular  B. Context-free  C. Context-sensitive  D. Recursively enumerable  
List II (Accepting automaton): I. Linear-bounded automaton  II. Turing machine  III. Finite automaton  IV. Non-deterministic pushdown automaton

(1) A-III, B-IV, C-II, D-I  
(2) A-III, B-I, C-IV, D-II  
(3) A-III, B-IV, C-I, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(3)** — The Chomsky hierarchy and the corresponding machines.

</details>

**Q2.** `High`  
Given below are two statements.  
Statement I: Deterministic PDAs accept exactly the same class of languages as non-deterministic PDAs.  
Statement II: The language {w w^R : w ∈ {a, b}\*} can be accepted by a non-deterministic PDA but not by any deterministic PDA.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — DPDAs accept the proper subclass of deterministic CFLs.

</details>

**Q3.** `High`  
Which of the following languages is a deterministic context-free language?

(1) {w w : w ∈ {a, b}\*}  
(2) {w w^R : w ∈ {a, b}\*}  
(3) {a^n b^n c^n : n ≥ 0}  
(4) {w c w^R : w ∈ {a, b}\*}  

<details><summary>Answer</summary>

**(4)** — The marker c tells the DPDA when to stop pushing and start matching.

</details>

**Q4.** `High`  
Which of the following languages is NOT context-free?

(1) {a^n b^n c^n : n ≥ 0}  
(2) {a^n b^m c^n : n, m ≥ 0}  
(3) {a^n b^n : n ≥ 0}  
(4) {a^n b^n c^m d^m : n, m ≥ 0}  

<details><summary>Answer</summary>

**(1)** — A PDA cannot compare three counts; the pumping lemma for CFLs shows it is not context-free.

</details>

**Q5.** `High`  
Which of the following languages is NOT context-free?

(1) {a^n b^n c^m d^m}  
(2) {a^n b^m c^n d^m}  
(3) {a^n b^m c^m d^n}  
(4) {a^m b^n : m ≠ n}  

<details><summary>Answer</summary>

**(2)** — The crossed dependencies (a with c, b with d) cannot be handled by one stack.

</details>

**Q6.** `High`  
Which of the following languages is NOT context-free?

(1) {w : w has equal numbers of a's and b's}  
(2) {w w : w ∈ {a, b}\*}  
(3) {w w^R : w ∈ {a, b}\*}  
(4) {a^i b^j : i ≤ j}  

<details><summary>Answer</summary>

**(2)** — {ww} needs to compare the first half with the second half in the same order, which a stack cannot do.

</details>

**Q7.** `High`  
Context-free languages are closed under which of the following operations?  
A. Union  B. Intersection  C. Complement  D. Kleene star  E. Intersection with a regular language  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) B, C and E only  
(3) A, D and E only  
(4) A, B and D only  

<details><summary>Answer</summary>

**(3)** — CFLs are closed under union, concatenation, star, homomorphism and intersection with regular languages, but not under intersection or complement.

</details>

**Q8.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Context-free languages are not closed under intersection.  
Reason R: Context-free languages are closed under union.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true; A is shown by {a^n b^n c^m} ∩ {a^m b^n c^n} = {a^n b^n c^n}.

</details>

**Q9.** `Medium`  
Given below are two statements.  
Statement I: Deterministic context-free languages are closed under union.  
Statement II: Deterministic context-free languages are closed under complement.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — DCFLs are closed under complement but not under union or intersection.

</details>

**Q10.** `High`  
A PDA can accept a language by

(1) final state only  
(2) either final state or empty stack; both give the same class of languages for non-deterministic PDAs  
(3) neither  
(4) empty stack only  

<details><summary>Answer</summary>

**(2)** — For DPDAs, acceptance by empty stack accepts only languages with the prefix property.

</details>

**Q11.** `High`  
A PDA with two stacks is equivalent in power to a

(1) linear-bounded automaton  
(2) Turing machine  
(3) one-stack PDA  
(4) finite automaton  

<details><summary>Answer</summary>

**(2)** — Two stacks can simulate the tape of a Turing machine, one holding each side of the head.

</details>

**Q12.** `Medium`  
The transition function of a non-deterministic PDA maps

(1) Q × (Σ ∪ {ε}) × Γ to finite subsets of Q × Γ\*  
(2) Q × Σ × Γ to Q × Γ\*  
(3) Q × Σ to Q  
(4) Q × Γ to Σ  

<details><summary>Answer</summary>

**(1)** — Γ is the stack alphabet.

</details>

**Q13.** `Medium`  
In the pumping lemma for context-free languages, a long string z in L is written as z = uvwxy with

(1) |vx| ≥ 1 and |vwx| ≤ p, and u v^i w x^i y ∈ L for all i ≥ 0  
(2) only v pumped  
(3) |uv| ≤ p  
(4) v = x = ε allowed  

<details><summary>Answer</summary>

**(1)** — Two parts, v and x, are pumped together.

</details>

**Q14.** `Medium`  
Which problem is decidable for context-free grammars?

(1) Whether L(G) = Σ\*  
(2) Whether two CFGs generate the same language  
(3) Whether a CFG is ambiguous  
(4) Whether L(G) is empty  

<details><summary>Answer</summary>

**(4)** — Emptiness, finiteness and membership are decidable for CFLs.

</details>

**Q15.** `High`  
Given below are two statements.  
Statement I: The equivalence of two context-free grammars is undecidable.  
Statement II: Whether the intersection of two context-free languages is empty is undecidable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are undecidable; they are proved by reduction from the Post correspondence problem.

</details>

**Q16.** `Medium`  
The intersection of a context-free language and a regular language is

(1) always context-free  
(2) never context-free  
(3) always regular  
(4) always context-sensitive but not context-free  

<details><summary>Answer</summary>

**(1)** — A PDA and a DFA can run in parallel (product construction).

</details>

**Q17.** `Medium`  
The complement of a context-free language is

(1) always regular  
(2) never context-free  
(3) always context-sensitive (recursive)  
(4) always context-free  

<details><summary>Answer</summary>

**(3)** — Every CFL is recursive, and recursive languages are closed under complement, but the complement need not be context-free.

</details>

**Q18.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The language {a^n b^n : n ≥ 0} is context-free but not regular.  
Reason R: A PDA can push a symbol for each a and pop one for each b, but a finite automaton cannot count without bound.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This is the standard separating example between Type 3 and Type 2.

</details>

**Q19.** `Medium`  
Which of the following is accepted by a deterministic PDA?

(1) {a^n b^n : n ≥ 1} ∪ {a^n b^(2n) : n ≥ 1}  
(2) {a^n b^n : n ≥ 1}  
(3) {w w^R}  
(4) {a^i b^j c^k : i = j or j = k}  

<details><summary>Answer</summary>

**(2)** — The union in option 1 requires guessing whether to match each a with one b or two.

</details>

**Q20.** `Medium`  
Every context-free language without ε can be generated by a grammar in

(1) Greibach normal form only  
(2) Chomsky normal form only  
(3) both Chomsky and Greibach normal forms  
(4) neither  

<details><summary>Answer</summary>

**(3)** — Normal forms do not reduce generative power.

</details>

**Q21.** `Medium`  
Given below are two statements.  
Statement I: Every regular language is a deterministic context-free language.  
Statement II: Every deterministic context-free language is regular.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — {a^n b^n} is a deterministic CFL that is not regular.

</details>

**Q22.** `Medium`  
Context-free languages are closed under

(1) reversal  
(2) set difference  
(3) complement  
(4) intersection  

<details><summary>Answer</summary>

**(1)** — Reverse every production of the grammar.

</details>

**Q23.** `Medium`  
The language {a^m b^n c^k : m = n or n = k} is

(1) context-free and inherently ambiguous  
(2) regular  
(3) deterministic context-free  
(4) not context-free  

<details><summary>Answer</summary>

**(1)** — It is the union of two CFLs, but strings with m = n = k always have two parse trees.

</details>

**Q24.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The language {a^(n²) : n ≥ 0} is not context-free.  
Reason R: The language {a^(n²) : n ≥ 0} can be generated by a regular grammar.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Unary CFLs are regular (Parikh), and {a^(n²)} is not regular, so it is not context-free either.

</details>

**Q25.** `Medium`  
A PDA for {a^n b^n : n ≥ 0} uses the stack to

(1) store the state  
(2) count the a's and match each b with one of them  
(3) reverse the input  
(4) store the whole input  

<details><summary>Answer</summary>

**(2)** — It pushes on a and pops on b, accepting when the stack is empty at the end.

</details>

**Q26.** `Low`  
The stack of a PDA has

(1) unbounded size, but access only at the top  
(2) bounded size  
(3) two ends  
(4) random access  

<details><summary>Answer</summary>

**(1)** — This restricted access is what limits PDAs compared with Turing machines.

</details>

**Q27.** `Medium`  
Which of the following languages is context-free?

(1) {a^p : p prime}  
(2) {a^i b^j c^k : i = j}  
(3) {a^n b^n c^n}  
(4) {w w}  

<details><summary>Answer</summary>

**(2)** — c^k is free, so the language is {a^n b^n} followed by c\*.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: Whether a context-free language is regular is decidable.  
Statement II: Whether a context-free language is finite is decidable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Regularity of a CFL is undecidable; finiteness can be tested by looking for cycles in the variable graph of a CNF grammar.

</details>
