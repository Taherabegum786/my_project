# Set 9 — Semantic Analysis (attribute grammars, syntax-directed definitions and translation, type checking)

**25 questions** — High: 9, Medium: 15, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Consider the translation scheme E → E1 # T {E.val = E1.val × T.val} | T {E.val = T.val}, T → T1 & F {T.val = T1.val + F.val} | F {T.val = F.val}, F → num {F.val = num.val}. The value computed for 2 # 3 & 5 # 6 & 4 is

(1) 200  
(2) 160  
(3) 40  
(4) 72  

<details><summary>Answer</summary>

**(2)** — & binds tighter than # (it is lower in the grammar), so the value is 2 × (3 + 5) × (6 + 4) = 160.

</details>

**Q2.** `High`  
The translation scheme E → E + T {print("+")} | T, T → num {print(num.val)} prints what for the input 2 + 3 + 4?

(1) 23+4+  
(2) 2+3+4  
(3) +2+34  
(4) 234++  

<details><summary>Answer</summary>

**(1)** — The actions print the postfix form; + is left-associative.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (Concept): A. Synthesized attribute  B. Inherited attribute  C. S-attributed definition  D. L-attributed definition  
List II (Meaning): I. Uses only synthesized attributes  II. Computed from the attributes of the node's children  III. Inherited attributes depend only on the parent and on siblings to the left  IV. Computed from the attributes of the parent and/or siblings

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(3)** — Standard attribute grammar terminology.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: Every S-attributed definition is L-attributed.  
Statement II: Every L-attributed definition is S-attributed.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — L-attributed definitions may also have inherited attributes.

</details>

**Q5.** `High`  
S-attributed definitions are naturally evaluated during

(1) bottom-up (LR) parsing, by computing attributes when reducing  
(2) code optimization  
(3) lexical analysis  
(4) top-down parsing using inherited attributes  

<details><summary>Answer</summary>

**(1)** — Attribute values can be kept on the parser stack alongside grammar symbols.

</details>

**Q6.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: L-attributed definitions can be evaluated in a single depth-first, left-to-right traversal of the parse tree.  
Reason R: Every inherited attribute depends only on information from the parent and from siblings to its left, which is already available.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This is why L-attributed definitions suit top-down (LL) translation.

</details>

**Q7.** `High`  
An attribute grammar has a dependency graph with a cycle. This means that

(1) evaluation is trivial  
(2) there is no order in which all attributes can be evaluated  
(3) the grammar is S-attributed  
(4) the grammar is ambiguous  

<details><summary>Answer</summary>

**(2)** — Attribute evaluation follows a topological sort of an acyclic dependency graph.

</details>

**Q8.** `Medium`  
In the declaration grammar D → T L, T → int | float, L → L1 , id | id, the type is passed from T to the identifiers in L using

(1) a global variable  
(2) a synthesized attribute only  
(3) the symbol table only  
(4) an inherited attribute L.inh = T.type  

<details><summary>Answer</summary>

**(4)** — L1.inh = L.inh then passes the type down the list.

</details>

**Q9.** `Medium`  
A parse tree showing the values of attributes at each node is called

(1) a syntax tree  
(2) an activation tree  
(3) a DAG  
(4) an annotated (decorated) parse tree  

<details><summary>Answer</summary>

**(4)** — Attribute values are written next to the nodes.

</details>

**Q10.** `Medium`  
Given below are two statements.  
Statement I: A syntax-directed definition specifies semantic rules without specifying when they are evaluated.  
Statement II: A syntax-directed translation scheme embeds program fragments (semantic actions) within production bodies, fixing the evaluation order.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This is the distinction between SDDs and SDTs.

</details>

**Q11.** `High`  
Match List I with List II.  
List I (Type concept): A. Coercion  B. Cast  C. Overloading  D. Parametric polymorphism  
List II (Description): I. One operator or function name with several meanings depending on the argument types  II. Explicit type conversion written by the programmer  III. Implicit type conversion inserted by the compiler  IV. A single definition that works uniformly for many types, such as a generic list

(1) A-III, B-II, C-IV, D-I  
(2) A-II, B-III, C-I, D-IV  
(3) A-III, B-I, C-II, D-IV  
(4) A-III, B-II, C-I, D-IV  

<details><summary>Answer</summary>

**(4)** — Type concepts handled during semantic analysis.

</details>

**Q12.** `High`  
Given below are two statements.  
Statement I: Static type checking is done at compile time, while dynamic type checking is done at run time.  
Statement II: A strongly typed language guarantees that a program accepted by its compiler will run without type errors.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard definitions.

