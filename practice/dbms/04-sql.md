# Set 4 — SQL (DDL, constraints, queries, NULLs, joins, subqueries, views, stored procedures, triggers, SQL injection)

**51 questions** — High: 18, Medium: 32, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). The query SELECT COUNT(*), COUNT(salary) FROM EMP returns

(1) 4 and 4  
(2) 6 and 4  
(3) 6 and 6  
(4) 4 and 6  

<details><summary>Answer</summary>

**(2)** — COUNT(*) counts rows; COUNT(column) ignores NULLs.

</details>

**Q2.** `High`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). The query SELECT AVG(salary) FROM EMP returns

(1) 55000  
(2) NULL  
(3) 36666.67  
(4) 44000  

<details><summary>Answer</summary>

**(1)** — AVG ignores NULLs: 220000 / 4 = 55000.

</details>

**Q3.** `High`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). How many rows does SELECT dept, COUNT(*) FROM EMP GROUP BY dept HAVING COUNT(*) > 1 return?

(1) 2  
(2) 6  
(3) 3  
(4) 1  

<details><summary>Answer</summary>

**(1)** — CS has 3 rows and EE has 2; ME has only 1.

</details>

**Q4.** `High`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). How many rows does SELECT * FROM EMP WHERE salary > 45000 OR salary <= 45000 return?

(1) 0  
(2) 4  
(3) 2  
(4) 6  

<details><summary>Answer</summary>

**(2)** — For the two NULL salaries both comparisons are UNKNOWN, so those rows are not returned.

</details>

**Q5.** `Medium`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). How many rows does SELECT * FROM EMP WHERE salary BETWEEN 40000 AND 60000 return?

(1) 2  
(2) 5  
(3) 4  
(4) 3  

<details><summary>Answer</summary>

**(4)** — 40000, 50000 and 60000; BETWEEN is inclusive and NULLs do not qualify.

</details>

**Q6.** `Medium`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). Which names are returned by SELECT name FROM EMP WHERE name LIKE '_s%'?

(1) Asha only  
(2) Asha, Bala and Esha  
(3) Esha only  
(4) Asha and Esha  

<details><summary>Answer</summary>

**(4)** — _ matches exactly one character, so the second letter must be s.

</details>

**Q7.** `Medium`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). How many rows does SELECT * FROM EMP WHERE dept = 'CS' AND salary <> 50000 return?

(1) 0  
(2) 2  
(3) 3  
(4) 1  

<details><summary>Answer</summary>

**(4)** — Only Bala (60000); Farhan's NULL salary makes the condition UNKNOWN.

</details>

**Q8.** `Medium`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). The number of rows returned by SELECT * FROM EMP E1, EMP E2 WHERE E1.salary > E2.salary is

(1) 4  
(2) 6  
(3) 36  
(4) 12  

<details><summary>Answer</summary>

**(2)** — Among the four non-null salaries there are C(4, 2) = 6 ordered pairs with E1 higher.

</details>

**Q9.** `High`  
Table T1(x) contains 1, 2, 2, 3 and NULL; table T2(x) contains 2, 3 and 4. How many rows does SELECT * FROM T2 WHERE x NOT IN (SELECT x FROM T1) return?

(1) 1  
(2) 3  
(3) 2  
(4) 0  

<details><summary>Answer</summary>

**(4)** — For x = 4, "4 NOT IN (1, 2, 2, 3, NULL)" is UNKNOWN because of the NULL, so no row qualifies.

</details>

**Q10.** `High`  
Table T1(x) contains 1, 2, 2, 3 and NULL; table T2(x) contains 2, 3 and 4. The numbers of rows returned by SELECT x FROM T1 UNION SELECT x FROM T2 and by SELECT x FROM T1 UNION ALL SELECT x FROM T2 are respectively

(1) 4 and 8  
(2) 5 and 7  
(3) 5 and 8  
(4) 4 and 7  

