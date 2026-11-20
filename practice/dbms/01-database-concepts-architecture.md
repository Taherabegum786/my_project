# Set 1 — Database System Concepts and Architecture (data models, schemas, three-schema architecture, data independence, languages)

**39 questions** — High: 12, Medium: 24, Low: 3

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Level of the three-schema architecture): A. Internal level  B. Conceptual level  C. External level  
List II (Description): I. Describes the part of the database that a particular user group is interested in  II. Describes the physical storage structures and access paths  III. Describes the structure of the whole database for all users, hiding storage details

(1) A-II, B-I, C-III  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — The ANSI/SPARC three-schema architecture: internal, conceptual and external (view) levels.

</details>

**Q2.** `High`  
The ability to change the conceptual schema without having to change the external schemas or application programs is called

(1) data abstraction  
(2) physical data independence  
(3) logical data independence  
(4) data integrity  

<details><summary>Answer</summary>

**(3)** — Physical data independence is the ability to change the internal schema without changing the conceptual schema.

</details>

**Q3.** `High`  
Given below are two statements.  
Statement I: Physical data independence means that changes to the conceptual schema do not affect external schemas.  
Statement II: Logical data independence is harder to achieve than physical data independence.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Statement I describes logical data independence; physical data independence protects the conceptual schema from changes in the internal schema.

</details>

**Q4.** `High`  
Match List I with List II.  
List I (SQL command): A. CREATE  B. UPDATE  C. GRANT  D. ROLLBACK  
List II (Language category): I. Transaction control language  II. Data definition language  III. Data control language  IV. Data manipulation language

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-III, C-IV, D-I  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(4)** — DDL: CREATE, ALTER, DROP, TRUNCATE; DML: SELECT, INSERT, UPDATE, DELETE; DCL: GRANT, REVOKE; TCL: COMMIT, ROLLBACK, SAVEPOINT.

</details>

**Q5.** `High`  
Which of the following are DDL commands?  
A. ALTER  B. TRUNCATE  C. DELETE  D. DROP  E. INSERT  
Choose the correct answer from the options given below:

(1) B, C and E only  
(2) A, B, C and D only  
(3) A, C and D only  
(4) A, B and D only  

<details><summary>Answer</summary>

**(4)** — DELETE and INSERT are DML commands; TRUNCATE is DDL because it deallocates the data pages.

</details>

**Q6.** `High`  
The description of a database, which is specified during design and is not expected to change frequently, is called the

(1) database state  
(2) data dictionary  
(3) database instance  
(4) database schema  

<details><summary>Answer</summary>

**(4)** — The schema is the intension; the data in the database at a particular moment is the instance (extension or state).

</details>

**Q7.** `Medium`  
Given below are two statements.  
Statement I: The database schema is also called the extension of the database.  
Statement II: The database instance rarely changes once the database has been created.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — The schema is the intension; the instance (extension) changes with every update.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Data model): A. Hierarchical model  B. Network model  C. Relational model  D. Object-oriented model  
List II (Example system or origin): I. CODASYL DBTG, IDMS  II. IBM IMS  III. E. F. Codd, 1970  IV. ODMG standard, ObjectStore

(1) A-II, B-I, C-III, D-IV  
(2) A-II, B-III, C-I, D-IV  
(3) A-I, B-II, C-III, D-IV  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(1)** — IMS is hierarchical, IDMS follows the CODASYL network model, and Codd proposed the relational model.

</details>

**Q9.** `Medium`  
In the hierarchical data model, the relationships between records are represented as

(1) sets of key-value pairs  
(2) graphs with many-to-many links  
(3) tables  
(4) trees of parent-child relationships  

<details><summary>Answer</summary>

**(4)** — Each child record has only one parent; many-to-many relationships need virtual records.

</details>

**Q10.** `Medium`  
Information about the structure of the database, such as table definitions, constraints and access rights, is stored in the

(1) transaction log  
(2) data dictionary (system catalog)  
(3) buffer pool  
(4) index file  

<details><summary>Answer</summary>

**(2)** — This "data about data" is called metadata.

</details>

**Q11.** `High`  
Which of the following are disadvantages of a traditional file-processing system that a DBMS addresses?  
A. Data redundancy and inconsistency  B. Difficulty in accessing data  C. Integrity problems  D. Concurrent-access anomalies  E. Security problems  
Choose the correct answer from the options given below:

(1) B, D and E only  
(2) A, C and E only  
(3) A, B, C, D and E  
(4) A, B and C only  

<details><summary>Answer</summary>

**(3)** — All five are classic problems listed by Silberschatz.

</details>

**Q12.** `Medium`  
Which of the following is NOT a responsibility of a database administrator (DBA)?

