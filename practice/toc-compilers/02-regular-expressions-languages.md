# Set 2 — Regular Expressions, Regular Grammars, Closure Properties and the Pumping Lemma

**33 questions** — High: 12, Medium: 20, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Which of the following regular expressions is equivalent to (a + b)*?

(1) (ab)*  
(2) (a*b*)*  
(3) a* + b*  
(4) a*b*  

<details><summary>Answer</summary>

**(2)** — (a*b*)* can generate any string of a's and b's; a* + b* and a*b* cannot generate "ba".

</details>

**Q2.** `High`  
Which of the following identities about regular expressions is FALSE?

(1) (a + b)* = a* + b*  
(2) (ab)*a = a(ba)*  
(3) (a*)* = a*  
(4) a*a* = a*  

<details><summary>Answer</summary>

**(1)** — a* + b* does not contain mixed strings such as ab.

</details>

**Q3.** `High`  
By Arden's theorem, the equation R = Q + RP, where P does not contain ε, has the unique solution

(1) R = Q*P  
(2) R = PQ*  
(3) R = (P + Q)*  
(4) R = QP*  

<details><summary>Answer</summary>

**(4)** — It is used to derive a regular expression from a finite automaton.

</details>

**Q4.** `High`  
The regular expression 0*(10*)* denotes

(1) strings ending in 0  
(2) strings with an even number of 1s  
(3) all strings over {0, 1}  
(4) strings with no two consecutive 1s  

<details><summary>Answer</summary>

**(3)** — Any string can be written as a block of 0s followed by blocks each starting with a 1.

</details>

**Q5.** `High`  
A regular expression for strings over {a, b} that end with "ab" is

(1) ab(a + b)*  
(2) a*b*ab  
(3) (a + b)*ab(a + b)*  
(4) (a + b)*ab  

<details><summary>Answer</summary>

**(4)** — ab(a + b)* gives strings starting with ab, and (a + b)*ab(a + b)* gives those containing ab.

</details>

**Q6.** `Medium`  
Which regular expression describes strings over {0, 1} with at least one 1?

(1) (0 + 1)*0  
(2) 0*1*  
(3) (01)*  
(4) 0*1(0 + 1)*  

<details><summary>Answer</summary>

**(4)** — The first 1 can be preceded by any number of 0s and followed by anything.

</details>

**Q7.** `Medium`  
The regular expression (0 + 1)*1(0 + 1)(0 + 1) describes strings in which

(1) the third symbol from the left is 1  
(2) the string ends in 111  
(3) the third symbol from the right is 1  
(4) there are three 1s  

<details><summary>Answer</summary>

**(3)** — Exactly two symbols follow the chosen 1.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Language): A. {a^n b^n : n ≥ 0}  B. {a^m b^n : m, n ≥ 0}  C. {a^n b^n c^n : n ≥ 0}  D. {w w^R : w ∈ {a, b}*}  
List II (Smallest class containing it): I. Regular  II. Context-sensitive but not context-free  III. Context-free but not regular (deterministic)  IV. Context-free but not deterministic context-free

(1) A-III, B-I, C-II, D-IV  
(2) A-III, B-II, C-I, D-IV  
(3) A-I, B-III, C-II, D-IV  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(1)** — {w w^R} needs non-determinism to guess the middle; {w c w^R} is deterministic.

</details>

**Q9.** `High`  
Which of the following languages is regular?

(1) {w : w has equal numbers of a's and b's}  
(2) {a^p : p is prime}  
(3) {a^n b^n : n ≥ 1}  
(4) {a^n b^n : 1 ≤ n ≤ 100}  

<details><summary>Answer</summary>

**(4)** — Any finite language is regular.

</details>

**Q10.** `High`  
Which of the following languages is regular?

