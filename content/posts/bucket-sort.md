+++
date = "2011-05-23T21:59:00-07:00"
draft = false
title = "Bucket Sort"
slug = "bucket-sort"
tags = ["D", "Sorting"]

+++
<a title="D Source Code" href="https://bitbucket.org/jwright/bucket-sort/overview">D Source Code</a>

Sorting is a very important operation in computer programs. Knuth devotes an entire chapter to sorting and search. Sorting algorithms, like most algorithms, use the <a href="http://en.wikipedia.org/wiki/Big_Oh_notation">Big O notation</a> to compare <a href="http://en.wikipedia.org/wiki/Computational_complexity_theory">computational complexity</a>.  <a href="http://en.wikipedia.org/wiki/Bucket_sort">Bucket sort</a> is one such sorting algorithm.  however bucket sort typically doesn’t actually sort the array.  In the normal case, bucket sort is used to partition the data set into groups, or buckets.  Each bucket is then sorted using a separate algorithm such as quicksort, or insertion sort.

<!--more-->

Bucket sort leverages the fact that some algorithms are more efficient on smaller lists.  <a href="http://en.wikipedia.org/wiki/Insertion_sort">Insertion Sort</a> is one such algorithm.  While insertion sort has an upper bound of O(n<sup>2</sup>), on small lists its performance is typically much better.  In insertion sort, performance is limited by the delta between current position and its correct position.  For small lists, this delta is typically small.  Insertion sort, is also stable, in-place, and unlike merge sort, easy to write an efficient implementation.

D provides a number  of features that make bucket sort easier to implement, especially its fantastic array support.
<pre lang="d" escaped="true">uint[] bucket_sort(uint[] unsorted_data, immutable uint num_buckets,
immutable uint threads)
{
    immutable auto interval =
                  (minPos!("a &gt; b")(unsorted_data)[0]/num_buckets)+1;

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
}</pre>
Line 5 illustrates an extremely powerful feature of D: Template Mixins.  Line 5 uses the “a &gt; b” string as compiled code within the function minPos.  minPos() returns a range slice with the minimum key as the first element.  Passing the “a &gt; b” reverses this function, ergo the maximum key is the first position.  This is an extremely powerful technique influenced from functional languages.  D also allows one to concatenate arrays easily, using the “~=” operator.  This, as you can see, makes rejoining the buckets easy.

D is a powerful language, and the lambda functions offer a whole new design perspective.  Look for my next article where I leverage D’s <a href="http://www.digitalmars.com/d/2.0/phobos/std_parallelism.html#TaskPool">TaskPool</a> to parallelize bucket sort.
