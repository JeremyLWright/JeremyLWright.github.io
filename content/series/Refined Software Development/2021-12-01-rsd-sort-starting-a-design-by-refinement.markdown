---
title: "TLA+ Design By Refinement: Sorting Part 1"
date: 2021-12-01T00:00:00-07:00
slug: rsd-vending 
series: ["Refined Software Development"]
languages:
- tla+
tags:  
- Design
- book
---

Today we're going to start a design using TLA+'s refinement relation technique. Refinement is a formal process of describing a system in successive increments of detail. For our design we're going to implement a refinement for sorting. Refinement is one of those practical skills that I feel is best understood by doing. Reading the theory of refinement makes more sense after we've completed one. So let's dive in.


<!-- more -->

# Designing Sorting

Now, the key to refinement (and good design in general) is to describe our system abstraction. Then we make incremental steps to define how our system achieves it's goals. Said another way, we want to describe **what** our system does before we describe **how**. As an engineer, I find this incredibly difficult. Typically when designing systems on a team, we describe pieces and components we already have. We sketch code to describe small details. While this can work, it means we're working at the wrong level of detail. We end up spending time discussing details of components before we flush out the needs of those components. Finally, it sometimes feels wasteful to _just design_ something. "Working code is the best evidence", but I ask the best evidence of what? The term working means that that code achieves some well understood outcome. Refinement is simply a concrete technique for defining that outcome. 

## Design By Refinement

I'm working on a design process that helps focus on the **what** and ignores the **how** until the end. This assures that we understand what your system is supposed to do, and we are left with a single question, "Does this system implement what we need?"

1. What is the goal? (The outcome goal of this question is to identify the domain language of the problem. It's easier for someone to start talking about their goals, than to ask them this directly.
   1. What is the domain language of the system?
1. What are the properties you want the system to hold/maintain?
1. What are the actions you want the system to perform?
1. What is a proposed solution?

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

[^1]: Pressler, Ron. _TLA+ in Practice and Theory Part 1: The Principles of TLA+_. https://pron.github.io/posts/tlaplus_part1
