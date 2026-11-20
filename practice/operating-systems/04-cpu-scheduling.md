# Set 4 — CPU Scheduling (criteria, algorithms, Gantt-chart numericals, multiprocessor and real-time scheduling)

**55 questions** — High: 27, Medium: 27, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Three processes P1, P2 and P3 arrive at time 0 in that order with CPU burst times of 24, 3 and 3 ms. The average waiting time under FCFS scheduling is

(1) 17 ms  
(2) 5.67 ms  
(3) 3 ms  
(4) 27 ms  

<details><summary>Answer</summary>

**(1)** — Waiting times are 0, 24 and 27 ms; the average is 51/3 = 17 ms.

</details>

**Q2.** `High`  
Processes P1, P2 and P3 with burst times 24, 3 and 3 ms all arrive at time 0. If they arrive in the order P2, P3, P1, the average waiting time under FCFS is

(1) 17 ms  
(2) 3 ms  
(3) 10 ms  
(4) 5 ms  

<details><summary>Answer</summary>

**(2)** — Waiting times are 0, 3 and 6 ms; the average is 3 ms, showing how much FCFS depends on arrival order.

</details>

**Q3.** `High`  
Processes P1, P2 and P3 with burst times 24, 3 and 3 ms arrive at time 0 in that order. The average waiting time under round-robin scheduling with a time quantum of 4 ms is

(1) 6 ms  
(2) 5.67 ms  
(3) 17 ms  
(4) 4 ms  

<details><summary>Answer</summary>

**(2)** — Gantt chart: P1 0–4, P2 4–7, P3 7–10, P1 10–30. Waiting times are 6, 4 and 7; the average is 17/3 ≈ 5.67 ms.

</details>

**Q4.** `High`  
Consider processes with (arrival time, burst time): P1 (0, 7), P2 (2, 4), P3 (4, 1), P4 (5, 4). The average waiting time under non-preemptive SJF scheduling is

(1) 4  
(2) 6  
(3) 3  
(4) 5  

<details><summary>Answer</summary>

**(1)** — Order P1 (0–7), P3 (7–8), P2 (8–12), P4 (12–16). Waiting times 0, 6, 3, 7; average 16/4 = 4.

</details>

**Q5.** `High`  
Consider processes with (arrival time, burst time): P1 (0, 7), P2 (2, 4), P3 (4, 1), P4 (5, 4). The average waiting time under preemptive SJF (shortest remaining time first) scheduling is

(1) 4  
(2) 7  
(3) 5  
(4) 3  

<details><summary>Answer</summary>

**(4)** — Gantt: P1 0–2, P2 2–4, P3 4–5, P2 5–7, P4 7–11, P1 11–16. Waiting times 9, 1, 0, 2; average 12/4 = 3.

</details>

**Q6.** `High`  
Consider processes with (arrival time, burst time): P1 (0, 7), P2 (2, 4), P3 (4, 1), P4 (5, 4). The average turnaround time under SRTF scheduling is

(1) 8  
(2) 7  
(3) 6  
(4) 9  

<details><summary>Answer</summary>

**(2)** — Completion times are 16, 7, 5 and 11; turnaround times 16, 5, 1, 6; average 28/4 = 7.

</details>

**Q7.** `High`  
Consider processes with (arrival time, burst time): P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5). The average waiting time under SRTF scheduling is

(1) 13  
(2) 7.75  
(3) 6.5  
(4) 8.75  

<details><summary>Answer</summary>

**(3)** — Gantt: P1 0–1, P2 1–5, P4 5–10, P1 10–17, P3 17–26. Waiting times 9, 0, 15, 2; average 26/4 = 6.5.

</details>

**Q8.** `High`  
Consider processes with (arrival time, burst time): P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5). The average waiting time under non-preemptive SJF scheduling is

(1) 8.75  
(2) 7.75  
(3) 6.5  
(4) 9.25  

<details><summary>Answer</summary>

