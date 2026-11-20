# Set 5 — Process Synchronization (critical section, Peterson's solution, semaphores, monitors, classical problems)

**45 questions** — High: 18, Medium: 26, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Which three requirements must a solution to the critical-section problem satisfy?

(1) Progress, starvation and deadlock  
(2) Mutual exclusion, hold and wait, and no preemption  
(3) Atomicity, consistency and isolation  
(4) Mutual exclusion, progress and bounded waiting  

<details><summary>Answer</summary>

**(4)** — These are the standard requirements; the solution must not assume anything about the relative speeds of processes.

</details>

**Q2.** `High`  
A counting semaphore S is initialised to 10. Then 6 wait (P) operations and 4 signal (V) operations are performed on it. The final value of S is

(1) 20  
(2) 8  
(3) 4  
(4) 0  

<details><summary>Answer</summary>

**(2)** — 10 − 6 + 4 = 8.

</details>

**Q3.** `High`  
A counting semaphore is initialised to 7. Then 20 P (wait) operations and 15 V (signal) operations are completed on it. The final value of the semaphore is

(1) 0  
(2) 12  
(3) 5  
(4) 2  

<details><summary>Answer</summary>

**(4)** — 7 − 20 + 15 = 2.

</details>

**Q4.** `High`  
In the semaphore implementation in which processes block on a waiting queue, a semaphore value of −3 means that

(1) 3 signal operations are pending  
(2) the semaphore is corrupted  
(3) 3 processes are waiting on the semaphore  
(4) 3 resources are available  

<details><summary>Answer</summary>

**(3)** — The magnitude of a negative value equals the number of processes blocked on it.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: Peterson's solution satisfies mutual exclusion, progress and bounded waiting for two processes.  
Statement II: Peterson's solution is guaranteed to work on modern architectures that reorder memory operations, without memory barriers.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Instruction reordering by compilers and processors can break it unless memory barriers are used.

</details>

**Q6.** `High`  
In Peterson's solution for two processes, the shared variables are

(1) a single integer lock  
(2) boolean flag[2] and int turn  
(3) a monitor and a condition variable  
(4) a binary semaphore and a counting semaphore  

<details><summary>Answer</summary>

**(2)** — flag[i] shows that Pi wants to enter; turn shows whose turn it is.

</details>

**Q7.** `High`  
A simple strict-alternation solution using a single shared variable turn (each process waits until turn equals its own number) violates which requirement?

(1) Bounded waiting  
(2) Progress  
(3) Atomicity  
(4) Mutual exclusion  

<details><summary>Answer</summary>

**(2)** — A process outside its critical section can block the other one from entering if it is not its turn.

</details>

**Q8.** `Medium`  
Using a single shared lock variable that is tested and then set in two separate (non-atomic) steps can violate

(1) mutual exclusion  
(2) progress  
(3) bounded waiting  
(4) portability  

<details><summary>Answer</summary>

**(1)** — Both processes can see the lock free before either sets it.

</details>

**Q9.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Disabling interrupts is not a suitable way to implement critical sections on a multiprocessor.  
Reason R: Disabling interrupts on one processor does not stop processes on other processors from accessing shared data, and it is time-consuming to send the message to all processors.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — It works only on a uniprocessor, and even there it is unwise for user programs.

</details>

**Q10.** `High`  
Match List I with List II.  
List I (Synchronization tool): A. Spinlock  B. Counting semaphore  C. Binary semaphore  D. Monitor  
List II (Description): I. Behaves like a mutex lock with values 0 and 1  II. High-level construct in which only one process is active at a time  III. Busy-waits until the lock becomes available  IV. Controls access to a resource with a finite number of instances

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-I, C-IV, D-II  
(3) A-III, B-IV, C-II, D-I  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(1)** — Standard descriptions of synchronization primitives.

</details>

**Q11.** `Medium`  
Spinlocks are most appropriate when

(1) the lock is held for a short time on a multiprocessor  
(2) the process needs to perform I/O while holding the lock  
(3) the lock is held for a long time on a uniprocessor  
(4) there is only one process  

