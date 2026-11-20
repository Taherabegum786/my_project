# Set 10 — Data Warehousing and Data Mining (OLAP, schemas, association rules, classification, clustering, other mining tasks)

**45 questions** — High: 17, Medium: 27, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
According to W. H. Inmon, a data warehouse is a

(1) collection of unrelated files  
(2) subject-oriented, integrated, time-variant and non-volatile collection of data supporting decision making  
(3) volatile, application-oriented, current collection of data  
(4) normalized OLTP database  

<details><summary>Answer</summary>

**(2)** — This is the standard definition of a data warehouse.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Feature): A. OLTP  B. OLAP  
List II (Characteristic): I. Short, frequent update transactions on current, detailed, normalized data  II. Complex read-mostly analytical queries on historical, summarized data

(1) A-I, B-II  
(2) A-II, B-I  
(3) Both I  
(4) Both II  

<details><summary>Answer</summary>

**(1)** — OLTP supports day-to-day operations; OLAP supports decision making.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (OLAP operation): A. Roll-up  B. Drill-down  C. Slice  D. Pivot  
List II (Description): I. Selecting a single value on one dimension, giving a sub-cube  II. Rotating the axes of the cube to give an alternative presentation  III. Aggregating data by climbing a concept hierarchy or reducing dimensions  IV. Going from less detailed to more detailed data

(1) A-III, B-IV, C-II, D-I  
(2) A-IV, B-III, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(4)** — Dice selects on two or more dimensions.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: In a star schema, dimension tables are normalized into several related tables.  
Statement II: A snowflake schema has no fact table.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Normalized dimension tables describe a snowflake schema, which still has a central fact table.

</details>

**Q5.** `High`  
A data cube has 3 dimensions and no concept hierarchies. The number of cuboids (including the apex and base cuboids) is

(1) 6  
(2) 9  
(3) 8  
(4) 3  

<details><summary>Answer</summary>

**(3)** — Each dimension is either included or aggregated away: 2^3 = 8.

</details>

**Q6.** `High`  
A data cube has 3 dimensions with concept hierarchies of 4, 3 and 2 levels (not counting the virtual top level "all"). The total number of cuboids is

(1) 60  
(2) 24  
(3) 9  
(4) 512  

<details><summary>Answer</summary>

**(1)** — ∏(L_i + 1) = 5 × 4 × 3 = 60.

</details>

**Q7.** `Medium`  
In a concept hierarchy for location, which is the correct order from the lowest (most detailed) to the highest level?

(1) State, country, city, street  
(2) Street, city, state, country  
(3) Country, state, city, street  
(4) City, street, country, state  

<details><summary>Answer</summary>

**(2)** — Roll-up climbs from street towards country.

</details>

**Q8.** `Medium`  
Match List I with List II.  
List I (OLAP server type): A. ROLAP  B. MOLAP  C. HOLAP  
List II (Description): I. Combines relational storage for detailed data with multidimensional arrays for aggregates  II. Stores data in an extended relational DBMS and maps OLAP operations to SQL  III. Stores data in specialized multidimensional array structures

(1) A-II, B-III, C-I  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — ROLAP scales well; MOLAP gives fast indexing into precomputed data.

</details>

**Q9.** `Medium`  
ETL in data warehousing stands for

(1) Evaluate, Test, Launch  
(2) Extract, Transform, Load  
(3) Export, Translate, Log  
(4) Enter, Transfer, Link  

<details><summary>Answer</summary>

**(2)** — Data is extracted from sources, cleaned and transformed, and loaded into the warehouse.

</details>

**Q10.** `Medium`  
A data mart is

(1) a subset of a data warehouse focused on a single department or subject area  
(2) a backup of the warehouse  
(3) an operational database  
(4) a type of OLTP system  

<details><summary>Answer</summary>

**(1)** — Dependent data marts are fed from the enterprise warehouse.

</details>

**Q11.** `High`  
Arrange the steps of the knowledge discovery in databases (KDD) process in order.  
A. Data mining  B. Data cleaning and integration  C. Pattern evaluation and presentation  D. Data selection and transformation

