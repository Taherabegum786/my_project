# Set 2 — Operating System Basics (structure, services, system calls, dual mode, system boot)

**41 questions** — High: 11, Medium: 28, Low: 2

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Kernel structure): A. Monolithic  B. Microkernel  C. Layered  D. Hybrid  
List II (Example): I. Mach  II. Windows NT  III. Traditional UNIX  IV. THE operating system

(1) A-III, B-IV, C-I, D-II  
(2) A-III, B-I, C-II, D-IV  
(3) A-III, B-I, C-IV, D-II  
(4) A-I, B-III, C-IV, D-II  

<details><summary>Answer</summary>

**(3)** — UNIX is monolithic, Mach a microkernel, Dijkstra's THE system layered, Windows NT a hybrid.

</details>

**Q2.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A microkernel operating system is generally more reliable and secure than a monolithic one.  
Reason R: Most services run as user-level processes, so a failure in a service does not crash the kernel.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Moving services out of the kernel limits the damage of faults, at the cost of message-passing overhead.

</details>

**Q3.** `High`  
The main disadvantage of the microkernel approach is

(1) difficulty of porting  
(2) performance overhead of increased message passing between user-space services  
(3) lack of modularity  
(4) poor security  

<details><summary>Answer</summary>

**(2)** — Services communicate through the kernel by message passing, adding system-call and context-switch overhead.

</details>

**Q4.** `High`  
Which of the following instructions should be privileged (allowed only in kernel mode)?  
A. Set the value of the timer  B. Read the clock  C. Turn off interrupts  D. Access an I/O device  E. Issue a trap instruction  
Choose the correct answer from the options given below:

(1) A, B and C only  
(2) A, C, D and E only  
(3) A, C and D only  
(4) B, D and E only  

<details><summary>Answer</summary>

**(3)** — Reading the clock is harmless, and a trap is how user programs request kernel services.

</details>

**Q5.** `High`  
In the dual-mode operation described by Silberschatz, the mode bit is

(1) 1 for kernel mode and 0 for user mode  
(2) 0 for kernel mode and 1 for user mode  
(3) 0 for both modes  
(4) not stored in hardware  

<details><summary>Answer</summary>

**(2)** — The hardware switches to kernel mode (0) on a trap or interrupt and back to user mode (1) before passing control to a user program.

</details>

**Q6.** `High`  
A timer is used in an operating system mainly to

(1) keep the date and time  
(2) synchronise processes  
(3) measure disk speed  
(4) prevent a user program from getting stuck in an infinite loop and never returning control to the OS  

<details><summary>Answer</summary>

**(4)** — The timer interrupts after a set period, so the OS regains control.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (System call category): A. Process control  B. File management  C. Information maintenance  D. Protection  
List II (Example UNIX call): I. getpid()  II. chmod()  III. fork()  IV. open()

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-II, D-I  
(3) A-III, B-IV, C-I, D-II  
(4) A-IV, B-III, C-I, D-II  

<details><summary>Answer</summary>

**(3)** — fork is process control, open file management, getpid information maintenance, chmod protection.

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Windows API): A. CreateProcess()  B. WaitForSingleObject()  C. CreatePipe()  D. ReadFile()  
List II (UNIX equivalent): I. pipe()  II. wait()  III. fork()  IV. read()

(1) A-III, B-I, C-II, D-IV  
(2) A-III, B-II, C-I, D-IV  
(3) A-III, B-II, C-IV, D-I  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(2)** — Standard Windows/UNIX system call correspondence.

</details>

**Q9.** `Medium`  
Which of the following are general methods of passing parameters to a system call?  
A. In registers  B. In a block or table in memory whose address is passed in a register  C. Pushed onto the stack  D. Through a file on disk  
Choose the correct answer from the options given below:

(1) A, B, C and D  
(2) B, C and D only  
(3) A and B only  
(4) A, B and C only  

<details><summary>Answer</summary>

**(4)** — Registers, a memory block, or the stack are used; files are not.

</details>

**Q10.** `Medium`  
A trap (or exception) is

(1) a type of system program  
(2) a scheduling algorithm  
(3) a hardware interrupt from an I/O device  
(4) a software-generated interrupt caused by an error or by a user request for an OS service  

<details><summary>Answer</summary>

**(4)** — Examples: division by zero, an invalid memory access, or a system call.

</details>

**Q11.** `Medium`  
The printf() function in a C program ultimately invokes which system call to display output?

(1) read()  
(2) write()  
(3) exec()  
(4) ioctl()  

<details><summary>Answer</summary>

**(2)** — printf is a library function that buffers output and calls write().

</details>

**Q12.** `Medium`  
Given below are two statements.  
Statement I: An application programming interface such as POSIX or the Win32 API hides most details of the system call interface from programmers.  
Statement II: A program written using the POSIX API can, in principle, be compiled on any system that supports POSIX.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — APIs give portability and convenience over raw system calls.

</details>

**Q13.** `High`  
The initial program that runs when a computer is powered on and loads the operating system kernel is the

