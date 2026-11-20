# Set 7 — Estimation and Scheduling (LOC and FP estimation, COCOMO, Putnam, scheduling, earned value)

**30 questions** — High: 13, Medium: 16, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Using the basic COCOMO model, the effort for an organic-mode project of 32 KLOC (E = 2.4 × KLOC^(1.05) person-months) is approximately

(1) 91.3 PM  
(2) 230.4 PM  
(3) 145.5 PM  
(4) 76.8 PM  

<details><summary>Answer</summary>

**(1)** — 2.4 × 32^(1.05) ≈ 91.3 person-months.

</details>

**Q2.** `High`  
For an organic-mode project with an effort of 91.3 person-months, the basic COCOMO development time D = 2.5 × E^(0.38) is approximately

(1) 36.5 months  
(2) 13.9 months  
(3) 9.1 months  
(4) 18.2 months  

<details><summary>Answer</summary>

**(2)** — 2.5 × 91.3^(0.38) ≈ 13.9 months, so about 91.3 / 13.9 ≈ 6.6 people on average.

</details>

**Q3.** `High`  
Match List I with List II.  
List I (Basic COCOMO mode): A. Organic  B. Semi-detached  C. Embedded  
List II (Effort equation): I. E = 3.6 (KLOC)^(1.20)  II. E = 2.4 (KLOC)^(1.05)  III. E = 3.0 (KLOC)^(1.12)

(1) A-III, B-II, C-I  
(2) A-II, B-I, C-III  
(3) A-I, B-III, C-II  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — For a 32 KLOC project these give about 91, 146 and 230 person-months.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: An embedded-mode COCOMO project operates under tight hardware, software and operational constraints.  
Statement II: For the same size, basic COCOMO gives the least effort for embedded-mode projects.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Embedded mode has the largest coefficient and exponent, and hence the most effort.

</details>

**Q5.** `High`  
A system has 20 external inputs, 15 external outputs, 10 external inquiries, 5 internal logical files and 3 external interface files, all of average complexity (weights 4, 5, 4, 10 and 7). The unadjusted function point count is

(1) 300  
(2) 342  
(3) 266  
(4) 228  

<details><summary>Answer</summary>

**(3)** — 20 × 4 + 15 × 5 + 10 × 4 + 5 × 10 + 3 × 7 = 80 + 75 + 40 + 50 + 21 = 266.

</details>

**Q6.** `High`  
A system has 266 unadjusted function points, and the sum of the 14 value adjustment factors (ΣFi) is 42. The adjusted function point count is approximately

(1) 308  
(2) 359  
(3) 285  
(4) 266  

<details><summary>Answer</summary>

**(3)** — FP = UFP × (0.65 + 0.01 × ΣFi) = 266 × 1.07 ≈ 284.6.

</details>

**Q7.** `High`  
The value adjustment factor in function point analysis, 0.65 + 0.01 × ΣFi with 14 factors each rated 0 to 5, lies in the range

(1) 0.5 to 1.5  
(2) 0.65 to 1.35  
(3) 1 to 2  
(4) 0 to 1  

<details><summary>Answer</summary>

**(2)** — ΣFi ranges from 0 to 70.

</details>

**Q8.** `High`  
Using three-point estimation, a module has optimistic, most likely and pessimistic sizes of 4600, 6900 and 8600 LOC. The expected size is

(1) 6700 LOC  
(2) 6900 LOC  
(3) 7000 LOC  
(4) 6800 LOC  

<details><summary>Answer</summary>

**(4)** — (4600 + 4 × 6900 + 8600) / 6 = 6800 LOC.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Function point component): A. External input  B. External output  C. External inquiry  D. Internal logical file  
List II (Description): I. A logical group of data maintained within the application boundary  II. Data or control information entering the application from outside  III. An input-output combination that retrieves data without derived data  IV. Derived information, such as reports, sent outside the application

(1) A-II, B-III, C-IV, D-I  
(2) A-IV, B-II, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(4)** — External interface files are maintained by other applications.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Function points can be estimated early in the life cycle, before the code is written.  
Reason R: Function points are derived from the requirements (inputs, outputs, inquiries and files), and are independent of the programming language.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — LOC can be known accurately only after coding.

</details>

**Q11.** `High`  
Brooks' law states that

(1) adding manpower to a late software project makes it later  
(2) work expands to fill the time available  
(3) software projects are always on time  
(4) the cost of fixing a defect doubles every phase  

<details><summary>Answer</summary>

**(1)** — New people need training, and communication overhead grows.

</details>

**Q12.** `Medium`  
The number of communication paths among a team of 10 developers is

(1) 45  
(2) 10  
(3) 100  
(4) 20  

<details><summary>Answer</summary>

**(1)** — n(n − 1)/2 = 45; this growth in paths is one reason behind Brooks' law.

</details>

**Q13.** `High`  
In earned value analysis, BCWS = 100, BCWP = 80 and ACWP = 90 (in thousands). The schedule performance index (SPI) and cost performance index (CPI) are

(1) 1.25 and 1.13  
(2) 0.8 and 1.13  
(3) 0.8 and 0.89  
(4) 0.89 and 0.8  

<details><summary>Answer</summary>

**(3)** — SPI = BCWP / BCWS = 0.8 (behind schedule); CPI = BCWP / ACWP ≈ 0.89 (over budget).

</details>

**Q14.** `Medium`  
In earned value analysis, the schedule variance (SV) and cost variance (CV) are defined as

