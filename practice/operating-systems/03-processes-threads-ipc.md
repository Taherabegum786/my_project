# Set 3 — Processes, Threads and Interprocess Communication

**51 questions** — High: 19, Medium: 31, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
How many times is "hello" printed by the following C code?  
fork(); fork(); printf("hello");

(1) 4  
(2) 8  
(3) 3  
(4) 2  

<details><summary>Answer</summary>

**(1)** — Each fork doubles the number of processes: 2 × 2 = 4 processes, each prints once.

</details>

**Q2.** `High`  
A process executes the code for (i = 0; i < 3; i++) fork(); The total number of processes at the end, including the original, is

(1) 7  
(2) 8  
(3) 6  
(4) 3  

<details><summary>Answer</summary>

**(2)** — n forks in sequence give 2^n = 8 processes, i.e. 7 child processes.

</details>

**Q3.** `High`  
A program executes for (i = 0; i < n; i++) fork(); The number of child processes created is

(1) n  
(2) 2n  
(3) 2^n  
(4) 2^n − 1  

<details><summary>Answer</summary>

**(4)** — There are 2^n processes in total, one of which is the original parent.

</details>

**Q4.** `High`  
How many processes in total (including the original) exist after the following statement executes?  
fork() && fork() || fork();

(1) 8  
(2) 3  
(3) 4  
(4) 5  

<details><summary>Answer</summary>

**(4)** — The parent's first two forks succeed and short-circuit the OR; the two children that get 0 each execute the third fork: 1 + 4 = 5.

</details>

**Q5.** `High`  
How many processes in total exist after executing the following code?  
if (fork() == 0) fork();

(1) 4  
(2) 2  
(3) 3  
(4) 6  

<details><summary>Answer</summary>

**(3)** — Only the child of the first fork executes the second fork, giving parent, child and grandchild.

</details>

**Q6.** `High`  
The value returned by fork() to the child process and to the parent process is respectively

(1) 0 and 0  
(2) the PID of the child and 0  
(3) 0 and the PID of the child  
(4) −1 and the PID of the parent  

<details><summary>Answer</summary>

**(3)** — fork returns −1 to the parent if creation fails.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Process state transition): A. Running to Ready  B. Running to Waiting  C. Waiting to Ready  D. Ready to Running  
List II (Cause): I. The process issues an I/O request  II. Dispatch by the CPU scheduler  III. Interrupt, e.g. time quantum expiry  IV. Completion of the I/O operation

(1) A-II, B-I, C-IV, D-III  
(2) A-I, B-III, C-IV, D-II  
(3) A-III, B-IV, C-I, D-II  
(4) A-III, B-I, C-IV, D-II  

<details><summary>Answer</summary>

**(4)** — Standard five-state process model transitions.

</details>

**Q8.** `High`  
Which of the following process state transitions is NOT possible in the five-state model?

(1) Running to Ready  
(2) Ready to Running  
(3) Running to Waiting  
(4) Waiting to Running  

<details><summary>Answer</summary>

**(4)** — A process whose I/O completes must first become Ready; only the dispatcher moves a process to Running.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Scheduler): A. Long-term scheduler  B. Short-term scheduler  C. Medium-term scheduler  
List II (Function): I. Selects which ready process gets the CPU next  II. Swaps processes out of and into memory  III. Controls the degree of multiprogramming by admitting jobs

(1) A-III, B-I, C-II  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — The long-term scheduler admits jobs, the CPU scheduler dispatches, the medium-term scheduler swaps.

</details>

**Q10.** `Medium`  
The degree of multiprogramming is controlled by the

(1) dispatcher  
(2) short-term scheduler  
(3) medium-term scheduler only  
(4) long-term scheduler  

<details><summary>Answer</summary>

**(4)** — The long-term (job) scheduler decides how many processes are in memory.

</details>

**Q11.** `High`  
Which of the following is NOT stored in the process control block (PCB)?

(1) Program counter  
(2) Source code of the program  
(3) Process state  
(4) CPU register contents  

<details><summary>Answer</summary>

**(2)** — The PCB holds state, PC, registers, scheduling, memory-management, accounting and I/O status information.

</details>

**Q12.** `Medium`  
A process that has terminated but whose parent has not yet called wait() is called a

(1) orphan process  
(2) daemon process  
(3) blocked process  
(4) zombie process  

<details><summary>Answer</summary>

**(4)** — Its entry remains in the process table until the parent collects its exit status.

</details>

**Q13.** `Medium`  
A process whose parent has terminated without waiting for it is called an orphan process. In Linux it is adopted by

