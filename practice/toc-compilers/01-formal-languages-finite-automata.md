# Set 1 — Formal Languages, Diagonalization and Finite Automata (DFA, NFA, minimization, Moore and Mealy machines)

**38 questions** — High: 15, Medium: 22, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The minimum number of states in a DFA over {0, 1} accepting strings in which the number of 0s is divisible by 3 is

(1) 3  
(2) 2  
(3) 4  
(4) 6  

<details><summary>Answer</summary>

**(1)** — The DFA counts 0s modulo 3; 1s do not change the state.

</details>

**Q2.** `High`  
The minimum number of states in a DFA that accepts binary numbers divisible by 5 (reading the most significant bit first, and treating the empty string as 0) is

(1) 5  
(2) 4  
(3) 6  
(4) 10  

<details><summary>Answer</summary>

**(1)** — One state for each remainder 0–4; reading bit b takes remainder r to (2r + b) mod 5.

</details>

**Q3.** `High`  
The minimum number of states in a DFA over {0, 1} accepting all strings that end with 01 is

(1) 2  
(2) 5  
(3) 4  
(4) 3  

<details><summary>Answer</summary>

**(4)** — States track the longest suffix that is a prefix of 01: ε, 0 and 01.

</details>

**Q4.** `High`  
The minimum number of states in a DFA over {0, 1} accepting all strings that contain 101 as a substring is

(1) 3  
(2) 6  
(3) 5  
(4) 4  

<details><summary>Answer</summary>

**(4)** — States for ε, 1, 10 and 101 (the last one is a trap accepting state).

</details>

**Q5.** `High`  
The minimum number of states in a DFA over {0, 1} accepting strings whose third symbol from the right end is 1 is

(1) 4  
(2) 8  
(3) 6  
(4) 3  

<details><summary>Answer</summary>

**(2)** — The DFA must remember the last three symbols: 2³ = 8 states. An NFA needs only 4.

</details>

**Q6.** `High`  
A minimal DFA for strings over {0, 1} in which the nth symbol from the right is 1 has

(1) n² states  
(2) 2n states  
(3) n + 1 states  
(4) 2^n states  

<details><summary>Answer</summary>

**(4)** — This family shows that the subset construction can cause an exponential blow-up.

</details>

**Q7.** `High`  
The minimum number of states in a DFA over {0, 1} accepting strings with an even number of 0s and an odd number of 1s is

(1) 2  
(2) 3  
(3) 6  
(4) 4  

<details><summary>Answer</summary>

**(4)** — One state for each combination of parities.

</details>

**Q8.** `High`  
The minimum number of states in a DFA over {0, 1} accepting strings that start with 1 and end with 0 is

(1) 5  
(2) 4  
(3) 3  
(4) 6  

<details><summary>Answer</summary>

**(2)** — A start state, a dead state (string begins with 0), and two states for "starts with 1, last symbol 0 or 1".

</details>

**Q9.** `Medium`  
The minimum number of states in a DFA over {0, 1} accepting all strings of length exactly 3 is

(1) 3  
(2) 4  
(3) 8  
(4) 5  

<details><summary>Answer</summary>

**(4)** — States count the length 0, 1, 2, 3, plus a dead state for longer strings.

</details>

**Q10.** `Medium`  
The minimum number of states in a DFA over {0, 1} accepting strings that contain exactly two 1s is

(1) 6  
(2) 3  
(3) 4  
(4) 5  

<details><summary>Answer</summary>

**(3)** — States for zero, one and two 1s, plus a dead state for more than two.

</details>

**Q11.** `Medium`  
The minimum number of states in a DFA over {a, b} accepting strings in which the number of a's is even and the number of b's is divisible by 3 is

(1) 8  
(2) 12  
(3) 6  
(4) 5  

<details><summary>Answer</summary>

**(3)** — Product of a mod-2 counter and a mod-3 counter: 2 × 3 = 6.

</details>

**Q12.** `Medium`  
The minimum number of states in a DFA over {0, 1} accepting strings in which the first and last symbols are the same (strings of length at least 1) is

(1) 4  
(2) 3  
(3) 5  
(4) 6  

