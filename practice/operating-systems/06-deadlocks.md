# Set 6 — Deadlocks (characterization, resource-allocation graphs, prevention, avoidance and Banker's algorithm, detection, recovery)

**38 questions** — High: 17, Medium: 21, Low: 0

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Which of the following conditions must hold simultaneously for a deadlock to occur?  
A. Mutual exclusion  B. Hold and wait  C. No preemption  D. Circular wait  E. Starvation  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) B, C, D and E only  
(3) A, B, C and D only  
(4) A, B, C, D and E  

<details><summary>Answer</summary>

**(3)** — These are the four Coffman conditions; starvation is not one of them.

</details>

**Q2.** `High`  
A system has 3 processes sharing 4 instances of a resource type. Each process needs at most 2 instances. Which of the following is true?

(1) The system is deadlock-free  
(2) At most one process can run  
(3) Deadlock can occur  
(4) Deadlock occurs always  

<details><summary>Answer</summary>

**(1)** — Deadlock-free if R ≥ n(k − 1) + 1 = 3 × 1 + 1 = 4; with 4 instances some process can always finish.

</details>

**Q3.** `High`  
A system has 6 processes, each of which may need up to 3 tape drives. The minimum number of tape drives that guarantees freedom from deadlock is

(1) 18  
(2) 12  
(3) 13  
(4) 19  

<details><summary>Answer</summary>

**(3)** — n(k − 1) + 1 = 6 × 2 + 1 = 13.

</details>

**Q4.** `High`  
A system has 6 identical resources and n processes competing for them. Each process can request at most 2 resources. The maximum value of n for which the system is guaranteed to be deadlock-free is

(1) 3  
(2) 4  
(3) 5  
(4) 6  

<details><summary>Answer</summary>

**(3)** — n(2 − 1) + 1 ≤ 6 gives n ≤ 5.

</details>

**Q5.** `High`  
Five processes need at most 2, 3, 4, 5 and 6 instances of a resource respectively. The minimum number of instances that guarantees no deadlock is

(1) 16  
(2) 21  
(3) 15  
(4) 20  

<details><summary>Answer</summary>

**(1)** — Σ(max − 1) + 1 = (1 + 2 + 3 + 4 + 5) + 1 = 16.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: If a resource-allocation graph contains no cycle, there is no deadlock.  
Statement II: If a resource-allocation graph contains a cycle and every resource type has several instances, a deadlock must exist.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — With several instances per type, a cycle is necessary but not sufficient for deadlock.

</details>

**Q7.** `High`  
If every resource type has exactly one instance, a cycle in the resource-allocation graph is

(1) both necessary and sufficient for deadlock  
(2) neither necessary nor sufficient  
(3) necessary but not sufficient for deadlock  
(4) sufficient but not necessary  

<details><summary>Answer</summary>

**(1)** — With single instances, a cycle implies a deadlock.

</details>

**Q8.** `Medium`  
In a resource-allocation graph, an edge from a process Pi to a resource type Rj is called a

(1) claim edge  
(2) assignment edge  
(3) wait-for edge  
(4) request edge  

<details><summary>Answer</summary>

**(4)** — An edge from Rj to Pi is an assignment edge; claim edges (dashed) are used in avoidance.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Deadlock prevention): A. Deny mutual exclusion  B. Deny hold and wait  C. Deny no preemption  D. Deny circular wait  
List II (Technique): I. Impose a total ordering on resource types and request them in increasing order  II. Request all resources before starting execution  III. Take resources away from a process that waits for another resource  IV. Make resources shareable, e.g. by spooling a printer

(1) A-IV, B-II, C-III, D-I  
(2) A-IV, B-III, C-II, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-IV, B-II, C-I, D-III  

<details><summary>Answer</summary>

**(1)** — Each prevention method breaks one of the four conditions.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Requesting all resources before execution prevents deadlock but can cause low resource utilisation and starvation.  
Reason R: Resources may be allocated long before they are used, and a process needing many popular resources may wait indefinitely.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — These are the two drawbacks of denying hold and wait.

