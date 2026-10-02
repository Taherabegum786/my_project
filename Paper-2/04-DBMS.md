# Paper 2 · Unit 4 — Database Management Systems

**Expected questions: 10–12 · Target: 10+ · Type: normalisation, keys, SQL output, transactions, concepts — very scoring**

## Syllabus Checklist
- [ ] Database system concepts & architecture: data models, schemas, instances, three-schema architecture, data independence, database languages & interfaces, centralised & client/server architecture
- [ ] Data modelling: ER diagram, relational model (constraints, languages, design, programming), relational algebra & calculus, codd rules
- [ ] SQL: data definition, types, constraints, queries, insert, delete, update, views, stored procedures, functions, triggers, SQL injection
- [ ] Normalisation: functional dependencies, 1NF, 2NF, 3NF, BCNF, multivalued dependencies & 4NF, join dependencies & 5NF, inclusion dependencies
- [ ] Transaction processing, concurrency control & recovery
- [ ] Physical database design: file organisation, indexing (single-level, multilevel, B-tree, B+-tree), query processing & optimisation
- [ ] Object & object-relational databases; database security
- [ ] Enhanced data models: temporal, multimedia, deductive, XML & internet databases, mobile, GIS, genome, distributed databases
- [ ] Data warehousing & data mining: OLAP, data cube, association rules, classification, clustering
- [ ] Big data systems: characteristics, types, architecture, MapReduce, Hadoop, NoSQL (CAP theorem, document, key-value, column, graph)

---

## 1. Architecture

A database management system stands between users and stored data. Its central achievement is *data
independence*: applications describe what data they want, and the system decides how it is stored and
found, so that storage can change without rewriting programs.

### 1.1 Three-Schema (ANSI/SPARC) Architecture

<!-- latex: p2-04-threeschema -->
```mermaid
flowchart TB
    U1[User 1] --> E1[External view 1]
    U2[User 2] --> E2[External view 2]
    E1 & E2 -->|logical data independence| C[Conceptual schema<br/>entities, relations, constraints]
    C -->|physical data independence| I[Internal schema<br/>storage, indexes, file organisation]
    I --> DB[(Stored database)]
```
- **Logical data independence**: change conceptual schema without changing external views (harder to achieve).
- **Physical data independence**: change internal schema without changing conceptual schema.
- **Schema** = structure (intension, changes rarely); **Instance** = data at a moment (extension).
- Languages: **DDL** (CREATE, ALTER, DROP, TRUNCATE), **DML** (SELECT, INSERT, UPDATE, DELETE), **DCL** (GRANT, REVOKE), **TCL** (COMMIT, ROLLBACK, SAVEPOINT).
- Data models: hierarchical (IMS, tree), network (CODASYL, graph), relational (Codd 1970), object-oriented, object-relational.
- Architectures: centralised, **2-tier** client/server, **3-tier** (client – application server – DB server).

### 1.2 DBMS Components
Query processor (DDL interpreter, DML compiler, query evaluation engine), storage manager (authorisation, transaction manager, file manager, buffer manager), data dictionary (metadata).

## 2. ER Model

The entity–relationship model is a picture of the real world before any tables exist: things (entities),
their properties (attributes) and the associations between them (relationships). Chen's notation, shown
below, is the one used in the examination.

<!-- latex: p2-04-er-notation -->
```
 ER notation (Chen)
 ┌────────┐   Entity              ╔════════╗  Weak entity
 └────────┘                       ╚════════╝
 (  attr  )   Attribute           (( multi ))  Multivalued
 ( _key_ )    Key (underlined)    (  - - -  )  Derived (dashed)
  ◇           Relationship        ◈            Identifying relationship (double diamond)
 ═══          Total participation  ───         Partial participation
```

<!-- latex: p2-04-er-example -->
```mermaid
erDiagram
    STUDENT ||--o{ ENROLLS : has
    COURSE ||--o{ ENROLLS : includes
    DEPARTMENT ||--|{ COURSE : offers
    STUDENT {
        int roll_no PK
        string name
        date dob
    }
    COURSE {
        string course_id PK
        string title
        int credits
    }
    ENROLLS {
        int roll_no FK
        string course_id FK
        string grade
    }
```

- **Cardinality**: 1:1, 1:N, M:N. **Participation**: total (every entity participates — double line) or partial.
- **Weak entity**: no key of its own; identified via owner entity + partial key (discriminator).
- **Specialisation** (top-down), **generalisation** (bottom-up), **aggregation** (relationship as entity). Disjoint/overlapping, total/partial constraints.

### ER → Relational mapping (minimum tables)

