---
author: admin
comments: true
date: 2013-05-14 04:28:58+00:00
layout: post
slug: haskell-a-few-problems-later
title: Haskell a Few Problems Later
wordpress_id: 871
languages:
- Haskell
---

Well, the Haskell honeymoon is over for me. I spent some time working on a few Project Euler problems this weekend, and my initial assumptions formed from toy problems were dashed. While I was able to solve 3 problems fairly quickly, I faced a number of non trivial bugs, and memory issues. On the other side of my naïve passion, I’m finding a functional thought process, and it’s exciting.

<!--more-->

My problems were really centered around a naïve belief that Haskell could convert my inefficient algorithms to some "mathematically pure" representation. I am still learning a great deal about Haskell, and the point remains, low-level memory issues independent of "high-level" classification are ever present. As I study Haskell, I am beginning to appreciate the syntax. However, my goals for Haskell weren’t ever to use it deeply, but instead to develop my sense of functional design. Enter the python list comprehension. I use python extensively for school, and the latest project I was working on, used Python to implement a Naïve Bayesian Classifier. Essentially, one is supposed to collect all the words in document, collect all the unique words, and select all the words which are not too short or too long. Python’s list comprehensions make this elegant and fast!
    
     def text_process_all(self, exampleset):
            processed_training_set = [self.text_process_entry(i) for i in self.training_set]
            processed_training_set = filter(lambda x: len(x[0]) > 0, processed_training_set) 
    




Python’s list comprehensions are a function concept that increase the [performance](http://wiki.python.org/moin/PythonSpeed/PerformanceTips#Python_is_not_C) of python loops. The benevolent dictator for life wrote a succinct article about [loop performance in python](http://www.python.org/doc/essays/list2str.html). One outcome of this essay is that to make python fast stay inside the C part of python. List comprehensions do just this. Essentially they vectorize an operation and return back up to python once the list is composed. Functional concepts with a performance boost. Awesome.




[suffusion-adsense client='ca-pub-6284398857369558' slot='1495369305' width='728' height='90'] 
