# Set 8 — Virtual Memory (demand paging, page replacement, frame allocation, thrashing, working sets)

**47 questions** — High: 19, Medium: 27, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
For the reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames (initially empty), the number of page faults under FIFO replacement is

(1) 16  
(2) 9  
(3) 15  
(4) 12  

<details><summary>Answer</summary>

**(3)** — FIFO gives 15 faults for this standard reference string.

</details>

**Q2.** `High`  
For the reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames (initially empty), the number of page faults under LRU replacement is

(1) 15  
(2) 9  
(3) 12  
(4) 10  

<details><summary>Answer</summary>

**(3)** — LRU gives 12 faults.

</details>

**Q3.** `High`  
For the reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames (initially empty), the number of page faults under optimal replacement is

(1) 9  
(2) 8  
(3) 6  
(4) 12  

<details><summary>Answer</summary>

**(1)** — The optimal algorithm replaces the page used furthest in the future and gives 9 faults.

</details>

**Q4.** `Medium`  
For the reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 4 frames (initially empty), the numbers of page faults under FIFO and LRU are respectively

(1) 10 and 8  
(2) 10 and 10  
(3) 12 and 8  
(4) 9 and 8  

<details><summary>Answer</summary>

**(1)** — With 4 frames FIFO gives 10 faults and LRU gives 8.

</details>

**Q5.** `High`  
For the reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 under FIFO replacement, the numbers of page faults with 3 frames and with 4 frames are respectively

(1) 9 and 8  
(2) 10 and 9  
(3) 9 and 10  
(4) 10 and 8  

<details><summary>Answer</summary>

**(3)** — More frames give more faults: this is Belady's anomaly.

</details>

**Q6.** `High`  
Belady's anomaly, in which increasing the number of frames can increase the number of page faults, can occur with

(1) optimal replacement  
(2) FIFO  
(3) any stack algorithm  
(4) LRU  

<details><summary>Answer</summary>

**(2)** — LRU and OPT are stack algorithms and never exhibit the anomaly.

</details>

**Q7.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: FIFO page replacement never suffers from Belady's anomaly.  
Reason R: LRU is a stack algorithm: the set of pages in memory with n frames is always a subset of the set with n + 1 frames.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — FIFO is the classic algorithm that does show Belady's anomaly; LRU does not, because it is a stack algorithm.

</details>

**Q8.** `High`  
For the reference string 1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3, 2, 1, 2, 3, 6 with 4 frames (initially empty), the numbers of page faults under FIFO, LRU and optimal replacement are respectively

(1) 10, 10 and 8  
(2) 16, 15 and 11  
(3) 14, 8 and 10  
(4) 14, 10 and 8  

<details><summary>Answer</summary>

**(4)** — Simulation gives FIFO 14, LRU 10 and OPT 8.

</details>

**Q9.** `Medium`  
For the reference string 1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3, 2, 1, 2, 3, 6 with 3 frames (initially empty), the number of page faults under LRU is

(1) 16  
(2) 14  
(3) 11  
(4) 15  

<details><summary>Answer</summary>

**(4)** — Simulation gives LRU 15 (FIFO 16, OPT 11).

</details>

**Q10.** `Medium`  
For the reference string 4, 7, 6, 1, 7, 6, 1, 2, 7, 2 with 3 frames (initially empty), the number of page faults under optimal replacement is

(1) 7  
(2) 5  
(3) 4  
(4) 6  

<details><summary>Answer</summary>

**(2)** — 4, 7, 6 fault; 1 replaces 4; 2 replaces 1 (not used again); total 5.

</details>

**Q11.** `Medium`  
For the reference string 0, 1, 2, 3, 0, 1, 4, 0, 1, 2, 3, 4 under FIFO replacement, the numbers of page faults with 3 and 4 frames are respectively

(1) 9 and 10  
(2) 8 and 10  
(3) 10 and 9  
(4) 9 and 9  

<details><summary>Answer</summary>

**(1)** — This string, too, shows Belady's anomaly.

</details>

**Q12.** `High`  
The page replacement algorithm that has the lowest page-fault rate but cannot be implemented in practice is

(1) Optimal (OPT/MIN)  
(2) FIFO  
(3) LRU  
(4) Second chance  

<details><summary>Answer</summary>

