---
title: "What can't flowcharts do?" 
date: 2022-04-24T00:00:00-07:00
slug: flowcharts-cant
tags:
- student
---

When we begin programming we're often taught to start with flowcharts. This is not bad advice. Flowcharts are a tool to help you slowdown and focus on an ordering of events or actions. Together these actions achieve some outcome. This series of actions to achieve an outcome we call an algorithm. Great! Now we're really programming. However, it can seem (at the beginning) that flowcharts can capture any set of ordered work. Alas, this is not true. Flowcharts do a poor job of describing distributed algorithms. Yes you can define a given trace of the confluence of multiple actors, but 1 flowchart to rule them all? No. 

Systems of systems and concurrent mutation cannot be expressed well in a flowchart. When you have multiple systems running at the same time they each have their own _independent_ flowchart. The confluence of these flowcharts running at the same time is not easily expressed (at least to humans) due to interleaving. Interleaving is the various independent states interaction in random "befores" and "afters". In a distributed system, unless the algorithm specifically orders these events, they are random. You can have ANY ordering of states across each independent system. Can you draw an non-deterministic ordering of parallel states? 

This enters the world of formal methods tools like TLA+ and Alloy. Instead of drawing each state, you discuss the relationships between states. Hence, you define each transition. Then tooling (TLA+'s model checker TLC, or Alloy's Instance Generator) follow relationships and check that system constraints hold across all orderings.

Hence, don't draw states. Describe relationships, and let the computer check states. 

