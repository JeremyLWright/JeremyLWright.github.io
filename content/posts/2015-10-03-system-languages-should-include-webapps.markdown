---
author: Jeremy
date: 2015-10-03 00:00:00+00:00
slug: system-languages-include-web
title: "System languages should include Webapps"
draft: false
categories:
- Opinion
tags:
- D
- Rust
- C++
---

I was reading an [FAQ][cpp-novice] today about some subtle C++ point and I came across
a comment that explicitly excludes the beginning language-learner.

> By the way, it confuses most novice C++ programmers that private virtuals
> can be overridden... However the private virtual approach is now common
> enough that confusion of novices is less of a concern.

This left me frustrated that a language that has been core to my personal
success so flippantly brushed aside its future user. There is deep active
effort to modernize, and refresh C++ today.  However, lending a hand to
beginners I feel is currently not C++'s forte.  While there are massively more
resources now for one to learn programming, than when I started, the struggles
of a beginner to understand are still present. This comment left my thinking
not that this C++ idiom is easier not, its that there aren't any novices left
in the C++ community. 

I am currently reintroducing myself to D, and there were two things that
I really admired about the community. The first is the frankness of the
languages users to define the identity of D. During the [DConf videos][dconf]
speakers voice pain points, and inconsistencies in the language. The point
isn't just to complain, but Walter Bright (the language's author) is sitting
right in the audience and carefully considers each point. For example, one
individual suggested that D's mixins are "unprincipled" in that their are
strings rather than expression trees in C#'s LINQ, or AST's as in Rust's
macros. Walter however [responded][unprincipled-mixins] that he agrees mixins
are unprincipled, but "...they are easy to understand."  Making mixins as
straightforward as string manipulation makes an otherwise advanced technique
something a novice and use in their own programs. I can certainly attest to
that. I started working on a LINQ provider for a custom database engine at my
work. Its not an easy, straight-forward task. Implementing mixins as string
manipulation is a beautiful concession to making a language easier to use. 

The second principle I loved about the D community, and reinforced my decision
to step back into it &mdash; and the thesis of this post &mdash;, is a single
statement on [D's roadmap][Ds-roadmap] "Emphasize [vibe.d][vibe.d]".
[Vibe.d][vibe.d] is an asynchronous I/O and web framework library for D.
I find the combination of I/O library and web framework similar to [Play
Framework's][play-framework] approach from Scala.  D is classified as a system
language. The same class as C++. However the D community (as does the [Rust
community][craig-rust-reddit] [1][rust-web], [2][rust-arewewebyet] that web
services are a key feature.  C++ is entrenched in enterprise applications.
However languages like D, and Rust are among the few that can compete with
C++'s performance. This is, I believe, C++'s last attractive feature,
entrenchment.  C++ is hard to learn, hard to use, tends to define language
experts (see Haskell).  But its everywhere, and I can get a good paying job by
knowing it. HTTP/REST has established itself as the lingua-franca of Service
Oriented Architectures.  [LinkedIn][linkedin] maintains a beautiful and
informative blog about engineering
a massively-online-multiplayer-role-playing-game, also known as a social
network. At it's heart are a number of services, written in various languages,
all linked together via HTTP.  

HTTP is the key that binds them all. D is on-board with HTTP, and embracing
the Web. Rust appears to be as well. This is certainly a massive opportunity
to compete with C++ at the heart of its entrenchment, enterprise services.



[craig-rust-reddit]: https://www.reddit.com/r/rust/comments/3n3b2d/trying_rust_for_web_services/cvl1lx1
[rust-web]: https://blog.wearewizards.io/trying-rust-for-web-services
[rust-areweweb]: http://arewewebyet.com/
[pragmatic-rest]: http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
[vibe.d]: http://vibed.org/
[cpp-novice]: https://isocpp.org/wiki/faq/strange-inheritance
[dconf]: http://dconf.org/2015/index.html
[unprincipled-mixins]: https://www.youtube.com/watch?v=s83u5iw67TY
[Ds-roadmap]: http://wiki.dlang.org/Vision/2015H1
[play-framework]: https://playframework.com/
[linkedin]: http://engineering.linkedin.com/play/play-framework-linkedin
