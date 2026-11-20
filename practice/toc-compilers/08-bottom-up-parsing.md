# Set 8 — Syntax Analysis: Bottom-Up Parsing (shift-reduce, operator precedence, LR(0), SLR, CLR, LALR)

**30 questions** — High: 12, Medium: 17, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The number of states in the canonical collection of LR(0) items for the augmented expression grammar E' → E, E → E + T | T, T → T * F | F, F → (E) | id is

(1) 9  
(2) 10  
(3) 12  
(4) 14  

<details><summary>Answer</summary>

**(3)** — States I0 to I11, as in the Dragon Book.

</details>

**Q2.** `High`  
For the grammar S → CC, C → cC | d, the numbers of states in the LR(0) (SLR), canonical LR(1) and LALR(1) automata are respectively

(1) 10, 10 and 7  
(2) 7, 7 and 10  
(3) 7, 10 and 7  
(4) 7, 10 and 10  

<details><summary>Answer</summary>

**(3)** — LALR merges LR(1) states with the same core: 10 states become 7.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (Parser): A. LR(0)  B. SLR(1)  C. LALR(1)  D. Canonical LR(1)  
List II (Lookahead used for reductions): I. LR(1) items, with states having identical cores merged  II. No lookahead: reduce whenever a complete item is present  III. FOLLOW set of the left-hand non-terminal  IV. Exact lookahead symbols carried in LR(1) items

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-III, C-I, D-IV  
(3) A-II, B-I, C-III, D-IV  
(4) A-III, B-II, C-I, D-IV  

<details><summary>Answer</summary>

**(2)** — Power increases from LR(0) to SLR, LALR and canonical LR.

</details>

**Q4.** `High`  
Arrange the following parsers in increasing order of the class of grammars they can handle.  
A. LALR(1)  B. LR(0)  C. Canonical LR(1)  D. SLR(1)

(1) B, D, C, A  
(2) B, D, A, C  
(3) B, A, D, C  
(4) D, B, A, C  

<details><summary>Answer</summary>

**(2)** — LR(0) ⊂ SLR(1) ⊂ LALR(1) ⊂ LR(1).

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: The grammar S → L = R | R, L → *R | id, R → L is not SLR(1).  
Statement II: The grammar S → L = R | R, L → *R | id, R → L is LALR(1).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — In SLR, = is in FOLLOW(R), causing a shift-reduce conflict between shifting = and reducing R → L; LALR lookaheads avoid it.

</details>

**Q6.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Merging LR(1) states with the same core to form LALR(1) states can introduce reduce-reduce conflicts but never shift-reduce conflicts.  
Reason R: The shift actions of a state depend only on its core, so a shift-reduce conflict after merging would already exist in one of the original LR(1) states.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The grammar S → aAd | bBd | aBe | bAe, A → c, B → c is LR(1) but not LALR(1) because of reduce-reduce conflicts.

</details>

**Q7.** `High`  
The grammar S → Aa | bAc | dc | bda, A → d is

(1) neither SLR(1) nor LALR(1)  
(2) SLR(1) and LALR(1)  
(3) LALR(1) but not SLR(1)  
(4) SLR(1) but not LALR(1)  

<details><summary>Answer</summary>

**(3)** — FOLLOW(A) = {a, c}, so SLR has a conflict on a after d, while LALR lookaheads distinguish the cases.

</details>

**Q8.** `High`  
The grammar S → aAd | bBd | aBe | bAe, A → c, B → c is

(1) LR(1) but not LALR(1)  
(2) SLR(1)  
(3) not LR(1)  
(4) LALR(1)  

<details><summary>Answer</summary>

**(1)** — The LR(1) states for A → c· and B → c· have the same core and merge into a state with reduce-reduce conflicts.

</details>

**Q9.** `High`  
In shift-reduce parsing, a handle is

(1) the first symbol on the stack  
(2) a substring that matches the right side of a production and whose reduction is one step of a rightmost derivation in reverse  
(3) any substring of the right sentential form  
(4) the lookahead symbol  

<details><summary>Answer</summary>

**(2)** — Reducing a handle moves the parse one step back towards the start symbol.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Conflict or term): A. Shift-reduce conflict  B. Reduce-reduce conflict  C. Viable prefix  D. Handle pruning  
List II (Meaning): I. A prefix of a right sentential form that can appear on the stack of a shift-reduce parser  II. The parser cannot decide whether to shift or to reduce  III. The parser cannot decide which of two productions to reduce by  IV. Repeatedly reducing handles to obtain the rightmost derivation in reverse

(1) A-II, B-I, C-III, D-IV  
(2) A-II, B-III, C-IV, D-I  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(4)** — Basic shift-reduce terminology.

</details>

**Q11.** `High`  
The four actions of an LR parser are

(1) shift, goto, follow and first  
(2) scan, parse, check and emit  
(3) push, pop, read and write  
(4) shift, reduce, accept and error  

<details><summary>Answer</summary>

**(4)** — The GOTO table is used after a reduction to find the next state.

</details>

**Q12.** `High`  
Given below are two statements.  
Statement I: An ambiguous grammar can never be LR(k) for any k.  
Statement II: Yacc can use an ambiguous grammar if precedence and associativity declarations resolve the conflicts.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Yacc's default is to prefer shift in a shift-reduce conflict and the earlier production in a reduce-reduce conflict.

</details>

**Q13.** `Medium`  
In an LR(0) automaton, a state containing both A → α· and B → β·aγ has a

(1) no conflict  
(2) goto conflict  
(3) shift-reduce conflict  
(4) reduce-reduce conflict  

<details><summary>Answer</summary>

**(3)** — The parser could reduce by A → α or shift a.

</details>

