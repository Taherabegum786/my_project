# Set 9 — 2-D Viewing (window-to-viewport mapping, viewing pipeline) and Line and Polygon Clipping

**20 questions** — High: 9, Medium: 10, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
A window with corners (0, 0) and (10, 10) is mapped to a viewport with corners (100, 100) and (300, 300). The point (5, 5) maps to

(1) (150, 150)  
(2) (105, 105)  
(3) (250, 250)  
(4) (200, 200)  

<details><summary>Answer</summary>

**(4)** — sx = sy = 200 / 10 = 20; x' = 100 + (5 − 0) × 20 = 200.

</details>

**Q2.** `High`  
A window with corners (10, 10) and (50, 60) is mapped to the normalised viewport (0, 0) to (1, 1). The point (20, 30) maps to

(1) (0.4, 0.25)  
(2) (0.5, 0.5)  
(3) (0.25, 0.4)  
(4) (0.2, 0.3)  

<details><summary>Answer</summary>

**(3)** — x' = (20 − 10) / 40 = 0.25; y' = (30 − 10) / 50 = 0.4.

</details>

**Q3.** `High`  
In the window-to-viewport transformation, the scaling factor in x is

(1) (xvmax − xvmin) / (xwmax − xwmin)  
(2) xvmax / xwmax  
(3) xwmin / xvmin  
(4) (xwmax − xwmin) / (xvmax − xvmin)  

<details><summary>Answer</summary>

**(1)** — If sx ≠ sy, the object is distorted.

</details>

**Q4.** `High`  
In the Cohen-Sutherland algorithm with region-code bits ordered Top, Bottom, Right, Left, and a clip window from (0, 0) to (10, 10), the region code of the point (−3, 15) is

(1) 1001  
(2) 0110  
(3) 1010  
(4) 0101  

<details><summary>Answer</summary>

**(1)** — The point is above the window (top bit) and to its left (left bit).

</details>

**Q5.** `High`  
In the Cohen-Sutherland algorithm with bits ordered Top, Bottom, Right, Left and a clip window from (0, 0) to (10, 10), the region code of the point (12, 5) is

(1) 0100  
(2) 1000  
(3) 0001  
(4) 0010  

<details><summary>Answer</summary>

**(4)** — It lies only to the right of the window.

</details>

**Q6.** `High`  
Given below are two statements.  
Statement I: In Cohen-Sutherland clipping, a line is trivially accepted if both endpoint codes are 0000.  
Statement II: In Cohen-Sutherland clipping, a line is trivially rejected if the logical OR of the endpoint codes is non-zero.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The test for trivial rejection is a non-zero logical AND, meaning both endpoints are outside the same edge.

</details>

**Q7.** `High`  
A line from (−5, 3) to (15, 9) is clipped against the window (0, 0)–(10, 10) by the Liang-Barsky algorithm. The parameter values u1 and u2 of the visible part are

(1) 0.25 and 1  
(2) 0.25 and 0.75  
(3) 0 and 1  
(4) 0.5 and 1  

<details><summary>Answer</summary>

**(2)** — The line enters at x = 0 (u = 5/20) and leaves at x = 10 (u = 15/20); the clipped segment is (0, 4.5) to (10, 7.5).

</details>

**Q8.** `High`  
Match List I with List II.  
List I (Clipping algorithm): A. Cohen-Sutherland  B. Liang-Barsky  C. Sutherland-Hodgman  D. Weiler-Atherton  
List II (Characteristic): I. Polygon clipping that also handles concave polygons correctly by following boundaries  II. Line clipping using 4-bit region codes  III. Polygon clipping against each edge of a convex window in turn  IV. Line clipping using the parametric line equation, generally more efficient

(1) A-II, B-IV, C-III, D-I  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-III, C-IV, D-I  
(4) A-IV, B-II, C-III, D-I  

<details><summary>Answer</summary>

**(1)** — Standard 2-D clipping algorithms.

</details>

**Q9.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The Sutherland-Hodgman algorithm can produce extraneous connecting edges when clipping a concave polygon.  
Reason R: Sutherland-Hodgman outputs a single vertex list, so separate visible pieces are joined along the window boundary.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — The Weiler-Atherton algorithm avoids this problem.

