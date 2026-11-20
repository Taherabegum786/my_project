# Set 10 — 3-D Object Representation, Curves and Surfaces, Projections, Illumination and Rendering

**27 questions** — High: 12, Medium: 14, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
For the cubic Bézier curve with control points P0 (0, 0), P1 (1, 2), P2 (3, 2) and P3 (4, 0), the point at t = 0.5 is

(1) (2, 1.5)  
(2) (2, 1)  
(3) (2, 2)  
(4) (1.5, 2)  

<details><summary>Answer</summary>

**(1)** — B(0.5) = 0.125 P0 + 0.375 P1 + 0.375 P2 + 0.125 P3 = (2, 1.5).

</details>

**Q2.** `Medium`  
For the quadratic Bézier curve with control points (0, 0), (2, 4) and (4, 0), the point at t = 0.5 is

(1) (2, 2)  
(2) (2, 1)  
(3) (2, 4)  
(4) (4, 2)  

<details><summary>Answer</summary>

**(1)** — B(0.5) = 0.25 P0 + 0.5 P1 + 0.25 P2 = (2, 2).

</details>

**Q3.** `High`  
A Bézier curve with n + 1 control points is a polynomial of degree

(1) 2n  
(2) 3 always  
(3) n  
(4) n + 1  

<details><summary>Answer</summary>

**(3)** — Four control points give a cubic Bézier curve.

</details>

**Q4.** `High`  
Which of the following are properties of Bézier curves?  
A. The curve passes through the first and last control points  B. The curve lies within the convex hull of its control points  C. Moving one control point changes the whole curve  D. The degree is independent of the number of control points  
Choose the correct answer from the options given below:

(1) A, B, C and D  
(2) A, B and C only  
(3) A, B and D only  
(4) B, C and D only  

<details><summary>Answer</summary>

**(2)** — D is a property of B-splines, not of Bézier curves.

</details>

**Q5.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: B-spline curves provide local control.  
Reason R: A B-spline curve lies within the convex hull of its control points.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but local control comes from each basis function being non-zero over only a limited parameter range.

</details>

**Q6.** `High`  
Match List I with List II.  
List I (Parallel projection): A. Orthographic  B. Isometric  C. Cavalier  D. Cabinet  
List II (Characteristic): I. Oblique projection in which lines perpendicular to the view plane are drawn at full length  II. Projectors perpendicular to the view plane, showing front, top or side views  III. Oblique projection in which receding lines are drawn at half length  IV. Axonometric projection in which all three axes are equally foreshortened

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-IV, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-I, C-IV, D-III  

<details><summary>Answer</summary>

**(2)** — Dimetric and trimetric are other axonometric projections.

</details>

**Q7.** `High`  
Given below are two statements.  
Statement I: In a perspective projection, objects farther from the viewer appear smaller.  
Statement II: A perspective projection preserves the relative proportions of objects regardless of their distance.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Parallel projection preserves relative proportions; perspective gives realism but not true measurements.

</details>

**Q8.** `High`  
A perspective projection with two vanishing points is called

(1) one-point perspective  
(2) two-point perspective  
(3) parallel projection  
(4) three-point perspective  

<details><summary>Answer</summary>

**(2)** — The number of principal vanishing points equals the number of principal axes cut by the projection plane.

</details>

**Q9.** `High`  
Match List I with List II.  
List I (Shading method): A. Flat (constant) shading  B. Gouraud shading  C. Phong shading  
List II (Method): I. Interpolates surface normals across the polygon and computes intensity at each pixel  II. Uses a single intensity for each polygon  III. Computes intensities at vertices and interpolates them across the polygon

(1) A-I, B-III, C-II  
(2) A-II, B-III, C-I  
(3) A-II, B-I, C-III  
(4) A-III, B-II, C-I  

<details><summary>Answer</summary>

**(2)** — Phong shading renders specular highlights more accurately but costs more.

</details>

**Q10.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Gouraud shading can miss specular highlights that fall inside a polygon.  
Reason R: Gouraud shading computes intensities only at the vertices and linearly interpolates them.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Phong shading interpolates normals instead, so highlights inside polygons appear.

</details>

**Q11.** `High`  
In the basic illumination model, diffuse (Lambertian) reflection is proportional to

(1) cos θ, where θ is the angle between the surface normal and the light direction  
(2) cos^n φ, where φ is the angle between the reflection and viewing directions  
(3) the area of the polygon  
(4) the distance to the viewer  

<details><summary>Answer</summary>

**(1)** — Specular reflection in the Phong model is proportional to cos^n φ.

</details>

**Q12.** `High`  
Match List I with List II.  
List I (Visible-surface method): A. Z-buffer (depth buffer)  B. Painter's (depth-sort) algorithm  C. Back-face detection  D. Warnock's algorithm  
List II (Idea): I. Recursive subdivision of the screen area until each area is simple  II. Removes polygons whose normal faces away from the viewer  III. Stores the depth of the nearest surface at each pixel  IV. Draws polygons from back to front so nearer ones overwrite farther ones

(1) A-III, B-II, C-IV, D-I  
(2) A-III, B-IV, C-II, D-I  
(3) A-IV, B-III, C-II, D-I  
(4) A-III, B-IV, C-I, D-II  

<details><summary>Answer</summary>

