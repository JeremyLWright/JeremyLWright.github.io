---
author: Jeremy
comments: true
date: 2011-10-23 19:00:21+00:00
layout: post
slug: making-c-like-python-the-anderson-smart-pointer-pattern
title: 'Making C++ like Python: The Anderson Smart Pointer Pattern'
wordpress_id: 468
tags:
- Coding
- memory
- Python
- RAII
languages: 
- C++
- D
---

Choosing to use C++ brings the additional complexity of memory management.  Dennis Ritchie once stated: The C Programming Language — A language which combines the flexibility of assembly language with the power of assembly language. C++ inherits much of that _flexibility, _however, this [incidental complexity](http://www.infoq.com/presentations/Are-We-There-Yet-Rich-Hickey), can be relegated to a single class, leaving you with the high-level elegance of Python. RAII help with this additional complexity, however without a pattern for guidance implementing RAII consistently can be difficult, defeating the safety it provides.

<!-- more -->

Resource Acquisition Is Initialization ([RAII](http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization)) is a powerful tool for managing resources.  RAII [justifies](http://www.research.att.com/~bs/bs_faq2.html#finally) the apparent missing finally clause. Stroustrup claims that with proper RAII,  [finally](http://www.research.att.com/~bs/bs_faq2.html#finally) is not required. D also [implements](http://www.d-programming-language.org/exception-safe.html) RAII with scope operators. Ok, so RAII is powerful, but what is it?

In C++, destructors are the only entity guaranteed to execute after an exception.  So resources which need to be automatically reclaimed need  to acquire at initialization, and release at destruction.  Such resources must be declared on the stack, to permit this idiom.

Writing exception-safe code, e.g. managing resources throughout exceptions is difficult, and while RAII makes it easier, managing RAII correctly is difficult without a pattern. A colleague of mine, [Anderson](http://www.chrisanderman.com/), developed a fantastic pattern/[policy](http://erdani.com/publications/cuj-2005-12.pdf) using smart pointers which makes RAII automatic.

Two patterns compose the Anderson Smart Pointer Pattern: Factory Constructor, and PIMPL.

    
    #ifdef _WIN
    #include <memory>
    #else
    #include <tr1/memory>
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
        c->self = c;
        return c;
    }




This pattern is used as an RAII [policy](http://erdani.com/publications/cuj-2005-12.pdf). Using the pattern liberally can eliminate new and delete from your program, and you will not leak memory. Even with multiple exceptions, you're [program will not leak](https://bitbucket.org/jwright/cse310-red-black-tree/overview).  Creating an instance of an RAII class is easy now:



    
    Name::Ptr myInstance = Name::construct();




This Pattern will make one extra virtual call as it performs the reference counting, but the performance hit is typically nominal compared to the safety it provides to the system. The Anderson Smart-Pointer Pattern increases robustness of your programs, but interestingly it also provides a new elegance. Since one is not managing memory, and resources constantly, it makes C++ perform more like a high level language. For example, I implemented a [red black tree](https://bitbucket.org/jwright/cse310-red-black-tree/src/d787e75b724a/BaseCode/RedBlackTree.cpp#cl-137) using this pattern.  I didn't need to worry about deleting nodes, just the requirements of my program. With the incidental complexity relegated to a single class, I am left with the elegant, expressiveness of Python, yet retain the raw performance of C++.