**(1)** — It needs knowledge of the future reference string; it is used as a benchmark.

</details>

**Q13.** `High`  
Given below are two statements.  
Statement I: The second-chance (clock) algorithm is a FIFO algorithm that skips a page whose reference bit is 1, clearing the bit.  
Statement II: If all reference bits are set, second-chance degenerates into FIFO.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The hand clears every bit in one sweep and then replaces the page it started from.

</details>

**Q14.** `Medium`  
In the enhanced second-chance algorithm that uses the (reference bit, modify bit) pair, the best page to replace is in the class

(1) (1, 1)  
(2) (0, 0)  
(3) (1, 0)  
(4) (0, 1)  

<details><summary>Answer</summary>

**(2)** — (0, 0): neither recently used nor modified, so it need not be written back.

</details>

**Q15.** `High`  
In a demand-paging system, the memory access time is 200 ns and the average page-fault service time is 8 ms. If the page-fault rate is 1 in 1000, the effective access time is approximately

(1) 8 ms  
(2) 8.2 µs  
(3) 200 ns  
(4) 1 µs  

<details><summary>Answer</summary>

**(2)** — EAT = 0.999 × 200 + 0.001 × 8,000,000 ≈ 8199.8 ns ≈ 8.2 µs, a 40-fold slowdown.

</details>

**Q16.** `High`  
With a memory access time of 200 ns and a page-fault service time of 8 ms, to keep the slowdown due to paging below 10%, the page-fault rate must be less than about

(1) 1 in 4,000,000  
(2) 1 in 400,000  
(3) 1 in 1000  
(4) 1 in 40,000  

<details><summary>Answer</summary>

**(2)** — 220 > 200 + 7,999,800p gives p < 2.5 × 10^-6, i.e. fewer than 1 fault in 400,000 accesses.

</details>

**Q17.** `Medium`  
A page fault takes 8 ms if a free frame is available or the replaced page is clean, and 20 ms if the replaced page is modified; 70% of replaced pages are modified. The memory access time is 100 ns. The maximum page-fault rate for an effective access time of 200 ns is approximately

(1) 6.1 × 10^-6  
(2) 5 × 10^-6  
(3) 1.25 × 10^-5  
(4) 1 × 10^-4  

<details><summary>Answer</summary>

**(1)** — Average service time = 0.3 × 8 + 0.7 × 20 = 16.4 ms; 200 = (1 − p) 100 + p × 16.4 × 10^6 gives p ≈ 6.1 × 10^-6.

</details>

**Q18.** `High`  
Arrange the steps in handling a page fault in the correct order.  
A. Schedule a disk read of the page into a free frame  B. Trap to the operating system  C. Restart the instruction that caused the fault  D. Check that the reference was a valid memory access  E. Update the page table

(1) B, A, D, E, C  
(2) B, D, E, A, C  
(3) D, B, A, E, C  
(4) B, D, A, E, C  

<details><summary>Answer</summary>

**(4)** — Trap, check validity, read the page, update the tables, restart the instruction.

</details>

**Q19.** `High`  
Thrashing occurs when

(1) the page size is too large  
(2) the CPU is idle because of I/O  
(3) a process spends more time paging than executing  
(4) the TLB hit ratio is 100%  

<details><summary>Answer</summary>

**(3)** — As the degree of multiprogramming increases beyond a point, CPU utilisation drops sharply.

</details>

**Q20.** `High`  
Given below are two statements.  
Statement I: Using a local replacement algorithm completely eliminates thrashing.  
Statement II: If the sum of the working-set sizes of all processes exceeds the number of available frames, thrashing will occur.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Local replacement only stops one thrashing process from stealing frames from others; it does not solve the problem.

</details>

**Q21.** `High`  
Using the working-set model with window Δ = 10, the working set at time t for the most recent references 2, 6, 1, 5, 7, 7, 7, 7, 5, 1 is

(1) {1, 5, 7}  
(2) {7}  
(3) {2, 6, 1, 5, 7, 7}  
(4) {1, 2, 5, 6, 7}  

<details><summary>Answer</summary>

**(4)** — The working set is the set of distinct pages in the last Δ references.

</details>

**Q22.** `Medium`  
In the page-fault frequency (PFF) scheme, if the page-fault rate of a process rises above an upper bound, the OS