(1) B, A, D, C  
(2) A, B, D, C  
(3) D, B, A, C  
(4) B, D, A, C  

<details><summary>Answer</summary>

**(4)** — Data mining is one step of the larger KDD process.

</details>

**Q12.** `High`  
In five transactions {bread, milk}, {bread, diaper, beer, eggs}, {milk, diaper, beer, cola}, {bread, milk, diaper, beer}, {bread, milk, diaper, cola}, the support of {milk, diaper, beer} is

(1) 60%  
(2) 80%  
(3) 40%  
(4) 20%  

<details><summary>Answer</summary>

**(3)** — It appears in 2 of the 5 transactions.

</details>

**Q13.** `High`  
In five transactions {bread, milk}, {bread, diaper, beer, eggs}, {milk, diaper, beer, cola}, {bread, milk, diaper, beer}, {bread, milk, diaper, cola}, the confidence of the rule {milk, diaper} → {beer} is

(1) 50%  
(2) 67%  
(3) 100%  
(4) 40%  

<details><summary>Answer</summary>

**(2)** — support({milk, diaper, beer}) / support({milk, diaper}) = 2 / 3.

</details>

**Q14.** `Medium`  
In five transactions {bread, milk}, {bread, diaper, beer, eggs}, {milk, diaper, beer, cola}, {bread, milk, diaper, beer}, {bread, milk, diaper, cola}, the confidence of {beer} → {diaper} is

(1) 100%  
(2) 75%  
(3) 60%  
(4) 80%  

<details><summary>Answer</summary>

**(1)** — Every transaction containing beer (3 of them) also contains diaper.

</details>

**Q15.** `High`  
Given below are two statements.  
Statement I: The Apriori property states that every non-empty subset of a frequent itemset must also be frequent.  
Statement II: If an itemset is infrequent, all of its supersets are also infrequent.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This anti-monotone property lets Apriori prune candidates.

</details>

**Q16.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: FP-growth is usually faster than Apriori on large datasets.  
Reason R: FP-growth mines frequent itemsets from a compressed FP-tree without generating candidate itemsets.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Apriori needs repeated database scans and candidate generation.

</details>

**Q17.** `Medium`  
The lift of an association rule A → B is defined as

(1) confidence(A → B) / support(B)  
(2) confidence(A → B) × support(A)  
(3) support(A) × support(B)  
(4) support(A ∪ B)  

<details><summary>Answer</summary>

**(1)** — Lift > 1 indicates positive correlation; lift = 1 means independence.

</details>

**Q18.** `High`  
Match List I with List II.  
List I (Technique): A. Classification  B. Clustering  C. Association rule mining  D. Regression  
List II (Description): I. Predicting a continuous numeric value  II. Assigning objects to predefined classes using labelled training data  III. Grouping similar objects without predefined labels  IV. Discovering items that frequently occur together

(1) A-II, B-III, C-IV, D-I  
(2) A-III, B-II, C-IV, D-I  
(3) A-II, B-III, C-I, D-IV  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(1)** — Classification and regression are supervised; clustering is unsupervised.

</details>

**Q19.** `High`  
The entropy of a training set with 9 positive and 5 negative examples is approximately

(1) 0.357  
(2) 1.0  
(3) 0.5  
(4) 0.940  

<details><summary>Answer</summary>

**(4)** — −(9/14) log2(9/14) − (5/14) log2(5/14) ≈ 0.940.

</details>

**Q20.** `Medium`  
A set with 9 positive and 5 negative examples is split on an attribute into subsets with class counts (2+, 3−), (4+, 0−) and (3+, 2−). The information gain of the split is approximately

(1) 0.940  
(2) 0.247  
(3) 0.048  
(4) 0.151  

<details><summary>Answer</summary>

**(2)** — 0.940 − [(5/14)(0.971) + (4/14)(0) + (5/14)(0.971)] ≈ 0.247.

</details>

**Q21.** `Medium`  
Match List I with List II.  
List I (Decision-tree algorithm): A. ID3  B. C4.5  C. CART  
List II (Splitting criterion): I. Gini index  II. Information gain  III. Gain ratio

