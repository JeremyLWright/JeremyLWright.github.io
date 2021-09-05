---
author: admin
comments: true
date: 2013-07-14 23:00:11+00:00
layout: post
slug: is-monolithic-code-faster
title: Is Monolithic Code Faster?
wordpress_id: 704
languages:
- C++
tags:
- Compilation
- optimization
- performance
---

As a software engineer I have a vested interest in disproving this statement. Bjarne Stroustroup says C++ is designed to create efficient abstractions. A software engineer’s  job is to create simple [abstractions ](http://www.codestrokes.com/2012/09/abstraction-in-plain-english/)to complex systems. State machines form a large part of many systems. The other day, a co-worker came to me, and asked, “Is it better to make straight line code for each case statement, even if it repeats, or is it better to abstraction into functions and make the code ‘cleaner’.”  Is “cleaner” code faster?
<!-- more -->


## The Experiment


The experiment I propose is to make a peanut butter and jelly sandwich, using a finite state machine.

[caption id="attachment_1089" align="alignleft" width="97"][![sm](http://www.codestrokes.com/wp-content/uploads/2013/07/sm1-97x300.png)](http://www.codestrokes.com/wp-content/uploads/2013/07/sm1.png) State Machine expressed in 4 separate methods.[/caption]

The state machine has a series of steps, each of which take a number of ticks. The tick simply counts the  amount of time in each state. The ticks simulate work being done in that state. For this experiment we are defining monolithic code to mean a switch() statement with no function calls. For modular code we offer 3 solutions:



	
  1. a switch statement with the state code abstracted into functions. Each function then returns the state transition.

	
  2. States abstracted into C++ objects

	
  3. Lastly, a high level state machine using Boost MSM.




### Code Overview


For each state machine type, lets look at the an example state to compare their structure. Firstly, the "monolithic" state:

    
    case EAT_SANDWICH:
    if(step_tick <= 0 && sandwiches_to_eat <= 0) //We've eaten all sandwiches
    {
        step_tick = 20;
        s = GO_TO_WORK;
    }
    else if(step_tick <= 0) //We've eaten 1 more sandwich
    {
        --sandwiches_to_eat;
        step_tick = 10;
        s = REMOVE_BREAD;
    }
    // else Continue eating current sandwich
    break;


Here s is the state. At the top of the machine is a switch(s). When the ticks are up, the state transitions to the next state. In this case Go To Work or Remove Bread to make another sandwich.

    
    SandwichState_t eat_sandwich_process()
    {
        static int sandwiches_to_eat = 3;
        static int tick = 10;
        --tick;
        if(tick <= 0 && sandwiches_to_eat <= 0)
        {
            sandwiches_to_eat = 3;
            tick = 10;
            return REMOVE_BREAD;
        }
        else if(tick <= 0)
        {
            --sandwiches_to_eat;
            tick = 10;
            return GO_TO_WORK;
        }
        return EAT_SANDWICH;
    }


This state is the identical to the monolithic, except the state is moved into a function, and the state is returned instead of mutating a variable.

    
    int eat_sandwich()
    {
        static int sandwiches_to_eat = 3;
        static int tick = 10;
        --tick;
        if(tick <= 0 && sandwiches_to_eat <= 0)
        {
            sandwiches_to_eat = 3;
            tick = 10;
            s.f = remove_bread;
        }
        else if(tick <= 0)
        {
            --sandwiches_to_eat;
            tick = 10;
            s.f = go_to_work;
        }
        else
            s.f = eat_sandwich;
        return 0;
    }


This third method is a uses a function pointer s.f. State transitions are performed by mutating the function pointer, and jumping to it e.g. sf();

    
    Row < EatSandwich       , none  , GoToWork          , ResetTick, user_is_full   >,
    Row < EatSandwich       , none  , RemoveBread       , ResetTick, user_is_hungry >,


This is Boost's MSM. essentially, MSM is a domain specific language described completely within a C++ template.


## Results


[caption id="attachment_1097" align="alignleft" width="300"][![O2Speedups](http://www.codestrokes.com/wp-content/uploads/2013/07/O2Speedups-300x225.png)](http://www.codestrokes.com/wp-content/uploads/2013/07/O2Speedups.png) Speedup normalized against the monolithic case. (Compiled with O2 optimization)[/caption]

I started this project with the full intention of cheating to assure monolithic code is slower than "proper" code. However, the evidence shows, properly abstracted code can be faster, but there is a limit. As MSM shows one can take abstraction too far or too general such that performance becomes difficult. So How does this happen? One of the most impacting tool for code performance, caching, and compilers have a fancy trick to optimize cache performance. Inlining.


## Inlining


Function inlining is simply a copy-paste operation by the compiler to remove the overhead of a function call. In gcc, and Visual Studio, the compiler is free to inline any function it wills. Conversely, the inline keyword simply provides a suggestion or a hint to the compiler to inline a function. The compiler is free to ignore the suggestion. Once the compiler chooses to inline a function, it simply copies the source from the function and replaces the function call itself.

However, additional performance is offered beyond simply eliminating the CALL instruction. Optimization is performed in multiple passes. As such removing function calls, can simplify optimization techniques such as global-flow analysis, and register allocation. Therefore, once a function is inlined, additional performance tweaks may be made specific to the environment of the original call. This means the while a function may be optimized on it's own. It will be done so only once. However an inlined function, since the source of the function is laid directly into flow of the program, the compiler can optimize the function specific to that region.

Many language support function inlining. Java, C++ have an inline keyword. During compilation inlining seems straight forward, however what about dynamic languages? I was surprised to learn that Python inlines.  PyPy uses a Just-In-Time compiler to make inline decisions at runtime. The benefit of inline decisions deferred to runtime, is the JIT is able to see the full program at once, as opposed to only a single file at a time as a batch compiler does.


## Conclusion


Cleanly abstracted code can be faster than monolithic code. Even without cheating the benchmark :-).  Compilers make advanced optimizations, as such it's of little benefit to immediately make a blanket statement to try to beat the performance of an optimizing compiler. For dynamic languages, JIT systems make even more comprehensive enhancements offering staggering performance.

Reference:
[http://en.wikipedia.org/wiki/Inline_expansion](http://en.wikipedia.org/wiki/Inline_expansion)
[http://en.wikipedia.org/wiki/Inline_caching](http://en.wikipedia.org/wiki/Inline_caching)
[http://www.iecc.com/linker/linker11.html](http://www.iecc.com/linker/linker11.html)

[http://morepypy.blogspot.com/2011/02/pypy-faster-than-c-on-carefully-crafted.html](http://morepypy.blogspot.com/2011/02/pypy-faster-than-c-on-carefully-crafted.html)