</details>

**Q10.** `Medium`  
In the Sutherland-Hodgman algorithm, when an edge goes from a vertex inside the clip boundary to a vertex outside it, the algorithm outputs

(1) only the intersection point with the boundary  
(2) both vertices  
(3) nothing  
(4) only the inside vertex  

<details><summary>Answer</summary>

**(1)** — Inside to inside outputs the second vertex; outside to inside outputs the intersection and the second vertex; outside to outside outputs nothing.

</details>

**Q11.** `Medium`  
Arrange the 2-D viewing pipeline stages in order.  
A. Normalised coordinates  B. Device coordinates  C. Modelling coordinates  D. World coordinates  E. Viewing coordinates

(1) D, C, E, A, B  
(2) C, D, A, E, B  
(3) C, E, D, A, B  
(4) C, D, E, A, B  

<details><summary>Answer</summary>

**(4)** — Clipping is usually performed in normalised coordinates.

</details>

**Q12.** `Medium`  
The region of the scene selected for display is called the

(1) frame buffer  
(2) viewport  
(3) window  
(4) clip code  

<details><summary>Answer</summary>

**(3)** — The viewport is the area of the display device where the window is mapped.

</details>

**Q13.** `Medium`  
Given below are two statements.  
Statement I: Making the viewport smaller while keeping the window fixed shrinks the displayed picture.  
Statement II: Making the window larger while keeping the viewport fixed shows a smaller part of the scene in more detail (zooming in).

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A larger window shows more of the scene at a smaller scale (zooming out).

</details>

**Q14.** `Medium`  
In Cohen-Sutherland clipping with bits Top, Bottom, Right, Left and the window (0, 0)–(10, 10), a line from (−1, −1) to (5, −2) is

(1) clipped against two edges  
(2) trivially accepted  
(3) trivially rejected, because both codes have the bottom bit set  
(4) clipped against the left edge only  

<details><summary>Answer</summary>

**(3)** — The codes are 0101 and 0100; their logical AND, 0100, is non-zero.

</details>

**Q15.** `Medium`  
The Nicholl-Lee-Nicholl line clipping algorithm

(1) avoids multiple clipping of an individual line segment by creating more regions around the window  
(2) clips polygons  
(3) clips curves  
(4) uses region codes only  

<details><summary>Answer</summary>

**(1)** — It needs fewer intersection calculations than Cohen-Sutherland but works only in 2-D.

</details>

**Q16.** `Medium`  
In the Liang-Barsky algorithm, a parameter p\_k = 0 for some boundary means that the line is

(1) parallel to that boundary  
(2) outside the window  
(3) perpendicular to that boundary  
(4) a point  

<details><summary>Answer</summary>

**(1)** — If additionally q\_k &lt; 0, the line is completely outside that boundary.

</details>

**Q17.** `Medium`  
Text clipping strategies include

(1) only polygon clipping  
(2) all-or-none string clipping, all-or-none character clipping and clipping individual characters  
(3) the z-buffer  
(4) only line clipping  

<details><summary>Answer</summary>

**(2)** — They trade accuracy for speed.

</details>

**Q18.** `Low`  
Clipping is the process of

(1) filling a polygon  
(2) scaling an object  
(3) removing the parts of a picture that lie outside a specified region  
(4) rotating an object  

<details><summary>Answer</summary>

**(3)** — The region is usually a rectangular clip window.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: Liang-Barsky clipping generally needs fewer intersection calculations than Cohen-Sutherland clipping.  
Statement II: Cohen-Sutherland clipping can be extended to three dimensions using 6-bit region codes.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — In 3-D, there are six clipping planes, so the codes have six bits.

</details>

**Q20.** `Medium`  
The Weiler-Atherton polygon clipping algorithm differs from Sutherland-Hodgman in that it

(1) cannot clip concave polygons  
(2) processes the polygon edges in random order  
(3) clips only lines  
(4) follows the polygon boundary and switches to the window boundary at exit points, producing separate polygons where needed  

<details><summary>Answer</summary>

**(4)** — It is suitable for arbitrary (including concave) polygons.

</details>
