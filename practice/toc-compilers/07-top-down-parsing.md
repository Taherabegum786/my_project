# Set 7 — Syntax Analysis: Top-Down Parsing (FIRST, FOLLOW, recursive descent, LL(1))

**28 questions** — High: 12, Medium: 15, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
For the grammar E → TE', E' → +TE' | ε, T → FT', T' → *FT' | ε, F → (E) | id, the set FIRST(E') is

(1) {(, id}  
(2) {+, ε}  
(3) {+, ), $}  
(4) {+}  

<details><summary>Answer</summary>

**(2)** — E' can start with + or derive ε.

</details>

**Q2.** `High`  
For the grammar E → TE', E' → +TE' | ε, T → FT', T' → *FT' | ε, F → (E) | id, the set FOLLOW(T) is

(1) {+, ), $}  
(2) {), $}  
(3) {+, *}  
(4) {*, +, ), $}  

<details><summary>Answer</summary>

**(1)** — FOLLOW(T) contains FIRST(E') − {ε} = {+} and, because E' can vanish, FOLLOW(E') = {), $}.

</details>

**Q3.** `High`  
For the grammar E → TE', E' → +TE' | ε, T → FT', T' → *FT' | ε, F → (E) | id, the set FOLLOW(F) is

(1) {(, id}  
(2) {*, $}  
(3) {*, +, ), $}  
(4) {+, ), $}  

<details><summary>Answer</summary>

**(3)** — FOLLOW(F) includes FIRST(T') − {ε} = {*} and FOLLOW(T) = {+, ), $}.

</details>

**Q4.** `High`  
For the grammar E → TE', E' → +TE' | ε, T → FT', T' → *FT' | ε, F → (E) | id, the set FOLLOW(E) is

(1) {(, id}  
(2) {+, ), $}  
(3) {$}  
(4) {), $}  

<details><summary>Answer</summary>

**(4)** — $ because E is the start symbol, and ) from F → (E).

</details>

**Q5.** `High`  
In the LL(1) parsing table for E → TE', E' → +TE' | ε, T → FT', T' → *FT' | ε, F → (E) | id, the production E' → ε is placed in the entries

