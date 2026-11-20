# Set 4 — Object-Oriented Programming and C++ (classes, constructors, overloading, inheritance, virtual functions, templates, exceptions, streams)

**37 questions** — High: 16, Medium: 20, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
What is the output of the following C++ program?  
class A { public: A() { cout &lt;&lt; "A"; } ~A() { cout &lt;&lt; "a"; } };  
class B : public A { public: B() { cout &lt;&lt; "B"; } ~B() { cout &lt;&lt; "b"; } };  
int main() { B obj; }

(1) ABab  
(2) ABba  
(3) BAab  
(4) BAba  

<details><summary>Answer</summary>

**(2)** — Base constructors run before derived ones; destructors run in the reverse order.

</details>

**Q2.** `High`  
What is the output of the following C++ program, where M prints "M"/"m" in its constructor/destructor?  
class B : public A { M m; public: B() { cout &lt;&lt; "B"; } ~B() { cout &lt;&lt; "b"; } };  — A prints "A"/"a"; main: B obj;

(1) AMBabm  
(2) ABMmba  
(3) AMBbma  
(4) MABbam  

<details><summary>Answer</summary>

**(3)** — Order of construction: base class, then members, then the body of the derived constructor; destruction is the reverse.

</details>

**Q3.** `High`  
What is the output of the following C++ code?  
class Base { public: virtual void show() { cout &lt;&lt; "Base"; } };  
class Derived : public Base { public: void show() { cout &lt;&lt; "Derived"; } };  
Base \*p = new Derived; p-&gt;show();

(1) Compilation error  
(2) BaseDerived  
(3) Derived  
(4) Base  

<details><summary>Answer</summary>

**(3)** — A virtual function is bound at run time to the type of the object pointed to.

</details>

**Q4.** `High`  
In the previous program, if show() in Base is NOT declared virtual, the call p-&gt;show() through a Base pointer prints

(1) Derived  
(2) Compilation error  
(3) BaseDerived  
(4) Base  

<details><summary>Answer</summary>

**(4)** — Without virtual, the call is bound at compile time using the pointer's static type.

</details>

**Q5.** `High`  
What is the output of the following C++ code?  
class B { public: ~B() { cout &lt;&lt; "~B"; } };  
class D : public B { public: ~D() { cout &lt;&lt; "~D"; } };  
B \*p = new D; delete p;

(1) ~D  
(2) ~D~B  
(3) ~B  
(4) ~B~D  

<details><summary>Answer</summary>

**(3)** — Without a virtual destructor, only the base destructor runs (formally the behaviour is undefined); with a virtual destructor the output is ~D~B.

</details>

**Q6.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A base class intended for polymorphic use should have a virtual destructor.  
Reason R: Deleting a derived object through a base pointer without a virtual destructor fails to call the derived destructor.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Resources held by the derived part would otherwise leak.

</details>

**Q7.** `High`  
In C++, the value printed by cout &lt;&lt; sizeof('A'); and by cout &lt;&lt; sizeof(E); for an empty class E {}; are respectively

(1) 4 and 1  
(2) 1 and 1  
(3) 4 and 0  
(4) 1 and 0  

<details><summary>Answer</summary>

**(2)** — A char literal has type char in C++; an empty class has size 1 so that distinct objects have distinct addresses.

</details>

**Q8.** `High`  
What is the output of the following C++ code?  
void f(int x) { cout &lt;&lt; "int "; }  void f(double x) { cout &lt;&lt; "double "; }  
int main() { f(5); f(5.0); f('a'); }

(1) int int int  
(2) int double int  
(3) int double double  
(4) Compilation error  

<details><summary>Answer</summary>

**(2)** — 'a' is promoted from char to int, which is a better match than conversion to double.

</details>

**Q9.** `High`  
What is the output of the following C++ code?  
int add(int a, int b = 10, int c = 20) { return a + b + c; }  
cout &lt;&lt; add(1) &lt;&lt; " " &lt;&lt; add(1, 2) &lt;&lt; " " &lt;&lt; add(1, 2, 3);

(1) 31 23 33  
(2) 31 23 6  
(3) 1 3 6  
(4) 31 13 6  

<details><summary>Answer</summary>

**(2)** — Missing trailing arguments take their default values.

</details>

**Q10.** `High`  
What is the output of the following C++ code?  
class C { public: static int n; C() { n++; } };  int C::n = 0;  
int main() { C a, b, c; cout &lt;&lt; C::n; }

(1) 1  
(2) 3  
(3) 0  
(4) Compilation error  

<details><summary>Answer</summary>

**(2)** — A static data member is shared by all objects of the class.

</details>

**Q11.** `High`  
What is the output of the following C++ code?  
try { throw 5; cout &lt;&lt; "X"; } catch (int e) { cout &lt;&lt; "int " &lt;&lt; e; } catch (...) { cout &lt;&lt; "other"; }

