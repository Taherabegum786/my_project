# Set 8 — Database Recovery, Security and Authorization

**34 questions** — High: 11, Medium: 22, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Recovery technique): A. Deferred update  B. Immediate update  C. Shadow paging  
List II (Operations needed after a crash): I. NO-UNDO/NO-REDO  II. NO-UNDO/REDO  III. UNDO/REDO

(1) A-II, B-I, C-III  
(2) A-II, B-III, C-I  
(3) A-I, B-III, C-II  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(2)** — Deferred update writes nothing to the database before commit; shadow paging switches page tables atomically at commit.

</details>

**Q2.** `High`  
The write-ahead logging (WAL) rule requires that

(1) log records be written only at commit  
(2) the log records for an update be written to stable storage before the updated data page is written to disk  
(3) the log be deleted after each checkpoint  
(4) data pages be written before log records  

<details><summary>Answer</summary>

**(2)** — Also, all log records of a transaction must be forced before it commits.

</details>

**Q3.** `High`  
A log contains, in order: &lt;T1 start&gt;, &lt;T1, A, 10, 20&gt;, &lt;T2 start&gt;, &lt;T1 commit&gt;, &lt;checkpoint {T2}&gt;, &lt;T3 start&gt;, &lt;T2, B, 5, 15&gt;, &lt;T3, C, 7, 9&gt;, &lt;T3 commit&gt;, and then the system crashes. With immediate update, the recovery manager must

(1) undo T3 and redo T2  
(2) undo T2 and redo T3  
(3) undo T1 and T2  
(4) redo T1, T2 and T3  

<details><summary>Answer</summary>

**(2)** — T1 committed before the checkpoint, so its updates are already on disk; T3 committed after it and must be redone; T2 never committed and must be undone.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: A checkpoint reduces the amount of the log that must be scanned during recovery.  
Statement II: Transactions that committed before the last checkpoint must be redone after a crash.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Their changes were flushed to disk at the checkpoint, so they need neither undo nor redo.

</details>

**Q5.** `High`  
Match List I with List II.  
List I (Buffer policy): A. Steal  B. No-steal  C. Force  D. No-force  
List II (Meaning): I. Pages updated by a transaction are written to disk when it commits  II. Updated pages may be written before commit, so UNDO is needed  III. Updated pages need not be written at commit, so REDO is needed  IV. Updated pages cannot be written to disk before commit

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(3)** — Most real systems use steal/no-force, which requires both UNDO and REDO.

</details>

**Q6.** `High`  
Arrange the phases of the ARIES recovery algorithm in order.  
A. Undo  B. Analysis  C. Redo

(1) B, A, C  
(2) A, B, C  
(3) B, C, A  
(4) C, B, A  

<details><summary>Answer</summary>

**(3)** — Analysis finds dirty pages and active transactions; redo repeats history; undo rolls back losers.

</details>

**Q7.** `Medium`  
Given below are two statements.  
Statement I: ARIES uses a log sequence number (LSN) stored in each page to avoid redoing updates that are already on disk.  
Statement II: During undo, ARIES writes compensation log records (CLRs).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — CLRs are redo-only records that make undo idempotent across repeated crashes.

</details>

**Q8.** `Medium`  
An update log record of the form &lt;Ti, X, V1, V2&gt; contains

(1) only the new value  
(2) the transaction, data item, old value and new value  
(3) the transaction, data item and commit time  
(4) the data item and its lock mode  

<details><summary>Answer</summary>

**(2)** — The old value is used for undo and the new value for redo.

</details>

**Q9.** `Medium`  
In shadow paging, a disadvantage is

(1) that it cannot handle a single transaction  
(2) that it requires UNDO after a crash  
(3) data fragmentation and the overhead of copying page tables, plus garbage collection  
(4) the need for a log for every update  

<details><summary>Answer</summary>

**(3)** — Updated pages change location on disk, which destroys clustering.

</details>

**Q10.** `Medium`  
A failure that destroys the contents of non-volatile storage, such as a head crash, is recovered using

(1) the buffer pool  
(2) the log only  
(3) shadow pages  
(4) a backup (archival dump) together with the log  

<details><summary>Answer</summary>

