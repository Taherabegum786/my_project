# Set 7 — Memory Management (address binding, contiguous allocation, paging, TLB, segmentation)

**49 questions** — High: 19, Medium: 29, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Consider a logical address space of 8 pages of 1024 words each, mapped onto a physical memory of 32 frames. The number of bits in the logical address and in the physical address are respectively

(1) 15 and 13  
(2) 13 and 10  
(3) 13 and 15  
(4) 10 and 15  

<details><summary>Answer</summary>

**(3)** — Logical: 8 × 1024 = 2^13 words; physical: 32 × 1024 = 2^15 words.

</details>

**Q2.** `High`  
A system uses 32-bit logical addresses, a page size of 4 KB and page-table entries of 4 bytes. The size of a single-level page table for one process is

(1) 4 MB  
(2) 4 KB  
(3) 1 MB  
(4) 2 MB  

<details><summary>Answer</summary>

**(1)** — 2^32 / 2^12 = 2^20 entries × 4 bytes = 4 MB.

</details>

**Q3.** `High`  
A computer has 64 MB of physical memory and a frame size of 4 KB. The number of bits needed for the frame number is

(1) 12  
(2) 26  
(3) 14  
(4) 16  

<details><summary>Answer</summary>

**(3)** — 64 MB / 4 KB = 2^26 / 2^12 = 2^14 frames.

</details>

**Q4.** `High`  
With a page size of 1024 bytes, the logical address 10000 (decimal) corresponds to

(1) page 8, offset 784  
(2) page 9, offset 1000  
(3) page 10, offset 0  
(4) page 9, offset 784  

<details><summary>Answer</summary>

**(4)** — 10000 / 1024 = 9 remainder 784.

</details>

**Q5.** `Medium`  
With a 4 KB page size, the 16-bit virtual address 0x3A7F has page number and offset

(1) 0x3A and 0x7F  
(2) 0xA and 0x37F  
(3) 7 and 0xA3F  
(4) 3 and 0xA7F  

<details><summary>Answer</summary>

**(4)** — The low 12 bits (0xA7F) are the offset; the remaining bits (0x3) give the page number.

</details>

**Q6.** `High`  
In a paging system with a TLB, the TLB access time is 20 ns, the memory access time is 100 ns and the TLB hit ratio is 80%. The effective memory access time is

(1) 120 ns  
(2) 220 ns  
(3) 140 ns  
(4) 200 ns  

<details><summary>Answer</summary>

**(3)** — EAT = 0.8 × (20 + 100) + 0.2 × (20 + 100 + 100) = 96 + 44 = 140 ns.

</details>

**Q7.** `High`  
In a paging system the TLB lookup takes 20 ns and a memory access 100 ns. If the hit ratio is 98%, the effective access time is

(1) 122 ns  
(2) 220 ns  
(3) 140 ns  
(4) 120 ns  

<details><summary>Answer</summary>

**(1)** — EAT = 0.98 × 120 + 0.02 × 220 = 117.6 + 4.4 = 122 ns.

</details>

**Q8.** `High`  
The TLB lookup takes 20 ns and a memory access 100 ns. The minimum TLB hit ratio needed to keep the effective memory access time at 130 ns is

(1) 95%  
(2) 90%  
(3) 80%  
(4) 85%  

<details><summary>Answer</summary>

**(2)** — 130 = h × 120 + (1 − h) × 220 gives 100h = 90, so h = 0.9.

</details>

**Q9.** `Medium`  
Without a TLB, a paging system with a single-level page table kept in memory, where a memory access takes 100 ns, has an effective access time of

(1) 200 ns  
(2) 100 ns  
(3) 300 ns  
(4) 150 ns  

<details><summary>Answer</summary>

**(1)** — Each reference needs one access for the page-table entry and one for the data.

</details>

**Q10.** `High`  
A TLB has 64 entries and the page size is 4 KB. The TLB reach is

(1) 64 KB  
(2) 4 MB  
(3) 16 MB  
(4) 256 KB  

<details><summary>Answer</summary>

**(4)** — TLB reach = number of entries × page size = 64 × 4 KB.

</details>

**Q11.** `High`  
Given below are two statements.  
Statement I: Paging eliminates internal fragmentation but can suffer from external fragmentation.  
Statement II: Segmentation eliminates internal fragmentation but can suffer from external fragmentation.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Paging is the reverse: no external fragmentation, but internal fragmentation in the last page.

</details>

**Q12.** `High`  
Match List I with List II.  
List I (Address binding time): A. Compile time  B. Load time  C. Execution time  
List II (Result): I. Requires hardware support such as a relocation register (MMU)  II. Absolute code is generated  III. Relocatable code is generated

