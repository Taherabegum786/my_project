# Set 11 — Protection, Security and Virtual Machines

**40 questions** — High: 10, Medium: 29, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
In the access-matrix model of protection, rows and columns represent respectively

(1) domains and objects  
(2) objects and domains  
(3) users and passwords  
(4) processes and files only  

<details><summary>Answer</summary>

**(1)** — Entry access(i, j) is the set of operations a process in domain Di may perform on object Oj.

</details>

**Q2.** `High`  
Match List I with List II.  
List I (Access-matrix implementation): A. Access control list  B. Capability list  C. Global table  D. Lock-key mechanism  
List II (Description): I. Each domain has a list of objects with the operations allowed on them  II. Each object has unique bit patterns (locks) and each domain has keys  III. Each object has a list of domains with their access rights  IV. A set of ordered triples &lt;domain, object, rights-set&gt;

(1) A-III, B-I, C-IV, D-II  
(2) A-III, B-IV, C-I, D-II  
(3) A-I, B-III, C-IV, D-II  
(4) A-III, B-I, C-II, D-IV  

<details><summary>Answer</summary>

**(1)** — An ACL stores a column of the access matrix; a capability list stores a row.

</details>

**Q3.** `High`  
Given below are two statements.  
Statement I: An access control list corresponds to a row of the access matrix.  
Statement II: A capability list corresponds to a column of the access matrix.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Rows are domains and columns are objects: an ACL is a column (per object) and a capability list is a row (per domain).

</details>

**Q4.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Revocation of access rights is more difficult with capability lists than with access control lists.  
Reason R: Capabilities are distributed throughout the system, so they must first be found before they can be revoked.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — With an ACL, rights are revoked simply by editing the object's list.

</details>

**Q5.** `Medium`  
Which of the following are schemes for revoking capabilities?  
A. Reacquisition  B. Back-pointers  C. Indirection  D. Keys  E. Aging  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) A and B only  
(3) A, B, C and D only  
(4) B, C and E only  

<details><summary>Answer</summary>

**(3)** — Aging is a scheduling technique, not a revocation scheme.

</details>

**Q6.** `High`  
The principle of least privilege states that

(1) programs, users and systems should be given just enough privileges to perform their tasks  
(2) all users should have administrator privileges  
(3) only the kernel has privileges  
(4) privileges should never change  

<details><summary>Answer</summary>

**(1)** — It limits the damage that a faulty or compromised component can do.

</details>

**Q7.** `Medium`  
In UNIX, the setuid bit on an executable file means that

(1) the file is hidden  
(2) the process runs with the user ID of the file's owner rather than of the user who runs it  
(3) the file can be executed only by the owner  
(4) the file cannot be deleted  

<details><summary>Answer</summary>

**(2)** — For example, passwd runs with root privileges to update the password file.

</details>

**Q8.** `Medium`  
In the Intel protection-ring architecture, the operating-system kernel runs in

(1) ring 2  
(2) ring 1  
(3) ring 0  
(4) ring 3  

<details><summary>Answer</summary>

**(3)** — User applications run in ring 3, the least privileged ring.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Program threat): A. Trojan horse  B. Trap door  C. Logic bomb  D. Buffer overflow  
List II (Description): I. Code that misuses its environment while appearing to be useful  II. Writing beyond the bounds of an array on the stack to overwrite the return address  III. A hidden hole intentionally left by the designer that bypasses normal security  IV. Code that initiates a security incident only under certain conditions

(1) A-I, B-III, C-IV, D-II  
(2) A-I, B-IV, C-III, D-II  
(3) A-III, B-I, C-IV, D-II  
(4) A-I, B-III, C-II, D-IV  

<details><summary>Answer</summary>

**(1)** — Standard program threats in Silberschatz.

</details>

**Q10.** `Medium`  
Match List I with List II.  
List I (Virus type): A. Boot virus  B. Macro virus  C. Polymorphic virus  D. Stealth virus  
List II (Characteristic): I. Changes its signature each time it is installed to avoid detection  II. Infects the boot sector and runs every time the system is booted  III. Written in a high-level macro language, e.g. in a word-processor document  IV. Modifies parts of the system that could be used to detect it

(1) A-II, B-I, C-III, D-IV  
(2) A-II, B-III, C-I, D-IV  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Common virus categories.

</details>

**Q11.** `Medium`  
The Morris worm of 1988 spread by exploiting

(1) the boot sector of floppy disks  
(2) weaknesses in the UNIX finger, sendmail and rsh programs  
(3) a macro in a word processor  
(4) a flaw in the Windows registry  

<details><summary>Answer</summary>

**(2)** — It was one of the first widely spread Internet worms.

</details>

**Q12.** `Medium`  
Given below are two statements.  
Statement I: Adding a random salt to each password before hashing defeats precomputed dictionary attacks on the password file.  
Statement II: Salting makes two users with the same password have the same stored hash.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — With different salts, identical passwords produce different hashes.

