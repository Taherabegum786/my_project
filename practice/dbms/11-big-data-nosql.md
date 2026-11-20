# Set 11 — Big Data Systems, Hadoop, MapReduce, HDFS and NoSQL

**43 questions** — High: 16, Medium: 26, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Big data characteristic): A. Volume  B. Velocity  C. Variety  D. Veracity  
List II (Meaning): I. Uncertainty or trustworthiness of the data  II. Huge amount of data  III. Speed at which data is generated and processed  IV. Different forms of data: structured, semi-structured and unstructured

(1) A-II, B-III, C-IV, D-I  
(2) A-III, B-II, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(1)** — Value is often added as a fifth V.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Type of data): A. Structured  B. Semi-structured  C. Unstructured  
List II (Example): I. JSON and XML documents  II. Video files and free text  III. Rows of a relational table

(1) A-II, B-I, C-III  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-III, B-I, C-II  

<details><summary>Answer</summary>

**(4)** — Types of big data.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (HDFS component): A. NameNode  B. DataNode  C. Secondary NameNode  
List II (Role): I. Stores the actual data blocks and serves read and write requests  II. Periodically merges the edit log with the file-system image (checkpointing)  III. Manages the namespace and metadata, including block locations

(1) A-III, B-I, C-II  
(2) A-III, B-II, C-I  
(3) A-II, B-I, C-III  
(4) A-I, B-III, C-II  

<details><summary>Answer</summary>

**(1)** — The Secondary NameNode is not a hot standby for the NameNode.

</details>

**Q4.** `High`  
In HDFS (Hadoop 2 and later), the default block size and the default replication factor are

(1) 256 MB and 3  
(2) 128 MB and 3  
(3) 64 MB and 2  
(4) 4 KB and 3  

<details><summary>Answer</summary>

**(2)** — Hadoop 1 used 64 MB blocks.

</details>

**Q5.** `High`  
A 640 MB file is stored in HDFS with a block size of 128 MB and a replication factor of 3. The number of blocks and the total storage used are

(1) 5 blocks and 640 MB  
(2) 5 blocks and 1920 MB  
(3) 10 blocks and 1280 MB  
(4) 15 blocks and 640 MB  

<details><summary>Answer</summary>

**(2)** — 640 / 128 = 5 blocks, each stored 3 times: 3 × 640 = 1920 MB.

</details>

**Q6.** `High`  
A 1 GB input file stored in HDFS with 128 MB blocks is processed by a MapReduce job. By default, the number of map tasks is

(1) 16  
(2) 1  
(3) 4  
(4) 8  

<details><summary>Answer</summary>

**(4)** — One map task per input split, and by default one split per block: 1024 / 128 = 8.

</details>

**Q7.** `High`  
Arrange the phases of a MapReduce job in order.  
A. Reduce  B. Map  C. Shuffle and sort  D. Input splitting

(1) B, D, C, A  
(2) D, B, C, A  
(3) D, C, B, A  
(4) D, B, A, C  

<details><summary>Answer</summary>

**(2)** — Map output is partitioned, sorted and sent to reducers, which write the final output.

</details>

**Q8.** `High`  
Given below are two statements.  
Statement I: A combiner performs local aggregation of map output on the mapper node to reduce data transferred to reducers.  
Statement II: The partitioner decides which reducer receives each intermediate key.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The default partitioner hashes the key modulo the number of reducers.

</details>

**Q9.** `High`  
In a word-count MapReduce job, the map function emits

(1) (1, word)  
(2) (document, count)  
(3) (word, 1) for each word in its input  
(4) the total count for each word  

<details><summary>Answer</summary>

**(3)** — The reducer sums the values for each word.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (YARN component): A. ResourceManager  B. NodeManager  C. ApplicationMaster  
List II (Role): I. Negotiates resources for one application and monitors its tasks  II. Allocates cluster resources among all applications  III. Launches and monitors containers on a single machine

(1) A-II, B-III, C-I  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — YARN separates resource management from the MapReduce programming model.

</details>

**Q11.** `High`  
Match List I with List II.  
List I (Hadoop ecosystem tool): A. Hive  B. Pig  C. HBase  D. Sqoop  
List II (Purpose): I. Transfers bulk data between Hadoop and relational databases  II. Column-oriented NoSQL store on top of HDFS  III. Data-warehouse system with an SQL-like query language (HiveQL)  IV. High-level data-flow scripting language (Pig Latin)

(1) A-IV, B-III, C-II, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(3)** — Other tools include Flume (log ingestion), ZooKeeper (coordination) and Oozie (workflow scheduling).

</details>

**Q12.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Apache Spark is usually faster than Hadoop MapReduce for iterative algorithms.  
Reason R: Spark can run only on a single machine.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Spark runs on clusters; it is faster because it keeps intermediate data in memory as RDDs.

</details>

**Q13.** `Medium`  
HDFS is designed for

(1) storing data only in memory  
(2) high-throughput streaming access to very large files with a write-once, read-many model  
(3) transactional updates with ACID guarantees  
(4) low-latency random reads and writes of small files  

<details><summary>Answer</summary>