**(2)** — Order P1 0–8, P2 8–12, P4 12–17, P3 17–26. Waiting times 0, 7, 15, 9; average 31/4 = 7.75.

</details>

**Q9.** `Medium`  
Consider processes with (arrival time, burst time): P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5). How many context switches occur under SRTF scheduling, not counting the initial dispatch at time 0?

(1) 4  
(2) 3  
(3) 5  
(4) 6  

<details><summary>Answer</summary>

**(1)** — The CPU passes P1 → P2 → P4 → P1 → P3, which is 4 switches.

</details>

**Q10.** `High`  
Five processes arrive at time 0 with (burst time, priority): P1 (10, 3), P2 (1, 1), P3 (2, 4), P4 (1, 5), P5 (5, 2). A smaller number means a higher priority. The average waiting time under non-preemptive priority scheduling is

(1) 3.2  
(2) 12  
(3) 8.2  
(4) 9.6  

<details><summary>Answer</summary>

**(3)** — Order P2, P5, P1, P3, P4 with waiting times 0, 1, 6, 16, 18; average 41/5 = 8.2.

</details>

**Q11.** `High`  
Five processes arrive at time 0 with burst times P1 = 10, P2 = 1, P3 = 2, P4 = 1 and P5 = 5. The average waiting time under SJF scheduling is

(1) 9.6  
(2) 8.2  
(3) 3.2  
(4) 5.4  

<details><summary>Answer</summary>

**(3)** — Order P2, P4, P3, P5, P1 with waiting times 0, 1, 2, 4, 9; average 16/5 = 3.2.

</details>

**Q12.** `Medium`  
Five processes arrive at time 0 in the order P1 to P5 with burst times 10, 1, 2, 1 and 5. The average waiting time under round robin with a time quantum of 1 is

(1) 8.2  
(2) 9.6  
(3) 5.4  
(4) 3.2  

<details><summary>Answer</summary>

**(3)** — Completion times are 19, 2, 7, 4 and 14; waiting times 9, 1, 5, 3, 9; average 27/5 = 5.4.

</details>

**Q13.** `High`  
Consider processes with (arrival time, burst time, priority): P1 (0, 5, 3), P2 (1, 3, 1), P3 (2, 8, 4), P4 (3, 6, 2). A smaller number means higher priority. The average waiting time under preemptive priority scheduling is

(1) 5.5  
(2) 6  
(3) 11  
(4) 5.25  

<details><summary>Answer</summary>

**(1)** — Gantt: P1 0–1, P2 1–4, P4 4–10, P1 10–14, P3 14–22. Waiting times 9, 0, 12, 1; average 22/4 = 5.5.

</details>

**Q14.** `High`  
Consider five jobs with (arrival time, service time): A (0, 3), B (2, 6), C (4, 4), D (6, 5), E (8, 2). Under highest response ratio next (HRRN) scheduling, the order of completion is

(1) A, B, E, C, D  
(2) A, C, B, E, D  
(3) A, B, C, E, D  
(4) A, B, C, D, E  

<details><summary>Answer</summary>

**(3)** — At t = 9 the ratios are C 2.25, D 1.6, E 1.5, so C runs; at t = 13 they are D 2.4 and E 3.5, so E runs before D.

</details>

**Q15.** `Medium`  
Consider five jobs with (arrival time, service time): A (0, 3), B (2, 6), C (4, 4), D (6, 5), E (8, 2). The average turnaround time under HRRN scheduling is

(1) 8.6  
(2) 7.6  
(3) 7.2  
(4) 8  

<details><summary>Answer</summary>

**(4)** — Completion times 3, 9, 13, 20, 15; turnaround times 3, 7, 9, 14, 7; average 40/5 = 8.

</details>

**Q16.** `Medium`  
Consider five jobs with (arrival time, service time): A (0, 3), B (2, 6), C (4, 4), D (6, 5), E (8, 2). The average turnaround time under SRTF scheduling is

(1) 7.6  
(2) 8  
(3) 8.6  
(4) 7.2  

<details><summary>Answer</summary>