(1) M[E', id]  
(2) M[E', +]  
(3) M[E', )] and M[E', $]  
(4) M[E', *]  

<details><summary>Answer</summary>

**(3)** — An ε-production is placed under every terminal in FOLLOW(E') = {), $}.

</details>

**Q6.** `High`  
A grammar is LL(1) if, for every pair of productions A → α | β,

(1) FIRST(α) and FIRST(β) are disjoint, and if β ⇒* ε then FIRST(α) and FOLLOW(A) are disjoint  
(2) α and β have the same length  
(3) A is the start symbol  
(4) the grammar is ambiguous  

<details><summary>Answer</summary>

**(1)** — Then each table entry holds at most one production.

</details>

**Q7.** `High`  
Given below are two statements.  
Statement I: A left-recursive grammar cannot be LL(1).  
Statement II: An ambiguous grammar cannot be LL(1).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Left recursion makes FIRST sets of the alternatives overlap, and ambiguity gives two entries in some cell.

</details>

**Q8.** `High`  
The grammar S → iEtSS' | a, S' → eS | ε, E → b (dangling else) is not LL(1) because

(1) FIRST(S) is empty  
(2) it has no ε-productions  
(3) the entry M[S', e] contains both S' → eS and S' → ε, since e is in FOLLOW(S')  
(4) it is left-recursive  

<details><summary>Answer</summary>

**(3)** — The grammar is ambiguous; in practice the conflict is resolved by choosing S' → eS.

</details>

**Q9.** `Medium`  
The grammar S → AaAb | BbBa, A → ε, B → ε is

(1) neither LL(1) nor LR(1)  
(2) LL(1) but not SLR(1)  
(3) SLR(1) but not LL(1)  
(4) both LL(1) and SLR(1)  

<details><summary>Answer</summary>

**(2)** — FIRST(AaAb) = {a} and FIRST(BbBa) = {b} are disjoint, but in SLR the reductions A → ε and B → ε both have lookahead set {a, b}.

</details>

**Q10.** `High`  
Which of the following grammars is LL(1)?

(1) S → A | B, A → a, B → a  
(2) S → aB | bA, A → a, B → b  
(3) S → Sa | b  
(4) S → aS | a  

<details><summary>Answer</summary>

**(2)** — The other grammars are left-recursive, need left factoring, or are ambiguous.

</details>

**Q11.** `Medium`  
The grammar S → aS | a is not LL(1). The transformation needed is

(1) conversion to CNF  
(2) adding an end marker  
(3) removal of left recursion  
(4) left factoring: S → aS', S' → S | ε  

<details><summary>Answer</summary>

**(4)** — Both alternatives begin with a.

</details>

**Q12.** `High`  
A recursive-descent parser

(1) uses an LR table  
(2) cannot handle ε-productions  
(3) is a bottom-up parser  
(4) is a top-down parser with one procedure for each non-terminal  

<details><summary>Answer</summary>

**(4)** — Without backtracking it is a predictive parser for LL(1) grammars.

</details>

**Q13.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A recursive-descent parser can loop forever on a left-recursive grammar.  
Reason R: For A → Aα, the procedure for A calls itself before consuming any input.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Left recursion must be eliminated before top-down parsing.

</details>

**Q14.** `High`  
A top-down parser produces

(1) a rightmost derivation  
(2) a leftmost derivation  
(3) no derivation  
(4) a rightmost derivation in reverse  

<details><summary>Answer</summary>

**(2)** — A bottom-up (LR) parser produces a rightmost derivation in reverse.

</details>

**Q15.** `Medium`  
In the table-driven predictive (LL(1)) parser, if the top of the stack is a non-terminal A and the current input symbol is a, the parser

(1) reduces by A  
(2) reports success  
(3) shifts a  
(4) replaces A by the right side of the production in M[A, a], pushed in reverse  

<details><summary>Answer</summary>

**(4)** — If M[A, a] is empty, it reports a syntax error.

</details>

**Q16.** `Medium`  
In LL(1), the first L, the second L and the 1 stand for

(1) left-to-right scan, LR items, one table  
(2) left-to-right scan, leftmost derivation, one symbol of lookahead  
(3) leftmost scan, last derivation, one state  
(4) left-recursive, left-factored, one production  

<details><summary>Answer</summary>

**(2)** — LR(k) means left-to-right scan, rightmost derivation in reverse, k symbols of lookahead.

</details>

**Q17.** `Medium`  
For the grammar S → ABC, A → a | ε, B → b | ε, C → c, the set FIRST(S) is

(1) {a, b, c}  
(2) {a}  
(3) {a, b}  
(4) {a, b, c, ε}  

<details><summary>Answer</summary>

**(1)** — A and B can both vanish, so c can also begin S; C cannot vanish, so ε is not included.

</details>

**Q18.** `Medium`  
For the grammar S → aSb | ε, the set FOLLOW(S) is

(1) {b}  
(2) {a, b, $}  
(3) {$}  
(4) {b, $}  

<details><summary>Answer</summary>

**(4)** — $ because S is the start symbol, and b from S → aSb.

</details>

**Q19.** `Medium`  
For the grammar S → AB, A → a | ε, B → b | ε, the set FOLLOW(A) is

(1) {b, $}  
(2) {$}  
(3) {a, b, $}  
(4) {b}  

<details><summary>Answer</summary>

**(1)** — FIRST(B) = {b, ε}; since B can vanish, FOLLOW(S) = {$} is added.

</details>

**Q20.** `Medium`  
Given below are two statements.  
Statement I: Every unambiguous grammar is LL(1).  
Statement II: Every LL(1) grammar is unambiguous.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — For example, unambiguous left-recursive grammars are not LL(1).

</details>

**Q21.** `Medium`  
Panic-mode error recovery in an LL(1) parser uses

(1) backtracking  
(2) the synchronizing set of tokens, such as FOLLOW(A), to skip input until a token that can follow A is found  
(3) the LR automaton  
(4) reduction by the handle  

<details><summary>Answer</summary>

**(2)** — The non-terminal is popped and parsing resumes.

</details>

**Q22.** `Medium`  
A grammar G has productions S → aSb | ab. Which transformation makes it LL(1)?

(1) Removing left recursion  
(2) Left factoring: S → aS', S' → Sb | b  
(3) Converting to CNF  
(4) Adding ε-productions  

<details><summary>Answer</summary>

**(2)** — Both alternatives start with a.

</details>

**Q23.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: LL(1) parsers are more powerful than LR(1) parsers.  
Reason R: Every LL(1) grammar is also LR(1).

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — R is true, and it shows that LR(1) is the more powerful class, so A is false.

</details>

**Q24.** `Medium`  
The number of columns in an LL(1) parsing table for a grammar with 5 terminals is

(1) 7  
(2) 10  
(3) 6  
(4) 5  

<details><summary>Answer</summary>

**(3)** — One column per terminal, plus one for the end marker $.

</details>

**Q25.** `Low`  
Top-down parsing begins with

(1) a reduction  
(2) the start symbol of the grammar  
(3) the last token  
(4) the input string  

<details><summary>Answer</summary>

**(2)** — It expands non-terminals until the input string is produced.

</details>

**Q26.** `Medium`  
Which of the following can cause backtracking in a top-down parser that is not predictive?

(1) Unique FIRST sets  
(2) Productions of a non-terminal whose alternatives begin with the same terminal  
(3) An LL(1) grammar  
(4) An unambiguous grammar  

<details><summary>Answer</summary>

**(2)** — The parser may have to try the alternatives one by one.

</details>

**Q27.** `Medium`  
After eliminating left recursion from E → E + T | T, the result is

(1) E → T + E | T  
(2) E → E'T, E' → E + | ε  
(3) E → +TE | T  
(4) E → TE', E' → +TE' | ε  

<details><summary>Answer</summary>

**(4)** — A → Aα | β becomes A → βA', A' → αA' | ε.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: Indirect left recursion, such as S → Aa, A → Sb | c, cannot be removed.  
Statement II: FIRST(α) contains ε exactly when α can derive the empty string.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Indirect left recursion is removed by substituting productions in a fixed order of non-terminals.

</details>