**(2)** — It is optimized for batch processing rather than interactive access.

</details>

**Q14.** `Medium`  
Given below are two statements.  
Statement I: HDFS rack awareness places replicas on different racks to survive the failure of an entire rack.  
Statement II: HDFS stores each block only once to save space.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Blocks are replicated, by default three times.

</details>

**Q15.** `Medium`  
"Moving computation to the data" in Hadoop means that

(1) computation is done only on the client  
(2) data is copied to a central server for processing  
(3) map tasks are scheduled on nodes that hold the input blocks locally  
(4) the NameNode processes all data  

<details><summary>Answer</summary>

**(3)** — Data locality reduces network traffic.

</details>

**Q16.** `High`  
Match List I with List II.  
List I (NoSQL category): A. Key-value store  B. Document store  C. Column-family store  D. Graph database  
List II (Example): I. Neo4j  II. MongoDB  III. Cassandra  IV. Redis

(1) A-IV, B-III, C-II, D-I  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(2)** — Other examples: DynamoDB (key-value), CouchDB (document), HBase (column-family).

</details>

**Q17.** `High`  
The CAP theorem states that a distributed data store cannot simultaneously guarantee all three of

(1) consistency, atomicity and partitioning  
(2) concurrency, atomicity and persistence  
(3) consistency, availability and partition tolerance  
(4) capacity, accuracy and performance  

<details><summary>Answer</summary>

**(3)** — During a network partition a system must choose between consistency and availability.

</details>

**Q18.** `High`  
Given below are two statements.  
Statement I: BASE stands for Basically Available, Soft state, Eventually consistent.  
Statement II: Most NoSQL systems provide full ACID transactions across all nodes by default.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Many NoSQL systems relax consistency in favour of availability and scalability.

</details>

**Q19.** `High`  
In a replicated NoSQL store with N = 3 replicas, a write quorum W and a read quorum R guarantee that every read sees the latest write when

(1) R + W &lt; N  
(2) R + W = N − 1  
(3) R = W = 1  
(4) R + W &gt; N  

<details><summary>Answer</summary>

**(4)** — With R = 2 and W = 2, read and write sets must overlap in at least one replica.

</details>

**Q20.** `Medium`  
In a Dynamo-style store with N = 3, which setting gives strongly consistent reads?

(1) W = 1, R = 1  
(2) W = 1, R = 2  
(3) W = 0, R = 3  
(4) W = 2, R = 2  

<details><summary>Answer</summary>

**(4)** — 2 + 2 &gt; 3, so every read quorum overlaps every write quorum.

</details>

**Q21.** `Medium`  
Sharding in NoSQL databases means

(1) horizontally partitioning data across several servers by a shard key  
(2) replicating all data to every node  
(3) encrypting data at rest  
(4) normalizing tables  

<details><summary>Answer</summary>

**(1)** — It allows the database to scale out.

</details>

**Q22.** `Medium`  
Consistent hashing is used in distributed key-value stores to

(1) minimise the number of keys that must move when nodes are added or removed  
(2) encrypt keys  
(3) guarantee ACID transactions  
(4) sort keys alphabetically  

<details><summary>Answer</summary>

**(1)** — Keys and nodes are mapped onto a ring; each key goes to the next node clockwise.

</details>

**Q23.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Document databases such as MongoDB are well suited to data with varying structure.  
Reason R: Documents in the same collection need not have the same set of fields.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — MongoDB stores JSON-like BSON documents with a flexible schema.

</details>

**Q24.** `Medium`  
In MongoDB, the equivalents of a relational table and a row are respectively

(1) collection and document  
(2) index and key  
(3) document and collection  
(4) database and field  

<details><summary>Answer</summary>

**(1)** — A field corresponds to a column.

</details>

**Q25.** `Medium`  
Which MongoDB method retrieves documents matching a condition?

(1) get()  
(2) select()  
(3) find()  
(4) query()  

<details><summary>Answer</summary>

**(3)** — For example db.students.find({age: {$gt: 20}}).

</details>

**Q26.** `Medium`  
In the MongoDB aggregation pipeline, the stage that groups documents and computes aggregates is

(1) $match  
(2) $sort  
(3) $group  
(4) $project  

<details><summary>Answer</summary>

**(3)** — $match filters documents, $project reshapes them, and $sort orders them.

</details>

**Q27.** `Medium`  
Match List I with List II.  
List I (MongoDB index type): A. Compound index  B. Multikey index  C. Text index  D. Geospatial (2dsphere) index  
List II (Use): I. Indexes the elements of an array field  II. Supports queries on location data  III. Indexes several fields together  IV. Supports keyword search on string content

(1) A-III, B-I, C-II, D-IV  
(2) A-III, B-I, C-IV, D-II  
(3) A-III, B-IV, C-I, D-II  
(4) A-I, B-III, C-IV, D-II  

<details><summary>Answer</summary>

**(2)** — MongoDB also supports hashed indexes, used for hashed sharding.

</details>

**Q28.** `Medium`  
In Cassandra, the primary key consists of

(1) a sequence number only  
(2) a partition key, which determines the node, and optional clustering columns, which order rows within a partition  
(3) only a partition key  
(4) a foreign key  

