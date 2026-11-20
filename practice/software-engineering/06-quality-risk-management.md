# Set 6 — Software Quality, Reliability and Risk Management (McCall, ISO 9126, SQA, CMMI, RMMM)

**24 questions** — High: 10, Medium: 13, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (McCall's quality factor category): A. Product operation  B. Product revision  C. Product transition  
List II (Factors): I. Portability, reusability and interoperability  II. Correctness, reliability, efficiency, integrity and usability  III. Maintainability, flexibility and testability

(1) A-II, B-III, C-I  
(2) A-III, B-II, C-I  
(3) A-I, B-III, C-II  
(4) A-II, B-I, C-III  

<details><summary>Answer</summary>

**(1)** — McCall's model has 11 quality factors in three groups.

</details>

**Q2.** `High`  
Which of the following are the six quality characteristics of ISO 9126?  
A. Functionality  B. Reliability  C. Usability  D. Efficiency  E. Maintainability  F. Portability  
Choose the correct answer from the options given below:

(1) A, C, E and F only  
(2) A, B and C only  
(3) A, B, C, D, E and F  
(4) B, D, E and F only  

<details><summary>Answer</summary>

**(3)** — ISO/IEC 25010 replaced ISO 9126 and adds security and compatibility.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (CMMI maturity level): A. Level 1  B. Level 2  C. Level 3  D. Level 5  
List II (Name): I. Optimizing  II. Initial  III. Defined  IV. Managed

(1) A-II, B-IV, C-III, D-I  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(1)** — Level 4 is Quantitatively Managed (called Managed in the original CMM, where level 2 was Repeatable).

</details>

**Q4.** `High`  
A system has a mean time to failure (MTTF) of 68 days and a mean time to repair (MTTR) of 3 days. Its availability is approximately

(1) 97.1%  
(2) 90.4%  
(3) 99.0%  
(4) 95.8%  

<details><summary>Answer</summary>

**(4)** — Availability = MTTF / (MTTF + MTTR) = 68 / 71 ≈ 0.958.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: MTBF = MTTF + MTTR.  
Statement II: Availability is independent of the mean time to repair.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Availability = MTTF / (MTTF + MTTR), so it falls as repair time grows.

</details>

**Q6.** `High`  
A team finds 90 errors before delivery, and users report 10 defects after delivery. The defect removal efficiency (DRE) is

(1) 0.90  
(2) 0.81  
(3) 0.10  
(4) 0.99  

<details><summary>Answer</summary>

**(1)** — DRE = E / (E + D) = 90 / 100.

</details>

**Q7.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Quality assurance focuses on the process, while quality control focuses on the product.  
Reason R: Quality assurance aims to prevent defects, while quality control aims to detect them.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — QA defines and audits processes; QC inspects and tests work products.

</details>

**Q8.** `High`  
A risk has a probability of 70% and an estimated cost (impact) of Rs. 50,000 if it occurs. The risk exposure is

(1) Rs. 35,000  
(2) Rs. 50,000  
(3) Rs. 70,000  
(4) Rs. 15,000  

<details><summary>Answer</summary>

**(1)** — RE = P × C = 0.7 × 50,000.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Risk category): A. Project risks  B. Technical risks  C. Business risks  D. Unpredictable risks  
List II (Example): I. Building a product that no one wants (market risk)  II. Budget overrun and staff turnover  III. Risks that are extremely difficult to identify in advance  IV. Uncertainty about the interface or implementation technology

(1) A-II, B-IV, C-I, D-III  
(2) A-II, B-IV, C-III, D-I  
(3) A-IV, B-II, C-I, D-III  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(1)** — Pressman classifies risks as project, technical and business, and as known, predictable and unpredictable.

</details>

**Q10.** `High`  
RMMM stands for

(1) Reliability Measurement and Monitoring Method  
(2) Risk Mitigation, Monitoring and Management  
(3) Requirement Modelling and Maintenance Management  
(4) Risk Measurement, Modelling and Mapping  

<details><summary>Answer</summary>

**(2)** — The RMMM plan documents all risk-analysis work.

</details>

**Q11.** `Medium`  
Given below are two statements.  
Statement I: Reactive risk strategies deal with risks only when problems occur.  
Statement II: Proactive risk strategies identify, assess and plan for risks before technical work begins.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Pressman describes reactive strategies as "fire-fighting mode".