**(2)** — Z-buffer is an image-space method; depth sorting combines object and image space.

</details>

**Q13.** `High`  
Given below are two statements.  
Statement I: The z-buffer algorithm requires a depth buffer with one entry per pixel in addition to the frame buffer.  
Statement II: The z-buffer algorithm requires the polygons to be sorted by depth before processing.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The z-buffer processes polygons in any order; that independence from sorting is its main advantage.

</details>

**Q14.** `Medium`  
In back-face detection with a viewing direction V and polygon normal N (outward), a polygon is a back face if

(1) N × V = 0  
(2) N · V &lt; 0 always  
(3) N · V &gt; 0 (when V points from the viewer into the scene)  
(4) N · V = 0 always  

<details><summary>Answer</summary>

**(3)** — Conventions differ; with V pointing from the surface towards the viewer, back faces have N · V &lt; 0.

</details>

**Q15.** `Medium`  
Which of the following is a quadric surface?

(1) Bézier patch  
(2) Sphere  
(3) Plane  
(4) Polygon mesh  

<details><summary>Answer</summary>

**(2)** — Quadric surfaces (sphere, ellipsoid, torus, paraboloid, hyperboloid) are described by second-degree equations.

</details>

**Q16.** `Medium`  
Given below are two statements.  
Statement I: Interpolation splines pass through all their control points.  
Statement II: Approximation splines, such as Bézier and B-spline curves, generally do not pass through all their control points.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Cubic Bézier curves pass only through the first and last control points.

</details>

**Q17.** `Medium`  
C1 (first-order parametric) continuity between two curve sections means that

(1) the curves are straight lines  
(2) the curves meet and their first derivatives (tangent vectors) are equal at the joint  
(3) the curves have the same colour  
(4) the curves meet at a common point only  

<details><summary>Answer</summary>

**(2)** — C0 continuity means only that the curves meet; C2 also matches second derivatives.

</details>

**Q18.** `Medium`  
Arrange the 3-D viewing pipeline stages in order.  
A. Projection transformation  B. Modelling transformation  C. Viewing transformation  D. Workstation (viewport) transformation

(1) C, B, A, D  
(2) B, C, A, D  
(3) A, B, C, D  
(4) B, A, C, D  

<details><summary>Answer</summary>

**(2)** — Modelling to world coordinates, world to viewing, projection, then mapping to the device.

</details>

**Q19.** `Medium`  
A polygon mesh is often stored using

(1) a vertex table, an edge table and a polygon (surface-facet) table  
(2) a z-buffer  
(3) a colour table  
(4) only a frame buffer  

<details><summary>Answer</summary>

**(1)** — Geometric tables are supplemented by attribute tables for colour and transparency.

</details>

**Q20.** `Medium`  
NURBS stands for

(1) Normal Uniform Rendering Basis Surfaces  
(2) Non-Uniform Raster Bitmap Shapes  
(3) Non-Uniform Rational B-Splines  
(4) New Uniform Ray-traced B-Surfaces  

<details><summary>Answer</summary>

**(3)** — NURBS can represent conic sections such as circles exactly.

</details>

**Q21.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Ray tracing can produce reflections, refractions and shadows realistically.  
Reason R: Ray tracing follows rays from the eye through each pixel into the scene and recursively traces reflected and refracted rays.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — It is computationally expensive.

</details>

**Q22.** `Medium`  
In the 3-D homogeneous representation, a point (x, y, z) is written as

(1) (x, y, 1)  
(2) (x, y, z)  
(3) (1, x, y, z)  
(4) (x, y, z, 1)  

<details><summary>Answer</summary>

**(4)** — 3-D transformations are then 4 × 4 matrices.

</details>

**Q23.** `Medium`  
The 3-D rotation of a point about the z-axis by θ

(1) is a translation  
(2) changes x and y as in 2-D rotation and leaves z unchanged  
(3) changes only the z-coordinate  
(4) changes only x  

<details><summary>Answer</summary>

**(2)** — Rotations about the x- and y-axes are obtained by cyclic permutation of the coordinates.

</details>

**Q24.** `Medium`  
Given below are two statements.  
Statement I: The A-buffer extends the z-buffer to handle transparency and antialiasing.  
Statement II: The painter's algorithm always handles cyclically overlapping polygons without splitting them.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Cyclic overlap requires splitting polygons in the depth-sort method.

</details>

**Q25.** `Low`  
The phenomenon of light reflected from many surfaces in a scene, modelled crudely as a constant, is called

(1) ambient light  
(2) refraction  
(3) diffuse reflection  
(4) specular reflection  

<details><summary>Answer</summary>

**(1)** — Ambient light gives surfaces a base level of illumination.

</details>

**Q26.** `Medium`  
In 3-D clipping against a normalised view volume, the Cohen-Sutherland region codes use

(1) 6 bits  
(2) 3 bits  
(3) 8 bits  
(4) 4 bits  

<details><summary>Answer</summary>

**(1)** — There is one bit for each of the six clipping planes.

</details>

**Q27.** `Medium`  
A Bézier surface is defined by

(1) a single control point  
(2) a z-buffer  
(3) a 1-D array of control points  
(4) a 2-D grid (mesh) of control points, using two parameters u and v  

<details><summary>Answer</summary>

**(4)** — It is the Cartesian product of Bézier blending functions in u and v.

</details>
