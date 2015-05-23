+++
date = "2011-05-08T23:59:00-07:00"
draft = false
title = "The Red-Black Tree"
slug = "the-red-black-tree-part-1"
tags = ["C++", "comparison", "D", "Data Structure", "Tree"]

+++
<a title="C++ Source Code" href="https://bitbucket.org/jwright/cse310-red-black-tree/overview">C++ Source Code</a>
<a title="D Source Code" href="https://bitbucket.org/jwright/red-black-tree-d">D Source Code</a>

D provides a number of features that simplify designing software, especially in the embedded environment.  I will show in this 2 part comparison, between C++ and D, that D helps one write <strong>correct code</strong>.  Correct code is something <a href="http://erdani.com/" target="_blank">Andrei Alexandrescu</a>, stresses heavily as a prominent feature of D.   I use the Red-Black Tree for such a comparison since its complicated enough to make memory management difficult, while retaining real-world application.

<!--more-->

C++ makes memory management difficult in practice. Memory management, an incidental complexity of C++, is especially difficult in the presence of exceptions. O<span style="color: #000000;">ur goal is to make a fast, correct data structure, not </span><span style="color: #000000;">manage memory.  C++ obfuscates this goal. </span>

<span style="color: #000000;">There are a few idioms in C++ to help; Resource Acquisition Is Initialization, or RAII for short, states that “…the only code that can be guaranteed to be executed after an <a href="http://en.wikipedia.org/wiki/Exception_handling">exception</a> is thrown are the <a href="http://en.wikipedia.org/wiki/Destructor_%28computer_science%29">destructors</a> of objects residing on the <a href="http://en.wikipedia.org/wiki/Stack_%28data_structure%29">stack</a> (<a href="http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization" target="_blank">Wikipedia</a>)”. Smart Pointers help achieve this.  The Smart pointer offloads much of this responsibility, hiding the complexity, thereby allowing the programmer to focus solely on the task at hand.</span> I use an idiom I learned from my friend <a href="http://www.chrisanderman.com/" target="_blank">Chris</a>, to hide all raw pointers.
<pre lang="cpp" escaped="true">#include 

//Smart Class Idiom for RAII in C++
class SmartClass
{
public:
    typedef std::tr1::shared_ptr Ptr;
    typedef std::tr1::weak_ptr WeakPtr;
    static SmartClass::Ptr construct(arguments)
    {
	SmartClass::Ptr c(new SmartClass());
	c-&gt;self = c;
	return c;
    }

    virtual ~SmartClass();
private:
    SmartClass();
    SmartClass::WeakPtr self;

};</pre>
This is a very useful pattern for managing memory. The developer is not required to call delete, the smart pointer will do it automatically. Memory management is still not automatic, however. The programmer needs to resolve the smart vs. weak pointer relationship.  While this strong vs. weak is a much simpler question than determining the full <em>object lifecycle, </em><strong>considerable effort</strong> is still placed into managing memory. This detracts from our goal, while simultaneously, unnecessarily increasing our software’s complexity.

Firstly, what is a red-black tree? The <a href="http://en.wikipedia.org/wiki/Red-black_tree" target="_blank">Red-Black tree</a> is an interesting data structure because it provides a <em>balanced</em> binary tree.  There are several types of self-balancing binary trees available, AVL trees being one. The Red-Black tree, however, uses a less strict balancing mechanism than the AVL tree; this makes insertions to a Red-Black tree faster. Deletions are slower than an AVL tree. The Red-Black tree uses graph coloring to determining overall balance of the tree.

Balance is an important property of a binary tree to maintain algorithmic complexity. If there is not a rebalancing scheme in place, a BST can, depending on what order <em>keys</em> are inserted, fill out as a linked list. Searching a linked list is O(n) or “linear” time, not the preferable O(log n).

<em><a href="http://scienceblogs.com/goodmath/2009/11/advanced_haskell_data_structur.php"><img style="display: block; float: none; margin-left: auto; margin-right: auto;" src="http://scienceblogs.com/goodmath/upload/2007/01/unbalanced-trees.jpg" alt="" /></a></em>

