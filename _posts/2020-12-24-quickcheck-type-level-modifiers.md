---
layout: post
title: "Using QuickCheck's Positive Type Level Modifier"
date: 2020-12-24T00:00:00-07:00
slug: quickcheck-type-level-modifiers
draft: false
tags:
- QuickCheck
- I'm Stuck
languages:
- haskell
---

One of my students this semester was struggling with the material. This
student is a very diligent worker and has been researching the problems trying
to get a better understanding of the material before digging in. Sometimes
however, there is no replacement for just digging in and coding something.
This does at least two things, it solidifies the material you're read so far,
and most importantly it shows you the limits of what you currently understand
and urges you to learn more. Interestingly, I've found in my own intellectual
endeavors some things just don't make any sense until you've tried to use it
_in anger_.

---

I gave this student the advice to

> Put down the books.
> Pick up a pencil, some paper and a compiler
> Code it. Make your brain hurt.

As I was sharing this I realized how hypocritical I was. I've *been
learning* Haskell, and yet I haven't coded in Haskell in over a year. I've
been reading books, watching videos.

> I've been a Spectator.
> It's time to be a Doer.

I started working through the codewars.com problems, specifically working on
the test cases for this [problem](https://www.codewars.com/kata/576757b1df89ecf5bd00073b/train/haskell).

While coding the QuickCheck properties (tests) for this problem however, I was
completely lost at trying to build a property with only positive generator
values.

This particular test is trying to show that the height of the pyramid is the
length of the out put array/list.


```haskell
prop_heightIsLength :: Int ->  Bool
prop_heightIsLength height = length ( buildTower height ) == height
```

However, ```buildTower``` only defined for positive values. My first pass of
the property is generates negative values (and 0 values) as input. After some
searching I was able to find the Positive type modifier for quickcheck. 

https://hackage.haskell.org/package/QuickCheck-2.4.1.1/docs/Test-QuickCheck.html#t:Positive

```haskell
prop_heightIsLength :: Positive Int ->  Bool
prop_heightIsLength height = length ( buildTower height ) == height
```

However, this doesn't compile. 

```
Couldn't match expected type ‘Positive Int’
                  with actual type ‘Int’
```

Which brings me to my biggest challenge in learning anything new. Frequently
in learning something new I don't have enough knowledge to ask the right
question, or even understand the answer. This is one of those cases.

## Failed Questions

1. haskell unwrap Positive newtype
1. haskell use QuickCheck Positive
1. haskell constraint quickcheck generator

This lead me to the closest answer

https://stackoverflow.com/questions/11910143/positive-integer-type#11910221

However, it is demonstrating how to build a custom generator. I just want to
use the built in constraints! 

> Why is this so hard?
> Because I didn't know how to read the type signature of the Postive type.

```haskell
-- This property does not compile
prop_heightIsLength :: Positive Int ->  Bool
prop_heightIsLength height = length ( buildTower height ) == height


-- This property compiles
prop_heightIsLength' :: Positive Int ->  Bool
prop_heightIsLength' (Positive height) = length ( buildTower height ) == height
```

Naively, I thought the different is the parenthesis. Remember, parenthesis are
*only used for grouping* in haskell. They have no other purpose. The different
is *what is bound to the name ```height```*. In the first version, I'm binding
a ```Positive Int``` to the name ```height``` in the second version I'm
binding merely an ```Int``` to ```height```. The Positive type modifier
assures that the values bound to it's parameter are always positive. The bound
value however will retain the ```Int``` type, even though it's value is always
positive. 

I'm unstuck now. Moving on.


