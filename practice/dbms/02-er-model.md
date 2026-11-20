# Set 2 — Entity-Relationship Model (entities, attributes, relationships, constraints, EER and ER-to-relational mapping)

**38 questions** — High: 17, Medium: 20, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (ER notation): A. Double rectangle  B. Double ellipse  C. Dashed ellipse  D. Double diamond  
List II (Meaning): I. Derived attribute  II. Weak entity type  III. Identifying relationship type  IV. Multivalued attribute

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(2)** — Chen notation as used by Elmasri and Navathe.

</details>

**Q2.** `High`  
A weak entity type is one that

(1) has only derived attributes  
(2) does not have a key attribute of its own and is identified through its relationship with an owner entity type  
(3) has no attributes  
(4) participates in no relationship  

<details><summary>Answer</summary>

**(2)** — A weak entity has a partial key (discriminator) and total participation in its identifying relationship.

</details>

**Q3.** `High`  
The partial key of a weak entity type is shown in an ER diagram with

(1) no underline  
(2) a dashed (dotted) underline  
(3) a double underline  
(4) a solid underline  

<details><summary>Answer</summary>

**(2)** — The key of the weak entity is the owner's key plus the partial key.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: A weak entity type always has total participation in its identifying relationship.  
Statement II: An owner entity type must itself be a weak entity type.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The owner is normally a strong entity type (although a weak entity can, in turn, own another weak entity).

</details>

**Q5.** `High`  
An entity set E1 has attributes a1 (key) and a2; E2 has b1 (key) and b2. A many-to-many relationship R between them has attribute r1. The minimum number of tables required in the relational model is

(1) 4  
(2) 1  
(3) 2  
(4) 3  

<details><summary>Answer</summary>

**(4)** — One table for each entity set and one for R, with primary key (a1, b1).

</details>

**Q6.** `High`  
Entity sets E1 and E2 are connected by a one-to-many relationship R (one E1 to many E2), and R has no attributes of its own. The minimum number of tables required is

(1) 3  
(2) 4  
(3) 2  
(4) 1  

<details><summary>Answer</summary>

**(3)** — The key of E1 is added as a foreign key to the table of E2, the "many" side.

</details>

**Q7.** `High`  
Entity sets E1 and E2 are connected by a one-to-one relationship R, and both have total participation in R. The minimum number of tables required is

(1) 3  
(2) 2  
(3) 4  
(4) 1  

<details><summary>Answer</summary>

**(4)** — With total participation on both sides, both entity sets and the relationship can be merged into a single table.

</details>

**Q8.** `High`  
An entity set E has a key attribute k, a simple attribute a and a multivalued attribute m. The minimum number of tables needed to represent E in first normal form is

(1) 1  
(2) 2  
(3) 4  
(4) 3  

<details><summary>Answer</summary>

**(2)** — The multivalued attribute needs its own table with key (k, m).

</details>

**Q9.** `Medium`  
Entity set E1 (key a1, multivalued attribute a2) is in a one-to-many relationship R with entity set E2 (key b1); E2 is on the many side. The minimum number of tables in 1NF is

(1) 4  
(2) 3  
(3) 2  
(4) 5  

<details><summary>Answer</summary>

**(2)** — E1, a table for the multivalued attribute a2, and E2 with a1 as a foreign key: 3 tables.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Attribute type): A. Composite attribute  B. Multivalued attribute  C. Derived attribute  D. Key attribute  
List II (Example): I. Age, computed from Date_of_birth  II. Name, made of First_name and Last_name  III. Roll_no, which uniquely identifies a student  IV. Phone_numbers of a person

(1) A-II, B-IV, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(1)** — Standard attribute types in the ER model.

</details>

**Q11.** `High`  
In an ER diagram, total participation of an entity type in a relationship type is shown by

(1) a double line  
(2) an arrow  
(3) a dashed line  
(4) a single line  

<details><summary>Answer</summary>

**(1)** — Total participation (existence dependency) means every entity must take part in at least one relationship instance.

</details>

**Q12.** `Medium`  
The degree of a relationship type is

(1) the number of participating entity types  
(2) the number of its attributes  
(3) the number of tuples in it  
(4) its cardinality ratio  

<details><summary>Answer</summary>

**(1)** — Unary (recursive), binary and ternary relationships have degrees 1, 2 and 3.

</details>

**Q13.** `Medium`  
A relationship type in which the same entity type participates more than once in different roles, such as Supervises between employees, is called a

