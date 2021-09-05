---
author: admin
comments: true
date: 2013-08-02 16:51:40+00:00
layout: post
slug: my-haskell-environment-for-project-euler
title: My Haskell Environment for Project Euler
wordpress_id: 1131
tags:
- Functional
- automake
- dependencies
- dependency
- euler
- generation
- make
- project euler
languages:
- Haskell

---

For the last several months I've been working on Project Euler in Haskell. My intent has been to learn Haskell, and grasp the functional concepts. While working on several problems it's important to have a workflow that allows for a fast cycle time. I spent some time with Cabal, attempting to build a scheme that works efficiently, but was unable to do so. Instead I setup a mix of cabal-dev, and make to build a fast workflow that allow for compiling, testing, common code libraries, and benchmarks. This post is a walk though of that workflow. <!-- more -->
My most important requirements is cycle time. I a minimum edit-compile-test/execute cycle. This helps me to clearly and quickly work on problems. Especially in compiled languages with libraries, and common code, it is important that a single code change is a single file recompiles a minimum of effort ([Joel Spoksky](http://www.joelonsoftware.com/articles/fog0000000043.html)). Therefore my Makefile must describe the dependencies, which themselves are dynamic as the code base grows and changes. Cabal supposedly does this, but Project Euler is uniquely outside the framework offered by cabal. In Project Euler, each solution is a single executable. The project itself is many executables. Maintaining a cabal files for that many executables does not meet my desire for dynamically managed dependencies. Instead I favor make; simple _make_. Therefore the requirements of my project euler environemnt are:



	
  1. Primary Requirement

	
    * Fast Cycle Time




	
  2. Secondary Requirements

	
    * Testing

	
      * Unit testing is a minimum, but haskell allows test generation which is something I plan to learn and use heavily.




	
    * Sandbox Dependencies

	
      * standard and contributed libraries i.e. libraries not written by me should not clutter the standard library search space e.g. /usr/local/ghc/lib...




	
    * Minimal Rebuilt

	
      * I must have a clean and simple test environment to run unit tests on my common modules, as well as any project file

	
      * I want changing source files, should only rebuild the tests affected by those changes.




	
    * Benchmarking

	
      * I must have a dependable and repeatable benchmark for evaluating my code. Project Euler encourages one to complete each solution in 1 minute. Benchmarking is useful to see the common code base improve over time, as well as assert all programs complete in the encouraged time limit.




	
    * Profiling

	
      * Profiling is essential, especially in Haskell, since laziness makes space complexity difficult to estimate.







	
  3. Tertiary Requirements:

	
    * Background Exploration

	
      * I am using Project Euler as a conduit to learn Haskell. As such, I must be able to explore random ideas in a meaningful way. Those changes should be preserved do I can go back and look at my past attempts.








With these requirements in mind, and 10 Project Euler solutions complete, I set out to design a project environment. It's important that I already had some solutions complete before I started this endeavor. Why? Two reasons: 1 personally, I am prone to analysis-paralysis, in that I will tweak my editor, and build environment to get it "perfect" before I write any code. This is useless.Secondly, usually, you don't know what you need until you don't have it. By that I mean, 2 or 3 source files, it doesn't really matter how slow or inefficient your compile-test-execute loop is since its only a small environment. The start of time of the compiler is the most significant aspect of this cycle. The dependencies are not complex enough to really demonstrate the effort. However, as the project grows these inefficiencies build, and expand on one another until you realize what's missing. For me that was 10 solutions in.

At 10 solutions in I found myself trying to break a module into 2 pieces, and discovered the trivial _ghc --make_ step I used became less effective. At this point it wasn't really a time efficient, but an irritation. An irritation I knew would grow to zap a significant amount of time. I fix my own irritations as soon as I can in a process I call [Dev-Speed](https://summit.atlassian.com/archives/2012/dev-speed/moneypenny-speaks) (a term I stole from the development team at Atlassian). Dev-Speed is the concept that an efficient work environment will make a more efficient engineer, thus higher quality code. Efficiency for me is minimal irritation for common tasks. However, fixing any irritation as it raises it's head will take one back to analysis paralysis and nothing will get done. Thus dev-speed is the process of setting regular intervals for project effort. At the end of the interval I reward myself by fixing some irritation in my cycle. This has the added impact of accelerating my development. When I hit a problem instead of procrastinating by choosing a "better" font for my editor, I work harder to get to my dev-speed cycle sooner. 10 solutions ended my first cycle. Ah. Now it's time to make it awesome.

First step is purely mechanical: project structure. Initially I had a flat simple structure with a Makefile and my source files in the same folder. For a few sources this was fine. I know I would out grow this structure, but I choose to not spend any time thinking about a better structure and instead ignored the irritation until my dev-speed cycle. For my folder structure I like to be idiomatic of the language, so I searched: "Haskell project folder structure" and found (http://www.haskell.org/haskellwiki/Structure_of_a_Haskell_project). I stole the project structure outright.

    
    .
    ├── dist
    ├── doc
    │   ├── Background
    │   └── haskell-primes
    ├── src
    │   ├── Data
    │   └── Euler
    ├── testsuite
    │   ├── benchmarks
    │   └── tests
    │   └── Euler
    └── util


Now I have a clean, usable structure, and a place for everything to go. My requirements now have folders to work within. However there is a problem, I have a place to put _my own_ libraries, but what about standard libraries and packages for the project. I need sandbox builds. Coming from python, I love virtual environments. Professionally, all our projects are cross-compiled, and we worked out a similar virtual-environment setup for C++/ARM/x86/x86-64. As this is one of my requirements. I searched for Haskell virtual environments and found a project by Galois called cabal-dev, which creates cabal sandboxes. This allows me to list by dependencies locally, and install them locally. Now I can freely install Hackage packages without fear of corrupting other Haskell Projects of my own or on the system. Cleaning a corrupt cabal repository is easier too, just make clean!

Okay primary requirements are met. Contributed libraries will not clutter my global spaces, and I have a clean efficient folder structure to built my project. Next step is to setup my makefile to build everything. Make is a fantastic tool, really. It doesn't get a lot of direct attention or praise, but it is certainly the master of time based dependency management.


<blockquote>While tweaking the makefile, _make -d | less_ was massively useful. It prints out the process steps make is executing so you can tune the makefile to only rebuild what' necessary, our see what make believes is missing.</blockquote>


It's more than just a source building tool. Since I have common libraries shared among multiple executables I'm using ghc's makefile dependency features. ([http://www.haskell.org/ghc/docs/7.6.2/html/users_guide/separate-compilation.html#makefile-dependencies](http://www.haskell.org/ghc/docs/7.6.2/html/users_guide/separate-compilation.html#makefile-dependencies)). So lets analyze the dependencies.




All my source files are in /src. My library code is in /src/Euler. Data Files are in /src/Data. contributed libraries are installed by cabal-dev into /dist. Now as I create new solutions I don't want to edit the makefile to add the new source files. Make should just discover them. This is a wildcard pattern SRCS=$(wildcard src/*.hs) #Define a variable called SRCS, that includes all the .hs files in the src folder.  Now what we need is a mapping from the source files to the executable. Make needs to know what the resulting executable name will be in order to see that it's missing. For example lets say we want to compile /src/001.hs into /src/001. Make will start up and look for /src/001 if it doesn't exist, it will look for a rule that defines how to convert /src/001.hs to /src/001.

    
    all: $(PROGS)
    
    %: %.hs
    	$(HC) $(HC_OPTS) $*.hs
    .hs.o:
            $(HC) -c $< $(HC_OPTS)


These 2 rules do just that .hs -> .o -> executable (i.e. no extension). Said another way, give me something.hs and I'll return you something.o then give me something .o I'll return you an executable. Make calls these recipes. So we have a variable with a list of the .hs files called SRCS we need a list of the progs -> $(PROGS). Make has a facility for this called pattern substution.

    
    PROGS=$(patsubst %.hs,%,$(SRCS))


This line defines a variable that converts all the source files to executable names. In this case it simply drops the .hs extension. On windows one would want to add .exe

    
    PROGS=$(patsubst %.hs,%.exe,$(SRCS))


Now we have a list of the programs, and a list of the sources, but we have a catch. What about the libraries? Who depends on those? It's important that we setup our build such that only the solutions truely dependent on a library function will be rebuilt, otherwise we watse a great deal of time building project which haven;t actually changed. For this case, ghc will generate the dependency rules for us which describe which source files are dependent on which library sources. Additionally, when the dependencies are correct make -j will do the right thing, which can massively improve the build speed. Here's the rule to generate the build dependencies

    
    depend: .depend
        @:
    
    .depend: $(SRCS) $(DEP_LIBS)
        ghc -dep-makefile .depend -M $(HC_OPTS) $(SRCS)
    
    -include .depend


ghc will by default append the dependencies to the current Makefile. I personally don't like that. the  dependencies are a generated item, and should therefore not be checked into version control. So I generate a separate file .depend and include it with the -include. -include will not complain if the file doesn't exist, as is the case on a clean build.

[caption id="attachment_1135" align="alignright" width="300"][![Euler benchmarks up to 037](http://www.codestrokes.com/wp-content/uploads/2013/08/euler-300x225.png)](http://www.codestrokes.com/wp-content/uploads/2013/08/euler.png) Benchmarks generated with octave measuring the current solutions.[/caption]

Great! Now we have a dependable build system and make -j does the right thing. Next we need benchmarks. Beyond just the project euler guidelines benchmarks are extremely important. From an educational standpoint you have a quantitative item to measure progress, (or lack there of). From a professional point of view, it's always satisfying to display a graph showing your performance is better than someone else. Graphs are how gentlemen insult each other.

What are we benchmarking? Compile Time, Run Time, and a set of common functions. Compile time is important for comparing against the intrepreted langauges like Python. A runtime spec from Python includes the compile time ostensibly, so it's an interesting point of comparison. The general setup here is a JSON file which maps numbered solutions to the correct answers, a python script to run and time the programs and compare the answer, and lastly an octave script to tie all the data files together into beautiful soul crushing graphs. At the top level are the Makefile rules to execute the recipes in an sensible order.

I want to type _make check_ on the command line to verify all programs are correct. This is especially useful when hacking on library code since the changes could break old solutions. This is separate from _make test_ which runs my unit tests. Make check should output a graph file (eventually) so lets call out the file we want to generate

    
    check: euler.png
        @:


make needs a recipe for euler.png

    
    euler.png: dist/times.dat $(BENCH_PROGS)
            testsuite/benchmarks/prime > dist/bench.dat
            octave util/process.m
    
    dist/times.dat: $(PROGS)
    	util/EulerValues.py --answers util/answers.js --file dist/times.dat $(PROGS)


The euler graph needs runtimes, and the bench programs themselves. times.dat is generated by the python script and depends on the programs. Now each component is built, we can run the benchmark programs and finally octave to output the graph. There is the makefile in it's entirety

    
    SRCS=$(wildcard src/*.hs)
    BENCH_SRCS=$(wildcard testsuite/benchmarks/*.hs)
    BENCH_PROGS=$(patsubst %.hs,%,$(BENCH_SRCS))
    TEST_SRCS=$(wildcard testsuite/tests/Euler/*.hs)
    TEST_PROGS=$(patsubst %.hs,%,$(TEST_SRCS))
    LIBS=$(wildcard src/Euler/*.hs)
    PROGS=$(patsubst %.hs,%,$(SRCS))
    COMPILE_TIMES=dist/compile.dat
    HC=ghc
    DEP_LIBS=dist/packages-7.6.3.conf
    HC_OPTS=-O3 -isrc/ -package-db=$(DEP_LIBS)
    GET_TIMESTAMP=$(shell date +%s.%N)
    CABAL=$(HOME)/.cabal/bin/cabal-dev
    
    .SUFFIXES: .o .hs .hi .lhs .hc .s
    
    .PHONY: all clean depend test
    
    all: $(PROGS) .depend
    
    %: %.o $(LIBS) $(DEP_LIBS)
    	@echo -n "$*.hs\t" >> $(COMPILE_TIMES)
    	@echo -n "$(GET_TIMESTAMP)\t" >> $(COMPILE_TIMES)
    	$(HC) $(HC_OPTS) $*.hs
    	@echo "$(GET_TIMESTAMP)" >> $(COMPILE_TIMES)
    
    $(DEP_LIBS):
    	$(CABAL) install -s dist/ digits
    
    check: euler.png
    	@:
    
    test: $(TEST_PROGS)
    	$(foreach x,$(TEST_PROGS),./$(x)${\n})
    
    bench: $(BENCH_PROGS)
    	@:
    
    dist/times.dat: $(PROGS)
    	util/EulerValues.py --answers util/answers.js --file dist/times.dat $(PROGS)
    
    euler.png: dist/times.dat $(BENCH_PROGS)
    	testsuite/benchmarks/prime > dist/bench.dat
    	octave util/process.m
    
    clean: 
    	rm -rf $(PROGS) $(BENCH_PROGS) dist/* .depend
    	find . -name *.o -exec rm -rf {} \;
    	find . -name *.hi -exec rm -rf {} \;
    
    #Standard Suffix Rules
    .o.hi: 
    	@:
    
    .lhs.o:
    	$(HC) -c $< $(HC_OPTS)
    
    .hs.o:
    	$(HC) -c $< $(HC_OPTS)
    
    depend: $(SRCS) $(DEP_LIBS)
    	ghc -dep-makefile .depend -M $(HC_OPTS) $(SRCS)
    
    -include .depend


There we have it. A cleanly organized, portable project with minimal rebuild, and a fast edit/build/run cycle! I'm always looking for improvements for my next dev-speed cycle. Please comment on any points of improvements.