(1) init or systemd (PID 1)  
(2) its grandparent  
(3) no process  
(4) the swapper process  

<details><summary>Answer</summary>

**(1)** — init/systemd periodically calls wait() to release orphans.

</details>

**Q14.** `Medium`  
The exec() family of system calls

(1) creates a new child process  
(2) waits for a child to terminate  
(3) replaces the memory image of the calling process with a new program  
(4) duplicates file descriptors  

<details><summary>Answer</summary>

**(3)** — After a successful exec the original program no longer exists in that process.

</details>

**Q15.** `Medium`  
The layout of a process in memory, from low to high addresses, is usually

(1) stack, heap, data, text  
(2) data, text, stack, heap  
(3) heap, stack, text, data  
(4) text, data, heap, stack  

<details><summary>Answer</summary>

**(4)** — The heap grows upward and the stack grows downward toward each other.

</details>

**Q16.** `Medium`  
The time taken by the dispatcher to stop one process and start another is called

(1) turnaround time  
(2) response time  
(3) burst time  
(4) dispatch latency  

<details><summary>Answer</summary>

**(4)** — Dispatch latency includes the context switch and the switch to user mode.

</details>

**Q17.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Context-switch time is pure overhead.  
Reason R: The hardware saves and restores all process state automatically, without any work by the operating system.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — The kernel itself saves the context in the PCB and restores the next one; this work does nothing for any user process.

</details>

**Q18.** `High`  
Which of the following are shared by all the threads of a process?  
A. Code section  B. Data section  C. Stack  D. Open files  E. Program counter  
Choose the correct answer from the options given below:

(1) C and E only  
(2) A, B and D only  
(3) A, B and C only  
(4) A, B, C, D and E  

<details><summary>Answer</summary>

**(2)** — Each thread has its own stack, register set and program counter.

</details>

**Q19.** `High`  
Match List I with List II.  
List I (Multithreading model): A. Many-to-one  B. One-to-one  C. Many-to-many  
List II (Property): I. Each user thread maps to its own kernel thread; used by Linux and Windows  II. Many user threads are multiplexed over an equal or smaller number of kernel threads  III. A blocking system call blocks the whole process and threads cannot run in parallel on multiple processors

(1) A-I, B-III, C-II  
(2) A-II, B-I, C-III  
(3) A-III, B-I, C-II  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(3)** — Standard properties of the three threading models.

</details>

**Q20.** `High`  
Given below are two statements.  
Statement I: User-level threads can be created and switched faster than kernel-level threads.  
Statement II: In the many-to-one model, threads of the same process can run in parallel on different processors.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Only one thread at a time can access the kernel in the many-to-one model, so the threads cannot run in parallel.

</details>

**Q21.** `High`  
According to Amdahl's law, an application that is 75% parallel and 25% serial, run on 4 processing cores, has a maximum speedup of approximately

(1) 4  
(2) 2.28  
(3) 1.6  
(4) 3  

<details><summary>Answer</summary>

**(2)** — Speedup ≤ 1 / (0.25 + 0.75 / 4) = 1 / 0.4375 ≈ 2.28.

</details>

**Q22.** `High`  
According to Amdahl's law, if 25% of a program is serial, the maximum speedup obtainable with an unlimited number of processors is

(1) 2  
(2) unlimited  
(3) 4  
(4) 25  

<details><summary>Answer</summary>

**(3)** — As N tends to infinity the speedup approaches 1/S = 1/0.25 = 4.

</details>

**Q23.** `Medium`  
Given below are two statements.  
Statement I: Concurrency is possible on a single-core system by interleaving the execution of threads.  
Statement II: Parallelism requires more than one processing core.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Concurrency means making progress on several tasks; parallelism means running them at the same instant.

</details>

**Q24.** `Medium`  
Distributing subsets of the same data across cores and performing the same operation on each is called

(1) multiprogramming  
(2) data parallelism  
(3) pipelining  
(4) task parallelism  

<details><summary>Answer</summary>

**(2)** — Task parallelism instead distributes different operations.

</details>

**Q25.** `Medium`  
Match List I with List II.  
List I (Implicit threading approach): A. Thread pool  B. OpenMP  C. Fork-join  D. Grand Central Dispatch  
List II (Description): I. Compiler directives such as #pragma omp parallel  II. Apple's dispatch queues of blocks  III. A set of pre-created threads waiting for work  IV. A parent task splits work into subtasks and waits for them to finish