<details><summary>Answer</summary>

**(3)** — UNION removes duplicates, giving 1, 2, 3, NULL, 4; UNION ALL keeps all 5 + 3 rows.

</details>

**Q11.** `Medium`  
Table T1(x) contains 1, 2, 2, 3 and NULL. The query SELECT COUNT(x), COUNT(*), COUNT(DISTINCT x) FROM T1 returns

(1) 5, 5, 4  
(2) 4, 5, 3  
(3) 5, 4, 3  
(4) 4, 4, 3  

<details><summary>Answer</summary>

**(2)** — COUNT(x) and COUNT(DISTINCT x) ignore NULL.

</details>

**Q12.** `High`  
In SQL, the result of comparing NULL = NULL is

(1) an error  
(2) FALSE  
(3) UNKNOWN  
(4) TRUE  

<details><summary>Answer</summary>

**(3)** — To test for NULL, IS NULL must be used.

</details>

**Q13.** `High`  
In SQL three-valued logic, which of the following evaluates to TRUE?

(1) NOT UNKNOWN  
(2) UNKNOWN OR TRUE  
(3) UNKNOWN AND FALSE  
(4) UNKNOWN AND TRUE  

<details><summary>Answer</summary>

**(2)** — UNKNOWN OR TRUE is TRUE; UNKNOWN AND FALSE is FALSE; the others are UNKNOWN.

</details>

**Q14.** `High`  
Arrange the clauses of an SQL SELECT statement in their logical order of evaluation.  
A. SELECT  B. WHERE  C. GROUP BY  D. FROM  E. HAVING

(1) D, B, E, C, A  
(2) D, B, C, E, A  
(3) A, D, B, C, E  
(4) D, C, B, E, A  

<details><summary>Answer</summary>

**(2)** — FROM, WHERE, GROUP BY, HAVING, SELECT, then ORDER BY.

</details>

**Q15.** `High`  
Given below are two statements.  
Statement I: The WHERE clause filters rows before grouping, while HAVING filters groups after grouping.  
Statement II: Aggregate functions can be used directly in the WHERE clause.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Aggregate conditions must go in HAVING (or in a subquery).

</details>

**Q16.** `High`  
Match List I with List II.  
List I (Command): A. DELETE FROM T  B. TRUNCATE TABLE T  C. DROP TABLE T  
List II (Effect): I. Removes all rows quickly; table structure remains; usually cannot be rolled back  II. Removes the table definition and its data  III. Removes rows (optionally selected with WHERE) and can be rolled back

(1) A-II, B-I, C-III  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-III, B-I, C-II  

<details><summary>Answer</summary>

**(4)** — DELETE is DML; TRUNCATE and DROP are DDL.

</details>

**Q17.** `High`  
Given below are two statements.  
Statement I: A column with a UNIQUE constraint can never contain NULL.  
Statement II: A table can have only one PRIMARY KEY but several UNIQUE constraints.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — UNIQUE columns may contain NULLs (in most systems, several), while PRIMARY KEY columns may not.

</details>

**Q18.** `Medium`  
The condition salary > ALL (SELECT salary FROM EMP WHERE dept = 'EE'), where the EE salaries are 40000 and 45000, is equivalent to

(1) salary IN (40000, 45000)  
(2) salary > 45000  
(3) salary > 40000  
(4) salary > 85000  

<details><summary>Answer</summary>

**(2)** — > ALL means greater than the maximum of the set (assuming no NULLs).

</details>

**Q19.** `Medium`  
Which of the following is equivalent to x IN (subquery)?

(1) x = ALL (subquery)  
(2) x <> ANY (subquery)  
(3) x > ALL (subquery)  
(4) x = ANY (subquery)  

<details><summary>Answer</summary>

**(4)** — NOT IN is equivalent to <> ALL.

</details>