<details><summary>Answer</summary>

**(2)** — Queries are designed around the partition key.

</details>

**Q29.** `Medium`  
Given below are two statements.  
Statement I: Cassandra uses a master-slave architecture with a single master node.  
Statement II: Cassandra supports tunable consistency, letting each query choose levels such as ONE, QUORUM or ALL.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Cassandra is masterless (peer-to-peer); every node can accept reads and writes.

</details>

**Q30.** `Medium`  
Log-structured merge (LSM) trees, used in Cassandra, HBase and RocksDB, are optimized for

(1) small datasets only  
(2) high write throughput, by buffering writes in memory and flushing sorted runs (SSTables) to disk  
(3) in-place updates  
(4) read-only workloads  

<details><summary>Answer</summary>

**(2)** — Background compaction merges the SSTables.

</details>

**Q31.** `Medium`  
In NoSQL query optimization, data is often denormalized because

(1) it enforces referential integrity  
(2) denormalization reduces storage use  
(3) joins across distributed nodes are expensive, so data accessed together is stored together  
(4) NoSQL cannot store numbers  

<details><summary>Answer</summary>

**(3)** — Schema design is driven by query access patterns.

</details>

**Q32.** `Medium`  
Which of the following is a fully managed NoSQL database service offered in the cloud?

(1) Microsoft Access  
(2) Amazon DynamoDB  
(3) SQLite  
(4) MySQL Community Edition  

<details><summary>Answer</summary>

**(2)** — Others include Azure Cosmos DB and Google Cloud Bigtable/Firestore.

</details>

**Q33.** `Medium`  
Graph databases are best suited for

(1) storing large binary files  
(2) simple key look-ups only  
(3) queries that traverse many relationships, such as friend-of-friend or shortest-path queries  
(4) bulk numeric aggregation  

<details><summary>Answer</summary>

**(3)** — Neo4j uses the Cypher query language over nodes and relationships.

</details>

**Q34.** `Medium`  
Given below are two statements.  
Statement I: Eventual consistency guarantees that, if no new updates are made, all replicas will eventually converge to the same value.  
Statement II: Eventual consistency guarantees that every read returns the most recent write.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Reads may return stale data before the replicas converge.

</details>

**Q35.** `Medium`  
The Lambda architecture for big data processing combines

(1) an OLTP and an OLAP database  
(2) only a stream layer  
(3) a batch layer and a speed (real-time) layer with a serving layer  
(4) only a batch layer  

<details><summary>Answer</summary>

**(3)** — The Kappa architecture uses a single stream-processing layer.

</details>

**Q36.** `Medium`  
Which of the following tools is used for real-time distributed stream processing?

(1) Apache Oozie  
(2) Apache Kafka Streams / Apache Storm / Spark Streaming  
(3) Apache Hive  
(4) Apache Sqoop  

<details><summary>Answer</summary>

**(2)** — Hive, Sqoop and Oozie are batch-oriented tools.

</details>

**Q37.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In HDFS, the NameNode was a single point of failure in Hadoop 1.  
Reason R: The Secondary NameNode automatically takes over when the NameNode fails.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — The Secondary NameNode only creates checkpoints; Hadoop 2 added NameNode high availability with a standby NameNode.

</details>

**Q38.** `Medium`  
In MapReduce, the output of the map phase is

(1) sent directly to the client  
(2) discarded after reduce  
(3) written to HDFS with full replication  
(4) written to the local disk of the mapper node and then fetched by reducers  

<details><summary>Answer</summary>

**(4)** — Only the final reducer output is written to HDFS.

</details>

**Q39.** `Medium`  
Given below are two statements.  
Statement I: Key-value stores support complex queries on the internal structure of values.  
Statement II: Column-family stores group related columns together and store them contiguously.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A key-value store treats the value as opaque; access is by key.

</details>

**Q40.** `Medium`  
Which component coordinates distributed services in the Hadoop ecosystem, for example for leader election and configuration management?

(1) ZooKeeper  
(2) Flume  
(3) Mahout  
(4) Pig  

<details><summary>Answer</summary>

**(1)** — Flume ingests log data and Mahout provides machine-learning libraries.

</details>

**Q41.** `Low`  
Which data format is commonly used to store documents in MongoDB?

(1) XML only  
(2) YAML  
(3) CSV  
(4) BSON  

<details><summary>Answer</summary>

**(4)** — BSON is a binary representation of JSON.

</details>

**Q42.** `Medium`  
Secondary indexes in a sharded NoSQL database are often costly because

(1) they cannot be created  
(2) they disable replication  
(3) they double the data size  
(4) a query on the secondary key may have to be sent to every shard (scatter-gather)  

<details><summary>Answer</summary>

**(4)** — Queries that include the shard key can be routed to a single shard.

</details>

**Q43.** `Medium`  
Given below are two statements.  
Statement I: In MapReduce, the number of reducers is set by the user or configuration.  
Statement II: The number of map tasks always equals the number of reducers.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The number of map tasks depends on the number of input splits, independently of the number of reducers.

</details>