</details>

**Q11.** `High`  
Which of the following statements about safe and unsafe states is correct?

(1) An unsafe state is always a deadlocked state  
(2) A safe state can never lead to deadlock if the OS follows the avoidance algorithm, while an unsafe state may lead to deadlock  
(3) A deadlocked state is a safe state  
(4) Safe and unsafe states are the same  

<details><summary>Answer</summary>

**(2)** — Deadlocked states are a subset of unsafe states.

</details>

**Q12.** `High`  
In the Banker's algorithm, the Need matrix is calculated as

(1) Max − Allocation  
(2) Allocation − Max  
(3) Available − Allocation  
(4) Max + Allocation  

<details><summary>Answer</summary>

**(1)** — Need[i][j] is how many more instances of Rj process Pi may still request.

</details>

**Q13.** `High`  
Five processes P0 to P4 share resources A, B and C (10, 5 and 7 instances). Allocation: P0 (0,1,0), P1 (2,0,0), P2 (3,0,2), P3 (2,1,1), P4 (0,0,2). Max: P0 (7,5,3), P1 (3,2,2), P2 (9,0,2), P3 (2,2,2), P4 (4,3,3). Available is (3,3,2). The Need of P4 is

(1) (0,0,2)  
(2) (4,2,1)  
(3) (4,3,1)  
(4) (4,3,3)  

<details><summary>Answer</summary>

**(3)** — Need = Max − Allocation = (4,3,3) − (0,0,2) = (4,3,1).

</details>

**Q14.** `High`  
For the system with Allocation P0 (0,1,0), P1 (2,0,0), P2 (3,0,2), P3 (2,1,1), P4 (0,0,2), Max P0 (7,5,3), P1 (3,2,2), P2 (9,0,2), P3 (2,2,2), P4 (4,3,3) and Available (3,3,2), which of the following is a safe sequence?

(1) P4, P1, P3, P0, P2  
(2) P0, P1, P2, P3, P4  
(3) P1, P3, P4, P2, P0  
(4) P2, P1, P3, P4, P0  

<details><summary>Answer</summary>

**(3)** — Needs are P0 (7,4,3), P1 (1,2,2), P2 (6,0,0), P3 (0,1,1), P4 (4,3,1). Only P1 or P3 can go first; P1, P3, P4, P2, P0 succeeds.

</details>

**Q15.** `Medium`  
In the same Banker's example (Available (3,3,2); after granting P1's request for (1,0,2) the state is still safe), if P0 then requests (0,2,0), the request

(1) causes immediate deadlock  
(2) is rejected because it exceeds P0's maximum claim  
(3) must wait because the resulting state would be unsafe  
(4) is granted because resources are available and the state remains safe  

<details><summary>Answer</summary>

**(3)** — Available would become (2,1,0), which is not enough for any process's remaining need, so the state would be unsafe.

</details>

**Q16.** `High`  
A system has 12 instances of one resource type. P0 has a maximum need of 10 and holds 5, P1 a maximum of 4 and holds 2, P2 a maximum of 9 and holds 2. Which statement is correct?

(1) The state is safe with the safe sequence P0, P1, P2  
(2) The system is deadlocked  
(3) The state is safe with the safe sequence P1, P0, P2  
(4) The state is unsafe  

<details><summary>Answer</summary>

**(3)** — 3 are free; P1 can finish (5 free), then P0 (10 free), then P2.

</details>

**Q17.** `Medium`  
In the system with 12 instances where P0 (max 10, holds 5), P1 (max 4, holds 2) and P2 (max 9, holds 2), if P2 is given one more instance

(1) the state becomes unsafe  
(2) the state remains safe  
(3) P0 can finish first  
(4) the system immediately deadlocks  

<details><summary>Answer</summary>

**(1)** — Only 2 would remain free: P1 can finish (4 free), but then neither P0 (needs 5) nor P2 (needs 6) can be guaranteed.

</details>