(1) A-II, B-III, C-I  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — Execution-time binding lets a process move in memory during execution.

</details>

**Q13.** `High`  
With a relocation register value of 14000, the logical address 346 is mapped to the physical address

(1) 346  
(2) 14346  
(3) 13654  
(4) 14000  

<details><summary>Answer</summary>

**(2)** — Physical address = relocation (base) value + logical address.

</details>

**Q14.** `High`  
Memory partitions of 100 KB, 500 KB, 200 KB, 300 KB and 600 KB (in order) must hold processes of 212 KB, 417 KB, 112 KB and 426 KB (in order). Which placement algorithm allocates all four processes?

(1) First fit  
(2) Next fit starting at the 600 KB partition  
(3) Best fit  
(4) Worst fit  

<details><summary>Answer</summary>

**(3)** — Best fit uses 300, 500, 200 and 600 KB; first fit and worst fit leave the 426 KB process waiting.

</details>

**Q15.** `High`  
Memory partitions of 100 KB, 500 KB, 200 KB, 300 KB and 600 KB (in order) must hold processes of 212 KB, 417 KB, 112 KB and 426 KB (in order). Using first fit, the 112 KB process is placed in

(1) the 183 KB remainder of the 600 KB partition  
(2) the 200 KB partition  
(3) the 288 KB remainder of the 500 KB partition  
(4) the 300 KB partition  

<details><summary>Answer</summary>

**(3)** — 212 KB goes into 500 (leaving 288), 417 KB into 600, and 112 KB into the first hole large enough, the 288 KB remainder.

</details>

**Q16.** `Medium`  
Given below are two statements.  
Statement I: Best fit searches the entire list unless the list is ordered by size, and produces the smallest leftover hole.  
Statement II: Worst fit allocates the largest hole, producing the largest leftover hole.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Simulations show first fit and best fit are better than worst fit in time and storage use.

</details>

**Q17.** `Medium`  
According to the 50-percent rule for first-fit allocation, if N blocks are allocated, about 0.5N blocks are lost to fragmentation. The fraction of memory that may be unusable is about

(1) one-third  
(2) one-quarter  
(3) one-half  
(4) two-thirds  

<details><summary>Answer</summary>

**(1)** — 0.5N out of 1.5N blocks is one-third.

</details>

**Q18.** `Medium`  
Compaction as a solution to external fragmentation is possible only if

(1) relocation is dynamic and done at execution time  
(2) relocation is static and done at assembly time  
(3) paging is used  
(4) segments are of equal size  

<details><summary>Answer</summary>

**(1)** — Programs and data must be movable, so addresses must be bound at run time.

</details>

**Q19.** `High`  
A segment table has entries (base, limit): segment 0 (219, 600), segment 1 (2300, 14), segment 2 (90, 100), segment 3 (1327, 580), segment 4 (1952, 96). The physical address for the logical address (0, 430) is

(1) 649  
(2) 819  
(3) 430  
(4) 2730  

<details><summary>Answer</summary>

**(1)** — The offset 430 is less than the limit 600, so the address is 219 + 430 = 649.

</details>

**Q20.** `High`  
For the segment table with entries (base, limit): segment 0 (219, 600), segment 1 (2300, 14), segment 2 (90, 100), segment 3 (1327, 580), segment 4 (1952, 96), which logical address causes an addressing-error trap?

(1) (0, 430)  
(2) (2, 500)  
(3) (1, 10)  
(4) (3, 400)  

<details><summary>Answer</summary>

**(2)** — Segment 2 has a limit of 100, so offset 500 is illegal; (1, 10) → 2310 and (3, 400) → 1727 are valid.

</details>

**Q21.** `High`  
Match List I with List II.  
List I (Page-table structure): A. Hierarchical page table  B. Hashed page table  C. Inverted page table  
List II (Characteristic): I. One entry per physical frame of memory  II. The page table itself is paged, e.g. with an outer and an inner table  III. Virtual page numbers are hashed into a table with linked chains, common for address spaces larger than 32 bits

(1) A-III, B-II, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-III, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(3)** — Standard page-table structures.

</details>

**Q22.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: An inverted page table reduces the memory needed to store page tables.  
Reason R: An inverted page table makes it easy to share memory between processes.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — With one entry per frame, a frame can map only one virtual page, which makes sharing difficult.

</details>

**Q23.** `Medium`  
A system with 1 GB of physical memory and a 4 KB page size uses an inverted page table. The number of entries in the table is

(1) 2^30  
(2) 2^20  
(3) 2^12  
(4) 2^18  

<details><summary>Answer</summary>

**(4)** — 2^30 / 2^12 = 2^18 entries, one per frame.