**Q20.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A correlated subquery is generally evaluated once for each row of the outer query.  
Reason R: A subquery can be used with the EXISTS operator.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but R does not explain A; a correlated subquery is re-evaluated because it refers to columns of the outer query.

</details>

**Q21.** `Medium`  
The EXISTS operator returns TRUE if the subquery

(1) returns NULL  
(2) returns exactly one row  
(3) returns no rows  
(4) returns at least one row  

<details><summary>Answer</summary>

**(4)** — NOT EXISTS is TRUE when the subquery returns no rows.

</details>

**Q22.** `High`  
Match List I with List II.  
List I (Join): A. INNER JOIN  B. LEFT OUTER JOIN  C. FULL OUTER JOIN  D. CROSS JOIN  
List II (Result): I. All rows of both tables, with NULLs where there is no match  II. Every combination of rows from the two tables  III. Only matching rows  IV. All rows of the left table, with NULLs where the right has no match

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-I, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(2)** — Types of SQL joins.

</details>

**Q23.** `Medium`  
A table R has 4 rows and a table S has 4 rows. The number of rows in R CROSS JOIN S is

(1) 16  
(2) 4  
(3) 0  
(4) 8  

<details><summary>Answer</summary>

**(1)** — The Cartesian product has 4 × 4 rows.

</details>

**Q24.** `High`  
Given below are two statements.  
Statement I: A view defined on a single table without aggregates, DISTINCT or GROUP BY is generally updatable.  
Statement II: A view defined using GROUP BY and aggregate functions is generally updatable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Updates through a grouped view cannot be mapped unambiguously to base rows.

</details>

**Q25.** `Medium`  
The WITH CHECK OPTION clause in a view definition ensures that

(1) the view is materialized  
(2) rows inserted or updated through the view satisfy the view's WHERE condition  
(3) indexes are created on the view  
(4) the view cannot be queried  

<details><summary>Answer</summary>

**(2)** — Otherwise a row could "disappear" from the view after being updated through it.

</details>

**Q26.** `Medium`  
A materialized view differs from an ordinary view in that

(1) it has no defining query  
(2) it cannot be queried  
(3) its result is physically stored and must be kept up to date when base tables change  
(4) it cannot use joins  

<details><summary>Answer</summary>

**(3)** — Materialized views speed up queries at the cost of maintenance.

</details>

**Q27.** `High`  
Match List I with List II.  
List I (Trigger element): A. Event  B. Condition  C. Action  
List II (Meaning): I. The statements executed when the trigger fires  II. The database modification (INSERT, UPDATE or DELETE) that activates the trigger  III. A test that must be true for the action to run

(1) A-III, B-II, C-I  
(2) A-II, B-I, C-III  
(3) A-II, B-III, C-I  
(4) A-I, B-III, C-II  

<details><summary>Answer</summary>

**(3)** — Triggers follow the event-condition-action (ECA) model.

</details>

**Q28.** `Medium`  
In a row-level trigger, the values of a row before and after an UPDATE are referenced as

(1) OLD and NEW  
(2) PRIOR and NEXT  
(3) FIRST and LAST  
(4) BEFORE and AFTER  

<details><summary>Answer</summary>

**(1)** — A statement-level trigger fires once per statement, not once per affected row.

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: A stored procedure is compiled and stored in the database server and can be called by applications.  
Statement II: Stored procedures can reduce network traffic because several SQL statements execute on the server in one call.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are advantages of stored procedures.

</details>

**Q30.** `Medium`  
Which of the following distinguishes a stored function from a stored procedure in SQL?

(1) A procedure must return a value  
(2) A function returns a value and can be used within an SQL expression  
(3) A function cannot contain SQL statements  
(4) A function cannot have parameters  

<details><summary>Answer</summary>

**(2)** — Procedures are invoked with CALL and return results through OUT parameters.

</details>

