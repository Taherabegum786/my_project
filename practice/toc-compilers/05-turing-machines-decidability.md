# Set 5 — Turing Machines, Chomsky Hierarchy, Decidability and Unsolvable Problems

**31 questions** — High: 13, Medium: 17, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Grammar type in the Chomsky hierarchy): A. Type 0  B. Type 1  C. Type 2  D. Type 3  
List II (Grammar): I. Regular  II. Unrestricted  III. Context-free  IV. Context-sensitive

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Type 0 ⊃ Type 1 ⊃ Type 2 ⊃ Type 3.

</details>

**Q2.** `High`  
A context-sensitive grammar has productions α → β with

(1) |α| ≤ |β| (non-contracting), except possibly S → ε  
(2) β = ε allowed everywhere  
(3) α a single terminal  
(4) |α| = 1  

<details><summary>Answer</summary>

**(1)** — Context-sensitive languages are accepted by linear-bounded automata.

</details>

**Q3.** `High`  
Given below are two statements.  
Statement I: Every recursive language is recursively enumerable.  
Statement II: Every recursively enumerable language is recursive.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The halting problem is recursively enumerable but not recursive.

</details>

**Q4.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: If a language L and its complement are both recursively enumerable, then L is recursive.  
Reason R: Turing machines for L and its complement can be run in parallel, and exactly one of them accepts any given input.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The combined machine always halts with the right answer.

</details>

**Q5.** `High`  
The halting problem for Turing machines is

(1) decidable  
(2) regular  
(3) not recursively enumerable  
(4) recursively enumerable but undecidable  

<details><summary>Answer</summary>

**(4)** — A universal TM can simulate and accept when the machine halts, but no TM decides it.

</details>

**Q6.** `High`  
The complement of the halting problem is

(1) context-free  
(2) recursively enumerable but not recursive  
(3) not recursively enumerable  
(4) recursive  

<details><summary>Answer</summary>

**(3)** — If both it and HALT were RE, HALT would be decidable.

</details>

**Q7.** `High`  
Rice's theorem states that

(1) every TM halts on some input  
(2) every non-trivial property of the languages recognised by Turing machines is undecidable  
(3) every property of Turing machines is decidable  
(4) the halting problem is decidable for LBAs  

<details><summary>Answer</summary>

**(2)** — For example, whether L(M) is empty, finite or regular is undecidable.

</details>

**Q8.** `High`  
Which of the following problems is decidable?

(1) Whether two TMs accept the same language  
(2) Whether a TM accepts a regular language  
(3) Whether a TM halts on the empty input  
(4) Whether a DFA accepts a given string  

<details><summary>Answer</summary>

**(4)** — Membership, emptiness and equivalence are decidable for DFAs.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Problem): A. Membership for context-sensitive languages  B. Emptiness for context-free grammars  C. The halting problem  D. The complement of the halting problem  
List II (Status): I. Not recursively enumerable  II. Decidable, but PSPACE-complete in general  III. Recursively enumerable but not recursive  IV. Decidable in polynomial time

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(4)** — If both HALT and its complement were recursively enumerable, HALT would be decidable.

</details>

**Q10.** `High`  
The Post correspondence problem (PCP) is

(1) undecidable in general, but decidable for a one-letter alphabet  
(2) decidable for any alphabet  
(3) in P  
(4) context-free  

<details><summary>Answer</summary>

**(1)** — PCP is the standard tool for proving undecidability results about CFGs.

</details>

**Q11.** `Medium`  
A Post correspondence problem instance has the dominoes (top, bottom): A = (b, bbb), B = (babbb, ba), C = (ba, a). Which sequence is a solution?

(1) A C B  
(2) C A  
(3) A B  
(4) B A A C  

<details><summary>Answer</summary>

**(4)** — B A A C gives babbb·b·b·ba = babbbbbba on top and ba·bbb·bbb·a = babbbbbba on the bottom.

</details>

**Q12.** `High`  
Given below are two statements.  
Statement I: A multi-tape Turing machine can recognise languages that no single-tape Turing machine can.  
Statement II: A non-deterministic Turing machine can be simulated by a deterministic Turing machine.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Multi-tape TMs add speed (at most quadratic simulation overhead) but no power; non-determinism adds no power either.

</details>

**Q13.** `High`  
Which of the following models is NOT equivalent in power to a standard Turing machine?

(1) Multi-tape TM  
(2) Non-deterministic TM  
(3) Linear-bounded automaton  
(4) PDA with two stacks  

<details><summary>Answer</summary>

**(3)** — An LBA can use only the tape space occupied by its input and accepts exactly the context-sensitive languages.

</details>

**Q14.** `High`  
The Church-Turing thesis states that

(1) any function that can be computed by an effective procedure can be computed by a Turing machine  
(2) P = NP  
(3) Turing machines are faster than computers  
(4) every problem is decidable  

<details><summary>Answer</summary>

**(1)** — It is a thesis about the informal notion of computability, not a provable theorem.

</details>

**Q15.** `Medium`  
A universal Turing machine is one that

(1) has only two states  
(2) accepts only regular languages  
(3) takes the encoding of any TM M and an input w and simulates M on w  
(4) accepts every string  

