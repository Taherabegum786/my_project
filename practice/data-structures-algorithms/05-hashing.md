# Set 5 — Hashing (hash functions, collision resolution, load factor, analysis)

**31 questions** — High: 11, Medium: 19, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The keys 43, 165, 62, 123, 142 are inserted in that order into a hash table of size 11 with h(k) = k mod 11 and linear probing. The key 142 is stored at index

(1) 10  
(2) 3  
(3) 2  
(4) 1  

<details><summary>Answer</summary>

**(4)** — 142 mod 11 = 10 is taken by 43; index 0 is taken by 165; so 142 goes to index 1.

</details>

**Q2.** `High`  
The keys 89, 18, 49, 58, 69 are inserted in that order into a table of size 10 with h(k) = k mod 10 and linear probing. The keys 58 and 69 are stored at indices

(1) 1 and 2  
(2) 2 and 3  
(3) 0 and 1  
(4) 8 and 9  

<details><summary>Answer</summary>

**(1)** — 49 goes to 0 (after 9); 58 tries 8, 9, 0 and goes to 1; 69 tries 9, 0, 1 and goes to 2.

</details>

**Q3.** `High`  
The keys 89, 18, 49, 58, 69 are inserted in that order into a table of size 10 with h(k) = k mod 10 and quadratic probing (h(k) + i²) mod 10. The keys 58 and 69 are stored at indices

(1) 2 and 4  
(2) 1 and 2  
(3) 2 and 3  
(4) 3 and 0  

<details><summary>Answer</summary>

**(3)** — 58: 8, 9, then (8 + 4) mod 10 = 2. 69: 9, 0, then (9 + 4) mod 10 = 3.

</details>

**Q4.** `High`  
The keys 89, 18, 49, 58, 69 are inserted in that order into a table of size 10 with h1(k) = k mod 10, h2(k) = 7 − (k mod 7) and double hashing (h1 + i·h2) mod 10. The key 49 is stored at index

(1) 6  
(2) 9  
(3) 0  
(4) 3  

<details><summary>Answer</summary>

**(1)** — 49: h1 = 9 is occupied; h2 = 7 − 0 = 7; (9 + 7) mod 10 = 6.

</details>

**Q5.** `Medium`  
The keys 12, 18, 13, 2, 3, 23, 5, 15 are inserted into a table of size 10 with h(k) = k mod 10 and linear probing. The key 15 ends up at index

(1) 5  
(2) 8  
(3) 7  
(4) 9  

<details><summary>Answer</summary>

**(4)** — Indices 2–8 are filled by 12, 13, 2, 3, 23, 5 and 18; 15 probes 5, 6, 7, 8 and lands at 9.

</details>

**Q6.** `High`  
The keys 15, 11, 27, 8, 12, 32, 22, 37 are inserted into a table of size 7 using h(k) = k mod 7 and separate chaining. The length of the longest chain is

(1) 5  
(2) 3  
(3) 4  
(4) 2  

<details><summary>Answer</summary>

**(2)** — 15, 8 and 22 all hash to 1.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Collision resolution): A. Linear probing  B. Quadratic probing  C. Double hashing  D. Separate chaining  
List II (Characteristic): I. Avoids both primary and secondary clustering  II. Suffers from primary clustering  III. Colliding keys are stored in a linked list at the slot  IV. Avoids primary clustering but suffers from secondary clustering

(1) A-II, B-I, C-IV, D-III  
(2) A-IV, B-II, C-I, D-III  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(3)** — Standard properties of collision-resolution methods.

</details>

**Q8.** `High`  
In open addressing with uniform hashing and load factor α < 1, the expected number of probes in an unsuccessful search is at most

(1) α  
(2) 1/(1 − α)  
(3) 1 + α  
(4) log(1/α)  

<details><summary>Answer</summary>

**(2)** — For α = 0.5 this is 2 probes; for α = 0.9 it is 10.

</details>

**Q9.** `Medium`  
With open addressing and uniform hashing, the expected number of probes in an unsuccessful search when the table is 90% full is at most

(1) 9  
(2) 10  
(3) 5  
(4) 2  

<details><summary>Answer</summary>

**(2)** — 1/(1 − 0.9) = 10.

</details>

**Q10.** `Medium`  
With open addressing and uniform hashing, the expected number of probes in a successful search at load factor α = 0.5 is about

(1) 1.5  
(2) 2  
(3) 2.5  
(4) 1.39  

<details><summary>Answer</summary>

**(4)** — (1/α) ln(1/(1 − α)) = 2 ln 2 ≈ 1.39.

</details>

**Q11.** `High`  
In separate chaining with load factor α = n/m and simple uniform hashing, the expected time for an unsuccessful search is

(1) Θ(n)  
(2) Θ(1)  
(3) Θ(α²)  
(4) Θ(1 + α)  

<details><summary>Answer</summary>

**(4)** — The whole chain of length α on average is scanned, plus the cost of hashing.

</details>

**Q12.** `High`  
Given below are two statements.  
Statement I: In open addressing, the load factor can exceed 1.  
Statement II: In separate chaining, the load factor can exceed 1.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Open addressing stores every key in the table itself, so n ≤ m.

</details>

**Q13.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In open addressing, a deleted slot is usually marked as "deleted" instead of being made empty.  
Reason R: Emptying the slot could break the probe sequence and make later keys unreachable by search.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Such tombstones are skipped by searches but reused by insertions.

</details>

**Q14.** `High`  
In the division method h(k) = k mod m, a good choice of m is

(1) any even number  
(2) a prime not too close to a power of 2  
(3) a power of 10  
(4) a power of 2  

<details><summary>Answer</summary>

**(2)** — A power of 2 would use only the low-order bits of the key.

</details>

