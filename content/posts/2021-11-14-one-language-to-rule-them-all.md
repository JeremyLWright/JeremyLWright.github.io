---
title: "The Language as fast at C, higher level than Python, and finer control than Assembly" 
date: 2021-11-14T00:00:00-07:00
draft: true
slug: twenty-first-century-proof
languages:  
- tla+
- tlaps
tags:
- student
- question
- discussion
- 
---


A student asked a question in discussion this week, to the effect of

> Do you think there will be a language like Python that is higher and lower level and C? 

    "One language to rule them all" it's been the promise of programming forever. At one time C was the answer to that promise. It was the "high-level" language that was still high performance. As our industry matured I think we've realized that it's about specialization and purpose. You don't expect C, a general purpose programming language, to be great at fetching data from a database. The "limited/specialized" nature of SQL is what makes it so fast and useful. The more general form, Procedural SQL, much slower. Why? Because the optimizer's hands are tied, when your hands are not. 

Similarly, you wouldn't expect Python to be excellent at floating-point rasteization? We have Shader languages for that specialized environment of GPUs.

Would you expect Basic to be excellent at Smart Contracts on a blockchain? No, it was never intended for that purpose.

I think there will never be a language to rule them all. I suspect we couldn't even write down the requirements of such a language. And even if you did, they'd be out of date by the time you finished writing the list.

<!--more-->

This weekend I skimmed Leslie Lamport's [How to Write a 21st Century Proof](https://lamport.azurewebsites.net/pubs/proof.pdf). In it Lamport discusses how mathematicians process for proof has largely unchanged since the 17th century, "...Newton's _Principia_ seem quite modern..." he states. While I don't aspire to proof, this paper provides two illuminating points I want reflect. One more philosophical regarding the nature of working smart and working hard. The second, how structure itself is worthy of praise.

# A better work smarter

My issue with the platitude, "...work smarter not harder..." is that much of the work I do is hard. Applying intelligence, rigor, or discipline doesn't not, in general, nullify hard work. Lamport's recasting is insightful. It's that because our work is hard, doing it without "smarter" approaches renders it impossible. 

> Structure makes is possible, hard work makes it probable. 

For the task at hand, proof writing, structure provides a clarity that small details aren't missed. Its the "work smarter" component of the process. Only after this is a good result possible. Only after this does the real work begin.

# Structure is work, good work.

In my daily work, "working code speaks loudest". The key operational word here is *working*. Working code speaks loudest. I feel the stress on working is too often lacking. This phrase is used to assert that we should just start coding to show or _prove[^1]_ that something is a good idea. I understand the concept of play. Playing with code/idioms/tools to see if something is possible. However, to have a consistently good, consistently working outcome, it takes structure. 

Lamport, here, discusses structure in terms of a proof. I have a phrase, 'turn the crank'. In it I mean, reduce the hard things to a process so you can just turn the crank to _crank out_ the next thing, or the incrementally better thing. A lack of structure and/or process doesn't necessarily allow one to crank. Instead it leaves each successive step with this dilemma of what direction analysis paralysis. A structure around the problem at hand, allows one to continuously cut the problem in half. Each decision cuts off a branch of work one doesn't need to do, or is not important at the moment. The last of structure leaves one without this narrowing of effort. 

# Conclusion

I enjoyed the paper, and it's filled with interesting _exercises to the reader_ around proof, and building structure. I'm choosing to ignore these for now, and focus on model checking as I work on a new project idea called "Riffing Algorithms". 


[^1]: Prove in the colloquial sense, not the rigorous. mathematical sense.
