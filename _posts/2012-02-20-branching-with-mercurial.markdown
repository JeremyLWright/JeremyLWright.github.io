---
author: Jeremy
comments: true
date: 2012-02-20 02:18:15+00:00
layout: post
slug: branching-with-mercurial
title: Branching with Mercurial
wordpress_id: 556
tags:
- Project
---

Mercurial supports two separate methods for branching. The first is built into how distributed version control functions, in that every clone is a branch itself. This is the branching method Joel Sposky recommends on hginit.com. The second method is called _[local branches](http://mercurial.selenic.com/wiki/Branch)_. Initially I liked the local branch method; I liked it for the fact that I felt smart for using it. It did not improve productivity. There is a simple reason for this, with local branches it is difficult to diff the branch to the main branch of development e.g. the trunk. This post will walk through local branches, how I used then, and finally, how I quit local branches in favor of a cloning approach.

<!--more-->

I use version control because I like to experiment when I code. I frequently approach a class design as: What if _this_ happened? Frequently, people comment, "I don't need version control; I'm just one person." This is a rather naive perspective on version control. Yes, version control can be used to collaborate work between different people or different teams. In fact, originally, this was it's primary use case, however version control is so much more.

Personally, I feel very unsafe when working without version control, its coding without a safety net. Once you get something working, you don't want to touch it because you might never be able to get it back to this working state again. Version control fixes this behavior. When you get a semi-working version of something **tag it** then keep working; if you get something better, tag again. If you break it completely, revert back to the previous tag.  Its a great tool. Branches are that idea on steroids. I use branches extensively, at work I tag of ever issue number, for school/home I tag on each capricious thought. One project I implemented the [Game of Life](http://www.codestrokes.com/2011/10/parallel-game-of-life/), as a conduit to experiment with OpenMP. At one time I had 6 parallel branches each with a different experiment or idea:



	
  * Parallel Game of Life


	
    * data_dependency_tests

	
    * octave_experiments

	
    * pthread_vs_openmp

	
    * graphical_debugger

	
    * parallel-game-of-life

	
    * SDL_ext_experiments





Originally, I tried using local-branches. This is the _hg branch_ command. Just type hg branch, and a branch name, then keep working. To switch between branches use hg update -c <branch_name>. This is the problem. Its hard to work on multiple branches at that same time. I was constantly switching between branches, and that wasn't very productive.







The one upside to local branches is that all the branches are carried with the repository, so you can work on multiple branches on different computers just by cloning one repository. However the loss of productivity by constantly switching between different branches was too much. I now do something different. I clone for a branch. When I check out a new project, I create a directory first, then clone my remote-repository into that folder with the name _top _i.e. top-level. Then I hg clone any branches I want and start working. This makes it very easy to merge, between working copies, and diff changes. Then If I don't like an idea I can throw it away completely, and it doesn't dirty my changeset history!







Here is a snapshot of a project with all branches:


[![](http://www.codestrokes.com/wp-content/uploads/2012/02/Screenshot-GOF-300x272.png)](http://www.codestrokes.com/wp-content/uploads/2012/02/Screenshot-GOF.png)


Now I can create a tab in vim, and open each branch into a separate tab. Awesome!



