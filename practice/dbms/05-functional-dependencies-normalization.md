# Set 5 — Functional Dependencies and Normalization (closure, keys, Armstrong's axioms, minimal cover, 1NF–5NF, decomposition)

**55 questions** — High: 27, Medium: 28, Low: 0

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
For the relation R(A, B, C, D, E) with F = {A → BC, CD → E, B → D, E → A}, the closure B⁺ is

(1) {A, B, C, D, E}  
(2) {B, C, D}  
(3) {B, D}  
(4) {B}  

<details><summary>Answer</summary>

**(3)** — B → D, and no other dependency has its left side contained in {B, D}.

</details>

**Q2.** `High`  
For the relation R(A, B, C, D, E) with F = {A → BC, CD → E, B → D, E → A}, the candidate keys are

(1) A, B, C and D  
(2) A and E only  
(3) BC and CD only  
(4) A, E, BC and CD  

<details><summary>Answer</summary>

**(4)** — A⁺ = ABCDE; E → A; BC → BCD → E; CD → E → A. No single attribute other than A and E is a key.

</details>

**Q3.** `High`  
For the relation R(A, B, C, G, H, I) with F = {A → B, A → C, CG → H, CG → I, B → H}, the closure (AG)⁺ is

(1) {A, B, C, G, H, I}  
(2) {A, G, H, I}  
(3) {A, B, C, G, H}  
(4) {A, B, C, G}  

<details><summary>Answer</summary>

**(1)** — A gives B and C; CG then gives H and I. So AG is a superkey.

</details>