**Q31.** `High`  
A login form builds the query "SELECT * FROM users WHERE name = '" + input + "' AND pwd = '...'". Entering the name ' OR '1'='1' -- is an example of

(1) a buffer overflow  
(2) cross-site scripting  
(3) SQL injection  
(4) a denial-of-service attack  

<details><summary>Answer</summary>

**(3)** — The input changes the structure of the query so that its condition is always true.

</details>

**Q32.** `High`  
Which of the following is the most effective defence against SQL injection?

(1) Encrypting the database files  
(2) Using longer passwords  
(3) Using parameterised queries (prepared statements) with bound variables  
(4) Hiding error messages  

<details><summary>Answer</summary>

**(3)** — With bound parameters, user input is always treated as data, never as SQL code.

</details>

**Q33.** `Medium`  
In SQL, the data type NUMERIC(5, 2) can store a maximum value of

(1) 999.99  
(2) 99.999  
(3) 99999  
(4) 9999.99  

<details><summary>Answer</summary>

**(1)** — Precision 5 is the total number of digits, 2 of which follow the decimal point.

</details>

**Q34.** `Medium`  
Given below are two statements.  
Statement I: CHAR(n) stores fixed-length strings, padding shorter values with spaces.  
Statement II: VARCHAR(n) stores variable-length strings up to n characters.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both statements are true.

</details>

**Q35.** `Medium`  
For the scores 100, 90, 90 and 80 in descending order, the values produced by RANK() and DENSE_RANK() are respectively

(1) 1, 1, 2, 3 and 1, 2, 3, 4  
(2) 1, 2, 2, 3 and 1, 2, 2, 4  
(3) 1, 2, 2, 4 and 1, 2, 2, 3  
(4) 1, 2, 3, 4 and 1, 2, 2, 3  

<details><summary>Answer</summary>

**(3)** — RANK leaves a gap after ties; DENSE_RANK does not.

</details>

**Q36.** `Medium`  
Which SQL statement adds a new column phone to an existing table STUDENT?

(1) ALTER TABLE STUDENT ADD phone VARCHAR(15)  
(2) INSERT INTO STUDENT COLUMN phone  
(3) UPDATE STUDENT ADD phone VARCHAR(15)  
(4) MODIFY STUDENT phone VARCHAR(15)  

<details><summary>Answer</summary>

**(1)** — ALTER TABLE changes the schema; UPDATE changes data.

</details>

**Q37.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: SELECT DISTINCT can make a query slower.  
Reason R: Eliminating duplicates usually requires sorting or hashing the result.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — SQL keeps duplicates by default because duplicate elimination is expensive.

</details>

**Q38.** `Medium`  
What is the purpose of a SAVEPOINT in SQL?

(1) To create a backup  
(2) To mark a point within a transaction to which it can later be partially rolled back  
(3) To lock a table  
(4) To commit the transaction  

<details><summary>Answer</summary>

**(2)** — ROLLBACK TO SAVEPOINT undoes only the work done after the savepoint.

</details>

**Q39.** `Medium`  
Which SQL construct allows a program to process the rows of a query result one at a time?

(1) Index  
(2) Trigger  
(3) Cursor  
(4) View  

<details><summary>Answer</summary>

**(3)** — A cursor is declared, opened, fetched from and closed.

</details>

**Q40.** `Medium`  
Table EMP(eid, name, dept, salary) has the rows (1, Asha, CS, 50000), (2, Bala, CS, 60000), (3, Chitra, EE, 40000), (4, Deepak, EE, NULL), (5, Esha, ME, 70000), (6, Farhan, CS, NULL). The query SELECT SUM(salary) / COUNT(*) FROM EMP returns approximately

(1) 36667  
(2) 55000  
(3) 44000  
(4) NULL  

<details><summary>Answer</summary>

**(1)** — 220000 / 6 ≈ 36667, which differs from AVG(salary) because COUNT(*) includes the NULL rows.

</details>

