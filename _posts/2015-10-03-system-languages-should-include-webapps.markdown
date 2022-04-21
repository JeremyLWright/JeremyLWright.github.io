---
layout: post
author: Jeremy
date: 2015-10-03 00:00:00+00:00
slug: system-languages-include-web
title: "System languages should include Webapps"
draft: false
tags:
- Coding
languages:
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
success so flippantly brushed aside its future user. The C++ community is
certainly undergoing a transformation. There is active effort to modernize,
and refresh C++.  However, lending a hand to beginners is not C++'s forte.
There are more [resources](codereview.stackexchange.com) to learn programming
today than when I started, however the struggles of a beginner are largely
unchanged. This comment left me thinking not that this C++ idiom is easier
to understand, its that there aren't any novices left in the C++ community.

I am currently reintroducing myself to D. There are two things that
I admire about the community. First, D is frank about the inconsistencies in
their language, and actively try to make it easier to understand. Second,
D embraces web application.

During the [DConf videos][dconf] speakers voice pain points, and
inconsistencies in the language. The point isn't to complain, but to
acknowledge that language experts are not the only users.  With each point Walter
Bright (the language's author) carefully considers each point.

For example, one individual suggested that D's mixins are "unprincipled".
Unprincipled meaning mixins are strings rather than expression trees as in C#'s
LINQ, or Abstract Syntax Trees as in Rust's macros. Bright however
[responded][unprincipled-mixins] that he agrees mixins are unprincipled, but
"...[that] they are easy to understand."  Making mixins as straightforward as string
manipulation makes an otherwise advanced technique something a novice can use.

I can certainly attest to the complexity of C#'s LINQ. I've
<strike>worked</strike> struggled on a LINQ provider for a in-house database
engine. LINQ Expression Trees are certainly in the upper echelons of advanced
techniques. Implementing mixins as string manipulation is a beautiful
concession to making a language easier to use.

The second principle I loved about the D community, and the thesis of
this post, is a single statement on [D's roadmap][Ds-roadmap]
"Emphasize [vibe.d][vibe.d]".

[Vibe.d][vibe.d] is an asynchronous I/O and web framework library for D.
I find the combination of I/O library and web framework similar to [Play
Framework's][play-framework] approach from Scala.  D is classified as a system
language. The same class as C++. However the D community considers (as does the [Rust
community][craig-rust-reddit], [1][rust-web], [2][rust-areweweb]) web
services a key enabler.

C++ is entrenched in enterprise applications.  However languages like D, and
Rust are among the few that can compete with C++'s performance. This is,
I believe, C++'s last life-preserving feature, entrenchment.  C++ is hard to
learn, hard to use, tends to define language experts (also see Haskell).  But
it is everywhere, and I can get a good paying job by knowing it. 

HTTP/REST has established itself as the lingua-franca of Service Oriented
Architectures.  [LinkedIn][linkedin] maintains a beautiful and informative
blog about engineering a massively-online-multiplayer-role-playing-game, also
known as a social network. At it's heart are a number of services, written in
various languages, all linked together via HTTP. HTTP is the key that binds
them all. D is on-board with HTTP, and embracing the Web. Rust appears to be
as well. This is certainly a massive opportunity to compete with C++ at the
heart of its entrenchment, enterprise services.

As I work on my own personal projects, I like to use compiled languages. I have
quite a bit of experience with Django, but I don't feel confident to build
a large, long-term project in a duck-typed language. At risk of sounding like
a Haskeller, a strong type system really does help enforce a consistent
application. Even if one just considers refactoring, the compiler looks at
every line of code, and every function call, every time. I like to believe I'm
professional enough an engineer to say my unit-test exercise 100% coverage,
but I know I've never been successful in doing so. I would like to leverage my
expertise in C++ to build my personal web service experiments, but there
simply isn't a reasonable way to do that. Go is certainly a contender for this
space, but I prefer languages that give me more of a hand in generic
(parametric polymorphic) techniques. For me, now, that language is D. 

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
