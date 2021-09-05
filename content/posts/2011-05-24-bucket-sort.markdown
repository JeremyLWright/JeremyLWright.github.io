---
author: admin
comments: true
date: 2011-05-24 04:59:59+00:00
layout: post
slug: bucket-sort
title: Bucket Sort
wordpress_id: 101
tags:
- Coding
- D
- Sorting
---

[D Source Code](https://bitbucket.org/jwright/bucket-sort/overview)

Sorting is a very important operation in computer programs. Knuth devotes an entire chapter to sorting and search. Sorting algorithms, like most algorithms, use the [Big O notation](http://en.wikipedia.org/wiki/Big_Oh_notation) to compare [computational complexity](http://en.wikipedia.org/wiki/Computational_complexity_theory).  [Bucket sort](http://en.wikipedia.org/wiki/Bucket_sort) is one such sorting algorithm.  however bucket sort typically doesn’t actually sort the array.  In the normal case, bucket sort is used to partition the data set into groups, or buckets.  Each bucket is then sorted using a separate algorithm such as quicksort, or insertion sort.

<!-- more -->

Bucket sort leverages the fact that some algorithms are more efficient on smaller lists.  [Insertion Sort](http://en.wikipedia.org/wiki/Insertion_sort) is one such algorithm.  While insertion sort has an upper bound of O(n2), on small lists its performance is typically much better.  In insertion sort, performance is limited by the delta between current position and its correct position.  For small lists, this delta is typically small.  Insertion sort, is also stable, in-place, and unlike merge sort, easy to write an efficient implementation.

D provides a number  of features that make bucket sort easier to implement, especially its fantastic array support.

    
    uint[] bucket_sort(uint[] unsorted_data, immutable uint num_buckets,
    immutable uint threads)
    {
        immutable auto interval =
                      (minPos!("a > b")(unsorted_data)[0]/num_buckets)+1;
    
        //Unique to D, arrays dimensions are "backwards" from C
        auto buckets = new uint[][num_buckets]; 
    
        foreach(uint datum; unsorted_data)
        {
            scope(failure) { writefln("%d %d %d", datum, interval, num_buckets);}
            buckets[datum/(interval)] ~= datum;
        }
    
        uint[] s;
        foreach(uint[] bucket; buckets)
        {
            s ~= bucket.sort;
        }
        return s;
    }


Line 5 illustrates an extremely powerful feature of D: Template Mixins.  Line 5 uses the “a > b” string as compiled code within the function minPos.  minPos() returns a range slice with the minimum key as the first element.  Passing the “a > b” reverses this function, ergo the maximum key is the first position.  This is an extremely powerful technique influenced from functional languages.  D also allows one to concatenate arrays easily, using the “~=” operator.  This, as you can see, makes rejoining the buckets easy.

D is a powerful language, and the lambda functions offer a whole new design perspective.  Look for my next article where I leverage D’s [TaskPool](http://www.digitalmars.com/d/2.0/phobos/std_parallelism.html#TaskPool) to parallelize bucket sort.
