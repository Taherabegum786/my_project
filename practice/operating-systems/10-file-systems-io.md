# Set 10 — File Systems and I/O Systems (access methods, directories, allocation, free-space management, I/O hardware and kernel I/O)

**48 questions** — High: 13, Medium: 34, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A UNIX file system uses 1 KB blocks and 4-byte block addresses. An inode has 10 direct pointers, one single-indirect pointer and one double-indirect pointer. The maximum file size is approximately

(1) 64 MB  
(2) 16 GB  
(3) 266 KB  
(4) 10 KB  

<details><summary>Answer</summary>

**(1)** — (10 + 256 + 256²) × 1 KB = 65,802 KB ≈ 64.26 MB.

</details>

**Q2.** `High`  
A file system uses 4 KB blocks and 4-byte block addresses. An inode has 12 direct pointers and one single-, one double- and one triple-indirect pointer. The maximum file size is approximately

(1) 16 GB  
(2) 4 GB  
(3) 16 TB  
(4) 4 TB  

<details><summary>Answer</summary>

**(4)** — Each indirect block holds 1024 pointers: (12 + 1024 + 1024² + 1024³) × 4 KB ≈ 4 TB, dominated by the triple-indirect part.

</details>

**Q3.** `Medium`  
A file system uses 4 KB blocks and 4-byte block addresses. An inode has 12 direct pointers, one single-indirect pointer and one double-indirect pointer. The maximum file size is approximately

(1) 4 MB  
(2) 4 TB  
(3) 4 GB  
(4) 16 GB  

<details><summary>Answer</summary>

**(3)** — (12 + 1024 + 1024²) × 4 KB ≈ 4.004 GB.

</details>

**Q4.** `Medium`  
An inode has 10 direct pointers and 1 KB blocks. The byte at offset 20,000 of a file is found through the

(1) direct pointers  
(2) triple-indirect pointer  
(3) double-indirect pointer  
(4) single-indirect pointer  

<details><summary>Answer</summary>

**(4)** — 20,000 / 1024 gives logical block 19; blocks 0–9 are direct, so block 19 is the 10th entry of the single-indirect block.

</details>

**Q5.** `High`  
A 1 TB disk with 4 KB blocks manages free space with a bit vector. The size of the bit vector is

(1) 4 MB  
(2) 256 MB  
(3) 1 GB  
(4) 32 MB  

<details><summary>Answer</summary>

**(4)** — 2^40 / 2^12 = 2^28 blocks; 2^28 bits = 2^25 bytes = 32 MB.

</details>

**Q6.** `High`  
Match List I with List II.  
List I (File allocation method): A. Contiguous allocation  B. Linked allocation  C. Indexed allocation  
List II (Characteristic): I. Uses an index block holding all the block addresses; supports direct access without external fragmentation  II. Supports direct access easily but suffers from external fragmentation and difficulty growing files  III. No external fragmentation, but efficient only for sequential access

(1) A-II, B-III, C-I  
(2) A-II, B-I, C-III  
(3) A-I, B-III, C-II  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(1)** — The three classical disk allocation methods.

</details>

**Q7.** `High`  
Given below are two statements.  
Statement I: The File Allocation Table (FAT) used by MS-DOS is a variation of linked allocation.  
Statement II: In FAT, random access time is improved because the table can be cached and followed without reading every data block.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — The FAT holds one entry per block containing the number of the next block.

</details>

**Q8.** `High`  
A file of 100 blocks already exists, and its file-control block is in memory. How many disk I/O operations are needed to add a block at the beginning of the file under contiguous, linked and indexed allocation respectively (assuming there is room to grow only at the end for contiguous allocation)?

(1) 201, 2 and 1  
(2) 201, 1 and 1  
(3) 100, 1 and 2  
(4) 1, 101 and 1  

<details><summary>Answer</summary>

**(2)** — Contiguous: read and rewrite 100 blocks shifted by one, plus write the new block (201). Linked and indexed: write the new block only; the FCB in memory is updated.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Directory structure): A. Single-level  B. Two-level  C. Tree-structured  D. Acyclic graph  
List II (Feature): I. Allows files and subdirectories to be shared through links  II. All files in one directory, so names must be unique  III. A separate user file directory for each user under a master file directory  IV. Arbitrary depth with absolute and relative path names

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-III, B-II, C-IV, D-I  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(1)** — Standard directory structures.

</details>

**Q10.** `High`  
Given below are two statements.  
Statement I: A hard link can point to a file in a different file system.  
Statement II: When the target of a symbolic link is deleted, the symbolic link is left dangling.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A hard link refers to an inode number, which is meaningful only within one file system.