| Case | Tables |
|------|--------|
| Strong entity | 1 table each |
| 1:1 relationship | Merge into either side (total participation side preferred) |
| 1:N relationship | FK on N-side; no separate table |
| **M:N relationship** | **Separate table** with both PKs |
| Multivalued attribute | Separate table |
| Weak entity | Table with owner's PK + partial key |

Classic: E1 —M:N— E2 —1:N— E3 → minimum tables = 3 entities + 1 (for M:N) = **4**.

## 3. Keys & Integrity

Keys are how a relational database identifies rows and links tables. The three key concepts are nested, as
the figure shows; integrity constraints then forbid NULL primary keys and dangling foreign keys.

<!-- latex: p2-04-keys -->
```mermaid
flowchart TB
    SK[Super key<br/>any set that uniquely identifies] --> CK[Candidate key<br/>minimal super key]
    CK --> PK[Primary key<br/>chosen CK, NOT NULL]
    CK --> AK[Alternate keys<br/>remaining CKs]
    FK[Foreign key<br/>refers to PK of another relation]
```
- Number of super keys of R(A1…An) with single candidate key A1: **2ⁿ⁻¹**.
- With candidate keys A1 and A2: 2ⁿ⁻¹ + 2ⁿ⁻¹ − 2ⁿ⁻² = **3·2ⁿ⁻²**.
- **Entity integrity**: PK cannot be NULL. **Referential integrity**: FK value must match an existing PK or be NULL.
- ON DELETE CASCADE / SET NULL / RESTRICT.

**Codd's 12 rules (13 with Rule 0)**: Rule 0 foundation; 1 information; 2 guaranteed access; 3 systematic NULLs; 4 active online catalog; 5 comprehensive data sublanguage; 6 view updating; 7 high-level insert/update/delete; 8 physical data independence; 9 logical data independence; 10 integrity independence; 11 distribution independence; 12 non-subversion.

## 4. Relational Algebra & Calculus

Relational algebra is a small set of operations on tables that produce tables. Every SQL query is
translated into an algebra expression before it is optimised, which is why the algebra is examined so
often.

| Operation | Symbol | Notes |
|-----------|--------|-------|
| Selection | σ_cond(R) | Rows; commutative |
| Projection | π_attrs(R) | Columns; removes duplicates |
| Union | R ∪ S | Union-compatible |
| Difference | R − S | |
| Cartesian product | R × S | |R|·|S| tuples |
| Rename | ρ | |
| Intersection | R ∩ S = R − (R − S) | Derived |
| Natural join | R ⋈ S | Equal common attrs |
| Theta join | R ⋈_θ S | σ_θ(R × S) |
| Division | R ÷ S | "for all" queries |
| Outer joins | ⟕ ⟖ ⟗ | Keep unmatched with NULLs |

Fundamental: **σ, π, ∪, −, ×, ρ**. Relational algebra is **procedural**; relational calculus (TRC/DRC) is **non-procedural**. Safe calculus = relational algebra in power (relational completeness).

<!-- latex: p2-04-tuplesizes -->
```
Tuple sizes: R has m tuples, S has n tuples
R × S            → m·n
R ⋈ S            → 0 … m·n
R ∪ S            → max(m,n) … m+n
R ∩ S            → 0 … min(m,n)
R − S            → 0 … m
R ⟕ S (left outer) → at least m
```

Division example: "students who took **all** courses": π_{sid,cid}(Enrolled) ÷ π_{cid}(Course).

TRC: `{ t | t ∈ Student ∧ t.age > 20 }` · DRC: `{ <n> | ∃a (<n,a> ∈ Student ∧ a > 20) }`.

## 5. SQL

```sql
SELECT dept, COUNT(*) AS n, AVG(salary)
FROM   employee
WHERE  salary > 20000          -- filters rows (before grouping)
GROUP  BY dept
HAVING COUNT(*) > 2            -- filters groups
ORDER  BY n DESC;
```
Logical order of execution: **FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT**.

- `COUNT(*)` counts all rows; `COUNT(col)` ignores NULLs; aggregates (SUM/AVG/MAX/MIN) ignore NULLs.
- NULL comparisons give UNKNOWN; use `IS NULL`. `NULL = NULL` → UNKNOWN.
- `DELETE` (DML, row-wise, rollback possible, WHERE allowed) vs `TRUNCATE` (DDL, all rows, faster) vs `DROP` (removes table structure).
- `IN`, `EXISTS`, `ANY/SOME`, `ALL`: `x > ALL (subquery)` = greater than max; `x > ANY` = greater than min.
- `UNION` removes duplicates; `UNION ALL` keeps them.
- Correlated subquery: inner query refers to outer — evaluated per outer row.
- Constraints: PRIMARY KEY, FOREIGN KEY, UNIQUE (allows NULL), NOT NULL, CHECK, DEFAULT.
- **View**: virtual table (stored query); updatable if based on single table without aggregates/DISTINCT/GROUP BY. **Materialised view** stores results.
- **Trigger**: ECA (Event–Condition–Action) rule; BEFORE/AFTER, row-level/statement-level.
- **Stored procedure** (CALL, may not return value) vs **function** (returns value, usable in SELECT).
- **SQL injection**: attacker inserts SQL via input, e.g. `' OR '1'='1`. Prevent with **prepared statements/parameterised queries**, input validation, least privilege.

