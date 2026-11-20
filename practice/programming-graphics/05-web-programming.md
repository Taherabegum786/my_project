# Set 5 — Web Programming (HTML, DHTML, CSS, XML, JavaScript, Java, Servlets and Applets)

**33 questions** — High: 13, Medium: 19, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (HTML tag): A. &lt;a&gt;  B. &lt;img&gt;  C. &lt;table&gt;  D. &lt;form&gt;  
List II (Purpose): I. Collects user input to be submitted to a server  II. Creates a hyperlink using the href attribute  III. Embeds an image using the src attribute  IV. Arranges data in rows (&lt;tr&gt;) and cells (&lt;td&gt;)

(1) A-II, B-III, C-I, D-IV  
(2) A-II, B-III, C-IV, D-I  
(3) A-II, B-IV, C-III, D-I  
(4) A-III, B-II, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Basic HTML elements.

</details>

**Q2.** `High`  
In an HTML table, the attribute that makes a cell span two columns is

(1) width="2"  
(2) rowspan="2"  
(3) colspan="2"  
(4) span="2"  

<details><summary>Answer</summary>

**(3)** — rowspan makes a cell span several rows.

</details>

**Q3.** `High`  
DHTML (Dynamic HTML) is a combination of

(1) XML and XSLT  
(2) HTML and Java applets only  
(3) HTML, CSS, JavaScript and the DOM  
(4) HTTP and FTP  

<details><summary>Answer</summary>

**(3)** — Scripts manipulate the DOM and styles to change a page without reloading it.

</details>

**Q4.** `High`  
Given below are two statements.  
Statement I: HTML is case-insensitive for tag names, while XML is case-sensitive.  
Statement II: In XML, every element must be properly closed and nested.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — These are among the rules for a well-formed XML document.

</details>

**Q5.** `High`  
Match List I with List II.  
List I (XML technology): A. DTD  B. XSD (XML Schema)  C. XSLT  D. XPath  
List II (Purpose): I. Transforms XML documents into other formats such as HTML  II. Defines document structure with limited data types, in non-XML syntax  III. Selects nodes in an XML document using path expressions  IV. Defines document structure and rich data types, written in XML

(1) A-II, B-I, C-IV, D-III  
(2) A-IV, B-II, C-I, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — XML-related W3C standards.

</details>