**Q18.** `High`  
The time complexity of the safety algorithm of the Banker's algorithm for n processes and m resource types is

(1) O(m × n)  
(2) O(n³)  
(3) O(m² × n)  
(4) O(m × n²)  

<details><summary>Answer</summary>

**(4)** — In the worst case each of n passes scans n processes and compares m resources.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: The Banker's algorithm requires each process to declare in advance the maximum number of instances of each resource type it may need.  
Statement II: The Banker's algorithm can be applied only to resource types with a single instance.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The Banker's algorithm handles multiple instances; the resource-allocation-graph algorithm is the one limited to single instances.

</details>

**Q20.** `Medium`  
For deadlock detection when every resource type has a single instance, the OS maintains a

(1) wait-for graph  
(2) safe sequence table  
(3) resource-allocation graph with claim edges  
(4) Need matrix  

<details><summary>Answer</summary>

**(1)** — A wait-for graph is obtained by collapsing the resource nodes; a cycle means deadlock.

</details>

**Q21.** `Medium`  
Detecting a cycle in a wait-for graph of n vertices requires

(1) O(n²) operations  
(2) O(n³) operations  
(3) O(n) operations  
(4) O(log n) operations  

<details><summary>Answer</summary>

**(1)** — Cycle detection in a graph with up to n² edges takes O(n²).

</details>

**Q22.** `High`  
Match List I with List II.  
List I (Strategy): A. Deadlock prevention  B. Deadlock avoidance  C. Deadlock detection  D. Ignoring the problem  
List II (Method): I. Ostrich algorithm used by most general-purpose OSes  II. Banker's algorithm  III. Ensure at least one necessary condition cannot hold  IV. Allow deadlocks, then find and recover from them

(1) A-III, B-IV, C-II, D-I  
(2) A-II, B-III, C-IV, D-I  
(3) A-III, B-II, C-I, D-IV  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(4)** — The four approaches to handling deadlocks.

</details>

**Q23.** `Medium`  
Which of the following are issues that must be addressed when recovering from deadlock by resource preemption?  
A. Selecting a victim  B. Rollback  C. Starvation  D. Increasing the number of resource types  
Choose the correct answer from the options given below:

(1) A, B, C and D  
(2) A, B and C only  
(3) A and B only  
(4) B and D only  

<details><summary>Answer</summary>

**(2)** — The same victim must not always be picked, or it will starve.

</details>

**Q24.** `Medium`  
Aborting all deadlocked processes to recover from deadlock

(1) is cheap because no computation is lost  
(2) requires the Banker's algorithm  
(3) breaks the deadlock with certainty but at great expense  
(4) never breaks the deadlock  

<details><summary>Answer</summary>

**(3)** — Aborting one process at a time is cheaper per abort but requires repeated detection.

</details>

**Q25.** `Medium`  
A situation in which two processes keep changing their state in response to each other without making progress is called

(1) livelock  
(2) deadlock  
(3) starvation  
(4) thrashing  

<details><summary>Answer</summary>

**(1)** — In a livelock the processes are not blocked, but they still make no progress.

</details>

**Q26.** `Medium`  
Ordering resource types R1 &lt; R2 &lt; R3 and requiring every process to request resources in increasing order prevents deadlock because

(1) mutual exclusion is removed  
(2) preemption is allowed  
(3) processes never hold resources  
(4) a circular wait becomes impossible  

<details><summary>Answer</summary>

**(4)** — A cycle would require some process to request a lower-numbered resource while holding a higher one.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: Mutual exclusion cannot be denied for intrinsically non-shareable resources such as a mutex lock.  
Statement II: Read-only files are shareable resources and are not involved in deadlocks.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Shareable resources do not require mutually exclusive access.

</details>

**Q28.** `Medium`  
The wait-die and wound-wait schemes prevent deadlock using

(1) timestamps of processes or transactions  
(2) the Banker's algorithm  
(3) resource ordering  
(4) wait-for graphs  

<details><summary>Answer</summary>

