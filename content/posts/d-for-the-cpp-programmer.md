+++
date = "2011-05-17T20:06:00-07:00"
draft = false
title = "Class Invariants"
slug = "d-for-the-c-programmer-red-black-tree-part-3"
tags = ["D", "correct code", "C++", "comparison"]

+++
As a comparative study, I am porting a Red-Black Tree from C++ to the <a href="http://www.digitalmars.com/d/2.0/dmd-linux.html">D programming language</a> (<a href="http://www.codestrokes.com/archives/59">Part 1</a>, <a href="http://www.codestrokes.com/archives/83">Part 2</a>). Overall D is an easy, practical transition for the C++ programmer. D provides a number of features for implementing correct code, however it is D’s simplicity that makes it truly enticing as a replacement. While D retains <em>C Style Syntax, </em>it is considerably simpler than C++, especially in the presence of exceptions.

<!--more-->
<h3>Simple and Familiar</h3>
Readable code makes maintaining programs simpler, ergo cheaper.  D’s syntax stems from the same tree as C, allowing programmers to leverage their considerable experience; yet D comes with a number of useful changes to make code more readable, creating a simple, familiar environment.  This project was intended to expose the differences between D and C++.  Properties are an excellent example of a small change made in D, which reaps great benefit for readability.  Wait, what’s the problem? One can declare getters and setters in C++, isn’t that enough? I say no.  Take the following example in C++:
<pre lang="cpp" escaped="true">void RedBlackTree::Transplant(RedBlackNode::Ptr u, RedBlackNode::Ptr v)
{
    if(u-&gt;Parent() == nil)
        root = v;
    else if(u == u-&gt;Parent()-&gt;Left())
        u-&gt;Parent()-&gt;Left(v);
    else
        u-&gt;Parent()-&gt;Right(v);
    v-&gt;Parent(u-&gt;Parent());
}</pre>
Line 6 actually modified u’s right sibling (u-&gt;Parent()-&gt;Right()).  Where is the equal sign? There isn’t one. Experienced C++ programmers are used to looking at this deficiency as status quo.  However, its much easier in D to see the statement’s intent.
<pre lang="d" escaped="true">void Transplant(RedBlackNode u, RedBlackNode v)
{
	if(u.Parent == nil)
		root = v;
	else if(u == v.Parent.Left)
		u.Parent.Left = v;
	else
                u.Parent.Right = v;
	v.Parent = u.Parent;
}</pre>
D uses the property idiom to clearly show that an assignment is taking place.  This simple example is powerful.  Notice that the <em>syntax is nearly identical</em> between the 2 languages. This similarity makes it very easy for one to use their current C++ skills almost immediately.
<h3>C++ is Whitespace Sensitive</h3>
One of the biggest complaints I hear from new <a href="http://www.python.org">python</a> programmers is whitespace sensitivity.  Python uses whitespace as a method to control scope, something most editors do automatically anyway using indention.
<pre lang="python" escaped="true">def fn1(x):
    if(x is int):
        return 1+1;
    else:
        x = str(int(x) + 1)
        return x;</pre>
By forcing whitespace in the syntax braces (“{“ and “}”) are unnecessary, and all python programs look the same making it easier to share code.  It works well, and Python if very consistent in it’s implementation. C style languages are not whitespace sensitive, <strong>except</strong> special cases in C++.
<pre lang="cpp" escaped="true">void fn1()
{
	vector&lt;vector&lt;int&gt;&gt; stl_2d_vector; //Doesn't compile
	vector&lt;vector&lt;int&gt; &gt; stl_2d_vector; //Does compile
}</pre>
C++ uses the angle-brackets “&lt;” and “&gt;” for a number of functions:
<ol>
	<li>Templates</li>
	<li>Less-Than, Greater-Than comparison</li>
	<li>Bit-Wise Shifting</li>
	<li>Stream-Insertion Operator</li>
	<li>Stream-Extraction Operator</li>
</ol>
This isn’t so bad except that there are two separate, semantic classes here.  Sometimes the &lt; and &gt; characters are used to <strong>enclose text</strong> as in the &lt;int&gt; example above.  Otherwise, the &lt; and &gt; characters do <strong>not enclose text</strong> and form an independent operator.  Said another way, angle brackets can form a digraph operator, and can form a semantic grouping…depending on the context.  Context makes C++ difficult to read.

This is just one example of how the obtuse syntax of C++ makes writing a compiler as well as readable code, difficult.  In this example, the compiler is trying to treat the “&gt;&gt;” digraph as an operator, instead of grouping the template arguments.  The space between the 2 “&gt;” symbol allows the compiler to pair the angle brackets, enclose the template and compile the expression.

D provides a <a href="http://www.digitalmars.com/d/2.0/templates-revisited.html">consistent alternative</a>. Which leverage an existing operator for enclosing symbols, the parentheses.  D makes instantiating templates easy:
<pre lang="d">void fn1()
{
	vector!(vector!(int)) stl_2d_vector; //Does compile
	vector!(vector!(int) ) stl_2d_vector; //Still compiles
}</pre>
The “!” operator is always used as a unary operator. Sometimes it can be used as not or one’s complement (bit-twiddle) as in:
<pre lang="d">if( t != 1) //If T is not equal to 1
    //Do Something
t = !t; // One's complement t;</pre>
However, ! always means “I stand alone, and I modify the token to my right”.  When we create a template, the ! modifies the enclosing parenthetical statement to transform it to a template expression.  D does not overload operators, or tokens. D does not use context sensitive syntax.  D, like python, allows one to write very readable software.

D gives us tools to write <a href="http://www.codestrokes.com/archives/83">correct code</a>, and offers a simplified syntax that leverages our existing C++ experience.  Starting new projects in a new language is a daunting task, yet D offers a lower-risk path in upgrading to a modern language.  D isn’t perfect but it provides a number of features for C++ developers to start solving real problems, today.
