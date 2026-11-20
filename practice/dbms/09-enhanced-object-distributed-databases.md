# Set 9 — Object and Object-Relational Databases, Enhanced Data Models (temporal, multimedia, deductive, XML, mobile, GIS, genome) and Distributed Databases

**39 questions** — High: 10, Medium: 28, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Database type): A. Temporal database  B. Deductive database  C. Spatial (GIS) database  D. Multimedia database  
List II (Characteristic): I. Uses rules and facts, typically in Datalog, to infer new facts  II. Stores images, audio and video and supports content-based retrieval  III. Records valid time and/or transaction time of facts  IV. Stores geometric data such as points, lines and polygons, indexed by R-trees

(1) A-III, B-IV, C-I, D-II  
(2) A-I, B-III, C-IV, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-I, C-II, D-IV  

<details><summary>Answer</summary>

**(3)** — Enhanced data models covered in Elmasri and Navathe.

</details>

**Q2.** `High`  
Given below are two statements.  
Statement I: Valid time is the time period during which a fact is true in the real world.  
Statement II: Transaction time is the time period during which a fact is stored in the database.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — A bitemporal database records both valid time and transaction time.

</details>

**Q3.** `Medium`  
A temporal database that records both valid time and transaction time is called a

(1) snapshot database  
(2) bitemporal database  
(3) rollback database only  
(4) historical database only  

<details><summary>Answer</summary>

**(2)** — Valid-time-only databases are historical; transaction-time-only databases are rollback databases.

</details>

**Q4.** `High`  
In a deductive database, a Datalog rule such as ancestor(X, Y) :- parent(X, Y). is made up of

(1) a table and an index  
(2) a key and a value  
(3) a head and a body  
(4) a fact and a trigger  

<details><summary>Answer</summary>

**(3)** — The head is derived when all literals in the body are true; facts are rules with empty bodies.

</details>

**Q5.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Deductive databases can express recursive queries such as the transitive closure of a parent relation.  
Reason R: Datalog rules can be recursive, with the head predicate appearing in the body.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Recursive views in SQL:1999 (WITH RECURSIVE) offer similar power.

</details>

**Q6.** `Medium`  
In Datalog, stratification is required when a program uses

(1) negation, so that a predicate is not defined in terms of its own negation  
(2) constants  
(3) aggregate functions only  
(4) recursion only  

<details><summary>Answer</summary>

**(1)** — Stratified negation gives a well-defined meaning to programs with negation.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (XML technology): A. DTD  B. XML Schema  C. XPath  D. XQuery  
List II (Purpose): I. Path expressions for selecting nodes in an XML document  II. Query language with FLWOR expressions  III. Older grammar for document structure, with limited data types  IV. XML-based schema language with rich data types

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-II, D-I  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — XML schema and query standards from the W3C.

</details>

**Q8.** `Medium`  
The FLWOR expression in XQuery stands for

(1) For, Let, Where, Order by, Return  
(2) From, Let, Where, Order, Rank  
(3) For, Loop, While, Or, Repeat  
(4) Find, Locate, Where, Order, Retrieve  

<details><summary>Answer</summary>

**(1)** — It is analogous to SELECT-FROM-WHERE in SQL.

</details>

**Q9.** `Medium`  
Given below are two statements.  
Statement I: An XML document is well-formed if it follows the syntax rules of XML, such as properly nested tags.  
Statement II: Every well-formed XML document is valid with respect to any DTD.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A valid document must also conform to its DTD or schema; well-formedness alone is not enough.

</details>

**Q10.** `Medium`  
XML data is best described as

(1) unstructured data  
(2) semi-structured data  
(3) binary data  
(4) structured data  

<details><summary>Answer</summary>

**(2)** — XML is self-describing, with tags giving structure but no fixed schema required.

</details>

**Q11.** `High`  
Match List I with List II.  
List I (Object database concept): A. Object identifier (OID)  B. Encapsulation  C. Inheritance  D. Polymorphism  
List II (Meaning): I. A subclass acquires the attributes and methods of its superclass  II. Same operation name bound to different implementations depending on the object type  III. System-generated identity that is unique and immutable  IV. Objects are accessed only through their defined operations

(1) A-IV, B-III, C-I, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — Basic concepts of object-oriented databases.

</details>

**Q12.** `Medium`  
The ODMG standard for object databases defines

(1) ODL for schema definition and OQL for queries  
(2) XPath and XQuery  
(3) SQL and PL/SQL  
(4) Datalog and Prolog  

