---
title: "Design by Refinement Part 3: Sorting by Refinement"
date: 2021-12-28T00:00:00-07:00
slug: rsd-sorting 
series: ["Refined Software Development"]
languages:
- tla+
tags:  
- Design
- book
---

In the last two posts we've been studying refinement, and how to utilize refinement into a methodical approach to describe a system and a proposed solutions. Now let's apply it to a simple example, sorting. 

# Designing Sorting

This article is intended to be paired with it's accompanying video.

Before we begin, let's think about what we want to accomplish:

1. We want to express the essence of sorting. What is sorting? What is a definition such that *any* sorting algorithm can be shown to meet or conform to this abstract definition.
2. We want to express a specific algorithm, Bubble Sort, and show that it matches our abstract definition. 

Notice that each goal reflexively adds value to the other.

Goal 1 allows us to express the basic form of what "sort" means. This is design. We are thinking deeply about our system where we try to write down definitions that describe behaviors. When we eventually get to implementation, these invariants and properties can become properties for a QuickCheck-style test library. 

Goal 2 allows us to see that a known algorithm implements our "ideal" sorting algorithm. Additionally, Goal 2 offers evidence that our abstract definition is right! This is actually the most important outcome. If your design is wrong, it doesn't matter if all your tests pass. Identifying that your abstraction and understanding of the abstraction is right is crucial! 

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
