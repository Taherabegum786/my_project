# Set 3 — Programming in C: Arrays, Strings, Pointers, Functions, Structures, Unions, Storage Classes, Preprocessor, Files and Command-Line Arguments

**36 questions** — High: 20, Medium: 15, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
What is the output of the following C code?  
char s[] = "hello"; printf("%zu %zu", sizeof(s), strlen(s));

(1) 6 6  
(2) 6 5  
(3) 5 6  
(4) 5 5  

<details><summary>Answer</summary>

**(2)** — sizeof includes the terminating null character; strlen does not.

</details>

**Q2.** `High`  
What is the output of the following C code?  
int a[] = {1, 2, 3, 4, 5}; int \*p = a; p += 2; printf("%d %d", \*p, \*(p + 2));

(1) 1 3  
(2) 3 4  
(3) 2 4  
(4) 3 5  

<details><summary>Answer</summary>

**(4)** — After p += 2, p points to a[2].

</details>

**Q3.** `High`  
On a system with 4-byte int, what is the output of the following C code?  
int a[3][4]; printf("%zu", sizeof(a));

(1) 48  
(2) 16  
(3) 8  
(4) 12  

<details><summary>Answer</summary>

**(1)** — 3 × 4 elements × 4 bytes = 48.

</details>

**Q4.** `High`  
What is the output of the following C code?  
char \*p = "ABCDE"; printf("%c %s", \*(p + 2), p + 3);

(1) C CDE  
(2) C DE  
(3) B DE  
(4) D DE  

<details><summary>Answer</summary>

**(2)** — \*(p + 2) is the third character; p + 3 points to the substring starting at D.

</details>

**Q5.** `High`  
What is the output of the following C code?  
int x = 10; int \*p = &x; int \*\*q = &p; \*\*q = 20; printf("%d", x);

(1) 20  
(2) Address of x  
(3) Compilation error  
(4) 10  

<details><summary>Answer</summary>

**(1)** — \*\*q dereferences twice and refers to x itself.

</details>

**Q6.** `High`  
What is the output of the following C code?  
int a[] = {10, 20, 30}; printf("%d %d", \*a + 1, \*(a + 1));

(1) 20 11  
(2) 11 11  
(3) 20 20  
(4) 11 20  

<details><summary>Answer</summary>

**(4)** — \*a + 1 adds 1 to a[0]; \*(a + 1) is a[1].

</details>

**Q7.** `High`  
What is the output of the following C code?  
int a[2][3] = {{1, 2, 3}, {4, 5, 6}}; int (\*p)[3] = a; printf("%d %d", \*(\*(p + 1) + 2), \*\*p);

(1) 5 1  
(2) 6 4  
(3) 3 1  
(4) 6 1  

<details><summary>Answer</summary>

**(4)** — p + 1 points to the second row; adding 2 selects its third element, 6.

</details>

**Q8.** `High`  
What is the output of the following C code?  
\#define SQ(x) x \* x  
printf("%d", SQ(3 + 2));

(1) 11  
(2) 25  
(3) 13  
(4) 10  

<details><summary>Answer</summary>

**(1)** — The macro expands to 3 + 2 \* 3 + 2 = 11; it should be written as ((x) \* (x)).

</details>

**Q9.** `High`  
What is the output of the following C code, in which f is defined as int f(void) { static int c = 0; return ++c; }?  
f(); f(); printf("%d", f());

(1) 0  
(2) 3  
(3) 1  
(4) 2  

<details><summary>Answer</summary>

**(2)** — A static local variable keeps its value between calls.

</details>

**Q10.** `High`  
What is the output of the following C code?  
void f(int n) { if (n &gt; 0) { f(n - 1); printf("%d", n); } }  — called as f(3)

(1) 3210  
(2) 321  
(3) 123  
(4) 0123  

<details><summary>Answer</summary>

**(3)** — Each call prints after its recursive call returns, so the smallest value is printed first.

</details>

**Q11.** `High`  
What is the output of f(1234), where int f(int n) { if (n == 0) return 0; return n % 10 + f(n / 10); }?

(1) 4  
(2) 24  
(3) 10  
(4) 1234  

<details><summary>Answer</summary>

**(3)** — It sums the decimal digits: 4 + 3 + 2 + 1 = 10.

</details>

**Q12.** `High`  
What is the output of the following C code?  
void swap(int a, int b) { int t = a; a = b; b = t; }  — main: int x = 1, y = 2; swap(x, y); printf("%d %d", x, y);

