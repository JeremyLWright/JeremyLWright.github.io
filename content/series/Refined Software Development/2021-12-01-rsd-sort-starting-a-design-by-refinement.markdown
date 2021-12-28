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

In principle Test Driven Development (TDD[^2]) is an implementation technique. TDD promises to help it's practitioners build the described design, and not overbuild. However, in practice I've seen TDD used as the design methodology. Designing software in this way is similar the Monte Carlo method to computing $$\pi$$. 

- We randomly place specific tests
- We adjust the implementation to conform to the new test.
- Repeat until our system sufficiently approximates our needs.

This is not design. We're just exploring. There is a time and place for exploring[^3], production engineering however is not it. My main challenge against this methodology is that "design by writing directed tests" doesn't capture the essence of a design. Interestingly, generative/property-based testing is appropriate here. In property based testing, the primary goal is to express the properties, or invariants of the system. This is good! Expressing invariants are a higher-level concept thus a level appropriate for expressing abstractions. However, property based testing has not yet made a strong foothold in our industry. I believe it's the same root of why we use TDD to "design"... we don't focus on the abstractions of our systems directly. Instead we group requirements together as tests, and "smear them together[^1]" until we have a system. Our abstractions are thus an emergent property. Never intentionally designed, we don't understand our systems enough to know when we break those abstractions. Fine, how do we design the abstraction directly then? How do we express an abstraction without venturing too deep into ivory tower architecture. Let's look at abstractions' foil, refinement. 

<!-- more -->

# What is Refinement

Today we're going to design using TLA+'s refinement technique. Refinement is a technique that relates two descriptions. The descriptions are of the same system, but at different levels of detail, e.g, an abstract one and an implementable one. Visually, I think about refinement and abstraction as a "dial". Turning up or increasing the detail, refines a system. Turning down or decreasing detail, abstracts a system. The abstract system, we can think of as a summary of the detailed system. It will share some of the same elements by but it leaves out a lot. Yet that absence has purpose. It allows us to focus on the intent, the essence, the *abstraction* itself! This is also precisely where TLA+ helps. When we describe our abstract system we state the properties of the system as either invariants (statements that are true in every state), or temporal properties (statements that are true over a set of states). Those properties of the abstract system MUST be true of the detailed system. Hence, as we refine (add detail) TLA+ assures we continue to maintain the same design goals. 

For our design we're going to refine sorting. Refine is discussed in *The Hyperbook*[^4] at length, but I think refinement is one of those practical skills. Refinement is best learnt by doing. Reading the theory of refinement makes more sense after we've completed one. So let's dive in.

# Designing Sorting

This article is intended to be paired with it's accompanying video.

Before we begin, let's think about what we want to accomplish:

1. We want to express the essence of sorting. What is sorting? What is a definition such that *any* sorting algorithm can be shown to meet or conform to this abstract definition.
2. We want to express a specific algorithm, Bubble Sort, and show that it matches our abstract definition. 

Notice that each goal reflexively adds value to the other.

Goal 1 allows us to express the basic form of what "sort" means. This is design. We are thinking deeply about our system where we try to write down definitions that describe behaviors. When we eventually get to implementation, these invariants and properties can become properties for a QuickCheck-style test library. 

Goal 2 allows us to see that a known algorithm implements our "ideal" sorting algorithm. Additionally, Goal 2 offers evidence that our abstract definition is right! This is actually the most important outcome. If your design is wrong, it doesn't matter if all your tests pass. Identifying that your abstraction and understanding of the abstraction is right is crucial! 

## Good design requires revision

Sometimes it feels wasteful to _just design_. Sometimes stated as an abusive misrepresentation of the Agile Manifesto's [^5] "Working software over comprehensive documentation", but I ask what does _working_ mean? Does everyone on the team have the same understanding of _working_? Does the code achieve the same well understood outcome? Refinement is simply a concrete technique for defining that outcome. Now, the key to refinement (and good design in general) is to describe our system abstraction. Then we make incremental steps to define how our system achieves it's goals. Said another way, we want to describe **what** our system does before we describe **how**. This is sometimes mentioned as the difference in declarative and imperative code. In the case of TLA+ we can write multiple drafts of the system and show correspondence via refinement mappings. This is challenging to admit. Good design requires revision. When you realize revision is part of the process it makes sense that we don't start with code, we start with trying to understand. 

## Design By Refinement

I have 4 steps to design by refinement: 