</details>

**Q12.** `Medium`  
A risk table (risk projection) lists for each risk its

(1) test cases  
(2) category, probability and impact  
(3) design patterns  
(4) cost per line of code  

<details><summary>Answer</summary>

**(2)** — Risks are sorted by probability and impact, and a cut-off line separates those that will be managed.

</details>

**Q13.** `Medium`  
Match List I with List II.  
List I (Cost of quality component): A. Prevention costs  B. Appraisal costs  C. Internal failure costs  D. External failure costs  
List II (Example): I. Rework due to defects found before delivery  II. Training, planning and quality planning  III. Complaint resolution and warranty work after delivery  IV. Inspections, testing and equipment calibration

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — External failure costs are the most expensive.

</details>

**Q14.** `Medium`  
Six Sigma aims at a defect rate of no more than

(1) 3.4 defects per million opportunities  
(2) 34 defects per million  
(3) 6 defects per hundred  
(4) 1 defect per thousand  

<details><summary>Answer</summary>

**(1)** — Its improvement methodology is DMAIC: define, measure, analyse, improve and control.

</details>

**Q15.** `Medium`  
A formal technical review (FTR) typically involves

(1) 3 to 5 people, advance preparation of no more than about 2 hours, and a meeting of less than 2 hours  
(2) only the author  
(3) no records  
(4) 20 to 30 people for a full day  

<details><summary>Answer</summary>

**(1)** — The review focuses on the product, not the producer.

</details>

**Q16.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Software reliability can be improved by testing alone, without good design.  
Reason R: Testing can show the presence of defects but cannot prove their absence.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — R (Dijkstra) is true; it is exactly why reliability must also be built in through good processes and design, so A is false.

</details>

**Q17.** `Medium`  
Fagan inspection is

(1) a risk-analysis method  
(2) a formal, highly structured review process with defined roles such as moderator, reader and recorder  
(3) a type of unit testing  
(4) an informal walkthrough  

<details><summary>Answer</summary>

**(2)** — Inspections are among the most effective defect-detection techniques.

</details>

**Q18.** `Medium`  
The ISO 9001 standard applies to

(1) programming languages  
(2) quality management systems of organisations in any industry, including software  
(3) only software products  
(4) network protocols  

<details><summary>Answer</summary>

**(2)** — ISO 90003 gives guidelines for applying ISO 9001 to software.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: Statistical SQA ignores the causes of defects.  
Statement II: Statistical SQA uses the Pareto principle: about 80% of defects come from about 20% of causes.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Statistical SQA collects and categorises defect data to find and fix the vital few causes.

</details>

**Q20.** `Medium`  
The probability of failure on demand (POFOD) is an appropriate reliability metric for

(1) batch payroll systems  
(2) protection systems that are called upon only occasionally, such as an emergency shutdown  
(3) games  
(4) continuously running systems  

<details><summary>Answer</summary>

**(2)** — ROCOF (rate of occurrence of failures) suits continuously running systems.

</details>

**Q21.** `Medium`  
In risk management, the risk referent level is

(1) the probability of a risk  
(2) the point at which the project should be stopped or significantly changed if a risk (or combination of risks) reaches it  
(3) the number of risks  
(4) the cost of mitigation  

<details><summary>Answer</summary>

**(2)** — Typical referents are cost, schedule and performance.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: CMMI level 3 (Defined) requires that the organisation's processes be documented, standardised and integrated.  
Statement II: At CMMI level 1 (Initial), processes are well defined and predictable.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — At level 1, processes are ad hoc and success depends on individual effort.

</details>

**Q23.** `Low`  
Software reliability is defined as

(1) the number of lines of code  
(2) the probability of failure-free operation of a program in a specified environment for a specified time  
(3) the cost of development  
(4) the speed of execution  

<details><summary>Answer</summary>

**(2)** — It is one of the most important quality attributes.

</details>

**Q24.** `Medium`  
Musa's basic execution time model and the Jelinski-Moranda model are examples of

(1) design patterns  
(2) software reliability growth models  
(3) process models  
(4) cost estimation models  

<details><summary>Answer</summary>

**(2)** — They predict how reliability improves as defects are removed during testing.

</details>
