# Set 8 — 2-D Geometric Transformations (translation, scaling, rotation, reflection, shear, homogeneous coordinates, composite transforms)

**24 questions** — High: 10, Medium: 13, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Rotating the point (3, 4) counter-clockwise by 90° about the origin gives

(1) (−4, 3)  
(2) (4, 3)  
(3) (4, −3)  
(4) (−3, −4)  

<details><summary>Answer</summary>

**(1)** — x' = x cos θ − y sin θ = −4; y' = x sin θ + y cos θ = 3.

</details>

**Q2.** `High`  
Rotating the point (2, 0) counter-clockwise by 30° about the origin gives approximately

(1) (1.732, 1)  
(2) (1.732, −1)  
(3) (2, 1)  
(4) (1, 1.732)  

<details><summary>Answer</summary>

**(1)** — (2 cos 30°, 2 sin 30°) = (1.732, 1).

</details>

**Q3.** `High`  
Rotating the point (4, 2) counter-clockwise by 90° about the pivot point (2, 2) gives

(1) (0, 2)  
(2) (−2, 4)  
(3) (2, 4)  
(4) (4, 4)  

<details><summary>Answer</summary>

**(3)** — Translate by (−2, −2) to get (2, 0), rotate to (0, 2), and translate back to (2, 4).

</details>

**Q4.** `High`  
Scaling the point (3, 3) by a factor of 2 in both directions about the fixed point (2, 2) gives

(1) (6, 6)  
(2) (5, 5)  
(3) (8, 8)  
(4) (4, 4)  

<details><summary>Answer</summary>

**(4)** — x' = 2 + 2 × (3 − 2) = 4, and likewise y' = 4.

</details>

**Q5.** `High`  
Match List I with List II.  
List I (Reflection of the point (3, 4)): A. About the x-axis  B. About the y-axis  C. About the line y = x  D. About the origin  
List II (Result): I. (4, 3)  II. (3, −4)  III. (−3, −4)  IV. (−3, 4)

(1) A-II, B-IV, C-I, D-III  
(2) A-IV, B-II, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(1)** — Reflection about y = −x gives (−4, −3).

</details>

**Q6.** `High`  
An x-direction shear with shear factor shx = 2 maps the point (1, 1) to

(1) (2, 2)  
(2) (3, 1)  
(3) (3, 3)  
(4) (1, 3)  

<details><summary>Answer</summary>

**(2)** — x' = x + shx × y = 3; y' = y.

</details>

**Q7.** `Medium`  
A y-direction shear with shear factor shy = 3 maps the point (2, 1) to

(1) (5, 1)  
(2) (2, 7)  
(3) (8, 1)  
(4) (2, 4)  

<details><summary>Answer</summary>

**(2)** — y' = y + shy × x = 1 + 6 = 7; x' = x.

</details>

**Q8.** `High`  
Homogeneous coordinates are used in 2-D graphics mainly so that

(1) curves can be drawn  
(2) translation, as well as rotation and scaling, can be represented as a matrix multiplication, allowing composite transformations to be combined into one matrix  
(3) the image can be stored in less memory  
(4) colours can be represented  

<details><summary>Answer</summary>

**(2)** — A 2-D point (x, y) becomes (x, y, 1), and transformations become 3 × 3 matrices.

</details>

**Q9.** `High`  
Given below are two statements.  
Statement I: Matrix multiplication of 2-D transformations is always commutative.  
Statement II: Translation cannot be written as a matrix multiplication even in homogeneous coordinates.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — Composite transformations are generally not commutative, and homogeneous coordinates exist precisely so that translation becomes a matrix product.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Two successive translations are multiplicative.  
Reason R: T(tx1, ty1) · T(tx2, ty2) = T(tx1 + tx2, ty1 + ty2).

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — R shows that successive translations are additive; successive scalings are multiplicative.

</details>

**Q11.** `High`  
The composite transformation for rotation by θ about an arbitrary pivot point (xr, yr) is

(1) T(xr, yr) · R(θ) · T(−xr, −yr)  
(2) T(−xr, −yr) · R(θ) · T(xr, yr)  
(3) R(θ) only  
(4) R(θ) · T(xr, yr)  

<details><summary>Answer</summary>

