---
title: "Flowcharts as a Conversation: Rubber Ducking our Designs"
date: 2021-11-08T00:00:00-07:00
slug: rsd-vending 
series: ["Refined Software Development"]
languages:
- tla+
tags:  
- Design
- book
---

Imagine a design process as a conversation. What could you accomplish if you could
ask your designs questions? That flow chart on the wall or whiteboard... What
would you ask it if you could? 

# The Devil is in the Details

Have you ever worked with a detail-oriented colleague? One of those
individuals who consistently asks you to clarify your position. Whenever you
make an adjustment, this colleague goes back and rechecks all previous
statements. They're your partner.  They aren't there to affirm you, or your ego.
They are there to assure the work you do is as correct as it can be. They
allow you to remain mentally at the high-level concepts, while they concern
themselves with the minutia.  Our experience shows us that it is the minutia
that introduces fundamental flaws, concepts we addressed, but relaxed for some
other constraint suddenly renders our algorithms errant. The English idiom,
_the devil is in the details_ is nowhere less true than software.

In this post, I propose [TLA+](https://github.com/tlaplus)[^2] is your
detail-oriented colleague, a mechanical friend for transforming your
flowcharts and design sketches into a conversation where the computer helps
you identify gaps and fallacies. We'll also see how [TLA+ can draw your flowcharts](/img/soda.png) as well so you don't lose that visual feedback.

TLA+ is a specification language. TLA+ targets a tool called TLC. Together
they can help you design applications, especially concurrent and parallel
systems. TLA+ while being a deeply rigorous verification tool for parallel
systems, can also be used for sketching simple systems. Engineers and students
alike use flow charts to sketch their programs. TLA+ can be used for these
simple use cases as well a conversational transformation from a static description
of boxes and arrows to a interactive conversation. 

## Caveats to the reader

If you are a reader who's an accomplished programmer, or you know programming
and software engineering well, this post may seem simplistic, however I encourage
you to read this post and watch the video[^3]. TLA+ is a deep tool but it is
only through humility that we can learn to express it's power. TLA+ will
render you a beginner again. This is a good thing, although you will not feel
productive immediately. You will not skim the book over a weekend and apply it
to your problem on Monday.  This will take time, but I believe it is time well
spent. 

Give TLA+ a chance to work *on* you, so that it can work *for* you.

This post is intended to be paired with a video[^3].

<!-- more -->

# Without TLA+ we design with a 'Yes-Man'

Whiteboards don't check anything. They are a medium for getting
your thoughts out of your head. This is a great technique for slowing down,
yes. When you need to brainstorm, or *ideation* you don't want that detail
focus. In that phase, Whiteboards are great! Use them! However, once that
phase is done, jumping from whiteboards to coding could be a mistake.
Whiteboards don't check anything. They don't help reason through the details.
They don't check that the system actually achieves your goal. They don't check
that the system has subtlety errant transitions.

## A Simple Vending Machine

For example, given a sketch of a vending machine, you could ask questions such
as, "Will you vend soda without money?" Or potentially you could ask, "What
would you do if you ran out of soda?" Conversation is a powerful tool for
thought, however the quality of the conversation as a diagnostic tool is
dependent on who the conversation is with. 

{{< gravizo "What would you ask a flowchart?" >}}
digraph A {
"Want Soda" -> "Have Soda" [label="Money in Machine"];
"Have Soda" -> "Want Soda" [label="Drink Soda"];
}
{{< /gravizo >}}


This graph is simple, but as we can immediately see it's too simple to express
our needs. It doesn't capture how much money we have, or that our money is
decreasing as we drink soda. In the traditional paradigm, we just add more
states


{{< gravizo "More detail, but still hard to 'check'" >}}
digraph A {
"I have money?" -> "I Want Soda" [label="Yes"];
"I have money?" -> "???" [label="No"]; 
"I Want Soda" -> "I Have Soda" [label="Money in Machine"];
"I Have Soda" -> "I Want Soda" [label="Drink Soda"];
}
{{< /gravizo >}}

What happens when you don't have money? If your design as a conversation, and
entity you could interview, not only would the design process be more
collaborative, but your designs would be more resistant to change.  Finally,
instead of just drawing within a design tool, using the computer for little
more than a collaborative scratch-pad the computer itself would be a colleague
assisting your design and though process.  Helping to identify details you may
mentally _skip over_. 

Now, herein lies the value of leaving the whiteboard, and providing
a checkable system definition. We could, with enough effort and time prove to
ourselves that the system is sound. Given enough effort and time, we could
potentially be correct. However we don't build systems alone. For your next
colleague to understand the system they'd have to apply the same thought
process, the same rigorous, tedious, process to prove to themselves they
understand the system and that it achieves the goal. Furthermore, this process?
Includes you. You have to be present in transferring that knowledge. Other
engineering disciplines don't do this. They produce blueprints, models,
*finite element analyses*, that serve are checkable artifacts the system
design is sound, that the components chosen meet specified criteria. We
software engineers should be so bold to follow the footsteps of the
hard-sciences and specify our systems.  

# Setting up TLA+

Markus Kuppe has a great walk through of using the toolbox[^1]. If you simply hate Eclipse, that's
understandable and there is a VS Code offering as well. However, if you are
using TLA+ for the first time, I recommend trying the toolbox since it's the
easiest to get started. In my experience defining the models takes some tribal
knowledge in the VS code style. While it's easier for a git workflow, it takes
some getting used to. Try the toolbox first, then decide if you should choose
VS Code instead.

## Setup TLC to draw flowcharts/state-diagrams

Add parameters to the TLC command line in the toolbox ``-dump dot,actionlabels,colorize,snapshot  soda.dot``
[Configure TLC to dump state diagram](/img/2021-11-03-tla-plus-as-a-flowchart.png)

Doing this will dump a new file ``soda.dot`` every time the model is run.
I like to put an fswatch on the dot file so the diagram redraws automatically.

``
fswatch -o soda.dot | xargs -n1 dot soda.dot -Tpng -osoda.png
``

Now everytime soda.dot changes, the dot compiler will make a new png.

# Sketching out soda machine

Imagine we have the following toy program or assignment.

> Design a vending machine. 
> 1. The machine must take money, and deliver soda. 
> 1. If no soda is available then the machine must not keep the money.

What's your traditional design process? Sketch a flowchart, or some UML? Let's
take a step back and recall how we used to design things before we were
programmers. Those first programs we design where it all fit inside ``main()
``  because we didn't know how to make functions yet. In a word, Let's Start
Simply.

## What are the variables? 

1. I, the user, wants soda, so lets make a variable for that ``IWantSoda``
1. Next, there is a soda machine with some number of sodas inside
   ``sodaMachine``
1. I could presently have a soda or not, ``IHaveSoda``
1. Finally, I have some amount of money, ``Money``


The professional programmers among you may be thinking
now about abstractions. The electrical engineers among you may be thinking how
the hardware will function or what interrupts need to be configured. These are
good, but let's come _up_ a level of detail. In a future post I will describe
_refinement_ as a method of connecting a very high-level description, the
essence/pseudocode of our designs to an actual design.

Great, now that we have the variables let's consider what possible values
those variables have. 

1. ``Money`` must be greater than or equal to 0.
1. ``sodaMachine`` must be greater than or equal to 0 sodas.
1. ``IWantSoda`` is true or false.
1. ``IHaveSoda`` is true or false.

That's it. That's our domain. So let's next consider our actions.

## What are the Actions?

An action in TLA+ is a transition between states. It's simply the edges of our
flowchart.

{{< gravizo "Edges are actions" >}}
digraph A {
"Some State A" -> "Some State B" [label="Edges are actions"];
}
{{< /gravizo >}}

1. If the soda machine has soda, and I don't, then I put money in the machine.
   That's an action ``PutMoneyInMachine`` (This might become
   a function/procedure in our final program, but for now, let's just call it
   an action)
	1. When I put money in the machine either the machine has soda, or it
	   doesn't. If it does then the machine takes my money and gives me
	   a soda.

