---
title: "The World Is Not Incremental"
date: 2021-03-03T15:00:00-07:00
draft: false
categories: 
- Design
slug: not-incremental
languages:  
- tla+
tags:
- model
---

I've been struggling to understand the stress the TLA⁺ community is putting on the presence of _math_ in the  specifications.
Namely, that specifications are not programming, and the math simplifies, by abstraction, the system. 

> What exactly is being simplified by using math, instead of "programming"?

During TLA⁺ study group this week, we discussed at least 1 aspect that applying math simplifies the description of our systems $$\rightarrow$$ The number of states.

<!-- more -->

The [Hyperbook](https://lamport.azurewebsites.net/tla/hyperbook.html) defines the standard model of digital systems as

> The Standard Model &mdash; An abstract system is described as a collection of behaviors,
> each representing a possible execution of the system, where a behavior is a 
> sequence of states and a state is an assignment of values to variables.

The subtle, intriguing part of this definition is the _a state is an assignment of values to variables_. Variables. Plural.

Hence, a state transition is not defined as an assignment, but rather a set of consistent definitions from a to b.

Consider the following C code 

```C
int main(int argc, const char *argv[])
{
	int a = 1;
	int b = 5;
	auto c = a + b;

	//State isn't complete until here..
	return 0;
}
```

Compare this to how we would represent this state in math, e.g., as part of the standard model. We abstract away the incremental nature of "assignment" and "operations". Instructions are implementation details, they are simply how we build a digital system. They are not in themselves part of our system.

$$
Init \triangleq 
  \wedge a = 1
	\wedge b = 5
	\wedge c = 1 + 5$$

However, when programming, these incremental states are real. We must consider them, especially in the presence of errors.

{{< gravizo "Example System States for C Program" >}}
  digraph G {
    a [label="A\n{a=5}"]
    b [label="B\n{a=5 b=3}"]
    c [label="C\n{a=5 b=3 c=8}"]
    done [fillcolor="grey" label="Done"]

    init -> a
    a -> b
    b -> c
    c -> done
  }
{{< /gravizo >}}

Consider a language with exceptions. You have the following

{{< gravizo "State explosions due to exceptions" >}}
  digraph G {
    a [label="A\n{a=5}"]
    b [label="B\n{a=5 b=3}"]
    c [label="C\n{a=5 b=3 c=8}"]
    done [fillcolor="grey" label="Done"]
    throw [label="Handle Exception"]

    init -> a
    a -> b
    b -> c
    c -> done
    
    init -> throw [label="throw BadThingException();"]
    a -> throw [label="throw BadThingException();"]
    b -> throw [label="throw BadThingException();"]
    c -> throw [label="throw BadThingException();"]
    throw -> done
  }
{{< /gravizo >}}

Similarly, go code has checks for nil, but the effect is the same, state explosion as the programmer assembles a particular complete state incrementally.

Thus, math allows us to more concisely describe a single atomic state. This has other impacts however though, which the hyperbook attempts to tease out in Section 2.7, Question 2.2. The next steps of my study, thus are to tackle this question and enrich my greycode specification.

# [Learning Questions]({{<ref "2020-05-25-learning-process.markdown">}})

- Express [GreyCode](https://github.com/JeremyLWright/specs/blob/algorithm/max/algorithm/GreyCodeCounter/GreyCodeCounter.tla) in TLA⁺
- Express the invariants in greycode as a temporal action instead of using ghost variables.
- Hyperbook Section 2.7: Question 2.2


# Acknowledgements

Thank you to Alexander N. for his collaboration, time and insight into TLA⁺.