(1) interrupt handler  
(2) scheduler  
(3) shell  
(4) bootstrap program (boot loader)  

<details><summary>Answer</summary>

**(4)** — It is stored in firmware (ROM/EEPROM, BIOS or UEFI) and may load a second-stage loader such as GRUB.

</details>

**Q14.** `Medium`  
The Master Boot Record (MBR) on a BIOS-based disk occupies

(1) the first sector (512 bytes) of the disk  
(2) the last sector of the disk  
(3) the first track  
(4) a separate EEPROM chip  

<details><summary>Answer</summary>

**(1)** — The MBR holds the first-stage boot code and the partition table; GPT is the UEFI replacement.

</details>

**Q15.** `Medium`  
On a UNIX/Linux system, the first user-level process started by the kernel, which has process ID 1, is

(1) swapper  
(2) cron  
(3) bash  
(4) init (or systemd)  

<details><summary>Answer</summary>

**(4)** — init/systemd starts all other services and adopts orphan processes.

</details>

**Q16.** `High`  
Match List I with List II.  
List I (System type): A. Batch system  B. Time-sharing system  C. Hard real-time system  D. Distributed system  
List II (Characteristic): I. Collection of independent computers that appears to users as a single system  II. Jobs with similar needs are grouped and run without user interaction  III. CPU is switched among users frequently to give fast response  IV. Tasks must be completed within guaranteed deadlines

(1) A-II, B-III, C-I, D-IV  
(2) A-II, B-III, C-IV, D-I  
(3) A-III, B-II, C-IV, D-I  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(2)** — Standard classification of operating systems.

</details>

**Q17.** `High`  
Given below are two statements.  
Statement I: Multiprogramming increases CPU utilisation by keeping several jobs in memory so that the CPU always has one to execute.  
Statement II: Time-sharing systems give longer response times than batch systems.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Time-sharing switches the CPU among users frequently precisely to give short response times.

</details>

**Q18.** `Medium`  
Spooling stands for

(1) Sequential Process Ordering On-Line  
(2) System Program Operation On-Line  
(3) Simultaneous Peripheral Operations On-Line  
(4) Shared Peripheral Output On Line  

<details><summary>Answer</summary>

**(3)** — Spooling uses the disk as a large buffer, for example for printer output.

</details>

**Q19.** `Medium`  
The separation of policy from mechanism means that

(1) policies are implemented in hardware  
(2) mechanisms change frequently while policies never change  
(3) mechanisms determine how to do something while policies decide what will be done  
(4) the OS decides what to do and how to do it in the same module  

<details><summary>Answer</summary>

**(3)** — Separating them allows a policy to be changed without changing the underlying mechanism.

</details>

**Q20.** `Medium`  
Arrange the following storage devices in decreasing order of access speed.  
A. Main memory  B. Registers  C. Hard disk  D. Cache  E. Solid-state disk

(1) B, D, A, C, E  
(2) B, A, D, E, C  
(3) B, D, A, E, C  
(4) D, B, A, C, E  

<details><summary>Answer</summary>

**(3)** — Registers, cache, main memory, SSD, magnetic disk.

</details>

**Q21.** `Medium`  
Which of the following is a volatile storage?

(1) Main memory (DRAM)  
(2) Flash memory  
(3) Magnetic disk  
(4) Optical disk  

<details><summary>Answer</summary>

**(1)** — DRAM loses its contents when power is removed.

</details>

**Q22.** `Medium`  
In symmetric multiprocessing (SMP)

(1) one processor controls the others and assigns them tasks  
(2) only one processor can run the OS while others run user programs  
(3) each processor performs all tasks, including operating-system functions, and they share memory  
(4) processors do not share memory  

<details><summary>Answer</summary>

**(3)** — Asymmetric multiprocessing uses a boss-worker relationship.

</details>

**Q23.** `Medium`  
In a clustered system using asymmetric clustering

(1) one machine is in hot-standby mode, monitoring the active server and taking over if it fails  
(2) all machines run applications and monitor each other  
(3) there is no shared storage  
(4) each node runs a different operating system  

<details><summary>Answer</summary>

**(1)** — In symmetric clustering, all hosts run applications and monitor each other.

</details>

**Q24.** `Medium`  
Which of the following is NOT an operating-system service?

(1) Compiling application programs  
(2) I/O operations  
(3) Program execution  
(4) Error detection  

<details><summary>Answer</summary>

**(1)** — Compilation is done by a compiler, which is a system program, not an OS service.

</details>

**Q25.** `Medium`  
The command interpreter in UNIX-like systems is called the

(1) loader  
(2) daemon  
(3) kernel  
(4) shell  

<details><summary>Answer</summary>

**(4)** — Examples are sh, bash, csh and ksh.

</details>

**Q26.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Loadable kernel modules allow the kernel to be extended without recompiling it or rebooting.  
Reason R: Linux is distributed under the GNU General Public License.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but the licence has nothing to do with why modules can be loaded at run time.

</details>