</details>

**Q11.** `High`  
The UNIX command chmod 754 file sets the permissions to

(1) rw-r-xr--  
(2) rwxrw-r--  
(3) rwxr-x--x  
(4) rwxr-xr--  

<details><summary>Answer</summary>

**(4)** — 7 = rwx (owner), 5 = r-x (group), 4 = r-- (others).

</details>

**Q12.** `High`  
If the umask is 022, a newly created regular file (default mode 666) gets the permissions

(1) rwxr-xr-x  
(2) rw-------  
(3) rw-r--r--  
(4) rw-rw-rw-  

<details><summary>Answer</summary>

**(3)** — 666 with the 022 bits cleared gives 644 = rw-r--r--; directories (777) get 755.

</details>

**Q13.** `Medium`  
Match List I with List II.  
List I (Access method): A. Sequential access  B. Direct (relative) access  C. Indexed access  
List II (Description): I. Blocks can be read or written in any order using a relative block number  II. An index of pointers to blocks is searched to find a record  III. Records are processed in order, one after the other, like a tape

(1) A-I, B-III, C-II  
(2) A-III, B-II, C-I  
(3) A-III, B-I, C-II  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(3)** — Standard file access methods.

</details>

**Q14.** `High`  
Arrange the layers of a layered file system from the top (closest to the application) to the bottom.  
A. Basic file system  B. Logical file system  C. I/O control  D. File-organisation module

(1) D, B, A, C  
(2) B, D, C, A  
(3) B, D, A, C  
(4) B, A, D, C  

<details><summary>Answer</summary>

**(3)** — Application programs → logical file system → file-organisation module → basic file system → I/O control → devices.

</details>

**Q15.** `Medium`  
In UNIX, the file control block (FCB) is called the

(1) inode  
(2) dentry  
(3) file descriptor  
(4) superblock  

<details><summary>Answer</summary>

**(1)** — The inode stores ownership, permissions, size, timestamps and block pointers.

</details>

**Q16.** `Medium`  
In the Linux virtual file system (VFS), the four primary object types are

(1) process, thread, task and signal  
(2) inode, file, superblock and dentry  
(3) block, sector, track and cylinder  
(4) file, directory, link and pipe  

<details><summary>Answer</summary>

**(2)** — VFS lets the kernel treat different file systems uniformly.

</details>

**Q17.** `Medium`  
A bit vector 0000 0000 0000 0000 0000 0000 0010 1100 (16-bit words, 1 means free) is used for free-space management. The number of the first free block is

(1) 34  
(2) 50  
(3) 42  
(4) 26  

<details><summary>Answer</summary>

**(4)** — The first 16-bit word is all 0s; in the second word the first 1 is at offset 10, so the block number is 16 × 1 + 10 = 26.

</details>

**Q18.** `Medium`  
Which free-space management technique stores the address of the first free block and the number of free contiguous blocks that follow it?

(1) Grouping  
(2) Bit vector  
(3) Linked list  
(4) Counting  

<details><summary>Answer</summary>

**(4)** — Counting works well when space is allocated and freed in contiguous runs.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: A linked-list free-space scheme needs no extra space other than a pointer to the first free block.  
Statement II: Traversing the free list to find many free blocks is efficient.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Traversing the list requires reading each block, which is slow, though it is rarely needed.

</details>

**Q20.** `Medium`  
Match List I with List II.  
List I (Consistency semantics): A. UNIX semantics  B. Session semantics  C. Immutable-shared-file semantics  
List II (Description): I. A file declared shared cannot be modified  II. Writes are visible to other users immediately  III. Writes become visible only to sessions that open the file after it is closed (as in AFS)

(1) A-II, B-III, C-I  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — Standard file-sharing consistency semantics.

</details>

**Q21.** `Medium`  
A file-system journal (log) is used to

(1) recover quickly after a crash by replaying or discarding logged metadata transactions  
(2) encrypt data  
(3) speed up random reads  
(4) compress files  

<details><summary>Answer</summary>

**(1)** — ext3, ext4 and NTFS are journaling file systems.

</details>

**Q22.** `Medium`  
The UNIX fsck utility is used for

(1) mounting remote file systems  
(2) creating backups  
(3) checking and repairing file-system consistency  
(4) formatting a disk  

<details><summary>Answer</summary>

**(3)** — It compares directory structures with the data blocks and fixes inconsistencies.

</details>