<details><summary>Answer</summary>

**(1)** — ODL is the Object Definition Language and OQL the Object Query Language.

</details>

**Q13.** `Medium`  
Given below are two statements.  
Statement I: Object-relational databases extend the relational model with user-defined types, inheritance and reference types.  
Statement II: SQL:1999 introduced user-defined structured types and REF types.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both statements are true.

</details>

**Q14.** `Medium`  
In an object database, an object's identity

(1) changes when its attribute values change  
(2) is independent of its attribute values and remains the same throughout its lifetime  
(3) is the primary key chosen by the user  
(4) is its memory address  

<details><summary>Answer</summary>

**(2)** — Value-based identity (keys) is the relational approach.

</details>

**Q15.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Object databases reduce the impedance mismatch between programming languages and databases.  
Reason R: Object databases store all data in flat relational tables.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Object databases store objects with the type system of the programming language, which is why the mismatch is reduced.

</details>

**Q16.** `Medium`  
A collection type in an object-relational database that can hold an unordered set of values, possibly with duplicates, is a

(1) set  
(2) multiset (bag)  
(3) list  
(4) array  

<details><summary>Answer</summary>

**(2)** — A set has no duplicates; lists and arrays are ordered.

</details>

**Q17.** `High`  
Match List I with List II.  
List I (Distributed database fragmentation): A. Horizontal fragmentation  B. Vertical fragmentation  C. Mixed (hybrid) fragmentation  
List II (Description): I. Combination of horizontal and vertical fragmentation  II. A subset of the tuples of a relation, defined by a selection  III. A subset of the attributes of a relation, each fragment including the key

(1) A-I, B-III, C-II  
(2) A-III, B-II, C-I  
(3) A-II, B-III, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(3)** — Horizontal fragments are reconstructed by union, vertical fragments by join.

</details>

**Q18.** `High`  
Given below are two statements.  
Statement I: A horizontally fragmented relation is reconstructed by taking the natural join of its fragments.  
Statement II: A vertically fragmented relation is reconstructed by taking the union of its fragments.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — It is the other way round: horizontal fragments are combined by union and vertical fragments by join.

</details>

**Q19.** `High`  
Match List I with List II.  
List I (Transparency in a distributed DBMS): A. Location transparency  B. Fragmentation transparency  C. Replication transparency  
List II (Description): I. Users need not know how many copies of the data exist  II. Users need not know where the data is stored  III. Users need not know how a relation is divided into pieces

(1) A-III, B-II, C-I  
(2) A-II, B-III, C-I  
(3) A-II, B-I, C-III  
(4) A-I, B-III, C-II  

<details><summary>Answer</summary>

**(2)** — Types of distribution transparency.

</details>

**Q20.** `High`  
Arrange the steps of the two-phase commit protocol for a committing transaction in order.  
A. The coordinator sends commit to all participants  B. Participants reply "ready" (vote yes)  C. The coordinator sends prepare to all participants  D. Participants acknowledge and the coordinator writes the end record

(1) C, A, B, D  
(2) A, C, B, D  
(3) C, B, A, D  
(4) B, C, A, D  

<details><summary>Answer</summary>

**(3)** — Phase 1 is voting (prepare and votes); phase 2 is the decision (commit or abort).

</details>

**Q21.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The two-phase commit protocol can block participants if the coordinator fails.  
Reason R: A participant that voted "ready" cannot decide on its own whether to commit or abort.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Three-phase commit was proposed to reduce this blocking.

</details>

**Q22.** `Medium`  
In two-phase commit, if any participant votes "abort",

(1) the coordinator decides to abort the transaction at all sites  
(2) the coordinator commits anyway  
(3) the protocol restarts automatically  
(4) only that participant aborts  

<details><summary>Answer</summary>

**(1)** — Commit requires unanimous "ready" votes.

</details>

**Q23.** `Medium`  
The semijoin operation is used in distributed query processing to

(1) replicate relations  
(2) increase the data transferred  
(3) reduce the amount of data transferred between sites by sending only join-attribute values first  
(4) encrypt data  

<details><summary>Answer</summary>

**(3)** — Only the tuples that will actually join are then shipped.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: In a homogeneous distributed database, all sites use the same DBMS software.  
Statement II: A federated database is a collection of autonomous, possibly heterogeneous databases that cooperate.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Multidatabase or federated systems give a global view over independent databases.

</details>

**Q25.** `Medium`  
Full replication of a database at every site improves

(1) availability and the speed of read-only queries  
(2) update performance  
(3) concurrency control simplicity  
(4) storage efficiency  

