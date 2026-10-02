# Paper 1 · Unit 5 — Mathematical Reasoning & Aptitude

**Expected questions: ~5 (10 marks) · Target: 5/5 (pure practice unit)**

## Syllabus Checklist
- [ ] Types of reasoning
- [ ] Number series, letter series, codes
- [ ] Relationships (blood relations)
- [ ] Classification
- [ ] Mathematical aptitude: fraction, time & distance, ratio, proportion, percentage, profit & loss,
      interest & discounting, averages

---

## 1. Number Series — Pattern Checklist

```mermaid
flowchart TD
    A[Given series] --> B{Differences constant?}
    B -->|Yes| AP[Arithmetic progression]
    B -->|No| C{Second differences constant?}
    C -->|Yes| Q[Quadratic pattern]
    C -->|No| D{Ratios constant?}
    D -->|Yes| GP[Geometric progression]
    D -->|No| E{Squares / cubes ± k?}
    E -->|Yes| SC[n² ± k, n³ ± k]
    E -->|No| F{Alternate terms?}
    F -->|Yes| ALT[Two interleaved series]
    F -->|No| G[Mixed: ×a+b, primes, Fibonacci]
```

Examples:
- 2, 6, 12, 20, 30, **42** → n(n+1)
- 3, 7, 15, 31, 63, **127** → ×2 + 1
- 1, 8, 27, 64, **125** → n³
- 2, 3, 5, 7, 11, **13** → primes
- 1, 1, 2, 3, 5, 8, **13** → Fibonacci
- 4, 9, 25, 49, 121, **169** → squares of primes
- 1, 2, 6, 24, 120, **720** → ×2, ×3, ×4 … (factorials)

## 2. Letter Series & Coding

Position table (memorise both directions):
```
A B C D E F G H I J K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
Z Y X W V U T S R Q P  O  N  M  L  K  J  I  H  G  F  E  D  C  B  A   (reverse)
```
Trick: **EJOTY** = 5, 10, 15, 20, 25. Opposite pairs sum to 27 (A↔Z, M↔N).

- Coding: If CAT → DBU (+1 each), then DOG → **EPH**.
- If CAT = 24 (3+1+20), then DOG = 4+15+7 = **26**.
- Reverse coding: CAT → XZG (opposite letters).

## 3. Blood Relations

Use a **family tree diagram** with symbols:
```
  +  male    −  female    ═  married    │ parent-child    ─ siblings

  Example: "A is the brother of B. B is the daughter of C. C is the husband of D."
              C(+) ═ D(−)
                  │
           ┌──────┴──────┐
         A(+)          B(−)
   → D is A's MOTHER.
```
Coded relations: "P + Q means P is father of Q; P × Q means P is sister of Q" → draw step-by-step.

## 4. Classification (Odd one out)
Find the common property in 3 of 4: primes, squares, multiples, vowels, same-category items.
Example: 121, 144, 169, **190** → 190 is not a perfect square.

## 5. Arithmetic Aptitude — Formula Bank

### Percentage
```
x% of y = y% of x
Increase by a% then b% ⇒ net = a + b + ab/100
If price ↑ r%, consumption must ↓ by r/(100+r) × 100 % to keep expenditure same
Successive discount d1, d2 ⇒ d1 + d2 − d1·d2/100
```

### Profit & Loss
```
Profit% = (SP − CP)/CP × 100
SP = CP × (100 + P%)/100
Marked price M, discount d% ⇒ SP = M(100 − d)/100
Two items sold at same SP, one at x% gain, other at x% loss ⇒ always LOSS of x²/100 %
Dishonest dealer (uses 900g for 1kg) ⇒ gain = 100/900 × 100 = 11.11%
```

### Simple & Compound Interest
```
SI = P·R·T/100
CI: A = P(1 + R/100)^T ;  CI = A − P
CI − SI for 2 yrs = P(R/100)²
CI − SI for 3 yrs = P(R/100)²(3 + R/100)
Money doubles in T years at SI ⇒ R = 100/T
```

### Ratio, Proportion, Averages
```
a : b = c : d  ⇒ ad = bc
Mean proportional of a, b = √(ab);  Third proportional to a, b = b²/a
Average = Sum / Count
If one value replaced changes average by d over n items ⇒ change in value = n·d
Average speed (equal distances) = 2xy/(x + y)
```

### Time, Speed, Distance
```mermaid
flowchart LR
    D[Distance] --- S[Speed × Time]
    K[km/h → m/s : × 5/18] --- M[m/s → km/h : × 18/5]
```
- Relative speed: same direction **(a − b)**, opposite direction **(a + b)**.
- Train crossing pole: time = L / S; crossing platform: (L + P) / S.
- Boats: downstream = u + v, upstream = u − v; still water speed = (D + U)/2, stream = (D − U)/2.

### Time & Work
```
A does work in a days, B in b days ⇒ together = ab/(a + b) days
Pipes: inlet +, outlet − (rates add)
M1·D1·H1 / W1 = M2·D2·H2 / W2
```

## Worked Examples

1. A price rises 20% then falls 20%. Net? → 20 − 20 − 400/100 = **−4%** (loss).
2. ₹5000 at 10% CI for 2 yrs: CI − SI = 5000 × (0.1)² = **₹50**.
3. A car goes at 40 km/h and returns at 60 km/h. Average speed = 2×40×60/100 = **48 km/h**.
4. A can finish in 10 days, B in 15. Together = 150/25 = **6 days**.
5. Two articles each sold at ₹990, one at 10% profit, another at 10% loss. → **1% loss**.

---

## Previous Year Questions (PYQ pattern)

1. Next term: 2, 5, 10, 17, 26, ? → **37** (n² + 1)
2. Next term: 1, 4, 9, 16, 25, ? → **36**
3. Missing: 3, 12, 48, ?, 768 → **192** (×4)
4. Next: 6, 11, 21, 36, 56, ? → **81** (diffs 5,10,15,20,25)
5. Letter series: AZ, BY, CX, ? → **DW**
6. If TEACHER is coded as VGCEJGT (+2), then STUDENT → **UVWFGPV**
7. If PEN = 35 (16+5+14), INK = ? → 9+14+11 = **34**
8. Pointing to a photograph, a man says, "Her mother is the only daughter of my mother." The man is the girl's: **Maternal uncle**
9. A is B's sister, C is B's mother, D is C's father, E is D's mother. A is E's: **Great-granddaughter**
10. Odd one out: 27, 64, 125, 144 → **144** (not a cube)
11. A shopkeeper marks 25% above CP and allows 10% discount. Gain% = 1.25 × 0.9 = 1.125 → **12.5%**
12. A sum doubles in 8 years at SI. Rate = **12.5%**
13. A train 150 m long passes a pole in 15 s. Speed = 10 m/s = **36 km/h**
14. Average of 5 numbers is 20; one number removed, average becomes 18. Removed number = 100 − 72 = **28**
15. Ratio of A:B = 2:3, B:C = 4:5. A:B:C = **8:12:15**
16. If the population increases 10% annually, from 10000 after 2 years: **12100**
17. Salary increased by 25%; by what % must it be reduced to restore? 25/125 × 100 = **20%**
18. Two trains 120 m and 180 m at 50 & 40 km/h opposite directions. Time to cross = 300 / (90×5/18) = 300/25 = **12 s**

## Quick Revision Box
- Net % change = a + b + ab/100 · Same SP, ±x% ⇒ loss x²/100 %
- CI−SI (2 yr) = P(R/100)² · Avg speed = 2xy/(x+y)
- EJOTY = 5,10,15,20,25 · Opposite letters sum to 27
