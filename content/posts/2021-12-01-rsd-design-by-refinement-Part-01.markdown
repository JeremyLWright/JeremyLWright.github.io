---
title: "Design by Refinement: TDD is not Design"
date: 2021-12-01T00:00:00-07:00
slug: rsd-sorting 
languages:
- tla+
tags:  
- Design
- book
---

American Sign Language has this beautiful word roughly translated to *blur* or *smear*. It means to blur details of a situation in order to see some greater value. It's similar to the idea of [not seeing the forest for the trees](https://idioms.thefreedictionary.com/not+see+the+forest+for+the+trees)... in order to see the forest, the bigger picture, you need to *blur* the details. 

In principle Test Driven Development (TDD[^2]) is an implementation technique. TDD promises to help it's practitioners build the described design, and not overbuild. However, in practice I've seen TDD incorrectly used if TDD stood for Test Drive *Design*. Designing software by iteratively adding tests is similar the Monte Carlo method to computing $$\pi$$[^6]. 

- Randomly place a directed/specific tests
- Adjust the implementation to conform to the new test.
- Repeat until the system sufficiently approximates our needs.

This is not design. It's exploration. There is a time and place for exploring[^3], production engineering however is not it. My main challenge against this methodology of "design by writing directed tests" is that tests cannot capture the essence of a design. I am careful to discriminate directed test here.  For I believe, interestingly, generative/property-based testing is appropriate here. In property based testing, the primary goal is to express the properties, or invariants of the system. This is good! Expressing invariants are a higher-level concept thus a level appropriate for expressing abstractions. However, property-based testing has not yet made a strong foothold in our industry, Why? I believe it's the same root of why we use TDD to "design"... we don't focus on the abstractions, we don't focus on the system directly. Instead we start with a "solution" and iterate until "it's right". We do this when group requirements as tests, and "smear them together[^1]" until we have a system. Our abstractions are thus an emergent property, never intentionally designed, we don't understand our systems well enough to know when we break those abstractions. Fine, how do we design the abstraction directly then? How do we express an abstraction without venturing too deep into ivory tower architecture. Let's look at abstractions' foil, refinement. 

<!-- more -->

# What is Refinement

Today we're going to design using TLA+'s refinement technique. Refinement is a technique that relates two descriptions. The descriptions are of the same system, but at different levels of detail, e.g, an abstract one and an implementable one. Visually, I think about refinement and abstraction as a "dial". Turning up or increasing the detail, refines a system. Turning down or decreasing detail, abstracts a system. The abstract system, we can think of as a summary of the detailed system. It will share some of the same elements by but it leaves out a lot. Yet that absence has purpose. It allows us to focus on the intent, the essence, the *abstraction* itself! This is also precisely where TLA+ helps. When we describe our abstract system we state the properties of the system as either invariants (statements that are true in every state), or temporal properties (statements that are true over a set of states). Those properties of the abstract system MUST be true of the detailed system. Hence, as we refine (add detail) TLA+ assures we continue to maintain the same design goals. 

For our design we're going to refine sorting. Refine is discussed in *The Hyperbook*[^4] at length, but I think refinement is one of those practical skills. Refinement is best learnt by doing. Reading the theory of refinement makes more sense after we've completed one. So let's dive in.

## Refinement Mappings

Define a refinement mapping...


## Good design requires revision

Sometimes it feels wasteful to _just design_. Sometimes stated as an abusive misrepresentation of the Agile Manifesto's [^5] "Working software over comprehensive documentation", but I ask what does _working_ mean? Does everyone on the team have the same understanding of _working_? Does the code achieve the same well understood outcome? Refinement is simply a concrete technique for defining that outcome. Now, the key to refinement (and good design in general) is to describe our system abstraction. Then we make incremental steps to define how our system achieves it's goals. Said another way, we want to describe **what** our system does before we describe **how**. This is sometimes mentioned as the difference in declarative and imperative code. In the case of TLA+ we can write multiple drafts of the system and show correspondence via refinement mappings. This is challenging to admit. Good design requires revision. When you realize revision is part of the process it makes sense that we don't start with code, we start with trying to understand. 

# How can we apply this?

TODO

# Acknowledgements

I am sincerely thankful for the editing effort of Chris R. and the technical feedback from Alexander N. This series would not have the flow or clarity it does without their efforts. Thank you both.

# References

[^1]: This phrase is beautiful in Sign Language. If you ever see me at a conference, please ask me for it's ASL translation. 
[^2]: Wikipedia. Test Driven Development. https://en.wikipedia.org/wiki/Test-driven_development
[^3]: Research. "Spike story" , whatever you call it, it's not production development. 
[^4]: Lamport, Leslie. The Hyperbook. https://lamport.azurewebsites.net/tla/hyperbook.html
[^5]: Beck, K. Grenning, J. et. al. Agile Manifesto. https://agilemanifesto.org/
[^6]: Academo. Estimating Pi using the Monte Carlo Method. https://academo.org/demos/estimating-pi-monte-carlo/