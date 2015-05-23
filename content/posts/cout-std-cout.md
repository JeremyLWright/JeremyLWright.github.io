+++
date = "2011-08-19T23:00:00-07:00"
draft = false
title = "Why do some tutorials use std::cout and others use just cout?"
slug = "why-do-some-tutorials-use-stdcout-and-others-use-just-cout"
tags = ["tutorial"]

+++
<!--more-->Many tutorials start "Hello World" like so:

```cpp
#include <iostream>
using namespace std;
int main()
{
    cout << "Hello World" << endl;
    return 0;
}
```

However sometimes, and in my opinion the more correct version is written:

```cpp
#include <iostream>
int main()
{
    std::cout << "Hello World" << std::endl;
    return 0;
}
```

The difference between the 2 programs is the double colon (::).  This is called the <strong>namespace resolution operator</strong>.  C++ has a wonderful concept called namespaces.  Namespaces allow you to group or organize sets of objects into named collections.  That collection is called a namespace.  Namespaces are similar to URLs. Take www.codestrokes.com for example.  Read right-to-left, the URL breaks down the enormous internet into successively more specific collections. First the<em> .com</em> "namespace"; Then more specific the: <em>codestrokes</em>. Then a single server, the most specific: <em>www</em>.

C++ allows you to make a similar grouping structure, but instead of period (.) denoting the individual collections we use ::.  Ergo to create a similar structure in C++:

```cpp
namespace com {
    namespace codestrokes {
        class www {
            //This is the actual class, the "thing" we wanted.
        };
    } // End of the code strokes namespace.
} //End of the com namespace
```

Now if we want to access the www object in our namespace we do:

```cpp
int main()
{
    com::codestrokes::www myBlogInstance;
}
```

Equivalently:

```cpp
using namespace com::codestrokes; //This is the key difference.
int main()
{
    www myBlogInstance;
}
```

Namespaces allow you to define functions and classes without fear of clashing names with another class. Its is extremely useful, and a huge benefit over C.  So in the hello world example <code>cout</code> is an object that lives inside the <code>std</code> namespace.  If you want to access that function you need to resolve the namespace with the :: operator. So in effect the <code>using</code> statement is a shortcut.

In programming practice however, it is considered bad form to use a <code>using</code> statement for anything except the <code>std</code> namespace. It doesn't affect the size of your executable, its just a style issue.

So why do I claim <code>std::cout</code> is more correct than just
<code>cout</code>? Namespace are a pervasive component of the language. If you
gloss over them at the beginning then you could code for years without truly
understand how simple, and fantastic namespaces are. So use namespaces. For
personal projects, group your classes under your last name, just for practice.
Namespaces are a good thing and can greatly simplify your software.