<details><summary>Answer</summary>

**(1)** — Spinning avoids a context switch, which pays off only when the wait is short and another CPU can release the lock.

</details>

**Q12.** `Medium`  
The test_and_set() hardware instruction, used in the simple lock algorithm, guarantees mutual exclusion but does NOT satisfy

(1) mutual exclusion  
(2) bounded waiting  
(3) atomicity  
(4) progress  

<details><summary>Answer</summary>

**(2)** — A process may keep losing the race; a more complex algorithm with a waiting array is needed for bounded waiting.

</details>

**Q13.** `Medium`  
The compare_and_swap(value, expected, new_value) instruction sets value to new_value only if

(1) value is zero  
(2) the lock is held  
(3) new_value is greater than value  
(4) value equals expected  

<details><summary>Answer</summary>

**(4)** — It always returns the original value and is executed atomically.

</details>

**Q14.** `High`  
In the bounded-buffer producer-consumer problem with n buffers, the semaphores mutex, empty and full are initialised to

(1) 1, n and 0  
(2) n, 1 and 0  
(3) 0, n and 1  
(4) 1, 0 and n  

<details><summary>Answer</summary>

**(1)** — empty counts empty slots, full counts full slots and mutex protects the buffer.

</details>

**Q15.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In the producer-consumer solution, swapping the order of the two signal() operations at the end of the producer causes deadlock.  
Reason R: A producer that blocks on wait(empty) while holding mutex prevents the consumer from ever entering to free a slot.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — The order of signal operations is harmless; it is swapping wait(mutex) and wait(empty) that can deadlock, as R describes.

</details>

**Q16.** `High`  
In the first readers-writers problem (readers have priority), which process may starve?

(1) Readers  
(2) Writers  
(3) Both readers and writers  
(4) Neither  

<details><summary>Answer</summary>

**(2)** — A continuous stream of readers can keep a writer waiting forever.

</details>

**Q17.** `Medium`  
In the first readers-writers solution, the variables rw_mutex, mutex and read_count are initialised to

(1) 0, 1 and 1  
(2) 1, 1 and 1  
(3) 1, 1 and 0  
(4) 1, 0 and 0  

<details><summary>Answer</summary>

**(3)** — The first reader locks rw_mutex and the last reader releases it.

</details>

**Q18.** `High`  
In the dining-philosophers problem with five philosophers, if each philosopher picks up the left chopstick first and then the right one

(1) the problem is solved correctly  
(2) only one philosopher can eat at a time  
(3) deadlock can occur when all pick up their left chopsticks at the same time  
(4) starvation is impossible  

<details><summary>Answer</summary>

**(3)** — Each holds one chopstick and waits for another: a circular wait.

</details>

**Q19.** `High`  
Which of the following are remedies for deadlock in the dining-philosophers problem?  
A. Allow at most four philosophers at the table at the same time  B. Allow a philosopher to pick up chopsticks only if both are available  C. Odd-numbered philosophers pick up the left chopstick first and even-numbered the right one first  D. Increase the thinking time of every philosopher  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) B, C and D only  
(3) A and D only  
(4) A, B, C and D  

<details><summary>Answer</summary>

**(1)** — Changing the thinking time does not remove the possibility of circular wait.

</details>

**Q20.** `High`  
Given below are two statements.  
Statement I: Within a monitor, only one process can be active at a time.  
Statement II: If x.signal() is executed when no process is waiting on x, the signal is remembered and the next x.wait() returns immediately.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A condition-variable signal with no waiting process has no effect; unlike a semaphore, it is not remembered.

</details>

**Q21.** `Medium`  
Two processes P1 and P2 share a variable x, initially 0. P1 executes x = x + 1 and P2 executes x = x − 1, each implemented as load, modify and store, with arbitrary interleaving. The set of possible final values of x is

(1) {−1, 1}  
(2) {0}  
(3) {−2, 0, 2}  
(4) {−1, 0, 1}  

<details><summary>Answer</summary>

**(4)** — Without interleaving the result is 0; if one store overwrites the other, the result is 1 or −1.

</details>

