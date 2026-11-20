# Set 7 — Output Primitives: Line Drawing (DDA, Bresenham), Mid-Point Circle and Ellipse, Polygon Filling

**23 questions** — High: 10, Medium: 12, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Using Bresenham's line algorithm from (20, 10) to (30, 18), the initial decision parameter p0 = 2Δy − Δx is

(1) 2  
(2) 8  
(3) 16  
(4) 6  

<details><summary>Answer</summary>

**(4)** — Δx = 10 and Δy = 8, so p0 = 16 − 10 = 6.

</details>

**Q2.** `High`  
Bresenham's line algorithm from (20, 10) to (30, 18) plots which pixel immediately after (22, 12)?

(1) (22, 13)  
(2) (24, 13)  
(3) (23, 13)  
(4) (23, 12)  

<details><summary>Answer</summary>

**(4)** — The decision parameter at that step is −2 &lt; 0, so y does not change: (23, 12).

</details>

**Q3.** `High`  
For a line from (20, 10) to (30, 18) drawn with Bresenham's algorithm, the number of pixels plotted, including both endpoints, is

(1) 18  
(2) 10  
(3) 8  
(4) 11  

<details><summary>Answer</summary>

**(4)** — For a gentle slope, one pixel is plotted for each x from 20 to 30.

</details>

**Q4.** `High`  
Using the DDA algorithm with rounding (0.5 rounded up) for the line from (2, 3) to (12, 8), the first four pixels plotted are

(1) (2, 3), (3, 3.5), (4, 4), (5, 4.5)  
(2) (2, 3), (3, 4), (4, 4), (5, 5)  
(3) (2, 3), (3, 3), (4, 4), (5, 4)  
(4) (2, 3), (4, 4), (6, 5), (8, 6)  

<details><summary>Answer</summary>

**(2)** — The slope is 0.5, so y increases by 0.5 per step: 3.5 rounds to 4, 4.0 stays 4, 4.5 rounds to 5.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: The DDA algorithm uses floating-point arithmetic and rounding at each step.  
Statement II: Bresenham's line algorithm uses only integer addition, subtraction and multiplication by 2.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — This is why Bresenham's algorithm is faster and better suited to hardware.

</details>

**Q6.** `High`  
In the mid-point circle algorithm for radius r, the initial decision parameter p0 is

(1) 1 − r (that is, 5/4 − r rounded)  
(2) 2r − 1  
(3) r  
(4) r²  

<details><summary>Answer</summary>

**(1)** — For r = 10, p0 = −9.

</details>

**Q7.** `High`  
Using the mid-point circle algorithm for radius 10 centred at the origin, the pixels computed in the first octant are

(1) (0, 10), (1, 9), (2, 8), (3, 7), (4, 6), (5, 5)  
(2) (0, 10), (2, 10), (4, 9), (6, 8), (7, 7)  
(3) (0, 10), (1, 10), (2, 10), (3, 10), (4, 9), (5, 9), (6, 8), (7, 7)  
(4) (0, 10), (1, 10), (2, 9), (3, 9), (4, 8), (5, 8), (6, 7), (7, 7)  

<details><summary>Answer</summary>

**(3)** — This is the standard example in Hearn and Baker.

</details>

**Q8.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The mid-point circle algorithm computes points for only one octant.  
Reason R: A circle is symmetric only about the x-axis.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — A circle is symmetric in all eight octants, which is why one octant suffices.

</details>

**Q9.** `Medium`  
For the mid-point ellipse algorithm with rx = 8 and ry = 6, the initial decision parameter in region 1, p1(0) = ry² − rx² ry + rx²/4, is

(1) 332  
(2) −300  
(3) −332  
(4) −348  

<details><summary>Answer</summary>

**(3)** — 36 − 384 + 16 = −332.

</details>

**Q10.** `Medium`  
The mid-point ellipse algorithm divides the first quadrant into two regions according to

(1) whether the slope of the curve is less than or greater than −1 in magnitude  
(2) the sign of x  
(3) the radius  
(4) the colour of the pixels  

<details><summary>Answer</summary>

**(1)** — In region 1 x is stepped; in region 2, y is stepped.

</details>

**Q11.** `Medium`  
An ellipse has symmetry in

(1) 2 halves only  
(2) 8 octants  
(3) no symmetry  
(4) 4 quadrants  

<details><summary>Answer</summary>

**(4)** — Unlike a circle, an ellipse is not symmetric about the line y = x.

</details>

