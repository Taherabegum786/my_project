# Set 6 — Phases of a Compiler and Lexical Analysis

**28 questions** — High: 8, Medium: 19, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Arrange the phases of a compiler in the order in which they process the source program.  
A. Intermediate code generation  B. Syntax analysis  C. Code optimization  D. Lexical analysis  E. Semantic analysis

(1) D, E, B, A, C  
(2) D, B, A, E, C  
(3) B, D, E, A, C  
(4) D, B, E, A, C  

<details><summary>Answer</summary>

**(4)** — Lexical, syntax and semantic analysis, then intermediate code generation, optimization and target code generation.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Compiler phase): A. Lexical analysis  B. Syntax analysis  C. Semantic analysis  D. Code generation  
List II (Main activity): I. Type checking and building attribute information  II. Grouping characters into tokens  III. Mapping intermediate code to target machine instructions and allocating registers  IV. Building a parse tree from tokens according to the grammar

(1) A-II, B-I, C-IV, D-III  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(2)** — The analysis phases form the front end and the synthesis phases the back end.

</details>

**Q3.** `High`  
The number of tokens in the C statement printf("i = %d, &i = %x", i, &i); is

(1) 9  
(2) 13  
(3) 8  
(4) 10  

<details><summary>Answer</summary>

**(4)** — printf ( "i = %d, &i = %x" , i , & i ) ; — the string literal is a single token.

</details>

**Q4.** `High`  
The number of tokens in the C declaration int a[10], \*p = &a[0]; is

(1) 14  
(2) 13  
(3) 16  
(4) 15  

<details><summary>Answer</summary>

**(4)** — int a [ 10 ] , \* p = & a [ 0 ] ; — 15 tokens.

</details>

**Q5.** `Medium`  
The number of tokens in the C statement x = y++ + ++z; is

(1) 8  
(2) 7  
(3) 6  
(4) 9  

<details><summary>Answer</summary>

**(1)** — x = y ++ + ++ z ; — the lexer uses the longest-match rule for ++.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: A lexeme is a sequence of characters in the source program that matches the pattern for a token.  
Statement II: A token is a pair consisting of a token name and an optional attribute value.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — For example the lexeme "count" gives the token (id, pointer to the symbol-table entry).

</details>

**Q7.** `High`  
Which of the following is usually detected by the lexical analyzer?

(1) An undeclared variable  
(2) Type mismatch in an expression  
(3) A missing semicolon  
(4) An illegal character such as @ in a C program outside a string  

<details><summary>Answer</summary>

**(4)** — Missing semicolons are syntax errors; type mismatches and undeclared names are semantic errors.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Error): A. The character @ appearing outside a string in a C program  B. Unbalanced parentheses  C. Adding an integer to an array  D. Division by a zero value read from the input  
List II (Where it is detected): I. Semantic analysis  II. Syntax analysis  III. Lexical analysis  IV. Only at run time

(1) A-III, B-I, C-II, D-IV  
(2) A-III, B-II, C-IV, D-I  
(3) A-II, B-III, C-I, D-IV  
(4) A-III, B-II, C-I, D-IV  

<details><summary>Answer</summary>

**(4)** — A value that is known only at run time cannot be checked by any compiler phase.

</details>

**Q9.** `Medium`  
The symbol table is accessed by

(1) only the parser  
(2) most phases of the compiler  
(3) only the code generator  
(4) only the lexical analyzer  

<details><summary>Answer</summary>

**(2)** — Entries are created during analysis and used during semantic checking and code generation.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The front end of a compiler is largely independent of the target machine.  
Reason R: The front end analyses the source program and produces an intermediate representation, leaving machine-specific work to the back end.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This separation allows m front ends and n back ends to give m × n compilers.

</details>

**Q11.** `Medium`  
Lex (or Flex) generates

(1) a parser from a context-free grammar  
(2) an optimizer  
(3) an assembler  
(4) a lexical analyzer from regular-expression patterns  

<details><summary>Answer</summary>

**(4)** — Yacc (or Bison) generates LALR(1) parsers.

</details>

**Q12.** `Medium`  
A Lex specification consists of three sections separated by %%. They are

(1) tokens, grammar and actions  
(2) header, body and footer  
(3) declarations, translation rules, and auxiliary functions  
(4) states, transitions and outputs  

<details><summary>Answer</summary>

**(3)** — Translation rules have the form "pattern { action }".

</details>

**Q13.** `Medium`  
When two Lex patterns match the input, Lex chooses

(1) the longest match, and among equal-length matches the pattern listed first  
(2) the shorter match  
(3) the pattern listed last  
(4) a random pattern  

<details><summary>Answer</summary>

