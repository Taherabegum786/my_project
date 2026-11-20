# Set 7 — Transaction Processing and Concurrency Control (ACID, schedules, serializability, recoverability, locking, timestamps)

**46 questions** — High: 23, Medium: 22, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (ACID property): A. Atomicity  B. Consistency  C. Isolation  D. Durability  
List II (Responsible component or meaning): I. Recovery manager ensures committed changes survive failures  II. Concurrency-control manager makes concurrent execution look serial  III. Transaction is all-or-nothing, ensured by the recovery (undo) mechanism  IV. A correct transaction preserves database integrity constraints; responsibility of the programmer

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-IV, C-II, D-I  
(3) A-IV, B-III, C-II, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — ACID properties and the components that enforce them.

</details>

**Q2.** `High`  
Arrange the transaction states in the order a successful transaction passes through them.  
A. Committed  B. Active  C. Partially committed

(1) C, B, A  
(2) A, B, C  
(3) B, A, C  
(4) B, C, A  

<details><summary>Answer</summary>

**(4)** — A failing transaction goes from active or partially committed to failed and then aborted.

</details>

**Q3.** `High`  
Consider the schedule S: r1(A) w1(A) r2(A) w2(A) r1(B) w1(B) r2(B) w2(B). Which statement is correct?

(1) S is not view serializable  
(2) S is conflict serializable and equivalent to T1 followed by T2  
(3) S is conflict serializable and equivalent to T2 followed by T1  
(4) S is not conflict serializable  

<details><summary>Answer</summary>

**(2)** — All conflicting pairs order T1 before T2, so the precedence graph has only the edge T1 → T2.

</details>

**Q4.** `High`  
Consider the schedule S: r1(A) r2(A) w1(A) w2(A). Which statement is correct?

(1) S is a serial schedule  
(2) S is conflict serializable  
(3) S is neither conflict serializable nor view serializable  
(4) S is view serializable but not conflict serializable  

<details><summary>Answer</summary>

**(3)** — r2(A) before w1(A) gives T2 → T1, and r1(A) before w2(A) gives T1 → T2: a cycle (a lost update). With no blind writes, it is not view serializable either.

</details>

**Q5.** `High`  
Consider the schedule S: r1(A) w2(A) w1(A) w3(A). Which statement is correct?

(1) S is view serializable but not conflict serializable  
(2) S is serial  
(3) S is neither view nor conflict serializable  
(4) S is conflict serializable  

<details><summary>Answer</summary>

**(1)** — The precedence graph has a cycle between T1 and T2, but S is view equivalent to T1, T2, T3 because w2(A) and w1(A) are blind writes overwritten by T3.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: Every conflict-serializable schedule is view serializable.  
Statement II: Every view-serializable schedule is conflict serializable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A view-serializable schedule that is not conflict serializable must contain blind writes.

</details>

**Q7.** `High`  
Consider the schedule S: r1(X) r2(Z) r1(Z) r3(X) r3(Y) w1(X) w3(Y) r2(Y) w2(Z) w2(Y). The equivalent serial order is

(1) T1, T2, T3  
(2) S is not conflict serializable  
(3) T2, T3, T1  
(4) T3, T1, T2  

<details><summary>Answer</summary>

**(4)** — Edges: T3 → T1 (r3(X) before w1(X)), T1 → T2 (r1(Z) before w2(Z)) and T3 → T2 (w3(Y) before r2(Y)); the topological order is T3, T1, T2.

</details>

**Q8.** `Medium`  
Consider the schedule S: r1(X) w1(X) r2(X) w2(X) r2(Y) w2(Y) r1(Y) w1(Y). Which statement is correct?

(1) S is serial  
(2) S is not conflict serializable  
(3) S is conflict serializable as T1, T2  
(4) S is conflict serializable as T2, T1  

<details><summary>Answer</summary>

**(2)** — On X, T1 precedes T2; on Y, T2 precedes T1, giving a cycle.

</details>

**Q9.** `High`  
Conflict serializability of a schedule is tested by

(1) checking that every transaction commits  
(2) checking that the precedence graph is acyclic  
(3) counting the number of locks  
(4) checking that no transaction reads uncommitted data  

<details><summary>Answer</summary>

**(2)** — If the precedence graph has no cycle, a topological sort gives an equivalent serial order.

</details>

**Q10.** `Medium`  
Two operations in a schedule conflict if they belong to different transactions, access the same data item, and

