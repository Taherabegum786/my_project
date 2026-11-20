# Set 3 — Relational Model (keys, integrity constraints, Codd's rules, relational algebra and relational calculus)

**47 questions** — High: 19, Medium: 27, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Relation R has 10 tuples and 3 attributes, and relation S has 20 tuples and 4 attributes. The Cartesian product R × S has

(1) 200 tuples and 12 attributes  
(2) 30 tuples and 12 attributes  
(3) 200 tuples and 7 attributes  
(4) 30 tuples and 7 attributes  

<details><summary>Answer</summary>

**(3)** — The number of tuples is 10 × 20 = 200, and the degree is 3 + 4 = 7.

</details>

**Q2.** `High`  
Relations R(A, B) with 10 tuples and S(B, C) with 20 tuples are joined by natural join. The maximum and minimum possible numbers of tuples in R ⋈ S are

(1) 200 and 10  
(2) 200 and 0  
(3) 30 and 0  
(4) 20 and 10  

<details><summary>Answer</summary>

**(2)** — If every tuple has the same B value the result is 10 × 20; if no B values match it is empty.

</details>

**Q3.** `High`  
In R(A, B) with 10 tuples, B is a foreign key, not allowed to be null, referencing the primary key B of S(B, C), which has 20 tuples. The number of tuples in R ⋈ S is

(1) 30  
(2) 200  
(3) 20  
(4) 10  

<details><summary>Answer</summary>

**(4)** — Each R tuple matches exactly one S tuple, because B is the key of S and referential integrity holds.

</details>

**Q4.** `High`  
Relations r(A, B) = {(1, 2), (2, 3), (3, 4)} and s(B, C) = {(2, 5), (3, 6), (3, 7), (9, 9)}. The number of tuples in the natural join r ⋈ s is

(1) 3  
(2) 5  
(3) 4  
(4) 2  

<details><summary>Answer</summary>

**(1)** — (1, 2, 5), (2, 3, 6) and (2, 3, 7); (3, 4) has no matching B in s.

</details>

**Q5.** `Medium`  
Relations r(A, B) = {(1, 2), (2, 3), (3, 4)} and s(B, C) = {(2, 5), (3, 6), (3, 7), (9, 9)}. The numbers of tuples in the left outer join and the full outer join of r and s on B are respectively

(1) 4 and 4  
(2) 3 and 5  
(3) 3 and 4  
(4) 4 and 5  

<details><summary>Answer</summary>

**(4)** — Left outer join adds (3, 4, NULL); full outer join also adds (NULL, 9, 9).

</details>

**Q6.** `Medium`  
Relations r(A, B) = {(1, 2), (2, 3), (3, 4)} and s(B, C) = {(2, 5), (3, 6), (3, 7), (9, 9)}. The number of tuples in the semijoin r ⋉ s (tuples of r that join with some tuple of s) is

(1) 1  
(2) 3  
(3) 2  
(4) 4  

<details><summary>Answer</summary>

**(3)** — (1, 2) and (2, 3) have matches in s; a semijoin never duplicates r tuples.

</details>

**Q7.** `High`  
Relation Enrolled(Student, Course) contains (s1, c1), (s1, c2), (s2, c1), (s3, c1), (s3, c2), (s3, c3), and Course(Course) contains c1 and c2. The result of Enrolled ÷ Course is

(1) {s1, s3}  
(2) {s3}  
(3) {s1}  
(4) {s1, s2, s3}  

<details><summary>Answer</summary>

**(1)** — Division returns the students enrolled in every course of Course: s1 and s3 (s2 lacks c2).

</details>

**Q8.** `High`  
The relational algebra division R(A, B) ÷ S(B) can be expressed using basic operators as

(1) π_A(R × S) − R  
(2) π_A(R) ∩ π_A(S)  
(3) π_A(R − S)  
(4) π_A(R) − π_A((π_A(R) × S) − R)  

<details><summary>Answer</summary>

**(4)** — (π_A(R) × S) − R gives the missing combinations; their A values are removed from π_A(R).

</details>

**Q9.** `High`  
Which of the following is the set of fundamental (basic) operations of relational algebra?

(1) Selection, projection, join, intersection and division  
(2) Union, intersection, join and division  
(3) Selection, projection, union, set difference, Cartesian product and rename  
(4) Selection, projection, aggregation and sorting  

<details><summary>Answer</summary>

**(3)** — Intersection, join and division can be derived from the basic operations.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Operation): A. σ  B. π  C. ρ  D. ÷  
List II (Meaning): I. Rename  II. Project  III. Select  IV. Division

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-I, C-II, D-IV  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(3)** — σ selects tuples, π selects attributes, ρ renames and ÷ divides.