<details><summary>Answer</summary>

**(3)** — It is the theoretical model of a stored-program computer.

</details>

**Q16.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The diagonal language L\_d = {w\_i : M\_i does not accept w\_i} is recursively enumerable.  
Reason R: If some TM M\_j accepted L\_d, then w\_j would be in L\_d exactly when it is not.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — R is the contradiction that proves L\_d is not recursively enumerable.

</details>

**Q17.** `Medium`  
Which of the following is closed under complement?  
A. Regular languages  B. Recursive languages  C. Recursively enumerable languages  D. Context-sensitive languages  
Choose the correct answer from the options given below:

(1) B and C only  
(2) A, B, C and D  
(3) A, B and D only  
(4) A and C only  

<details><summary>Answer</summary>

**(3)** — CSLs are closed under complement by the Immerman-Szelepcsényi theorem; RE languages are not.

</details>

**Q18.** `Medium`  
A Turing machine that halts on every input is called a

(1) transducer only  
(2) decider (total TM)  
(3) linear-bounded automaton  
(4) recogniser  

<details><summary>Answer</summary>

**(2)** — The languages of deciders are the recursive languages.

</details>

**Q19.** `Medium`  
Arrange the following classes of languages in increasing order of inclusion.  
A. Context-free  B. Recursive  C. Regular  D. Context-sensitive  E. Recursively enumerable

(1) C, D, A, B, E  
(2) A, C, D, B, E  
(3) C, A, B, D, E  
(4) C, A, D, B, E  

<details><summary>Answer</summary>

**(4)** — Regular ⊂ CFL ⊂ CSL ⊂ recursive ⊂ RE, all inclusions proper.

</details>

**Q20.** `Medium`  
Given below are two statements.  
Statement I: Every recursive language is context-sensitive.  
Statement II: Every context-sensitive language is recursive.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — There are recursive languages that are not context-sensitive (by diagonalization).

</details>

**Q21.** `Medium`  
Which of the following problems about a Turing machine M is decidable?

(1) Whether M halts on all inputs  
(2) Whether L(M) is regular  
(3) Whether L(M) is empty  
(4) Whether M has more than 10 states  

<details><summary>Answer</summary>

**(4)** — It is a property of the machine's description, not of its language, so Rice's theorem does not apply.

</details>

**Q22.** `Medium`  
Which problem is undecidable for context-free grammars?

(1) Membership  
(2) Whether L(G) = Σ\*  
(3) Finiteness  
(4) Emptiness  

<details><summary>Answer</summary>

**(2)** — Universality of CFGs is undecidable.

</details>

**Q23.** `Medium`  
If problem A reduces to problem B (A ≤ B) and A is undecidable, then

(1) nothing can be concluded  
(2) A is decidable  
(3) B is decidable  
(4) B is undecidable  

<details><summary>Answer</summary>

**(4)** — A decider for B would give a decider for A.

</details>

**Q24.** `Medium`  
A Turing machine that computes the function f(n) = n + 1 on unary input 1^n must

(1) erase all symbols  
(2) reverse the input  
(3) never halt  
(4) move to the end of the input and write one more 1  

<details><summary>Answer</summary>

**(4)** — Such simple constructions are typical exam exercises.

</details>

**Q25.** `Medium`  
Given below are two statements.  
Statement I: Every Turing machine halts on every input.  
Statement II: The set of strings on which a given TM halts is always recursive.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — A TM may loop forever, and its halting set is recursively enumerable but not necessarily recursive.

</details>

**Q26.** `Medium`  
A linear-bounded automaton is a Turing machine whose tape head

(1) has two tapes  
(2) can move only to the right  
(3) has no tape  
(4) stays within the portion of the tape containing the input  

<details><summary>Answer</summary>

**(4)** — LBAs accept exactly the context-sensitive languages.

</details>

**Q27.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The emptiness problem for linear-bounded automata is undecidable.  
Reason R: The membership problem for linear-bounded automata is undecidable.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — LBA membership is decidable (finitely many configurations), while LBA emptiness is undecidable.

</details>

**Q28.** `Medium`  
The number of Turing machines (with a fixed tape alphabet) is

(1) zero  
(2) finite  
(3) countably infinite  
(4) uncountable  

<details><summary>Answer</summary>

**(3)** — Each TM has a finite description that can be encoded as a string.

</details>

**Q29.** `Low`  
The Turing machine model was proposed by Alan Turing in

(1) 1971  
(2) 1956  
(3) 1936  
(4) 1926  

<details><summary>Answer</summary>

**(3)** — His paper "On Computable Numbers" also introduced the universal machine.

</details>

**Q30.** `Medium`  
In the standard TM, one move consists of

(1) reading the whole input at once  
(2) reading a symbol, writing a symbol, moving the head one cell left or right, and changing state  
(3) reading a symbol only  
(4) popping a stack  

<details><summary>Answer</summary>

**(2)** — δ: Q × Γ → Q × Γ × {L, R}.

</details>

**Q31.** `Medium`  
Given below are two statements.  
Statement I: The class P is closed under complement.  
Statement II: The class NP is known to be closed under complement.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Whether NP = co-NP is an open problem.

</details>