</details>

**Q13.** `Medium`  
Under structural equivalence of types, two type expressions are equivalent if

(1) they have the same name  
(2) they are declared in the same scope  
(3) they are built from the same basic types by the same type constructors  
(4) they have the same size  

<details><summary>Answer</summary>

**(3)** — Under name equivalence, types are equivalent only if they have the same name.

</details>

**Q14.** `Medium`  
In C, the declarations "typedef int A; typedef int B;" are compatible with each other because C uses

(1) no type checking  
(2) dynamic typing  
(3) name equivalence for typedefs  
(4) structural (or rather typedef-transparent) equivalence, since typedef only creates an alias  

<details><summary>Answer</summary>

**(4)** — Structure types in C, by contrast, are compared by name (tag).

</details>

**Q15.** `Medium`  
Type inference in languages such as ML and Haskell is performed by

(1) lexical analysis  
(2) guessing types at run time  
(3) ignoring types  
(4) unification of type expressions (Hindley-Milner algorithm)  

<details><summary>Answer</summary>

**(4)** — The most general type of each expression is computed without declarations.

</details>

**Q16.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Checking that a variable is declared before use cannot be done by a context-free grammar alone.  
Reason R: The language {wcw : w is a string} models declaration before use, and it is not context-free.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Such checks are done during semantic analysis, using the symbol table.

</details>

**Q17.** `Medium`  
The type expression for an array of 10 pointers to integers is

(1) function(integer, pointer)  
(2) pointer(array(0..9, integer))  
(3) integer × 10  
(4) array(0..9, pointer(integer))  

<details><summary>Answer</summary>

**(4)** — Type constructors are applied from the outside in.

</details>

**Q18.** `Medium`  
For the expression x + y, where x is an int and y is a float, a C compiler

(1) reports a type error  
(2) converts x to float (widening) and performs floating-point addition  
(3) uses integer addition  
(4) converts y to int  

<details><summary>Answer</summary>

**(2)** — Implicit widening coercion follows the usual arithmetic conversions.

</details>

**Q19.** `Medium`  
In an SDT, a semantic action placed at the right end of a production is executed

(1) never  
(2) before the production is applied  
(3) when the body has been completely recognised (on reduction in a bottom-up parser)  
(4) only during lexical analysis  

<details><summary>Answer</summary>

**(3)** — Such postfix SDTs can be implemented directly during LR parsing.

</details>

**Q20.** `Medium`  
Given below are two statements.  
Statement I: Inherited attributes are useful for passing context information, such as the expected type, down the parse tree.  
Statement II: Synthesized attributes of terminals are supplied by the lexical analyzer.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — For example num.val comes from the token's attribute value.

</details>

**Q21.** `Medium`  
For the SDD with productions S → AB {A.i = 1; B.i = A.s; S.s = B.s}, A → a {A.s = A.i + 1}, B → b {B.s = B.i × 2}, the value of S.s for the input ab is

(1) 3  
(2) 6  
(3) 2  
(4) 4  

<details><summary>Answer</summary>

**(4)** — A.s = 1 + 1 = 2; B.i = 2; B.s = 4; S.s = 4.

</details>

**Q22.** `Medium`  
Which kind of SDD can always be evaluated in any bottom-up parser during parsing?

(1) L-attributed definitions  
(2) Definitions with cyclic dependencies  
(3) S-attributed definitions  
(4) Any SDD  

<details><summary>Answer</summary>

**(3)** — They need only synthesized attributes, computed at reduction time.

</details>

**Q23.** `Low`  
The semantic analyzer uses which data structure to check that identifiers are declared and used with the correct types?

(1) Flow graph  
(2) Activation tree  
(3) Symbol table  
(4) Parse table  

<details><summary>Answer</summary>

**(3)** — Each identifier's entry records its type, scope and other attributes.

</details>

**Q24.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Every L-attributed definition can be evaluated during LR parsing without any modification.  
Reason R: LR parsers know the production being used before they reach its right end.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — An LR parser does not know the production until it reduces; marker non-terminals are needed to handle inherited attributes, so A is false.

</details>

**Q25.** `Medium`  
A dependency graph for attribute evaluation has an edge from attribute b to attribute c when

(1) c is computed using b  
(2) c is inherited  
(3) b and c belong to the same node  
(4) b and c are both synthesized  

<details><summary>Answer</summary>

**(1)** — A topological sort of the graph gives a valid evaluation order.

</details>