**Nth highest salary**:
```sql
SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp);   -- 2nd highest
```

## 6. Functional Dependencies & Normalisation

A functional dependency $X \to Y$ says that the value of $X$ determines the value of $Y$. Redundancy arises
when a table stores such facts about only part of its key, or about non-key attributes; normalisation
removes it by splitting the table so that every fact is stored once.

### 6.1 Armstrong's Axioms
- **Reflexivity**: Y ⊆ X ⇒ X → Y · **Augmentation**: X → Y ⇒ XZ → YZ · **Transitivity**: X → Y, Y → Z ⇒ X → Z
- Derived: Union, Decomposition, Pseudo-transitivity (X → Y, WY → Z ⇒ WX → Z).
- Sound and complete.

### 6.2 Attribute Closure — Finding Candidate Keys
R(A, B, C, D, E), F = {A → B, B → C, CD → E}
<!-- latex: p2-04-closure -->
```
A⁺   = {A, B, C}
AD⁺  = {A, D, B, C, E}  = all → AD is a key
A and D never appear on the RHS → every key must contain both → AD is the ONLY candidate key
```
Trick: attributes not on any RHS must be in every key; attributes only on RHS are never in a key.

**Minimal (canonical) cover**: single attribute on RHS → remove extraneous LHS attributes → remove redundant FDs.

### 6.3 Normal Forms

Each normal form forbids one more kind of undesirable dependency. The nested diagram is a reminder that
higher normal forms imply all the lower ones.

<!-- latex: p2-04-normalforms -->
```mermaid
flowchart LR
    U[Unnormalised] -->|atomic values| N1[1NF]
    N1 -->|no partial dependency| N2[2NF]
    N2 -->|no transitive dependency| N3[3NF]
    N3 -->|every determinant is a super key| BC[BCNF]
    BC -->|no non-trivial MVD| N4[4NF]
    N4 -->|no non-trivial join dependency| N5[5NF / PJNF]
```

| NF | Condition (for every non-trivial FD X → A) |
|----|--------------------------------------------|
| 1NF | All attributes atomic (no repeating groups / multivalued) |
| 2NF | 1NF + no **partial** dependency (non-prime attribute depends on part of a candidate key) |
| 3NF | X is a super key **OR** A is a **prime** attribute |
| BCNF | X is a **super key** |
| 4NF | For every non-trivial MVD X →→ Y, X is a super key |
| 5NF | Every join dependency is implied by candidate keys |

- Relation with **only two attributes is always in BCNF**.
- If all candidate keys are single attributes ⇒ automatically 2NF.
- If all attributes are prime ⇒ automatically 3NF.

### 6.4 Decomposition Properties

| Property | Test |
|----------|------|
| **Lossless join** (must) | R into R1, R2 is lossless iff (R1 ∩ R2) → R1 or (R1 ∩ R2) → R2 |
| **Dependency preserving** (desirable) | (F1 ∪ F2)⁺ = F⁺ |

- **3NF** decomposition: always lossless **and** dependency-preserving (synthesis algorithm).
- **BCNF** decomposition: always lossless but **not always** dependency-preserving.

**Worked**: R(A,B,C), F = {AB → C, C → B}. Keys: AB, AC. C → B: C not super key but B is prime → **3NF, not BCNF**. BCNF decomposition (C,B), (A,C) loses AB → C.

## 7. Transactions

A transaction is a unit of work — such as a fund transfer — that must happen completely or not at all, even
when many transactions run at once and the system may crash. The ACID properties state these guarantees.

### ACID
| Property | Ensured by |
|----------|-----------|
| **A**tomicity (all or nothing) | Recovery manager (undo log) |
| **C**onsistency | Programmer + integrity constraints |
| **I**solation | Concurrency control manager |
| **D**urability | Recovery manager (redo log) |

### Transaction States
<!-- latex: p2-04-txstates -->
```mermaid
stateDiagram-v2
    [*] --> Active
    Active --> PartiallyCommitted: last statement executed
    Active --> Failed: error
    PartiallyCommitted --> Committed: written to stable storage
    PartiallyCommitted --> Failed
    Failed --> Aborted: rollback
    Committed --> [*]
    Aborted --> [*]
```

