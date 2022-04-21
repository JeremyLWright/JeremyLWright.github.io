---
layout: post
author: Jeremy
comments: true
date: 2011-06-06 06:59:00+00:00
layout: post
slug: type-safe-variable-argument-lists
title: Type-Safe Variable Argument Lists
wordpress_id: 172
tags:
- Coding
- Algorithm
- D
- Type Safety
---

Type-safety is a popular topic. Perceived as a panacea for bad software, the Department of Defense implemented Ada.  The original thought was restriction synonymous with robustness. From this, opponents claim type safe languages place the programmer’s hands in handcuffs, thereby thwarting generic code. Modern languages, such as D, and Java leverage a statically checked type system with a focus on consistency, not restriction.  Modern type systems abet generic code, without sacrificing robustness.  Today, there seems to be a general trend toward strong typing.  Personally, I try to leverage the type system as a tool to ensure correct code.


<blockquote>D is a powerful  language, that statically checks code correctness via a strong type system, yet still offers flexible constructs.</blockquote>


D’s focus of code correctness, provides a strong type system, in a manner conducive to generic code.  D’s type-safe variable argument list is an example of this.<!--more-->

[Singularity](http://research.microsoft.com/en-us/projects/singularity/), [D](http://www.d-programming-language.org), [Verve](http://channel9.msdn.com/Shows/Going+Deep/Verve-A-Type-Safe-Operating-System), all make use of static typing as a tool to check program correctness.  Singularity is not a language, but rather an operating system written in a derivative of C# called [Sing#](http://en.wikipedia.org/wiki/Sing_Sharp).  Sing# exposes a statically check message passing system called channels for inter-process communication.  The Sing# compiler, [Bartok](http://en.wikipedia.org/wiki/Bartok_%28compiler%29), can statically verify space partitioning. Singularity calls this verification a software isolated process.


<blockquote>The SIP (Software Isolated Process) defined by the Singularity project demonstrate the incredible power of strong, static type checking.</blockquote>


The type guarantee within a SIP is so strong that Singularity doesn’t require a hardware MMU. Turning off the [MMU](http://en.wikipedia.org/wiki/Memory_management_unit) dramatically improves performance by essentially eliminating the cost of calling kernel code from application space.  Performance. That’s a pretty strong motivation for static type-checking.  Not to be left behind, D uses the [Safe-D](http://www.d-programming-language.org/safed.html) standard to make similar guarantees.  Furthermore, with a stricter environment leveraged by strong typing, the compiler may make extra optimizations to further improve performance.

Strong typing can increase performance, but its original intent was to improve robustness.  Ada typifies this.  Ada was developed by the Department of Defense for missiles and avionic equipment.  VHDL, a hardware description language based on Ada, attempts to make the same guarantees to improve dependability of custom hardware in FPGAs and ASICs. Yet, one possible example against strong typing is restriction prevents generic, flexible code, the proverbial “handcuffs”. This, however is a [moo point](http://www.urbandictionary.com/define.php?term=moo+point).

I worked on a logging mechanism for an avionic platform a few years ago.  This platform was written in C++ and the logging interface used a variable argument list.  Our coding standard strictly forbade variable argument lists. Despite this the developer wanted a _printf like _interface.  The code looked similar to the following.

    
    class BadIdea {
    public:
        BadIdea (){}
        virtual ~BadIdea (){}
        int datum;
    private:
    };
    
    void logging_function(int g, ...)
    {
        return;
    }
    
    int main(int argc, const char *argv[])
    {
        BadIdea y;
        logging_function(5, y);
        return 0;
    }


Luckily, gcc 4.5 notices that one cannot pass a class object (Non-POD type) to a variable argument list.  The compiler issues the following error.  This is correct behavior and an excellent use of static type checking.
`badidea.cpp: In function ‘int main(int, const char**)’:
badidea.cpp:18:22: error: cannot pass objects of non-trivially-copyable type
‘class BadIdea’ through ‘...’`
Sadly, however C++ has not always done this.  Instead the error was similar to the following.
`badidea.cpp: In function ‘int main(int, const char**)’:
badidea.cpp:18:22: warning: cannot pass non POD type through ‘...’
call will abort at runtime`
Call will _abort_ at runtime! This is only a warning? Seriously? Yes, this bug took our team several weeks to find.  The build system didn’t turn on warnings, so we never saw this.  As an aside this is an excellent argument for treating all warnings as errors.  The intention was a generic interface, yet C++’s type system wouldn’t support this. We turned on warnings, but left the offending code. The offending code flies to this day.

This week I implemented a bloom filter in D. A bloom filter is a statistical data structure similar to a hash table; however, unlike a hash table, a bloom filter stores “if” the data exists, instead of the data itself. Common in large data environments, such as BigTable, bloom filters use a number of hash functions when inserting and querying the data structure. The number of hash functions used is called k, where k’s value determines the false positive rate. Increasing k lowers the false positive rate, but the tradeoff is that it also increases the time to insert an element.


<blockquote>D is great at providing a simple way to implement exactly what one needs.</blockquote>


Implementing the hash functions as part of the bloom filter is a violation of the single-responsibility theorem.  Since the number of hash functions control the false positive rate, _and _the overall performance of the structure, the user should be able to control the hash functions.  The bloom filter’s sole purpose is store a value’s availability, nothing more.  Therefore, I needed to allow the user to pass in some arbitrary number of hash functions into the bloom filter.  D provides variable argument lists, but better still, it provides a type-safe version. The bloom filter’s constructor looks like the following.

    
    /**
     * Create a Bloom filter of a specified size.
     * Params:
     *	size = The number of bits for the bloom filter.
     *	hash_fns =	accept an arbitrary number of hash functions as a
     *     strongly typed array of function pointers.
     */
    this(size_t size, uint function(string)[] hash_fns ...)
    {
        this.hash_functions = hash_fns;
        a.length = size;
    }
    
    /* ... */
    int main(...)
    {
          /* Pass 2 function pointers to the variable argument list */
          Bloom b1 = new Bloom(5, &sax_hash, &sdbm_hash);
    }


The bloom filter has no idea how big the hash list is, it just uses the hash functions generically.

    
    void add(string s)
    {
        foreach(fn; hash_functions)
        {
            a[fn(s)%a.length] = 1; //a is a BitArray from std.bitmanip
        }
    }


Excellent, no warnings. Statically typed interface, yet generic and flexible.  D truly is a fantastic language.

D provides a strongly typed variable argument list, to make code generic while maintaining correctness.  In fact D’s type system is very strong, and even provides a “safe” subset of the language to further increase the strictness.  Modules may be categorized into 1 of 3 classes: @safe, @trusted, @system.  The categories restrict which modules may be linked together, ensuring that code who claims to be safe, continues to be. D is a powerful  language, that statically checks code correctness via a strong type system, yet still offers flexible constructs.
