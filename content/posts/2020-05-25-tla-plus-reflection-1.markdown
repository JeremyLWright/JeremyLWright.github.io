---
title: "TLA+ Chapter 1: Reflection"
date: 2020-05-25T15:00:14-07:00
categories: 
- design
slug: tla-chap1
series: "Practical TLA+"
tags:  
- tla+
- hillel
- book
---

The first time I opened [Hillel's
book](https://www.hillelwayne.com/post/practical-tla/) and skimmed the first
chapter I was subconsciously looking for a reason not to sink a bunch of time
into yet another language/ecosystem project. That bias prevented me from
seeing the point of the first chapter.

<!-- more -->

Hillel's first chapter ends with a definition of stuttering and how in the
presence of real world temporal effects, a safe, reliable in all cases wire
transfer system borders on impossible. This initially turned me off,
sophomorically reflecting, "Well if this book won't let me make reliable
software then forget it."

This result however is precisely what formal methods and TLA+ in particular
seeks to provide. These tools tell you, in 22 lines of PlusCal that your
assumptions about the eventual consistency of your system is invalid. 

> PlusCal shows you in 22 lines that your assumptions of your are invalid. 

This simply wire transfer specification generates 25 unique system states, and
the seemingly obvious property that no money gets created or lost *doesn't
hold*.  In my experience, these types of fundamental properties are exactly
the type of thing that get's lost in requirements, and never gets checked in
testing. This is where PlusCal shines: showing you that your assumptions need
refinement. 

## [Learning Questions]({{< ref "2020-05-25-learning-process.markdown" >}})

This leads me to refine my motivation for learning TLA+ (and PlusCal).
Throughout this journey, we'll see what of these motivations hold to be true
and which are refined:

1. Build intuitive models to validate system assumptions.
1. Build models to verify the "obvious stuff".
1. Identify when system properties change.
	1. When working on a legacy system are assumptions and practices that were
	   try at the beginning of the design still true? Id est, do the
	   invariants and eventual consistent properties of the system still hold
	   after the countless features and patches added over time?


## [Anki Cards]({{< ref "2020-05-25-learning-process.markdown" >}})

1. In temporal logic {{c1::Stuttering}} is when a process simply stops.
1. Stuttering models what real world phenomena?
	1. Timeouts, slow consumers, server crashes.