(1) BCWS − BCWP and ACWP − BCWP  
(2) ACWP − BCWS and BCWP − ACWP  
(3) BCWS − ACWP and BCWP − BCWS  
(4) BCWP − BCWS and BCWP − ACWP  

<details><summary>Answer</summary>

**(4)** — Negative values indicate being behind schedule or over budget.

</details>

**Q15.** `High`  
In a project network, activity A (3 days) precedes B (4 days) and C (2 days); B precedes D (5 days); C precedes E (6 days); D and E precede F (2 days). The length of the critical path is

(1) 16 days  
(2) 12 days  
(3) 14 days  
(4) 13 days  

<details><summary>Answer</summary>

**(3)** — A–B–D–F takes 3 + 4 + 5 + 2 = 14 days; A–C–E–F takes 13 days.

</details>

**Q16.** `Medium`  
In the project network where A (3) precedes B (4) and C (2), B precedes D (5), C precedes E (6), and D and E precede F (2), the slack (float) of activity C is

(1) 0 days  
(2) 3 days  
(3) 2 days  
(4) 1 day  

<details><summary>Answer</summary>

**(4)** — C lies on the path A–C–E–F of 13 days, one day shorter than the critical path.

</details>

**Q17.** `Medium`  
The 40-20-40 rule of effort distribution assigns

(1) 40% to coding  
(2) 40% to maintenance  
(3) 40% to front-end analysis and design, 20% to coding and 40% to testing  
(4) equal effort to all phases  

<details><summary>Answer</summary>

**(3)** — It is a rough guideline for distributing development effort.

</details>

**Q18.** `Medium`  
Given below are two statements.  
Statement I: In the Putnam (SLIM) model, effort is very sensitive to the delivery time, varying inversely with its fourth power.  
Statement II: The Putnam model is based on the Rayleigh-Norden curve of staffing.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Compressing the schedule therefore increases effort sharply.

</details>

**Q19.** `Medium`  
Intermediate COCOMO refines basic COCOMO by multiplying the nominal effort by

(1) the number of function points  
(2) the number of developers  
(3) a constant of 2  
(4) an effort adjustment factor computed from 15 cost drivers  

<details><summary>Answer</summary>

**(4)** — Cost drivers cover product, hardware, personnel and project attributes.

</details>

**Q20.** `Medium`  
COCOMO II defines three sub-models, namely

(1) waterfall, spiral and agile  
(2) organic, semi-detached and embedded  
(3) basic, intermediate and detailed  
(4) application composition, early design and post-architecture  

<details><summary>Answer</summary>

**(4)** — The application composition model uses object points.

</details>

**Q21.** `Medium`  
A project of 33,200 LOC is estimated with an average productivity of 620 LOC per person-month. The estimated effort is about

(1) 80 PM  
(2) 62 PM  
(3) 54 PM  
(4) 33 PM  

<details><summary>Answer</summary>

**(3)** — 33,200 / 620 ≈ 53.5 person-months.

</details>

**Q22.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Lines-of-code measures are language-dependent.  
Reason R: Function points are measured in lines of code.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Function points are language-independent measures of functionality; LOC depends on the language because the same function takes different numbers of lines.

</details>

**Q23.** `Medium`  
A Gantt chart (timeline chart) shows

(1) the tasks of a project as horizontal bars against a time axis  
(2) the data flow  
(3) the class structure  
(4) the risk table  

<details><summary>Answer</summary>

**(1)** — PERT/CPM networks show the dependencies between tasks.

</details>

**Q24.** `Medium`  
PERT estimates the expected duration of an activity as

(1) (o + m + p)/3  
(2) (o + 4m + p)/6  
(3) (o + 2m + p)/4  
(4) m  

<details><summary>Answer</summary>

**(2)** — o is optimistic, m most likely and p pessimistic time.

</details>

**Q25.** `Medium`  
The wideband Delphi technique is used for

(1) expert-judgment-based estimation through anonymous rounds of estimates and discussion  
(2) configuration management  
(3) coding  
(4) testing  

<details><summary>Answer</summary>

**(1)** — Estimates converge over several rounds.

</details>

**Q26.** `Medium`  
For a vocabulary of n1 = 10 distinct operators and n2 = 7 distinct operands, with N1 = 16 and N2 = 15 total occurrences, the Halstead program volume V = N log2 n is approximately

(1) 155  
(2) 180  
(3) 127  
(4) 100  

<details><summary>Answer</summary>

**(3)** — N = 31 and n = 17, so V = 31 × log2 17 ≈ 126.7.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: Halstead's program length N is the total number of operator and operand occurrences.  
Statement II: Halstead's vocabulary n is the number of distinct operators plus the number of distinct operands.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Both are basic Halstead measures.

</details>

**Q28.** `Medium`  
Given below are two statements.  
Statement I: Activities on the critical path have positive slack.  
Statement II: A work breakdown structure (WBS) divides the project into a hierarchy of smaller, manageable tasks.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Critical-path activities have zero slack; any delay in them delays the project.

</details>

**Q29.** `Low`  
KLOC stands for

(1) key lines of code  
(2) known lines of code  
(3) kernel lines of code  
(4) kilo (thousand) lines of code  

<details><summary>Answer</summary>

**(4)** — Effort is often expressed in person-months per KLOC.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: In basic COCOMO, effort grows linearly with size for every mode.  
Statement II: In basic COCOMO, development time grows faster than effort.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — The exponents above 1 make effort grow faster than size, and time grows much more slowly than effort.

</details>