**(4)** — Gantt: A 0–3, B 3–4, C 4–8, E 8–10, B 10–15, D 15–20. Turnaround 3, 13, 4, 14, 2; average 36/5 = 7.2.

</details>

**Q17.** `Medium`  
The response ratio used in highest response ratio next (HRRN) scheduling is

(1) (waiting time + service time) / service time  
(2) service time / waiting time  
(3) waiting time / service time  
(4) (waiting time + service time) / waiting time  

<details><summary>Answer</summary>

**(1)** — It favours short jobs, but the ratio of a long job grows as it waits, so there is no starvation.

</details>

**Q18.** `Medium`  
Six processes with (arrival time, burst time) P1 (0, 4), P2 (1, 5), P3 (2, 2), P4 (3, 1), P5 (4, 6), P6 (6, 3) are scheduled using round robin with a quantum of 2. A newly arrived process joins the ready queue before a process whose quantum has just expired. The completion time of P2 is

(1) 15  
(2) 21  
(3) 18  
(4) 17  

<details><summary>Answer</summary>

**(3)** — Gantt: P1 0–2, P2 2–4, P3 4–6, P1 6–8, P4 8–9, P5 9–11, P2 11–13, P6 13–15, P5 15–17, P2 17–18, P6 18–19, P5 19–21.

</details>

**Q19.** `High`  
Which scheduling algorithm gives the minimum average waiting time for a given set of processes that are all available at the same time?

(1) FCFS  
(2) Priority  
(3) Round robin  
(4) SJF  

<details><summary>Answer</summary>

**(4)** — SJF is provably optimal for average waiting time; its preemptive version SRTF is optimal when arrivals differ.

</details>

**Q20.** `High`  
Given below are two statements.  
Statement I: SJF scheduling is optimal but difficult to implement because the length of the next CPU burst is not known in advance.  
Statement II: The next CPU burst is usually predicted as an exponential average of the measured lengths of previous bursts.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — τ(n+1) = α t(n) + (1 − α) τ(n).

</details>

**Q21.** `High`  
Using exponential averaging with α = 0.5 and an initial prediction τ0 = 10 ms, the predicted length of the next CPU burst after observed bursts of 6 ms and then 4 ms is

(1) 8 ms  
(2) 6 ms  
(3) 7 ms  
(4) 5 ms  

<details><summary>Answer</summary>

**(2)** — τ1 = 0.5 × 6 + 0.5 × 10 = 8; τ2 = 0.5 × 4 + 0.5 × 8 = 6 ms.

</details>

**Q22.** `Medium`  
In exponential averaging τ(n+1) = α t(n) + (1 − α) τ(n), the value α = 0 means that

(1) only the most recent burst matters  
(2) all bursts are given equal weight  
(3) recent history has no effect on the prediction  
(4) the prediction is always zero  

<details><summary>Answer</summary>

**(3)** — With α = 0 the prediction never changes; with α = 1 only the last burst counts.

</details>

**Q23.** `High`  
Match List I with List II.  
List I (Scheduling algorithm): A. FCFS  B. Round robin  C. SJF  D. Priority  
List II (Problem/feature): I. Convoy effect  II. Needs knowledge of the next CPU burst length  III. Indefinite blocking (starvation), solved by aging  IV. Performance depends heavily on the size of the time quantum

(1) A-I, B-IV, C-III, D-II  
(2) A-I, B-IV, C-II, D-III  
(3) A-I, B-II, C-IV, D-III  
(4) A-IV, B-I, C-II, D-III  

<details><summary>Answer</summary>

**(2)** — Standard characteristics of each algorithm.

</details>

**Q24.** `High`  
Which of the following scheduling algorithms are non-preemptive?  
A. FCFS  B. Round robin  C. SRTF  D. HRRN  
Choose the correct answer from the options given below:

(1) A, B and D only  
(2) B and C only  
(3) A and D only  
(4) A, C and D only  

<details><summary>Answer</summary>