</details>

**Q13.** `Medium`  
A one-time password scheme protects against

(1) denial of service  
(2) reuse of an eavesdropped password  
(3) trap doors  
(4) buffer overflows  

<details><summary>Answer</summary>

**(2)** — Each password is valid for only one session.

</details>

**Q14.** `Medium`  
Two-factor authentication requires

(1) two different user names  
(2) logging in twice  
(3) two of the following: something you know, something you have, something you are  
(4) two passwords  

<details><summary>Answer</summary>

**(3)** — For example a password together with a hardware token or a fingerprint.

</details>

**Q15.** `Medium`  
Match List I with List II.  
List I (Intrusion detection approach): A. Signature-based detection  B. Anomaly detection  
List II (Description): I. Detects deviations from normal behaviour and can find previously unknown attacks, with more false alarms  II. Looks for patterns of known attacks and cannot detect new attacks

(1) A-II, B-I  
(2) A-I, B-II  
(3) Both use pattern matching only  
(4) Both can detect only known attacks  

<details><summary>Answer</summary>

**(1)** — The two main approaches to intrusion detection.

</details>

**Q16.** `Medium`  
In the US Department of Defense TCSEC (Orange Book) classification, the division that provides minimal protection is

(1) D  
(2) A  
(3) B  
(4) C  

<details><summary>Answer</summary>

**(1)** — The levels from lowest to highest are D, C1, C2, B1, B2, B3 and A1.

</details>

**Q17.** `Medium`  
Tripwire is an example of a

(1) virus  
(2) file-integrity checking tool that detects changes to files using stored signatures  
(3) password cracker  
(4) firewall  

<details><summary>Answer</summary>

**(2)** — It compares current file hashes with a stored database.

</details>

**Q18.** `Medium`  
Given below are two statements.  
Statement I: In discretionary access control (DAC), the owner of an object decides who may access it.  
Statement II: In mandatory access control (MAC), access is decided by system-wide policy that users cannot override.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — SELinux implements mandatory access control.

</details>

**Q19.** `Medium`  
Role-based access control (RBAC) assigns privileges to

(1) roles, which are then assigned to users  
(2) hardware devices  
(3) network ports only  
(4) individual files  

<details><summary>Answer</summary>

**(1)** — Solaris 10 and later implement RBAC.

</details>

**Q20.** `Medium`  
Which of the following is a network or system threat rather than a program threat?

(1) Logic bomb  
(2) Trap door  
(3) Port scanning  
(4) Trojan horse  

<details><summary>Answer</summary>

**(3)** — Port scanning, worms and denial-of-service attacks target systems and networks.

</details>

**Q21.** `High`  
Match List I with List II.  
List I (Hypervisor type): A. Type 0  B. Type 1  C. Type 2  
List II (Example): I. VMware ESX, Citrix XenServer  II. VMware Workstation, Oracle VirtualBox  III. IBM LPARs, Oracle LDOMs (firmware-based)

(1) A-III, B-II, C-I  
(2) A-I, B-III, C-II  
(3) A-III, B-I, C-II  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(3)** — Silberschatz's classification of virtual machine managers.

</details>

**Q22.** `High`  
Given below are two statements.  
Statement I: In paravirtualization, the guest operating system is modified to work with the VMM.  
Statement II: In paravirtualization, the guest operating system is unaware that it is running in a virtual machine.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A paravirtualized guest knows about the hypervisor and calls it directly.

</details>

**Q23.** `High`  
In the trap-and-emulate method of virtualization, when the guest kernel (running in virtual kernel mode, which is physical user mode) executes a privileged instruction

(1) the guest is terminated  
(2) it causes a trap to the VMM, which emulates the instruction for the guest  
(3) it executes directly on the hardware  
(4) the instruction is ignored  

<details><summary>Answer</summary>

**(2)** — Non-privileged instructions run natively at full speed.

</details>

**Q24.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Classic x86 processors could not be virtualized with pure trap-and-emulate.  
Reason R: Intel VT-x and AMD-V add hardware support for virtualization.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but the reason classic x86 failed is that some sensitive instructions (such as POPF) do not trap.

</details>

**Q25.** `Medium`  
Binary translation in a VMM such as VMware

(1) converts binary files to text  
(2) translates virtual addresses to physical addresses  
(3) rewrites sensitive guest kernel instructions into safe instruction sequences at run time  
(4) compiles the guest OS from source  

<details><summary>Answer</summary>

**(3)** — Translated code is cached for reuse.

</details>

**Q26.** `Medium`  
Nested page tables (Intel EPT, AMD RVI/NPT) are a hardware feature that

(1) replace the hypervisor  
(2) add more TLB entries  
(3) encrypt guest memory  
(4) speeds up memory virtualization by letting the hardware translate guest-physical to host-physical addresses  

<details><summary>Answer</summary>

**(4)** — They avoid the overhead of software-maintained shadow page tables.

</details>

