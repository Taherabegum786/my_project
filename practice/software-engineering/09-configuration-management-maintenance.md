# Set 9 — Software Configuration Management, Maintenance, Reuse, Re-engineering and Reverse Engineering

**22 questions** — High: 7, Medium: 14, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Maintenance type): A. Corrective  B. Adaptive  C. Perfective  D. Preventive  
List II (Purpose): I. Changing the software to improve future maintainability or reliability  II. Fixing defects discovered after delivery  III. Adding enhancements and improving performance as user requirements evolve  IV. Modifying the software to work in a changed environment, such as a new OS

(1) A-II, B-IV, C-I, D-III  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(3)** — Preventive maintenance is also called re-engineering.

</details>

**Q2.** `High`  
Which type of maintenance usually accounts for the largest share of maintenance effort?

(1) Corrective  
(2) Perfective  
(3) Adaptive  
(4) Preventive  

<details><summary>Answer</summary>

**(2)** — Studies typically attribute about half of maintenance effort to perfective changes.

</details>

**Q3.** `High`  
Given below are two statements.  
Statement I: A baseline is a specification or product that has been formally reviewed and agreed upon and can be changed only through formal change control.  
Statement II: A software configuration item (SCI) is information created as part of the software process, such as a document, test suite or program component.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Baselines mark milestones in the delivery of SCIs.

</details>

**Q4.** `High`  
Which of the following are tasks in software configuration management?  
A. Identification of configuration items  B. Version control  C. Change control  D. Configuration auditing  E. Status reporting  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) A, B and C only  
(3) B, C and D only  
(4) A, D and E only  

<details><summary>Answer</summary>

**(1)** — These are the SCM tasks described by Pressman.

</details>

**Q5.** `High`  
In change control, the body that evaluates and approves or rejects change requests is the

(1) quality circle  
(2) test team  
(3) change control board (or change control authority)  
(4) end users only  

<details><summary>Answer</summary>

**(3)** — An approved change leads to an engineering change order (ECO).

</details>

**Q6.** `High`  
Arrange the activities of Pressman's software re-engineering process model in a typical order.  
A. Reverse engineering  B. Inventory analysis  C. Forward engineering  D. Document restructuring  E. Code restructuring

(1) A, B, D, E, C  
(2) B, D, A, E, C  
(3) D, B, A, C, E  
(4) B, A, D, E, C  

<details><summary>Answer</summary>

**(2)** — Data restructuring accompanies code restructuring; the model is cyclic.

</details>

**Q7.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Reverse engineering extracts design and specification information from existing source code.  
Reason R: Reverse engineering changes the functionality of the system.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Reverse engineering is analysis only; it does not change the system.

</details>

**Q8.** `Medium`  
Forward engineering in the context of re-engineering means

(1) testing only  
(2) analysing old code  
(3) deleting the old system  
(4) using recovered design information to restructure or rebuild the system with modern methods  

<details><summary>Answer</summary>

**(4)** — It often improves quality and adds new functions.

</details>

**Q9.** `Medium`  
Given below are two statements.  
Statement I: Git is a distributed version control system in which every developer has a full copy of the repository history.  
Statement II: Subversion (SVN) is a distributed version control system.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — SVN and CVS are centralised version control systems.

</details>

**Q10.** `Medium`  
Match List I with List II.  
List I (Lehman's law of software evolution): A. Continuing change  B. Increasing complexity  C. Continuing growth  D. Declining quality  
List II (Statement): I. Functionality must grow to maintain user satisfaction  II. A system must be continually adapted or it becomes progressively less useful  III. Quality appears to decline unless the system is adapted to environmental changes  IV. As a system evolves, its complexity increases unless work is done to reduce it

(1) A-II, B-IV, C-III, D-I  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-IV, C-I, D-III  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — Lehman's laws apply to E-type (real-world) systems.

</details>

**Q11.** `Medium`  
Maintenance typically accounts for what share of the total life-cycle cost of software?

(1) About 25%  
(2) About 60% or more  
(3) Less than 5%  
(4) About 10%  

<details><summary>Answer</summary>

**(2)** — Estimates usually range from 60% to 80%.

</details>

**Q12.** `Medium`  
The abstraction level of reverse engineering refers to

(1) the testing level  
(2) the number of lines of code  
(3) the sophistication of the design information that can be extracted, from procedural design up to data flow and ER models  
(4) the programming language  

<details><summary>Answer</summary>

**(3)** — Completeness, interactivity and directionality are other properties of reverse engineering.

</details>

**Q13.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Software reuse can reduce development cost and improve reliability.  
Reason R: Reused components have already been tested and used in working systems.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Reuse also brings costs: finding, understanding and adapting components.

</details>

**Q14.** `Medium`  
COTS stands for

(1) Common Object Transfer Standard  
(2) Commercial Off-The-Shelf  
(3) Code Optimization Tool Set  
(4) Configuration Of Test Suites  

<details><summary>Answer</summary>

**(2)** — COTS components are bought and integrated rather than built.

</details>

**Q15.** `Medium`  
Domain engineering in software reuse involves

(1) fixing defects  
(2) identifying, constructing, cataloguing and disseminating reusable components for an application domain  
(3) writing user manuals  
(4) testing one program  

<details><summary>Answer</summary>

**(2)** — Its three major activities are analysis, construction and dissemination.

</details>

**Q16.** `Medium`  
Given below are two statements.  
Statement I: Legacy systems are always easy to maintain because they are well documented.  
Statement II: A legacy system is an old system that remains in use because it is critical to the business.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Legacy systems often have poor documentation, obsolete technology and degraded structure.

</details>

**Q17.** `Medium`  
Code restructuring in re-engineering

(1) modifies the code to improve its structure and quality without changing its function  
(2) translates the code to another hardware platform only  
(3) removes all comments  
(4) changes the external behaviour of the code  

<details><summary>Answer</summary>

**(1)** — It is similar to refactoring at a larger scale.

</details>

**Q18.** `Medium`  
In version control, branching is used to

(1) compile the code  
(2) delete old versions  
(3) develop features or fixes in parallel without affecting the main line, merging them later  
(4) test the system  

<details><summary>Answer</summary>

**(3)** — Merging combines the changes from branches.

</details>

**Q19.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Configuration auditing ensures that a change has been properly implemented.  
Reason R: SCM is applied only after the software is delivered.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — SCM is an umbrella activity applied throughout the software process.

</details>

**Q20.** `Medium`  
The SCM repository is

(1) a design pattern  
(2) a test-case generator  
(3) a compiler  
(4) a database that stores configuration items, their versions and relationships  

<details><summary>Answer</summary>

**(4)** — It supports versioning, dependency tracking, requirements tracing and audit trails.

</details>

**Q21.** `Low`  
Reverse engineering of data typically produces

(1) test cases  
(2) data models such as entity-relationship diagrams from existing database structures  
(3) a new user interface  
(4) machine code  

<details><summary>Answer</summary>

**(2)** — It is often the first reverse-engineering task.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: Re-engineering is always cheaper than developing a new system from scratch.  
Statement II: Inventory analysis in re-engineering assesses applications by business criticality, longevity and maintainability.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Re-engineering is not always cheaper; inventory analysis helps decide which applications are worth re-engineering.

</details>
