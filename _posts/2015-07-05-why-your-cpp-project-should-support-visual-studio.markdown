---
layout: post
author: Jeremy
date: 2015-07-05 00:00:00+00:00
slug: your_cpp_project_should_support_visual_studio
title: Your C++ Project should support Visual Studio
draft: true
expiryDate: 2020-01-01T00:00:00+00:00
languages:
- C++
tags:
- open-source
---

Coming from a Linux background, and knowing that my four readers are Linux
guys, I write this article with great trepidation. This article is likely to
induce _unsubscribe_ urges in 75% of my reader-base. I hear you. This is not
some fan boy with the common, "Linux is too hard." Or "I need a good IDE".
I've seen the visual C++ compiler (in debug mode) catch some fantastic
defects. 

> Running your unit tests compiled with Visual C++'s <tt>/MTd</tt> will
> increase your code quality.

<!--more-->

# All compilers are great!

This article could easily be titled, "Your C++ project should support
valgrind" which is entirely true. Equally true that your C++ project should
support clang. I love writing in the clang compiler environment. The debug
errors are ascii-art! How great is that? &mdash; Great! 

Similarity, Valgrind is a beautiful tool for
tweaking performance, and finding difficult, non-deterministic memory bugs.
The Visual C++ compiler has something that these two platforms lack: iterator
debugging. 

# Iterator Debugging

Iterator debugging is a feature of the debug version of Visual C++'s standard
library. It enforces iterator validity with debug asserts. The asserts are
triggered by standard rules, ensuring that you code uses iterators correctly
even if the code may work otherwise. Ensuring correctness is an improvement
over "it works" since one day it won't work. For example, take this simple
snippet of code.

```cpp
#include <iostream>
#include <vector>
#include <utility>

int main()
{
    std::vector<int> v{1,2,3,4,5};
    auto i = std::begin(v);
    v.push_back(6);
    std::cout << *i << '\n';   
    return 0;
}
```

Do you see the defect? Compiling this on g++ results in no errors, and
compiling on Visual C++ results in no errors as well. However compiling with
the debug standard library offers a wonderful insight to the correctness of
your program. 

# OMG I hate Visual Studio's solution files

The Visual C++ compiler has a reputation for poor standards support, and
lacking modern C++ features. Yeah, me too. Its a whole other world to learn
the property pages for Visual Studio. However I use Visual C++ just as I use
gcc for small projects.  I compile from the command line. 

```bash
C:\> cl /Ehsc /MTd program.cpp
```
Its quick, easy. 

# Get Paid help, for free
Most users of Visual C++ are professional programmers working on commercial
software packages.  If your open source project uses a permissive license, and
already supports building with Visual Studio its likely inclusion in a large
projects will increase the test coverage of your project. I know for myself,
when I include an open source project on my work, I push all enhancements
upstream to express our gratitude. 

# Conclusion
It is interesting that we have so many differing competing compilers
available. Rust on the other hand doesn't have a standard but instead there is
a single compiler that forms the defacto standard of the language. Luckily we
as C++ developers have multiple compilers available each with different
strengths. By compiling our programs with multiple compilers we will increase
the quality of our programs by leveraging each platform's individual
strengths.