(1) 1 1  
(2) 1 2  
(3) 2 2  
(4) 2 1  

<details><summary>Answer</summary>

**(2)** — C passes arguments by value; swapping requires passing pointers.

</details>

**Q13.** `High`  
On a typical system where int is 4 bytes with 4-byte alignment, sizeof(struct s) for struct s { char c; int i; char d; } is

(1) 8  
(2) 6  
(3) 12  
(4) 16  

<details><summary>Answer</summary>

**(3)** — Padding: c (1) + 3 bytes, i (4), d (1) + 3 bytes of trailing padding.

</details>

**Q14.** `Medium`  
On a typical system where int is 4 bytes with 4-byte alignment, sizeof(struct s) for struct s { int i; char c; char d; } is

(1) 12  
(2) 8  
(3) 6  
(4) 10  

<details><summary>Answer</summary>

**(2)** — Reordering members so that the small ones are together reduces padding: 4 + 1 + 1 + 2.

</details>

**Q15.** `High`  
On a typical system with 4-byte int and 8-byte double, sizeof(union u) for union u { int i; char c[6]; double d; } is

(1) 6  
(2) 18  
(3) 8  
(4) 24  

<details><summary>Answer</summary>

**(3)** — A union is as large as its largest member (rounded up for alignment).

</details>

**Q16.** `High`  
Given below are two statements.  
Statement I: All members of a union share the same memory location.  
Statement II: All members of a structure can hold valid values at the same time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Writing one union member overwrites the others.

</details>

**Q17.** `High`  
On a 64-bit system with 4-byte int, the code void g(int a[]) { printf("%zu ", sizeof(a)); } with main: int a[10]; g(a); printf("%zu", sizeof(a)); prints

(1) 40 40  
(2) 40 8  
(3) 4 40  
(4) 8 40  

<details><summary>Answer</summary>

**(4)** — An array parameter is adjusted to a pointer, so sizeof gives the pointer size (8).

</details>

**Q18.** `High`  
Match List I with List II.  
List I (Declaration): A. int \*p[10];  B. int (\*p)[10];  C. int (\*p)(int);  D. int \*p(int);  
List II (Meaning): I. A function taking int and returning a pointer to int  II. An array of 10 pointers to int  III. A pointer to an array of 10 ints  IV. A pointer to a function taking int and returning int

(1) A-II, B-IV, C-III, D-I  
(2) A-III, B-II, C-IV, D-I  
(3) A-II, B-III, C-I, D-IV  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(4)** — [] and () bind more tightly than \*, so parentheses change the meaning.

</details>

**Q19.** `High`  
Match List I with List II.  
List I (Storage class): A. auto  B. register  C. static (local)  D. extern  
List II (Property): I. Declares a variable defined in another file or later in the program  II. Default for local variables; lifetime of the block  III. Suggests keeping the variable in a CPU register; its address cannot be taken  IV. Lifetime of the whole program but scope of the block

(1) A-II, B-III, C-I, D-IV  
(2) A-II, B-IV, C-III, D-I  
(3) A-III, B-II, C-IV, D-I  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(4)** — C storage classes.

</details>

**Q20.** `Medium`  
What is the output of the following C code?  
char s1[] = "abc", s2[] = "abc"; printf("%d %d", s1 == s2, strcmp(s1, s2));

(1) 0 1  
(2) 1 1  
(3) 0 0  
(4) 1 0  

<details><summary>Answer</summary>

**(3)** — s1 == s2 compares the addresses of two different arrays; strcmp compares contents and returns 0 for equal strings.

</details>

**Q21.** `Medium`  
What is the output of the following C code?  
printf("%zu", strlen("abc\0def"));

(1) 8  
(2) 3  
(3) 6  
(4) 7  

<details><summary>Answer</summary>

**(2)** — strlen stops at the first null character.

</details>

**Q22.** `Medium`  
What is the output of the following C code?  
\#define STR(x) #x  
\#define CAT(a, b) a##b  
int xy = 7; printf("%s %d", STR(hello), CAT(x, y));

(1) Compilation error  
(2) x y 7  
(3) hello 7  
(4) "hello" xy  

<details><summary>Answer</summary>

**(3)** — \# turns the argument into a string literal; ## pastes x and y into the identifier xy.

</details>