**(1)** — Applied right to left: move the pivot to the origin, rotate, then move back.

</details>

**Q12.** `Medium`  
The inverse of a rotation matrix R(θ) is

(1) the identity matrix  
(2) undefined  
(3) R(θ) itself  
(4) its transpose, R(−θ)  

<details><summary>Answer</summary>

**(4)** — Rotation matrices are orthogonal with determinant 1.

</details>

**Q13.** `Medium`  
The 3 × 3 homogeneous matrix for translation by (tx, ty) has tx and ty in

(1) the last column (first two rows), with the remaining part being the identity  
(2) every entry  
(3) the last row  
(4) the diagonal  

<details><summary>Answer</summary>

**(1)** — Using column vectors, [x', y', 1] = T · [x, y, 1].

</details>

**Q14.** `Medium`  
Given below are two statements.  
Statement I: Uniform scaling preserves the shape (angles) of an object.  
Statement II: Differential (non-uniform) scaling always preserves the shape of an object.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Non-uniform scaling distorts shapes, for example turning a circle into an ellipse.

</details>

**Q15.** `Medium`  
A scaling transformation with scale factors less than 1

(1) enlarges the object and moves it away from the origin  
(2) reduces the object and moves it closer to the coordinate origin  
(3) reflects the object  
(4) rotates the object  

<details><summary>Answer</summary>

**(2)** — Scaling about the origin also changes the object's position unless a fixed point is used.

</details>

**Q16.** `Medium`  
Reflection about the line y = x is equivalent to

(1) a rotation of 90°  
(2) a translation  
(3) a shear  
(4) a reflection about the x-axis followed by a counter-clockwise rotation of 90°  

<details><summary>Answer</summary>

**(4)** — Its matrix swaps the x and y coordinates.

</details>

**Q17.** `Medium`  
Rotating the point (1, 0) counter-clockwise by 45° about the origin gives approximately

(1) (1, 1)  
(2) (0.5, 0.5)  
(3) (0.707, 0.707)  
(4) (0.707, −0.707)  

<details><summary>Answer</summary>

**(3)** — (cos 45°, sin 45°).

</details>

**Q18.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A rigid-body transformation preserves distances and angles.  
Reason R: A rigid-body transformation consists only of rotations, translations and reflections.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Scaling and shear are not rigid-body transformations.

</details>

**Q19.** `Medium`  
The determinant of a 2-D rotation matrix is

(1) 1  
(2) 0  
(3) cos θ  
(4) −1  

<details><summary>Answer</summary>

**(1)** — Rotations preserve area and orientation.

</details>

**Q20.** `Medium`  
Transforming an object from one Cartesian coordinate system to another, whose origin is at (x0, y0) and whose axes are rotated by θ, is done by

(1) S(θ) only  
(2) R(−θ) · T(−x0, −y0)  
(3) R(θ) · T(x0, y0)  
(4) T(x0, y0) · R(θ)  

<details><summary>Answer</summary>

**(2)** — First translate the new origin to the old origin, then rotate the axes to align them.

</details>

**Q21.** `Medium`  
The matrix [[1, 0, 0], [0, −1, 0], [0, 0, 1]] in homogeneous coordinates represents

(1) reflection about the x-axis  
(2) rotation by 90°  
(3) reflection about the y-axis  
(4) scaling by −1  

<details><summary>Answer</summary>

**(1)** — It negates the y-coordinate.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: Shear transformations change the area of an object.  
Statement II: An affine transformation preserves parallel lines.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A shear matrix has determinant 1, so it preserves area while distorting shape.

</details>

**Q23.** `Low`  
In 2-D, a translation moves every point of an object by

(1) a reflection  
(2) a scale factor  
(3) a fixed angle  
(4) the same distance in a given direction  

<details><summary>Answer</summary>

**(4)** — It is a rigid-body transformation.

</details>

**Q24.** `Medium`  
Scaling an object with sx = 2 and sy = 1 about the origin transforms a unit square with corners (0, 0) and (1, 1) into a rectangle with area

(1) 1  
(2) 4  
(3) 3  
(4) 2  

<details><summary>Answer</summary>

**(4)** — The area is multiplied by |sx × sy| = 2.

</details>
