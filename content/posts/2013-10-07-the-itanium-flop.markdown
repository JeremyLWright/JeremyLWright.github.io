---
author: admin
comments: true
date: 2013-10-07 01:23:13+00:00
layout: post
slug: the-itanium-flop
title: The Itanium Flop
wordpress_id: 1201
tags:
- Necromancy
- itanium
- knuth
- multicore
---

I wake up in the morning with ideas that please me, and some of those ideas actually please me also later in the day when I've entered them into my computer. - Donald Knuth

I'm on a bit of a Knuth kick right now, and I've been procrastinating studying, and homework to find interviews, and papers by the master himself. I currently have a list of microfiche references to check out as soon as I get to the basement of my university's library: Woot, [computational necromancy](http://www.chrisfenton.com/homebrew-cray-1a/)! Through this, I came across a quote in an [interview](http://www.informit.com/articles/article.aspx?p=1193856), "...worse than the "[Itanium](http://en.wikipedia.org/wiki/Itanium)" approach that was supposed to be so terrific—until it turned out that the wished-for compilers were basically impossible to write." What? I thought it was simply market forces that drive the x86-64 ahead of Itanium: nope!

<!-- more -->

[This](https://www.usenix.org/legacy/event/usenix05/tech/general/gray/gray.pdf) paper discusses some of the advanced features of the Itanium platform as well as Intel's intention for those features. Essentially, the Itanium platform is about empowering software developers. The CPU even provides a "software TLB". In a typical software application performance is dependent on the CPU's ability to pipeline, and reorder instructions. This is typically done in hardware. While this approach has proven workable, Intel notes the limitations of "speculation" by the hardware. The thought then arises, why not turn the advanced speculation functions over to the compiler writer. Itanium is born. Gray discusses how these functions while advanced leaves a huge responsibility on the already loaded optimized running in the compiler. The paper, is a great read, and as Knuth alludes, a similar situation is happening with multi-core today.

Hardware designers have hit physical limits with clock speeds, just as they hit speculation limits almost a decade before. The hardware engineers are pushing the onus of performance to software once again. Are we ready to carry the torch this time?