**Q15.** `Medium`  
The multiplication method of hashing computes h(k) = ⌊m (kA mod 1)⌋ with 0 < A < 1. Knuth suggests A ≈

(1) 0.5  
(2) 0.75  
(3) 0.618 (the golden-ratio conjugate)  
(4) 0.333  

<details><summary>Answer</summary>

**(3)** — (√5 − 1)/2 ≈ 0.618 works well; the value of m is not critical in this method.

</details>

**Q16.** `Medium`  
Three keys are hashed independently and uniformly into a table of 10 slots. The probability that there is at least one collision is

(1) 0.28  
(2) 0.30  
(3) 0.10  
(4) 0.72  

<details><summary>Answer</summary>

**(1)** — P(no collision) = (10 × 9 × 8) / 10³ = 0.72, so P(collision) = 0.28.

</details>

**Q17.** `Medium`  
In universal hashing, for any two distinct keys, the probability that they collide under a hash function chosen at random from the family is at most

(1) 1/m  
(2) 1/n  
(3) 1/m²  
(4) 1/2  

<details><summary>Answer</summary>

**(1)** — This guarantees good expected performance for any input.

</details>

**Q18.** `Medium`  
Given below are two statements.  
Statement I: Perfect hashing guarantees O(1) worst-case search time for a static set of keys.  
Statement II: Perfect hashing typically uses two levels of hashing with universal hash functions.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The second-level table for a slot with n_j keys has size n_j², which makes collisions avoidable.

</details>

**Q19.** `Medium`  
Rehashing is performed when

(1) a search fails  
(2) the hash function returns zero  
(3) a key is deleted  
(4) the load factor exceeds a threshold, so a larger table is allocated and all keys are reinserted  

<details><summary>Answer</summary>

**(4)** — Doubling the table keeps the amortized insertion cost O(1).

</details>

**Q20.** `Medium`  
Linear probing suffers from primary clustering, which means that

(1) keys are stored in linked lists  
(2) long runs of occupied slots form and grow, increasing search times  
(3) keys that hash to the same slot follow the same probe sequence  
(4) the table can never be full  

<details><summary>Answer</summary>

**(2)** — Secondary clustering refers to keys with the same home slot sharing a probe sequence.

</details>

**Q21.** `Medium`  
Quadratic probing with a prime table size is guaranteed to find an empty slot for insertion if the table is

(1) of any load factor  
(2) at least 90% full  
(3) completely full  
(4) at most half full  

<details><summary>Answer</summary>

**(4)** — The first ⌈m/2⌉ probe positions are distinct when m is prime.

</details>

**Q22.** `Medium`  
Cuckoo hashing guarantees

(1) no rehashing ever  
(2) O(log n) lookup  
(3) sorted order of keys  
(4) O(1) worst-case lookup time, since a key is in one of two possible locations  

<details><summary>Answer</summary>

**(4)** — Insertion may displace keys and occasionally requires rehashing.

</details>

**Q23.** `Medium`  
Which of the following is NOT a desirable property of a hash function?

(1) It uses all of the key  
(2) It is fast to compute  
(3) It distributes keys uniformly over the table  
(4) It maps similar keys to the same slot  

<details><summary>Answer</summary>

**(4)** — Similar keys should be spread out to avoid clustering.

</details>

**Q24.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Hash tables are not suitable for range queries.  
Reason R: A hash table keeps its keys in sorted order.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — A good hash function scatters keys, so neighbouring keys are not stored near each other.

</details>

**Q25.** `Medium`  
A hash table of size 10 uses h(k) = k mod 10 and linear probing. After inserting 21, 31, 41 in that order, how many probes are needed to insert 51?

(1) 3  
(2) 1  
(3) 2  
(4) 4  

<details><summary>Answer</summary>

**(4)** — 51 probes slots 1, 2, 3 (taken by 21, 31, 41) and then 4.

</details>

**Q26.** `Medium`  
In separate chaining, inserting a new key at the head of the chain takes

(1) O(1) time  
(2) O(α) time  
(3) O(n) time  
(4) O(log n) time  

<details><summary>Answer</summary>

**(1)** — Checking for duplicates first would cost O(1 + α).

</details>

**Q27.** `Medium`  
In double hashing, the second hash function h2(k) must never evaluate to

(1) an odd number  
(2) a prime  
(3) 0  
(4) 1  

<details><summary>Answer</summary>

**(3)** — A zero step would probe the same slot forever; h2(k) should also be relatively prime to m.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: Extendible hashing uses a directory of pointers to buckets.  
Statement II: Linear hashing requires a directory that doubles on every split.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Linear hashing needs no directory; buckets are split in a fixed linear order.

</details>

**Q29.** `Low`  
A Bloom filter can report

(1) only exact counts  
(2) false negatives but not false positives  
(3) neither false positives nor false negatives  
(4) false positives but not false negatives  

<details><summary>Answer</summary>

**(4)** — It is a space-efficient probabilistic set-membership structure.

</details>

**Q30.** `Medium`  
The keys 25, 36, 47, 58 are inserted into a table of size 11 with h(k) = k mod 11 and linear probing. The number of collisions (occupied slots probed) is

(1) 3  
(2) 0  
(3) 10  
(4) 6  

<details><summary>Answer</summary>

**(4)** — All four hash to 3: 36 makes 1 probe of an occupied slot, 47 makes 2 and 58 makes 3, total 6.

</details>

**Q31.** `Medium`  
In the mid-square hashing method

(1) the key is multiplied by 0.618  
(2) the key is split into parts that are added  
(3) the key is squared and the middle digits of the result are used as the address  
(4) the key is divided by the table size  

<details><summary>Answer</summary>

**(3)** — Folding splits the key into parts that are added together.

</details>