**(3)** — Round robin and SRTF preempt the running process.

</details>

**Q25.** `High`  
Aging is a technique used to

(1) decrease the quantum of long jobs  
(2) reduce context-switch overhead  
(3) terminate old processes  
(4) gradually increase the priority of processes that wait in the system for a long time  

<details><summary>Answer</summary>

**(4)** — Aging prevents starvation in priority scheduling.

</details>

**Q26.** `High`  
If the time quantum in round-robin scheduling is made very large, the algorithm behaves like

(1) multilevel queue scheduling  
(2) FCFS  
(3) priority scheduling  
(4) SJF  

<details><summary>Answer</summary>

**(2)** — Every process finishes its burst within one quantum, so RR reduces to FCFS.

</details>

**Q27.** `Medium`  
If the time quantum in round-robin scheduling is very small

(1) throughput increases indefinitely  
(2) starvation occurs  
(3) the algorithm becomes FCFS  
(4) context-switch overhead becomes very high  

<details><summary>Answer</summary>

**(4)** — Most CPU time is then spent switching (processor sharing in the limit).

</details>

**Q28.** `Medium`  
In round-robin scheduling with 5 processes in the ready queue and a time quantum of 20 ms, the maximum time a process waits before getting its next quantum is

(1) 80 ms  
(2) 120 ms  
(3) 20 ms  
(4) 100 ms  

<details><summary>Answer</summary>

**(1)** — A process waits at most (n − 1) × q = 4 × 20 = 80 ms.

</details>

**Q29.** `Medium`  
In round robin, each time quantum is 10 ms and each context switch takes 1 ms. If all processes use their full quantum, the CPU efficiency is approximately

(1) 100%  
(2) 90.9%  
(3) 81.8%  
(4) 99%  

<details><summary>Answer</summary>

**(2)** — Useful time / total time = 10 / (10 + 1) ≈ 90.9%.

</details>

**Q30.** `High`  
Match List I with List II.  
List I (Scheduling criterion): A. Throughput  B. Turnaround time  C. Waiting time  D. Response time  
List II (Definition): I. Time from submission until the first response is produced  II. Number of processes completed per unit time  III. Total time spent in the ready queue  IV. Time from submission to completion

(1) A-II, B-III, C-IV, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-IV, B-II, C-III, D-I  

<details><summary>Answer</summary>

**(2)** — Standard scheduling criteria definitions.

</details>

**Q31.** `High`  
Which of the following scheduling criteria should be maximised?  
A. CPU utilisation  B. Throughput  C. Turnaround time  D. Waiting time  E. Response time  
Choose the correct answer from the options given below:

(1) C, D and E only  
(2) A and B only  
(3) A, B and C only  
(4) B and E only  

<details><summary>Answer</summary>

**(2)** — Utilisation and throughput are maximised; the time measures are minimised.

</details>

**Q32.** `Medium`  
Turnaround time is equal to

(1) arrival time + burst time  
(2) waiting time − burst time  
(3) completion time − burst time  
(4) completion time − arrival time  

<details><summary>Answer</summary>

**(4)** — Waiting time = turnaround time − burst time.

</details>

**Q33.** `Medium`  
CPU scheduling decisions are preemptive when a process switches

(1) from running to ready state  
(2) from running to terminated state  
(3) from running to waiting state  
(4) from new to ready state  

<details><summary>Answer</summary>

**(1)** — Switching from running to waiting or terminating is voluntary (non-preemptive); running to ready and waiting to ready allow preemption.

</details>

**Q34.** `High`  
Given below are two statements.  
Statement I: In multilevel queue scheduling, processes move between queues according to their CPU-burst behaviour.  
Statement II: In multilevel feedback queue scheduling, a process is permanently assigned to one queue when it enters the system.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — The two descriptions are swapped: multilevel queues assign processes permanently, while feedback queues let them move.

</details>

**Q35.** `Medium`  
In a multilevel feedback queue scheduler, a process that uses too much CPU time is

