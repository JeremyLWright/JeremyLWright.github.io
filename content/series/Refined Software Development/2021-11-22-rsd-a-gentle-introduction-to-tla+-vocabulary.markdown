---
title: "A Gentle Introduction to the Vocabulary of TLA+"
date: 2021-11-21:00:00-07:00
slug: rsd-math 
series: ["Refined Software Development"]
languages:
- tla+
tags:  
- math
- book
---

One of the challenges in TLA+ is all the new "words": $$\in$$ $$\forall$$ $$\exists$$ $$\cap$$ $$\cup$$ $$\land$$ $$\lor$$. These things have names such as: in, forall, there exists, and, or, etc. 

Unfortunately, these "words" are referred to as "simple math" in the TLA+ community which brings with it a judgment that one should already know this material. Furthermore, if you read Specifying Systems[^1], the author indeed asserts that your education has been a disservice for you not knowing this material. While I deeply respect the impact Dr. Lamport brings to our industry, I feel this is unfair and doesn't reflect the fact that there is not 1 path to being a programmer. Programmers of all disciplines and backgrounds who arrive at TLA+, recognize there must be a better way to describe and architect our concurrent systems. It behooves us, to encourage them that TLA+ indeed such a solution, and mentor the potential gaps in architecture or math vocabulary. 

# Not all who wander are lost

My own background, I have a Bachelor's of Electrical Engineering, and a Masters of Computer Science with a concentration in Information Assurance (Software Security). I didn't know these math operations. I had an understanding of some within the context of digital logic, but even that didn't really help and may have been more of a distraction rather than starting fresh.  

Regardless of whether, my schools did me a disservice, everyone who arrives at
TLA+'s front door, arrives from a different path[^2]. Thus I propose, as a community, we encourage everyone with an interesting to study TLA+ and better software architecture as a whole, then we'll mentor their math skills to where they need to be. 

## Welcome Node Programmers

{{< figure src="/img/nodejs-new-pantone-black.svg" title="Node JS Logo" width="60" >}} 

Maybe you, dear reader, are a self-taught Node.JS programmer. All this "math" is "not programming". First, welcome Mr./Ms. Node Programmer. I'm proud that you have come to learn our tool. TLA+ indeed has a place on the systems you are building. Even if you just use the sketching style I describe in my [last video]({{< ref "/series/Refined Software Development/2021-11-03-tla-plus-as-a-flowchart.markdown" >}})[^4], your software will be better because of it. If you have questions about how does TLA+ apply to your problem, ping me. I'd love to discussion TLA+ in such a domain.

## Welcome Non-Programmers

Maybe you are a high-school student, you stumbled upon this via _The Algorithm_. Take it as a compliment. _The Algorithm_ thinks you are intelligent and brilliant. Welcome. I am especially interested in seeing how the informal programmer/student interprets the value of TLA+. Feel free to [contact me]({{< ref "/about.md" >}}). I'd love to hear real feedback about your experience learning this material.

Thus, this is my introduction to the "simple math" which I will simply call, vocabulary of TLA+. The benefit of TLA+'s design, and indeed the genius, is this vocabulary is comes from branches of math[^5] which have existed for decades, or even centuries. It's a proven[^3] grammar for precisely communicating complex ideas. TLA+ is yet just one among a sea of domains described in the language of math. 

# TLA+ is not like learning a programming language

I made a similar encouragement/warning in the last post, but I restate it again. Learning TLA+ is a unique[^6] language. I'm still a student of the language myself and I'm finding that it can describe the small, and the medium. I have yet to describe a big system myself in TLA+, but Paxos' specification, and later proof[^7] declare yes. Learning TLA+ requires intentional practice, but I consider the time spent well worth it. 

## TLA+ specs are not programs. They don't "run"

TLA+ programs do not "run" they are more akin to flowcharts. They describe the entire set of states and transitions between states. You don't "run" or "execute" a spec, you state properties (which I call questions). TLC then checks if that property is true.