### Schedules & Serializability

When transactions interleave, the result is correct if it is equivalent to some serial order. Conflict
serializability is tested by drawing a precedence graph and looking for a cycle.
- **Conflicting operations**: same data item, different transactions, at least one write (RW, WR, WW).
- **Conflict serializable** ⇔ **precedence graph is acyclic** (edge Ti → Tj if Ti's op conflicts with and precedes Tj's).
- **View serializable**: same initial reads, same reads-from, same final writes. Every conflict-serializable schedule is view serializable; a view-serializable schedule that is not conflict-serializable has **blind writes**.
- Number of serial schedules of n transactions: **n!**.

<!-- latex: p2-04-schedule -->
```
Example schedule:  r1(A) w2(A) w1(A) r3(A)
Conflicts: r1(A)→w2(A): T1→T2 ; w2(A)→w1(A): T2→T1 ⇒ cycle ⇒ NOT conflict serializable
```

### Recoverability hierarchy
<!-- latex: p2-04-recoverability -->
```
 Serial ⊂ Strict ⊂ Cascadeless (ACA) ⊂ Recoverable ⊂ All schedules
```
- **Recoverable**: if Tj reads from Ti, Ti commits before Tj commits.
- **Cascadeless**: read only committed data.
- **Strict**: no read/write of item until the last writer commits/aborts.

### Concurrency problems
Lost update (WW), dirty read (WR — uncommitted dependency), unrepeatable read (RW), phantom read (insertions).
SQL isolation levels: READ UNCOMMITTED < READ COMMITTED < REPEATABLE READ < SERIALIZABLE.

### Concurrency Control Protocols

| Protocol | Key points |
|----------|-----------|
| Lock-based (S/X) | S compatible with S only |
| **Basic 2PL** | Growing phase then shrinking phase; ensures conflict serializability; **deadlock possible**, cascading rollback possible |
| **Strict 2PL** | Hold **X locks** till commit → cascadeless, strict |
| **Rigorous 2PL** | Hold **all locks** till commit; serial order = commit order |
| Conservative 2PL | Acquire all locks before starting → **deadlock-free** |
| **Timestamp ordering** | Older first; Read: if TS(T) < W-TS(X) → rollback; Write: if TS(T) < R-TS(X) or < W-TS(X) → rollback. Deadlock-free, may starve |
| **Thomas' write rule** | Ignore obsolete write instead of rollback → allows some view-serializable schedules |
| Validation (optimistic) | Read → validate → write phases |
| Multiversion (MVCC) | Readers don't block writers |
| Multiple granularity | Intention locks IS, IX, SIX |

Deadlock prevention with timestamps:
<!-- latex: p2-04-waitdie -->
```
 Wait–Die  (non-preemptive): older requests → WAITS;   younger requests → DIES (rolled back)
 Wound–Wait (preemptive):    older requests → WOUNDS (aborts) younger;  younger requests → WAITS
```

### Recovery
- **Log-based**: `<T start>`, `<T, X, old, new>`, `<T commit>`.
- **Deferred update** (NO-UNDO/REDO), **Immediate update** (UNDO/REDO).
- **Checkpoint** reduces log scanning. After crash: transactions committed after checkpoint → REDO; uncommitted → UNDO.
- **ARIES** (WAL, LSN, repeating history): Analysis → Redo → Undo.
- **WAL (Write-Ahead Logging)**: log record written to stable storage before data page.
- Shadow paging: no log needed; copy-on-write page table.

## 8. File Organisation & Indexing

An index is to a table what the index of a book is to its pages: a small, ordered structure that leads
straight to the wanted rows. B$^{+}$-trees dominate because they stay balanced and short even for very large
files.

| Index | Description |
|-------|-------------|
| Primary | On ordering **key** field; sparse (one entry per block) |
| Clustering | On ordering **non-key** field |
| Secondary | On non-ordering field; **dense** |
| Dense | Entry for every record |
| Sparse | Entry for some records (needs sorted file) |
| Multilevel | Index on index — log_fo(blocks) levels |

- A file can have **at most one primary or clustering index** but many secondary indexes.

### B-Tree vs B+ Tree

<!-- latex: p2-04-bplustree -->
```
 B+ tree of order 3 (internal: keys only, leaves linked)
                 [ 30 | 60 ]
               /      |      \
        [10|20]    [30|40]   [60|70|80]   ← leaves contain all keys,
           └──────►───┘──────►────┘          linked for range queries
```

