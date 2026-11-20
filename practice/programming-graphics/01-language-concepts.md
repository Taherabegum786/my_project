# Set 1 — Language Design and Translation Issues, Paradigms, Binding and Elementary Data Types

**30 questions** — High: 8, Medium: 20, Low: 2

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Programming paradigm): A. Imperative  B. Functional  C. Logic  D. Object-oriented  
List II (Example language): I. Prolog  II. Haskell  III. C  IV. Smalltalk

(1) A-III, B-II, C-I, D-IV  
(2) A-II, B-III, C-I, D-IV  
(3) A-III, B-II, C-IV, D-I  
(4) A-III, B-I, C-II, D-IV  

<details><summary>Answer</summary>

**(1)** — Imperative languages change state with assignments; functional languages evaluate expressions; logic languages use rules and queries.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Binding time): A. Language design time  B. Language implementation time  C. Compile time  D. Run time  
List II (Example of what is bound): I. The value of a variable  II. The meaning of the symbol \* as multiplication  III. The type of a variable declared int x in C  IV. The range of values of type int (for example 16 or 32 bits)

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-III, C-IV, D-I  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(4)** — Early binding gives efficiency; late binding gives flexibility.

</details>

**Q3.** `High`  
Given below are two statements.  
Statement I: In static typing, type checking is done at compile time.  
Statement II: In dynamic typing, the type of a variable is bound when a value is assigned at run time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — C, C++ and Java are statically typed; Python and JavaScript are dynamically typed.

</details>

**Q4.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Early (static) binding generally leads to more efficient programs than late (dynamic) binding.  
Reason R: With early binding, decisions are made once at compile time instead of repeatedly during execution.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Late binding, as in dynamic dispatch, gives flexibility at a run-time cost.

</details>

**Q5.** `High`  
Arrange the stages of translating a high-level program into an executing program in order.  
A. Loading  B. Compilation  C. Linking  D. Execution

(1) C, B, A, D  
(2) B, A, C, D  
(3) A, B, C, D  
(4) B, C, A, D  

<details><summary>Answer</summary>

**(4)** — The compiler produces object code, the linker combines modules and libraries, and the loader places the program in memory.

</details>

**Q6.** `High`  
Which of the following are properties of an imperative language?  
A. Variables representing memory cells  B. Assignment statements  C. Iteration  D. Referential transparency as the central principle  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) A, B, C and D  
(3) B, C and D only  
(4) A and D only  

<details><summary>Answer</summary>

**(1)** — Referential transparency is the hallmark of pure functional languages.

</details>

**Q7.** `Medium`  
A virtual computer, in the sense of Pratt and Zelkowitz, is

(1) a physical machine  
(2) the computer as seen by the programmer, defined by the programming language and implemented by hardware, firmware and software  
(3) a virus  
(4) a network computer  

<details><summary>Answer</summary>

**(2)** — For example, the "C virtual computer" executes C programs.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Concept): A. Lifetime  B. Scope  C. l-value  D. r-value  
List II (Meaning): I. The region of program text in which a name is visible  II. The period of execution during which storage is bound to a variable  III. The value stored in a variable  IV. The address (location) of a variable

(1) A-I, B-II, C-IV, D-III  
(2) A-II, B-I, C-III, D-IV  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(4)** — In x = x + 1, the left x denotes an l-value and the right x an r-value.

</details>

**Q9.** `High`  
Given below are two statements.  
Statement I: A strongly typed language detects all type errors.  
Statement II: C is a strongly typed language because it allows implicit conversions and unions without checks.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — C permits unchecked unions, casts and pointer arithmetic, so it is usually considered weakly typed.

</details>

**Q10.** `Medium`  
Scalar (elementary) data types include

(1) integers, reals, characters, Booleans, enumerations and pointers  
(2) lists and sets  
(3) classes and files  
(4) arrays and records  

<details><summary>Answer</summary>

**(1)** — Composite data types include arrays, records (structures), unions, strings, sets and files.

</details>

**Q11.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: An interpreter is useful during program development.  
Reason R: Interpreted programs run faster than compiled programs.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Interpreters are useful because they report errors immediately and allow statement-by-statement execution; compiled programs usually run faster.

</details>

**Q12.** `Medium`  
A language feature that allows a name to be bound to different types or objects at different times is related to

(1) constant folding  
(2) dynamic binding  
(3) static binding  
(4) macro expansion  

<details><summary>Answer</summary>

**(2)** — Dynamic binding of methods to calls is the basis of run-time polymorphism.

</details>

**Q13.** `Medium`  
Formal methods for describing programming language syntax include

(1) flowcharts only  
(2) BNF and EBNF grammars and syntax diagrams  
(3) UML only  
(4) ER diagrams  

<details><summary>Answer</summary>

**(2)** — EBNF adds notation for optional and repeated items.