### Designing a Bicycle

Consider the following analogy: There is a piece of tubular steel sitting on a table. It's not part of any design. It's not serving any function. It's static. However it does have certain properties such as tensile strength, hardness, pliability, etc. Say you want to build a bicycle frame. You might ask, "For a 45 kg rider, is this tub of steel strong enough to hold up the cyclist, and tolerate the stresses of road riding?"

As a material scientist, you could put the steel in a series of machines and tests the various mechanical properties necessary to answer your question, "Can this steel be a bicycle frame?" 

Now, take this one step further. Instead of having the steel itself, and all the machines to test the various properties, you have a a spec sheet. A table of values measure by the steel manufacture (or a 3rd party testing lab). You describe the forces placed on the bicycle frame you intend to build and a tool checks if the steel you desire withstands those forces. 

This is what TLA+ is like. You describe the bicycle frame as a specification. Then you state forces that act on your design, in this case a bicycle frame. TLC checks that the properties of the steel you choose supports the forces you declare your design withstands. 

Now, is your bicycle indestructible? No. You as the designing could have missed a force such that TLC didn't check. Hence if this force occurs in the real world, the frame may fail. This is just how our software systems function. We apply our experience and knowledge to declare our specifications. Yet we use tools to check of those specifications meet our constraints. 

Notice that this is different then how we normally build software systems. To follow the analogy, we'd first build the bicycle, then test-ride it on our nice easy course. If that test fails, we add more steel, or change the geometry, etc. We continue in this fashion until our bike doesn't crash when we ride it on our custom designed course. We then, let others use the bicycle. If they crash it we ask them what happened, and we again change the bike. 

# Describing our systems

Now we know that TLA+ isn't a programming language. What is it? This is where the math comes in. Math is the language TLA+ expresses itself in. It feels a little basic learning some of these idioms.

 <!-- I myself tried to skip past this introduction the first time I saw it. For example, I saw a page in _The Hyperbook_[^10] teaching me *and* ($$\land$$). I thought to myself, I'm way past this. ``if(thing1 && thing2)`` Unfortunately, this is a false equivalency. 

{{< figure src="/img/john-cena-confused.gif" title="John Cena Confused">}} 

$$\land$$ is **not** the same as ``&&`` they both are pronounced as _and_.  For example, in programming we take advantage of short-circuit evaluation in languages like C and Python, thing2 isn't even evaluated. Yet, remember TLA+ isn't "evaluated" at all.   -->







# References

[^1]: Lamport, Leslie. _Specifying Systems_. https://lamport.azurewebsites.net/tla/book-02-08-08.pdf 
[^2]: Ironically, TLA+ a tool designed to model and describe the various
  behaviors of a complex system, seems to assume everyone has the same
  background, e.g., same set of behaviors, leading to TLA+. This is not the
  case. 
[^3]: Literally.
[^4]: Wright, Jeremy. _Flowcharts as a Conversation: Rubber Ducking our Designs_. https://quiescent.us/series/refined-software-development/rsd-vending/
[^5]: TLA+ leverages temporal logic, prepositional logic and set theory.  See [^1]. 
[^6]: TLA+ is not alone in the domain of specification languages. Alloy[^8], Spin[^9], are both examples of languages designed to describe systems in a machine checkable way. Yet, TLA+ is unique in that it directly models time, and allows checking of properties via it's inclusion of temporal logic. 
[^7]: Lamport, Leslie. _Byzantizing Paxos by Refinement_. https://www.microsoft.com/en-us/research/publication/byzantizing-paxos-refinement/
[^8]: Jackson, Daniel. _Alloy_ https://alloytools.org/alloy6.html
[^9]: Bell Labs: Computing Sciences Research Center. _Verifying Multi-threaded Software with Spin._ https://spinroot.com/spin/whatispin.html
[^10]: Lamport, Leslie. _The Hyperbook_. https://lamport.azurewebsites.net/tla/hyperbook.html