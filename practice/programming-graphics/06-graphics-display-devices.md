# Set 6 — Computer Graphics: Video Display Devices, Raster-Scan and Random-Scan Systems, Input Devices

**24 questions** — High: 8, Medium: 15, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
The frame buffer size needed for a 1024 × 768 display with 24 bits per pixel is

(1) 3 MB  
(2) 1.5 MB  
(3) 768 KB  
(4) 2.25 MB  

<details><summary>Answer</summary>

**(4)** — 1024 × 768 × 3 bytes = 2,359,296 bytes = 2.25 MB.

</details>

**Q2.** `High`  
A raster system with a resolution of 640 × 480 and 8 bits per pixel needs a frame buffer of

(1) 600 KB  
(2) 2.4 MB  
(3) 300 KB  
(4) 307 MB  

<details><summary>Answer</summary>

**(3)** — 640 × 480 = 307,200 bytes = 300 KB.

</details>

**Q3.** `Medium`  
A 1280 × 1024 display with 24-bit colour needs a frame buffer of

(1) 1.25 MB  
(2) 5 MB  
(3) 3.75 MB  
(4) 2.5 MB  

<details><summary>Answer</summary>

**(3)** — 1280 × 1024 × 3 bytes = 3,932,160 bytes = 3.75 MB.

</details>

**Q4.** `High`  
A raster display of 1024 × 768 pixels is refreshed 60 times per second. The time available to access each pixel (ignoring retrace) is about

(1) 21 ns  
(2) 2.1 ns  
(3) 16.7 ms  
(4) 210 ns  

<details><summary>Answer</summary>

**(1)** — 1 / (1024 × 768 × 60) s ≈ 21.2 ns.

</details>

**Q5.** `High`  
With 24 bits per pixel, the number of colours that can be displayed is

(1) about 16.7 million (2^24)  
(2) 24  
(3) 65,536  
(4) 256  

<details><summary>Answer</summary>

**(1)** — This is called true colour.

</details>

**Q6.** `High`  
A system has an 8-bit frame buffer used as an index into a colour lookup table with 24-bit entries. How many colours can be displayed simultaneously, and from how large a palette?

(1) 16.7 million out of 256  
(2) 256 out of about 16.7 million  
(3) 256 out of 256  
(4) 8 out of 24  

<details><summary>Answer</summary>

**(2)** — The lookup table saves frame-buffer memory while allowing a large palette.

</details>

**Q7.** `High`  
Match List I with List II.  
List I (Display): A. Raster-scan display  B. Random-scan (vector) display  C. Direct-view storage tube  D. Plasma panel  
List II (Characteristic): I. Draws pictures one line at a time from a display list, producing smooth lines  II. Sweeps the beam row by row and stores pixel intensities in a frame buffer  III. Stores the picture as a charge distribution behind the screen, so no refresh is needed  IV. Flat-panel emissive display using ionised gas between glass plates

(1) A-I, B-II, C-III, D-IV  
(2) A-II, B-I, C-III, D-IV  
(3) A-II, B-I, C-IV, D-III  
(4) A-II, B-III, C-I, D-IV  

<details><summary>Answer</summary>

**(2)** — Common display technologies in Hearn and Baker.

</details>

**Q8.** `High`  
Given below are two statements.  
Statement I: Random-scan systems produce smooth line drawings because the beam follows the line path directly.  
Statement II: Random-scan systems are well suited to displaying realistic shaded scenes.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Raster systems are needed for realistic shaded and filled images.

</details>

**Q9.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Random-scan displays show jagged (aliased) lines.  
Reason R: In a raster system, lines are approximated by discrete pixel positions on a grid.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Random-scan displays draw lines directly and smoothly; jaggedness is a raster-display effect, as R explains.

</details>

**Q10.** `Medium`  
In a CRT, persistence of a phosphor is defined as

(1) the number of pixels per inch  
(2) the time to draw one frame  
(3) the time for the emitted light to decay to one-tenth of its original intensity  
(4) the speed of the electron beam  

<details><summary>Answer</summary>

**(3)** — Lower-persistence phosphors need higher refresh rates to avoid flicker.

</details>

**Q11.** `Medium`  
Interlaced scanning displays

(1) only half the image  
(2) odd-numbered lines in one pass and even-numbered lines in the next  
(3) no image  
(4) all lines in each pass  

<details><summary>Answer</summary>

**(2)** — It effectively doubles the refresh rate seen by the eye, reducing flicker at low refresh rates.

</details>

**Q12.** `Medium`  
The shadow-mask method for colour CRTs uses

