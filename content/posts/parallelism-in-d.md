+++
date = "2011-05-23T21:59:00-07:00"
draft = false
title = "Parallelism in D"
slug = "parallelism-in-d-bucket-sort-part-2"
tags = ["D", "Sorting", "parallel", "real-time"]

+++
Parallelism, it sounds like a religion, and in some sense it is. Like many facets of software engineering, writing good parallel code is more of an art than a science.  I come from a FPGA background where parallelism is part of the language; part of the culture! The tools are designed to find deadlocks, analyze timing and the language itself is fully aware of parallelism.  The hardware world understands parallelism, yet writing parallel software is still difficult.  D is making some pioneering steps in the right direction for <a href="http://www.digitalmars.com/d/2.0/phobos/std_parallelism.html">parallelism</a>.  I use a parallel implementation of bucket sort to show how D makes writing parallel code, correct.

<!--more-->

Parallelism is ingrained in the hardware engineer’s mind. The motivating purpose of parallelism is <strong>performance. </strong>There is simply no other justification for the pains of parallelism except the high performance potential it offers. The FPGA engineer’s tool-chain evolves around this fact.  The tools are designed to find deadlocks, analyze timing; however the most valuable feature is that the language itself is fully aware of parallelism. Take this simple Verilog example:
<pre lang="verilog" escaped="true">always @ (posedge clock or negedge reset_n)
begin
    if (reset_n == 1'b0) begin
        counter_out &lt;=#1  4'b0000;
    end
    else if (enable == 1'b1) begin
        counter_out &lt;=#1  counter_out + 1;
        counter_in &lt;=#1 counter_in - 1;
        led_out &lt;=#1 led_out ^ 1;
    end
end</pre>
The &lt;= operator is called the non-blocking assignment.  In the example above, all three lines in the else condition execute simultaneously.  This is important; just by reading the code you can see that it is parallel.  Our software languages, C, C++, Java, do not make parallel code obvious.  In these languages parallelism tends to feel like a bolt-on, aftermarket feature that never really flows with the rest of the language, or design idioms.  While researching the background on this article, I found a fantastic write up on <a href="http://www.futurechips.org/tips-for-power-coders/parallel-programming.html">What Makes Parallel Programs Hard</a>.  The author contends that parallel programs are hard because of inter-task dependencies.  This is true, but I would further the point that if the language supported parallelism at its core, as Hardware Description Languages do, writing parallel software wouldn’t be so difficult. Furthermore, if a language offered parallel idioms, duplicating robust parallel code would also be easier.

HDLs make it obvious that the code is parallel, until D I haven’t seen a language do it quite so well.  <a href="http://www.codestrokes.com/?p=101">Bucket Sort Part 1</a> was a quick introduction to Bucket Sort as an algorithm, but the real power of bucket sort is how easily it can be parallelized. Once the list is segmented or “bucketized” each bucket may be sorted simultaneously.  I wrote a D implementation of this, and parallelism really offers incredible performance here.  Take a look.<a href="http://www.codestrokes.com/wp-content/uploads/2011/05/threading_compared.png"><img style="background-image: none; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border-width: 0px;" title="threading_compared" src="http://www.codestrokes.com/wp-content/uploads/2011/05/threading_compared_thumb.png" alt="threading_compared" width="1026" height="768" border="0" /></a>

This compares the runtimes of sorting 10 million numbers using various configurations of bucket sort.  Consistently, the multithreaded version is faster.  So how does D makes this easy?
<pre lang="d" escaped="true">uint[] bucket_sort(uint[] unsorted_data, immutable uint num_buckets)
{
    immutable auto interval = (minPos!("a &gt; b")(unsorted_data)[0]/num_buckets)+1;
    auto buckets = new uint[][num_buckets];

    foreach(uint datum; unsorted_data)
    {
        scope(failure) { writefln("%d %d %d", datum, interval, num_buckets);}
        buckets[datum/(interval)] ~= datum;
    }

    uint[] s;
    version(MultiThreaded)
    {
        foreach(ref bucket; taskPool.parallel(buckets))
        {
            bucket.sort;
        }

    }
    else
    {
        foreach(uint[] bucket; buckets)
        {
            bucket.sort;
        }
    }

    foreach(uint[] bucket; buckets)
    {
        s ~= bucket;
    }
    return s;
}</pre>
This code has the obviousness we are looking for.  taskPool.parallel comes from the <a href="http://www.digitalmars.com/d/2.0/phobos/std_parallelism.html">std.parallelism</a> module starting in <a href="http://www.digitalmars.com/d/download.html">D 2.053</a>.  Simply, by reading the source code, one can see that this code is parallel.  That’s it. The taskPool.parallel routine automatically divvies out units of work between new threads; more importantly, taskPool.parallel automatically joins all threads them at the end of the foreach scope.

Using this, we can find the optimal configuration of bucket size for both single-threaded and multi-threaded versions of the code.

<a href="http://www.codestrokes.com/wp-content/uploads/2011/05/single_threaded.png"><img style="background-image: none; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border-width: 0px;" title="single_threaded" src="http://www.codestrokes.com/wp-content/uploads/2011/05/single_threaded_thumb.png" alt="single_threaded" width="1026" height="768" border="0" /></a>

<a href="http://www.codestrokes.com/wp-content/uploads/2011/05/multi_threaded.png"><img style="background-image: none; padding-left: 0px; padding-right: 0px; display: inline; padding-top: 0px; border-width: 0px;" title="multi_threaded" src="http://www.codestrokes.com/wp-content/uploads/2011/05/multi_threaded_thumb.png" alt="multi_threaded" width="1026" height="768" border="0" /></a>

Interestingly, the optimal setting was different between the multithreaded and single threaded versions with multithreaded at 800 buckets and single threaded at 45,800 buckets.  However we can see from the standard deviation plots a sizable variation within a single configuration’s bucket size, while the average runtimes remains fairly flat.  Ergo, bucket size is not the performance bottle neck, it’s the actual sorting, and parallelism drastically illustrates this in the “Threading Compared” plot.

D provides two primary multithreading techniques, <a href="http://www.digitalmars.com/d/2.0/phobos/std_parallelism.html">std.parallelism</a>, discussed here, and <a href="http://www.digitalmars.com/d/2.0/phobos/std_concurrency.html">std.concurrency</a> with a powerful message passing framework for effective inter-thread communication.  D makes robust, readable, parallel code, easy and correct.  In our case of bucket sort, with only a single line of code.