**(1)** — So "if" is a keyword only if the keyword pattern is listed before the identifier pattern.

</details>

**Q14.** `Medium`  
Input buffering with sentinels in a lexical analyzer is used to

(1) detect syntax errors  
(2) store tokens  
(3) reduce memory  
(4) reduce the number of tests for the end of the buffer for each character read  

<details><summary>Answer</summary>

**(4)** — A special sentinel character marks the end of each buffer half.

</details>

**Q15.** `Medium`  
Given below are two statements.  
Statement I: A single-pass compiler performs all phases in one scan of the source program.  
Statement II: A multi-pass compiler always produces faster target code than a single-pass compiler.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Extra passes allow more optimization but do not guarantee faster code.

</details>

**Q16.** `Medium`  
The task of recognising keywords such as "if" and "while" is usually done by

(1) the parser only  
(2) the optimizer  
(3) treating them as reserved words, entered in the symbol table or matched by separate patterns  
(4) the code generator  

<details><summary>Answer</summary>

**(3)** — Reserved words cannot be used as identifiers.

</details>

**Q17.** `Medium`  
Panic-mode error recovery in a lexical analyzer

(1) deletes successive characters until a well-formed token is found  
(2) rewrites the source file  
(3) asks the user  
(4) stops compilation immediately  

<details><summary>Answer</summary>

**(1)** — Other options include inserting, deleting, replacing or transposing characters.

</details>

**Q18.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Lexical analysis is separated from syntax analysis.  
Reason R: Recognising tokens requires the full power of context-free grammars.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Tokens are described by regular expressions, which allows simple and fast DFA-based scanners.

</details>

**Q19.** `Medium`  
Which of the following is NOT a token class in a typical programming language?

(1) Keyword  
(2) Identifier  
(3) Operator  
(4) Comment  

<details><summary>Answer</summary>

**(4)** — Comments and white space are stripped by the lexer and not passed to the parser.

</details>

**Q20.** `Medium`  
Match List I with List II.  
List I (Tool or concept): A. Yacc  B. Lex  C. Preprocessor  D. Assembler  
List II (Function): I. Converts assembly language into relocatable machine code  II. Generates an LALR parser  III. Generates a lexical analyzer  IV. Handles macros and file inclusion before compilation

(1) A-III, B-II, C-IV, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(2)** — Language-processing tools.

</details>

**Q21.** `Medium`  
In the Lex pattern [a-zA-Z\_][a-zA-Z0-9\_]\*, the strings matched are

(1) identifiers that start with a letter or underscore  
(2) floating-point numbers  
(3) integers  
(4) keywords only  

<details><summary>Answer</summary>

**(1)** — The first character cannot be a digit.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: Code optimization is an optional phase of a compiler.  
Statement II: Intermediate code makes it easier to retarget a compiler to a new machine.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Only analysis and code generation are essential.

</details>

**Q23.** `Low`  
The output of the lexical analyzer is

(1) machine code  
(2) a stream of tokens  
(3) a parse tree  
(4) three-address code  

<details><summary>Answer</summary>

**(2)** — The parser requests tokens one at a time, typically through a getNextToken function.

</details>

**Q24.** `Medium`  
Which phase of the compiler is responsible for checking that a variable is declared before it is used?

(1) Code generation  
(2) Lexical analysis  
(3) Semantic analysis  
(4) Syntax analysis  

<details><summary>Answer</summary>

**(3)** — Declaration-before-use is a context-sensitive property not captured by a CFG.

</details>

**Q25.** `Medium`  
A compiler written in language L that runs on machine M and generates code for machine N is described as

(1) an interpreter  
(2) a cross compiler  
(3) a native compiler  
(4) a decompiler  

<details><summary>Answer</summary>

**(2)** — A native compiler generates code for the machine it runs on.

</details>

**Q26.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Lexical analyzers are usually implemented as DFAs.  
Reason R: Token patterns cannot be described by regular expressions.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Token patterns are regular expressions, which is exactly why they can be compiled to DFAs.

</details>

**Q27.** `Medium`  
The phases of a compiler that depend mainly on the source language and not on the target machine form the

(1) loader  
(2) front end  
(3) back end  
(4) middle end only  

<details><summary>Answer</summary>

**(2)** — Lexical, syntax and semantic analysis and intermediate code generation.

</details>

**Q28.** `Medium`  
The number of tokens in the statement if (a &gt;= b) max = a; else max = b; is

(1) 16  
(2) 14  
(3) 15  
(4) 17  

<details><summary>Answer</summary>

**(3)** — if ( a &gt;= b ) max = a ; else max = b ; — 15 tokens.

</details>