(1) A-I, B-III, C-II  
(2) A-II, B-III, C-I  
(3) A-II, B-I, C-III  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(2)** — Gain ratio corrects information gain's bias towards many-valued attributes.

</details>

**Q22.** `Medium`  
The Gini index of a node with 9 positive and 5 negative examples is approximately

(1) 0.459  
(2) 0.940  
(3) 0.153  
(4) 0.643  

<details><summary>Answer</summary>

**(1)** — 1 − (9/14)² − (5/14)² ≈ 0.459.

</details>

**Q23.** `High`  
Given below are two statements.  
Statement I: k-nearest neighbour is a lazy learner that does no generalisation until a query is received.  
Statement II: In k-NN, a larger value of k always reduces the classification error.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Too large a k blurs class boundaries; k is usually chosen by validation (often odd to avoid ties).

</details>

**Q24.** `Medium`  
The Euclidean and Manhattan distances between the points (1, 2) and (4, 6) are respectively

(1) 25 and 7  
(2) 5 and 5  
(3) 5 and 7  
(4) 7 and 5  

<details><summary>Answer</summary>

**(3)** — Euclidean: sqrt(3² + 4²) = 5; Manhattan: 3 + 4 = 7.

</details>

**Q25.** `High`  
Given below are two statements.  
Statement I: A support vector machine finds the hyperplane that maximises the margin between classes.  
Statement II: The support vectors are the training points that lie closest to the decision boundary.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Kernels (polynomial, RBF) let SVMs learn non-linear boundaries.

</details>

**Q26.** `Medium`  
The kernel trick in support vector machines allows

(1) faster training on linear data only  
(2) computing inner products in a high-dimensional feature space without mapping the data explicitly  
(3) using SVMs for clustering only  
(4) eliminating support vectors  

<details><summary>Answer</summary>

**(2)** — This lets SVMs learn non-linear decision boundaries efficiently.

</details>

**Q27.** `High`  
Match List I with List II.  
List I (Hidden Markov model problem): A. Evaluation  B. Decoding  C. Learning  
List II (Algorithm): I. Baum-Welch (forward-backward)  II. Forward algorithm  III. Viterbi algorithm

(1) A-III, B-II, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-III, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(3)** — The three fundamental problems of HMMs.

</details>

**Q28.** `Medium`  
In a hidden Markov model,

(1) the states are hidden and only the observations emitted by them are visible  
(2) there are no transition probabilities  
(3) observations are independent of states  
(4) the states are directly observed  

<details><summary>Answer</summary>

**(1)** — An HMM is defined by transition probabilities, emission probabilities and initial-state probabilities.

</details>

**Q29.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: k-medoids clustering is more sensitive to outliers than k-means.  
Reason R: k-means represents each cluster by the mean of its points, which extreme values can shift substantially.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — k-medoids uses actual data points as centres and is more robust to outliers than k-means.

</details>

**Q30.** `Medium`  
Match List I with List II.  
List I (Clustering method): A. k-means  B. Agglomerative hierarchical  C. DBSCAN  D. k-medoids (PAM)  
List II (Category or feature): I. Density-based; finds clusters of arbitrary shape and marks noise  II. Partitioning; cluster centre is an actual object  III. Partitioning; cluster centre is the mean  IV. Builds a dendrogram by repeatedly merging the closest clusters

(1) A-III, B-IV, C-I, D-II  
(2) A-II, B-IV, C-I, D-III  
(3) A-III, B-I, C-IV, D-II  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(1)** — Common clustering algorithms.

</details>

**Q31.** `Medium`  
In DBSCAN, the two parameters that must be specified are

(1) k and the number of iterations  
(2) ε (neighbourhood radius) and MinPts  
(3) the number of clusters and the learning rate  
(4) support and confidence  

<details><summary>Answer</summary>

**(2)** — Points with at least MinPts neighbours within ε are core points.

</details>

**Q32.** `Medium`  
In hierarchical clustering, single linkage defines the distance between two clusters as

(1) the maximum distance between their points  
(2) the average distance between their points  
(3) the distance between their centroids  
(4) the minimum distance between their points  

<details><summary>Answer</summary>

