---
title: "TDD is not Design: How refinement, not tests, elucidates abstraction"
date: 2021-12-01T00:00:00-07:00
slug: rsd-sorting 
series: ["Refined Software Development"]
languages:
- tla+
tags:  
- Design
- book
---

American Sign Language has this beautiful word roughly translated to *blur* or *smear*. It means to blur details of a situation in order to see some greater value. It's similar to the idea of [not seeing the forest for the trees](https://idioms.thefreedictionary.com/not+see+the+forest+for+the+trees)... in order to see the forest, the bigger picture, you need to *blur* the details. 

In principle TDD (Test Driven Development) is an implementation technique. TDD promises to help it's practitioners build the described design, and not overbuild the said solution. However, in practice I've seen TDD used as the design methodology itself. Designing software in this way is similar the Monte Carlo method to computing $$\pi$$. 

- We randomly place specific tests
- We adjust the implementation to conform to the new test.
- Repeat until our system sufficiently approximates our needs.

This is not design. We're just exploring. There is a time and place for that, production engineering, I feel, however is not it. My main challenge against this methodology is that it doesn't capture the essence of the design needs. Interestingly, generative/property-based testing is appropriate here. It's primary goal is to express the properties, or invariants of the system. Property based testing has not yet made a strong foothold in our industry. I believe it's the same root of why we use TDD to "design"...We don't focus on the abstractions of our systems directly. Instead we group requirements together as tests, and "smear them together[^1]" until we have a system. Our abstractions are thus an emergent property. Never intentionally designed, we don't understand our systems enough to know when we break those abstractions. Fine, how do we design the abstraction directly then? How do we express an abstraction without venturing too deep into the ivory tower architecture. Let's look at abstractions' foil, refinement. 

<!-- more -->

Today we're going to start a design using TLA+'s refinement technique. I think about refinement and abstraction visually as a relaxation of the amount of detail between two descriptions of a system. The abstract system, we can think of as a summary of the detailed system. It will share some of the same elements by but it leaves out a lot. Yet that absence has purpose. It allows us to focus on the intent, the essence, the *abstract* itself!

Academically, refinement is a formal process of describing a system in successive increments of detail. For our design we're going to implement a refinement for sorting. Refinement is one of those practical skills that I feel is best understood by doing. Reading the theory of refinement makes more sense after we've completed one. So let's dive in.

# Designing Sorting

Before we begin, let's think about what we want to accomplish:

1. We want to express the essence of sorting. What is sorting in the abstract such that *any* sorting algorithm can be shown to meet or conform to this abstract definition.
2. We want to express a specific algorithm, Bubble Sort, and show that it matches our abstract definition. 

Notice that each goal reflexively adds value to the other. Goal 1, allows us to express the basic form of what "sort" means. We can use this to make properties for a QuickCheck-style test library. Goal 2 allows us to see that a known algorithm implements our "ideal" sorting algorithm. Additionally, Goal 2 offers evidence that our abstract is right! This is actually the most important outcome. Identifying that your abstraction and understanding of the abstraction is right is crucial! 

## Say What... Not How...

Now, the key to refinement (and good design in general) is to describe our system abstraction. Then we make incremental steps to define how our system achieves it's goals. Said another way, we want to describe **what** our system does before we describe **how**. As an engineer, I find this incredibly difficult. Typically when designing systems on a team, we describe pieces and components we already have. We sketch code to describe small details. While this can work, it means we're working at the wrong level of detail. We end up spending time discussing details of components before we flush out the needs of those components. Finally, it sometimes feels wasteful to _just design_ something. "Working code is the best evidence", but I ask, "...the best evidence of what?"  The term _working_ means that that code achieves some well understood outcome. Refinement is simply a concrete technique for defining that outcome. 

## Design By Refinement

I'm working on a design process that helps focus on the **what** and ignores the **how** until the end. This assures that we understand what your system is supposed to do, and we are left with a single question, "Does this system implement what we need?"

1. What is the goal? (The outcome goal of this question is to identify the domain language of the problem. It's easier for someone to start talking about their goals, than to ask them this directly.
   1. What is the domain language of the system?
1. What are the properties you want the system to hold/maintain?
1. What are the actions you want the system to perform?
1. What is a proposed solution?

{{< figure src="/img/rsd-02-refinement/relax.png" title="Defining Sorting 2 Ways" >}}

Let's apply this to sorting.

### What is our goal

Given an input of values, I want an output of values in ascending order.

#### Domain Language Definitions

Sorted: Sorted values are values which are ordered in an ascending or descending order. 

### What properties should the system hold/maintain

1. Our sorting system should be resilient to an empty input. Empty inputs are already sorted.
2. Our sorting system should only sort finite sets.

### What Actions should the system perform

1. Our system performs a sort in an input.

### What is a proposed solution?

Notice that we haven't discussed how we will sort things. We didn't discuss specific sorting algorithms. We didn't discuss performance considerations such as time-complexity nor space-complexity.





# References

[^1]: BTW, this phrase is beautiful in Sign Language. If you ever see me in a conference, please ask me for it's ASL translation. 