(1) X int 5  
(2) int 5  
(3) int 5 other  
(4) other  

<details><summary>Answer</summary>

**(2)** — Control leaves the try block at the throw, and the first matching handler runs.

</details>

**Q12.** `Medium`  
What is the output of the following C++ code?  
try { throw 'a'; } catch (int e) { cout &lt;&lt; "int"; } catch (...) { cout &lt;&lt; "other"; }

(1) 97  
(2) other  
(3) a  
(4) int  

<details><summary>Answer</summary>

**(2)** — No conversion from char to int is applied when matching handlers, so the catch-all handler runs.

</details>

**Q13.** `High`  
What is the output of the following C++ code?  
class C { public: C() {} C(const C &) { cout &lt;&lt; "copy "; } };  
void f(C c) {}  
int main() { C a; f(a); C b = a; }

(1) copy  
(2) nothing  
(3) copy copy  
(4) copy copy copy  

<details><summary>Answer</summary>

**(3)** — The copy constructor is called when an object is passed by value and when an object is initialised from another.

</details>

**Q14.** `Medium`  
What is the output of the following C++ code?  
int x = 1;  
int main() { int x = 2; cout &lt;&lt; x &lt;&lt; ::x; }

(1) 12  
(2) 21  
(3) 22  
(4) 11  

<details><summary>Answer</summary>

**(2)** — ::x refers to the global x, hidden by the local x.

</details>

**Q15.** `Medium`  
What is the output of the following C++ code?  
int a = 5; int &r = a; r = 10; cout &lt;&lt; a;

(1) 5  
(2) Address of a  
(3) Compilation error  
(4) 10  

<details><summary>Answer</summary>

**(4)** — A reference is an alias for the variable it is bound to.

</details>

**Q16.** `Medium`  
What is the output of the following C++ code?  
template &lt;class T&gt; T mx(T a, T b) { return a &gt; b ? a : b; }  
cout &lt;&lt; mx(3, 7) &lt;&lt; " " &lt;&lt; mx(2.5, 1.5);

(1) 7 2  
(2) 7 2.5  
(3) 3 1.5  
(4) Compilation error  

<details><summary>Answer</summary>

**(2)** — The template is instantiated separately for int and for double.

</details>

**Q17.** `Medium`  
What is the output of the following C++ code?  
class P { public: int x; P(int v) : x(v) {} P operator+(const P &o) { return P(x + o.x \* 2); } };  
P a(3), b(4); P c = a + b; cout &lt;&lt; c.x;

(1) 7  
(2) 11  
(3) 14  
(4) 10  

<details><summary>Answer</summary>

**(2)** — a + b calls a.operator+(b), which computes 3 + 4 × 2.

</details>

**Q18.** `Medium`  
In C++, a class has prefix operator++ adding 10 and postfix operator++(int) adding 1 to a member v, initially 0. After ++a; a++; the value of a.v is

(1) 20  
(2) 11  
(3) 2  
(4) 10  

<details><summary>Answer</summary>

**(2)** — The dummy int parameter distinguishes the postfix form.

</details>

**Q19.** `High`  
Which of the following operators CANNOT be overloaded in C++?  
A. ::  B. .  C. ?:  D. sizeof  E. []  
Choose the correct answer from the options given below:

(1) A, B, C, D and E  
(2) A, B, C and D only  
(3) A and B only  
(4) C, D and E only  

<details><summary>Answer</summary>

**(2)** — The subscript operator [] can be overloaded; .\* also cannot be overloaded.

</details>

**Q20.** `High`  
Match List I with List II.  
List I (OOP concept): A. Encapsulation  B. Inheritance  C. Polymorphism  D. Abstraction  
List II (Meaning): I. One interface with many implementations, chosen by the object's type  II. Bundling data with the methods that operate on it and hiding internal details  III. Showing only essential features and hiding implementation complexity  IV. A class acquiring the properties of another class

(1) A-IV, B-II, C-I, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-IV, C-III, D-I  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(4)** — The four pillars of object-oriented programming.

</details>

**Q21.** `High`  
Given below are two statements.  
Statement I: A class that has at least one pure virtual function is an abstract class and cannot be instantiated.  
Statement II: A derived class of an abstract class is abstract unless it overrides all the pure virtual functions.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — A pure virtual function is declared as virtual void f() = 0;.

</details>

**Q22.** `High`  
Match List I with List II.  
List I (Base-class member under public inheritance): A. public  B. protected  C. private  
List II (Access in the derived class): I. Not accessible  II. Remains protected  III. Remains public

(1) A-III, B-I, C-II  
(2) A-III, B-II, C-I  
(3) A-I, B-II, C-III  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(2)** — Under private inheritance, public and protected members both become private.

</details>

**Q23.** `Medium`  
The diamond problem in multiple inheritance (D derives from B and C, which both derive from A) is resolved in C++ by

