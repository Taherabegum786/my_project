# Set 10 — Run-Time Environments (storage organization, activation records, parameter passing, scoping, symbol tables)

**24 questions** — High: 10, Medium: 13, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Consider: procedure p(x, y) { x = x + 1; y = y + 1; } and the main program a = 1; p(a, a); print(a). The values printed under call by value, call by reference and call by value-result are respectively

(1) 3, 3 and 2  
(2) 1, 2 and 3  
(3) 1, 3 and 3  
(4) 1, 3 and 2  

<details><summary>Answer</summary>

**(4)** — By value: a is unchanged. By reference: x and y are both a, incremented twice. By value-result: x and y become 2 and are copied back to a.

</details>

**Q2.** `High`  
Consider swap(x, y) { t = x; x = y; y = t; } called as swap(a, b) with a = 1 and b = 2. The values of a and b afterwards under call by value and under call by reference are respectively

(1) 2, 1 and 2, 1  
(2) 1, 2 and 1, 2  
(3) 2, 1 and 1, 2  
(4) 1, 2 and 2, 1  

<details><summary>Answer</summary>

**(4)** — Call by value swaps only the local copies.

</details>

**Q3.** `High`  
Consider: int x = 1; void f() { print(x); } void g() { int x = 2; f(); } and main calls g(). The values printed under static and dynamic scoping are respectively

(1) 2 and 1  
(2) 1 and 1  
(3) 1 and 2  
(4) 2 and 2  

<details><summary>Answer</summary>

**(3)** — Static scoping uses the x in f's defining environment (global); dynamic scoping uses the most recent active binding (g's x).

</details>

**Q4.** `High`  
Match List I with List II.  
List I (Parameter passing method): A. Call by value  B. Call by reference  C. Call by value-result  D. Call by name  
List II (Description): I. The address of the actual parameter is passed  II. The actual parameter is textually substituted and re-evaluated on each use  III. The value is copied in, and the final value is copied back on return  IV. The value of the actual parameter is copied into the formal

(1) A-IV, B-III, C-I, D-II  
(2) A-IV, B-I, C-III, D-II  
(3) A-I, B-IV, C-III, D-II  
(4) A-IV, B-I, C-II, D-III  

<details><summary>Answer</summary>

**(2)** — Call by name is implemented with thunks (as in ALGOL 60).

</details>

**Q5.** `High`  
Match List I with List II.  
List I (Activation record field): A. Control link  B. Access link  C. Saved machine status  D. Return value  
List II (Purpose): I. Points to the activation record of the lexically enclosing procedure, for non-local data  II. Points to the activation record of the caller  III. Holds the return address and register contents  IV. Space for the value returned to the caller

(1) A-I, B-II, C-III, D-IV  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-III, C-I, D-IV  
(4) A-II, B-I, C-III, D-IV  

<details><summary>Answer</summary>

**(4)** — The control link is also called the dynamic link, and the access link the static link.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: Static allocation of activation records cannot support recursion.  
Statement II: Stack allocation of activation records supports recursion.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — With static allocation (as in early FORTRAN) each procedure has only one activation record.

</details>

**Q7.** `High`  
main calls fact(5), where fact(n) returns 1 if n ≤ 1 and n × fact(n − 1) otherwise. The maximum number of activation records on the control stack, including main's, is

(1) 7  
(2) 6  
(3) 5  
(4) 10  

<details><summary>Answer</summary>

**(2)** — main, fact(5), fact(4), fact(3), fact(2) and fact(1) are active together.

</details>

**Q8.** `High`  
In the typical run-time memory layout of a C program,

(1) there is no heap  
(2) the code and static data are at fixed locations, and the heap and stack grow towards each other  
(3) the heap is inside the stack  
(4) the stack and the heap both grow towards higher addresses  

<details><summary>Answer</summary>

**(2)** — The heap usually grows upward and the stack downward.

</details>

**Q9.** `Medium`  
An activation tree represents

(1) the flow graph  
(2) the parse tree  
(3) the sequence of procedure activations during one run, with each child a call made by its parent  
(4) the call graph of a program at compile time  

<details><summary>Answer</summary>

**(3)** — The control stack at any time holds the activations on a path from the root.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Reference counting reclaims cyclic garbage as soon as the cycle becomes unreachable.  
Reason R: Objects in an unreachable cycle still have non-zero reference counts.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Because of R, reference counting cannot reclaim cycles; tracing collectors can.

</details>

