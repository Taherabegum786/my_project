# Set 9 — Storage Management (disk structure, disk scheduling, RAID, disk management)

**45 questions** — High: 14, Medium: 30, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A disk has 200 cylinders (0 to 199). The request queue is 98, 183, 37, 122, 14, 124, 65, 67 and the head is at cylinder 53. The total head movement under FCFS scheduling is

(1) 236  
(2) 640  
(3) 208  
(4) 382  

<details><summary>Answer</summary>

**(2)** — 53→98→183→37→122→14→124→65→67 = 45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = 640 cylinders.

</details>

**Q2.** `High`  
A disk has 200 cylinders (0 to 199). The request queue is 98, 183, 37, 122, 14, 124, 65, 67 and the head is at cylinder 53. The total head movement under SSTF scheduling is

(1) 299  
(2) 208  
(3) 236  
(4) 640  

<details><summary>Answer</summary>

**(3)** — Order 65, 67, 37, 14, 98, 122, 124, 183: 12 + 2 + 30 + 23 + 84 + 24 + 2 + 59 = 236.

</details>

**Q3.** `High`  
A disk has 200 cylinders (0 to 199). The request queue is 98, 183, 37, 122, 14, 124, 65, 67 and the head is at cylinder 53, moving towards cylinder 0. The total head movement under SCAN scheduling is

(1) 236  
(2) 331  
(3) 382  
(4) 208  

<details><summary>Answer</summary>

**(1)** — 53 → 0 (53 cylinders), then 0 → 183 (183 cylinders): 236.

</details>

**Q4.** `Medium`  
A disk has 200 cylinders (0 to 199). The request queue is 98, 183, 37, 122, 14, 124, 65, 67 and the head is at cylinder 53, moving towards cylinder 0. The total head movement under LOOK scheduling is

(1) 299  
(2) 236  
(3) 322  
(4) 208  

<details><summary>Answer</summary>

**(4)** — 53 → 14 (39 cylinders), then 14 → 183 (169 cylinders): 208.

</details>

**Q5.** `High`  
A disk has 200 cylinders (0 to 199). The request queue is 98, 183, 37, 122, 14, 124, 65, 67 and the head is at cylinder 53, moving towards higher cylinders. The total head movement under C-SCAN, counting the return seek from 199 to 0, is

(1) 382  
(2) 331  
(3) 386  
(4) 322  

<details><summary>Answer</summary>

**(1)** — 53 → 199 (146), 199 → 0 (199), 0 → 37 (37): 382.

</details>

**Q6.** `Medium`  
A disk has 200 cylinders (0 to 199). The request queue is 98, 183, 37, 122, 14, 124, 65, 67 and the head is at cylinder 53, moving towards higher cylinders. The total head movement under C-LOOK, counting the jump back, is

(1) 322  
(2) 382  
(3) 331  
(4) 299  

<details><summary>Answer</summary>

**(1)** — 53 → 183 (130), jump 183 → 14 (169), 14 → 37 (23): 322.

</details>

**Q7.** `High`  
A disk has 200 cylinders (0 to 199). The request queue is 82, 170, 43, 140, 24, 16, 190 and the head is at cylinder 50. The total head movement under SSTF scheduling is

(1) 642  
(2) 314  
(3) 332  
(4) 208  

<details><summary>Answer</summary>

**(4)** — Order 43, 24, 16, 82, 140, 170, 190: 7 + 19 + 8 + 66 + 58 + 30 + 20 = 208.

</details>

**Q8.** `Medium`  
A disk has 200 cylinders (0 to 199). The request queue is 82, 170, 43, 140, 24, 16, 190 and the head is at cylinder 50, moving towards higher cylinders. The total head movement under SCAN scheduling is

(1) 391  
(2) 314  
(3) 332  
(4) 341  

<details><summary>Answer</summary>

**(3)** — 50 → 199 (149), then 199 → 16 (183): 332.

</details>

**Q9.** `Medium`  
A disk has 200 cylinders (0 to 199). The request queue is 82, 170, 43, 140, 24, 16, 190 and the head is at cylinder 50, moving towards higher cylinders. The total head movement under LOOK scheduling is

(1) 208  
(2) 332  
(3) 341  
(4) 314  

<details><summary>Answer</summary>

**(4)** — 50 → 190 (140), then 190 → 16 (174): 314.

</details>