</details>

**Q11.** `Medium`  
R ∩ S can be expressed using only set difference as

(1) R − (S − R)  
(2) R − (R − S)  
(3) (R − S) − S  
(4) S − R  

<details><summary>Answer</summary>

**(2)** — Removing from R the tuples that are not in S leaves exactly R ∩ S.

</details>

**Q12.** `High`  
Relations R and S are union-compatible with m and n tuples respectively (m ≥ n). The numbers of tuples in R ∪ S lie in the range

(1) n to m  
(2) m × n  
(3) 0 to m + n  
(4) m to m + n  

<details><summary>Answer</summary>

**(4)** — At least the larger relation, and at most every tuple of both if there are no duplicates.

</details>

**Q13.** `Medium`  
Two relations are union-compatible if they have

(1) the same degree and corresponding attributes have the same domains  
(2) at least one common attribute  
(3) the same primary key  
(4) the same number of tuples  

<details><summary>Answer</summary>

**(1)** — Union, intersection and difference require union compatibility.

</details>

**Q14.** `Medium`  
Given below are two statements.  
Statement I: Selection is commutative: σ_c1(σ_c2(R)) = σ_c2(σ_c1(R)).  
Statement II: A cascade of projections π_L1(π_L2(R)) can be replaced by π_L2(R) when L1 ⊆ L2.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The cascade of projections is equivalent to the outermost projection π_L1(R), not π_L2(R).

</details>

**Q15.** `High`  
Match List I with List II.  
List I (Key): A. Superkey  B. Candidate key  C. Primary key  D. Foreign key  
List II (Definition): I. A minimal superkey  II. A set of attributes that uniquely identifies a tuple  III. Attributes referring to the primary key of another (or the same) relation  IV. The candidate key chosen by the designer to identify tuples

(1) A-II, B-I, C-III, D-IV  
(2) A-I, B-II, C-IV, D-III  
(3) A-II, B-I, C-IV, D-III  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — Every candidate key is a superkey, but not conversely.

</details>

**Q16.** `High`  
A relation R(A, B, C, D, E) has A as its only candidate key. The number of superkeys of R is

(1) 5  
(2) 15  
(3) 32  
(4) 16  

<details><summary>Answer</summary>

**(4)** — Any superset of {A}: 2^4 = 16.

</details>

**Q17.** `High`  
A relation R(A, B, C, D, E) has exactly two candidate keys, A and B. The number of superkeys of R is

(1) 16  
(2) 24  
(3) 28  
(4) 32  

<details><summary>Answer</summary>

**(2)** — Supersets of A: 16; supersets of B: 16; supersets of both A and B: 8; total 16 + 16 − 8 = 24.

</details>

**Q18.** `Medium`  
A relation R(A, B, C, D, E) has exactly two candidate keys, AB and CD. The number of superkeys of R is

(1) 18  
(2) 16  
(3) 14  
(4) 28  

<details><summary>Answer</summary>

**(3)** — Supersets of AB: 8; of CD: 8; of ABCD: 2; total 8 + 8 − 2 = 14.

</details>

**Q19.** `High`  
Match List I with List II.  
List I (Integrity constraint): A. Entity integrity  B. Referential integrity  C. Key constraint  D. Domain constraint  
List II (Rule): I. Values of an attribute must be atomic values from its domain  II. No primary-key value can be NULL  III. No two tuples can have the same value for a candidate key  IV. A foreign-key value must match an existing primary-key value or be NULL

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(3)** — The basic relational constraints.

</details>

**Q20.** `High`  
Which of the following update operations on a referenced relation can violate referential integrity?  
A. Insertion of a tuple into the referenced relation  B. Deletion of a tuple from the referenced relation  C. Modification of the primary key of a referenced tuple  
Choose the correct answer from the options given below:

(1) A only  
(2) A, B and C  
(3) A and B only  
(4) B and C only  

<details><summary>Answer</summary>

**(4)** — Inserting a new referenced tuple cannot leave any foreign key dangling.

</details>

**Q21.** `Medium`  
Which constraints can be violated by an insert operation on a relation?  
A. Domain constraint  B. Key constraint  C. Entity integrity  D. Referential integrity  
Choose the correct answer from the options given below:

(1) A, C and D only  
(2) B and C only  
(3) A and B only  
(4) A, B, C and D  

<details><summary>Answer</summary>

**(4)** — An insert can violate all four kinds of constraints.

</details>

**Q22.** `Medium`  
When a referenced tuple is deleted, the option ON DELETE CASCADE