1. What is the goal? 
2. What are the properties you want the system to hold/maintain?
3. What are the actions you want the system to perform?
4. What is a proposed solution?

Along the way we'll see how in this sorting example that between our abstract/idea definition and our implementable/detailed definition our start and end states are the same. This will be our refinement mapping relating the two systems... but let's not get ahead of ourselves. Let's work the process.

### What is our goal

> The outcome goal of this question is to identify the domain language of the problem. 

Given an input of values, I want an output of values in ascending order.


{{< gravizo "Ideal Sorting" >}}
  digraph G {
    Start [label="Start\n[7,3,8,1]"]
    Magic
    End [label="End\n[1,3,7,8]"]

    Start -> Magic
    Magic -> End
  }
{{< /gravizo >}}


#### Domain Language Definitions

Sorted: Sorted values are values which are ordered in an ascending or descending order. 

### What properties should the system hold/maintain

> The outcome goal of this question is to identify the properties we should either maintain or conversely the properties we should never violate. In TLA+, these are our invariants and temporal properties. In Code, these are our generative tests. 

1. Our sorting system should be resilient to an empty input. Empty inputs are already sorted.
2. Our sorting system should only sort finite sets.

### What Actions should the system perform

> The outcome goal of this question is to identify the verbs, the *somethings* that get done. 

1. Our system performs a sort on an input.

### What is a proposed solution?

> Notice that we haven't discussed how we will sort things. We didn't discuss specific sorting algorithms. We didn't discuss performance considerations such as time-complexity nor space-complexity. This is intentional. We are intentionally **not** discussing an implementation. We want to deal with the abstract directly. We want to express the ideals of our system before we get hamstrung by details of implementation, and the messy real world. 

Successively swap values until the input is sorted.

{{< figure src="/img/rsd-02-refinement/relax.png" title="Defining Sorting 2 Ways" >}}

Notice that our proposed solution and the ideal solution share the same start and end states! 

This is our refinement mapping! That's it!

- One system.
- Described two ways.
- Both ways share the same start and end states.
- The middle states can change. 

# Refinement in TLA+

Let's work through the same process, this time expressing our goals in TLA+


## What is the goal

Given an input of values, I want an output of values in ascending order.

```
IsSortedAsc(seq) == \A a,b \in 1..N: a < b => seq[a] <= seq[b]
```

## What are the properties you want the system to hold/maintain

```
EventuallySortedAsc == <>[]IsSortedAsc(A) \* Always, eventually the input is sorted
InputSizeDoesntChange == Len(A) = N \* The Input is always the same length, e.g., we cannot sort by throwing away the input.
```

## What are the actions you want the system to perform

```
SortByMagic(seq) == CHOOSE p \in Shuffle(seq) : IsSortedAsc(p) \* Given all shuffled inputs, pick the sorted one.
```

### How do we shuffle in TLA+?

```
ApplyIndices(seq, indices) == [ i \in 1..Len(seq) |-> seq[indices[i]]]
Shuffle(seq) == {ApplyIndices(seq, p) : p \in Permutations(1..Len(seq))}
```


## What is a proposed solution?

Now we have our ideal system. We checked our invariants. Let's try to implement BubbleSort in the algorithm dialect of TLA+, PlusCal.

```
(*--fair algorithm BubbleSort {
    variables A \in [1..N -> Int], A0 = A, i = 1, j = 1, totalSteps = 0;
    { while (i < N) {
        j := i + 1;
        while (j > 1 /\ A[j - 1] > A[j]) {
            A[j-1] := A[j] || A[j] := A[j - 1];
            j := j - 1;
            totalSteps := totalSteps + 1;
        };
        i := i + 1;
        totalSteps := totalSteps + 1;
    };
    }
}
*)
```

Finally, we can check correspondence between our two definitions:

```
Mapping == 
    INSTANCE sort WITH 
        \* magic sort side <- bubble sort side
        A <- IF pc = "Done" THEN A ELSE A0

Refinement == Mapping!Spec
```

# References

[^1]: This phrase is beautiful in Sign Language. If you ever see me at a conference, please ask me for it's ASL translation. 
[^2]: Wikipedia. Test Driven Development. https://en.wikipedia.org/wiki/Test-driven_development
[^3]: Research. "Spike story" , whatever you call it, it's not production development. 
[^4]: Lamport, Leslie. The Hyperbook. https://lamport.azurewebsites.net/tla/hyperbook.html
[^5]: Beck, K. Grenning, J. et. al. Agile Manifesto. https://agilemanifesto.org/