| B-Tree | B+ Tree |
|--------|---------|
| Data pointers in all nodes | Data pointers only at leaves |
| No duplicate keys | Internal keys repeated in leaves |
| Leaves not linked | Leaves linked → efficient range/sequential access |
| Lower fan-out | Higher fan-out (internal nodes smaller) → fewer levels |

Order p (max children): every node ≤ p children; non-root internal ≥ ⌈p/2⌉ children; root ≥ 2.
**Order calculation**: block 1024 B, key 9 B, block pointer 6 B, record pointer 7 B.
- B+ internal: p·6 + (p−1)·9 ≤ 1024 → 15p ≤ 1033 → **p = 68**.
- B+ leaf: q(9 + 7) + 6 ≤ 1024 → **q = 63**.
- B-tree node: p·6 + (p−1)(9 + 7) ≤ 1024 → 22p ≤ 1040 → **p = 47**.

**Hashing**: static (overflow chains), dynamic — extendible hashing (directory doubles, global/local depth), linear hashing.

### Query Optimisation
- Heuristics: perform **selection early**, projection early, most restrictive selection first, avoid Cartesian products, replace × + σ with joins.
- Cost-based: estimate block transfers & seeks. Join algorithms: nested-loop (nr·bs + br), block nested-loop (br·bs + br), indexed, sort-merge, hash join.
- Query tree; equivalence rules (σ commutes, cascade of π, joins associative/commutative).

## 9. Advanced & Enhanced Databases

| Model | Notes |
|-------|-------|
| OODBMS | Objects, OID, inheritance; ODMG standard, OQL |
| ORDBMS | Relational + UDTs, inheritance (PostgreSQL, Oracle) |
| Temporal | Valid time & transaction time |
| Multimedia | Images, audio, video; content-based retrieval |
| Deductive | Facts + rules; **Datalog** (Prolog-like) |
| XML DB | XPath, XQuery; native XML DBs |
| Mobile | Intermittent connectivity, caching |
| GIS | Spatial data: raster/vector; R-trees, quad-trees |
| Genome | Biological sequence data |
| **Distributed DB** | Fragmentation (horizontal, vertical, mixed), replication, transparency; **2PC** (two-phase commit: prepare → commit) — blocking; 3PC non-blocking |

**Security**: discretionary (GRANT/REVOKE, `WITH GRANT OPTION`), mandatory (Bell-LaPadula: no read up, no write down), role-based access control, statistical DB inference control, encryption.

## 10. Data Warehousing & Mining

Operational databases record today's transactions; a data warehouse collects years of history from many
sources for analysis. Data mining then searches that history for patterns.

<!-- latex: p2-04-warehouse -->
```mermaid
flowchart LR
    S1[(OLTP sources)] --> ETL[ETL<br/>Extract, Transform, Load]
    S2[(Flat files)] --> ETL
    ETL --> DW[(Data warehouse<br/>subject-oriented, integrated,<br/>time-variant, non-volatile)]
    DW --> DM[Data marts]
    DW --> OLAP[OLAP cube]
    OLAP --> BI[Reports / dashboards / mining]
```

- Definition by **W.H. Inmon**: subject-oriented, integrated, time-variant, non-volatile. Kimball: dimensional modelling (bottom-up data marts).
- Schemas: **Star** (one fact table + denormalised dimensions), **Snowflake** (normalised dimensions), **Fact constellation / Galaxy** (multiple fact tables).
- OLAP operations: **roll-up** (aggregate up / drill-up), **drill-down**, **slice** (fix one dimension), **dice** (sub-cube on multiple), **pivot** (rotate).
- ROLAP (relational), MOLAP (multidimensional arrays), HOLAP (hybrid).
- Number of cuboids in n-dimensional cube without hierarchies: **2ⁿ**; with Lᵢ levels: Π(Lᵢ + 1).
- OLTP (current, detailed, many short transactions, normalised) vs OLAP (historical, summarised, complex queries, denormalised).

### Data mining (KDD process)
Selection → Pre-processing → Transformation → **Data mining** → Interpretation/Evaluation.

**Association rules** (Apriori):
<!-- latex: p2-04-association -->
```
Support(A→B)    = count(A ∪ B) / N
Confidence(A→B) = support(A ∪ B) / support(A)
Lift            = confidence(A→B) / support(B)    (>1 positive correlation)
Apriori property: every subset of a frequent itemset is frequent (anti-monotone)
FP-growth: no candidate generation (FP-tree)
```
- Classification (supervised): decision tree (ID3 – information gain, C4.5 – gain ratio, CART – Gini), Naive Bayes, k-NN, SVM.
- Clustering (unsupervised): k-means (partitioning), k-medoids (PAM), hierarchical (agglomerative/divisive), DBSCAN (density).
- Outlier detection, regression.