(1) Granting authorisation for data access  
(2) Schema definition  
(3) Routine maintenance such as backups  
(4) Writing every end-user application program  

<details><summary>Answer</summary>

**(4)** — Application programs are written by application programmers.

</details>

**Q13.** `Medium`  
Match List I with List II.  
List I (DBMS component): A. DDL interpreter  B. DML compiler  C. Query evaluation engine  D. Buffer manager  
List II (Function): I. Executes low-level instructions generated by the DML compiler  II. Translates DML statements in a query language into an evaluation plan  III. Fetches data from disk into main memory and decides what to cache  IV. Interprets DDL statements and records the definitions in the data dictionary

(1) A-IV, B-I, C-II, D-III  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — Components of the query processor and the storage manager.

</details>

**Q14.** `High`  
Given below are two statements.  
Statement I: In a two-tier architecture, the application on the client machine invokes database functionality directly at the server, for example through ODBC or JDBC.  
Statement II: In a three-tier architecture, the client communicates only with an application server, which in turn communicates with the database server.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Three-tier architectures are typical of web applications.

</details>

**Q15.** `Medium`  
In a three-tier client/server architecture, business logic usually resides in the

(1) client tier  
(2) network layer  
(3) database server  
(4) application server (middle tier)  

<details><summary>Answer</summary>

**(4)** — The client handles presentation, and the database server handles data management.

</details>

**Q16.** `Medium`  
A DBMS in which the data and the DBMS software reside at a single site is called a

(1) centralized DBMS  
(2) parallel DBMS  
(3) federated DBMS  
(4) distributed DBMS  

<details><summary>Answer</summary>

**(1)** — Distributed DBMSs spread data and software over several sites.

</details>

**Q17.** `High`  
Match List I with List II.  
List I (Data model category): A. High-level (conceptual) data model  B. Representational (implementation) data model  C. Low-level (physical) data model  
List II (Example): I. Relational model  II. Description of record formats, ordering and access paths  III. Entity-Relationship model

(1) A-I, B-III, C-II  
(2) A-II, B-I, C-III  
(3) A-III, B-I, C-II  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(3)** — Elmasri and Navathe's classification of data models.

</details>

**Q18.** `Medium`  
A DBMS interface that allows users to specify queries by filling in example values in a table skeleton is

(1) a menu-based interface  
(2) a forms-based interface  
(3) a natural-language interface  
(4) Query-By-Example (QBE)  

<details><summary>Answer</summary>

**(4)** — QBE was developed at IBM by Moshe Zloof.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: A procedural DML requires the user to specify what data is needed and how to get it.  
Statement II: SQL is primarily a declarative (non-procedural) language.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Relational algebra is procedural; SQL and relational calculus are declarative.

</details>

**Q20.** `Medium`  
Which of the following describes a "view" in a DBMS?

(1) An index on a table  
(2) A physical copy of a table stored on disk  
(3) A virtual relation defined by a query on base relations  
(4) A backup of the database  

<details><summary>Answer</summary>

**(3)** — A view is part of the external level and normally stores no data (unless materialized).

</details>

**Q21.** `Medium`  
Which of the following is an example of metadata?

(1) The salary of an employee  
(2) The data type and length of the column Salary  
(3) A row of the Employee table  
(4) The result of a query  

<details><summary>Answer</summary>

**(2)** — Metadata describes the data rather than being the data itself.

</details>

**Q22.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Programs written for a DBMS have program-data independence.  
Reason R: The structure of data files is stored in the DBMS catalog, separately from the access programs.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Because the structure is in the catalog, changing it does not require changing the programs.

</details>

**Q23.** `Medium`  
The DBMS component that ensures that the database remains in a consistent state despite system failures and concurrent transactions is the

(1) transaction manager  
(2) query optimizer  
(3) file manager  
(4) DDL compiler  

<details><summary>Answer</summary>

**(1)** — The transaction manager includes concurrency control and recovery.

</details>

**Q24.** `Medium`  
A database that holds data about a single specific application area and supports a limited set of users is a

(1) distributed database  
(2) personal or departmental database  
(3) data warehouse  
(4) data mart only  

<details><summary>Answer</summary>

**(2)** — Classification by number of users: single-user versus multiuser systems.

</details>

**Q25.** `Medium`  
Which of the following is NOT a feature of the database approach?

(1) Data duplication in separate files for each application  
(2) Support of multiple views of the data  
(3) Insulation between programs and data  
(4) Self-describing nature of the database system  

<details><summary>Answer</summary>

**(1)** — Separate per-application files are a feature of traditional file processing.

</details>