That's it. Our system is pretty simple, when we have money, we buy soda until
the machine is out of soda, or we are out of money. So far, TLA+ hasn't given
us anything a normal flowchart can't, but we're about to make our flowchart
answer questions. 

## Interviewing our Flowchart

What would you ask our design if you could? Perhaps, Do I eventually got soda?
TLA+ uses a branch of mathematics called Temporal Logic, which allows us to
ask questions such as _eventually_ and _always_. Additionally, we can combine
these to ask if "once something happens it remains". In TLA+ we express these
questions with ``<> means eventually`` and ``[] means always``.

| English | TLA+ |
|---------|------|
| eventually | ``<>`` |
| always | ``[]`` |

Thus our question:

| English | TLA+ |
|---------|------|
| "Do I eventually get soda" | ``<>IHaveSoda`` (Remember IHaveSoda TRUE or FALSE, i.e., ``IHaveSoda \in {TRUE, FALSE}``). |

However, we can only have soda, if we have money, hence we need to express the
idea if "_always_ when I have money, then _eventually_ I have soda" This is called
"implication" in TLA+ we express this as ``[](IHaveMoney => <>IHaveSoda)`` 

| English | TLA+ |
|---------|------|
| _always_ when I have money, then _eventually_ I have soda | ``[](IHaveMoney => <>IHaveSoda)`` |

However, as we'll see in the video[^3], TLC finds a counter-example for this
temporal equation. TLC shows us a case we didn't consider.

That's it! Let's model this in TLA+ and see how the process makes our designs
interactive. Follow along with the video[^3], or check-out the spec and play with
it yourself. 

# Acknowledgements

My deepest thanks to my colleagues for providing an environment conducive of
learning and applying this material. I'd like to thank [Alexander Niederbühl](https://github.com/Alexander-N) for his review of this post and his
consistent attendance of our TLA+ study group. I'd like to thank [John McConnell](https://github.com/johnmcconnell) for asking thought provoking
questions that drive me to better understand. Finally, I'd like to thank the TLA+
mailing list for kindly engaging with my questions and taking each question as
an opportunity to teach.

# References

[^1]: Kuppe, Markus. TLA+ Toolbox. https://www.youtube.com/watch?v=U2FAnyPygrA
[^2]: TLC is an explicit state model checker for specifications written in TLA+. The TLA+Toolbox is an IDE for TLA+.  https://github.com/tlaplus
[^3]: Wright, Jeremy. Sketching Designs with TLA+. https://youtu.be/kUpYe3X48mg
