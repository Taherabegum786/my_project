# Set 6 — File Organization, Indexing, Hashing, Query Processing and Optimization

**43 questions** — High: 15, Medium: 27, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A B+ tree uses blocks of 512 bytes, search keys of 9 bytes and block pointers of 6 bytes. The maximum order p of an internal node (maximum number of tree pointers) is

(1) 46  
(2) 34  
(3) 56  
(4) 31  

<details><summary>Answer</summary>

**(2)** — p × 6 + (p − 1) × 9 ≤ 512 gives 15p ≤ 521, so p = 34.

</details>

**Q2.** `High`  
A B+ tree uses blocks of 512 bytes, search keys of 9 bytes and record pointers of 7 bytes; each leaf also holds one 6-byte next-leaf pointer. The maximum number of keys in a leaf node is

(1) 37  
(2) 34  
(3) 31  
(4) 32  

<details><summary>Answer</summary>

**(3)** — q × (9 + 7) + 6 ≤ 512 gives 16q ≤ 506, so q = 31.

</details>

**Q3.** `Medium`  
A B+ tree uses blocks of 1024 bytes, search keys of 9 bytes and block pointers of 6 bytes. The maximum order of an internal node is

(1) 69  
(2) 64  
(3) 113  
(4) 68  

<details><summary>Answer</summary>

**(4)** — 6p + 9(p − 1) ≤ 1024 gives 15p ≤ 1033, so p = 68.

</details>

**Q4.** `Medium`  
A B+ tree uses 4096-byte blocks, 12-byte keys and 8-byte block pointers. The maximum number of child pointers in an internal node is

(1) 256  
(2) 204  
(3) 205  
(4) 341  

<details><summary>Answer</summary>

**(3)** — 8p + 12(p − 1) ≤ 4096 gives 20p ≤ 4108, so p = 205.

</details>

**Q5.** `High`  
A file has 30,000 records of 100 bytes each, stored unspanned in 1024-byte blocks and ordered on a key. The number of block accesses needed for a binary search on the data file is approximately

(1) 3000  
(2) 12  
(3) 10  
(4) 15  

<details><summary>Answer</summary>

**(2)** — bfr = 10 records per block, so 3000 blocks; ⌈log2 3000⌉ = 12.

</details>

**Q6.** `High`  
For the same file of 3000 blocks (30,000 records), a primary index with 15-byte entries (9-byte key, 6-byte pointer) is built in 1024-byte blocks. The number of block accesses to find a record using binary search on the index is

(1) 45  
(2) 7  
(3) 6  
(4) 12  

<details><summary>Answer</summary>

**(2)** — 68 entries per index block; 3000 entries need 45 blocks; ⌈log2 45⌉ = 6 index accesses plus 1 data access.

</details>

**Q7.** `Medium`  
A dense secondary index on a non-ordering key of a file with 30,000 records uses 15-byte entries in 1024-byte blocks (68 entries per block). The number of index blocks is

(1) 30,000  
(2) 442  
(3) 300  
(4) 45  

<details><summary>Answer</summary>

**(2)** — One entry per record: ⌈30,000 / 68⌉ = 442 blocks.

</details>

**Q8.** `Medium`  
For a primary index of 3000 entries with a fan-out of 68, a multilevel index has how many levels?

(1) 3  
(2) 2  
(3) 1  
(4) 4  

<details><summary>Answer</summary>

**(2)** — Level 1 needs ⌈3000 / 68⌉ = 45 blocks; level 2 needs 1 block. Search cost is 2 index accesses + 1 data access.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Index type): A. Primary index  B. Clustering index  C. Secondary index  D. Dense index  
List II (Description): I. Has an index entry for every search-key value (every record)  II. Defined on the ordering key field of an ordered file  III. Defined on a non-key ordering field of an ordered file  IV. Defined on a non-ordering field; a file can have several

(1) A-II, B-III, C-I, D-IV  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — A file can have at most one primary or clustering index, but many secondary indexes.