</details>

**Q24.** `High`  
In a two-level paging scheme for a 32-bit logical address with 4 KB pages and 4-byte page-table entries, chosen so that each inner page table fits in one page, the address is divided as

(1) 12 bits outer page, 8 bits inner page, 12 bits offset  
(2) 16 bits outer page, 4 bits inner page, 12 bits offset  
(3) 8 bits outer page, 12 bits inner page, 12 bits offset  
(4) 10 bits outer page, 10 bits inner page, 12 bits offset  

<details><summary>Answer</summary>

**(4)** — A 4 KB page holds 1024 four-byte entries, so each level uses 10 bits.

</details>

**Q25.** `Medium`  
A system has 46-bit virtual addresses, 8 KB pages and 4-byte page-table entries. How many levels of paging are needed if every page table must fit in a single page?

(1) 2  
(2) 3  
(3) 5  
(4) 4  

<details><summary>Answer</summary>

**(2)** — The offset is 13 bits; a page holds 2048 = 2^11 entries; (46 − 13) / 11 = 3 levels.

</details>

**Q26.** `Medium`  
The optimal page size p that minimises page-table overhead plus internal fragmentation, for an average process size s and a page-table-entry size e, is p = sqrt(2se). For s = 1 MB and e = 8 bytes, p is

(1) 4 KB  
(2) 1 KB  
(3) 8 KB  
(4) 2 KB  

<details><summary>Answer</summary>

**(1)** — sqrt(2 × 2^20 × 8) = sqrt(2^24) = 2^12 = 4096 bytes.

</details>

**Q27.** `Medium`  
On average, the internal fragmentation per process in a paging system is about

(1) one frame per segment  
(2) one page  
(3) zero  
(4) half a page  

<details><summary>Answer</summary>

**(4)** — Only the last page of a process is partly used, on average half-full.

</details>

**Q28.** `Medium`  
The valid-invalid bit in a page-table entry indicates

(1) whether the page is read-only  
(2) whether the page is shared  
(3) whether the page has been modified  
(4) whether the page is in the process's logical address space (and, with demand paging, in memory)  

<details><summary>Answer</summary>

**(4)** — Accessing an invalid page causes a trap to the operating system.

</details>

**Q29.** `Medium`  
An address space identifier (ASID) stored in each TLB entry

(1) identifies the process the entry belongs to, so the TLB need not be flushed on every context switch  
(2) stores the frame number  
(3) marks the entry as dirty  
(4) stores the page offset  

<details><summary>Answer</summary>

**(1)** — Without ASIDs, the TLB must be flushed when the address space changes.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: Shared pages allow several processes to share the same reentrant code, such as a library.  
Statement II: To share code, the code must not modify itself during execution.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Each process has its own data pages while mapping the same code frames.

</details>

**Q31.** `Medium`  
In the Intel IA-32 architecture, a logical address is translated by the segmentation unit into a

(1) virtual page number  
(2) segment selector  
(3) linear address, which the paging unit translates into a physical address  
(4) physical address directly  

<details><summary>Answer</summary>

**(3)** — IA-32 supports segmentation with paging.

</details>

**Q32.** `High`  
Using the buddy system with a 256 KB memory segment, a request for 21 KB is satisfied with a block of size

(1) 21 KB  
(2) 64 KB  
(3) 24 KB  
(4) 32 KB  

<details><summary>Answer</summary>

**(4)** — Blocks are powers of two: 256 → 128 → 64 → 32; the smallest power of two ≥ 21 KB is 32 KB.

</details>

**Q33.** `Medium`  
In the buddy system, a 32 KB block is allocated for a 21 KB request. The internal fragmentation is

(1) 11 KB  
(2) 0 KB  
(3) 5 KB  
(4) 21 KB  

<details><summary>Answer</summary>

**(1)** — 32 − 21 = 11 KB is wasted inside the block.

</details>

**Q34.** `Medium`  
The slab allocator in the Linux kernel

(1) allocates memory in power-of-two blocks only  
(2) uses caches of pre-allocated objects of each kernel data-structure type, avoiding fragmentation  
(3) is used only for user processes  
(4) is a page-replacement algorithm  

<details><summary>Answer</summary>

**(2)** — Each cache consists of slabs of contiguous pages holding objects of one type.

</details>

**Q35.** `Medium`  
Swapping a process out of memory to a backing store and later back in is used to

(1) speed up I/O  
(2) reduce internal fragmentation  
(3) increase the size of the TLB  
(4) allow the total memory of all processes to exceed physical memory  

<details><summary>Answer</summary>

**(4)** — Modern systems swap pages rather than entire processes.

</details>