(1) A-I, B-III, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-IV, B-I, C-III, D-II  

<details><summary>Answer</summary>

**(3)** — Common implicit threading techniques.

</details>

**Q26.** `Medium`  
Given below are two statements.  
Statement I: Pthreads is a thread library implementation available only on Linux.  
Statement II: pthread_join() makes the calling thread wait for the specified thread to terminate.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Pthreads is a POSIX specification, implemented on Linux, macOS, Solaris and other UNIX-like systems.

</details>

**Q27.** `Medium`  
In deferred thread cancellation

(1) the target thread periodically checks whether it should terminate, at cancellation points  
(2) the target thread is terminated immediately  
(3) the whole process is terminated  
(4) the thread cannot be cancelled  

<details><summary>Answer</summary>

**(1)** — Deferred cancellation is the Pthreads default and lets the thread release resources safely.

</details>

**Q28.** `Medium`  
Which IPC mechanism is generally faster once established?

(1) Message passing  
(2) Pipes  
(3) Shared memory  
(4) Sockets  

<details><summary>Answer</summary>

**(3)** — After the region is set up, accesses need no kernel intervention; message passing needs a system call per message.

</details>

**Q29.** `High`  
Given below are two statements.  
Statement I: Message passing is easier to implement than shared memory in a distributed system.  
Statement II: Message passing is useful for exchanging smaller amounts of data because no conflicts need be avoided.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard comparisons of the two IPC models.

</details>

**Q30.** `High`  
In the bounded-buffer producer-consumer solution using a circular array of size n with in and out pointers (and no count variable), the buffer is full when

(1) in == out  
(2) (in + 1) % n == out  
(3) in == n  
(4) (out + 1) % n == in  

<details><summary>Answer</summary>

**(2)** — This scheme can hold at most n − 1 items, because in == out is used to mean "empty".

</details>

**Q31.** `Medium`  
When both send() and receive() are blocking, the arrangement is called a

(1) pipe  
(2) rendezvous  
(3) mailbox  
(4) signal  

<details><summary>Answer</summary>

**(2)** — Sender and receiver meet at the point of message transfer.

</details>

**Q32.** `Medium`  
Match List I with List II.  
List I (Buffering capacity of a message queue): A. Zero capacity  B. Bounded capacity  C. Unbounded capacity  
List II (Behaviour of the sender): I. Never blocks  II. Must block until the receiver receives the message  III. Blocks only when the queue is full

(1) A-III, B-II, C-I  
(2) A-II, B-III, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(2)** — Zero-capacity links need a rendezvous; unbounded queues never block the sender.

</details>

**Q33.** `Medium`  
In indirect communication, messages are sent to and received from

(1) stacks  
(2) process identifiers  
(3) mailboxes (ports)  
(4) registers  

<details><summary>Answer</summary>

**(3)** — In direct communication, processes name each other explicitly.

</details>

**Q34.** `High`  
Given below are two statements.  
Statement I: An ordinary (anonymous) pipe in UNIX is unidirectional and requires a parent-child relationship between the communicating processes.  
Statement II: A named pipe (FIFO) can be used only between a parent and its child process.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Named pipes appear in the file system and can be used by unrelated processes.

</details>

**Q35.** `Medium`  
After the call pipe(fd) in UNIX

(1) fd[0] is the read end and fd[1] is the write end  
(2) both ends can be used for reading and writing  
(3) fd[0] is the write end and fd[1] is the read end  
(4) fd[0] and fd[1] are the same descriptor  

<details><summary>Answer</summary>

**(1)** — Data written to fd[1] is read from fd[0].

</details>

**Q36.** `Medium`  
In a remote procedure call (RPC), packaging the parameters into a form that can be transmitted over the network is called

(1) polling  
(2) binding  
(3) stubbing  
(4) marshalling  

<details><summary>Answer</summary>

**(4)** — The client stub marshals the parameters; XDR is a machine-independent representation.

</details>

**Q37.** `Medium`  
Which of the following signals cannot be caught or ignored by a UNIX process?

(1) SIGTERM  
(2) SIGINT  
(3) SIGALRM  
(4) SIGKILL  

<details><summary>Answer</summary>

**(4)** — SIGKILL (and SIGSTOP) always take effect.

</details>

**Q38.** `Medium`  
A socket is identified by

(1) a process ID and a port  
(2) a file descriptor only  
(3) an IP address concatenated with a port number  
(4) a MAC address  

<details><summary>Answer</summary>

**(3)** — A connection is identified by the pair of sockets at its two ends.