## 11. Big Data & NoSQL

When data become too large, too fast or too varied for a single relational server, systems distribute them
across many machines and often relax strict consistency in exchange for availability.

- **5 Vs**: Volume, Velocity, Variety, Veracity, Value (3 Vs originally — Doug Laney).
- Types: structured, semi-structured (JSON, XML), unstructured (text, video).
- **Hadoop**: HDFS (NameNode = master/metadata, DataNode = storage; default block 128 MB, replication 3) + **MapReduce** (Map → Shuffle & Sort → Reduce) + **YARN** (ResourceManager, NodeManager). Ecosystem: Hive (SQL-like), Pig (Pig Latin), HBase (column store), Sqoop (RDBMS ↔ HDFS), Flume (logs), ZooKeeper (coordination), Oozie (workflow), Spark (in-memory, RDDs).
- **CAP theorem** (Brewer): a distributed system can guarantee only **2 of 3**: Consistency, Availability, Partition tolerance. (CP: HBase, MongoDB; AP: Cassandra, CouchDB, DynamoDB.)
- **BASE**: Basically Available, Soft state, Eventual consistency (vs ACID).

| NoSQL type | Examples |
|-----------|----------|
| Key–value | Redis, DynamoDB, Riak |
| Document | MongoDB, CouchDB |
| Column-family | Cassandra, HBase, Bigtable |
| Graph | Neo4j, JanusGraph |

## 12. Deeper Dive — SQL on Real Tables, Minimal Cover, Full Normalisation & Schedules

### 12.1 SQL Worked on Sample Data

**EMP**

| eid | name | dept | salary |
|-----|------|------|--------|
| 1 | Asha | CS | 50000 |
| 2 | Ravi | CS | 40000 |
| 3 | Meena | EE | 45000 |
| 4 | John | EE | 30000 |
| 5 | Priya | ME | 60000 |
| 6 | Kiran | NULL | 35000 |

**DEPT**

| dept | building |
|------|----------|
| CS | B1 |
| EE | B2 |
| CE | B3 |

| # | Query | Result |
|---|-------|--------|
| 1 | `SELECT dept, COUNT(*), AVG(salary) FROM EMP GROUP BY dept HAVING COUNT(*) > 1` | (CS, 2, 45000), (EE, 2, 37500) |
| 2 | `SELECT name FROM EMP WHERE salary > (SELECT AVG(salary) FROM EMP)` | avg = 43333.33 → Asha, Meena, Priya |
| 3 | `SELECT COUNT(dept), COUNT(DISTINCT dept) FROM EMP` | 5, 3 (NULL ignored) |
| 4 | `EMP JOIN DEPT ON EMP.dept = DEPT.dept` | 4 rows (Asha, Ravi, Meena, John) |
| 5 | `EMP LEFT JOIN DEPT …` | 6 rows (Priya & Kiran get NULL building) |
| 6 | `EMP RIGHT JOIN DEPT …` | 5 rows (CE appears with NULL employee) |
| 7 | `EMP FULL OUTER JOIN DEPT …` | 7 rows |
| 8 | Correlated: `SELECT name FROM EMP e1 WHERE salary = (SELECT MAX(salary) FROM EMP e2 WHERE e2.dept = e1.dept)` | Asha, Meena, Priya (Kiran excluded: NULL = NULL is UNKNOWN) |
| 9 | `SELECT dept FROM DEPT WHERE dept NOT IN (SELECT dept FROM EMP)` | **Empty!** The subquery contains NULL, so every NOT IN test is UNKNOWN |
| 10 | Same with `NOT EXISTS (SELECT * FROM EMP WHERE EMP.dept = DEPT.dept)` | CE ✔ — NOT EXISTS is NULL-safe |

### 12.2 Minimal (Canonical) Cover — Worked

F = {A → BC, B → C, A → B, AB → C}
<!-- latex: p2-04-mincover -->
```
1. Split RHS:            A → B, A → C, B → C, A → B, AB → C
2. Remove duplicates:    A → B, A → C, B → C, AB → C
3. Extraneous LHS attr:  in AB → C, B is extraneous since A⁺ = {A, B, C} ∋ C  → A → C (duplicate)
4. Redundant FDs:        A → C follows from A → B and B → C → remove
Minimal cover Fc = { A → B, B → C }
```

### 12.3 Normalisation — From 1NF to BCNF

R(S, C, I, P, G) — Student, Course, Instructor, instructor Phone, Grade.
F = { SC → G, C → I, I → P }. S and C never appear on the right → **candidate key = SC**.