**Q10.** `Medium`  
A disk has 5000 cylinders (0 to 4999). The head is at cylinder 143 and the queue is 86, 1470, 913, 1774, 948, 1509, 1022, 1750, 130. The total head movement under SSTF is

(1) 1745  
(2) 9769  
(3) 7081  
(4) 3319  

<details><summary>Answer</summary>

**(1)** — Order 130, 86, 913, 948, 1022, 1470, 1509, 1750, 1774: 13 + 44 + 827 + 35 + 74 + 448 + 39 + 241 + 24 = 1745.

</details>

**Q11.** `Medium`  
A disk has 5000 cylinders (0 to 4999). The head is at cylinder 143, moving towards higher cylinders, and the queue is 86, 1470, 913, 1774, 948, 1509, 1022, 1750, 130. The total head movement under LOOK is

(1) 3319  
(2) 3363  
(3) 1745  
(4) 9769  

<details><summary>Answer</summary>

**(1)** — 143 → 1774 (1631), then 1774 → 86 (1688): 3319.

</details>

**Q12.** `High`  
Which disk scheduling algorithm may cause starvation of requests that are far from the current head position?

(1) SSTF  
(2) FCFS  
(3) C-SCAN  
(4) SCAN  

<details><summary>Answer</summary>

**(1)** — SSTF always serves the nearest request, so a stream of nearby requests can postpone distant ones indefinitely.

</details>

**Q13.** `High`  
Match List I with List II.  
List I (Disk scheduling algorithm): A. SCAN  B. C-SCAN  C. LOOK  D. SSTF  
List II (Characteristic): I. Selects the request with the minimum seek time from the current head position  II. Like the elevator algorithm, but the arm goes only as far as the last request in each direction  III. Arm moves end to end, servicing requests in both directions (elevator algorithm)  IV. Services requests in one direction only and returns to the beginning without servicing on the return trip

(1) A-II, B-IV, C-III, D-I  
(2) A-III, B-II, C-IV, D-I  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-II, D-I  

<details><summary>Answer</summary>

**(3)** — Standard disk scheduling algorithms.

</details>

**Q14.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: C-SCAN provides a more uniform waiting time than SCAN.  
Reason R: C-SCAN treats the cylinders as a circular list, so requests at both ends wait about the same time.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — In SCAN, cylinders in the middle are visited twice as often as those at the ends.

</details>

**Q15.** `High`  
A disk has 16 surfaces, 128 tracks per surface, 256 sectors per track and 512 bytes per sector. Its capacity is

(1) 64 MB  
(2) 128 MB  
(3) 512 MB  
(4) 256 MB  

<details><summary>Answer</summary>

**(4)** — 2^4 × 2^7 × 2^8 × 2^9 = 2^28 bytes = 256 MB.

</details>

**Q16.** `High`  
A disk rotates at 7200 rpm. The average rotational latency is approximately

(1) 2.08 ms  
(2) 8.33 ms  
(3) 16.67 ms  
(4) 4.17 ms  

<details><summary>Answer</summary>

**(4)** — One rotation takes 60,000 / 7200 = 8.33 ms; the average latency is half a rotation.

</details>

**Q17.** `Medium`  
A disk rotating at 15,000 rpm has an average rotational latency of

(1) 8 ms  
(2) 1 ms  
(3) 4 ms  
(4) 2 ms  

<details><summary>Answer</summary>

**(4)** — One rotation takes 4 ms; half of it is 2 ms.

</details>

**Q18.** `High`  
A disk has an average seek time of 4 ms, rotates at 6000 rpm and has 100 sectors per track. The average time to read one sector is

(1) 9.1 ms  
(2) 14.1 ms  
(3) 10 ms  
(4) 9 ms  

<details><summary>Answer</summary>

**(1)** — Seek 4 ms + average latency 5 ms + transfer 10 ms / 100 = 0.1 ms, total 9.1 ms.

</details>

**Q19.** `Medium`  
A disk rotates at 6000 rpm and has 100 sectors of 512 bytes per track. The maximum data transfer rate is

(1) 512 KB/s  
(2) 5.12 MB/s  
(3) 6 MB/s  
(4) 51.2 MB/s  

<details><summary>Answer</summary>

**(2)** — 100 rotations per second × 100 × 512 bytes = 5.12 × 10^6 bytes per second.

</details>

**Q20.** `Medium`  
The time for the disk arm to move the heads to the cylinder containing the desired sector is called

(1) positioning time  
(2) transfer time  
(3) seek time  
(4) rotational latency  

<details><summary>Answer</summary>