**(4)** — Complete linkage uses the maximum distance and average linkage the mean.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: k-means always finds the globally optimal clustering.  
Statement II: k-means requires the number of clusters k to be specified in advance.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — k-means converges to a local optimum that depends on the initial centres.

</details>

**Q34.** `Medium`  
Match List I with List II.  
List I (Mining task): A. Link analysis  B. Sequence (sequential pattern) analysis  C. Social network analysis  D. Summarization  
List II (Example): I. Finding influential people using centrality measures  II. PageRank and HITS (hubs and authorities)  III. Customers who buy a PC then buy a printer within a month  IV. Producing a compact description of a subset of data

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-I, C-III, D-IV  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(4)** — Descriptive mining tasks listed in the syllabus.

</details>

**Q35.** `Medium`  
In social network analysis, betweenness centrality of a node measures

(1) how often it lies on shortest paths between other nodes  
(2) the average distance to all other nodes  
(3) the number of its direct connections  
(4) its PageRank  

<details><summary>Answer</summary>

**(1)** — Degree centrality counts connections; closeness centrality uses the average distance.

</details>

**Q36.** `Medium`  
Dependency modelling in data mining refers to

(1) finding significant dependencies between variables, for example with Bayesian networks  
(2) clustering data  
(3) indexing data  
(4) removing duplicate records  

<details><summary>Answer</summary>

**(1)** — Models can be structural (which variables depend on which) or quantitative (strengths).

</details>

**Q37.** `Medium`  
Linear regression fits a model of the form

(1) y = a + bx that minimises the sum of squared errors  
(2) y = 1 / (1 + e^(−x))  
(3) a set of association rules  
(4) a decision tree  

<details><summary>Answer</summary>

**(1)** — Logistic regression, which uses the sigmoid, is used for classification.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: Overfitting occurs when a model learns noise in the training data and performs poorly on unseen data.  
Statement II: Pruning a decision tree increases overfitting.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Pruning removes branches that fit noise, so it reduces overfitting.

</details>

**Q39.** `Medium`  
Naive Bayes classification assumes that

(1) attributes are conditionally independent given the class  
(2) all attributes are numeric  
(3) there are only two classes  
(4) the classes are equally likely  

<details><summary>Answer</summary>

**(1)** — Despite this strong assumption, it often works well in practice.

</details>

**Q40.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Data warehouses are usually denormalized.  
Reason R: Denormalization reduces the number of joins needed by analytical queries, at the cost of redundancy.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Updates are rare in a warehouse, so redundancy causes few anomalies.

</details>

**Q41.** `Medium`  
A slowly changing dimension of Type 2 handles a change in a dimension attribute by

(1) overwriting the old value  
(2) deleting the dimension  
(3) adding a new column only  
(4) adding a new row with the new value, keeping the old row for history  

<details><summary>Answer</summary>

**(4)** — Type 1 overwrites; Type 3 adds a column for the previous value.

</details>

**Q42.** `Medium`  
Given below are two statements.  
Statement I: A fact table typically contains numeric measures and foreign keys to dimension tables.  
Statement II: Dimension tables are usually much larger than fact tables.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Fact tables, with one row per event, are usually far larger.

</details>

**Q43.** `Low`  
Which of the following is an example of a measure in a sales data warehouse?

(1) Product name  
(2) Store city  
(3) Month  
(4) Sales amount  

<details><summary>Answer</summary>

**(4)** — Measures are numeric facts that are aggregated; the others are dimension attributes.

</details>

**Q44.** `Medium`  
In the Apriori algorithm, candidate itemsets of size k are generated by

(1) random selection  
(2) joining frequent itemsets of size k − 1 and pruning candidates with an infrequent subset  
(3) scanning the database once  
(4) sorting transactions  

<details><summary>Answer</summary>

**(2)** — The database is then scanned to count the support of the remaining candidates.

</details>

**Q45.** `Medium`  
Precision in classification is defined as

(1) TP / (TP + FN)  
(2) (TP + TN) / total  
(3) TP / (TP + FP)  
(4) TN / (TN + FP)  

<details><summary>Answer</summary>

**(3)** — Recall (sensitivity) is TP / (TP + FN).

</details>