<!-- latex: p2-04-decomp -->
```mermaid
flowchart TD
    R["R(S, C, I, P, G)<br/>key SC — 1NF"] -->|"partial dependency C → I, P"| A["R1(S, C, G)"]
    R --> B["R2(C, I, P)<br/>2NF, transitive C → I → P"]
    B -->|"remove transitive dependency"| B1["R21(C, I)"]
    B --> B2["R22(I, P)"]
```
Final schema: **(S, C, G), (C, I), (I, P)** — every determinant is a key → BCNF; decomposition is lossless (common attributes C and I are keys of a side) and preserves all three FDs.

### 12.4 Recoverability Examples (W = write, R = read, C = commit)

| Schedule | Classification |
|----------|---------------|
| W1(A) R2(A) C2 C1 | **Not recoverable** — T2 commits after reading T1's uncommitted data, before T1 commits |
| W1(A) R2(A) C1 C2 | Recoverable, but not cascadeless (abort of T1 forces abort of T2) |
| W1(A) C1 R2(A) C2 | Cascadeless (reads only committed data) |
| W1(A) W2(A) C1 C2 | Cascadeless but **not strict** (T2 overwrote uncommitted A) |

### 12.5 Precedence Graphs

Schedule S: R1(A) W1(A) R2(A) W2(A) R1(B) W1(B) R2(B) W2(B)
<!-- latex: p2-04-prec-ok -->
```mermaid
flowchart LR
    T1((T1)) -->|"W1(A) before R2(A); W1(B) before R2(B)"| T2((T2))
```
Acyclic → conflict serializable, equivalent to serial order **T1 → T2**.

Schedule S′: R1(X) R2(Y) W2(X) W1(Y)
<!-- latex: p2-04-prec-cycle -->
```mermaid
flowchart LR
    T1((T1)) -->|"R1(X) before W2(X)"| T2((T2))
    T2 -->|"R2(Y) before W1(Y)"| T1
```
Cycle → **not** conflict serializable.

### 12.6 Two-Phase Locking — Lock Point

<!-- latex: p2-04-2pl -->
```
 locks held
   │        ╱‾‾‾‾╲
   │      ╱        ╲
   │    ╱  growing   ╲  shrinking
   │  ╱    phase      ╲   phase
   └──────────●──────────────────── time
          lock point (last lock acquired)
 Serializability order of 2PL transactions = order of their lock points
```

### 12.7 Extendible Hashing (sketch)

<!-- latex: p2-04-extendible -->
```
 Global depth 2                     Buckets (local depth)
 directory
  00 ──────────────►  [ 4, 12, 32 ]   (d = 2)
  01 ──────┐
  11 ──────┴───────►  [ 1, 5, 21 ]    (d = 1)  ← two directory entries share it
  10 ──────────────►  [ 10, 6 ]       (d = 2)
 Overflow of a bucket with local depth = global depth → directory doubles
 Overflow with local depth < global depth → split bucket only
```

### 12.8 Data Cube Lattice (3 dimensions → 2³ = 8 cuboids)

<!-- latex: p2-04-cuboids -->
```mermaid
flowchart TB
    A["(time, item, location)<br/>base cuboid"] --> B["(time, item)"]
    A --> C["(time, location)"]
    A --> D["(item, location)"]
    B --> E["(time)"]
    B --> F["(item)"]
    C --> E
    C --> G["(location)"]
    D --> F
    D --> G
    E --> H["( ) apex cuboid"]
    F --> H
    G --> H
```

---

## Previous Year Questions (PYQ pattern)

**Architecture & ER**
1. Ability to change the conceptual schema without changing application programs: **logical data independence**
2. The overall design of the database is called: **schema**
3. A weak entity set is represented by: **double rectangle**
4. Minimum number of tables for E1 (1)–R–(N) E2 with no attributes on R: **2**
5. Minimum tables for M:N relationship between two entities: **3**
6. Which is a DCL command? **GRANT**
7. TRUNCATE is a: **DDL command**

**Keys**

8. R(A,B,C,D) with only candidate key A — number of super keys: 2³ = **8**
9. R(A,B,C,D) with candidate keys A and B: 8 + 8 − 4 = **12**
10. Which key cannot be NULL? **Primary key**

**Relational algebra / SQL**

11. R has 10 tuples, S has 5; R × S has: **50**
12. Which RA operation answers "for all" queries? **Division**
13. Which is not a fundamental RA operation? (a) σ (b) π (c) ∩ (d) − — **Ans: (c)**
14. `SELECT COUNT(*)` vs `COUNT(salary)` on a table with 10 rows and 2 NULL salaries: **10 and 8**
15. HAVING is applied: **after GROUP BY on groups**
16. `salary > ALL (SELECT salary FROM emp WHERE dept = 5)` means: **greater than the maximum salary of dept 5**
17. Which set operator retains duplicates? **UNION ALL**
18. A trigger follows which model? **Event–Condition–Action**
19. Best protection against SQL injection: **parameterised/prepared statements**