**Q26.** `Medium`  
In the context of DBMS, "entity integrity" and "referential integrity" are examples of

(1) security mechanisms  
(2) indexing techniques  
(3) storage structures  
(4) integrity constraints  

<details><summary>Answer</summary>

**(4)** — Integrity constraints are enforced by the DBMS to keep data valid.

</details>

**Q27.** `Medium`  
Match List I with List II.  
List I (User type): A. Naive (parametric) end users  B. Sophisticated end users  C. Application programmers  D. DBA  
List II (Description): I. Has central control over data and programs  II. Use canned transactions, such as bank tellers  III. Write programs that access the database  IV. Formulate queries directly using a query language or analysis tools

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-IV, B-II, C-III, D-I  

<details><summary>Answer</summary>

**(2)** — Categories of database users.

</details>

**Q28.** `Low`  
SQL was originally developed at IBM under the name

(1) QBE  
(2) QUEL  
(3) SEQUEL  
(4) Datalog  

<details><summary>Answer</summary>

**(3)** — SEQUEL (Structured English Query Language) was developed for System R.

</details>

**Q29.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The TRUNCATE command cannot normally be rolled back in many DBMSs.  
Reason R: TRUNCATE is a DML command that deletes rows one at a time and logs each deletion.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — TRUNCATE is a DDL command that deallocates whole data pages without logging individual rows, which is why it is fast and usually not undoable.

</details>

**Q30.** `Medium`  
Which of the following terms refers to the conceptual design of the database being independent of any particular DBMS?

(1) Requirements analysis  
(2) Tuning  
(3) Physical design  
(4) Logical design  

<details><summary>Answer</summary>

**(4)** — Conceptual (ER) design is DBMS-independent; logical design maps it to the data model of a DBMS, and physical design is DBMS-specific.

</details>

**Q31.** `Medium`  
Arrange the phases of database design in the correct order.  
A. Logical design (data-model mapping)  B. Requirements collection and analysis  C. Physical design  D. Conceptual design

(1) B, A, D, C  
(2) B, D, C, A  
(3) B, D, A, C  
(4) D, B, A, C  

<details><summary>Answer</summary>

**(3)** — Requirements, conceptual schema (ER), logical schema, then physical schema.

</details>

**Q32.** `Medium`  
Given below are two statements.  
Statement I: A DBMS cache (buffer) is used to reduce the number of disk accesses.  
Statement II: The storage manager is the interface between the low-level data stored in the database and the application programs and queries.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The storage manager includes the authorization and integrity manager, transaction manager, file manager and buffer manager.

</details>

**Q33.** `Low`  
A database that stores data in a single file per application and uses a host language for all processing is called a

(1) relational DBMS  
(2) file-processing system  
(3) NoSQL database  
(4) object DBMS  

<details><summary>Answer</summary>

**(2)** — File-processing systems preceded DBMSs.

</details>

**Q34.** `Medium`  
Which of the following correctly matches a database language with its paradigm?

(1) Tuple relational calculus — procedural  
(2) SQL — procedural  
(3) Relational algebra — procedural  
(4) Domain relational calculus — procedural  

<details><summary>Answer</summary>

**(3)** — Relational algebra specifies a sequence of operations; both calculi are declarative.

</details>

**Q35.** `Medium`  
Given below are two statements.  
Statement I: An embedded SQL program uses a host language such as C or Java together with SQL statements.  
Statement II: The mismatch between the set-at-a-time model of SQL and the record-at-a-time model of host languages is called impedance mismatch.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Cursors are used to bridge the mismatch.

</details>

**Q36.** `Medium`  
In which of the following data models can a record type have more than one parent (owner) record type?

(1) Flat-file model  
(2) Key-value model  
(3) Hierarchical model  
(4) Network model  

<details><summary>Answer</summary>

**(4)** — The network model allows a member record to belong to several set types.

</details>

**Q37.** `Low`  
The person who designs and implements DBMS software packages is called a

(1) DBMS system designer and implementer  
(2) DBA  
(3) database designer  
(4) end user  

<details><summary>Answer</summary>

**(1)** — Database designers design the database for an application; system designers build the DBMS software itself.

</details>

**Q38.** `High`  
Given below are two statements.  
Statement I: A data model is a collection of concepts used to describe the structure of a database, its operations and its constraints.  
Statement II: Relational, network and hierarchical models are all record-based (representational) data models.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard textbook statements.

</details>

**Q39.** `Medium`  
Given below are two statements.  
Statement I: A relational DBMS does not require any schema to be defined before data is inserted.  
Statement II: Every relational DBMS stores each table in a separate operating-system file.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Relational systems require a schema first, and storage of tables in files is implementation-dependent.

</details>