The Red-Black tree uses graph coloring to maintain balance. Balance guarantee’s O(log n) search performance.
<h3>C++ Insert</h3>
<pre lang="cpp" escaped="true">void RedBlackTree::Insert(uint32_t key)
{
    RedBlackNode::Ptr z = RedBlackNode::construct(key);
    RedBlackNode::Ptr x = root;
    RedBlackNode::Ptr y = nil;

    while(x != nil)
    {
        y = x;
        if(z-&gt;Key() &lt; x-&gt;Key())
            x = x-&gt;Left();
        else
            x = x-&gt;Right();
    }

    z-&gt;Parent(y);
    if(y == nil)
        root = z;
    else if(z-&gt;Key() &lt; y-&gt;Key())
        y-&gt;Left(z);
    else
        y-&gt;Right(z);
    z-&gt;Left(nil);
    z-&gt;Right(nil);
    z-&gt;Color(RedBlackNode::RED);
    Insert_Fixup(z);
}</pre>
There are a few issues with this implementation.  If an exception occurs while inserting a node, the Insert_Fixup() doesn’t get run.  An exception in this code, will not cause a memory, leak, however it will leave the tree in an indeterminate state. Any subsequent insertion into the tree will cause Insert_Fixup() to fail. This is <strong>NOT</strong> correct code.
<h3>C++ Delete</h3>
<pre lang="cpp" escaped="true">void RedBlackTree::Delete(uint32_t key)
{

    RedBlackNode::Ptr z = Search(key);
    RedBlackNode::Ptr x;
    if(z == nil)
        return;

    RedBlackNode::Ptr y = z;
    RedBlackNode::color_t original_color = y-&gt;Color();
    if(z-&gt;Left() == nil)
    {
        x = z-&gt;Right();
        Transplant(z,z-&gt;Right());
    }
    else if(z-&gt;Right() == nil)
    {
        x = z-&gt;Left();
        Transplant(z,z-&gt;Left());
    }
    else
    {
        y = Minimum(z-&gt;Right());
        original_color = y-&gt;Color();
        x = y-&gt;Right();
        if(y-&gt;Parent() == z)
        {
            x-&gt;Parent(y);
        }
        else
        {
            Transplant(y,y-&gt;Right());
            y-&gt;Right(z-&gt;Right());
            y-&gt;Right()-&gt;Parent(y);
        }
        Transplant(z,y);
        y-&gt;Left(z-&gt;Left());
        y-&gt;Left()-&gt;Parent(y);
        y-&gt;Color(z-&gt;Color());
    }
    if(original_color == RedBlackNode::BLACK)
    {
        Delete_Fixup(x);
    }
}</pre>
The Smart Pointer pointer idiom really flexes its power here. The most difficult part about the Red-Black Tree implementation is deleting nodes. One needs to be careful not to <span style="color: #0000ff;">delete </span><span style="color: #000000;">nodes too soon and cause a <a href="http://en.wikipedia.org/wiki/Dangling_pointer"><em>dangling-pointer</em></a><em> </em>yet, its important that one does delete the nodes to prevent a leak memory, however as you can see there are no delete calls above. The Smart Pointers handle delete when the node falls out of scope.  This implementation does not leak memory! (See the valgrind scripts for evidence).  That is a powerful statement in C++, and difficult to achieve with manual memory management. </span>

<span style="color: #000000;">Additionally, smart pointers indirectly offer a very powerful tool: Division of responsibility. The Smart pointers are responsible for managing memory. In the spirit of the <em>Single-Responsibility-Theorem</em>, they only manage memory, and they do it well. So well, that the developer can focus on the algorithm alone, instead of disrupting the flow with extra memory management code. </span>
<h4>Conclusion</h4>
<span style="color: #000000;">Excellent! We have a self-balancing BST, that doesn’t leak memory, however is this code correct? No. It is possible, that an exception will leave the tree in a bad state, thereby invalidating the entire structure.  We need a mechanism that provides transactional semantics.  This is difficult in C++, especially due to the <a href="http://en.wikipedia.org/wiki/Exception_handling_syntax#C.2B.2B">lack of a <span style="color: #0000ff;">finally</span> statement</a></span><span style="color: #0000ff;">.</span>

It’s important to understand that smart pointer’s are not a panacea. They do not solve all memory management issue in C++. There are still artifacts of memory management without our algorithm, detracting from the simplicity of our design.  Without a comprehensive memory solution, we will never lose this incidental complexity.

D provides a number of features that helps one write transactional, <strong>correct</strong> code. One issue, is in C++, exceptions are much of a “bolt-on” feature.  Much as exceptions are pervasive in our daily lives so in D, exceptions are pervasive in the language.  Its naïve to believe that code will not fail, yet this is how exception management in C++ feels. As evidence of this, one may throw an exception from anywhere in D, even in a destructor; C++ cannot do <a href="http://www.parashift.com/c++-faq-lite/exceptions.html#faq-17.9">this</a>.

In Part 2, we’ll look at how D’s exception management, garbage collection, and the <a href="http://www.d-programming-language.org/exception-safe.html">scope() statement</a> help us write clear, correct code, while lowering incidental complexity.