(1) deletes the referencing tuples as well  
(2) sets them to a default value  
(3) sets the foreign keys of referencing tuples to NULL  
(4) rejects the deletion  

<details><summary>Answer</summary>

**(1)** — SET NULL and SET DEFAULT are alternatives; RESTRICT or NO ACTION rejects the deletion.

</details>

**Q23.** `High`  
Match List I with List II.  
List I (Codd's rule): A. Rule 1  B. Rule 2  C. Rule 3  D. Rule 4  
List II (Name): I. Dynamic online catalog based on the relational model  II. Guaranteed access rule  III. Information rule  IV. Systematic treatment of null values

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(1)** — Rule 1: all information is in tables; Rule 2: every value is reachable by table, primary key and column; Rule 3: nulls; Rule 4: the catalog is itself relational.

</details>

**Q24.** `Medium`  
Match List I with List II.  
List I (Codd's rule): A. Rule 8  B. Rule 9  C. Rule 10  D. Rule 12  
List II (Name): I. Non-subversion rule  II. Physical data independence  III. Logical data independence  IV. Integrity independence

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-III, C-I, D-IV  
(3) A-II, B-IV, C-III, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(1)** — Rule 11 is distribution independence, and Rule 0 is the foundation rule.

</details>

**Q25.** `Medium`  
Codd's rules, including Rule 0 (the foundation rule), number

(1) 10  
(2) 12  
(3) 13  
(4) 15  

<details><summary>Answer</summary>

**(3)** — Rules 0 to 12 are usually called "Codd's twelve rules".

</details>

**Q26.** `Medium`  
Codd's non-subversion rule states that

(1) nulls must be supported  
(2) views must be updatable  
(3) the catalog must be relational  
(4) a low-level (record-at-a-time) language must not be able to bypass the integrity rules expressed in the high-level relational language  

<details><summary>Answer</summary>

**(4)** — This is Rule 12.

</details>

**Q27.** `High`  
Given below are two statements.  
Statement I: In the relational model, the tuples of a relation have no inherent order.  
Statement II: In the relational model, a relation may contain duplicate tuples.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A relation is a set of tuples, so duplicates are not allowed (SQL tables, however, are multisets).

</details>

**Q28.** `Medium`  
The degree and the cardinality of a relation are respectively

(1) the number of attributes and the number of tuples  
(2) the number of tuples and the number of attributes  
(3) the number of keys and the number of tuples  
(4) the number of tables and the number of rows  

<details><summary>Answer</summary>

**(1)** — A relation with 5 columns and 100 rows has degree 5 and cardinality 100.

</details>

**Q29.** `High`  
Given below are two statements.  
Statement I: Tuple relational calculus is a non-procedural query language.  
Statement II: Safe expressions of tuple relational calculus, safe expressions of domain relational calculus and basic relational algebra have the same expressive power.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This equivalence is the basis of Codd's notion of relational completeness.

</details>

**Q30.** `Medium`  
In tuple relational calculus, the expression {t | t ∈ Employee ∧ t.salary > 50000} returns

(1) the number of employees with salary greater than 50000  
(2) all employee tuples with salary greater than 50000  
(3) the salary attribute of all employees  
(4) an empty set always  

<details><summary>Answer</summary>

**(2)** — t ranges over Employee tuples that satisfy the condition.

</details>

**Q31.** `Medium`  
A relational calculus expression is called unsafe if it

(1) uses the ∀ quantifier  
(2) can produce an infinite result, such as {t | ¬(t ∈ R)}  
(3) contains a join  
(4) uses more than one relation  

<details><summary>Answer</summary>

**(2)** — Safe expressions restrict results to values in the domain of the expression.

</details>

**Q32.** `Medium`  
The relational calculus query {t | ∃s ∈ R (t[A] = s[A])} corresponds to the relational algebra expression

(1) R × R  
(2) π_A(R)  
(3) R ÷ A  
(4) σ_A(R)  

<details><summary>Answer</summary>

**(2)** — It returns the A values of tuples in R.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: Domain relational calculus uses variables that range over tuples.  
Statement II: Query-By-Example (QBE) is based on tuple relational calculus.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — DRC variables range over attribute domains, and QBE is based on domain relational calculus.

</details>

**Q34.** `Medium`  
A query asking for "students who have taken all courses offered by the CS department" is most naturally expressed in relational algebra using

(1) outer join  
(2) division  
(3) Cartesian product only  
(4) union  

<details><summary>Answer</summary>

**(2)** — "For all" queries correspond to division (or to ∀ in relational calculus).

</details>

**Q35.** `Medium`  
Which of the following relational algebra operations is NOT commutative?

(1) Natural join  
(2) Union  
(3) Intersection  
(4) Set difference  

<details><summary>Answer</summary>

**(4)** — R − S is generally different from S − R.

</details>

**Q36.** `Medium`  
For relations R(A, B) and S(B, C), the theta join R ⋈ (R.B = S.B) S differs from the natural join in that the theta (equi) join

(1) always returns more tuples  
(2) keeps both B columns in the result  
(3) removes duplicate columns  
(4) cannot be expressed with Cartesian product  

<details><summary>Answer</summary>

**(2)** — Natural join is an equijoin followed by removal of the duplicate attribute.

</details>

**Q37.** `High`  
The number of tuples in σ_c(R), where R has n tuples, lies in the range

(1) 0 to n  
(2) 1 to n  
(3) n to 2n  
(4) exactly n  

<details><summary>Answer</summary>

**(1)** — Selection returns the tuples satisfying c, which may be none or all.

</details>

**Q38.** `Medium`  
Projection π_A(R) on a relation R with n tuples (set semantics, n ≥ 1) returns

(1) more than n tuples  
(2) 0 tuples always  
(3) between 1 and n tuples  
(4) exactly n tuples  

<details><summary>Answer</summary>

**(3)** — Duplicates are removed, so the number of distinct A values ranges from 1 to n.

</details>

**Q39.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A foreign key may contain NULL values.  
Reason R: Entity integrity states that no primary-key value can be NULL.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but R concerns primary keys; a NULL foreign key is allowed because referential integrity requires a match only for non-null values.

</details>

**Q40.** `Medium`  
Given below are two statements.  
Statement I: A primary key can contain NULL values if the relation is small.  
Statement II: A relation can have only one candidate key.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Primary keys never allow NULLs, and a relation can have several candidate keys.

</details>

**Q41.** `Medium`  
The outer join operations were introduced into relational algebra in order to

(1) keep tuples that have no matching tuple in the other relation, padding with NULLs  
(2) remove duplicate tuples  
(3) perform division  
(4) reduce the size of results  

<details><summary>Answer</summary>

**(1)** — Left, right and full outer joins differ in which side's unmatched tuples are kept.

</details>

**Q42.** `Medium`  
The grouping operator γ in extended relational algebra, written γ_G,F(R), groups the tuples of R by attributes G and

(1) applies aggregate functions F such as SUM, COUNT and AVG to each group  
(2) sorts them  
(3) removes all NULLs  
(4) projects only G  

<details><summary>Answer</summary>

**(1)** — It corresponds to GROUP BY with aggregate functions in SQL.

</details>

**Q43.** `Low`  
The relational model was proposed by

(1) Peter Chen  
(2) Ronald Fagin  
(3) E. F. Codd  
(4) C. J. Date  

<details><summary>Answer</summary>

**(3)** — Codd's 1970 paper "A Relational Model of Data for Large Shared Data Banks".

</details>

**Q44.** `Medium`  
Arrange the following query languages in order of the year they were proposed or developed.  
A. SQL (SEQUEL)  B. Relational algebra  C. Query-By-Example

(1) C, B, A  
(2) B, A, C  
(3) B, C, A  
(4) A, B, C  

<details><summary>Answer</summary>

**(2)** — Relational algebra (Codd, 1970), SEQUEL (1974), QBE (1975–77).

</details>

**Q45.** `Medium`  
Given relation R(A, B, C) with tuples (1, 2, 3), (1, 2, 4), (2, 2, 3), the number of tuples in π_A,B(R) is

(1) 1  
(2) 6  
(3) 2  
(4) 3  

<details><summary>Answer</summary>

**(3)** — (1, 2) and (2, 2): the duplicate (1, 2) is removed.

</details>

**Q46.** `Medium`  
Which relational algebra expression returns the names of employees who work in department 5, for Employee(Eno, Name, Dno)?

(1) π_Dno=5(σ_Name(Employee))  
(2) π_Name(σ_Dno=5(Employee))  
(3) σ_Dno=5(π_Name(Employee))  
(4) σ_Name(Employee) × Dno  

<details><summary>Answer</summary>

**(2)** — Selection must be applied before projecting away Dno.

</details>

**Q47.** `Medium`  
Given below are two statements.  
Statement I: The rename operator ρ is used to delete attributes from a relation.  
Statement II: The natural join of two relations with no common attributes is always empty.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — ρ renames relations or attributes (projection removes attributes), and a natural join with no common attributes equals the Cartesian product.

</details>