**Q23.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A function-like macro can produce unexpected results when its argument has side effects, such as MAX(i++, j).  
Reason R: Macro names are conventionally written in capital letters.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(2)** — Both are true, but the problem arises because the preprocessor substitutes the argument text, which may then be evaluated more than once.

</details>

**Q24.** `High`  
Match List I with List II.  
List I (fopen mode): A. "r"  B. "w"  C. "a"  D. "r+"  
List II (Behaviour): I. Opens an existing file for reading and writing  II. Opens for reading; fails if the file does not exist  III. Creates a file or truncates an existing one, for writing  IV. Opens for writing at the end of the file, creating it if necessary

(1) A-II, B-III, C-IV, D-I  
(2) A-III, B-II, C-IV, D-I  
(3) A-II, B-III, C-I, D-IV  
(4) A-II, B-IV, C-III, D-I  

<details><summary>Answer</summary>

**(1)** — "w+" and "a+" also allow reading.

</details>

**Q25.** `Medium`  
To find the size of a file in C, a program can use

(1) fgetc once  
(2) fopen only  
(3) sizeof(fp)  
(4) fseek(fp, 0, SEEK\_END) followed by ftell(fp)  

<details><summary>Answer</summary>

**(4)** — ftell returns the current file position.

</details>

**Q26.** `High`  
A C program is run as ./prog one two three. The values of argc and argv[1] are

(1) 3 and "prog"  
(2) 3 and "one"  
(3) 4 and "./prog"  
(4) 4 and "one"  

<details><summary>Answer</summary>

**(4)** — argv[0] is the program name, so argc counts it too.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: The name of an array in C is a modifiable pointer variable.  
Statement II: In most expressions, the name of an array decays to a pointer to its first element.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — An array name is not a modifiable lvalue; a = p is an error.

</details>

**Q28.** `Medium`  
Dereferencing a pointer that has been freed is an example of

(1) a dangling pointer  
(2) a wild pointer that was never initialised  
(3) a null pointer  
(4) a memory leak  

<details><summary>Answer</summary>

**(1)** — A memory leak is allocated memory that is never freed.

</details>

**Q29.** `Medium`  
The function calloc(n, size) differs from malloc(n × size) in that calloc

(1) frees memory automatically  
(2) initialises the allocated memory to zero  
(3) allocates on the stack  
(4) cannot fail  

<details><summary>Answer</summary>

**(2)** — realloc changes the size of a previously allocated block.

</details>

**Q30.** `Medium`  
Given below are two statements.  
Statement I: A void pointer can be dereferenced directly in C.  
Statement II: A void pointer can hold the address of an object of any data type.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — A void pointer must be cast to a specific pointer type before it is dereferenced.

</details>

**Q31.** `Medium`  
In C, a function that calls itself is called

(1) a callback  
(2) a static function  
(3) a recursive function  
(4) an inline function  

<details><summary>Answer</summary>

**(3)** — Each call gets its own activation record on the stack.

</details>

**Q32.** `Medium`  
Which header file declares the functions malloc and free?

(1) stdlib.h  
(2) string.h  
(3) stdio.h  
(4) malloc.c  

<details><summary>Answer</summary>

**(1)** — string.h declares strlen, strcpy and strcmp.

</details>

**Q33.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Passing a large structure by pointer is more efficient than passing it by value.  
Reason R: Passing by value copies the entire structure.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — A pointer to const can be used when the function must not modify it.

</details>

**Q34.** `Medium`  
The #ifndef / #define / #endif idiom at the top of a header file is used to

(1) declare global variables  
(2) speed up linking  
(3) prevent the header from being included more than once in a translation unit (include guard)  
(4) define macros  

<details><summary>Answer</summary>

**(3)** — \#pragma once is a common non-standard alternative.

</details>

**Q35.** `Low`  
Which function reads a whole line of text safely from a file stream in C?

(1) getch  
(2) gets  
(3) fgets  
(4) scanf("%s")  

<details><summary>Answer</summary>

**(3)** — gets was removed from C11 because it cannot limit the input length.

</details>

**Q36.** `Medium`  
What does the expression \*p++ do when p points into an int array?

(1) Increments the value pointed to  
(2) Advances p and then returns the new value  
(3) Is a syntax error  
(4) Returns the value pointed to and then advances p to the next element  

<details><summary>Answer</summary>

**(4)** — Postfix ++ binds more tightly than \*, so it applies to p.

</details>