**Q12.** `High`  
Match List I with List II.  
List I (Fill algorithm or test): A. Scan-line polygon fill  B. Boundary fill  C. Flood fill  D. Odd-even rule  
List II (Idea): I. Fills an interior region of a uniform colour, replacing it with a new colour  II. Starts at an interior point and fills outward until the boundary colour is reached  III. A point is inside if a ray from it crosses the boundary an odd number of times  IV. Finds intersections of each scan line with polygon edges and fills between pairs

(1) A-II, B-IV, C-I, D-III  
(2) A-IV, B-II, C-III, D-I  
(3) A-IV, B-II, C-I, D-III  
(4) A-IV, B-I, C-II, D-III  

<details><summary>Answer</summary>

**(3)** — The non-zero winding-number rule is another inside-outside test.

</details>

**Q13.** `High`  
Given below are two statements.  
Statement I: A 4-connected boundary fill can leak through diagonal gaps in a boundary that an 8-connected fill would not.  
Statement II: An 8-connected fill tests the four diagonal neighbours in addition to the four horizontal and vertical neighbours.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — An 8-connected fill is the one that can leak through diagonal gaps; Statement I reverses the roles.

</details>

**Q14.** `Medium`  
In the scan-line polygon fill algorithm, the data structure that holds the edges intersected by the current scan line is the

(1) frame buffer  
(2) z-buffer  
(3) active edge table (active edge list)  
(4) edge table (sorted edge table)  

<details><summary>Answer</summary>

**(3)** — The sorted edge table holds all edges, bucketed by their minimum y.

</details>

**Q15.** `Medium`  
In the scan-line polygon fill algorithm, a vertex where the two edges lie on opposite sides of the scan line is

(1) counted twice  
(2) counted once (often by shortening one of the edges)  
(3) filled with the boundary colour  
(4) ignored  

<details><summary>Answer</summary>

**(2)** — A vertex at a local extremum (both edges on the same side) is counted twice.

</details>

**Q16.** `Medium`  
The number of pixels plotted by a DDA or Bresenham algorithm for a line from (x1, y1) to (x2, y2) is

(1) 1  
(2) (x2 − x1)(y2 − y1)  
(3) |x2 − x1| + |y2 − y1|  
(4) max(|x2 − x1|, |y2 − y1|) + 1  

<details><summary>Answer</summary>

**(4)** — One pixel per unit step along the major axis, plus the starting pixel.

</details>

**Q17.** `Medium`  
Using Bresenham's algorithm from (0, 0) to (8, 4), the initial decision parameter is

(1) 4  
(2) 8  
(3) 0  
(4) −8  

<details><summary>Answer</summary>

**(3)** — p0 = 2Δy − Δx = 8 − 8 = 0.

</details>

**Q18.** `Medium`  
Using the mid-point circle algorithm for radius 8, the initial decision parameter is

(1) −8  
(2) 1  
(3) 7  
(4) −7  

<details><summary>Answer</summary>

**(4)** — p0 = 1 − r.

</details>

**Q19.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Recursive flood-fill algorithms can overflow the stack for large regions.  
Reason R: Each pixel may generate several recursive calls that remain pending.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Scan-line (span) fill methods reduce the stack depth.

</details>

**Q20.** `Medium`  
Antialiasing techniques such as supersampling and area sampling are used to

(1) compress images  
(2) speed up line drawing  
(3) increase resolution in hardware  
(4) reduce the jagged appearance of lines and edges  

<details><summary>Answer</summary>

**(4)** — Pixel intensities are adjusted according to how much of the pixel the line covers.

</details>

**Q21.** `Low`  
Scan conversion is the process of

(1) compressing images  
(2) converting colour to grayscale  
(3) converting an analog image to digital  
(4) converting a geometric primitive, such as a line or circle, into a set of pixels  

<details><summary>Answer</summary>

**(4)** — It is also called rasterization.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: The non-zero winding number rule and the odd-even rule always give the same result.  
Statement II: For self-intersecting polygons, the two rules can classify some regions differently.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — For a five-pointed star, the central pentagon is outside by the odd-even rule but inside by the non-zero rule.

</details>

**Q23.** `Medium`  
In the DDA algorithm for a line with slope m where |m| ≤ 1, at each step

(1) x is incremented by m  
(2) x is incremented by 1 and y by m  
(3) y is incremented by 1 and x by 1/m  
(4) both x and y are incremented by 1  

<details><summary>Answer</summary>

**(2)** — For |m| &gt; 1, y is incremented by 1 and x by 1/m.

</details>