(1) terminated  
(2) moved to a lower-priority queue  
(3) moved to the waiting queue  
(4) moved to a higher-priority queue  

<details><summary>Answer</summary>

**(2)** — I/O-bound and interactive processes stay in the higher-priority queues.

</details>

**Q36.** `Medium`  
Which of the following is NOT a parameter needed to define a multilevel feedback queue scheduler?

(1) The scheduling algorithm for each queue  
(2) The method used to demote or upgrade a process  
(3) The number of queues  
(4) The size of main memory  

<details><summary>Answer</summary>

**(4)** — Memory size is unrelated to the definition of an MLFQ scheduler.

</details>

**Q37.** `Medium`  
The convoy effect, in which many short processes wait behind one long process, is associated with

(1) round robin  
(2) FCFS  
(3) SRTF  
(4) SJF  

<details><summary>Answer</summary>

**(2)** — It lowers CPU and device utilisation.

</details>

**Q38.** `Medium`  
In a system, each process spends 80% of its time waiting for I/O. With 4 processes in memory, the approximate CPU utilisation is

(1) 80%  
(2) 59%  
(3) 41%  
(4) 20%  

<details><summary>Answer</summary>

**(2)** — Utilisation = 1 − p^n = 1 − 0.8^4 = 1 − 0.4096 ≈ 59%.

</details>

**Q39.** `High`  
Given below are two statements.  
Statement I: Rate-monotonic scheduling assigns static priorities, with a shorter period meaning a higher priority.  
Statement II: Earliest-deadline-first scheduling assigns priorities dynamically according to deadlines.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — RM is optimal among static-priority algorithms; EDF is dynamic.

</details>

**Q40.** `High`  
The worst-case CPU utilisation bound that guarantees schedulability of two processes under rate-monotonic scheduling is approximately

(1) 100%  
(2) 83%  
(3) 69%  
(4) 78%  

<details><summary>Answer</summary>

**(2)** — Bound = n(2^(1/n) − 1) = 2(√2 − 1) ≈ 0.828 for n = 2; it tends to ln 2 ≈ 69% as n grows.

</details>

**Q41.** `Medium`  
Two periodic tasks have (period, execution time) of (50, 20) and (100, 35). Their total CPU utilisation is

(1) 75%  
(2) 67.5%  
(3) 85%  
(4) 55%  

<details><summary>Answer</summary>

**(1)** — 20/50 + 35/100 = 0.40 + 0.35 = 0.75, which is below the RM bound of 0.828, so they are schedulable under RM.

</details>

**Q42.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Two tasks with (period, execution time) of (50, 25) and (80, 35) can be scheduled by EDF but may miss deadlines under rate-monotonic scheduling.  
Reason R: Their utilisation of about 94% is at most 100%, but exceeds the rate-monotonic bound of about 83% for two tasks.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — EDF can theoretically achieve 100% utilisation; above the RM bound, schedulability under RM is not guaranteed, and this set does miss a deadline under RM.

</details>

**Q43.** `Medium`  
The upper bound on CPU utilisation for a set of periodic tasks to be schedulable under EDF is

(1) 83%  
(2) 100%  
(3) There is no bound  
(4) 69%  

<details><summary>Answer</summary>

**(2)** — EDF is optimal for preemptive uniprocessor scheduling of periodic tasks.

</details>

**Q44.** `High`  
Priority inversion occurs when

(1) two processes have the same priority  
(2) a low-priority process holds a resource needed by a high-priority process, and a medium-priority process preempts the low-priority one  
(3) a high-priority process always runs first  
(4) the scheduler reverses the priority queue  

<details><summary>Answer</summary>

**(2)** — It is solved by the priority-inheritance protocol (famous in the Mars Pathfinder case).

</details>

**Q45.** `Medium`  
Given below are two statements.  
Statement I: Processor affinity means that a process prefers to keep running on the processor on which it is currently executing.  
Statement II: Processor affinity increases cache misses because the process keeps moving between processors.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Affinity avoids migration, so the process can reuse the contents of its processor's cache.

