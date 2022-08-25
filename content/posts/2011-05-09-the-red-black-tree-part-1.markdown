---
author: Jeremy
comments: true
date: 2011-05-09 06:59:01+00:00
layout: post
slug: the-red-black-tree-part-1
title: The Red-Black Tree
wordpress_id: 59
tags:
- Algorithm
- comparison
- Data Structure
- Tree
languages:
- C++
- D
---

[C++ Source Code](https://bitbucket.org/jwright/cse310-red-black-tree/overview)
[D Source Code](https://bitbucket.org/jwright/red-black-tree-d)

D provides a number of features that simplify designing software, especially in the embedded environment.  I will show in this 2 part comparison, between C++ and D, that D helps one write **correct code**.  Correct code is something [Andrei Alexandrescu](http://erdani.com/), stresses heavily as a prominent feature of D.   I use the Red-Black Tree for such a comparison since its complicated enough to make memory management difficult, while retaining real-world application.

<!--more-->

C++ makes memory management difficult in practice. Memory management, an incidental complexity of C++, is especially difficult in the presence of exceptions. Our goal is to make a fast, correct data structure, not manage memory.  C++ obfuscates this goal. 

There are a few idioms in C++ to help; Resource Acquisition Is Initialization, or RAII for short, states that “…the only code that can be guaranteed to be executed after an [exception](http://en.wikipedia.org/wiki/Exception_handling) is thrown are the [destructors](http://en.wikipedia.org/wiki/Destructor_%28computer_science%29) of objects residing on the [stack](http://en.wikipedia.org/wiki/Stack_%28data_structure%29) ([Wikipedia](http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization))”. Smart Pointers help achieve this.  The Smart pointer offloads much of this responsibility, hiding the complexity, thereby allowing the programmer to focus solely on the task at hand. I use an idiom I learned from my friend [Chris](http://www.chrisanderman.com/), to hide all raw pointers.
```cpp
#include <memory>

//Smart Class Idiom for RAII in C++
class SmartClass
{
public:
    typedef std::tr1::shared_ptr Ptr;
    typedef std::tr1::weak_ptr WeakPtr;
    static SmartClass::Ptr construct(arguments)
    {
        SmartClass::Ptr c(new SmartClass());
        c->self = c;
        return c;
    }

    virtual ~SmartClass();
private:
    SmartClass();
    SmartClass::WeakPtr self;

};
```


This is a very useful pattern for managing memory. The developer is not
required to call delete, the smart pointer will do it automatically. Memory
management is still not automatic, however. The programmer needs to resolve
the smart vs. weak pointer relationship.  While this strong vs. weak is a much
simpler question than determining the full _object lifecycle, _**considerable
effort** is still placed into managing memory. This detracts from our goal,
while simultaneously, unnecessarily increasing our software’s complexity.

Firstly, what is a red-black tree? The [Red-Black tree](http://en.wikipedia.org/wiki/Red-black_tree) is an interesting data
structure because it provides a _balanced_ binary tree.  There are several
types of self-balancing binary trees available, AVL trees being one. The
Red-Black tree, however, uses a less strict balancing mechanism than the AVL
tree; this makes insertions to a Red-Black tree faster. Deletions are slower
than an AVL tree. The Red-Black tree uses graph coloring to determining
overall balance of the tree.

Balance is an important property of a binary tree to maintain algorithmic
complexity. If there is not a rebalancing scheme in place, a BST can,
depending on what order _keys_ are inserted, fill out as a linked list.
Searching a linked list is O(n) or “linear” time, not the preferable O(log n).

[![](http://scienceblogs.com/goodmath/upload/2007/01/unbalanced-trees.jpg)](http://scienceblogs.com/goodmath/2009/11/advanced_haskell_data_structur.php)

The Red-Black tree uses graph coloring to maintain balance. Balance guarantee’s O(log n) search performance.


### C++ Insert

```cpp

    
    void RedBlackTree::Insert(uint32_t key)
    {
        RedBlackNode::Ptr z = RedBlackNode::construct(key);
        RedBlackNode::Ptr x = root;
        RedBlackNode::Ptr y = nil;
    
        while(x != nil)
        {
            y = x;
            if(z->Key() < x->Key())
                x = x->Left();
            else
                x = x->Right();
        }
    
        z->Parent(y);
        if(y == nil)
            root = z;
        else if(z->Key() < y->Key())
            y->Left(z);
        else
            y->Right(z);
        z->Left(nil);
        z->Right(nil);
        z->Color(RedBlackNode::RED);
        Insert_Fixup(z);
    }
```


There are a few issues with this implementation.  If an exception occurs while inserting a node, the Insert_Fixup() doesn’t get run.  An exception in this code, will not cause a memory, leak, however it will leave the tree in an indeterminate state. Any subsequent insertion into the tree will cause Insert_Fixup() to fail. This is **NOT** correct code.


### C++ Delete


```cpp    
    void RedBlackTree::Delete(uint32_t key)
    {
    
        RedBlackNode::Ptr z = Search(key);
        RedBlackNode::Ptr x;
        if(z == nil)
            return;
    
        RedBlackNode::Ptr y = z;
        RedBlackNode::color_t original_color = y->Color();
        if(z->Left() == nil)
        {
            x = z->Right();
            Transplant(z,z->Right());
        }
        else if(z->Right() == nil)
        {
            x = z->Left();
            Transplant(z,z->Left());
        }
        else
        {
            y = Minimum(z->Right());
            original_color = y->Color();
            x = y->Right();
            if(y->Parent() == z)
            {
                x->Parent(y);
            }
            else
            {
                Transplant(y,y->Right());
                y->Right(z->Right());
                y->Right()->Parent(y);
            }
            Transplant(z,y);
            y->Left(z->Left());
            y->Left()->Parent(y);
            y->Color(z->Color());
        }
        if(original_color == RedBlackNode::BLACK)
        {
            Delete_Fixup(x);
        }
    }
```


The Smart Pointer pointer idiom really flexes its power here. The most difficult part about the Red-Black Tree implementation is deleting nodes. One needs to be careful not to delete nodes too soon and cause a [_dangling-pointer_](http://en.wikipedia.org/wiki/Dangling_pointer)_ _yet, its important that one does delete the nodes to prevent a leak memory, however as you can see there are no delete calls above. The Smart Pointers handle delete when the node falls out of scope.  This implementation does not leak memory! (See the valgrind scripts for evidence).  That is a powerful statement in C++, and difficult to achieve with manual memory management. 

Additionally, smart pointers indirectly offer a very powerful tool: Division of responsibility. The Smart pointers are responsible for managing memory. In the spirit of the _Single-Responsibility-Theorem_, they only manage memory, and they do it well. So well, that the developer can focus on the algorithm alone, instead of disrupting the flow with extra memory management code. 


#### Conclusion


Excellent! We have a self-balancing BST, that doesn’t leak memory, however is this code correct? No. It is possible, that an exception will leave the tree in a bad state, thereby invalidating the entire structure.  We need a mechanism that provides transactional semantics.  This is difficult in C++, especially due to the [lack of a finally statement](http://en.wikipedia.org/wiki/Exception_handling_syntax#C.2B.2B).

It’s important to understand that smart pointer’s are not a panacea. They do not solve all memory management issue in C++. There are still artifacts of memory management without our algorithm, detracting from the simplicity of our design.  Without a comprehensive memory solution, we will never lose this incidental complexity.

D provides a number of features that helps one write transactional, **correct** code. One issue, is in C++, exceptions are much of a “bolt-on” feature.  Much as exceptions are pervasive in our daily lives so in D, exceptions are pervasive in the language.  Its naïve to believe that code will not fail, yet this is how exception management in C++ feels. As evidence of this, one may throw an exception from anywhere in D, even in a destructor; C++ cannot do [this](http://www.parashift.com/c++-faq-lite/exceptions.html#faq-17.9).

In Part 2, we’ll look at how D’s exception management, garbage collection, and the [scope() statement](http://www.d-programming-language.org/exception-safe.html) help us write clear, correct code, while lowering incidental complexity.