</details>

**Q10.** `High`  
Given below are two statements.  
Statement I: A primary index is a sparse index with one entry per data block.  
Statement II: A secondary index on a key field is a dense index.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Each data block has one anchor record in a primary index; a secondary index must point to every record.

</details>

**Q11.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: B+ trees are preferred over B trees for database indexes.  
Reason R: In a B+ tree, all data pointers are stored in the leaves, which are linked, so internal nodes have a higher fan-out and range queries are efficient.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Higher fan-out gives fewer levels, and linked leaves support sequential access.

</details>

**Q12.** `High`  
Given below are two statements.  
Statement I: In a B tree, every key appears exactly once, either in an internal node or in a leaf.  
Statement II: In a B+ tree, the leaf nodes are not linked to one another.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — B+ tree leaves are linked to support range queries.

</details>

**Q13.** `Medium`  
In a B+ tree of order p (maximum p pointers per internal node), every internal node except the root has at least

(1) ⌈p / 2⌉ pointers  
(2) p / 2 − 1 pointers  
(3) p − 1 pointers  
(4) 2 pointers  

<details><summary>Answer</summary>

**(1)** — The root needs at least 2 pointers if it is an internal node.

</details>

**Q14.** `Medium`  
Searching for a key in a B+ tree with n keys and fan-out f requires approximately

(1) O(1) node accesses  
(2) O(n) node accesses  
(3) O(log\_f n) node accesses  
(4) O(f) node accesses  

<details><summary>Answer</summary>

**(3)** — All leaves are at the same depth, which is logarithmic in n.

</details>

**Q15.** `High`  
Match List I with List II.  
List I (File organization): A. Heap (pile) file  B. Sorted (sequential) file  C. Hashed file  
List II (Characteristic): I. Very fast equality search on the hash field, but not suited to range queries  II. Insertion is cheap, but search requires a linear scan  III. Binary search and efficient range queries on the ordering field, but costly insertion

(1) A-II, B-I, C-III  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — Basic file organizations.

</details>

**Q16.** `High`  
In extendible hashing, when a bucket whose local depth equals the global depth overflows,

(1) only the bucket is split  
(2) the whole file is rehashed  
(3) the directory is doubled and the bucket is split  
(4) an overflow chain is created  

<details><summary>Answer</summary>

**(3)** — If the local depth is less than the global depth, the bucket is split without doubling the directory.

</details>

**Q17.** `Medium`  
In extendible hashing with a global depth of 3, the directory has

(1) 6 entries  
(2) 9 entries  
(3) 3 entries  
(4) 8 entries  

<details><summary>Answer</summary>

**(4)** — The directory has 2^d entries, where d is the global depth.

</details>

**Q18.** `Medium`  
Linear hashing differs from extendible hashing in that it

(1) cannot handle overflow  
(2) uses a directory  
(3) uses only static buckets  
(4) grows the file one bucket at a time in a fixed order without a directory  

<details><summary>Answer</summary>

**(4)** — Buckets are split in linear order, with overflow chains handling temporary overflow.

</details>

**Q19.** `Medium`  
In static hashing, the problem of a bucket becoming full is usually handled by

(1) splitting the root  
(2) doubling the directory  
(3) overflow chaining  
(4) rebuilding a B+ tree  

<details><summary>Answer</summary>

**(3)** — Too many overflow buckets degrade performance, which motivates dynamic hashing.

</details>

**Q20.** `High`  
Relation student has 5000 records in 100 blocks and takes has 10,000 records in 400 blocks. With student as the outer relation and only one block of each relation in memory, the worst-case cost of a simple nested-loop join is

(1) 500 block transfers  
(2) 2,000,100 block transfers  
(3) 40,100 block transfers  
(4) 1,000,400 block transfers  

<details><summary>Answer</summary>

**(2)** — n\_r × b\_s + b\_r = 5000 × 400 + 100 = 2,000,100.

</details>

