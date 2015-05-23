+++
date = "2011-05-12T19:40:00-07:00"
draft = false
title = "Class Invariants"
slug = "class-invariants-red-black-tree-part-2"
tags = ["D", "correct code"]

+++
This week, I started porting my <a href="http://www.codestrokes.com/archives/59">C++ implementation</a> of the Red-Black tree to D.  I am trying to pay special attention to the features of D, intended to make writing correct code easier. While on that vane,  I was reading an excellent <a href="http://reprog.wordpress.com/2010/04/25/writing-correct-code-part-1-invariants-binary-search-part-4a/">article</a>, discussing invariants, and I was pleased to find such a useful implementation of the <a href="http://www.digitalmars.com/d/2.0/class.html#Invariant">class invariant</a> in the D language.

<!--more-->

Invariants come from the same “<a href="http://en.wikipedia.org/wiki/Design_by_contract">design-by-contract</a>” idiom, famous for pre- and post- conditions. Essentially, invariants describe a state, or behavior which must remain true for a class.  If the invariant fails, during the classes life-cycle something is wrong; either the assumptions underlying the class’s behavior (the invariant is wrong), or a bug in the class itself.  In either case, the invariant help the you, the developer find a problem.  While discussing this feature a colleague asked,
<blockquote>Why would I want to maintain a ‘fixed’ state in my class. How does this not interfere with the classes behavior?  I don’t see how I would use this in a nontrivial application.</blockquote>
<span style="color: #555555;">“How do I use this in a real application?” its quite a loaded question, however valuable. For my small red-black tree, I’m using invariants to check that the “<a href="http://en.wikipedia.org/wiki/Red-black_tree#Properties">black-height</a>” is maintained.  This is essential to the performance of the class, both in terms of correctness, and run-time complexity.  The Delete operation, for instance, will not function correctly if the black height is incorrect. This “black-height” is a property of the entire class as a whole, it must be maintained at all time for the class to be correct.  This is the very definition of the <a href="http://en.wikipedia.org/wiki/Class_invariant">class invariant</a>. Excellent! However this still doesn’t satisfy our question; in a more general context, how does the class invariant help us? </span>

<span style="color: #555555;">The intent of the class invariant is to maintain a <strong>consistent state</strong>, not a fixed one.  Consistency is an important concept we work hard to maintain in our programs. Instead of a class, with its mutable state, lets look at a simpler construct in programming, a loop. </span>

<span style="color: #555555;">The loop conditional can be thought of as an invariant for that scope. When the invariant is no longer true, the work of our loop is done.  For example:</span>
<pre escaped="true" lang="cpp">for (size_t i=0; i &lt; string.length(); ++i)
{
	//do something...
}</pre>
The, <em>i &lt; string.length(), </em>is a simple invariant in that it must remain true through the life of the loop.  We cannot allow our index <em>i </em>to grow unbounded, or risk causing a segfault. Invariants, therefore, are an intimate part of controlling program consistency. Especially consistency through multiple states. We extend this concept to the class to keep a consistent view of data, or some more dynamic property.

So invariants are good, they help one question their design assumptions, and maintain class consistency. What does D provide to help us use this? The <a href="http://www.digitalmars.com/d/2.0/class.html#Invariant">class invariant</a>.
<pre escaped="true"  lang="d">class RedBlackTree {
    public:
        this()
        {
            nil = new RedBlackNode(0);
            nil.Left = nil;
            nil.Right = nil;
            nil.Parent = nil;
            nil.Color = RedBlackNode.Colors.BLACK;
            root = nil;
        }
        ~this(){ }

        unittest
        {
		///TODO fill out the unit tests.
        }

        invariant()
        {
            //Check the black height is equal across all simple paths
            assert(verify_black_height() == true);
        }</pre>
D provides a custom function that will automatically be called before and after any public method is called.  This functionality is compiled out in release versions. So when the class is <a href="http://en.wikipedia.org/wiki/Open/closed_principle">closed</a>, we can compile for release and automatically remove the runtime overhead. This makes for an extremely useful, yet low-cost vector toward writing <strong>correct code</strong>.

D’s support for class invariants helps one achieve correct code simply, and concisely.  The language support permits the asserts to be checked automatically with minimal affect to the programmer’s flow. The class invariant contracts do not affect final performance in release builds. Consequently, invariants are a powerful tool in the quest for correct code and D leverages that perfectly!