**Normalisation**

20. R(A,B,C,D), F = {A→B, B→C, C→D}. Candidate key? **A**; Normal form? **2NF** (transitive dependencies exist)
21. R(A,B,C,D), F = {AB→C, C→D}. Key AB; C→D is transitive → **2NF**, not 3NF
22. R(A,B,C), F = {AB→C, C→A}. Keys AB, CB. Highest NF: **3NF** (C→A, A is prime)
23. Every relation with two attributes is in: **BCNF**
24. Decomposition of R(A,B,C) with A→B into (A,B),(A,C) is: **lossless** (common A → AB)
25. Which NF deals with multivalued dependency? **4NF**; join dependency? **5NF**
26. BCNF decomposition always guarantees: **lossless join** (not dependency preservation)
27. Closure of {A} under {A→B, B→C, C→D, D→E}: **ABCDE**

**Transactions**

28. Which ACID property is ensured by the concurrency control manager? **Isolation**
29. A schedule is conflict serializable iff its precedence graph is: **acyclic**
30. 2PL ensures: **conflict serializability** (not freedom from deadlock)
31. Strict 2PL avoids: **cascading rollbacks**
32. In wait-die, if an older transaction requests a lock held by a younger: **older waits**
33. In wound-wait, if an older transaction requests: **younger is aborted (wounded)**
34. Thomas' write rule modifies: **timestamp ordering protocol**
35. Number of serial schedules for 4 transactions: **24**
36. Reading uncommitted data is: **dirty read**
37. Write-ahead logging ensures: **log record on stable storage before data item**
38. After a crash, a transaction that has `<start>` and `<commit>` in log is: **redone**

**Indexing**

39. B+ tree leaves are linked to support: **range queries / sequential access**
40. Max number of primary indexes on a file: **1**
41. Order of B+ tree internal node: block 512 B, key 10 B, pointer 6 B: p·6 + (p−1)·10 ≤ 512 → 16p ≤ 522 → **p = 32**
42. Secondary index is usually: **dense**

**Warehousing / mining / big data**

43. Data warehouse is NOT: (a) subject-oriented (b) volatile (c) time-variant (d) integrated — **Ans: (b)**
44. OLAP operation that rotates the axes: **pivot**
45. Star schema has: **one fact table, denormalised dimension tables**
46. Support of {bread, butter} in 5 of 20 transactions: **25%**; if bread in 10 → confidence(bread→butter) = **50%**
47. Apriori uses the property: **all subsets of a frequent itemset are frequent**
48. CAP theorem: choose **2 of Consistency, Availability, Partition tolerance**
49. MongoDB is a: **document store**; Cassandra: **column-family**; Neo4j: **graph**
50. In Hadoop, metadata is stored by: **NameNode**
51. K-means is a: **partitioning clustering** algorithm

**More practice questions**

52. A NOT IN subquery whose result contains NULL returns: **no rows**
53. COUNT(DISTINCT dept) on values {CS, CS, EE, NULL}: **2**
54. Minimal cover of {A → B, B → C, A → C}: **{A → B, B → C}**
55. R(A, B, C, D), F = {A → B, C → D}. Candidate key: **AC**; highest normal form: **1NF** (partial dependencies)
56. A schedule in which transactions read only committed data is: **cascadeless**
57. Schedule R1(X) R2(Y) W2(X) W1(Y) is: **not conflict serializable**
58. In 2PL, the equivalent serial order follows the: **lock points**
59. In extendible hashing, the directory doubles when an overflowing bucket's local depth: **equals the global depth**
60. Number of cuboids for 4 dimensions without hierarchies: **16**
61. Apex cuboid represents: **the grand total (all dimensions aggregated)**
62. Full outer join of R (5 tuples) and S (3 tuples) with 2 matching pairs (one-to-one): 2 + 3 + 1 = **6 tuples**

## Quick Revision Box
- 3NF: X superkey OR A prime · BCNF: X superkey
- Lossless: (R1∩R2) → R1 or R2 · 3NF = lossless + dep. preserving
- Conflict serializable ⇔ acyclic precedence graph · 2PL → serializable but deadlock possible
- Wait-die: old waits, young dies · Wound-wait: old wounds, young waits
- CAP: pick 2 · HDFS NameNode/DataNode · MapReduce Map→Shuffle→Reduce