**Q21.** `High`  
For student (100 blocks) and takes (400 blocks), with student as the outer relation, the worst-case cost of a block nested-loop join is

(1) 2,000,100  
(2) 40,400  
(3) 40,100  
(4) 500  

<details><summary>Answer</summary>

**(3)** — b\_r × b\_s + b\_r = 100 × 400 + 100 = 40,100 block transfers.

</details>

**Q22.** `Medium`  
For a nested-loop join of student (100 blocks) and takes (400 blocks), if the smaller relation fits entirely in memory, the cost is

(1) 40,100 block transfers  
(2) 500 block transfers  
(3) 400 block transfers  
(4) 100 block transfers  

<details><summary>Answer</summary>

**(2)** — Each relation is read only once: b\_r + b\_s = 500.

</details>

**Q23.** `Medium`  
The cost of a merge join on two relations that are already sorted on the join attribute, with b\_r and b\_s blocks, is about

(1) 2(b\_r + b\_s) log(b\_r + b\_s)  
(2) b\_r × b\_s  
(3) b\_r + b\_s block transfers  
(4) b\_r log b\_s  

<details><summary>Answer</summary>

**(3)** — Each block is read once; if unsorted, sorting cost must be added.

</details>

**Q24.** `High`  
Match List I with List II.  
List I (Query processing step): A. Parsing and translation  B. Optimization  C. Evaluation  
List II (Description): I. The query-execution engine executes the chosen plan  II. The query is checked for syntax and translated into relational algebra  III. The lowest-cost evaluation plan is chosen from equivalent plans

(1) A-I, B-III, C-II  
(2) A-II, B-I, C-III  
(3) A-II, B-III, C-I  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(3)** — The three basic steps of query processing.

</details>

**Q25.** `High`  
Which of the following heuristics is used in query optimization?

(1) Perform selections and projections as early as possible  
(2) Avoid using indexes  
(3) Perform joins before selections  
(4) Perform Cartesian products as early as possible  

<details><summary>Answer</summary>

**(1)** — Pushing selections and projections down reduces the size of intermediate results.

</details>

**Q26.** `High`  
Given below are two statements.  
Statement I: Cost-based optimization estimates the cost of alternative plans using statistics in the catalog.  
Statement II: Heuristic optimization uses transformation rules, such as pushing selections down, without estimating costs.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Most optimizers combine both approaches.

</details>

**Q27.** `Medium`  
The number of different join orders for a join of n relations grows as

(1) (2(n − 1))! / (n − 1)!  
(2) n  
(3) log n  
(4) n²  

<details><summary>Answer</summary>

**(1)** — For n = 3 it is 12, and for n = 7 it is 665,280, which is why optimizers use dynamic programming.

</details>

**Q28.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Pipelining can be used for every relational operation, including sorting.  
Reason R: In pipelining, the result of one operation is passed directly to the next operation without writing temporary relations to disk.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Sorting and some aggregations are blocking operations that need their whole input before producing output.

</details>

**Q29.** `Medium`  
Which of the following equivalence rules is valid in relational algebra?

(1) π\_L(E1 − E2) = π\_L(E1) − π\_L(E2) always  
(2) σ\_θ(E1 × E2) = E1 ⋈\_θ E2  
(3) E1 − E2 = E2 − E1  
(4) σ\_θ1(E) ∪ σ\_θ2(E) = σ\_θ1 ∧ θ2(E)  

<details><summary>Answer</summary>

**(2)** — Selection on a Cartesian product is a theta join; projection does not distribute over difference in general.

</details>

**Q30.** `Medium`  
The selectivity of a condition is

(1) the cost of reading the relation  
(2) the number of attributes in the result  
(3) the number of indexes used  
(4) the fraction of tuples that satisfy the condition  

<details><summary>Answer</summary>

**(4)** — Optimizers use selectivity to estimate the size of intermediate results.

</details>

**Q31.** `Medium`  
For a relation r with n\_r = 10,000 tuples and an attribute A with V(A, r) = 50 distinct values, the estimated number of tuples satisfying A = a is