**Q22.** `Medium`  
Two processes share a variable x, initially 5. Each executes x = x + 1 once, implemented as load, increment and store. The possible final values of x are

(1) 5, 6 or 7  
(2) 6 or 7  
(3) only 7  
(4) only 6  

<details><summary>Answer</summary>

**(2)** — A lost update gives 6; serial execution gives 7.

</details>

**Q23.** `High`  
To make sure that statement S1 in process P1 executes before statement S2 in process P2, using a semaphore synch, the initial value of synch and the code are

(1) synch = 1; P1: S1; signal(synch);  P2: wait(synch); S2;  
(2) synch = 0; P1: S1; signal(synch);  P2: wait(synch); S2;  
(3) synch = 1; P1: wait(synch); S1;  P2: signal(synch); S2;  
(4) synch = 0; P1: wait(synch); S1;  P2: S2; signal(synch);  

<details><summary>Answer</summary>

**(2)** — P2 blocks until P1 has finished S1 and signalled.

</details>

**Q24.** `Medium`  
A situation in which several processes access and manipulate the same data concurrently and the outcome depends on the order of access is called a

(1) deadlock  
(2) race condition  
(3) livelock  
(4) starvation  

<details><summary>Answer</summary>

**(2)** — Synchronization is needed to prevent race conditions.

</details>

**Q25.** `Medium`  
Given below are two statements.  
Statement I: A binary semaphore can be used as a mutex lock.  
Statement II: A counting semaphore can be implemented using binary semaphores.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are standard results.

</details>

**Q26.** `Medium`  
In the monitor signalling discipline "signal and wait"

(1) the signal is ignored  
(2) the signalling process waits until the signalled process leaves the monitor or waits on another condition  
(3) both processes continue together  
(4) the signalling process continues and the signalled process waits  

<details><summary>Answer</summary>

**(2)** — In "signal and continue" the signalling process continues instead.

</details>

**Q27.** `Medium`  
Which classical synchronization problem models a shop where a single worker sleeps when there are no customers and customers leave if all waiting chairs are full?

(1) Cigarette smokers  
(2) Sleeping barber  
(3) Readers-writers  
(4) Dining philosophers  

<details><summary>Answer</summary>

**(2)** — The sleeping barber problem uses semaphores for customers, the barber and a mutex.

</details>

**Q28.** `Medium`  
Which of the following is a liveness failure?  
A. Deadlock  B. Starvation  C. Priority inversion  
Choose the correct answer from the options given below:

(1) B and C only  
(2) A, B and C  
(3) A only  
(4) A and B only  

<details><summary>Answer</summary>

**(2)** — Each of them can prevent a process from making progress.

</details>

**Q29.** `Medium`  
A semaphore S used for mutual exclusion should be initialised to

(1) the number of processes  
(2) −1  
(3) 0  
(4) 1  

<details><summary>Answer</summary>

**(4)** — One process can enter; the next one blocks until the first signals.

</details>

**Q30.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: wait() and signal() operations on a semaphore must be executed atomically.  
Reason R: If two processes modify the semaphore value at the same time, the update may be lost.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The semaphore operations are themselves critical sections.

</details>

**Q31.** `Medium`  
Busy waiting wastes CPU cycles because

(1) the process loops continuously checking a condition  
(2) the process is blocked  
(3) the process is swapped out  
(4) the process makes a system call  

<details><summary>Answer</summary>

**(1)** — A spinning process uses the CPU without doing useful work.

</details>

**Q32.** `Medium`  
Which of the following hardware features is used to guarantee that changes made by one processor become visible to other processors before later operations?

(1) Translation lookaside buffer  
(2) Memory barrier (fence)  
(3) Base register  
(4) Interrupt vector  

<details><summary>Answer</summary>

**(2)** — Memory barriers prevent reordering across the barrier.

</details>

**Q33.** `Medium`  
A semaphore whose value can range over an unrestricted domain is called a

(1) spinlock  
(2) binary semaphore  
(3) mutex  
(4) counting semaphore  

<details><summary>Answer</summary>

**(4)** — Binary semaphores take only the values 0 and 1.