</details>

**Q39.** `Medium`  
Thread-local storage (TLS) is

(1) storage for thread IDs only  
(2) data that each thread keeps its own copy of  
(3) data shared by all threads of a process  
(4) the stack of the kernel  

<details><summary>Answer</summary>

**(2)** — TLS persists across function calls, unlike local variables, but is private to a thread.

</details>

**Q40.** `Medium`  
In the scheduler activation scheme, the kernel informs the user-level thread library about events such as a thread about to block by means of

(1) an upcall  
(2) a system call  
(3) a page fault  
(4) a signal to every thread  

<details><summary>Answer</summary>

**(1)** — Upcalls are handled by the thread library's upcall handler on a lightweight process.

</details>

**Q41.** `Medium`  
Which of the following benefits of multithreading is illustrated by a web browser that remains interactive while an image is loading?

(1) Responsiveness  
(2) Resource sharing  
(3) Economy  
(4) Scalability  

<details><summary>Answer</summary>

**(1)** — Another thread continues to respond to the user.

</details>

**Q42.** `Medium`  
Creating a thread is cheaper than creating a process because

(1) threads do not need a stack  
(2) threads share the address space and resources of the process  
(3) threads cannot do I/O  
(4) threads do not run on the CPU  

<details><summary>Answer</summary>

**(2)** — There is no need to allocate a new address space or duplicate resources.

</details>

**Q43.** `Medium`  
Arrange the following in the order in which they occur when a process is created in UNIX and runs a new program.  
A. The child calls exec()  B. The parent calls fork()  C. The parent's wait() returns the child's exit status  D. The child calls exit()

(1) A, B, C, D  
(2) B, C, A, D  
(3) B, A, D, C  
(4) B, A, C, D  

<details><summary>Answer</summary>

**(3)** — The parent forks, the child execs and finally exits, and only then can the parent's wait() return with the exit status.

</details>

**Q44.** `Medium`  
The medium-term scheduler is used mainly to

(1) select the next process to run  
(2) select jobs from the job pool  
(3) handle interrupts  
(4) remove processes from memory to reduce the degree of multiprogramming  

<details><summary>Answer</summary>

**(4)** — Swapping out partially executed processes improves the process mix or frees memory.

</details>

**Q45.** `Medium`  
A process is said to be I/O-bound if it

(1) never performs I/O  
(2) spends more time doing computation than I/O  
(3) is always in the ready queue  
(4) spends more time doing I/O than computation  

<details><summary>Answer</summary>

**(4)** — The long-term scheduler should admit a good mix of I/O-bound and CPU-bound processes.

</details>

**Q46.** `Medium`  
When a process terminates, causing all its children to be terminated as well, this is called

(1) orphaning  
(2) cascading termination  
(3) process aging  
(4) deferred cancellation  

<details><summary>Answer</summary>

**(2)** — Some systems do not allow a child to exist if its parent has terminated.

</details>

**Q47.** `Medium`  
Which Linux system call creates a new task and, through flags such as CLONE_VM and CLONE_FILES, decides how much is shared with the parent?

(1) clone()  
(2) exec()  
(3) spawn()  
(4) fork()  

<details><summary>Answer</summary>

**(1)** — Linux does not distinguish processes from threads; clone() with sharing flags creates threads.

</details>

**Q48.** `Medium`  
Which of the following is a lightweight process?

(1) An orphan  
(2) A zombie  
(3) A thread  
(4) A daemon  

<details><summary>Answer</summary>

**(3)** — A thread is often called a lightweight process.

</details>

**Q49.** `Low`  
A process running in the background that provides a service and is not attached to a terminal is called a

(1) shell  
(2) orphan  
(3) zombie  
(4) daemon  

<details><summary>Answer</summary>

**(4)** — Examples are sshd, cron and httpd.

</details>

**Q50.** `Medium`  
How many processes in total exist after the following code runs?  
if (fork()) fork(); fork();

(1) 6  
(2) 4  
(3) 8  
(4) 5  

<details><summary>Answer</summary>

**(1)** — The parent creates two children before the last fork (3 processes); each of them forks once more: 3 × 2 = 6.

</details>

**Q51.** `Medium`  
How many processes in total, including the parent, are created by the following code?  
for (i = 0; i < 4; i++) if (fork() == 0) break;

(1) 4  
(2) 5  
(3) 16  
(4) 8  

<details><summary>Answer</summary>

**(2)** — Each child breaks out of the loop immediately, so only the parent forks four times: 1 + 4 = 5.

</details>