<details><summary>Answer</summary>

**(3)** — A start state, then for each first symbol a state for "last symbol same" and one for "last symbol different".

</details>

**Q13.** `High`  
In the subset construction, an NFA with n states can result in a DFA with at most

(1) n states  
(2) 2^n states  
(3) n² states  
(4) 2n states  

<details><summary>Answer</summary>

**(2)** — Each DFA state is a subset of the NFA states.

</details>

**Q14.** `High`  
Given below are two statements.  
Statement I: An NFA with ε-transitions accepts a larger class of languages than an NFA without them.  
Statement II: Every NFA can be converted into an equivalent DFA.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — DFAs, NFAs and ε-NFAs all accept exactly the regular languages.

</details>

**Q15.** `High`  
Match List I with List II.  
List I (Machine): A. Moore machine  B. Mealy machine  C. DFA  D. Two-way DFA  
List II (Property): I. Accepts only regular languages despite moving the head in both directions  II. Output depends on the current state and the current input  III. Output depends only on the current state  IV. Has no output other than accept or reject

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(1)** — Moore and Mealy machines are finite-state transducers.

</details>

**Q16.** `Medium`  
For an input string of length n, a Moore machine produces an output string of length

(1) n + 1  
(2) n  
(3) n − 1  
(4) 2n  

<details><summary>Answer</summary>

**(1)** — It produces an output in the start state before reading any input; a Mealy machine produces n outputs.

</details>

**Q17.** `Medium`  
Given below are two statements.  
Statement I: Every Mealy machine can be converted into an equivalent Moore machine, possibly with more states.  
Statement II: Every Moore machine can be converted into an equivalent Mealy machine with the same number of states.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The equivalence ignores the extra initial output of the Moore machine.

</details>

**Q18.** `High`  
In a DFA, the transition function δ maps

(1) Q × (Σ ∪ {ε}) to 2^Q  
(2) Q × Σ to Q  
(3) Q to Σ  
(4) Q × Σ to 2^Q  

<details><summary>Answer</summary>

**(2)** — For an NFA, δ maps Q × Σ (or Q × (Σ ∪ {ε})) to 2^Q.

</details>

**Q19.** `High`  
The Myhill-Nerode theorem implies that a language L is regular if and only if

(1) L has a regular grammar with ε-productions  
(2) L is finite  
(3) the relation "xz ∈ L exactly when yz ∈ L for all z" has finitely many equivalence classes  
(4) L is accepted by a PDA  

<details><summary>Answer</summary>

**(3)** — The number of classes equals the number of states of the minimal DFA.

</details>

**Q20.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The minimal DFA for a regular language is unique up to renaming of states.  
Reason R: Its states correspond one-to-one to the Myhill-Nerode equivalence classes of the language.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — DFA minimization merges indistinguishable states.

</details>

**Q21.** `Medium`  
In DFA minimization by the table-filling (partitioning) method, two states are distinguishable if

(1) both are accepting  
(2) some string leads one of them to an accepting state and the other to a non-accepting state  
(3) they are reachable from the start state  
(4) they have the same number of transitions  

<details><summary>Answer</summary>

**(2)** — The initial partition separates accepting and non-accepting states.

</details>

**Q22.** `High`  
The set of all languages over the alphabet {0, 1} is

(1) empty  
(2) uncountable  
(3) finite  
(4) countably infinite  

<details><summary>Answer</summary>

**(2)** — It is the power set of the countable set Σ*, which is uncountable by Cantor's diagonal argument.

</details>

**Q23.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: There exist languages that are not accepted by any Turing machine.  
Reason R: A Turing machine can simulate any finite automaton.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but A follows from counting: there are countably many TMs and uncountably many languages.

</details>

**Q24.** `Medium`  
Cantor's diagonal argument is used to prove that

(1) the set of real numbers in [0, 1] is uncountable  
(2) every TM halts  
(3) every language is regular  
(4) the set of integers is countable  

<details><summary>Answer</summary>

**(1)** — A number differing from the ith listed number in the ith digit cannot be in the list.

</details>

**Q25.** `Medium`  
Russell's paradox concerns

