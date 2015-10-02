---
author: Jeremy
comments: true
date: 2011-08-19 16:55:56+00:00
layout: post
slug: why-do-some-tutorials-use-stdcout-and-others-use-just-cout
title: Why do some tutorials use std::cout and others use just cout?
wordpress_id: 277
categories:
- C++ Beginner
tags:
- tutorial
---

<!-- more -->Many tutorials start "Hello World" like so:

    
    #include <iostream>
    using namespace std;
    int main()
    {
        cout << "Hello World" << endl;
        return 0;
    }


However sometimes, and in my opinion the more correct version is written:

    
    #include <iostream>
    int main()
    {
        std::cout << "Hello World" << std::endl;
        return 0;
    }




The difference between the 2 programs is the double colon (::).  This is called the **namespace resolution operator**.  C++ has a wonderful concept called namespaces.  Namespaces allow you to group or organize sets of objects into named collections.  That collection is called a namespace.  Namespaces are similar to URLs. Take www.codestrokes.com for example.  Read right-to-left, the URL breaks down the enormous internet into successively more specific collections. First the_ .com_ "namespace"; Then more specific the: _codestrokes_. Then a single server, the most specific: _www_.

C++ allows you to make a similar grouping structure, but instead of period (.) denoting the individual collections we use ::.  Ergo to create a similar structure in C++:

    
    namespace com {
        namespace codestrokes {
            class www {
                //This is the actual class, the "thing" we wanted.
            };
        } // End of the code strokes namespace.
    } //End of the com namespace


Now if we want to access the www object in our namespace we do:

    
    int main()
    {
        com::codestrokes::www myBlogInstance;
    }


Equivalently:

    
    using namespace com::codestrokes; //This is the key difference.
    int main()
    {
        www myBlogInstance;
    }


Namespaces allow you to define functions and classes without fear of clashing names with another class. Its is extremely useful, and a huge benefit over C.  So in the hello world example `cout` is an object that lives inside the `std` namespace.  If you want to access that function you need to resolve the namespace with the :: operator. So in effect the `using` statement is a shortcut.

In programming practice however, it is considered bad form to use a `using` statement for anything except the `std` namespace. It doesn't affect the size of your executable, its just a style issue.

So why do I claim `std::cout` is more correct than just `cout`? Namespace are a pervasive component of the language. If you gloss over them at the beginning then you could code for years without truly understand how simple, and fantastic namespaces are. So use namespaces. For personal projects, group your classes under your last name, just for practice. Namespaces are a good thing and can greatly simplify your software.
