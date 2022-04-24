---
title: "C's Missing Operator" 
date: 2022-04-24T00:00:00-07:00
slug: c-missing-operator
draft: true
languages:  
- C
tags:
- study
---
I recently did a deep dive for my personal project on combinators for library design. Specifically a combinator is a function with a matching input and output type so you can combine the functions in any way. The Operators in C are combinators. Their types are compatible so you can coming say + and * together. In some languages, such as haskell, you can define functions as "infix" which means you can make a function run "between" to inputs. This allows you to make your own custom operators just like functions!

It comes back to the power of operators, and how we humans think about transformation using them. This also speaks to "what is missing" If you are buildign a compiler, which ALL languages need a compiler, what is the operators that chooses between two matching string patterns? C doesn't have one, you can define a function for this purpose, but an operator? no, C sadly doesn't let you extend the function call syntax in that way. So one could say the root missing behavior is in-fix function notation, thus making any operator possible.