**Q23.** `Medium`  
Mounting a file system means

(1) copying it to another disk  
(2) deleting all files  
(3) attaching it to the directory tree at a specified mount point  
(4) formatting it  

<details><summary>Answer</summary>

**(3)** — The mounted file system's root then appears at the mount point.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: Advisory file locks are enforced by the operating system.  
Statement II: A shared lock lets several processes read a file concurrently, while an exclusive lock allows only one process.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Mandatory locks are enforced by the OS; advisory locks rely on cooperating processes.

</details>

**Q25.** `Medium`  
For sequential file access, which caching techniques improve performance?

(1) Free-behind and read-ahead  
(2) LRU only  
(3) Write-through only  
(4) Random replacement  

<details><summary>Answer</summary>

**(1)** — A page is freed as soon as the next one is requested, and the next pages are read in advance.

</details>

**Q26.** `Medium`  
A unified buffer cache

(1) is a separate cache for each file  
(2) caches file data and memory-mapped pages in one page cache, avoiding double caching  
(3) is used only by the kernel  
(4) is stored on disk  

<details><summary>Answer</summary>

**(2)** — Without it, data read through read() and through mmap() could be cached twice.

</details>

**Q27.** `High`  
Match List I with List II.  
List I (I/O technique): A. Polling  B. Interrupt-driven I/O  C. Direct memory access (DMA)  
List II (Description): I. The device controller notifies the CPU when it is ready  II. A controller transfers a whole block between the device and memory without involving the CPU for each byte  III. The CPU repeatedly reads the device status register (busy waiting)

(1) A-III, B-II, C-I  
(2) A-I, B-III, C-II  
(3) A-II, B-I, C-III  
(4) A-III, B-I, C-II  

<details><summary>Answer</summary>

**(4)** — Three ways to perform I/O.

</details>

**Q28.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: DMA is preferred for large data transfers.  
Reason R: During DMA the CPU must copy every byte from the device controller into memory.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — The DMA controller does the copying; the CPU is interrupted only when the whole block is done.

</details>

**Q29.** `Medium`  
When the DMA controller takes the memory bus away from the CPU for one word at a time, this is called

(1) cycle stealing  
(2) burst mode  
(3) bus mastering only  
(4) polling  

<details><summary>Answer</summary>

**(1)** — The CPU is briefly prevented from accessing main memory.

</details>

**Q30.** `Medium`  
Match List I with List II.  
List I (Kernel I/O service): A. Buffering  B. Caching  C. Spooling  D. Device reservation  
List II (Purpose): I. Gives a process exclusive access to a device  II. Holds output for a device that cannot accept interleaved data streams, such as a printer  III. Copes with speed and transfer-size mismatches between devices  IV. Keeps a copy of data in faster storage for reuse

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-IV, C-I, D-II  
(3) A-IV, B-III, C-II, D-I  
(4) A-III, B-IV, C-II, D-I  

<details><summary>Answer</summary>

**(4)** — Services of the kernel I/O subsystem.

</details>

**Q31.** `Medium`  
Double buffering is used to

(1) increase seek time  
(2) allow a producer to fill one buffer while a consumer empties the other  
(3) avoid DMA  
(4) reduce memory usage  

<details><summary>Answer</summary>

**(2)** — It decouples the producer and the consumer of the data.

</details>

**Q32.** `Medium`  
Match List I with List II.  
List I (Device type): A. Block device  B. Character device  C. Network device  
List II (Example/interface): I. Keyboard, accessed with get() and put() one character at a time  II. Disk, accessed with read(), write() and seek() on fixed-size blocks  III. Accessed through the socket interface

(1) A-I, B-II, C-III  
(2) A-II, B-III, C-I  
(3) A-II, B-I, C-III  
(4) A-III, B-I, C-II  

<details><summary>Answer</summary>

**(3)** — Common categories in the application I/O interface.

</details>

**Q33.** `Medium`  
Given below are two statements.  
Statement I: A non-blocking I/O call suspends the process until all the requested data has been transferred.  
Statement II: An asynchronous I/O call blocks the process until the transfer completes.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Both calls return immediately: non-blocking I/O with whatever data is available, asynchronous I/O with notification later.

</details>

**Q34.** `Medium`  
Vectored I/O (scatter-gather), as provided by readv() in UNIX, allows

(1) bypassing the kernel  
(2) DMA without a controller  
(3) several devices to be read at once  
(4) one system call to perform I/O involving multiple memory buffers  

<details><summary>Answer</summary>

**(4)** — It avoids several system calls and helps atomicity.