(1) {a^n b^m : n > m}  
(2) {w ∈ {a, b}* : #a(w) mod 3 = #b(w) mod 3}  
(3) {w ∈ {a, b}* : #a(w) = #b(w)}  
(4) {a^(n²) : n ≥ 1}  

<details><summary>Answer</summary>

**(2)** — A DFA tracks (#a − #b) mod 3 with 3 states.

</details>

**Q11.** `High`  
Given below are two statements.  
Statement I: If a language satisfies the conditions of the pumping lemma, it must be regular.  
Statement II: The pumping lemma can be used to prove that a language is not regular.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Some non-regular languages satisfy the pumping conditions, so the lemma is only a necessary condition.

</details>

**Q12.** `High`  
In the pumping lemma for regular languages, a string w with |w| ≥ p is split as w = xyz with

(1) |y| ≥ p  
(2) |y| ≥ 1 and |xy| ≤ p, and xy^i z ∈ L for all i ≥ 0  
(3) y = ε allowed and |xy| ≤ p  
(4) x = ε always  

<details><summary>Answer</summary>

**(2)** — p is the pumping length (at most the number of DFA states).

</details>

**Q13.** `High`  
Match List I with List II.  
List I (Class of languages): A. Context-free languages  B. Deterministic context-free languages  C. Recursively enumerable languages  D. Regular languages  
List II (An operation under which the class is NOT closed): I. Union  II. Intersection  III. Complement  IV. Infinite union

(1) A-II, B-I, C-III, D-IV  
(2) A-II, B-III, C-I, D-IV  
(3) A-III, B-I, C-II, D-IV  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(1)** — RE languages are closed under intersection and union, DCFLs under complement, and regular languages under complement, which rules out each distractor.

</details>

**Q14.** `High`  
Which of the following operations are regular languages NOT closed under?

(1) Reversal  
(2) Union  
(3) Complement  
(4) Infinite union  

<details><summary>Answer</summary>

**(4)** — An infinite union of the finite languages {a^n b^n} gives the non-regular {a^n b^n : n ≥ 0}.

</details>

**Q15.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The intersection of two regular languages is regular.  
Reason R: The intersection is accepted by a DFA whose states are the union of the two DFAs' state sets.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — The product construction uses pairs of states, running both DFAs in parallel.

</details>

**Q16.** `Medium`  
If L1 is regular and L2 is any language, then L1 ∪ L2 is

(1) regular or non-regular, depending on L2  
(2) always non-regular  
(3) always regular  
(4) always context-free  

<details><summary>Answer</summary>

**(1)** — For example, with L1 = ∅ the result is L2, which may be non-regular.

</details>

**Q17.** `Medium`  
A right-linear grammar has productions of the form

(1) any production  
(2) A → Bx  
(3) A → BC or A → a  
(4) A → xB or A → x, where x is a string of terminals  

<details><summary>Answer</summary>

**(4)** — Right-linear and left-linear grammars both generate exactly the regular languages.

</details>

**Q18.** `Medium`  
Given below are two statements.  
Statement I: A grammar mixing left-linear and right-linear productions always generates a regular language.  
Statement II: Every regular language can be generated by a right-linear grammar.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Mixing them can generate {a^n b^n}: S → aA, A → Sb, S → ε.

</details>

**Q19.** `Medium`  
The regular expression for the language over {a, b} in which every string has an even number of a's is

(1) (aa + b)*  
(2) a*b*a*  
(3) (b*ab*ab*)*  
(4) b*(ab*ab*)*  

<details><summary>Answer</summary>

**(4)** — After any leading b's, a's come in pairs separated by any number of b's.

</details>

**Q20.** `Medium`  
Which of the following is the language of the regular expression (a + ε)(b + ε)?

(1) {ε, ab}  
(2) {ε, a, b, ab}  
(3) {ab}  
(4) {a, b, ab}  

<details><summary>Answer</summary>

**(2)** — Each factor contributes its symbol or nothing.

</details>

**Q21.** `Medium`  
The value of ∅* is

(1) undefined  
(2) {ε}  
(3) Σ*  
(4) ∅  

<details><summary>Answer</summary>

**(2)** — The Kleene star of any language contains ε; ε* is also {ε}.

</details>

**Q22.** `Medium`  
Which of the following problems is decidable for regular languages?  
A. Membership  B. Emptiness  C. Finiteness  D. Equivalence of two regular languages  
Choose the correct answer from the options given below:

(1) B and D only  
(2) A, B, C and D  
(3) A and B only  
(4) A, B and C only  

<details><summary>Answer</summary>

**(2)** — All of these are decidable using DFAs.

</details>

**Q23.** `Medium`  
The reversal of a regular language is

(1) context-free but not regular  
(2) never regular  
(3) regular only if the language is finite  
(4) always regular  

<details><summary>Answer</summary>

**(4)** — Reverse the edges of an NFA and swap the start and accepting states.

</details>

**Q24.** `Medium`  
The quotient L1/L2 = {x : xy ∈ L1 for some y ∈ L2} of a regular language L1 by any language L2 is

(1) context-free  
(2) never regular  
(3) regular only if L2 is regular  
(4) always regular  

<details><summary>Answer</summary>

**(4)** — It is a subset of the prefixes of L1 and can be accepted by the DFA of L1 with new accepting states.

</details>

**Q25.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The language {a^p : p is prime} is not regular.  
Reason R: Its complement is finite.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — A is true (by the pumping lemma), but its complement {a^n : n not prime} is infinite.

</details>

**Q26.** `Medium`  
Which of the following regular expressions denotes the strings over {0, 1} in which every 0 is immediately followed by 1?

(1) (1 + 01)*  
(2) (01)*  
(3) 1*01*  
(4) (0 + 1)*01  

<details><summary>Answer</summary>

**(1)** — Each occurrence of 0 is part of a 01 block.

</details>

**Q27.** `Medium`  
The minimum length of the strings generated by the regular expression (a + b)(a + b)(aa + bb)* is

(1) 1  
(2) 4  
(3) 0  
(4) 2  

<details><summary>Answer</summary>

**(4)** — The two leading symbols are mandatory and the starred part can be empty.

</details>

**Q28.** `Medium`  
The regular expression a(a + b)*b + b(a + b)*a describes strings over {a, b} that

(1) start and end with the same symbol  
(2) start and end with different symbols  
(3) contain ab  
(4) have even length  

<details><summary>Answer</summary>

**(2)** — Each alternative starts with one symbol and ends with the other.

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: Every finite language is regular.  
Statement II: Every regular language is finite.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — a* is regular and infinite.

</details>

**Q30.** `Low`  
Regular expressions were introduced by

(1) Stephen Kleene  
(2) John Backus  
(3) Noam Chomsky  
(4) Alan Turing  

<details><summary>Answer</summary>

**(1)** — Kleene's theorem shows they describe exactly the languages of finite automata.

</details>

**Q31.** `Medium`  
Which of the following languages over {a, b} is NOT regular?

(1) Strings ending in b  
(2) Strings of length divisible by 4  
(3) Strings with an even number of a's  
(4) Strings in which the number of a's equals the number of b's  

<details><summary>Answer</summary>

**(4)** — Equality of counts requires unbounded counting.

</details>

**Q32.** `Medium`  
If L is regular, then which of the following is also regular?  
A. The set of prefixes of strings in L  B. The set of suffixes of strings in L  C. The complement of L  D. L ∩ {a^n b^n}  
Choose the correct answer from the options given below:

(1) A and D only  
(2) A, B and C only  
(3) B, C and D only  
(4) A, B, C and D  

<details><summary>Answer</summary>

**(2)** — Intersecting with the non-regular {a^n b^n} need not give a regular language.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: The language {a^n b^n : n ≥ 0} ∪ {a^m b^n : m ≠ n} is regular.  
Statement II: The union of two non-regular languages is always non-regular.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The union in Statement I is a*b*, which is regular, so Statement II is false.

</details>