(1) ternary relationship  
(2) identifying relationship  
(3) recursive (unary) relationship  
(4) weak relationship  

<details><summary>Answer</summary>

**(3)** — Role names distinguish the participations, for example supervisor and supervisee.

</details>

**Q14.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A ternary relationship cannot always be replaced by three binary relationships without loss of information.  
Reason R: The three binary relationships may not capture which combinations of the three entities actually occur together.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — For example Supplies(Supplier, Part, Project) differs from Can_supply, Uses and Supplies_to taken together.

</details>

**Q15.** `Medium`  
In the (min, max) notation, the constraint (0, N) for an entity type in a relationship means

(1) every entity must participate at least N times  
(2) an entity participates exactly once  
(3) participation is partial and an entity can participate any number of times  
(4) participation is total  

<details><summary>Answer</summary>

**(3)** — min = 0 means partial participation; min ≥ 1 means total participation.

</details>

**Q16.** `High`  
Match List I with List II.  
List I (EER constraint): A. Disjointness constraint  B. Overlapping constraint  C. Total specialization  D. Partial specialization  
List II (Meaning): I. Every superclass entity must belong to some subclass  II. An entity may be a member of at most one subclass  III. An entity may belong to more than one subclass  IV. A superclass entity need not belong to any subclass

(1) A-II, B-I, C-III, D-IV  
(2) A-III, B-II, C-I, D-IV  
(3) A-II, B-III, C-I, D-IV  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(3)** — Constraints on specialization and generalization in the EER model.

</details>

**Q17.** `High`  
Given below are two statements.  
Statement I: Specialization is a top-down process of defining subclasses of an entity type.  
Statement II: Generalization is a bottom-up process of combining several entity types into a higher-level superclass.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — They are inverse processes of each other.

</details>

**Q18.** `Medium`  
In the EER model, a subclass inherits from its superclass

(1) only its relationships  
(2) only its key attribute  
(3) all attributes and relationships of the superclass  
(4) nothing  

<details><summary>Answer</summary>

**(3)** — Attribute and relationship inheritance is the key property of the IS-A hierarchy.

</details>

**Q19.** `Medium`  
A subclass that has more than one superclass, for example Teaching_assistant as a subclass of both Employee and Student, is called a

(1) aggregate  
(2) shared subclass (multiple inheritance)  
(3) union type  
(4) weak subclass  

<details><summary>Answer</summary>

**(2)** — A union type (category) is a subclass of a union of distinct superclasses with different keys.

</details>

**Q20.** `Medium`  
A category (union type) in the EER model is

(1) a set of weak entities  
(2) a subclass of the union of two or more superclasses of different entity types  
(3) a composite attribute  
(4) a ternary relationship  

<details><summary>Answer</summary>

**(2)** — For example Owner is a category of Person, Bank and Company.

</details>

**Q21.** `High`  
Aggregation in the ER model is used to

(1) represent multivalued attributes  
(2) define derived attributes  
(3) treat a relationship set together with its participating entity sets as a higher-level entity that can take part in other relationships  
(4) combine entity types into one table  

<details><summary>Answer</summary>

**(3)** — It is used to express relationships among relationships.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: In a one-to-many relationship from Department to Employee, a department can have at most one employee.  
Statement II: The cardinality ratio of a binary relationship can be 1:1, 1:N, N:1 or M:N.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — In 1:N from Department to Employee, a department can have many employees, but each employee works in at most one department.

</details>

**Q23.** `High`  
In mapping a one-to-one relationship between E1 and E2 to tables when only E2 has total participation, the preferred approach is to

(1) merge all attributes into one table regardless of participation  
(2) include the primary key of E2 in E1  
(3) include the primary key of E1 as a foreign key in the table for E2  
(4) create a separate table for the relationship  

<details><summary>Answer</summary>

**(3)** — Placing the foreign key on the side with total participation avoids NULLs.

</details>

**Q24.** `Medium`  
In mapping an EER specialization to relations, which option creates relations only for the subclasses, each including the attributes of the superclass?

(1) Single relation with multiple type attributes  
(2) Single relation with one type attribute  
(3) Multiple relations, subclass relations only  
(4) Multiple relations, superclass and subclasses  

<details><summary>Answer</summary>

**(3)** — This option works best for total, disjoint specializations.

</details>

**Q25.** `Medium`  
Which of the following is the correct ER-to-relational mapping of a multivalued attribute Skill of entity Employee (key Eno)?