</details>

**Q34.** `Medium`  
Three processes each need the shared resource R, which has two instances, protected by a counting semaphore. The semaphore should be initialised to

(1) 1  
(2) 3  
(3) 0  
(4) 2  

<details><summary>Answer</summary>

**(4)** — The initial value equals the number of available instances.

</details>

**Q35.** `Medium`  
Given below are two statements.  
Statement I: A deadlock-free solution can still lead to starvation.  
Statement II: A deadlock-free solution is necessarily starvation-free.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Deadlock-freedom guarantees that someone progresses, not that every process does.

</details>

**Q36.** `Medium`  
Which of the following is NOT a classical problem of synchronization?

(1) Travelling salesman problem  
(2) Dining-philosophers problem  
(3) Bounded-buffer problem  
(4) Readers-writers problem  

<details><summary>Answer</summary>

**(1)** — The travelling salesman problem is an optimisation problem.

</details>

**Q37.** `Medium`  
Lock-free algorithms based on compare-and-swap avoid

(1) shared memory  
(2) all forms of contention  
(3) the need for atomic instructions  
(4) the use of locks, so a thread cannot block other threads by holding a lock  

<details><summary>Answer</summary>

**(4)** — They rely on atomic CAS retries instead of locks.

</details>

**Q38.** `Medium`  
The wait() and signal() semaphore operations were originally called P and V by

(1) Dijkstra  
(2) Peterson  
(3) Lamport  
(4) Hoare  

<details><summary>Answer</summary>

**(1)** — P and V come from the Dutch words proberen (to test) and verhogen (to increment).

</details>

**Q39.** `Medium`  
Monitors were proposed as a synchronization construct by

(1) Lamport and Bakery  
(2) Coffman and Denning  
(3) Hoare and Brinch Hansen  
(4) Dijkstra and Peterson  

<details><summary>Answer</summary>

**(3)** — Hoare and Brinch Hansen developed the monitor concept in the 1970s.

</details>

**Q40.** `Medium`  
Lamport's bakery algorithm solves the critical-section problem for

(1) n processes using a numbered ticket for each  
(2) only reader processes  
(3) exactly two processes  
(4) only multiprocessor systems with hardware support  

<details><summary>Answer</summary>

**(1)** — Each process takes a number; the smallest number (ties broken by process ID) enters first.

</details>

**Q41.** `High`  
Given below are two statements.  
Statement I: A mutex lock must be released only by the thread that acquired it.  
Statement II: A semaphore can be signalled by a thread other than the one that performed wait on it.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This is why semaphores can be used for ordering (signalling) between threads.

</details>

**Q42.** `Medium`  
In a producer-consumer solution with 1 producer, 1 consumer and a buffer of 5 slots, the producer has inserted 7 items and the consumer has removed 4. The current values of the semaphores full and empty are

(1) 4 and 1  
(2) 3 and 2  
(3) 7 and 4  
(4) 2 and 3  

<details><summary>Answer</summary>

**(2)** — There are 7 − 4 = 3 items in the buffer, so full = 3 and empty = 5 − 3 = 2.

</details>

**Q43.** `Low`  
The cigarette smokers problem was proposed by

(1) Hoare  
(2) Knuth  
(3) Dijkstra  
(4) Patil  

<details><summary>Answer</summary>

**(4)** — Suhas Patil posed it to show the limits of semaphores without conditional constructs.

</details>

**Q44.** `Medium`  
Which of the following conditions can make a solution that satisfies mutual exclusion still be unacceptable?

(1) It does not depend on CPU speed  
(2) It forces processes to enter strictly alternately even when one does not want to enter  
(3) It guarantees bounded waiting  
(4) It guarantees progress  

<details><summary>Answer</summary>

**(2)** — Strict alternation violates the progress requirement.

</details>

**Q45.** `Medium`  
A condition variable in a monitor is used with the operations

(1) lock and unlock  
(2) P and V  
(3) wait and signal  
(4) send and receive  

<details><summary>Answer</summary>

**(3)** — x.wait() suspends the caller until another process calls x.signal().

</details>
