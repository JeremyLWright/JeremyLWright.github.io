---
author: Jeremy
comments: true
date: 2011-06-19 18:59:47+00:00
layout: post
slug: being-truely-productive
title: Being Truely Productive
wordpress_id: 219
tags:
- Writing
- process
- vim
---

Productivity is an elusive mistress.  I approach productivity much like any design problem. I lay out my requirements, and I iterate until I am happy with the outcome. Over the last few years I have spent a lot time laying out my design process.  Along the way I found a number of tools that were helpful.  This is my personal process and while I think it's a great process.  It's important to refactor for yourself. The key to my productivity is consistency. I work well with a defined workflow. Lastly, interruptions are a certainty, so one must find a way to make context switches less disruptive.


<blockquote>Try to setup natural stopping points in your process. You will be interrupted so make context switches cheap.</blockquote>


Consistency _is_ my process, and tools help me deal with strict and dynamic constraints.  I use a number of tools help me be productive, yet consistency is the most powerful function for me.

<!-- more -->Firstly, everyone needs a personal database. This is critical. A software engineer's job isn't really about writing code.  Its about organizing information, namely requirements, and teaching them to the computer. One needs a tool that can help organize this data.  I've used a number of tools, TomBoy is a close second, however I found that [OneNote](http://www.amazon.com/gp/product/B0039L2XMA/ref=as_li_ss_tl?ie=UTF8&tag=codestro-20&linkCode=as2&camp=217145&creative=399369&creativeASIN=B0039L2XMA) cannot be beat. Especially, with the new WebApp versions on live.com, I can use [OneNote](http://www.amazon.com/gp/product/B0039L2XMA/ref=as_li_ss_tl?ie=UTF8&tag=codestro-20&linkCode=as2&camp=217145&creative=399369&creativeASIN=B0039L2XMA) on any platform, even when I am not home.  [OneNote](http://www.amazon.com/gp/product/B0039L2XMA/ref=as_li_ss_tl?ie=UTF8&tag=codestro-20&linkCode=as2&camp=217145&creative=399369&creativeASIN=B0039L2XMA) is a table of contents for my brain.

[![Screenshot of OneNote on Live.com](http://www.codestrokes.com/wp-content/uploads/2011/06/OneNoteOnline-300x161.png)](http://www.codestrokes.com/wp-content/uploads/2011/06/OneNoteOnline.png)This brings me to a struggle I had to overcome. When I was in college, I enjoyed hating Microsoft. It was more of a social thing than an actual reason. Later I found that, there is balance, I don't have to be a Microsoft Fan-Boy to use their products. Use what works for you. Just because it isn't FSF, or GNU software doesn't mean its crap.  In fact it may be exactly what you need.


<blockquote>Don't undermine your productivity just to make a statement.</blockquote>


It is crucial that I maintain a homogeneous workflow regardless of my environment: Windows/Linux, Home/School/Office etc.  When choosing tools, I tend to not look for the most powerful, yet instead I search for  the simplest, lowest common denominator.  I use Vim, as an editor, and IDE. The Visual Studio IDE is  fantastic, but can I write Verilog in it? No. Eclipse is nice and  cross-platform, but can I edit .sdc files? No.  Vim is powerful, and  ubiquitous. I can do all of my work, anything I am tasked  with, in Vim. FPGA, C++, Java, C# .NET, PIC C, write a love letter to my  wife (probably most the important task), Vim does it all.   Regardless of the language, platform, or toolchain my editor is consistent. Constantly changing tools, helps you learn, but will not help you be more productive. Regardless of which tools you use, use them consistently.  The only downside I've found in learning Vim, has been if for some reason I am in any other editor I litter the page with little _:w_. Here is my [Vim Configuration.](https://bitbucket.org/jwright/vim-configuration) I am working on a dedicated article on my vim configuration. Lookout for it here.

Save everything.  Tool configurations, one-off scripts, capricious prototypes.  Keep it all.  It's important to realize that everything you create has value, and the value changes over time.  Keep it. I use mercurial.  It seems the DVCS movement is really taking over in cutting edge development companies.  Companies like [Atlassian](http://blogs.atlassian.com/developer/2011/02/moving_to_mercurial_-_why_we_did_it.html). DVCSs such as git, and mercurial do a number of things different that make the process more productive, but the single reason I switched to mercurial from subversion: **Local Commits**.  I cannot state enough how local commits have made me a better programmer.  Local commits do two things for me. They make context switches (i.e. interruptions) cheap, and local commits let me make more mistakes.

More mistakes? How does more mistakes make one _more productive_.  Simple, I keep a history of all my mistakes so I am not destined to repeat them.  Very often when I am working on a project I want to experiment with some new idiom or pattern.  I use the local commit like a video game save-point.  The commit message is usually something to the effect of:

    
    Mercurial Commit:
    Probably a bad idea. :-/ Save point for PIMPL experiment.


I freely continue with my idea. If it works out well, then excellent I can always look back and see how I added a given idiom to some existing code. Yet, more typically, my experiment is an utter failure.  I just hg revert, and done. However all is not lost, all that history is saved. I can always look back and see how I applied or rather misapplied my experiment. Reviewing my mistakes helps me to improve. Vim has nearly infinite undo, [persistent undo](https://groups.google.com/group/vim_announce/browse_thread/thread/66c02efd1523554b?pli=1), and [branching undo](http://vimdoc.sourceforge.net/htmldoc/undo.html), all in an effort to provide similar functionality.  This however is not sufficient. Mercurial lets you save your mistakes! 

<blockquote>Saving your mistakes may even be more important than the final solution.</blockquote>



Prototyping is an important way to gauge investment of your time. Before you start a project work out a bit of a prototype.  Sometimes I get an idea in my head and I just start hacking, usually once I get the idea flushed out I'm done.  I just wanted to see, "Will that work?" Prototyping makes this easy without being too costly, time wise.  I use 3 tools for my prototypes: Python, Octave, and Excel.  Between these three there isn't much one cannot do. Excel is great for just pounding out some number. I frequently use excel to mock out data sets to see where I need to instrument my code to capture some concept.

Lastly, you need a coding standard.  All the time. When writing personal code, maintainable typically isn't a concern. It's your code, you understand it. It's probably not a long lived project. A coding standard however doesn't slow you down, it makes you more effective.  If you write software consistently, you can lever [snippet tools](https://bitbucket.org/jwright/vim-configuration/src/1da9bad9fe53/snippets/), and code formatting tools to generate boiler plate for you. If you always use the same class layout its easy to go back and find what you need. Yet most important for me, consistency makes [wrong code look wrong](http://www.joelonsoftware.com/articles/Wrong.html).

Tools are important. As you can see, I use a number of tools regularly, however the best weapon against time is consistency.  Be consistent in your process, and you will reap rewards.  Please leave your comments. I am curious what tools and processes you, my readers, implement.