</details>

**Q35.** `Medium`  
In memory-mapped I/O

(1) only DMA is used  
(2) special I/O instructions such as IN and OUT are required  
(3) device control registers are mapped into the address space of the processor and accessed with ordinary load and store instructions  
(4) devices cannot be accessed by the kernel  

<details><summary>Answer</summary>

**(3)** — Isolated (port-mapped) I/O uses separate I/O instructions.

</details>

**Q36.** `Medium`  
The software component that hides the differences among device controllers from the kernel I/O subsystem is the

(1) scheduler  
(2) file system  
(3) device driver  
(4) interrupt vector  

<details><summary>Answer</summary>

**(3)** — Each driver presents a uniform interface for its class of devices.

</details>

**Q37.** `Medium`  
Which file attribute is used to identify a file uniquely within the file system, independent of its name?

(1) Type  
(2) Identifier (e.g. inode number)  
(3) Size  
(4) Location  

<details><summary>Answer</summary>

**(2)** — Names are for people; identifiers are for the system.

</details>

**Q38.** `Medium`  
In UNIX, a file's type can be recognised by its contents, for example by a magic number at the beginning of the file. Windows instead relies mainly on

(1) access control lists  
(2) file extensions  
(3) inode numbers  
(4) the superblock  

<details><summary>Answer</summary>

**(2)** — The extension (such as .exe or .docx) determines the associated program.

</details>

**Q39.** `Medium`  
Which of the following operations is NOT a basic file operation?

(1) Truncate  
(2) Create  
(3) Compile  
(4) Read  

<details><summary>Answer</summary>

**(3)** — Compiling is done by an application program, not by the file system.

</details>

**Q40.** `Medium`  
The per-process open-file table entry typically contains

(1) the disk block addresses  
(2) the size of the disk  
(3) the file pointer (current position) and access rights  
(4) the boot block  

<details><summary>Answer</summary>

**(3)** — The system-wide table holds the location on disk, the open count and other per-file data.

</details>

**Q41.** `Medium`  
Given below are two statements.  
Statement I: Linear-list directory implementation is simple but slow for searching.  
Statement II: Hash-table directory implementation speeds up searching but must handle collisions.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Hash tables with chaining are commonly used.

</details>

**Q42.** `Medium`  
A FAT16 file system with 2^16 clusters of 32 KB each can address a volume of at most

(1) 32 GB  
(2) 512 MB  
(3) 4 GB  
(4) 2 GB  

<details><summary>Answer</summary>

**(4)** — 2^16 × 32 KB = 2^31 bytes = 2 GB.

</details>

**Q43.** `Medium`  
Which backup strategy copies only the files changed since the last backup of any kind?

(1) Full backup  
(2) Incremental backup  
(3) Image backup  
(4) Mirror backup  

<details><summary>Answer</summary>

**(2)** — A differential backup copies all files changed since the last full backup.

</details>

**Q44.** `Medium`  
Given below are two statements.  
Statement I: In a general-graph directory structure, cycles can occur, so garbage collection may be needed to reclaim space.  
Statement II: An acyclic-graph directory structure allows a file to have more than one path name.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Links allow sharing; cycles complicate traversal and deletion.

</details>

**Q45.** `Medium`  
In the indexed allocation scheme, the linked scheme, multilevel index and combined scheme are used to

(1) improve security  
(2) eliminate the index block  
(3) handle files too large for a single index block  
(4) reduce seek time  

<details><summary>Answer</summary>

**(3)** — The UNIX inode is an example of the combined scheme.

</details>

**Q46.** `Low`  
Which file system is used by default on most modern Linux distributions?

(1) ext4  
(2) FAT32  
(3) NTFS  
(4) HFS+  

<details><summary>Answer</summary>

**(1)** — ext4 uses extents and journaling; NTFS is the Windows file system.

</details>

**Q47.** `Medium`  
In UNIX, the hard link count of a file is stored in its

(1) directory entry  
(2) data block  
(3) inode  
(4) superblock  

<details><summary>Answer</summary>

**(3)** — The file is deleted only when the link count drops to zero and no process has it open.

</details>

**Q48.** `Medium`  
The life cycle of a blocking read request ends with

(1) the process being moved from the wait queue to the ready queue after the device driver and interrupt handler complete the transfer  
(2) the file system deleting the file  
(3) the device controller calling the scheduler directly  
(4) the CPU polling the device  

<details><summary>Answer</summary>

**(1)** — The data is copied to the process's buffer and the process becomes ready.

</details>