</details>

**Q14.** `Medium`  
Formal models of semantics include

(1) lexical analysis  
(2) only syntax diagrams  
(3) regular expressions only  
(4) operational, denotational and axiomatic semantics  

<details><summary>Answer</summary>

**(4)** — Axiomatic semantics uses pre- and post-conditions (Hoare triples).

</details>

**Q15.** `Medium`  
Given below are two statements.  
Statement I: In C, the type of an expression can be changed with a cast.  
Statement II: Implicit type conversion (coercion) in C never loses information.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Conversions such as double to int or long to char can lose information.

</details>

**Q16.** `Medium`  
Which of the following is a declarative language?

(1) C  
(2) SQL  
(3) Assembly  
(4) Pascal  

<details><summary>Answer</summary>

**(2)** — Declarative languages specify what is wanted, not how to compute it.

</details>

**Q17.** `Medium`  
A programming environment includes

(1) only the hardware  
(2) only the compiler  
(3) only the operating system  
(4) tools such as editors, compilers, debuggers, profilers, version control and build tools that support program development  

<details><summary>Answer</summary>

**(4)** — Integrated development environments (IDEs) combine these tools.

</details>

**Q18.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Java programs are portable across platforms.  
Reason R: Java provides automatic garbage collection.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but portability comes from compiling to bytecode that runs on any JVM.

</details>

**Q19.** `Medium`  
Aliasing occurs when

(1) a program uses recursion  
(2) a variable has no name  
(3) two or more names refer to the same memory location  
(4) a name refers to two locations  

<details><summary>Answer</summary>

**(3)** — Pointers and reference parameters can create aliases, which make programs harder to reason about.

</details>

**Q20.** `Medium`  
Garbage collection is used to

(1) reclaim heap storage that is no longer reachable  
(2) delete files  
(3) clear the stack  
(4) remove dead code  

<details><summary>Answer</summary>

**(1)** — Java, Python and many other languages provide automatic garbage collection.

</details>

**Q21.** `Medium`  
Which of the following is a composite (structured) data type?

(1) Character  
(2) Boolean  
(3) Integer  
(4) Record (structure)  

<details><summary>Answer</summary>

**(4)** — A record groups elements of possibly different types.

</details>

**Q22.** `Medium`  
An enumeration type in C

(1) is a user-defined type whose values are named integer constants  
(2) is a floating-point type  
(3) stores strings  
(4) is a pointer type  

<details><summary>Answer</summary>

**(1)** — For example enum colour { RED, GREEN, BLUE }.

</details>

**Q23.** `Medium`  
Given below are two statements.  
Statement I: Static scoping determines non-local references from the program text.  
Statement II: Most modern languages, including C, Java and Python, use dynamic scoping by default.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — They use static (lexical) scoping; early Lisp and some shells used dynamic scoping.

</details>

**Q24.** `Low`  
FORTRAN, one of the earliest high-level languages, was designed mainly for

(1) scientific and numerical computation  
(2) artificial intelligence  
(3) business data processing  
(4) web development  

<details><summary>Answer</summary>

**(1)** — COBOL was designed for business data processing and LISP for AI.

</details>

**Q25.** `Medium`  
Match List I with List II.  
List I (Language): A. COBOL  B. LISP  C. Prolog  D. Ada  
List II (Main application area or feature): I. Logic programming and AI  II. Business data processing  III. Safety-critical and embedded systems  IV. Symbolic processing with lists

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-I, C-IV, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(2)** — Ada was developed for the US Department of Defense.

</details>

**Q26.** `Medium`  
A type system is called type-safe if

(1) it has no types  
(2) it prevents operations from being applied to values of inappropriate types  
(3) it allows any operation on any value  
(4) it is interpreted  

<details><summary>Answer</summary>

**(2)** — Type safety rules out errors such as treating an integer as a pointer.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: An interpreted program generally executes faster than the same program compiled to machine code.  
Statement II: Java source code is compiled directly into native machine code for each processor.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Compiled code is generally faster, and Java is compiled to bytecode that is interpreted or JIT-compiled by the JVM.

</details>

**Q28.** `Medium`  
Which of the following languages uses indentation to define blocks?

(1) Pascal  
(2) C  
(3) Java  
(4) Python  

<details><summary>Answer</summary>

**(4)** — C, Java and many others use braces or keywords such as begin and end.

</details>

**Q29.** `Low`  
The ability of a language to treat functions as values that can be passed as arguments and returned from functions is called

(1) static binding  
(2) first-class functions  
(3) overloading  
(4) coercion  

<details><summary>Answer</summary>

**(2)** — Higher-order functions are central to functional programming.

</details>

**Q30.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Pure functional programs are easier to reason about and parallelise.  
Reason R: Pure functions have no side effects, so a call always returns the same result for the same arguments.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This property is referential transparency.

</details>