(1) allocates another frame to the process  
(2) takes a frame away from the process  
(3) reduces the page size  
(4) terminates the process  

<details><summary>Answer</summary>

**(1)** — If the rate falls below a lower bound, a frame is taken away.

</details>

**Q23.** `High`  
Using proportional allocation, 62 free frames are divided between two processes of 10 pages and 127 pages. The numbers of frames allocated are approximately

(1) 4 and 57  
(2) 10 and 52  
(3) 31 and 31  
(4) 5 and 57  

<details><summary>Answer</summary>

**(1)** — 10/137 × 62 ≈ 4 and 127/137 × 62 ≈ 57.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: The minimum number of frames per process is defined by the computer architecture.  
Statement II: The maximum number of frames per process is defined by the amount of available physical memory.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — An instruction may need several pages at once, which sets the minimum.

</details>

**Q25.** `Medium`  
In global page replacement

(1) a process can select a replacement frame from the set of all frames, even one belonging to another process  
(2) a process selects a replacement frame only from its own set of frames  
(3) no page is ever replaced  
(4) only kernel pages are replaced  

<details><summary>Answer</summary>

**(1)** — Global replacement gives better throughput but a process cannot control its own fault rate.

</details>

**Q26.** `High`  
A program accesses every element of the array int data[128][128], stored in row-major order, with pages of 128 words (one row per page) and fewer frames than rows. If the elements are accessed column by column, the number of page faults is

(1) 16,384  
(2) 1  
(3) 128  
(4) 256  

<details><summary>Answer</summary>

**(1)** — Each access touches a different row (page), so there are 128 × 128 = 16,384 faults; row-by-row access gives only 128.

</details>

**Q27.** `Medium`  
Copy-on-write is used with fork() so that

(1) the child gets a copy of all pages immediately  
(2) the parent and child initially share pages, and a page is copied only when either process writes to it  
(3) the child cannot modify any page  
(4) pages are written to disk on creation  

<details><summary>Answer</summary>

**(2)** — It makes process creation fast, especially when exec() follows immediately.

</details>

**Q28.** `Medium`  
In demand paging, a page is brought into memory

(1) when the process terminates  
(2) only when it is needed (referenced)  
(3) before the process starts  
(4) at fixed intervals  

<details><summary>Answer</summary>

**(2)** — The lazy swapper (pager) never swaps a page in unless it is needed.

</details>

**Q29.** `Medium`  
Pure demand paging means

(1) the page size is fixed at 4 KB  
(2) pages are never replaced  
(3) a process starts with no pages in memory, and even the first instruction causes a page fault  
(4) all pages are loaded at the start  

<details><summary>Answer</summary>

**(3)** — Locality of reference keeps performance reasonable.

</details>

**Q30.** `Medium`  
The dirty (modify) bit associated with a page is used to

(1) avoid writing a page back to disk if it has not been modified  
(2) indicate the page is shared  
(3) indicate that the page has been referenced recently  
(4) mark invalid pages  

<details><summary>Answer</summary>

**(1)** — A clean page can simply be overwritten when it is replaced.

</details>

**Q31.** `High`  
Match List I with List II.  
List I (Page replacement algorithm): A. FIFO  B. Optimal  C. LRU  D. LFU  
List II (Page replaced): I. The page used least recently  II. The page used the fewest number of times  III. The oldest page in memory  IV. The page that will not be used for the longest time

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(2)** — MFU, in contrast, replaces the most frequently used page.

</details>

**Q32.** `Medium`  
LRU can be implemented exactly using

(1) the dirty bit only  
(2) a single reference bit  
(3) a FIFO queue  
(4) counters (time-of-use fields) or a stack of page numbers  

<details><summary>Answer</summary>

**(4)** — Both need hardware support; reference bits only approximate LRU.

</details>

**Q33.** `Medium`  
Locality of reference refers to the tendency of a program to

(1) access a relatively small set of pages over any short period  
(2) access pages in strictly sequential order  
(3) use only one page during its execution  
(4) access memory addresses randomly  

<details><summary>Answer</summary>

**(1)** — Locality is why demand paging and caching work.

</details>

**Q34.** `Medium`  
Memory-mapped files allow

(1) the CPU to read the disk directly  
(2) processes to avoid page faults  
(3) files to be stored in the TLB  
(4) file I/O to be treated as routine memory accesses by mapping disk blocks to pages in memory  

