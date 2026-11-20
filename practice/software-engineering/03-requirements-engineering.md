# Set 3 — Software Requirements (functional and non-functional requirements, elicitation, use cases, analysis modelling, SRS)

**27 questions** — High: 9, Medium: 17, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Requirement): A. The system shall allow a user to reset the password  B. The system shall respond to any query within 2 seconds  C. The system shall run on Linux and Windows  D. The system shall encrypt all stored passwords  
List II (Type): I. Portability requirement  II. Functional requirement  III. Security requirement  IV. Performance requirement

(1) A-II, B-I, C-IV, D-III  
(2) A-IV, B-II, C-I, D-III  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(3)** — Functional requirements describe what the system does; the others are non-functional (quality) requirements.

</details>

**Q2.** `High`  
Given below are two statements.  
Statement I: Functional requirements describe the services the system should provide.  
Statement II: Non-functional requirements describe constraints such as performance, reliability and usability.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Non-functional requirements often apply to the system as a whole.

</details>

**Q3.** `High`  
Arrange the requirements engineering tasks described by Pressman in order.  
A. Elicitation  B. Inception  C. Negotiation  D. Elaboration  E. Specification

(1) B, D, A, C, E  
(2) B, A, C, D, E  
(3) A, B, D, C, E  
(4) B, A, D, C, E  

<details><summary>Answer</summary>

**(4)** — Validation and requirements management follow specification.

</details>

**Q4.** `High`  
Which of the following are characteristics of a good SRS according to IEEE 830?  
A. Correct  B. Unambiguous  C. Complete  D. Verifiable  E. Describes how the system will be implemented  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) C, D and E only  
(3) A, B and E only  
(4) A, B, C and D only  

<details><summary>Answer</summary>

**(4)** — An SRS states what the system must do, not how it will be designed.

</details>

**Q5.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Every requirement in an SRS should be verifiable.  
Reason R: A requirement such as "the system should be user-friendly" cannot be tested objectively.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Requirements should be stated in measurable terms, for example "a new user completes registration within 3 minutes".

</details>

**Q6.** `High`  
In Quality Function Deployment (QFD), requirements that the customer does not explicitly state but whose absence causes dissatisfaction are called

(1) normal requirements  
(2) expected requirements  
(3) exciting requirements  
(4) functional requirements  

<details><summary>Answer</summary>

**(2)** — Normal requirements are stated explicitly; exciting requirements go beyond expectations.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Analysis model element): A. Scenario-based  B. Class-based  C. Behavioral  D. Flow-oriented  
List II (Example): I. State diagrams and sequence diagrams  II. Use cases and activity diagrams  III. Data flow diagrams and the data dictionary  IV. Class diagrams and CRC models

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(3)** — Elements of the requirements (analysis) model in Pressman.

</details>

**Q8.** `High`  
A level-0 data flow diagram (context diagram) shows

(1) only data stores  
(2) the internal processes in detail  
(3) the control flow of the program  
(4) the entire system as a single process (bubble) with its external entities and data flows  

<details><summary>Answer</summary>

**(4)** — Lower levels refine the single bubble into sub-processes.

</details>

**Q9.** `Medium`  
Given below are two statements.  
Statement I: A data flow diagram shows the sequence and control logic of processing.  
Statement II: When a DFD bubble is refined, the inputs and outputs of the refined diagram must match those of the parent bubble (balancing).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A DFD shows the flow of data, not control or sequencing.

</details>

**Q10.** `Medium`  
In a use case diagram, the relationship in which a base use case optionally includes extra behaviour under certain conditions is called

(1) association  
(2) generalization  
(3) extend  
(4) include  

<details><summary>Answer</summary>

**(3)** — An include relationship is mandatory: the base use case always uses the included behaviour.

</details>

**Q11.** `Medium`  
An actor in a use case diagram is

(1) a class in the system  
(2) a database table  
(3) a role played by a person or external system that interacts with the system  
(4) a test case  

<details><summary>Answer</summary>

**(3)** — Primary actors initiate use cases; secondary actors support the system.

</details>

**Q12.** `High`  
Which of the following is a technique for requirements elicitation?  
A. Interviews  B. Collaborative requirements gathering (JAD)  C. Questionnaires  D. Observation (ethnography)  E. Code inspection  
Choose the correct answer from the options given below:

(1) C, D and E only  
(2) A, B, C and D only  
(3) A, B, C, D and E  
(4) A, B and E only  

