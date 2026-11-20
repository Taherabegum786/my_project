# Set 5 — Object-Oriented Analysis and Design and UML

**21 questions** — High: 7, Medium: 13, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (UML relationship): A. Generalization  B. Composition  C. Aggregation  D. Dependency  
List II (Notation): I. Dashed line with an open arrowhead  II. Solid line with a hollow triangle pointing to the parent  III. Solid line with a filled diamond at the whole  IV. Solid line with a hollow diamond at the whole

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-III, B-II, C-IV, D-I  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(1)** — Realization is a dashed line with a hollow triangle.

</details>

**Q2.** `High`  
Given below are two statements.  
Statement I: In composition, the part cannot exist independently of the whole and is destroyed with it.  
Statement II: In aggregation, the part may exist independently of the whole.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — For example, rooms in a house (composition) versus players in a team (aggregation).

</details>

**Q3.** `High`  
Match List I with List II.  
List I (UML diagram): A. Sequence diagram  B. State machine diagram  C. Deployment diagram  D. Use case diagram  
List II (What it models): I. The physical nodes and the artifacts deployed on them  II. Interactions between objects ordered in time  III. Functional requirements as interactions between actors and the system  IV. The states of an object and the events that cause transitions

(1) A-II, B-I, C-IV, D-III  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(2)** — UML structural and behavioural diagrams.

</details>

**Q4.** `High`  
Which of the following are structural (static) UML diagrams?  
A. Class diagram  B. Component diagram  C. Deployment diagram  D. Activity diagram  E. Object diagram  
Choose the correct answer from the options given below:

(1) C, D and E only  
(2) A, B, C and E only  
(3) A, B, C, D and E  
(4) A, B and D only  

<details><summary>Answer</summary>

**(2)** — Activity diagrams are behavioural.

</details>

**Q5.** `High`  
In UML class notation, the visibility markers +, − and # denote respectively

(1) protected, private and public  
(2) private, public and protected  
(3) public, protected and private  
(4) public, private and protected  

<details><summary>Answer</summary>

**(4)** — ~ denotes package visibility.

</details>

**Q6.** `Medium`  
UML 2.x defines how many types of diagrams?

(1) 12  
(2) 16  
(3) 14  
(4) 9  

<details><summary>Answer</summary>

**(3)** — Seven structure diagrams and seven behaviour diagrams (including four interaction diagrams).

</details>

**Q7.** `Medium`  
The communication (collaboration) diagram and the sequence diagram are both

(1) interaction diagrams showing messages between objects  
(2) structure diagrams  
(3) deployment diagrams  
(4) use case diagrams  

<details><summary>Answer</summary>

**(1)** — The sequence diagram emphasises time ordering; the communication diagram emphasises links between objects.

</details>

**Q8.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Encapsulation improves maintainability.  
Reason R: Inheritance lets a subclass reuse the code of its superclass.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but encapsulation helps maintenance by hiding internal data behind an interface, which R does not mention.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (CK metric): A. WMC  B. DIT  C. NOC  D. CBO  
List II (Meaning): I. Number of immediate subclasses of a class  II. Sum of the complexities of the methods of a class  III. Number of other classes to which a class is coupled  IV. Length of the longest path from a class to the root of the inheritance tree

(1) A-II, B-IV, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-IV, B-II, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(1)** — The Chidamber-Kemerer suite also includes RFC and LCOM.

</details>

**Q10.** `Medium`  
In the CK metrics suite, LCOM measures

(1) lines of code per method  
(2) lack of cohesion among the methods of a class  
(3) the depth of inheritance  
(4) the number of classes  

<details><summary>Answer</summary>

**(2)** — A high LCOM suggests that the class should be split.

</details>

**Q11.** `Medium`  
The multiplicity 1..\* on an association end means

(1) exactly one  
(2) zero or one  
(3) one or more  
(4) zero or more  

<details><summary>Answer</summary>

**(3)** — 0..\* (or \*) means zero or more.

</details>

**Q12.** `Medium`  
Given below are two statements.  
Statement I: Inheritance always reduces coupling between a subclass and its superclass.  
Statement II: Polymorphism allows the same message to produce different behaviour depending on the receiving object's class.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Inheritance creates strong coupling between a subclass and its superclass.

</details>

**Q13.** `Medium`  
In UML, an "include" relationship between use cases is drawn as

(1) a solid line  
(2) a dashed arrow labelled «include» from the base use case to the included use case  
(3) a filled diamond  
(4) a hollow triangle  

<details><summary>Answer</summary>

**(2)** — An «extend» arrow points from the extending use case to the base use case.

</details>

**Q14.** `Medium`  
The Object Modeling Technique (OMT) was developed by

(1) James Rumbaugh  
(2) Ivar Jacobson  
(3) Peter Coad  
(4) Grady Booch  

<details><summary>Answer</summary>

**(1)** — Booch, Rumbaugh and Jacobson later unified their methods into UML.

</details>

**Q15.** `Medium`  
An activity diagram is most similar to

(1) a flowchart, showing the flow of activities, decisions and concurrency  
(2) an ER diagram  
(3) a class diagram  
(4) a deployment diagram  

<details><summary>Answer</summary>

**(1)** — Swimlanes show which actor or class is responsible for each activity.

</details>

**Q16.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A high depth of inheritance tree (DIT) makes a class harder to understand and test.  
Reason R: Deeper classes inherit more methods, so their behaviour is harder to predict.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — But a deeper hierarchy also indicates more reuse.

</details>

**Q17.** `Medium`  
Which UML diagram shows the organisation of model elements into groups and their dependencies?

(1) Package diagram  
(2) State diagram  
(3) Timing diagram  
(4) Sequence diagram  

<details><summary>Answer</summary>

**(1)** — Packages group related classes.

</details>

**Q18.** `Medium`  
In object-oriented analysis, a class responsible for coordinating a use case's steps is called a

(1) control class  
(2) entity class  
(3) boundary class  
(4) utility class  

<details><summary>Answer</summary>

**(1)** — Boundary classes handle interaction with actors; entity classes hold persistent information.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: Abstract classes cannot be instantiated directly.  
Statement II: An interface in UML is shown with the stereotype «interface» or as a lollipop symbol.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard UML conventions.

</details>

**Q20.** `Low`  
UML is standardised by the

(1) W3C  
(2) IEEE  
(3) Object Management Group (OMG)  
(4) ISO only  

<details><summary>Answer</summary>

**(3)** — The OMG adopted UML in 1997.

</details>

**Q21.** `Medium`  
Given below are two statements.  
Statement I: A sequence diagram shows the static structure of classes and their attributes.  
Statement II: A state machine diagram is usually drawn for every class, regardless of its behaviour.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Sequence diagrams show interactions over time; state diagrams are drawn only for classes with significant state-dependent behaviour.

</details>