**(4)** — Media failure requires restoring from a backup and replaying the archived log.

</details>

**Q11.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In deferred update, every transaction must be undone after a crash.  
Reason R: Updates are applied to the database only after the transaction reaches its commit point.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Because of R, uncommitted transactions never changed the database, so no UNDO is needed.

</details>

**Q12.** `Medium`  
Match List I with List II.  
List I (Storage type): A. Volatile storage  B. Non-volatile storage  C. Stable storage  
List II (Example): I. Information is never lost; approximated by replicating on several disks  II. Main memory and cache  III. Disk and flash memory

(1) A-III, B-II, C-I  
(2) A-II, B-I, C-III  
(3) A-II, B-III, C-I  
(4) A-I, B-III, C-II  

<details><summary>Answer</summary>

**(3)** — The log is kept on stable storage.

</details>

**Q13.** `Medium`  
In recovery, a "redo" of an operation must be

(1) idempotent: performing it several times has the same effect as performing it once  
(2) non-idempotent  
(3) performed in reverse order  
(4) performed only once  

<details><summary>Answer</summary>

**(1)** — A crash during recovery may cause the same redo to be repeated.

</details>

**Q14.** `High`  
A user grants a privilege WITH GRANT OPTION. This means that the recipient

(1) can revoke privileges from the grantor  
(2) cannot use the privilege  
(3) becomes the owner of the table  
(4) can pass the privilege on to other users  

<details><summary>Answer</summary>

**(4)** — Revoking with CASCADE then also removes the privileges the recipient granted.

</details>

**Q15.** `High`  
User A grants SELECT on a table to B WITH GRANT OPTION, and B grants it to C. If A revokes the privilege from B with CASCADE,

(1) neither loses it  
(2) both B and C lose the privilege (unless C has it from another source)  
(3) only C loses the privilege  
(4) only B loses the privilege  

<details><summary>Answer</summary>

**(2)** — C's privilege depended on B's grant, so it is removed when B's is.

</details>

**Q16.** `High`  
Match List I with List II.  
List I (Access control model): A. Discretionary access control  B. Mandatory access control  C. Role-based access control  
List II (Description): I. Privileges are assigned to roles, which are assigned to users  II. Owners grant and revoke privileges using GRANT and REVOKE  III. Access is based on security classes of subjects and objects, set by system policy

(1) A-II, B-III, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-I, C-III  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(1)** — DAC, MAC and RBAC.

</details>

**Q17.** `High`  
In the Bell-LaPadula model, the simple security property and the \*-property state respectively that

(1) subjects may read down and write down  
(2) a subject may not read an object of higher classification, and may not write an object of lower classification  
(3) a subject may read and write any object  
(4) a subject may not write up, and may not read down  

<details><summary>Answer</summary>

**(2)** — "No read up" and "no write down" prevent information flowing to lower classes.

</details>

**Q18.** `Medium`  
Given below are two statements.  
Statement I: Views can be used as a security mechanism to hide certain rows or columns from users.  
Statement II: A user who has been granted SELECT on a view automatically has SELECT on its base tables.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Users can be given access to a view without any privilege on the underlying tables.

</details>

**Q19.** `Medium`  
The problem of deducing confidential individual information from aggregate queries in a statistical database is called the

(1) impedance mismatch  
(2) phantom problem  
(3) lost update problem  
(4) inference problem  

<details><summary>Answer</summary>

**(4)** — Countermeasures include minimum query-set sizes and adding noise.

</details>

**Q20.** `Medium`  
Polyinstantiation in multilevel secure databases means

(1) several users share one account  
(2) a query has several plans  
(3) a table has several indexes  
(4) several tuples with the same key exist at different security classification levels  

<details><summary>Answer</summary>

**(4)** — It prevents low-clearance users from inferring the existence of high-classification data.

</details>

**Q21.** `Medium`  
Which SQL statement gives user Ravi the privilege to insert rows into table EMP?

(1) GRANT INSERT ON EMP TO Ravi  
(2) GRANT EMP INSERT Ravi  
(3) PERMIT Ravi INSERT EMP  
(4) ALLOW INSERT EMP Ravi  

<details><summary>Answer</summary>