**(3)** — Positioning (random-access) time = seek time + rotational latency.

</details>

**Q21.** `High`  
Match List I with List II.  
List I (RAID level): A. RAID 0  B. RAID 1  C. RAID 5  D. RAID 6  
List II (Organisation): I. Block-interleaved distributed parity  II. Mirroring  III. P + Q redundancy, tolerating two disk failures  IV. Block striping without redundancy

(1) A-IV, B-I, C-II, D-III  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — Standard RAID levels.

</details>

**Q22.** `High`  
Given below are two statements.  
Statement I: RAID 0 provides redundancy by mirroring every block.  
Statement II: RAID 4 stores parity on a dedicated disk, which can become a bottleneck for writes.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — RAID 0 is striping with no redundancy; mirroring is RAID 1.

</details>

**Q23.** `High`  
A RAID 5 array is built from 5 disks of 1 TB each. Its usable capacity is

(1) 5 TB  
(2) 4 TB  
(3) 2.5 TB  
(4) 1 TB  

<details><summary>Answer</summary>

**(2)** — One disk's worth of space holds parity: (5 − 1) × 1 TB = 4 TB.

</details>

**Q24.** `Medium`  
A RAID 6 array is built from 6 disks of 2 TB each. Its usable capacity is

(1) 6 TB  
(2) 10 TB  
(3) 12 TB  
(4) 8 TB  

<details><summary>Answer</summary>

**(4)** — Two disks' worth of space holds the P and Q redundancy: (6 − 2) × 2 TB = 8 TB.

</details>

**Q25.** `Medium`  
A RAID 1+0 (RAID 10) array uses 4 disks of 1 TB each. Its usable capacity is

(1) 1 TB  
(2) 3 TB  
(3) 2 TB  
(4) 4 TB  

<details><summary>Answer</summary>

**(3)** — Mirroring halves the raw capacity.

</details>

**Q26.** `Medium`  
In a mirrored pair, each disk has a mean time to failure of 100,000 hours and the mean time to repair is 10 hours. Assuming independent failures, the mean time to data loss is

(1) 10^6 hours  
(2) 5 × 10^8 hours  
(3) 10^10 hours  
(4) 10^5 hours  

<details><summary>Answer</summary>

**(2)** — MTTF² / (2 × MTTR) = 10^10 / 20 = 5 × 10^8 hours.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: RAID 1+0 (striped mirrors) is more robust than RAID 0+1 (mirrored stripes) when a single disk fails.  
Statement II: In RAID 0+1, the failure of a single disk makes an entire stripe unavailable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — In RAID 1+0 a failed disk affects only its mirror pair.

</details>

**Q28.** `Medium`  
Which RAID level uses bit-level or byte-level striping with a dedicated parity disk?

(1) RAID 6  
(2) RAID 5  
(3) RAID 3  
(4) RAID 1  

<details><summary>Answer</summary>

**(3)** — RAID 4 uses block-level striping with a dedicated parity disk.

</details>

**Q29.** `Medium`  
Arrange the steps in preparing a new disk for use in the correct order.  
A. Logical formatting (creating a file system)  B. Low-level (physical) formatting  C. Partitioning

(1) B, C, A  
(2) A, B, C  
(3) C, B, A  
(4) B, A, C  

<details><summary>Answer</summary>

**(1)** — Physical formatting creates sectors, partitioning divides the disk, and logical formatting writes file-system structures.

</details>

**Q30.** `Medium`  
Replacing a bad sector logically with a spare sector that the controller maps to the same sector number is called

(1) garbage collection  
(2) sector sparing (forwarding)  
(3) wear leveling  
(4) sector slipping  

<details><summary>Answer</summary>

**(2)** — Sector slipping instead shifts all sectors down by one.

</details>

**Q31.** `Medium`  
Given below are two statements.  
Statement I: Solid-state drives have no moving parts, so they have no seek time or rotational latency.  
Statement II: SSTF scheduling is essential for SSDs because seek time dominates their access time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — SSDs have no seek time, so simple FCFS-like scheduling is used.

</details>

**Q32.** `Medium`  
Wear leveling in NAND flash storage is used to

(1) spread erase cycles evenly across blocks so that no block wears out early  
(2) increase seek time  
(3) reduce rotational latency  
(4) compress data  

<details><summary>Answer</summary>

**(1)** — Each NAND block tolerates a limited number of erase cycles.

</details>

**Q33.** `Medium`  
In NAND flash storage, which of the following is true?

