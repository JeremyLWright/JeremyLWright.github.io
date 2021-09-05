---
author: Jeremy
comments: true
date: 2011-07-06 05:18:48+00:00
layout: post
slug: version-control-more-than-collaboration
title: Version Control More Than Collaboration
wordpress_id: 251
tags:
- Teaching
- Talks
- mercurial
- subversion
- version control
---

I've used version control in some form or another since I was a freshman in college, however I'm quite the anomaly.  I will use a tool fully knowing that its more than I need, just to learn something new.  Initially, this is how I approached version control. Except for a few unique situations version control of my homework, seemed like more work than it was worth.  I used to think version control was merely a collaboration tool for teams of people.  I couldn't have been more wrong.

<!-- more -->

Now I teach a small not-for-credit C++ class at ASU, and one of my students said something interesting:


<blockquote>I would use version control, but I'm only one person. Why do I need a collaboration tool for just myself?</blockquote>


I thought it was an excellent perspective, version control is primarily intended as a collaboration tool, simply look at [github](https://github.com/)'s slogan: _Social Coding.  _Coding for **groups of people**. Yet, version control is much more than that.  For instance how many times when writing a paper, do you use the Undo? For most non-technical computer users, its probably the only keyboard shortcut they know: Ctrl+Z.  Version control is essentially** infinite undo**. Revert is great.  It frees you from fear of breaking existing code.

I have a friend, lets call him my "lets-get-serious-friend".  Who is great at hacking out piles of code until something works. If you need a quick, solution this friend can nail it.  He'll try several different approaches toward a problem. If that doesn't work he'll comment out the function, with a comment of why it didn't work.

He's very organized about it, and its a solid approach for him. Yet, after he's finished a solution, he cannot quite remove all the dead code. Writing code is an artistic process and throwing code away, even if it doesn't quite work, is emotional. When the code is particularly clever, it is especially hard to hit the delete key (or rather the dd "key" :-).  Version control lets you remove all that emotion. You can keep it all, every version.  If in the future you find a use for that clever tidbit, its tucked away safely in your code repository.

Undo is nice, and being able to keep everything is better, but the nirvana of coding is branching. I came from subversion, so I never really learned to branch. However with my recent [Game Components](http://www.codestrokes.com/2011/06/game-framework-for-c-practicum/) project, I've really been leveraging the hg branch command.  Joel Spolsky says [not to use the named branch](http://hginit.com/00.html) feature in Mercurial, however I disagree; and the [Crucible/Fisheye](http://blogs.atlassian.com/devtools/2011/06/fisheye-crucible-26-commit-graph.html) team at Atlassian use named branches so its can't be all bad.  Let me give you an example.

I was hacking on the Models for my Game Components project, I [committed](https://bitbucket.org/jwright/gamecomponents/changeset/10efe59c3d75) the code,  but I wasn't really happy with the result. I decided a ModelFactory might be useful in fixing some of the code smell.  The code I had worked, but it was quite fragile, and it required the controller to know too much about the data.  _I think_ a factory will solve the problem, but I'm not quite sure.  I could try it out, and if it doesn't work revert, but refactoring in a ModelFactory is a bigger effort than I could support that day. So I branched:

    
    hg branch ModelFactory
    hg update -C ModelFactory
    hg commit --new-branch


Excellent. Now I have a clean place to play with my idea. If it fails I can just kill the branch, but the really great thing if I get stuck, I can jump back to my main (default) branch and continue working on some other component of my game:

    
    hg update -C default


So branching is a tool to help you deal with writer's block.  In a way, branching is like a little drawer.  When you want to work on that little project, open the drawer and pull out the item.  When you're bored or stuck, but it back in the drawer. Its always there. Its easily accessible, but it doesn't clutter up your workspace.

[Currently](https://bitbucket.org/jwright/gamecomponents/changeset/7f49b0b960c8), I'm still not convinced the ModelFactory fixes my issue, so I'm working on the level editor now, on the DialogEditorTool branch. School starts in about 1 month so I gotta figure it out by then, but it's there, in a branch, organized, and out of the way.  So version control is more than just a collaboration tool. It helps you permits you to keep your files clean, and free of dead code, while keeping every bit and byte. Version control, help you grow your code without fear of permanently losing some fragile configuration.  Its an process to help you stay organized even if your development plans aren't.