**Q36.** `Medium`  
In a system with base and limit registers, an address generated by a user process is legal if

(1) address ≥ base and address &lt; base + limit  
(2) address &lt; base  
(3) address equals base  
(4) address &gt; limit  

<details><summary>Answer</summary>

**(1)** — Otherwise the hardware traps to the operating system.

</details>

**Q37.** `Medium`  
Match List I with List II.  
List I (Term): A. Internal fragmentation  B. External fragmentation  C. Compaction  D. Paging  
List II (Description): I. Memory is free in total but not contiguous  II. Shuffling memory contents to place free memory in one block  III. Allocated memory slightly larger than requested; the difference is unused  IV. Non-contiguous allocation of fixed-size frames

(1) A-I, B-III, C-II, D-IV  
(2) A-III, B-II, C-I, D-IV  
(3) A-III, B-I, C-II, D-IV  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(3)** — Standard memory-management terms.

</details>

**Q38.** `Medium`  
The page-table base register (PTBR)

(1) stores the frame number of the current page  
(2) counts page faults  
(3) stores the size of the TLB  
(4) points to the page table of the currently running process  

<details><summary>Answer</summary>

**(4)** — Changing page tables on a context switch requires changing only this register.

</details>

**Q39.** `Medium`  
Given below are two statements.  
Statement I: A larger page size gives a smaller page table.  
Statement II: A larger page size reduces internal fragmentation.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A larger page wastes more space, on average half a page per process.

</details>

**Q40.** `Medium`  
A paging system uses a logical address space of 2^16 bytes with a page size of 512 bytes. The number of pages and the number of offset bits are

(1) 64 and 10  
(2) 512 and 7  
(3) 256 and 8  
(4) 128 and 9  

<details><summary>Answer</summary>

**(4)** — 2^16 / 2^9 = 2^7 = 128 pages; offset = log2 512 = 9 bits.

</details>

**Q41.** `Medium`  
Which part of the logical address is used to index the page table?

(1) Frame number  
(2) Offset  
(3) Segment limit  
(4) Page number  

<details><summary>Answer</summary>

**(4)** — The page number selects the entry; the offset is copied unchanged into the physical address.

</details>

**Q42.** `Medium`  
In segmentation, a logical address consists of

(1) a frame number and a page number  
(2) a segment number and an offset within the segment  
(3) a page number and an offset  
(4) a base and a limit  

<details><summary>Answer</summary>

**(2)** — The segment number indexes the segment table, which supplies the base and limit.

</details>

**Q43.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Segmentation supports the programmer's view of memory.  
Reason R: A program is viewed as a collection of logical units such as the main program, functions, stack and arrays, each of a different size.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Segmentation maps these variable-size logical units directly.

</details>

**Q44.** `Medium`  
Which of the following problems is NOT solved by paging?

(1) The need for contiguous physical memory for a process  
(2) Fitting variable-size chunks into the backing store  
(3) External fragmentation  
(4) Internal fragmentation  

<details><summary>Answer</summary>

**(4)** — Paging still wastes part of the last page of a process.

</details>

**Q45.** `Medium`  
In a paged system, the page-table length register (PTLR) is used to

(1) count the number of frames  
(2) store the size of the TLB  
(3) store the length of each page  
(4) check that a page number is within the valid range for the process  

<details><summary>Answer</summary>

**(4)** — Page numbers beyond the PTLR value cause a trap.

</details>

**Q46.** `Medium`  
A system with 48-bit virtual addresses and 4 KB pages would need how many entries in a single-level page table?

(1) 2^24  
(2) 2^48  
(3) 2^36  
(4) 2^12  

<details><summary>Answer</summary>

**(3)** — 2^48 / 2^12 = 2^36 entries, which is why multilevel or hashed tables are used.

</details>

**Q47.** `Medium`  
In a paging system, physical memory is divided into fixed-size blocks called

(1) segments  
(2) frames  
(3) partitions  
(4) pages  

<details><summary>Answer</summary>

**(2)** — Logical memory is divided into pages of the same size.

</details>

**Q48.** `Low`  
Which memory allocation technique places a new process in the first free hole after the point where the previous search ended?

(1) Best fit  
(2) Worst fit  
(3) Next fit  
(4) First fit  

<details><summary>Answer</summary>

**(3)** — Next fit is a variation of first fit that starts each search where the last one ended.

</details>

**Q49.** `Medium`  
In a system using paging, each memory reference to a page table entry that is not cached requires

(1) one extra memory access per level of the page table  
(2) a TLB flush  
(3) no memory access  
(4) a disk access  

<details><summary>Answer</summary>

**(1)** — A two-level table needs two extra accesses on a TLB miss.

</details>