(1) Reads are slower than writes  
(2) There is no limit on erase cycles  
(3) Data can be overwritten in place  
(4) A block must be erased before its pages can be rewritten  

<details><summary>Answer</summary>

**(4)** — The flash translation layer maps logical blocks to physical pages and performs garbage collection.

</details>

**Q34.** `Medium`  
Match List I with List II.  
List I (Storage attachment): A. Host-attached storage  B. Network-attached storage (NAS)  C. Storage-area network (SAN)  
List II (Description): I. Private network connecting servers and storage units, e.g. Fibre Channel  II. Accessed through local I/O ports such as SATA or SCSI  III. Accessed remotely over an IP network using protocols such as NFS or CIFS

(1) A-II, B-III, C-I  
(2) A-II, B-I, C-III  
(3) A-I, B-III, C-II  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(1)** — iSCSI carries SCSI over IP networks.

</details>

**Q35.** `Medium`  
The area of a disk partition that contains the bootstrap code is called the

(1) superblock  
(2) swap space  
(3) inode table  
(4) boot block  

<details><summary>Answer</summary>

**(4)** — The boot block is read by the firmware to start the boot loader.

</details>

**Q36.** `Medium`  
In the disk queue, if requests arrive only one at a time and the queue is always empty or has a single request, then all disk scheduling algorithms

(1) cause starvation  
(2) always perform like SSTF  
(3) perform the same as FCFS  
(4) perform worse than FCFS  

<details><summary>Answer</summary>

**(3)** — Scheduling only helps when there is a queue of requests to reorder.

</details>

**Q37.** `Medium`  
Which disk scheduling algorithm is also known as the elevator algorithm?

(1) SCAN  
(2) SSTF  
(3) FCFS  
(4) C-LOOK  

<details><summary>Answer</summary>

**(1)** — The arm behaves like an elevator, serving requests on the way up and on the way down.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: In C-LOOK, the arm goes only as far as the final request in each direction before jumping back.  
Statement II: In C-LOOK, requests are serviced on the return trip.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Like C-SCAN, C-LOOK services requests in one direction only.

</details>

**Q39.** `Medium`  
The Linux deadline I/O scheduler maintains separate queues for reads and writes and

(1) gives priority to writes  
(2) disables merging of requests  
(3) services only the oldest request  
(4) uses expiration times to prevent starvation of requests  

<details><summary>Answer</summary>

**(4)** — Reads are usually given shorter deadlines because processes block on them.

</details>

**Q40.** `Medium`  
In a disk, the set of tracks at the same arm position on all surfaces is called a

(1) cylinder  
(2) sector  
(3) block  
(4) cluster  

<details><summary>Answer</summary>

**(1)** — Switching surfaces within a cylinder needs no seek.

</details>

**Q41.** `Medium`  
Disk bandwidth is defined as

(1) the number of requests per second  
(2) the number of cylinders per second  
(3) the rotational speed  
(4) the total number of bytes transferred divided by the total time between the first request and the completion of the last transfer  

<details><summary>Answer</summary>

**(4)** — Disk scheduling aims to improve both access time and bandwidth.

</details>

**Q42.** `Low`  
Which RAID level offers the best write performance among levels that provide redundancy, at the cost of 50% storage overhead?

(1) RAID 6  
(2) RAID 1 (or 1+0)  
(3) RAID 5  
(4) RAID 4  

<details><summary>Answer</summary>

**(2)** — Mirroring needs no parity computation; each write simply goes to both disks.

</details>

**Q43.** `Medium`  
Swap space on Linux can be placed

(1) in a separate raw partition or in a file within a normal file system  
(2) only in a raw partition  
(3) only on optical media  
(4) only in main memory  

<details><summary>Answer</summary>

**(1)** — A raw swap partition avoids file-system overhead; a swap file is more flexible.

</details>

**Q44.** `Medium`  
With a request queue of 10, 22, 20, 2, 40, 6, 38 and the head at cylinder 20, which algorithm services the request at cylinder 20 first?

(1) FCFS only  
(2) SSTF only  
(3) Both SSTF and SCAN  
(4) Neither  

<details><summary>Answer</summary>

**(3)** — The head is already at cylinder 20, which is at distance zero; SCAN services it as it starts moving in either direction.

</details>

**Q45.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Disk scheduling is less important for SSDs than for magnetic disks.  
Reason R: SSD access time does not depend on the physical location of the data.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — There is no mechanical movement to minimise.

</details>