**Q4.** `High`  
Match List I with List II.  
List I (Armstrong's axiom or inference rule): A. Reflexivity  B. Augmentation  C. Transitivity  D. Pseudotransitivity  
List II (Rule): I. If X → Y and WY → Z, then WX → Z  II. If X → Y and Y → Z, then X → Z  III. If Y ⊆ X, then X → Y  IV. If X → Y, then XZ → YZ

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-IV, C-I, D-II  
(4) A-IV, B-III, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — Union, decomposition and pseudotransitivity can be derived from the three axioms.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: Armstrong's axioms are sound: they generate only functional dependencies that actually hold.  
Statement II: Armstrong's axioms are complete: repeated application generates all dependencies in F⁺.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Soundness and completeness of Armstrong's axioms.

</details>

**Q6.** `High`  
Which of the following inference rules is NOT valid for functional dependencies?

(1) If X → YZ, then X → Y  
(2) If X → Y and X → Z, then X → YZ  
(3) If XY → Z, then X → Z  
(4) If X → Y and YW → Z, then XW → Z  

<details><summary>Answer</summary>

**(3)** — A dependency cannot be weakened on the left: XY → Z does not imply X → Z.

</details>

**Q7.** `High`  
A canonical (minimal) cover of F = {A → BC, B → C, A → B, AB → C} is

(1) {A → B, AB → C}  
(2) {A → B, B → C}  
(3) {A → BC, B → C}  
(4) {A → C, B → C}  

<details><summary>Answer</summary>

**(2)** — Combine A → BC and A → B; A is extraneous in AB → C; C is extraneous in A → BC because A → B → C.

</details>

**Q8.** `Medium`  
Which of the following FD sets is equivalent to F = {A → C, AC → D, E → AD, E → H}?

(1) {A → D, E → H}  
(2) {AC → D, E → H}  
(3) {A → C, E → D}  
(4) {A → CD, E → AH}  

<details><summary>Answer</summary>

**(4)** — A → C and AC → D give A → CD; E → AD and A → C give everything in F, and E → AH plus A → CD gives back E → AD.

</details>

**Q9.** `High`  
The relation R(A, B, C, D, E) with F = {A → B, B → C, C → D, D → E} is in which highest normal form?

(1) 3NF  
(2) 2NF  
(3) 1NF  
(4) BCNF  

<details><summary>Answer</summary>

**(2)** — The only key is A (a single attribute), so there are no partial dependencies, but B → C is transitive.

</details>

**Q10.** `High`  
The relation R(A, B, C, D) with F = {AB → C, B → D} is in which highest normal form?

(1) 2NF  
(2) 3NF  
(3) 1NF  
(4) BCNF  

<details><summary>Answer</summary>

**(3)** — The key is AB, and B → D is a partial dependency of the non-prime attribute D.

</details>

**Q11.** `High`  
The relation R(A, B, C) with F = {AB → C, C → A} is in which highest normal form?

(1) BCNF  
(2) 1NF  
(3) 2NF  
(4) 3NF  

<details><summary>Answer</summary>

**(4)** — Keys are AB and BC. C → A violates BCNF, but A is prime, so R is in 3NF.

</details>

**Q12.** `High`  
The relation R(A, B, C, D) with F = {A → B, B → C, C → D, D → A} is in which highest normal form?

(1) 2NF  
(2) 1NF  
(3) 3NF  
(4) BCNF  

<details><summary>Answer</summary>

**(4)** — Every attribute is a candidate key, so every determinant is a superkey.

</details>

**Q13.** `High`  
The relation R(A, B, C, D, E, F) with F = {A → B, B → C, C → D, D → A, E → F} has how many candidate keys?

(1) 2  
(2) 1  
(3) 6  
(4) 4  

<details><summary>Answer</summary>

**(4)** — E must be in every key; AE, BE, CE and DE are the candidate keys.

</details>

**Q14.** `Medium`  
The relation R(A, B, C, D, E, F) with F = {A → B, B → C, C → D, D → A, E → F} is in which highest normal form?

(1) BCNF  
(2) 1NF  
(3) 2NF  
(4) 3NF  

<details><summary>Answer</summary>

**(2)** — E → F is a partial dependency: E is part of every key and F is non-prime.

</details>

**Q15.** `High`  
The relation R(A, B, C, D, E) with F = {AB → CDE, D → A} has candidate keys and highest normal form

(1) AB only, 2NF  
(2) AB and BD, BCNF  
(3) AB only, BCNF  
(4) AB and BD, 3NF  

<details><summary>Answer</summary>

**(4)** — D → A: D is not a superkey, but A is prime, so the relation is in 3NF but not BCNF.

</details>

**Q16.** `Medium`  
The relation R(A, B, C, D, E) with F = {AB → C, DE → B, C → D} has which candidate keys?

(1) AB only  
(2) AE and BE  
(3) ABE only  
(4) ABE, ACE and ADE  

<details><summary>Answer</summary>

**(4)** — E and A appear on no right-hand side, so every key contains AE; adding B, C or D gives a key.

</details>

**Q17.** `Medium`  
The relation R(A, B, C, D, E) with F = {AB → C, DE → B, C → D} is in which highest normal form?

(1) 1NF  
(2) 2NF  
(3) 3NF  
(4) BCNF  

<details><summary>Answer</summary>

**(3)** — All attributes are prime (keys ABE, ACE, ADE), so 3NF holds, but C → D violates BCNF.

</details>

**Q18.** `High`  
The relation R(A, B, C, D, E, F, G, H, I, J) with F = {AB → C, A → DE, B → F, F → GH, D → IJ} has the candidate key

(1) AB  
(2) ABD  
(3) A  
(4) ABF  

<details><summary>Answer</summary>

**(1)** — (AB)⁺ = ABCDEFGHIJ, and neither A nor B alone determines everything.

</details>

**Q19.** `Medium`  
The relation R(A, B, C, D, E, F, G, H, I, J) with F = {AB → C, BD → EF, AD → GH, A → I, H → J} has the candidate key

(1) BD  
(2) AB  
(3) AD  
(4) ABD  

<details><summary>Answer</summary>

**(4)** — A, B and D appear on no right-hand side, so they must be in every key, and ABD determines all attributes.

</details>

**Q20.** `Medium`  
The relation R(V, W, X, Y, Z) with F = {V → W, VW → X, Y → VX, Y → Z} is in which highest normal form?

(1) 3NF  
(2) 1NF  
(3) 2NF  
(4) BCNF  

<details><summary>Answer</summary>

**(3)** — The only key is Y, so there is no partial dependency, but V → W is transitive.

</details>

**Q21.** `High`  
Match List I with List II.  
List I (Normal form): A. 1NF  B. 2NF  C. 3NF  D. BCNF  
List II (Condition): I. For every non-trivial X → Y, X is a superkey  II. Every attribute value is atomic  III. No non-prime attribute is partially dependent on a candidate key  IV. No non-prime attribute is transitively dependent on a candidate key

(1) A-II, B-III, C-I, D-IV  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Definitions of the normal forms based on functional dependencies.

</details>

**Q22.** `High`  
A relation R is in 3NF if, for every non-trivial functional dependency X → A,

(1) X is a candidate key and A is non-prime  
(2) X is a superkey or A is a prime attribute  
(3) A is a prime attribute  
(4) X is a superkey  

<details><summary>Answer</summary>

**(2)** — BCNF drops the second alternative.

</details>

**Q23.** `High`  
Given below are two statements.  
Statement I: Every relation in BCNF is also in 3NF.  
Statement II: Every relation in 3NF is also in BCNF.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — BCNF is stricter; R(A, B, C) with AB → C and C → A is in 3NF but not BCNF.

</details>

**Q24.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A relation with only two attributes is always in BCNF.  
Reason R: Every non-trivial dependency in a two-attribute relation has a single attribute on its left side, and that attribute is then a key.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — In R(A, B), A → B makes A a key and B → A makes B a key.

</details>

**Q25.** `Medium`  
Every relation whose candidate keys are all single attributes is guaranteed to be in at least

(1) 3NF  
(2) BCNF  
(3) 2NF  
(4) 1NF only  

<details><summary>Answer</summary>

**(3)** — Partial dependency requires a composite key, so such a relation cannot violate 2NF (it may still violate 3NF).

</details>

**Q26.** `High`  
R(A, B, C) with F = {A → B} is decomposed into R1(A, B) and R2(A, C). The decomposition is

(1) lossless, because B → C  
(2) lossless, because A → AB and A is common  
(3) lossy, because there is no dependency on C  
(4) lossy, because B is not in R2  

<details><summary>Answer</summary>

**(2)** — A decomposition into R1 and R2 is lossless if R1 ∩ R2 → R1 or R1 ∩ R2 → R2.

</details>

**Q27.** `High`  
R(A, B, C) with F = {A → B} is decomposed into R1(A, B) and R2(B, C). The decomposition is

(1) lossy  
(2) lossless  
(3) in BCNF and lossless  
(4) lossless and dependency-preserving  

<details><summary>Answer</summary>

**(1)** — The common attribute B determines neither AB nor BC, so spurious tuples can appear.

</details>

**Q28.** `High`  
R(A, B, C, D) with F = {A → B, B → C, C → D} is decomposed into R1(A, B), R2(A, C) and R3(A, D). The decomposition is

(1) lossless but not dependency-preserving  
(2) lossless and dependency-preserving  
(3) lossy but dependency-preserving  
(4) lossy and not dependency-preserving  

<details><summary>Answer</summary>

**(1)** — A is a key and appears in every relation, so it is lossless, but B → C and C → D cannot be checked within any single relation.

</details>

**Q29.** `Medium`  
R(A, B, C, D) with F = {A → B, B → C, C → D} is decomposed into R1(A, B), R2(B, C) and R3(C, D). The decomposition is

(1) lossless but not dependency-preserving  
(2) lossy but dependency-preserving  
(3) lossy and not dependency-preserving  
(4) lossless and dependency-preserving  

<details><summary>Answer</summary>

**(4)** — Each dependency lies inside one relation, and the chain of keys joins losslessly.

</details>

**Q30.** `High`  
R(A, B, C) with F = {AB → C, C → A} is decomposed into R1(A, C) and R2(B, C) to achieve BCNF. Which statement is correct?

(1) It is lossless and dependency-preserving  
(2) The decomposition is lossy  
(3) It is lossless but does not preserve AB → C  
(4) It is not in BCNF  

<details><summary>Answer</summary>

**(3)** — R1 ∩ R2 = C → A, so it is lossless; but AB → C spans both relations.

</details>

**Q31.** `High`  
Given below are two statements.  
Statement I: A lossless-join, dependency-preserving decomposition into BCNF is always possible.  
Statement II: A lossless-join, dependency-preserving decomposition into 3NF is always possible.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — The 3NF synthesis algorithm guarantees both properties; BCNF decomposition is lossless but may lose dependencies.

</details>

**Q32.** `Medium`  
R(A, B, C, D, E) with F = {A → BC, CD → E, B → D, E → A} is decomposed into R1(A, B, C) and R2(C, D, E). The decomposition is

(1) lossless and in BCNF  
(2) lossless  
(3) lossy  
(4) dependency-preserving and lossless  

<details><summary>Answer</summary>

**(3)** — R1 ∩ R2 = C, and C⁺ = C, which is not a key of either relation.

</details>

**Q33.** `Medium`  
R(A, B, C, D, E) with F = {A → BC, CD → E, B → D, E → A} is decomposed into R1(A, B, C) and R2(A, D, E). The decomposition is

(1) lossy  
(2) lossless  
(3) neither lossless nor in 1NF  
(4) lossy and not dependency-preserving  

<details><summary>Answer</summary>

**(2)** — R1 ∩ R2 = A, and A is a key of R1 (indeed of R).

</details>

**Q34.** `High`  
Match List I with List II.  
List I (Normal form): A. 4NF  B. 5NF (PJNF)  C. BCNF  D. 3NF  
List II (Dependency addressed): I. Join dependencies  II. Multivalued dependencies  III. Functional dependencies where the determinant is not a superkey  IV. Transitive dependencies of non-prime attributes

(1) A-I, B-II, C-III, D-IV  
(2) A-II, B-III, C-I, D-IV  
(3) A-II, B-I, C-IV, D-III  
(4) A-II, B-I, C-III, D-IV  

<details><summary>Answer</summary>

**(4)** — Higher normal forms deal with multivalued and join dependencies.

</details>

**Q35.** `High`  
A multivalued dependency X →→ Y holds in R if

(1) Y is a subset of X  
(2) for each X value, the set of Y values is independent of the values of the remaining attributes  
(3) X and Y have no common attributes  
(4) Y is functionally determined by X  

<details><summary>Answer</summary>

**(2)** — Every FD X → Y is also an MVD X →→ Y.

</details>

**Q36.** `Medium`  
Given below are two statements.  
Statement I: Every functional dependency is also a multivalued dependency.  
Statement II: Every multivalued dependency is also a functional dependency.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — MVDs generalise FDs; the converse does not hold.

</details>

**Q37.** `Medium`  
A relation Course(Course, Teacher, Book), where each course has a set of teachers and a set of books chosen independently, violates which normal form?

(1) 4NF  
(2) BCNF  
(3) 2NF  
(4) 3NF  

<details><summary>Answer</summary>

**(1)** — Course →→ Teacher and Course →→ Book are non-trivial MVDs whose determinant is not a superkey.

</details>

**Q38.** `Medium`  
The complementation rule for multivalued dependencies states that if X →→ Y holds in R, then

(1) Y → X holds  
(2) X → Y holds  
(3) Y →→ X holds  
(4) X →→ R − X − Y also holds  

<details><summary>Answer</summary>

**(4)** — MVDs always come in complementary pairs.

</details>

**Q39.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Normalization reduces update, insertion and deletion anomalies.  
Reason R: Normalization always improves query performance by reducing the number of joins.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Normalization generally increases the number of joins; denormalization is sometimes used for performance.

</details>

**Q40.** `Medium`  
Which anomaly occurs when deleting the last employee of a department also removes all information about the department?

(1) Deletion anomaly  
(2) Update anomaly  
(3) Join anomaly  
(4) Insertion anomaly  

<details><summary>Answer</summary>

**(1)** — It arises when facts about different entities are stored in one relation.

</details>

**Q41.** `Medium`  
A relation is in first normal form if

(1) it has no transitive dependencies  
(2) it has a single-attribute key  
(3) it has no partial dependencies  
(4) all its attribute values are atomic (no repeating groups or nested relations)  

<details><summary>Answer</summary>

**(4)** — 1NF is part of the basic definition of a relation.

</details>

**Q42.** `Medium`  
An attribute is called prime if

(1) it is the primary key  
(2) it is a member of some candidate key  
(3) it appears on the right side of an FD  
(4) it is not null  

<details><summary>Answer</summary>

**(2)** — Non-prime attributes are not part of any candidate key.

</details>

**Q43.** `Medium`  
The closure F⁺ of a set of functional dependencies F is

(1) the set of attributes determined by F  
(2) the set of candidate keys  
(3) the minimal cover of F  
(4) the set of all functional dependencies logically implied by F  

<details><summary>Answer</summary>

**(4)** — Attribute closure X⁺ is used to test whether X → Y is in F⁺.

</details>

**Q44.** `Medium`  
A relation R(A, B, C, D) has F = {AB → CD, D → A}. Its candidate keys are

(1) AB, BD and AD  
(2) AB and BD  
(3) BD only  
(4) AB only  

<details><summary>Answer</summary>

**(2)** — D → A, so BD → ABD → ABCD; B alone determines nothing, and AD lacks B.

</details>

**Q45.** `Medium`  
For R(A, B, C, D, E) with F = {A → B, B → E, C → D}, the candidate key and the highest normal form are

(1) A, 3NF  
(2) AC, 2NF  
(3) AC, 3NF  
(4) AC, 1NF  

<details><summary>Answer</summary>

**(4)** — AC is the key; A → B is a partial dependency of the non-prime attribute B.

</details>

**Q46.** `Medium`  
Given below are two statements.  
Statement I: If X → Y holds, then XZ → Y also holds for any set Z.  
Statement II: If X → Y and Z → W hold, then XZ → YW holds.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both follow from augmentation and union (I is augmentation with reflexivity).

</details>

**Q47.** `Medium`  
An extraneous attribute in a functional dependency is one that

(1) appears in no candidate key  
(2) makes the dependency trivial  
(3) is always on the right-hand side  
(4) can be removed without changing the closure of the set of dependencies  

<details><summary>Answer</summary>

**(4)** — Removing extraneous attributes is a step in computing a canonical cover.

</details>

**Q48.** `Medium`  
A functional dependency X → Y is trivial if

(1) X ⊆ Y  
(2) X is a key  
(3) Y ⊆ X  
(4) X and Y are disjoint  

<details><summary>Answer</summary>

**(3)** — Trivial dependencies always hold, for example AB → A.

</details>

**Q49.** `High`  
For R(A, B, C, D, E, H) with F = {A → B, BC → D, E → C, D → A}, the candidate keys are

(1) AEH, BEH and DEH  
(2) EH only  
(3) AEH only  
(4) ACE, BCE and DCE  

<details><summary>Answer</summary>

**(1)** — E and H appear on no right-hand side; EH⁺ = EHC, and adding A, B or D completes a key.

</details>

**Q50.** `Medium`  
Arrange the normal forms in increasing order of strictness.  
A. BCNF  B. 3NF  C. 4NF  D. 2NF  E. 5NF

(1) D, A, B, C, E  
(2) D, B, A, C, E  
(3) B, D, A, C, E  
(4) D, B, C, A, E  

<details><summary>Answer</summary>

**(2)** — 2NF, 3NF, BCNF, 4NF and then 5NF; each is stricter than the previous one.

</details>

**Q51.** `Medium`  
The decomposition of R into R1 and R2 is lossless if and only if, with respect to F⁺,

(1) R1 ∪ R2 = R and R1 ∩ R2 is a key of R  
(2) R1 → R2  
(3) R1 ∩ R2 is empty  
(4) R1 ∩ R2 → R1 or R1 ∩ R2 → R2  

<details><summary>Answer</summary>

**(4)** — This is the binary lossless-join test.

</details>

**Q52.** `Medium`  
A decomposition is dependency-preserving if

(1) the union of the projections of F onto the decomposed relations is equivalent to F  
(2) every dependency in F holds in at least one relation  
(3) it is lossless  
(4) every relation is in BCNF  

<details><summary>Answer</summary>

**(1)** — Otherwise some dependency can only be checked by joining relations.

</details>

**Q53.** `Medium`  
Given below are two statements.  
Statement I: Domain-key normal form (DKNF) requires that every constraint follow from domain constraints and key constraints.  
Statement II: A relation in DKNF has no insertion or deletion anomalies.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — DKNF was proposed by Fagin as the "ultimate" normal form.

</details>

**Q54.** `Medium`  
A relation R(A, B, C) has the functional dependency A → B. Which of the following tuples, if inserted into R containing (a1, b1, c1), violates the dependency?

(1) (a2, b2, c1)  
(2) (a1, b1, c2)  
(3) (a2, b1, c1)  
(4) (a1, b2, c2)  

<details><summary>Answer</summary>

**(4)** — Two tuples with the same A value (a1) must have the same B value.

</details>

**Q55.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A relation whose candidate keys are all single attributes and which is in 3NF must be in BCNF.  
Reason R: In 3NF every determinant of a non-trivial dependency must be a superkey.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Date and Fagin showed that a 3NF relation whose keys are all simple is in BCNF (indeed in 5NF), so A is true; R is false because 3NF also allows X → A when A is prime.

</details>