**Q27.** `Medium`  
Which of the following is used by an I/O device to signal the CPU that it needs attention?

(1) Polling  
(2) System call  
(3) Trap  
(4) Interrupt  

<details><summary>Answer</summary>

**(4)** — Device controllers raise interrupts; the CPU uses the interrupt vector to find the handler.

</details>

**Q28.** `Medium`  
The interrupt vector is

(1) a queue of pending I/O requests  
(2) the stack of the interrupted process  
(3) a table of addresses of interrupt service routines  
(4) a register that stores the mode bit  

<details><summary>Answer</summary>

**(3)** — It is indexed by the interrupt number to locate the handler quickly.

</details>

**Q29.** `Medium`  
Which of the following is a non-maskable interrupt typically used for?

(1) Unrecoverable memory errors  
(2) Keyboard input  
(3) Disk I/O completion  
(4) Network packet arrival  

<details><summary>Answer</summary>

**(1)** — Non-maskable interrupts cannot be disabled and are reserved for critical events.

</details>

**Q30.** `Medium`  
Match List I with List II.  
List I (Term): A. Multiprocessing  B. Multiprogramming  C. Multithreading  D. Multitasking  
List II (Meaning): I. Several programs in memory, with the CPU switched when a job waits  II. More than one CPU executing simultaneously  III. Several threads of control within one process  IV. Rapid switching among jobs to give interactive response

(1) A-I, B-II, C-III, D-IV  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-I, C-III, D-IV  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(3)** — Standard definitions of the four terms.

</details>

**Q31.** `Medium`  
Which of the following is an example of a real-time operating system?

(1) VxWorks  
(2) Windows 95  
(3) MS-DOS  
(4) Ubuntu Desktop  

<details><summary>Answer</summary>

**(1)** — VxWorks, QNX and FreeRTOS are real-time operating systems.

</details>

**Q32.** `Medium`  
Given below are two statements.  
Statement I: In a soft real-time system, missing a deadline is treated as a total system failure.  
Statement II: Soft real-time systems give critical tasks priority over others but do not guarantee deadlines.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Missing a deadline is a failure only in a hard real-time system.

</details>

**Q33.** `Medium`  
Which of the following tools traces the system calls made by a running Linux process?

(1) grep  
(2) gdb  
(3) strace  
(4) ldd  

<details><summary>Answer</summary>

**(3)** — strace lists each system call with its arguments and return value.

</details>

**Q34.** `Medium`  
Which of the following is responsible for memory protection, i.e. preventing a process from accessing memory outside its address space, in the simplest scheme?

(1) Program counter  
(2) Interrupt vector  
(3) Stack pointer  
(4) Base and limit registers  

<details><summary>Answer</summary>

**(4)** — Every address generated in user mode is checked against the base and limit registers.

</details>

**Q35.** `Low`  
An operating system that allows a single user to run only one program at a time, such as MS-DOS, is called a

(1) time-sharing OS  
(2) single-user single-tasking OS  
(3) distributed OS  
(4) multi-user OS  

<details><summary>Answer</summary>

**(2)** — MS-DOS ran one program at a time for a single user.

</details>

**Q36.** `Medium`  
The kernel of macOS and iOS (Darwin/XNU) combines

(1) the Windows NT kernel and Mach  
(2) the Linux kernel and BSD  
(3) the Mach microkernel and BSD UNIX components  
(4) MINIX and Linux  

<details><summary>Answer</summary>

**(3)** — XNU is a hybrid kernel built on Mach with BSD layers.

</details>

**Q37.** `Medium`  
Which of the following events causes a switch from user mode to kernel mode?  
A. A system call  B. A hardware interrupt  C. A page fault  D. A function call within a user program  
Choose the correct answer from the options given below:

(1) A and D only  
(2) A, B, C and D  
(3) B, C and D only  
(4) A, B and C only  

<details><summary>Answer</summary>

**(4)** — An ordinary function call stays in user mode.

</details>

**Q38.** `Medium`  
The process of starting a computer by loading the kernel is called

(1) booting  
(2) paging  
(3) spooling  
(4) swapping  

<details><summary>Answer</summary>

**(1)** — The bootstrap program locates, loads and starts the kernel.

</details>

**Q39.** `Low`  
The portion of the operating system that is always resident in main memory is called the

(1) loader  
(2) shell  
(3) kernel  
(4) compiler  

<details><summary>Answer</summary>

**(3)** — The kernel runs at all times; other programs are system or application programs.

</details>

**Q40.** `Medium`  
Given below are two statements.  
Statement I: An emulator allows applications compiled for one hardware architecture to run on a different architecture.  
Statement II: Emulation usually runs faster than running the code natively.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Every instruction must be translated, so emulation is much slower than native execution.

</details>

**Q41.** `Medium`  
Which of the following is NOT a component of the UNIX system call interface category "device management"?

(1) fork()  
(2) read() on a device  
(3) write() on a device  
(4) ioctl()  

<details><summary>Answer</summary>

**(1)** — fork is process control; ioctl, read and write can operate on devices.

</details>