**Q11.** `High`  
Match List I with List II.  
List I (Garbage collection technique): A. Reference counting  B. Mark-and-sweep  C. Copying collection  D. Generational collection  
List II (Characteristic): I. Moves live objects to a new space, compacting memory  II. Collects young objects more often, since most objects die young  III. Reclaims an object as soon as its count drops to zero  IV. Marks reachable objects from the roots and then frees the unmarked ones

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-I, C-IV, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(1)** — Common garbage-collection strategies.

</details>

**Q12.** `Medium`  
A dangling reference occurs when

(1) a pointer refers to storage that has already been deallocated  
(2) memory is never freed  
(3) the stack overflows  
(4) a variable is not initialised  

<details><summary>Answer</summary>

**(1)** — For example, returning the address of a local variable in C.

</details>

**Q13.** `Medium`  
A display is used to

(1) allocate heap memory  
(2) access non-local variables in nested procedures quickly through an array of pointers to activation records at each nesting depth  
(3) show the output of a program  
(4) store the symbol table  

<details><summary>Answer</summary>

**(2)** — It avoids following a chain of access links.

</details>

**Q14.** `Medium`  
In a language with nested procedures, accessing a variable declared at nesting depth 1 from a procedure at nesting depth 3 using access links requires following

(1) 2 access links  
(2) 3 access links  
(3) 1 access link  
(4) no links  

<details><summary>Answer</summary>

**(1)** — The number of links equals the difference in nesting depths.

</details>

**Q15.** `Medium`  
Given below are two statements.  
Statement I: C passes an array parameter by copying all of its elements.  
Statement II: In Java, assigning a new object to a parameter inside a method changes the caller's variable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — In C the array name decays to a pointer; Java passes references by value, so reassigning the parameter has no effect on the caller.

</details>

**Q16.** `Medium`  
Which data structure is most commonly used to implement a symbol table in a compiler for fast look-up?

(1) Stack  
(2) Hash table  
(3) Queue  
(4) Linear list  

<details><summary>Answer</summary>

**(2)** — Scoping is handled by a stack of tables or by chaining entries by scope.

</details>

**Q17.** `Medium`  
To handle nested block scopes, a compiler can

(1) use only static allocation  
(2) use a single global table with no scope information  
(3) maintain a separate symbol table for each scope, linked to the table of the enclosing scope  
(4) ignore inner declarations  

<details><summary>Answer</summary>

**(3)** — Look-up searches the innermost table first and then outward.

</details>

**Q18.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Local variables of a recursive procedure must be allocated on the stack (or heap), not statically.  
Reason R: Several activations of the procedure may be alive at the same time, each needing its own copy of the locals.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Static allocation gives one copy per procedure.

</details>

**Q19.** `Medium`  
The calling sequence of a procedure call is code that

(1) optimizes the procedure body  
(2) links object files  
(3) allocates the activation record and fills in its fields on the caller and callee sides  
(4) parses the procedure  

<details><summary>Answer</summary>

**(3)** — The return sequence restores the machine state and returns.

</details>

**Q20.** `Medium`  
Under call by name, a procedure with formal parameter x evaluates the actual parameter expression

(1) only if x is assigned  
(2) never  
(3) each time x is used in the body  
(4) once, before the call  

<details><summary>Answer</summary>

**(3)** — Jensen's device exploits this behaviour.

</details>

**Q21.** `Medium`  
Heap allocation is needed for

(1) local variables of non-recursive procedures  
(2) register variables  
(3) global constants  
(4) data whose lifetime is not tied to procedure activations, such as dynamically created objects  

<details><summary>Answer</summary>

**(4)** — It is managed with malloc/free, new/delete or garbage collection.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: The access link of a procedure's activation record points to its caller.  
Statement II: In a language without nested procedures, such as C, access links are not needed.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — The access link points to the lexically enclosing procedure; the control link points to the caller.

</details>

**Q23.** `Low`  
The area of memory used to hold the activation records of procedures during execution is the

(1) code area  
(2) heap  
(3) control stack  
(4) static area  

<details><summary>Answer</summary>

**(3)** — Activation records are pushed on calls and popped on returns.

</details>

**Q24.** `Medium`  
A function in C returns a pointer to one of its local (automatic) variables. This is an error because

(1) local variables are stored in the heap  
(2) the local variable is freed when the function returns, leaving a dangling pointer  
(3) C does not allow pointers  
(4) the pointer is copied by value  

<details><summary>Answer</summary>

**(2)** — A static local variable would not have this problem.

</details>
