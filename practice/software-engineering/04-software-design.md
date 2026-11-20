# Set 4 — Software Design (design concepts, cohesion and coupling, architectural, data, user-interface and component-level design, design patterns)

**29 questions** — High: 11, Medium: 17, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Arrange the following types of cohesion from the lowest (worst) to the highest (best).  
A. Functional  B. Coincidental  C. Temporal  D. Sequential  E. Logical

(1) B, C, E, D, A  
(2) B, E, C, D, A  
(3) B, E, D, C, A  
(4) E, B, C, D, A  

<details><summary>Answer</summary>

**(2)** — Coincidental &lt; logical &lt; temporal &lt; procedural &lt; communicational &lt; sequential &lt; functional.

</details>

**Q2.** `High`  
Arrange the following types of coupling from the worst (tightest) to the best (loosest).  
A. Data coupling  B. Content coupling  C. Control coupling  D. Common coupling  E. Stamp coupling

(1) B, D, E, C, A  
(2) B, D, C, E, A  
(3) D, B, C, E, A  
(4) B, C, D, E, A  

<details><summary>Answer</summary>

**(2)** — Content &gt; common &gt; external &gt; control &gt; stamp &gt; data coupling.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (Coupling type): A. Content coupling  B. Common coupling  C. Control coupling  D. Data coupling  
List II (Description): I. Modules share global data  II. One module passes a flag that controls the logic of another  III. Modules communicate only through parameters that are elementary data items  IV. One module directly modifies or depends on the internal workings of another

(1) A-I, B-IV, C-II, D-III  
(2) A-IV, B-II, C-I, D-III  
(3) A-IV, B-I, C-II, D-III  
(4) A-IV, B-I, C-III, D-II  

<details><summary>Answer</summary>

**(3)** — Stamp coupling passes a whole data structure when only part is needed.

</details>

**Q4.** `High`  
Match List I with List II.  
List I (Cohesion type): A. Logical cohesion  B. Temporal cohesion  C. Communicational cohesion  D. Functional cohesion  
List II (Description): I. All elements contribute to a single well-defined task  II. Elements perform logically similar tasks, selected by a control flag  III. Elements operate on the same input or output data  IV. Elements are grouped because they execute at the same time, such as initialisation

(1) A-II, B-III, C-IV, D-I  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — Functional cohesion is the ideal.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: A good design aims for high cohesion and low coupling.  
Statement II: Functional independence is achieved by modules with a single purpose and limited interaction with other modules.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Cohesion and coupling are the two qualitative measures of functional independence.

</details>

**Q6.** `High`  
The concept of information hiding, proposed by David Parnas, states that

(1) modules should hide their design decisions and data from other modules, exposing only what is necessary through interfaces  
(2) code should be obfuscated  
(3) all data should be global  
(4) programs should not have comments  

<details><summary>Answer</summary>

**(1)** — It limits the propagation of errors and changes.

</details>

**Q7.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Dividing software into a very large number of tiny modules minimises total development cost.  
Reason R: As the number of modules grows, the cost of integrating them (interfaces) also grows.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — There is a region of minimum cost; too many modules raise integration cost, which is what R says, so A is false.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Architectural style): A. Data-centred  B. Data-flow  C. Call-and-return  D. Layered  
List II (Example): I. Pipes and filters  II. Main program and subprograms, remote procedure call  III. A central repository or blackboard accessed by independent clients  IV. OSI protocol stack with services at each level

(1) A-III, B-I, C-II, D-IV  
(2) A-I, B-III, C-II, D-IV  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-II, C-I, D-IV  

<details><summary>Answer</summary>

**(1)** — Architectural styles from Pressman and Shaw and Garlan.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Design principle): A. Single responsibility principle  B. Open-closed principle  C. Liskov substitution principle  D. Dependency inversion principle  
List II (Statement): I. Subclasses should be substitutable for their base classes  II. Depend on abstractions, not on concrete classes  III. A class should have only one reason to change  IV. A module should be open for extension but closed for modification

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-II, D-I  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — These, with interface segregation, form the SOLID principles.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Design pattern): A. Singleton  B. Observer  C. Adapter  D. Factory method  
List II (Category and purpose): I. Behavioral; notifies dependents automatically when an object changes state  II. Creational; lets subclasses decide which class to instantiate  III. Creational; ensures a class has only one instance  IV. Structural; converts the interface of a class into one that clients expect

(1) A-III, B-I, C-II, D-IV  
(2) A-III, B-IV, C-I, D-II  
(3) A-I, B-III, C-IV, D-II  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(4)** — Patterns from the Gang of Four catalogue.

</details>

**Q11.** `Medium`  
The Gang of Four catalogue classifies its 23 design patterns into

(1) architectural, process and test patterns  
(2) static and dynamic patterns  
(3) creational, structural and behavioral patterns  
(4) analysis, design and coding patterns  

<details><summary>Answer</summary>

**(3)** — Examples: Builder (creational), Decorator (structural), Strategy (behavioral).

</details>

**Q12.** `Medium`  
The Model-View-Controller (MVC) architecture separates

(1) the database from the network  
(2) hardware from software  
(3) data and business logic (model), presentation (view) and input handling (controller)  
(4) testing from development  

<details><summary>Answer</summary>