(1) using templates  
(2) declaring B and C with virtual inheritance from A  
(3) using friend functions  
(4) making A abstract  

<details><summary>Answer</summary>

**(2)** — Virtual inheritance ensures that D contains only one A sub-object.

</details>

**Q24.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: A friend function of a class can access its private members.  
Reason R: A friend function is a member function of that class.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — A friend function is not a member; the class grants it access explicitly.

</details>

**Q25.** `Medium`  
Function overloading in C++ is an example of

(1) compile-time (static) polymorphism  
(2) run-time polymorphism  
(3) dynamic binding  
(4) encapsulation  

<details><summary>Answer</summary>

**(1)** — Virtual functions provide run-time polymorphism.

</details>

**Q26.** `Medium`  
The this pointer in a non-static member function points to

(1) the first data member only  
(2) the base class  
(3) the class  
(4) the object on which the function was invoked  

<details><summary>Answer</summary>

**(4)** — Static member functions have no this pointer.

</details>

**Q27.** `Medium`  
Given below are two statements.  
Statement I: A constructor can be declared virtual in C++.  
Statement II: A destructor can be declared virtual in C++.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — Constructors cannot be virtual because the object's type is not yet complete during construction.

</details>

**Q28.** `Medium`  
Which of the following statements about new and malloc in C++ is correct?

(1) new returns void\* that must be cast  
(2) delete can free memory obtained from malloc  
(3) malloc calls constructors  
(4) new allocates memory and calls the constructor; delete calls the destructor and frees memory  

<details><summary>Answer</summary>

**(4)** — Memory from malloc must be released with free.

</details>

**Q29.** `Medium`  
Match List I with List II.  
List I (C++ stream object or class): A. cin  B. cerr  C. ofstream  D. ifstream  
List II (Purpose): I. Unbuffered standard error output  II. Standard input  III. Reading from a file  IV. Writing to a file

(1) A-I, B-II, C-IV, D-III  
(2) A-II, B-I, C-IV, D-III  
(3) A-II, B-I, C-III, D-IV  
(4) A-II, B-IV, C-I, D-III  

<details><summary>Answer</summary>

**(2)** — fstream supports both reading and writing.

</details>

**Q30.** `Medium`  
An inline function in C++

(1) cannot have parameters  
(2) is a request to the compiler to substitute the function body at the call site, avoiding call overhead  
(3) is always expanded at the call site by the compiler  
(4) must be recursive  

<details><summary>Answer</summary>

**(2)** — The compiler may ignore the request.

</details>

**Q31.** `Medium`  
Given below are two statements.  
Statement I: A template function is type-checked when it is instantiated with specific types.  
Statement II: Templates provide run-time polymorphism.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — Templates are a compile-time (parametric) polymorphism mechanism.

</details>

**Q32.** `Medium`  
In C++, a program can be split into several source files compiled separately. A global variable defined in one file is used in another by

(1) using a friend declaration  
(2) defining it again  
(3) using static  
(4) redeclaring it with extern in the other file  

<details><summary>Answer</summary>

**(4)** — Header files usually hold the extern declarations.

</details>

**Q33.** `Low`  
Which keyword is used to handle an exception in C++?

(1) try  
(2) catch  
(3) finally  
(4) throw  

<details><summary>Answer</summary>

**(2)** — C++ has try, throw and catch; finally exists in Java, not in C++.

</details>

**Q34.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: In C++, a member function declared const cannot modify the object's non-mutable data members.  
Reason R: A const member function can be called only on non-const objects.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(3)** — A const member function can be called on both const and non-const objects; inside it, this is a pointer to const.

</details>

**Q35.** `Medium`  
An exception thrown in a function that has no matching handler anywhere in the call chain results in

(1) the exception being ignored  
(2) a compile-time error  
(3) a call to std::terminate  
(4) the program continuing  

<details><summary>Answer</summary>

**(3)** — By default terminate calls abort.

</details>

**Q36.** `Medium`  
Event handling in C++ GUI frameworks (such as Qt signals and slots, or callbacks in other libraries) typically relies on

(1) the preprocessor only  
(2) function pointers, functors or virtual functions invoked when an event occurs  
(3) exception handling  
(4) file streams  

<details><summary>Answer</summary>

**(2)** — The framework calls the registered handler when the event is raised.

</details>

**Q37.** `Medium`  
What does the following C++ code print? class S { public: virtual double area() = 0; }; class Sq : public S { double s; public: Sq(double x) : s(x) {} double area() { return s \* s; } };  S \*p = new Sq(3); cout &lt;&lt; p-&gt;area();

(1) 6  
(2) Compilation error  
(3) 9  
(4) 3  

<details><summary>Answer</summary>

**(3)** — Sq implements the pure virtual function, so it can be instantiated and called through the base pointer.

</details>