**Q6.** `High`  
Arrange CSS rules in increasing order of specificity.  
A. ID selector (#main)  B. Element selector (p)  C. Inline style attribute  D. Class selector (.note)

(1) B, A, D, C  
(2) D, B, A, C  
(3) B, D, C, A  
(4) B, D, A, C  

<details><summary>Answer</summary>

**(4)** — !important declarations override normal specificity.

</details>

**Q7.** `High`  
In JavaScript, the values of "5" + 3 and "5" − 3 are respectively

(1) 8 and "2"  
(2) "53" and 2  
(3) "53" and "2"  
(4) 8 and 2  

<details><summary>Answer</summary>

**(2)** — + with a string performs concatenation; − converts its operands to numbers.

</details>

**Q8.** `High`  
In JavaScript, the results of 0 == "0" and 0 === "0" are respectively

(1) true and false  
(2) true and true  
(3) false and false  
(4) false and true  

<details><summary>Answer</summary>

**(1)** — == converts types before comparing; === compares without type conversion.

</details>

**Q9.** `Medium`  
In JavaScript, typeof null evaluates to

(1) "undefined"  
(2) "number"  
(3) "null"  
(4) "object"  

<details><summary>Answer</summary>

**(4)** — This is a long-standing quirk of the language; typeof undefined is "undefined".

</details>

**Q10.** `Medium`  
What is printed by the following JavaScript code?  
var x = 10; function f() { console.log(x); var x = 20; } f();

(1) 20  
(2) ReferenceError  
(3) 10  
(4) undefined  

<details><summary>Answer</summary>

**(4)** — The inner declaration var x is hoisted to the top of f, so x is undefined when logged.

</details>

**Q11.** `High`  
In Java, with String s1 = "Java", s2 = "Java", s3 = new String("Java");, the values of s1 == s2, s1 == s3 and s1.equals(s3) are

(1) true, true, true  
(2) true, false, false  
(3) false, false, true  
(4) true, false, true  

<details><summary>Answer</summary>

**(4)** — Literals are interned and share one object; new creates a separate object; equals compares contents.

</details>

**Q12.** `High`  
In Java, the statements System.out.println("a" + 1 + 2); and System.out.println(1 + 2 + "a"); print

(1) a12 and 12a  
(2) a3 and 3a  
(3) a12 and 3a  
(4) a3 and 12a  

<details><summary>Answer</summary>

**(3)** — + is evaluated left to right; once a String is involved, the rest is concatenation.

</details>

**Q13.** `Medium`  
In Java, System.out.println('a' + 1); prints

(1) Compilation error  
(2) 98  
(3) b  
(4) a1  

<details><summary>Answer</summary>

**(2)** — char is promoted to int, and 'a' is 97.

</details>

**Q14.** `Medium`  
In Java, after int x = 5; x += x++ + ++x; the value of x is

(1) 16  
(2) 12  
(3) 17  
(4) 18  

<details><summary>Answer</summary>

**(3)** — x = 5 + (5 + 7) = 17; Java evaluates operands left to right.

</details>

**Q15.** `High`  
Match List I with List II.  
List I (Servlet life-cycle method): A. init()  B. service()  C. destroy()  
List II (When it is called): I. Once, before the servlet is removed from service  II. Once, when the servlet is first loaded  III. For each client request; dispatches to doGet() or doPost()

(1) A-II, B-I, C-III  
(2) A-I, B-III, C-II  
(3) A-III, B-II, C-I  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — The servlet container (such as Tomcat) manages the life cycle.

</details>

**Q16.** `High`  
Arrange the life-cycle methods of a Java applet in the order in which they are first called.  
A. start()  B. init()  C. paint()  D. destroy()  E. stop()

(1) B, C, A, E, D  
(2) B, A, C, E, D  
(3) B, A, C, D, E  
(4) A, B, C, E, D  

<details><summary>Answer</summary>

**(2)** — Applets are deprecated in modern Java but remain in the syllabus.

</details>

**Q17.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Java programs are platform independent.  
Reason R: Java source code is compiled to native machine code for each processor.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — Java compiles to bytecode, which runs on any platform that has a JVM.

</details>

**Q18.** `Medium`  
Which of the following are mechanisms for session tracking in servlets?  
A. Cookies  B. URL rewriting  C. Hidden form fields  D. HttpSession  E. Applet threads  
Choose the correct answer from the options given below:

(1) B, C and E only  
(2) A and E only  
(3) A, B, C, D and E  
(4) A, B, C and D only  

<details><summary>Answer</summary>

**(4)** — HTTP is stateless, so these mechanisms maintain state across requests.

</details>

**Q19.** `Medium`  
Given below are two statements.  
Statement I: The HTTP POST method sends form data in the URL.  
Statement II: The HTTP GET method is preferred for sending large or sensitive data.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(2)** — It is the other way round: GET puts data in the URL, and POST (in the request body) suits large or sensitive data.

</details>

**Q20.** `Medium`  
Which of the following is true of Java?

(1) It supports explicit pointer arithmetic  
(2) It supports multiple inheritance of classes  
(3) It has automatic garbage collection  
(4) It requires manual memory deallocation  

<details><summary>Answer</summary>

**(3)** — Java supports multiple inheritance of interfaces but not of classes.

</details>

**Q21.** `Medium`  
Match List I with List II.  
List I (Java keyword): A. final (on a class)  B. static  C. abstract  D. interface  
List II (Meaning): I. Belongs to the class rather than to instances  II. The class cannot be subclassed  III. Declares a type with abstract methods that a class implements  IV. The class cannot be instantiated and may have abstract methods

(1) A-II, B-I, C-IV, D-III  
(2) A-I, B-II, C-IV, D-III  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-I, C-III, D-IV  

<details><summary>Answer</summary>

**(1)** — Basic Java modifiers.

</details>

**Q22.** `Medium`  
In Java, checked exceptions are those that

(1) must be either caught or declared in the throws clause, such as IOException  
(2) occur only at run time  
(3) cannot be caught  
(4) are subclasses of RuntimeException  

<details><summary>Answer</summary>

**(1)** — Unchecked exceptions, such as NullPointerException, extend RuntimeException.

</details>

**Q23.** `Medium`  
A thread in Java can be created by

(1) calling main twice  
(2) using the goto statement  
(3) extending the Thread class or implementing the Runnable interface  
(4) declaring a static block  

<details><summary>Answer</summary>

**(3)** — The thread's code goes in the run() method, and start() launches it.

</details>

**Q24.** `Medium`  
The DOCTYPE declaration &lt;!DOCTYPE html&gt; at the top of a page

(1) tells the browser to render the page in HTML5 standards mode  
(2) declares a JavaScript variable  
(3) includes a CSS file  
(4) is an HTML tag that is displayed  

<details><summary>Answer</summary>

**(1)** — Without it, browsers may use quirks mode.

</details>

**Q25.** `Medium`  
Given below are two statements.  
Statement I: An XML document is well-formed if it follows XML syntax rules.  
Statement II: An XML document is valid only if it is well-formed and conforms to a DTD or schema.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Every valid document is well-formed, but not conversely.

</details>

**Q26.** `Medium`  
In JavaScript, the event handler attribute that runs a script when a page has finished loading is

(1) onclick  
(2) onchange  
(3) onsubmit  
(4) onload  

<details><summary>Answer</summary>

**(4)** — onclick runs when an element is clicked.

</details>

**Q27.** `Medium`  
The &lt;meta&gt; tag in HTML is placed in the

(1) &lt;body&gt;  
(2) &lt;table&gt;  
(3) &lt;head&gt;  
(4) &lt;footer&gt;  

<details><summary>Answer</summary>

**(3)** — It gives metadata such as the character set and description.

</details>

**Q28.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: XML is suitable for exchanging data between heterogeneous systems.  
Reason R: XML is a W3C recommendation.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but suitability comes from XML being a self-describing, platform-independent text format.

</details>

**Q29.** `Medium`  
Which HTML5 element is used for self-contained content such as a blog post?

(1) &lt;frame&gt;  
(2) &lt;article&gt;  
(3) &lt;div&gt;  
(4) &lt;span&gt;  

<details><summary>Answer</summary>

**(2)** — Other semantic elements include &lt;header&gt;, &lt;nav&gt;, &lt;section&gt; and &lt;footer&gt;.

</details>

**Q30.** `Low`  
CSS stands for

(1) Coded Style Sheets  
(2) Cascading Style Sheets  
(3) Creative Style System  
(4) Computer Style Syntax  

<details><summary>Answer</summary>

**(2)** — CSS separates presentation from content.

</details>

**Q31.** `Medium`  
In JavaScript, the result of 0.1 + 0.2 === 0.3 is

(1) true  
(2) false  
(3) NaN  
(4) undefined  

<details><summary>Answer</summary>

**(2)** — Binary floating-point cannot represent 0.1 and 0.2 exactly.

</details>

**Q32.** `Medium`  
JSP (JavaServer Pages) differs from servlets in that JSP

(1) replaces HTML entirely  
(2) runs only on the client  
(3) cannot generate dynamic content  
(4) embeds Java code within HTML pages, and is translated into a servlet by the container  

<details><summary>Answer</summary>

**(4)** — JSP is convenient for presentation; servlets for control logic.

</details>

**Q33.** `Medium`  
In Java, the default value of an element of a newly created int array is

(1) undefined  
(2) null  
(3) garbage  
(4) 0  

<details><summary>Answer</summary>

**(4)** — Object reference arrays default to null.

</details>