(1) at least one of them is a write  
(2) both are reads  
(3) they are adjacent  
(4) both are writes only  

<details><summary>Answer</summary>

**(1)** — Read-read pairs never conflict.

</details>

**Q11.** `High`  
Transaction T1 has 3 operations and T2 has 2 operations. The number of possible concurrent schedules (interleavings preserving each transaction's internal order) is

(1) 20  
(2) 10  
(3) 6  
(4) 5  

<details><summary>Answer</summary>

**(2)** — C(5, 2) = 10.

</details>

**Q12.** `Medium`  
Three transactions T1, T2 and T3 each have 2 operations. The number of possible interleaved schedules is

(1) 90  
(2) 36  
(3) 6  
(4) 720  

<details><summary>Answer</summary>

**(1)** — 6! / (2! × 2! × 2!) = 90.

</details>

**Q13.** `Medium`  
For n transactions, the number of different serial schedules is

(1) n!  
(2) n²  
(3) n  
(4) 2^n  

<details><summary>Answer</summary>

**(1)** — Any ordering of the n transactions is a serial schedule.

</details>

**Q14.** `High`  
Match List I with List II.  
List I (Schedule property): A. Recoverable  B. Cascadeless  C. Strict  
List II (Condition): I. No transaction reads or overwrites an item written by an uncommitted transaction  II. If Tj reads an item written by Ti, then Ti commits before Tj commits  III. No transaction reads an item written by an uncommitted transaction

(1) A-III, B-II, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-I, C-III  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — Strict ⊆ cascadeless ⊆ recoverable.

</details>

**Q15.** `High`  
In a schedule, T2 reads a value written by T1 and T2 commits before T1. If T1 later aborts, the schedule is

(1) cascadeless  
(2) strict  
(3) recoverable  
(4) non-recoverable  

<details><summary>Answer</summary>

**(4)** — T2 has committed a value that never officially existed; the DBMS cannot undo T2.

</details>

**Q16.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Cascadeless schedules avoid cascading rollbacks.  
Reason R: In a cascadeless schedule, transactions read only values written by committed transactions.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — If no one reads uncommitted data, aborting one transaction cannot force others to roll back.

</details>

**Q17.** `High`  
Match List I with List II.  
List I (Concurrency problem): A. Lost update  B. Dirty read  C. Unrepeatable read  D. Phantom  
List II (Description): I. A transaction reads data written by an uncommitted transaction  II. Rows satisfying a condition appear when the query is re-executed because another transaction inserted them  III. An update by one transaction is overwritten by another  IV. A transaction reads the same item twice and gets different values

(1) A-I, B-III, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-I, C-II, D-IV  

<details><summary>Answer</summary>

**(3)** — Classic anomalies of concurrent execution.

</details>

**Q18.** `High`  
Match List I with List II.  
List I (SQL isolation level): A. Read uncommitted  B. Read committed  C. Repeatable read  D. Serializable  
List II (Anomaly still possible): I. None of dirty read, non-repeatable read or phantom  II. Phantoms only  III. Non-repeatable reads and phantoms  IV. Dirty reads, non-repeatable reads and phantoms

(1) A-IV, B-III, C-I, D-II  
(2) A-IV, B-II, C-III, D-I  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-II, D-I  

<details><summary>Answer</summary>

**(4)** — SQL-92 isolation levels and the phenomena they allow.

</details>

**Q19.** `High`  
Given below are two statements.  
Statement I: Basic two-phase locking guarantees freedom from deadlock.  
Statement II: Basic two-phase locking guarantees conflict serializability.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — 2PL can deadlock; deadlock handling is needed separately.

</details>

**Q20.** `High`  
In two-phase locking, the point at which a transaction acquires its final lock is called its

(1) save point  
(2) commit point  
(3) lock point  
(4) checkpoint  

<details><summary>Answer</summary>

**(3)** — Serializability order corresponds to the order of the lock points.

</details>

**Q21.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Strict two-phase locking produces cascadeless schedules.  
Reason R: Basic two-phase locking has a growing phase and a shrinking phase.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but A holds because strict 2PL keeps exclusive locks until commit or abort, which R does not mention.

</details>

**Q22.** `Medium`  
In rigorous two-phase locking, a transaction

(1) holds all locks, shared and exclusive, until it commits or aborts  
(2) releases shared locks early but holds exclusive locks  
(3) never uses shared locks  
(4) acquires all locks before it starts  

<details><summary>Answer</summary>

**(1)** — Under rigorous 2PL, transactions can be serialized in the order in which they commit.

</details>

**Q23.** `Medium`  
Conservative (static) two-phase locking

(1) allows lock upgrades  
(2) releases all locks at commit  
(3) acquires all locks before the transaction starts executing and is deadlock-free  
(4) never blocks  

<details><summary>Answer</summary>

**(3)** — If any lock is unavailable, the transaction waits without holding any locks.

</details>

**Q24.** `High`  
In the lock-compatibility matrix, which of the following pairs of lock requests on the same item are compatible?

(1) Shared and exclusive  
(2) Exclusive and exclusive  
(3) Shared and shared  
(4) Exclusive and shared  

<details><summary>Answer</summary>

**(3)** — Several transactions can read an item simultaneously, but a write needs an exclusive lock.

</details>

**Q25.** `High`  
Match List I with List II.  
List I (Intention lock mode): A. IS  B. IX  C. SIX  
List II (Meaning): I. Explicit shared lock on the node with intent to set exclusive locks lower down  II. Intent to set shared locks at a finer granularity  III. Intent to set exclusive or shared locks at a finer granularity

(1) A-I, B-III, C-II  
(2) A-II, B-III, C-I  
(3) A-III, B-II, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(2)** — Intention locks are used in multiple-granularity locking.

</details>

**Q26.** `Medium`  
In multiple-granularity locking, which of the following pairs of lock modes is compatible?

(1) X and IS  
(2) SIX and IX  
(3) IX and IX  
(4) IX and S  

<details><summary>Answer</summary>

**(3)** — IX is compatible with IS and IX; S is compatible only with IS and S.

</details>

**Q27.** `High`  
In basic timestamp ordering, transaction T issues write(Q) and TS(T) < R-timestamp(Q). The protocol

(1) rejects the write and rolls back T  
(2) executes the write  
(3) ignores the write  
(4) delays T  

<details><summary>Answer</summary>

**(1)** — A younger transaction has already read Q, so the value T would write is needed too late.

</details>

**Q28.** `High`  
Thomas' write rule modifies the timestamp-ordering protocol so that, when TS(T) < W-timestamp(Q) for a write(Q),

(1) the obsolete write is ignored  
(2) T waits  
(3) the write is executed and W-timestamp(Q) is decreased  
(4) T is rolled back  

<details><summary>Answer</summary>

**(1)** — Ignoring the outdated write allows some view-serializable schedules that are not conflict serializable.

</details>

**Q29.** `High`  
Given below are two statements.  
Statement I: The timestamp-ordering protocol ensures freedom from deadlock.  
Statement II: The timestamp-ordering protocol always produces recoverable schedules.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — No transaction ever waits, so there is no deadlock; but schedules may be non-recoverable unless extended (for example by delaying commits).

</details>

**Q30.** `High`  
Match List I with List II.  
List I (Deadlock prevention scheme): A. Wait-die  B. Wound-wait  
List II (When an older transaction requests a lock held by a younger one): I. The older transaction waits  II. The younger transaction is rolled back (wounded)

(1) A-I, B-II  
(2) A-II, B-I  
(3) Both I  
(4) Both II  

<details><summary>Answer</summary>

**(1)** — In wait-die an older requester waits and a younger requester dies; in wound-wait an older requester wounds the younger holder and a younger requester waits.

</details>

**Q31.** `Medium`  
In both wait-die and wound-wait, a transaction that is rolled back restarts with

(1) its original timestamp  
(2) a new, larger timestamp  
(3) the timestamp of the transaction that caused the rollback  
(4) timestamp zero  

<details><summary>Answer</summary>

**(1)** — Keeping the original timestamp ensures it eventually becomes the oldest, preventing starvation.

</details>

**Q32.** `Medium`  
Arrange the phases of validation-based (optimistic) concurrency control in order.  
A. Write phase  B. Read phase  C. Validation phase

(1) C, B, A  
(2) B, A, C  
(3) B, C, A  
(4) A, B, C  

<details><summary>Answer</summary>

**(3)** — Transactions work on local copies, validate, then write if validation succeeds.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: Optimistic concurrency control acquires locks before reading every item.  
Statement II: Optimistic concurrency control performs well when conflicts between transactions are rare.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Optimistic methods use no locks; they check for conflicts at validation time.

</details>

**Q34.** `Medium`  
In multiversion timestamp ordering

(1) deadlocks are frequent  
(2) write operations never fail  
(3) only one version of each item is kept  
(4) read operations never fail or wait  

<details><summary>Answer</summary>

**(4)** — A read returns the appropriate older version; writes may still cause rollbacks.

</details>

**Q35.** `Medium`  
Snapshot isolation, used in several commercial DBMSs, can still allow which anomaly?

(1) Dirty reads  
(2) Non-repeatable reads within a transaction  
(3) Write skew  
(4) Lost updates (under first-committer-wins)  

<details><summary>Answer</summary>

**(3)** — Two transactions reading overlapping data and writing disjoint items can violate a constraint.

</details>

**Q36.** `Medium`  
The phantom problem can be prevented by

(1) increasing the buffer size  
(2) using only shared locks  
(3) timestamping each tuple  
(4) index locking or predicate locking  

<details><summary>Answer</summary>

**(4)** — Locks on the index ranges or predicates also cover tuples that do not yet exist.

</details>

**Q37.** `Medium`  
In the tree protocol (a graph-based locking protocol)

(1) the first lock may be on any item, and later an item can be locked only if its parent is currently locked  
(2) it may cause deadlock  
(3) all locks are acquired at the start  
(4) it guarantees recoverability  

<details><summary>Answer</summary>

**(1)** — The tree protocol is deadlock-free and allows earlier unlocking than 2PL.

</details>

**Q38.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Starvation can occur in locking protocols.  
Reason R: A transaction may repeatedly be chosen as the victim of deadlock resolution or may wait while a stream of shared locks is granted.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The lock manager must grant requests fairly to avoid it.

</details>

**Q39.** `Medium`  
The deadlock detection approach in a DBMS uses a

(1) B+ tree  
(2) ER diagram  
(3) wait-for graph  
(4) precedence graph  

<details><summary>Answer</summary>

**(3)** — A cycle in the wait-for graph indicates a deadlock; a victim is then rolled back.

</details>

**Q40.** `Medium`  
Consider the schedule S: r2(X) r1(X) w2(X) r3(X) w1(X). Which statement is correct?

(1) S is serial  
(2) S is conflict serializable as T1, T2, T3  
(3) S is conflict serializable as T2, T3, T1  
(4) S is not conflict serializable  

<details><summary>Answer</summary>

**(4)** — r1(X) before w2(X) gives T1 → T2, and w2(X) before w1(X) gives T2 → T1, so there is a cycle.

</details>

**Q41.** `Medium`  
A schedule in which the operations of each transaction are executed consecutively, without interleaving, is called a

(1) serial schedule  
(2) serializable schedule  
(3) strict schedule  
(4) cascadeless schedule  

<details><summary>Answer</summary>

**(1)** — Every serial schedule is serializable.

</details>

**Q42.** `Medium`  
Given below are two statements.  
Statement I: Testing whether a schedule is view serializable is NP-complete.  
Statement II: Testing whether a schedule is conflict serializable can be done in polynomial time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Conflict serializability needs only a cycle check on the precedence graph.

</details>

**Q43.** `Medium`  
A transaction that has executed its final statement but whose output may still be in main memory is in the

(1) partially committed state  
(2) committed state  
(3) aborted state  
(4) active state  

<details><summary>Answer</summary>

**(1)** — A hardware failure at this point could still prevent its successful completion.

</details>

**Q44.** `Medium`  
Under two-phase locking, which of the following sequences for a single transaction is NOT allowed?

(1) lock-S(A), lock-X(B), unlock(A), unlock(B)  
(2) lock-X(A), unlock(A), lock-X(B), unlock(B)  
(3) lock-S(A), lock-S(B), unlock(B), unlock(A)  
(4) lock-X(A), lock-X(B), unlock(B), unlock(A)  

<details><summary>Answer</summary>

**(2)** — After unlock(A) begins the shrinking phase, no new lock can be acquired.

</details>

**Q45.** `Medium`  
Lock conversion from shared to exclusive (upgrade) under two-phase locking is permitted only during

(1) the growing phase  
(2) the commit phase  
(3) the validation phase  
(4) the shrinking phase  

<details><summary>Answer</summary>

**(1)** — Downgrades are allowed only in the shrinking phase.

</details>

**Q46.** `Low`  
The component of a DBMS that keeps track of the locks held and granted is the

(1) buffer manager  
(2) log manager  
(3) lock manager  
(4) query optimizer  

<details><summary>Answer</summary>

**(3)** — It maintains a lock table, often a hash table keyed by data item.

</details>