(1) a liquid crystal layer  
(2) three electron guns and a grid of red, green and blue phosphor dots  
(3) one electron gun and two phosphor layers  
(4) ionised gas  

<details><summary>Answer</summary>

**(2)** — The beam-penetration method uses two phosphor layers and gives only a few colours.

</details>

**Q13.** `Medium`  
The beam-penetration method of colour CRT display can produce

(1) millions of colours  
(2) only four colours: red, orange, yellow and green  
(3) black and white only  
(4) 256 colours  

<details><summary>Answer</summary>

**(2)** — Colour depends on how far the electrons penetrate the red and green layers.

</details>

**Q14.** `Medium`  
Given below are two statements.  
Statement I: An LCD is an emissive display that produces its own light at each pixel.  
Statement II: In a passive-matrix LCD, a transistor is placed at each pixel position.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — An LCD is non-emissive (it modulates light), and per-pixel transistors are the feature of active-matrix LCDs.

</details>

**Q15.** `Medium`  
Match List I with List II.  
List I (Input device): A. Light pen  B. Digitizer (graphics tablet)  C. Data glove  D. Trackball  
List II (Use): I. Grasping and moving virtual objects in three dimensions  II. Pointing directly at positions on the screen by detecting light from the screen  III. Entering coordinates by tracing a drawing on a flat surface  IV. Rotating a ball to move the cursor

(1) A-II, B-III, C-I, D-IV  
(2) A-II, B-III, C-IV, D-I  
(3) A-III, B-II, C-I, D-IV  
(4) A-II, B-I, C-III, D-IV  

<details><summary>Answer</summary>

**(1)** — Graphics input devices.

</details>

**Q16.** `Medium`  
The aspect ratio of a display is

(1) the refresh rate  
(2) the ratio of vertical points to horizontal points needed to produce equal-length lines in both directions (or width to height)  
(3) the number of pixels per inch  
(4) the number of colours  

<details><summary>Answer</summary>

**(2)** — A common screen aspect ratio is 4:3 (or 16:9 for wide screens).

</details>

**Q17.** `Medium`  
Resolution of a raster display is

(1) the number of colours  
(2) the refresh rate  
(3) the persistence  
(4) the maximum number of points that can be displayed without overlap, often given as pixels across × down  

<details><summary>Answer</summary>

**(4)** — For example 1920 × 1080.

</details>

**Q18.** `Medium`  
The display processor (graphics controller) in a raster system mainly

(1) frees the CPU from graphics tasks such as scan conversion of lines and polygons into the frame buffer  
(2) stores the program  
(3) manages the network  
(4) controls the keyboard  

<details><summary>Answer</summary>

**(1)** — Scan conversion converts output primitives into pixel intensities.

</details>

**Q19.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A random-scan display needs a higher-cost refresh process for complex pictures than for simple ones.  
Reason R: In a random-scan system, refresh time depends on the number of lines to be drawn.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Too many lines cause flicker because the display cannot be refreshed often enough.

</details>

**Q20.** `Medium`  
A frame buffer that stores one bit per pixel is called a

(1) colour map  
(2) bitmap  
(3) z-buffer  
(4) pixmap  

<details><summary>Answer</summary>

**(2)** — With several bits per pixel it is called a pixmap.

</details>

**Q21.** `Low`  
Horizontal retrace in a raster CRT is

(1) the return of the beam from the bottom to the top of the screen  
(2) the erasing of the screen  
(3) the return of the beam from the right end of a scan line to the left end of the next  
(4) the drawing of a vertical line  

<details><summary>Answer</summary>

**(3)** — Vertical retrace returns the beam from the bottom to the top after each frame.

</details>

**Q22.** `Medium`  
Given below are two statements.  
Statement I: A refresh rate below about 24 frames per second causes noticeable flicker.  
Statement II: Raster-scan systems typically refresh at 60 to 80 frames per second or more.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Higher refresh rates give a steadier picture.

</details>

**Q23.** `Medium`  
A raster system has 8 bits per pixel for each of red, green and blue, and a resolution of 512 × 512. The total frame buffer memory needed is

(1) 1 MB  
(2) 256 KB  
(3) 512 KB  
(4) 768 KB  

<details><summary>Answer</summary>

**(4)** — 512 × 512 × 3 bytes = 786,432 bytes = 768 KB.

</details>

**Q24.** `Medium`  
In a virtual-reality system, a head-mounted display (HMD) is used to

(1) provide a stereoscopic view that changes as the user's head moves  
(2) enter text  
(3) print images  
(4) scan documents  

<details><summary>Answer</summary>

**(1)** — Tracking devices report the head position to the computer.

</details>
