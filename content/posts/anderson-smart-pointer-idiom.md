+++
date = "2011-10-23T12:00:00-07:00"
draft = false
title = "Making C++ like Python: The Anderson Smart Pointer Pattern"
slug = "making-c-like-python-the-anderson-smart-pointer-pattern"
tags = ["c++", "D", "Python", "RAII"]

+++
Choosing to use C++ brings the additional complexity of memory management.  Dennis Ritchie once stated: The C Programming Language — A language which combines the flexibility of assembly language with the power of assembly language. C++ inherits much of that <em>flexibility, </em>however, this <a href="http://www.infoq.com/presentations/Are-We-There-Yet-Rich-Hickey">incidental complexity</a>, can be relegated to a single class, leaving you with the high-level elegance of Python. RAII help with this additional complexity, however without a pattern for guidance implementing RAII consistently can be difficult, defeating the safety it provides.

<!--more-->

Resource Acquisition Is Initialization (<a href="http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization">RAII</a>) is a powerful tool for managing resources.  RAII <a href="http://www.research.att.com/~bs/bs_faq2.html#finally">justifies</a> the apparent missing finally clause. Stroustrup claims that with proper RAII,  <a href="http://www.research.att.com/~bs/bs_faq2.html#finally">finally</a> is not required. D also <a href="http://www.d-programming-language.org/exception-safe.html">implements</a> RAII with scope operators. Ok, so RAII is powerful, but what is it?

In C++, destructors are the only entity guaranteed to execute after an exception.  So resources which need to be automatically reclaimed need  to acquire at initialization, and release at destruction.  Such resources must be declared on the stack, to permit this idiom.

Writing exception-safe code, e.g. managing resources throughout exceptions is difficult, and while RAII makes it easier, managing RAII correctly is difficult without a pattern. A colleague of mine, <a href="http://www.chrisanderman.com/">Anderson</a>, developed a fantastic pattern/<a href="http://erdani.com/publications/cuj-2005-12.pdf">policy</a> using smart pointers which makes RAII automatic.

Two patterns compose the Anderson Smart Pointer Pattern: Factory Constructor, and PIMPL.
<pre lang="cpp" escaped="true">#ifdef _WIN
#include &lt;memory&gt;
#else
#include &lt;tr1/memory&gt;
#endif

class Name
{
public:
#ifdef _WIN
    typedef std::shared_ptr Ptr; //This uses the class as a namespace.
    typedef std::weak_ptr WeakPtr;
#else
    typedef std::tr1::shared_ptr Ptr;
    typedef std::tr1::weak_ptr WeakPtr;
#endif
    static name::Ptr construct(); //Factory Constructor
    virtual ~name();
private:
    Name(); //Notice the constructor is private
    name::WeakPtr self; //self (from python), replaces this
};

Name::Ptr Name::construct()
{
    Name::Ptr c(new Name());
    //Self completes the PIMPL idiom,
    //thereby hiding all behavior behind a safe, reference counted wall
    c-&gt;self = c;
    return c;
}</pre>
<div>This pattern is used as an RAII <a href="http://erdani.com/publications/cuj-2005-12.pdf">policy</a>. Using the pattern liberally can eliminate new and delete from your program, and you will not leak memory. Even with multiple exceptions, you're <a href="https://bitbucket.org/jwright/cse310-red-black-tree/overview">program will not leak</a>.  Creating an instance of an RAII class is easy now:</div>
<pre lang="cpp" escaped="true">Name::Ptr myInstance = Name::construct();</pre>
<div>This Pattern will make one extra virtual call as it performs the reference counting, but the performance hit is typically nominal compared to the safety it provides to the system. The Anderson Smart-Pointer Pattern increases robustness of your programs, but interestingly it also provides a new elegance. Since one is not managing memory, and resources constantly, it makes C++ perform more like a high level language. For example, I implemented a <a href="https://bitbucket.org/jwright/cse310-red-black-tree/src/d787e75b724a/BaseCode/RedBlackTree.cpp#cl-137">red black tree</a> using this pattern.  I didn't need to worry about deleting nodes, just the requirements of my program. With the incidental complexity relegated to a single class, I am left with the elegant, expressiveness of Python, yet retain the raw performance of C++.</div><!--{NETBLOG_EXPORT} MTA0MTgz -->