<details><summary>Answer</summary>

**(2)** — Code inspection is a verification technique, not elicitation.

</details>

**Q13.** `Medium`  
A requirements traceability matrix is used to

(1) draw DFDs  
(2) estimate cost  
(3) link each requirement to its sources, design elements, code and test cases  
(4) schedule the project  

<details><summary>Answer</summary>

**(3)** — It helps assess the impact of changes and confirm that every requirement is tested.

</details>

**Q14.** `Medium`  
The data dictionary in structured analysis contains

(1) test results  
(2) the source code  
(3) definitions of all data elements, data flows and data stores used in the DFDs  
(4) the project schedule  

<details><summary>Answer</summary>

**(3)** — It gives each name a precise meaning.

</details>

**Q15.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Requirements validation checks that the requirements actually define the system the customer wants.  
Reason R: Requirements errors found after delivery are much cheaper to fix than errors found during the requirements phase.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Errors found later are far more expensive, which is why validation is done early.

</details>

**Q16.** `Medium`  
Which of the following is NOT a requirements validation technique?

(1) Test-case generation  
(2) Prototyping  
(3) Regression testing  
(4) Requirements reviews  

<details><summary>Answer</summary>

**(3)** — Regression testing is done after changes to code.

</details>

**Q17.** `Medium`  
Domain requirements are requirements that

(1) are always non-functional  
(2) are optional  
(3) apply only to the user interface  
(4) come from the application domain of the system and reflect its characteristics  

<details><summary>Answer</summary>

**(4)** — For example, rules and regulations of banking for a banking system.

</details>

**Q18.** `Medium`  
In a swimlane diagram (a variation of the activity diagram), each lane represents

(1) a time period  
(2) a use case  
(3) an actor or analysis class responsible for the activities in it  
(4) a database table  

<details><summary>Answer</summary>

**(3)** — It shows who is responsible for each activity.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: Once the SRS is approved, requirements never change in practice.  
Statement II: Requirements management is the process of managing changes to requirements throughout the project.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Requirements change frequently; change control and traceability are needed.

</details>

**Q20.** `Medium`  
Ambiguity in requirements can be reduced most effectively by

(1) starting coding early  
(2) avoiding customer contact  
(3) using precise, measurable language, glossaries and, where needed, formal specifications  
(4) writing longer documents  

<details><summary>Answer</summary>

**(3)** — Each requirement should have only one interpretation.

</details>

**Q21.** `Medium`  
The IEEE standard for the Software Requirements Specification is

(1) IEEE 1012  
(2) IEEE 730  
(3) IEEE 829  
(4) IEEE 830  

<details><summary>Answer</summary>

**(4)** — IEEE 829 is for test documentation and IEEE 730 for SQA plans.

</details>

**Q22.** `Medium`  
The Kano model classifies customer requirements into

(1) hardware and software  
(2) functional and non-functional only  
(3) basic (must-be), performance and excitement (delighter) requirements  
(4) internal and external  

<details><summary>Answer</summary>

**(3)** — It is related to the normal, expected and exciting requirements of QFD.

</details>

**Q23.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Use cases are useful for capturing functional requirements.  
Reason R: UML is standardised by the Object Management Group.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but use cases help because they describe actor-system interactions from the user's point of view.

</details>

**Q24.** `Medium`  
Feasibility study in requirements engineering assesses

(1) the cyclomatic complexity  
(2) the coupling of modules  
(3) the number of test cases  
(4) whether the system is technically, economically and operationally feasible  

<details><summary>Answer</summary>

**(4)** — It decides whether the project is worth pursuing.

</details>

**Q25.** `Low`  
SRS stands for

(1) System Resource Schedule  
(2) Software Release Summary  
(3) Software Requirements Specification  
(4) Structured Requirement Syntax  

<details><summary>Answer</summary>

**(3)** — It is the official statement of what the developers should implement.

</details>

**Q26.** `Medium`  
Given below are two statements.  
Statement I: An entity-relationship diagram can be used in data modelling during requirements analysis.  
Statement II: State diagrams model the behaviour of a system in response to external events.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are parts of the analysis model.

</details>

**Q27.** `Medium`  
Requirements negotiation is needed because

(1) testing is expensive  
(2) requirements are always consistent  
(3) customers and stakeholders often have conflicting requirements and limited resources  
(4) the developers write the requirements  

<details><summary>Answer</summary>

**(3)** — The win-win approach seeks requirements acceptable to all stakeholders.

</details>