(1) 200  
(2) 500  
(3) 50  
(4) 10,000  

<details><summary>Answer</summary>

**(1)** — Assuming uniform distribution: n\_r / V(A, r) = 10,000 / 50 = 200.

</details>

**Q32.** `Medium`  
External merge sort is used in query processing when

(1) the relation fits in memory  
(2) the relation to be sorted is larger than the available main memory  
(3) the relation is already sorted  
(4) a hash index exists  

<details><summary>Answer</summary>

**(2)** — Sorted runs are created and then merged in one or more passes.

</details>

**Q33.** `Medium`  
Hash join works only for

(1) equi-joins and natural joins  
(2) Cartesian products  
(3) outer joins with inequality conditions  
(4) any theta join  

<details><summary>Answer</summary>

**(1)** — Tuples are partitioned on the hash of the join attribute, so only equality conditions can be used.

</details>

**Q34.** `Medium`  
A covering index for a query is one that

(1) contains all the attributes the query needs, so the data file need not be accessed  
(2) covers all possible queries  
(3) covers the whole table  
(4) is always a clustered index  

<details><summary>Answer</summary>

**(1)** — The query can be answered from the index alone (an index-only scan).

</details>

**Q35.** `Medium`  
Given below are two statements.  
Statement I: A table can have several clustered indexes.  
Statement II: A clustered index determines the physical order of the data records.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Data can be physically ordered in only one way, so there is at most one clustered index.

</details>

**Q36.** `Medium`  
Which index structure is best suited for spatial queries such as "find all restaurants within this rectangle"?

(1) Hash index  
(2) Bitmap index  
(3) R-tree  
(4) B+ tree  

<details><summary>Answer</summary>

**(3)** — R-trees index multidimensional objects using minimum bounding rectangles.

</details>

**Q37.** `Medium`  
Bitmap indexes are most effective for attributes with

(1) frequently updated values  
(2) a very large number of distinct values  
(3) unique keys  
(4) a small number of distinct values, such as gender or state  

<details><summary>Answer</summary>

**(4)** — One bit vector per distinct value allows fast Boolean combination of conditions.

</details>

**Q38.** `Medium`  
The number of block accesses needed to retrieve a record through a B+ tree with 3 levels, including the data block, is

(1) 3  
(2) 4  
(3) 2  
(4) 5  

<details><summary>Answer</summary>

**(2)** — One access per tree level plus one access to the data block.

</details>

**Q39.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In a B+ tree, insertion can increase the height of the tree.  
Reason R: When the root splits, a new root is created one level above it.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — B+ trees grow at the root, which keeps all leaves at the same depth.

</details>

**Q40.** `Medium`  
In the catalog statistics used by a query optimizer, b\_r denotes

(1) the number of distinct values of an attribute  
(2) the number of tuples in r  
(3) the size of a tuple of r  
(4) the number of blocks containing tuples of r  

<details><summary>Answer</summary>

**(4)** — n\_r is the number of tuples and l\_r the size of a tuple.

</details>

**Q41.** `Low`  
Indexed sequential access method (ISAM) is an example of a

(1) dynamic tree index  
(2) bitmap index  
(3) static multilevel index with overflow areas  
(4) hash index  

<details><summary>Answer</summary>

**(3)** — ISAM indexes do not change on updates, so overflow chains grow; B+ trees replaced them.

</details>

**Q42.** `Medium`  
Given below are two statements.  
Statement I: Hash indexes support range queries efficiently.  
Statement II: B+ tree indexes support both equality and range queries.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Hashing scatters adjacent key values, so range queries need a full scan.

</details>

**Q43.** `Medium`  
In a B tree of order m, the maximum number of keys stored in a node is

(1) m + 1  
(2) m − 1  
(3) 2m  
(4) m  

<details><summary>Answer</summary>

**(2)** — A node with m child pointers holds m − 1 keys.

</details>
