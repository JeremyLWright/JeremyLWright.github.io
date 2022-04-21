---
layout: post
author: Jeremy
date: 2015-06-07 00:00:00+00:00
slug: converting-to-static-blog
title: Recasting how I blog
tags:
- Writing
- blogging
---

I wrote my first article for codestrokes in February 2011 - right as I was
accepted to graduate school. My goal was to improve my writing in preparation
for writing a thesis. While through grad school I started with more
traditional writing tool. I started to learn to write, and I found my writing
style: Simplicity.  I started writing with a big fancy word processor.
I blogged with a massive database backed blogging engine. By the time
I finished my thesis, I was writing in vim. I used a makefile to check
spelling and check for simple grammatical rules. The process was much simpler
to manage. This motivated me to convert my blog to a static site. This post
describes my process on simplifying my writing process.

<!--more-->

# My toolchain

The primary goal was leverage the writing tool chain I honed during my thesis
for maintaining my blog. I didn't want to complexity of a database backed
blogging site. I wanted to drop my hosting service. I wanted to write in
a markup language. I wrote my thesis in Latex, and I love the separation of
presentation from content. This site you are reading today is composed of:

1. Markdown written in Vim.
1. Changes tracked in git.
1. Markdown converted HTML via Hugo.
1. Static pages hosted by Github Pages.

# Choosing a static site generator

I actually didn't spend too much time working on this, since someone already
did a great deal of the work at https://www.staticgen.com/.  If you are
planning to use Github to host your blog, Jekyll will be the easiest to use.
The Github pages even include documentation on how to use Jekyll with Github
pages. I however have an aversion to Ruby (though an order of magnitude
weaker than my aversion to Java).  Near the top was [Hugo](gohugo.io).
A <del>colleague</del> friend of mine is quite a convincing evangelist of Go,
and I decided to give it a try. -- Boy, was I impressed -- The quality of the
documentation if fantastic. However my favorite feature of Hugo, it is
a single download. One executable. One. No dependencies... Its hard to express
how incredibly relieving this is. 

As an illustration, let me share with you a little lie. I didn't directly just
to staticgen.com, and find Hugo. I have an affinity for Haskell, and tried to
use a static site generator called [Hakyll](https://www.staticgen.com/hakyll).  
I closed the project from github. The repository included a cabal file, which
I promptly compiled. It took 25 minutes to build all the dependencies. Hakyll
seems awesome, but I wanted something simple. Simple that I can just write,
and the publication process becomes ancillary. Pieter Hintjens states that
a project should continuously seek to reduce barriers for participation.
Comment on this site are a perfect example. [Disqus](https://disqus.com/)
strikes a fantastic balance between reducing spam, without requiring everyone
to login to my site. I have no presumptions concerning this site, and
I completely understand that people do not need yet another account to manage.
I want people to comment, hence I use a service that reduces the barrier to
participate. 

A cabal file is a barrier to participate. I want to consume a project, I don't
want to contribute to it (yet). Hugo had the lowest barrier to entry of the
site generators I tried. One executable, no dependencies, and fantastic
documentation. 

# Exporting Content 

I had a significant number of posts in Wordpress. I wanted to be a good
content creator, and preserve my URIs.  Really, I'm _wicked_ lazy, and
preserving my permalinks meant I would not have to migrate my comments. Disqus
would pick them up on the new site. Thus I wanted an automated way of
exporting my posts from Wordpress. [Exitwp](https://github.com/thomasf/exitwp)
worked like a charm. 

# Choosing a theme

Hugo has a [theme gallery](https://github.com/spf13/hugoThemes/) for all the known themes associated with the
generator.  I picked [redlounge](https://github.com/tmaiaroto/hugo-redlounge).
My only customization was to add Google Analytics so I can track my meager
pages views. 

# Writing articles in a series

I tend to write articles broken over many pieces. In fact, this article is
part of my blog transition series. My series support was somewhat lacking in
Wordpress. For this reincarnation of codestrokes.com, I wanted series to be
nice and effective. Hugo's taxonomy makes this possible, but it was a great
series by another author, [Nate Finch](http://npf.io/series/hugo-101/) that
made it easy. Ironically, the series starts with an article about how to
design series into Hugo. Brilliant. 

# Hosting

I have a few requirements:

1. Custom domain must work (so I don't have to migrate comments :-) 
1. Publishing from git would be sweet, but I can configure Travis-CI or
   a deployment something to deal with that.

[Github pages!](https://pages.github.com/). I just followed the documentation.

# My Publishing Process

Here's how I write now:

1. Clone JeremyLWright@github.com
1. git checkout content
    1. The content branch holds the source, and theme files.
1. Clone the repository again into the public folder. 
1. The public folder should be on the master branch.
1. Write.
1. Revise.
1. Write...
1. Run Hugo.
1. Commit the content branch.
1. Commit the public branch.
1. Push!

I'm happy with my new process. I'm still working out some kinks with my pages
vs posts (hence you see the About Me page in the middle of my posts). I am
prone to shiny things so we'll see how long I keep it. This process is simple.
It removes the barriers of posting, and just lets me write in the tool I am
most comfortable, and but its hard to argue with simple. 