**Q14.** `Medium`  
For the expression grammar E → E + T | T, T → T * F | F, F → (E) | id, which statement is correct?

(1) It is LR(0)  
(2) It is LL(1)  
(3) It is SLR(1) but not LR(0)  
(4) It is ambiguous  

<details><summary>Answer</summary>

**(3)** — Some LR(0) states contain both a complete item and a shift item (e.g. E → T· and T → T·*F), but FOLLOW sets resolve them.

</details>

**Q15.** `Medium`  
An operator grammar is one in which

(1) the grammar is in CNF  
(2) all productions are left-recursive  
(3) no production has ε on its right side and no right side has two adjacent non-terminals  
(4) every production has an operator  

<details><summary>Answer</summary>

**(3)** — Operator-precedence parsing works on such grammars.

</details>

**Q16.** `Medium`  
In operator-precedence parsing, the relation a <· b between two terminals means

(1) a and b have equal precedence  
(2) a has higher precedence than b  
(3) a yields precedence to b (b's handle starts after a)  
(4) a and b cannot be adjacent  

<details><summary>Answer</summary>

**(3)** — a ·> b means a takes precedence; a ≐ b means they are in the same handle.

</details>

**Q17.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Canonical LR(1) parsers have many more states than LALR(1) parsers for typical programming languages.  
Reason R: LALR(1) parsers have the same number of states as SLR(1) parsers.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but R does not explain A; the LR(1) blow-up comes from splitting states by lookahead.

</details>

**Q18.** `Medium`  
Which parser generator tool produces LALR(1) parsers?

(1) Lex  
(2) Yacc (and Bison)  
(3) ANTLR (LL(*))  
(4) Flex  

<details><summary>Answer</summary>

**(2)** — Yacc stands for "Yet Another Compiler-Compiler".

</details>

**Q19.** `Medium`  
An LR(0) item is

(1) a production with a dot at some position on its right side  
(2) a terminal  
(3) a parse tree  
(4) a token  

<details><summary>Answer</summary>

**(1)** — For example A → X·YZ means X has been seen and YZ is expected.

</details>

**Q20.** `Medium`  
An LR(1) item has the form

(1) [A → α·β]  
(2) [α, β, a, b]  
(3) [A → α·β, a], where a is a lookahead terminal  
(4) [A, a]  

<details><summary>Answer</summary>

**(3)** — The lookahead is used only when the dot is at the right end.

</details>

**Q21.** `Medium`  
Given below are two statements.  
Statement I: Every SLR(1) grammar is LALR(1).  
Statement II: Every LALR(1) grammar is SLR(1).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — S → L = R | R, L → *R | id, R → L is LALR(1) but not SLR(1).

</details>

**Q22.** `Medium`  
A bottom-up parser builds the parse tree

(1) it does not build a tree  
(2) in level order  
(3) from the leaves to the root  
(4) from the root to the leaves  

<details><summary>Answer</summary>

**(3)** — It reduces the input to the start symbol.

</details>

**Q23.** `Medium`  
For the grammar S → aSb | ab and input aabb, the sequence of actions of a shift-reduce parser is

(1) shift, reduce, shift, reduce, accept  
(2) reduce, shift, shift, shift, accept  
(3) shift, shift, shift, reduce S → ab, shift, reduce S → aSb, accept  
(4) shift, shift, reduce, reduce, accept  

<details><summary>Answer</summary>

**(3)** — After shifting a, a, b the handle ab is on top; reduce it, shift b and reduce aSb.

</details>

**Q24.** `Medium`  
The LR parsing method is preferred in practice because

(1) it needs no tables  
(2) it is easy to write by hand  
(3) it can handle virtually all programming-language constructs that have CFGs, detects errors as early as possible, and is more general than LL  
(4) it works only for regular languages  

<details><summary>Answer</summary>

**(3)** — LR parsers are usually generated by tools.

</details>

**Q25.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The LALR(1) parser for a grammar has the same number of states as its SLR(1) parser.  
Reason R: Yacc generates LALR(1) parsers.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but A holds because both parsers are built from the LR(0) automaton.

</details>

**Q26.** `Medium`  
For the grammar S → CC, C → cC | d, the LALR(1) parser is

(1) not constructible  
(2) larger than the canonical LR(1) parser  
(3) identical in size to the canonical LR(1) parser  
(4) smaller than the canonical LR(1) parser and has no conflicts  

<details><summary>Answer</summary>

**(4)** — 7 states instead of 10, with no conflicts.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: An LR(0) parser can parse any unambiguous grammar.  
Statement II: An LR(0) grammar cannot have an ε-production whose reduction conflicts with a shift.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Many unambiguous grammars, such as the standard expression grammar, are not LR(0).

</details>

**Q28.** `Low`  
In LR(k), the letter R indicates that the parser constructs

(1) a reduced grammar  
(2) a regular expression  
(3) a recursive derivation  
(4) a rightmost derivation in reverse  

<details><summary>Answer</summary>

**(4)** — L stands for left-to-right scanning of the input.

</details>

**Q29.** `Medium`  
In an SLR parser, the action reduce by A → α is placed in state I for terminal a when A → α· is in I and

(1) a is in FOLLOW(A)  
(2) a is the next token in the input always  
(3) a is in FIRST(A)  
(4) a is in FIRST(α)  

<details><summary>Answer</summary>

**(1)** — This use of FOLLOW sets is what can cause spurious conflicts.

</details>

**Q30.** `Medium`  
The dangling-else conflict in an LR parser is a

(1) lexical conflict  
(2) shift-reduce conflict, usually resolved by shifting  
(3) reduce-reduce conflict  
(4) goto conflict  

<details><summary>Answer</summary>

**(2)** — Shifting associates else with the nearest unmatched if.

</details>