(1) Create a relation Emp_skill(Eno, Skill) with primary key (Eno, Skill)  
(2) Add Skill as a column of Employee  
(3) Ignore the attribute  
(4) Create a relation Emp_skill(Skill) with primary key Skill  

<details><summary>Answer</summary>

**(1)** — Each value of the multivalued attribute becomes a separate tuple.

</details>

**Q26.** `Medium`  
A weak entity set Dependent (partial key Dname) is owned by Employee (key Eno). The primary key of the relation for Dependent is

(1) (Eno, Dname)  
(2) Eno  
(3) Dname  
(4) a new surrogate key only  

<details><summary>Answer</summary>

**(1)** — The key is the owner's key plus the partial key, and Eno is also a foreign key.

</details>

**Q27.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In a one-to-many relationship, the attributes of the relationship can be moved to the entity type on the "many" side.  
Reason R: Each entity on the "many" side participates in at most one relationship instance.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Hence a relationship attribute such as Start_date can be stored with the employee.

</details>

**Q28.** `Medium`  
An attribute whose value can be computed from other attributes, such as Number_of_employees of a department, is called a

(1) stored attribute  
(2) key attribute  
(3) composite attribute  
(4) derived attribute  

<details><summary>Answer</summary>

**(4)** — Derived attributes are drawn as dashed ellipses.

</details>

**Q29.** `Medium`  
An attribute that can have a null value because it does not apply to some entities, for example Apartment_number for people living in houses, illustrates

(1) the multivalued property  
(2) a derived attribute  
(3) a composite key  
(4) a null value meaning "not applicable"  

<details><summary>Answer</summary>

**(4)** — Nulls can mean "not applicable" or "unknown".

</details>

**Q30.** `Medium`  
In UML class diagrams used for conceptual design, a relationship type is represented as

(1) a class  
(2) an association  
(3) a package  
(4) a generalization arrow  

<details><summary>Answer</summary>

**(2)** — Multiplicities such as 0..* and 1..1 express cardinality and participation.

</details>

**Q31.** `Medium`  
Who proposed the Entity-Relationship model?

(1) C. J. Date  
(2) E. F. Codd  
(3) Raymond Boyce  
(4) Peter Chen  

<details><summary>Answer</summary>

**(4)** — Chen published the ER model in 1976.

</details>

**Q32.** `Medium`  
How many relations are needed, at minimum, to represent a ternary relationship type R among entity types E1, E2 and E3 (each with its own key) when R is many-to-many-to-many?

(1) 1  
(2) 4  
(3) 6  
(4) 3  

<details><summary>Answer</summary>

**(2)** — One relation for each entity type and one for R, whose key combines the three foreign keys.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: A key attribute of an entity type must be composite.  
Statement II: An entity type can have more than one key attribute.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A key may be simple or composite, and an entity type can have several candidate keys (for example Vehicle_id and Registration).

</details>

**Q34.** `Medium`  
An entity set Employee has a recursive one-to-many relationship Manages (each employee has at most one manager). The minimum number of tables required is

(1) 1  
(2) 3  
(3) 2  
(4) 0  

<details><summary>Answer</summary>

**(1)** — A foreign key Manager_id referencing the same table represents the relationship.

</details>

**Q35.** `High`  
Match List I with List II.  
List I (Concept): A. Entity type  B. Entity set  C. Relationship type  D. Value set (domain)  
List II (Meaning): I. Set of allowed values for an attribute  II. Collection of all entities of a particular entity type at a point in time  III. Defines a set of associations among entities of given types  IV. Collection of entities that have the same attributes

(1) A-IV, B-III, C-II, D-I  
(2) A-IV, B-II, C-I, D-III  
(3) A-IV, B-II, C-III, D-I  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(3)** — Basic ER terminology.

</details>

**Q36.** `Medium`  
Given below are two statements.  
Statement I: In a ternary relationship, a cardinality constraint on one participating entity cannot always be expressed using binary relationships.  
Statement II: An identifying relationship connects a weak entity type to its owner.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both statements are standard results.

</details>

**Q37.** `Low`  
Which of the following ER notations represents a relationship type?

(1) Diamond  
(2) Rectangle  
(3) Line only  
(4) Ellipse  

<details><summary>Answer</summary>

**(1)** — Rectangles are entity types and ellipses are attributes.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: An ER diagram can directly represent functional dependencies among attributes.  
Statement II: The ER model is a representational (implementation) data model.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — The ER model is a conceptual (high-level) model, and it does not express arbitrary functional dependencies.

</details>
