---
author: admin
comments: true
date: 2013-04-22 05:29:11+00:00
layout: post
slug: haskell-day-1-again
title: Haskell Day 1 (Again)
wordpress_id: 850
categories:
- Functional
tags:
- functional
languages:
- Haskell
---

I've restarted my haskell programming education. Here is my implementation of [FizzBuzz](http://imranontech.com/2007/01/24/using-fizzbuzz-to-find-developers-who-grok-coding/)
<!-- more -->

    
    
    fizzbuzz x | x `mod` 15 == 0 = "FIZZBUZZ"
               | x `mod` 3  == 0 = "FIZZ"
               | x `mod` 5  == 0 = "BUZZ"
               | otherwise       = show x
    
    main = print (map fizzbuzz [1..100])
    


[suffusion-adsense client='ca-pub-6284398857369558' slot='1495369305' width='728' height='90']