(1) the number of states in a DFA  
(2) the pumping lemma  
(3) the set of all sets that do not contain themselves  
(4) the halting of Turing machines  

<details><summary>Answer</summary>

**(3)** — Such a set contains itself if and only if it does not; it showed that naive set theory is inconsistent.

</details>

**Q26.** `Medium`  
Given below are two statements.  
Statement I: The set of all subsets of the natural numbers is countable.  
Statement II: The set of all strings over a finite alphabet is countable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Strings can be listed by length; the power set of N is uncountable.

</details>

**Q27.** `Medium`  
The number of strings of length at most n over the alphabet {0, 1}, including the empty string, is

(1) 2^n  
(2) n²  
(3) 2^(n+1) − 1  
(4) 2^n − 1  

<details><summary>Answer</summary>

**(3)** — 1 + 2 + 4 + ... + 2^n = 2^(n+1) − 1.

</details>

**Q28.** `Medium`  
The number of strings of length 5 over {0, 1} that do not contain two consecutive 1s is

(1) 13  
(2) 8  
(3) 21  
(4) 16  

<details><summary>Answer</summary>

**(1)** — The counts follow the Fibonacci sequence: 2, 3, 5, 8, 13 for lengths 1 to 5.

</details>

**Q29.** `Medium`  
A DFA with n states accepts a non-empty language if and only if it accepts some string of length

(1) n²  
(2) less than n  
(3) greater than 2n  
(4) exactly n  

<details><summary>Answer</summary>

**(2)** — A shortest accepted string visits no state twice.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: A DFA with n states accepts an infinite language if and only if it accepts some string of length between n and 2n − 1.  
Statement II: Whether a DFA accepts an infinite language is undecidable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Finiteness of a regular language is decidable, using exactly the test in Statement I.

</details>

**Q31.** `Medium`  
The minimum number of states of a DFA over {0, 1} that accepts strings of length divisible by 2 or by 3 is

(1) 7  
(2) 6  
(3) 12  
(4) 5  

<details><summary>Answer</summary>

**(2)** — The DFA counts length modulo lcm(2, 3) = 6.

</details>

**Q32.** `Medium`  
Which of the following is true of a dead (trap) state in a DFA?

(1) It is the start state  
(2) It is always accepting  
(3) Every transition from it leads back to itself, and it is non-accepting  
(4) It has no outgoing transitions  

<details><summary>Answer</summary>

**(3)** — It is often omitted in drawings to give a partial DFA.

</details>

**Q33.** `Medium`  
Lexical analyzers are typically implemented using

(1) pushdown automata  
(2) linear-bounded automata  
(3) finite automata  
(4) Turing machines  

<details><summary>Answer</summary>

**(3)** — Token patterns are regular expressions, which are converted to DFAs (as by Lex).

</details>

**Q34.** `Low`  
The language accepted by a finite automaton is called a

(1) context-free language  
(2) recursive language  
(3) regular language  
(4) context-sensitive language  

<details><summary>Answer</summary>

**(3)** — Kleene's theorem: finite automata and regular expressions describe the same languages.

</details>

**Q35.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Finite automata cannot recognise the language {0^n 1^n : n ≥ 0}.  
Reason R: A finite automaton has no way to remember an unbounded count with finitely many states.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This language needs a stack (a PDA).

</details>

**Q36.** `Medium`  
Given below are two statements.  
Statement I: An NFA accepts a string if every possible computation path ends in an accepting state.  
Statement II: An NFA may have several transitions on the same symbol from one state.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — An NFA accepts if at least one computation path ends in an accepting state.

</details>

**Q37.** `Medium`  
The minimum number of states in a DFA over {0, 1} accepting strings that do not contain two consecutive 1s is

(1) 4  
(2) 2  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(4)** — States for "last symbol not 1", "last symbol 1" and a dead state after 11.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: The complement of a DFA's language is obtained by reversing all its transitions.  
Statement II: The complement of an NFA's language is always obtained by swapping its accepting and non-accepting states.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Swapping accepting states complements a DFA (reversing transitions gives the reversal); for an NFA the swap does not work in general.

</details>
