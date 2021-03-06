---
author: admin
comments: true
date: 2013-07-07 23:00:30+00:00
layout: post
slug: patterns-are-evidence-of-a-languages-lacking
title: Patterns are evidence of a language's lacking
wordpress_id: 875
categories:
- Algorithm
tags:
- DSL
- pattern
---

A coworker of mine stated something interesting, "...a pattern is evidence of missing feature in the language...". At first I struggled with this statement. How can you design a language general enough to be widely used, and simultaneously cover all the desirable idioms such that patterns are built in? At first this seemed silly to me, until I heard Erik Meijer state in a Haskell lecture, "..this is why we implemented LINQ as a pattern instead of a language feature..."

<!-- more -->

It's an interesting concept that a language is responsible for reducing patterns into the language itself. My coworker cited that subroutines were once a pattern for managing groups of functionality. Wikipedia defines a design pattern as a solution to a common problem in software engineering. In this respect, subroutines indeed were a pattern to assembly programmers.  Complex Instruction Sets allowed for a very different programming model than today’s assembly languages who are intended primarily for compilers, but humans. In this environment parameter passing was defined by convention, and even a companies coding standard. Adding a standard method for parameter passing, i.e. stack organization would massive improve productivity. C solved this and did so extremely efficiently. C’s parameter passing syntax makes it easy for programmers to describe small abstractions of functionality into individual blocks, or subroutines. Thus the language incorporated a prevalent pattern from industry.

Additionally, by incorporating this pattern into the syntax, the compiler writer is free to change the underlying implementation for each architecture. The PIC for instance has a hardware stack, thus the default pattern offered for some assemblers wouldn’t work directly. Ostensibly, one could adjust the pattern to work, and this is the recommended practice of patterns, to adjust their structure to fit the existing architecture however this incurs technical debt. Both in the original design to develop the correct adjustments to the pattern, as well as maintenance since the maintenance programmer is most likely left to rediscover the pattern’s structure. Thus while the subroutine pattern originally intended to reduce the complexity, once modified it incurs a new technical debt, translating the complexity to another part of the system. Luckily, Microchip offers a C compiler for the PIC thus, the syntax of C abstracts out the different methods the PIC manages a stack from different architectures. This is a massive productivity booster, and since the mechanical structure of a subroutine is abstracted away by the compiler, systems don’t incur the technical debt caused by modifying the pattern for this specific hardware.

So what is a language without patterns? I suspect such a language would by necessity be domain specific. Take the subroutine pattern again. C abstracted the subroutine into it’s syntax, much has Haskell has a function syntax. Haskell’s lazy semantics however have a more elaborate functional call hierarchy, as such ghc allocates all “stacks” as heap objects. In a talk Simon Peyton-Jones mentions that this made the LLVM port of Haskell more difficult. LLVM has a specific construct for stack allocated objects outside Haskell’s semantics. Currently, the LLVM backend is fantastic, and offers fantastic performance, especially for SIMD type programs, so the problem is obviously resolved. However it offers evidence to the point that any specific implementation forgoes some use cases.

I personally, like patterns, especially since they give programmers a common vocabulary for communicating complex structures, and behaviors. Domain specific languages are becoming a very popular topic. My latest studies of Haskell, show many such languages. Each program designing a domain specific language for the given requirements. Perhaps this is the future patterns, and programming in general. Future idioms may in fact encourage the implementation of domain specific languages, in which the required software is written.

Reference:



	
  * [http://blog.plover.com/prog/design-patterns.html](http://blog.plover.com/prog/design-patterns.html)

	
  * [http://en.wikipedia.org/wiki/Complex_instruction_set_computing](http://en.wikipedia.org/wiki/Complex_instruction_set_computing)

	
  * [http://en.wikipedia.org/wiki/IBM_Basic_assembly_language](http://en.wikipedia.org/wiki/IBM_Basic_assembly_language)

	
  * [http://channel9.msdn.com/Series/C9-Lectures-Erik-Meijer-Functional-Programming-Fundamentals/Lecture-Series-Erik-Meijer-Functional-Programming-Fundamentals-Chapter-1](http://channel9.msdn.com/Series/C9-Lectures-Erik-Meijer-Functional-Programming-Fundamentals/Lecture-Series-Erik-Meijer-Functional-Programming-Fundamentals-Chapter-1)

	
  * [http://www.haskell.org/pipermail/glasgow-haskell-users/2007-January/011838.html](http://www.haskell.org/pipermail/glasgow-haskell-users/2007-January/011838.html)


