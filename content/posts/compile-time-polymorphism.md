+++
date = "2012-02-05T14:14:00-07:00"
draft = false
title = "Compile-Time Polymorphism"
slug = "compile-time-polymorphism"
tags = ["c++", "idiom", "performance", "template", "virtual"]

+++
Polymorphism is a tool in object orientation, which allows us to model behavior, while simultaneously leverage existing code. Polymorphism allows is behavior reuse.  In C++ polymorphism, comes in 2 flavors, the standard runtime variant, and a curious compile time variant.  Runtime polymorphism, like Java, leverages virtual functions to dynamically bind[1. With virtual functions the compiler doesn't know which method to call until runtime. In C++ this is implemented with the <a href="http://en.wikipedia.org/wiki/Virtual_method_table">virtual method table</a>] a method at the call site. Compile Time polymorphism uses templates, to bind at compile time, thus negating the performance affect of virtual functions.

<!--more-->

Polymorphism is a powerful concept. Polymorphism is a powerful tool in object-orientation, allowing one to realistically model the behavior or structure of some entity in software. This is key to any software design. Regardless, of idioms, language, paradigm, a realistic model is essential to a good design. If follow every best practice in software design, but your system doesn't accurately reflect the real-world model, your software will be difficult to work with, and it will be impossible to bring new people on your project.  An accurate portrayal is required.

C++ affords us 2 forms of g: compile-time [2. Compile-Time polymorphism is also known as static polymorphism. I, however find this nomenclature confusing.  "static dynamicism".... Um, what?], and runtime.  Runtime is the most straightforward, and uses virtual functions.  However, as we'll see later, virtual function have their own performance costs.

<a href="http://www.codestrokes.com/wp-content/uploads/2012/02/SuperSimplePolymorphism.png.jpg.jpeg"><img class="aligncenter size-full wp-image-529" title="SuperSimplePolymorphism.jpg" src="http://www.codestrokes.com/wp-content/uploads/2012/02/SuperSimplePolymorphism.png.jpg.jpeg" alt="" width="125" height="185" /></a>

We're going to implement this very simple hierarchy, to demonstrate polymorphism is its most basic form.
<pre lang="cpp" escaped="true">struct Base {
    Base (){}
    virtual ~Base (){}
    virtual void DoSomething(){
        cout &lt;&lt; "Hello From Base." &lt;&lt; endl;
    }
};

struct Child : public Base {
    Child (){}
    virtual ~Child (){}
    virtual void DoSomething() {
        cout &lt;&lt; "Hello from Child." &lt;&lt; endl;
    }
};</pre>
Using the following driver code.
<pre lang="cpp" escaped="true">int main(int argc, char const *argv[]){   
    Base* b = new Child();
    b-&gt;DoSomething();
    delete b;
}</pre>
<pre lang="cpp" escaped="true">}</pre>
Produces the following output:
<pre lang="bash">bash $ ./a.out
Hello from Child</pre>
This works, and its a familiar idiom. However virtual functions have a some performance issues. Since the call isn't bound until until runtime, the methods cannot be inlined, and will probably incur a cache miss [1. <a href=" http://coldattic.info/shvedsky/pro/blogs/a-foo-walks-into-a-bar/posts/3">A foo walks into a bar</a>] , which on modern processors with the very deep caches is a very costly effect.

<a href="http://www.codestrokes.com/wp-content/uploads/2012/02/Untitled-1.png"><img class="aligncenter size-full wp-image-533" title="Normalized Virtual Performance" src="http://www.codestrokes.com/wp-content/uploads/2012/02/Untitled-1.png" alt="" width="605" height="340" /></a>

Secondly, even with cacheing aside virtual functions are about 2.5 times slower than direct function calls; where as inlining, i.e. zero-function overhead is about 20 times faster [1. <a href="http://assemblyrequired.crashworks.org/2009/01/19/how-slow-are-virtual-functions-really/">How Slow Are Virtual Functions Really</a>]. So this is a major issue is performance critical code, such as games. The EA directly states that virtual functions forbidden in their code [1. <a href="http://assemblyrequired.crashworks.org/2008/12/22/ea-stl-prevents-memory-leaks/#more-92">How the EA prevents Memory Leaks</a>].  However, polymorphism is a powerful tool. Are we relegated to a "lower" form of Object-Orientation with writing performance critical code? No. In fact the opposite is true.  C++'s template system is powerful and allows us to add dnasicm at compile time.

We can implement the same behavior as the UML figure above using templates. This improves the performance of our code in two ways. Firstly, by omitting virtual function we pickup a ~2.5x boost. Secondly, by using composition instead of inheritance we also get a small bump, and the compiler is more likely to inline the "inner" function.
<pre lang="cpp" escaped="true">template &lt;typename ChildType&gt;
struct Base {
    Base (){}
    virtual ~Base2 (){}
    void DoSomething() {
        myChild.DoSomething(); // This is the "inner" function.
    }
private:
    ChildType myChild;
};

struct Child /* Notice the lack of inheritance here */{
    Child () {}
    virtual ~Child(){}
    void DoSomething(){
        cout &lt;&lt; "Hello from Child." &lt;&lt; endl;
    }
};</pre>
Our driver is similar to before, except for the instantiation. Instead of inheriting behavior from a base class and overriding it, the Child, or implementing type, is passed in as an instantiation argument. This creates a new type, which is the dynamic behavior we want. Using the following driver code, we achieve the same output as before.
<pre lang="cpp" escaped="true">int main(int argc, char const *argv[]){   
    Base&lt;Child&gt;* b = new Base&lt;Child2&gt;();
    b-&gt;DoSomething();
    delete b;
}</pre>
C++11 (-std=c++0x in gcc4.6) allows one 1 more improvement in the driver code to prevent memory leaks.
<pre lang="cpp" escaped="true">int main(int argc, char const *argv[]){   
auto b2 = make_shared&lt;Base2&lt;Child2&gt; &gt;();
b2-&gt;DoSomething();
//Notice we don't have to call delete. Woot, exception safety!
}</pre>
So polymorphism is a powerful tool for creating dynamicism in programs, however with the inherent [1. Pun intended] performance issues the standard form of polymorphism is not the tool for every job. C++ templates allow use a manageable way to achieve similar behavior at compile time!

<hr />

<h4>References</h4>
