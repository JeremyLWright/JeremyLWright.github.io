---
author: admin
comments: true
date: 2013-10-20 23:00:00+00:00
layout: post
slug: idiomatic-learning
title: Idiomatic Learning
wordpress_id: 1126
tags:
- Idiom
languages:
- C++
- Haskell
- Python
---

When learning a new language I find it helpful to study a languages idioms. Idioms exist in a language for a specific reason. Sometimes that reason is to further the principles of the language, other times it’s to mask, or otherwise deal with some underlying design decision of the language. Currently, I am studying Haskell, and currently I am struggle to clarify the idioms of the language. The syntax is still very new and awkward, currently with a total authoring in Haskell of 713 lines.

<!--more-->

Python has some interesting idioms, but the one that really helped me when learning was “..tuples should have trailing commas…” At that time, the only other language I knew was C, and PIC Assembly. I was very much a hardware engineer, and Python, for me, was a step out of that hardware-centric mindset. So with such a staunch, inflexible background as this, such an idiom felt, dirty and wrong? My first reaction to this was, “What? Really? Why, are python programmers too lazy?” At first I refused to do this, claiming that my source code was more elegant, and clean. However some time later I learned the second part of this idiom, “…tuples should have trailing commas, BECAUSE syntactically the comma creates the tuple, not the parenthesizes.” Whoa! What an epiphany. From this simple clause, I can now create a tuple with 1 element! The because clause of an idiom, really opens doors in your mind. It really clarifies some subtle point, or characteristic of the language.

C++ on the other hand has a number of idioms that have become quite ingrained that it's hard to separate, "yeah that's just C++ syntax", from, "That's just how I do it," to, "Oh yeah, I guess template <typename T> class ... isn't very intuitive is it." C++ is a complex multi-paradigm language with one sweeping design decision: You pay for what you use. For instance, take class methods. In C++ class methods are not polymorphic by default. I remember as a fledgling C++ programmer asking my computer science friend, Brian, "...classes are useless without polymorphism. That's just stupid." He tried to explain it to me, but I was probably to frustrated to understand. What I didn't know was the because, and I continued my ignorant use of virtual until I read [The Design and Evolution of C++](http://www.amazon.com/gp/product/0201543303/ref=as_li_qf_sp_asin_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0201543303&linkCode=as2&tag=codestro-20)![](http://ir-na.amazon-adsystem.com/e/ir?t=codestro-20&l=as2&o=1&a=0201543303) that I learned the reason. Polymorphism requires a level of indirection to implement. Doing so affects performance. C++ doesn't push this on you unless you want it, just non-polymorphic by default, virtual if you want. Beautiful. Now as an embedded system designer I love this aspect of C++. I am free to use the features I need without paying for the ones I don't.

So now as I approach Haskell, I read blogs, and statements with a temporary suspension of judgement until I learn the because.