<details><summary>Answer</summary>

**(1)** — Updates become expensive because every copy must be changed.

</details>

**Q26.** `Medium`  
In the primary-copy method of distributed concurrency control

(1) the coordinator holds all copies  
(2) no locks are used  
(3) locks are requested only at the site holding the designated primary copy of the item  
(4) every copy must be locked  

<details><summary>Answer</summary>

**(3)** — It simplifies locking but the primary site can become a bottleneck.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: Data broadcasting from servers to mobile clients is never used in mobile databases.  
Statement II: Mobile databases must cope with frequent disconnections, limited bandwidth and limited battery power.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Broadcast disks are a common technique for disseminating data to many mobile clients.

</details>

**Q28.** `Medium`  
In GIS, data represented as a grid of cells, each holding a value, is called

(1) topological data  
(2) raster data  
(3) network data  
(4) vector data  

<details><summary>Answer</summary>

**(2)** — Vector data represents objects as points, lines and polygons.

</details>

**Q29.** `Medium`  
Which index is designed for multidimensional spatial data using minimum bounding rectangles?

(1) B+ tree  
(2) R-tree  
(3) Bitmap index  
(4) Hash index  

<details><summary>Answer</summary>

**(2)** — Quadtrees and k-d trees are other spatial structures.

</details>

**Q30.** `Medium`  
Genome data management systems must support

(1) only relational joins  
(2) only fixed-length numeric fields  
(3) only small transactional updates  
(4) very large sequence data, complex relationships and similarity searches over biological sequences  

<details><summary>Answer</summary>

**(4)** — Examples include GenBank and sequence-similarity tools such as BLAST.

</details>

**Q31.** `Medium`  
Content-based retrieval in multimedia databases means

(1) retrieving images or videos using features such as colour, texture and shape  
(2) retrieving objects by file name  
(3) retrieving only text  
(4) retrieving by creation date  

<details><summary>Answer</summary>

**(1)** — Features are extracted and indexed for similarity search.

</details>

**Q32.** `Medium`  
Given below are two statements.  
Statement I: In a client-server DBMS architecture, query processing and transaction management are done at the server.  
Statement II: In a peer-to-peer distributed DBMS, every site can act as both client and server.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard distributed architectures.

</details>

**Q33.** `Medium`  
In distributed deadlock detection, a deadlock that is not visible in any single local wait-for graph but exists in the union of the graphs is called a

(1) livelock  
(2) phantom deadlock  
(3) global deadlock  
(4) local deadlock  

<details><summary>Answer</summary>

**(3)** — A phantom deadlock is a false detection caused by delays in message delivery.

</details>

**Q34.** `Medium`  
The three-phase commit protocol differs from two-phase commit by

(1) eliminating the need for logs  
(2) adding a pre-commit phase so that participants can decide without blocking if the coordinator fails (assuming no network partition)  
(3) removing the voting phase  
(4) using no messages  

<details><summary>Answer</summary>

**(2)** — It is non-blocking under certain failure assumptions.

</details>

**Q35.** `Low`  
An object that remains in the database after the program that created it terminates is called a

(1) volatile object  
(2) transient object  
(3) persistent object  
(4) temporary object  

<details><summary>Answer</summary>

**(3)** — Persistence by reachability or naming is used in object databases.

</details>

**Q36.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Distributed databases can improve reliability and availability.  
Reason R: Distributed query processing must consider the cost of transferring data between sites.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but availability improves because replicated data remains accessible when a site fails.

</details>

**Q37.** `Medium`  
In XPath, the expression /bookstore/book[price &gt; 35]/title selects

(1) all prices greater than 35  
(2) the first book only  
(3) the title elements of books whose price is greater than 35  
(4) all bookstore elements  

<details><summary>Answer</summary>

**(3)** — The predicate in square brackets filters book elements.

</details>

**Q38.** `Medium`  
Which of the following is NOT a characteristic of a temporal database?

(1) Valid time  
(2) Ignoring the history of changes  
(3) Time-stamped tuples or attributes  
(4) Transaction time  

<details><summary>Answer</summary>

**(2)** — Temporal databases specifically keep history.

</details>

**Q39.** `Medium`  
In object-relational SQL, the keyword UNDER is used to

(1) define a view  
(2) grant privileges  
(3) define a subtype or subtable that inherits from another  
(4) create an index  

<details><summary>Answer</summary>

**(3)** — For example CREATE TYPE Student UNDER Person.

</details>