**Q27.** `Medium`  
Moving a running guest from one host to another with no interruption of service is called

(1) cloning  
(2) ballooning  
(3) snapshotting  
(4) live migration  

<details><summary>Answer</summary>

**(4)** — Memory pages are copied while the guest runs, then the final state is transferred.

</details>

**Q28.** `Medium`  
In memory ballooning, the VMM

(1) deletes guest processes  
(2) installs a driver in the guest that allocates memory to force the guest to page out, returning the freed memory to the VMM  
(3) adds memory chips to the host  
(4) shares identical pages  

<details><summary>Answer</summary>

**(2)** — This lets the VMM reclaim memory from guests when it is overcommitted.

</details>

**Q29.** `Medium`  
Match List I with List II.  
List I (Virtualization category): A. Programming-environment virtualization  B. Emulation  C. Application containment  
List II (Example): I. Linux containers, Solaris zones, BSD jails  II. QEMU running ARM code on an x86 host  III. Java Virtual Machine, .NET CLR

(1) A-III, B-II, C-I  
(2) A-III, B-I, C-II  
(3) A-II, B-III, C-I  
(4) A-I, B-II, C-III  

<details><summary>Answer</summary>

**(1)** — Variations of virtualization beyond full hypervisors.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: Containers share the host kernel and are therefore lighter weight than virtual machines.  
Statement II: A container can run a guest operating system with a different kernel from the host.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Containers must use the host's kernel; a VM can run any OS.

</details>

**Q31.** `Medium`  
The Popek and Goldberg requirements for a virtual machine monitor are

(1) portability, compatibility and scalability  
(2) speed, cost and size  
(3) fidelity, performance and safety (resource control)  
(4) isolation, encryption and compression  

<details><summary>Answer</summary>

**(3)** — A program in the VM should behave as on real hardware, run mostly at native speed, and the VMM must control all resources.

</details>

**Q32.** `Medium`  
The first commercially available virtual machine system was

(1) IBM VM/370  
(2) Xen  
(3) Hyper-V  
(4) VMware Workstation  

<details><summary>Answer</summary>

**(1)** — IBM VM/370 (1972) let each user run a separate CMS operating system in a VM.

</details>

**Q33.** `Medium`  
Which of the following is a benefit of virtual machines?  
A. Isolation of guests from each other  B. Running several different operating systems on one machine  C. Easier testing and development of operating systems  D. Server consolidation  
Choose the correct answer from the options given below:

(1) B, C and D only  
(2) A, B, C and D  
(3) A, C and D only  
(4) A and B only  

<details><summary>Answer</summary>

**(2)** — All four are standard benefits.

</details>

**Q34.** `Medium`  
A hypervisor that is built into a general-purpose operating system, such as KVM in Linux or Hyper-V in Windows Server, is classified as

(1) Type 2  
(2) Type 0  
(3) Type 3  
(4) Type 1  

<details><summary>Answer</summary>

**(4)** — Silberschatz treats them as Type 1 hypervisors because they run in kernel mode and use hardware assistance.

</details>

**Q35.** `Medium`  
Overcommitment of memory in a VMM means that

(1) the host has more memory than all guests  
(2) each guest gets exactly its share  
(3) memory is never reclaimed  
(4) guests are allocated more memory in total than physically exists  

<details><summary>Answer</summary>

**(4)** — It is supported by ballooning, page sharing and swapping.

</details>

**Q36.** `Medium`  
Given below are two statements.  
Statement I: Encrypting data protects confidentiality but not availability.  
Statement II: A denial-of-service attack threatens availability.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Security goals include confidentiality, integrity and availability.

</details>

**Q37.** `Medium`  
Code injection attacks such as stack-smashing can be mitigated by

(1) increasing the disk size  
(2) disabling the cache  
(3) using larger page sizes  
(4) making the stack non-executable (NX bit) and using address-space layout randomisation  

<details><summary>Answer</summary>

**(4)** — These defences make injected code harder to execute or locate.

</details>

**Q38.** `Medium`  
In the protection model, a domain switch in UNIX occurs when

(1) a file is opened  
(2) a page fault occurs  
(3) a process is swapped out  
(4) a process executes a setuid program, temporarily changing its user ID  

<details><summary>Answer</summary>

**(4)** — In UNIX a domain is associated with the user ID.

</details>

**Q39.** `Medium`  
In the access-matrix model, a right marked with an asterisk (for example read\*) indicates the

(1) copy right, allowing the right to be copied to other domains for the same object  
(2) control right  
(3) owner right  
(4) switch right  

<details><summary>Answer</summary>

**(1)** — Owner and control rights are separate special rights.

</details>

**Q40.** `Low`  
Which security mechanism examines packets and blocks traffic according to rules, separating trusted and untrusted networks?

(1) Compiler  
(2) Linker  
(3) Firewall  
(4) Assembler  

<details><summary>Answer</summary>

**(3)** — A firewall limits the network access between security domains.

</details>