**(1)** — In wait-die an older process waits and a younger one dies; in wound-wait an older process preempts a younger one.

</details>

**Q29.** `Medium`  
In the wait-die scheme, if an older process requests a resource held by a younger process, the older process

(1) is terminated  
(2) waits  
(3) is rolled back  
(4) preempts the resource  

<details><summary>Answer</summary>

**(2)** — Older processes may wait for younger ones; younger processes requesting resources held by older ones are rolled back (die).

</details>

**Q30.** `Medium`  
In the wound-wait scheme, if an older process requests a resource held by a younger process

(1) the younger process is rolled back (wounded)  
(2) the request is ignored  
(3) the older process waits  
(4) both processes are rolled back  

<details><summary>Answer</summary>

**(1)** — A younger process requesting a resource held by an older one waits.

</details>

**Q31.** `High`  
A system with Available = (1, 0, 0) for resource types A, B and C has three processes. Allocation: P0 (0,1,0), P1 (2,0,0), P2 (3,0,3). Request: P0 (0,0,0), P1 (2,0,2), P2 (0,0,0). Using the deadlock-detection algorithm, which statement is correct?

(1) P0 and P1 are deadlocked  
(2) The system is deadlocked  
(3) The system is not deadlocked; the sequence P0, P2, P1 completes  
(4) Only P1 is deadlocked  

<details><summary>Answer</summary>

**(3)** — P0 finishes: work (1,1,0); P2 finishes: (4,1,3); P1's request (2,0,2) can then be met.

</details>

**Q32.** `Medium`  
Deadlock avoidance is generally less restrictive than deadlock prevention because

(1) it never refuses a request  
(2) it allows circular waits that already exist  
(3) it denies a request only if granting it could lead to an unsafe state, rather than ruling out a necessary condition altogether  
(4) it does not need any information in advance  

<details><summary>Answer</summary>

**(3)** — Prevention constrains how requests may be made; avoidance decides dynamically.

</details>

**Q33.** `Medium`  
How often should the deadlock-detection algorithm be invoked?

(1) Only when the system is shut down  
(2) Never, because detection is impossible  
(3) After every instruction  
(4) It depends on how often deadlocks occur and how many processes they affect  

<details><summary>Answer</summary>

**(4)** — It may run on every request that cannot be granted, periodically, or when CPU utilisation drops below a threshold.

</details>

**Q34.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Most general-purpose operating systems, including Linux and Windows, ignore the deadlock problem.  
Reason R: Deadlocks occur infrequently, and prevention, avoidance or detection would be costly.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Applications are expected to handle deadlocks themselves.

</details>

**Q35.** `Medium`  
In a system with 4 processes and 5 resources of a single type, where each process needs at most 2 resources, the system

(1) is deadlock-free  
(2) may deadlock  
(3) always deadlocks  
(4) needs at least 8 resources to avoid deadlock  

<details><summary>Answer</summary>

**(1)** — 4 × (2 − 1) + 1 = 5, so at least one process can always obtain both resources.

</details>

**Q36.** `Medium`  
Which deadlock condition is broken by allowing the OS to take a resource away from a process that holds it?

(1) Mutual exclusion  
(2) Circular wait  
(3) No preemption  
(4) Hold and wait  

<details><summary>Answer</summary>

**(3)** — This works for resources whose state can be saved, such as CPU registers and memory.

</details>

**Q37.** `Medium`  
Which of the following is a necessary condition for a cycle in a wait-for graph to occur?

(1) Each process waits for a resource held by the next process in the cycle  
(2) All processes have the same priority  
(3) All resources have multiple instances  
(4) The system uses preemptive scheduling  

<details><summary>Answer</summary>

**(1)** — An edge Pi → Pj means Pi waits for a resource that Pj holds.

</details>

**Q38.** `Medium`  
Given below are two statements.  
Statement I: The resource-allocation-graph algorithm for deadlock avoidance uses claim edges.  
Statement II: A request is granted only if converting the claim edge to an assignment edge does not create a cycle.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This works for single-instance resource types.

</details>