**(1)** — The general form is GRANT privileges ON object TO users [WITH GRANT OPTION].

</details>

**Q22.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Encrypting data stored in a database protects it even if the storage media are stolen.  
Reason R: Encryption prevents authorised users from querying the data.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Authorised users with the key can still query the data; R is false.

</details>

**Q23.** `Medium`  
A database audit trail is

(1) the transaction log used for recovery only  
(2) a log of database accesses and operations, with the user and time, used for security review  
(3) a list of indexes  
(4) a backup copy  

<details><summary>Answer</summary>

**(2)** — Auditing helps detect misuse and is required by many regulations.

</details>

**Q24.** `Medium`  
Which of the following is a countermeasure against inference attacks on statistical databases?

(1) Removing indexes  
(2) Increasing the buffer size  
(3) Granting more privileges  
(4) Refusing queries whose result set is too small  

<details><summary>Answer</summary>

**(4)** — Other methods include partitioning the database and perturbing results.

</details>

**Q25.** `Medium`  
In Oracle-style DBMSs, a named collection of privileges that can be granted to users is called a

(1) view  
(2) role  
(3) schema  
(4) synonym  

<details><summary>Answer</summary>

**(2)** — Roles simplify the administration of privileges.

</details>

**Q26.** `Medium`  
Given below are two statements.  
Statement I: After a system crash, transactions that were active at the time of the crash must be rolled back.  
Statement II: After a system crash, transactions whose commit record is in the log must be redone if their updates may not have reached disk.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Losers are undone; winners are redone (subject to checkpoints).

</details>

**Q27.** `Medium`  
A log with &lt;T1 start&gt;, &lt;T1, A, 100, 200&gt;, &lt;T1, B, 50, 60&gt;, followed by a crash (no commit record for T1), is recovered under immediate update by

(1) setting A = 200 and B = 60  
(2) leaving A and B unchanged  
(3) setting A = 100 and B = 50  
(4) setting A = 200 and B = 50  

<details><summary>Answer</summary>

**(3)** — T1 did not commit, so it is undone using the old values, in reverse order.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: A fuzzy checkpoint requires all transactions to stop while dirty pages are written to disk.  
Statement II: In a simple (quiescent) checkpoint, new transactions are not allowed to start while the checkpoint is taken.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A fuzzy checkpoint lets transactions continue while dirty pages are written.

</details>

**Q29.** `Medium`  
Which of the following is NOT a type of failure considered in database recovery?

(1) Disk (media) failure  
(2) System crash  
(3) Transaction failure  
(4) Query optimization failure  

<details><summary>Answer</summary>

**(4)** — A poor plan is a performance problem, not a failure needing recovery.

</details>

**Q30.** `Medium`  
Remote backup systems provide high availability by

(1) keeping a copy of the database at a remote site that is kept up to date by shipping log records  
(2) using RAID 0  
(3) disabling transactions  
(4) backing up to tape weekly  

<details><summary>Answer</summary>

**(1)** — If the primary fails, the backup takes over.

</details>

**Q31.** `Medium`  
Given below are two statements.  
Statement I: SQL injection is possible only in web applications written in PHP.  
Statement II: Input validation alone is a complete defence against SQL injection.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Any language that builds SQL strings from input is vulnerable, and prepared statements are the primary defence.

</details>

**Q32.** `Medium`  
In SQL, the REVOKE statement with the RESTRICT option

(1) revokes privileges from all users  
(2) always revokes the privilege  
(3) grants the privilege back  
(4) fails if revoking would cause other privileges to be revoked in cascade  

<details><summary>Answer</summary>

**(4)** — CASCADE removes dependent privileges as well.

</details>

**Q33.** `Low`  
A user who owns a table automatically has

(1) all privileges on it, including the right to grant them  
(2) no privileges on it  
(3) only INSERT privilege  
(4) only SELECT privilege  

<details><summary>Answer</summary>

**(1)** — The creator (owner) of an object holds every privilege on it.

</details>

**Q34.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Log records must be written to stable storage before the transaction's commit record is considered complete.  
Reason R: Otherwise a committed transaction's updates could be lost in a crash, violating durability.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This is the commit rule of write-ahead logging.

</details>