**(3)** — It is widely used in web and GUI applications.

</details>

**Q13.** `High`  
Theo Mandel's three golden rules for user-interface design are

(1) use only keyboard input  
(2) use many colours, many fonts and many windows  
(3) place the user in control, reduce the user's memory load, and make the interface consistent  
(4) minimise testing, maximise features, use defaults  

<details><summary>Answer</summary>

**(3)** — For example, provide undo, use meaningful defaults and keep conventions consistent.

</details>

**Q14.** `Medium`  
Stepwise refinement, a top-down design strategy, was proposed by

(1) Niklaus Wirth  
(2) David Parnas  
(3) Barry Boehm  
(4) Edsger Dijkstra  

<details><summary>Answer</summary>

**(1)** — Each step decomposes a high-level statement into more detailed ones.

</details>

**Q15.** `Medium`  
Given below are two statements.  
Statement I: Abstraction allows a designer to focus on a problem at some level of generalisation without regard to low-level details.  
Statement II: Refactoring changes the external behaviour of a program to add new features.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Refactoring improves internal structure without changing external behaviour.

</details>

**Q16.** `Medium`  
In a structure chart, fan-out of a module is

(1) the number of modules it directly calls  
(2) the number of parameters  
(3) the depth of the chart  
(4) the number of modules that call it  

<details><summary>Answer</summary>

**(1)** — Fan-in is the number of modules that call a given module; high fan-in indicates reuse.

</details>

**Q17.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: High fan-out is generally desirable in a module structure.  
Reason R: A module with high fan-in is reused by many other modules.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — High fan-in is desirable; very high fan-out suggests that a module controls too many subordinates.

</details>

**Q18.** `Medium`  
In structured design, transform analysis is used when the data flow diagram shows

(1) no data flow  
(2) a single item triggering one of many paths (a transaction centre)  
(3) only data stores  
(4) incoming flow, a transform centre and outgoing flow  

<details><summary>Answer</summary>

**(4)** — Transaction analysis is used for transaction flow.

</details>

**Q19.** `Medium`  
The facade design pattern

(1) defines a family of algorithms  
(2) ensures one instance  
(3) provides a unified, simplified interface to a set of interfaces in a subsystem  
(4) lets an object change its behaviour when its state changes  

<details><summary>Answer</summary>

**(3)** — It reduces coupling between clients and subsystem classes.

</details>

**Q20.** `Medium`  
The interface segregation principle states that

(1) clients should not be forced to depend on interfaces they do not use  
(2) interfaces must not change  
(3) every class must implement every interface  
(4) interfaces should be as large as possible  

<details><summary>Answer</summary>

**(1)** — Many client-specific interfaces are better than one general-purpose interface.

</details>

**Q21.** `Medium`  
Which design pattern defines a family of algorithms, encapsulates each one and makes them interchangeable?

(1) Strategy  
(2) Builder  
(3) Composite  
(4) Proxy  

<details><summary>Answer</summary>

**(1)** — The client chooses the algorithm at run time.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: Architectural design defines the relationships among the major structural elements of the software.  
Statement II: Component-level design transforms structural elements into a procedural description of each component.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Data, architectural, interface and component-level design are the four design models in Pressman.

</details>

**Q23.** `Medium`  
Data design at the architectural level may involve

(1) writing test cases  
(2) choosing loop variables  
(3) selecting the colour scheme  
(4) designing a data warehouse or database to support business needs  

<details><summary>Answer</summary>

**(4)** — At the component level, data design chooses data structures.

</details>

**Q24.** `Medium`  
The design concept "separation of concerns" means that

(1) data and code are always mixed  
(2) a complex problem is easier to handle if it is subdivided into pieces that can each be solved independently  
(3) only one person designs the system  
(4) all concerns are placed in one module  

<details><summary>Answer</summary>

**(2)** — Modularity, aspects and functional independence are manifestations of this concept.

</details>

**Q25.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Global variables increase coupling between modules.  
Reason R: Modules that share global data are common-coupled, so a change to the data can affect all of them.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Common coupling is the second-worst kind of coupling.

</details>

**Q26.** `Medium`  
In component-level design, the Common Closure Principle states that

(1) all classes should be in one package  
(2) every class needs its own package  
(3) packages must never change  
(4) classes that change together should be packaged together  

<details><summary>Answer</summary>

**(4)** — Related principles are the Release Reuse Equivalency and Common Reuse principles.

</details>

**Q27.** `Medium`  
Which of the following is a structural design pattern?

(1) Iterator  
(2) Command  
(3) Observer  
(4) Decorator  

<details><summary>Answer</summary>

**(4)** — Decorator attaches additional responsibilities to an object dynamically.

</details>

**Q28.** `Low`  
A good software design should exhibit

(1) tight coupling and low cohesion  
(2) loose coupling and high cohesion  
(3) loose coupling and low cohesion  
(4) tight coupling and high cohesion  

<details><summary>Answer</summary>

**(2)** — This makes modules independent, understandable and maintainable.

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: The pipe-and-filter architecture is well suited to interactive applications with complex user interaction.  
Statement II: In a layered architecture, each layer may use the services of every other layer, above or below.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Pipe-and-filter suits batch transformation; in a strict layered architecture a layer uses only the layer directly below it.

</details>