</details>

**Q46.** `Medium`  
In multiprocessor load balancing, a periodic task that moves processes from overloaded to idle processors is called

(1) push migration  
(2) gang scheduling  
(3) pull migration  
(4) processor affinity  

<details><summary>Answer</summary>

**(1)** — In pull migration, an idle processor pulls a waiting task from a busy one.

</details>

**Q47.** `Medium`  
Under process-contention scope (PCS), threads

(1) compete for the CPU with other threads of the same process  
(2) are not scheduled at all  
(3) compete for the CPU with all threads in the system  
(4) are scheduled only by the kernel  

<details><summary>Answer</summary>

**(1)** — System-contention scope (SCS) competes among all threads in the system; one-to-one systems such as Linux use only SCS.

</details>

**Q48.** `Medium`  
Which of the following real-time scheduling policies are defined by POSIX?

(1) SCHED\_LOTTERY and SCHED\_FAIR  
(2) SCHED\_FIFO and SCHED\_RR  
(3) SCHED\_EDF and SCHED\_RM  
(4) SCHED\_SJF and SCHED\_HRRN  

<details><summary>Answer</summary>

**(2)** — SCHED\_OTHER is the implementation-defined non-real-time policy.

</details>

**Q49.** `Medium`  
In lottery scheduling, a process with more tickets

(1) is never preempted  
(2) gets a longer quantum  
(3) has a proportionally higher chance of getting the CPU  
(4) always runs first  

<details><summary>Answer</summary>

**(3)** — It is a probabilistic proportional-share scheduler.

</details>

**Q50.** `Medium`  
Which component gives control of the CPU to the process selected by the short-term scheduler?

(1) Loader  
(2) Dispatcher  
(3) Long-term scheduler  
(4) Interrupt handler  

<details><summary>Answer</summary>

**(2)** — It switches context, switches to user mode and jumps to the proper location.

</details>

**Q51.** `Medium`  
An I/O-bound process typically has

(1) exactly one CPU burst  
(2) many short CPU bursts  
(3) no CPU bursts  
(4) a few very long CPU bursts  

<details><summary>Answer</summary>

**(2)** — CPU-bound processes have a few long CPU bursts.

</details>

**Q52.** `High`  
Arrange the following algorithms in increasing order of average waiting time for processes with (arrival, burst): P1 (0, 7), P2 (2, 4), P3 (4, 1), P4 (5, 4).  
A. FCFS  B. SJF  C. SRTF

(1) C, A, B  
(2) B, C, A  
(3) A, B, C  
(4) C, B, A  

<details><summary>Answer</summary>

**(4)** — SRTF gives 3, SJF gives 4 and FCFS gives (0 + 5 + 7 + 7)/4 = 4.75.

</details>

**Q53.** `Medium`  
Which scheduling algorithm can lead to starvation?  
A. FCFS  B. SJF  C. Priority  D. Round robin  
Choose the correct answer from the options given below:

(1) A and D only  
(2) B and C only  
(3) A, B, C and D  
(4) A, B and C only  

<details><summary>Answer</summary>

**(2)** — FCFS and RR serve every process in turn; SJF and priority can postpone a process indefinitely.

</details>

**Q54.** `Low`  
A scheduling algorithm that assigns each process a fixed share of CPU time, e.g. 50% to one user's processes, is called

(1) fair-share scheduling  
(2) deadline scheduling  
(3) SJF scheduling  
(4) FCFS scheduling  

<details><summary>Answer</summary>

**(1)** — Fair-share scheduling allocates CPU among users or groups rather than individual processes.

</details>

**Q55.** `Medium`  
Simultaneous multithreading (hyper-threading) allows

(1) a process to run on two machines  
(2) one core to appear as multiple logical processors to the operating system  
(3) multiple cores to share one cache line  
(4) a thread to run without a stack  

<details><summary>Answer</summary>

**(2)** — Each hardware thread has its own architectural state; the OS schedules them as separate CPUs.

</details>