<details><summary>Answer</summary>

**(4)** — After mmap(), reads and writes to memory reach the file through the paging system.

</details>

**Q35.** `Medium`  
Which of the following reduces the number of page faults at process start-up by bringing in several pages at once?

(1) Prepaging  
(2) Compaction  
(3) Copy-on-write  
(4) Page buffering  

<details><summary>Answer</summary>

**(1)** — Prepaging pays off only if most of the pages brought in are actually used.

</details>

**Q36.** `Medium`  
Locking a page in memory (an I/O interlock) is needed when

(1) the page is not in the working set  
(2) the page holds read-only code  
(3) the page is dirty  
(4) an I/O device is transferring data to or from a buffer in that page  

<details><summary>Answer</summary>

**(4)** — Replacing the page during the transfer would corrupt the data.

</details>

**Q37.** `Medium`  
Given below are two statements.  
Statement I: vfork() does not use copy-on-write; the parent is suspended and the child uses the parent's address space.  
Statement II: vfork() is intended for use when the child calls exec() immediately after creation.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Any changes the child makes are visible to the parent.

</details>

**Q38.** `Medium`  
When a page fault occurs and there is no free frame, the operating system

(1) uses a page-replacement algorithm to select a victim frame  
(2) increases the size of memory  
(3) stops all other processes  
(4) terminates the process  

<details><summary>Answer</summary>

**(1)** — The victim is written out if it is dirty, then the new page is read in.

</details>

**Q39.** `Medium`  
If the degree of multiprogramming is increased beyond the point where thrashing begins, CPU utilisation

(1) keeps increasing  
(2) stays constant  
(3) drops sharply  
(4) becomes 100%  

<details><summary>Answer</summary>

**(3)** — Processes spend most of their time waiting on the paging device.

</details>

**Q40.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Virtual memory allows the logical address space of a process to be larger than physical memory.  
Reason R: The TLB caches recently used page-table entries.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but the TLB only speeds up translation; it is not why virtual memory can exceed physical memory.

</details>

**Q41.** `Medium`  
A process references 5 distinct pages and has 3 frames. Under any replacement algorithm, the minimum number of page faults is

(1) 15  
(2) 5  
(3) 3  
(4) 8  

<details><summary>Answer</summary>

**(2)** — Each distinct page faults at least once when first referenced.

</details>

**Q42.** `Medium`  
Which of the following algorithms approximates LRU using a reference bit and a circular list of pages?

(1) LFU  
(2) MFU  
(3) Clock (second chance)  
(4) FIFO  

<details><summary>Answer</summary>

**(3)** — The clock hand advances, clearing reference bits, until it finds a page with bit 0.

</details>

**Q43.** `Medium`  
Given below are two statements.  
Statement I: Increasing the page size generally reduces the number of page faults for programs with good locality.  
Statement II: A smaller page size allows better resolution, bringing in only the memory that is actually needed.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — These are two sides of the page-size trade-off.

</details>

**Q44.** `Medium`  
Which of the following is a counting-based page replacement algorithm?

(1) OPT  
(2) LFU  
(3) LRU  
(4) FIFO  

<details><summary>Answer</summary>

**(2)** — LFU and MFU keep a count of references to each page.

</details>

**Q45.** `Low`  
In Windows and Linux, the area of a disk used to hold pages that have been swapped out of memory is called

(1) swap space  
(2) the page cache  
(3) the master file table  
(4) the boot block  

<details><summary>Answer</summary>

**(1)** — Linux uses swap partitions or swap files; Windows uses pagefile.sys.

</details>

**Q46.** `Medium`  
Which of the following causes a page fault?

(1) Accessing a page whose valid-invalid bit is invalid  
(2) Executing a privileged instruction in kernel mode  
(3) A TLB hit  
(4) Accessing a page that is in memory  

<details><summary>Answer</summary>

**(1)** — The OS then checks whether the reference is illegal or the page is simply not in memory.

</details>

**Q47.** `Medium`  
The working set of a process is defined as

(1) the pages that are dirty  
(2) the set of pages referenced in the most recent Δ references  
(3) the pages in the TLB  
(4) all pages of the process  

<details><summary>Answer</summary>

**(2)** — Too small a Δ misses the locality; too large overlaps several localities.

</details>