**Q41.** `Medium`  
The SQL function COALESCE(salary, 0) returns

(1) 0 always  
(2) the count of non-null salaries  
(3) salary if it is not NULL, otherwise 0  
(4) NULL if salary is 0  

<details><summary>Answer</summary>

**(3)** — COALESCE returns its first non-null argument.

</details>

**Q42.** `Medium`  
Given below are two statements.  
Statement I: ORDER BY sorts in descending order by default.  
Statement II: ORDER BY can refer to a column alias defined in the SELECT list.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — The default order is ascending; ORDER BY is evaluated after SELECT, so aliases are allowed.

</details>

**Q43.** `Medium`  
Which of the following SQL constraints ensures that all values in a column satisfy a Boolean condition, such as age >= 18?

(1) FOREIGN KEY  
(2) CHECK  
(3) UNIQUE  
(4) DEFAULT  

<details><summary>Answer</summary>

**(2)** — A CHECK constraint is evaluated on insert and update.

</details>

**Q44.** `Medium`  
In SQL, the set operation that returns rows from the first query that are not in the second is

(1) EXCEPT (MINUS in Oracle)  
(2) UNION  
(3) JOIN  
(4) INTERSECT  

<details><summary>Answer</summary>

**(1)** — EXCEPT removes duplicates unless EXCEPT ALL is used.

</details>

**Q45.** `Medium`  
Table T1(x) contains 1, 2, 2, 3 and NULL; table T2(x) contains 2, 3 and 4. How many rows does SELECT x FROM T1 EXCEPT SELECT x FROM T2 return?

(1) 1  
(2) 3  
(3) 4  
(4) 2  

<details><summary>Answer</summary>

**(4)** — The distinct values 1 and NULL remain; set operations treat NULLs as equal to each other.

</details>

**Q46.** `Medium`  
Which privilege-related SQL statement removes previously granted privileges?

(1) REVOKE  
(2) DROP  
(3) ROLLBACK  
(4) DENY  

<details><summary>Answer</summary>

**(1)** — GRANT gives privileges; REVOKE takes them away.

</details>

**Q47.** `Low`  
Which SQL keyword is used to give a temporary name to a table or column in a query?

(1) AS  
(2) ALIAS  
(3) RENAME  
(4) LIKE  

<details><summary>Answer</summary>

**(1)** — For example SELECT e.name FROM EMP AS e.

</details>

**Q48.** `Medium`  
Given below are two statements.  
Statement I: A GROUP BY query may select a column that is neither grouped nor aggregated in standard SQL.  
Statement II: Every non-aggregated column in the SELECT list must appear in the GROUP BY clause in standard SQL.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Standard SQL requires each non-aggregated selected column to be in GROUP BY (or functionally dependent on it).

</details>

**Q49.** `Medium`  
Which of the following correctly lists employees whose salary is above the average salary?

(1) SELECT name, AVG(salary) FROM EMP  
(2) SELECT name FROM EMP WHERE salary > AVG(salary)  
(3) SELECT name FROM EMP HAVING salary > AVG(salary)  
(4) SELECT name FROM EMP WHERE salary > (SELECT AVG(salary) FROM EMP)  

<details><summary>Answer</summary>

**(4)** — An aggregate cannot appear directly in WHERE; a scalar subquery is used instead.

</details>

**Q50.** `Medium`  
ODBC and JDBC are

(1) NoSQL databases  
(2) standard application programming interfaces for accessing databases from programs  
(3) database recovery techniques  
(4) query optimization methods  

<details><summary>Answer</summary>

**(2)** — They provide call-level interfaces, unlike embedded SQL, which needs a precompiler.

</details>

**Q51.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In SQL, a table with no primary key can contain duplicate rows.  
Reason R: SQL automatically removes duplicate rows from every table.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — SQL tables are multisets; only constraints such as PRIMARY KEY or UNIQUE prevent duplicates.

</details>
