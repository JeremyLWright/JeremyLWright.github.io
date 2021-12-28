---
title: "Design by Refinement Part 2: Define your system before you propose a solution"
date: 2021-12-25T00:00:00-07:00
slug: rsd-sorting 
draft: true
series: ["Refined Software Development"]
languages:
- tla+
tags:  
- Design
- book
---

In the last post we defined refinement, and the application of refinement, the refinement mapping. How can we utilize these ideas to realize real systems?

## Design By Refinement

I have 4 steps to design by refinement: 

1. What is the goal? 
2. What are the properties you want the system to hold/maintain?
3. What are the actions you want the system to perform?
4. What is a proposed solution?

Along the way we'll see how in this sorting example that between our abstract/idea definition and our implementable/detailed definition our start and end states are the same. This will be our refinement mapping relating the two systems... but let's not get ahead of ourselves. Let's work the process.

### What is our goal

> The outcome goal of this question is to identify the domain language of the problem. 

### What properties should the system hold/maintain

> The outcome goal of this question is to identify the properties we should either maintain or conversely the properties we should never violate. In TLA+, these are our invariants and temporal properties. In Code, these are our generative tests. 


### What Actions should the system perform

> The outcome goal of this question is to identify the verbs, the *somethings* that get done. 


### What is a proposed solution?

> Notice that we haven't discussed how we will sort things. We didn't discuss specific sorting algorithms. We didn't discuss performance considerations such as time-complexity nor space-complexity. This is intentional. We are intentionally **not** discussing an implementation. We want to deal with the abstract directly. We want to express the ideals of our system before we get hamstrung by details of implementation, and the messy real world. 


# References

[^1]: This phrase is beautiful in Sign Language. If you ever see me at a conference, please ask me for it's ASL translation. 
[^2]: Wikipedia. Test Driven Development. https://en.wikipedia.org/wiki/Test-driven_development
[^3]: Research. "Spike story" , whatever you call it, it's not production development. 
[^4]: Lamport, Leslie. The Hyperbook. https://lamport.azurewebsites.net/tla/hyperbook.html
[^5]: Beck, K. Grenning, J. et. al. Agile Manifesto. https://agilemanifesto.org/