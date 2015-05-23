+++
date = "2011-10-23T12:00:00-07:00"
draft = false
title = "Parallel Binary Buddy: The Friendly Memory Manager"
slug = "parallel-binary-buddy-the-friendly-memory-manager"
tags = ["c++"]

+++
<p style="text-align: center;">Fragmentation, the
allocator's sin. Each byte
A buddy, A friend</p>
<p style="text-align: left;"><!--more--></p>

<h1><a name="SECTION00010000000000000000"></a>
Introduction</h1>
Memory management is pervasive in all forms of software, not just operating systems. Embedded Systems, when dynamic memory is acceptable, tend to use memory pools to the heap. Standard desktop applications use the platform's std::new or malloc. However, when a system is more complex, a memory manager may be used. Memory managers allow the programmer to strictly control application memory, in a way that flows with the rest of the system's design. A perfect example of the power a memory manager can provide, is MegaTexture, a component in id Software's new id Tech 5 graphics engine [<a href="Report.html#SIGGRAPH2009">5</a>].

In a video game, the system has 3 levels of memory: Non-Volatile Storage (e.g. Flash or rotating media), System Memory (RAM), and Video RAM. Video RAM is by far the fastest, yet most scarce, ergo the most precious. id Tech 5 implemented a memory manger that streams graphics data between these 3 memory layers. This allows the programmer to load enormous textures; textures which would not normally fit into Video RAM. The Memory Manager treats the System RAM, and finally Non-Volatile Storage as virtual memory for the Video card. Since MegaTexture is part of a game engine, the MegaTexture knows what parts of the map need to be drawn, depending on the player's locale. Using this spacial locality, the memory manager transfers the correct textures in varying levels of detail into the video card's RAM. This way, the system always has the correct textures ready to go. This fantastic system allows id Software to run incredibly high resolution screens at 60 frames per second!

id software's MegaTexture is just one example of how a custom memory manager can simplify, and improve the quality of one's software. For this project we implemented a parallel memory manager using the Binary Buddy allocation scheme. This scheme is used in tandem with the slab allocator, to provide dynamic memory for kernel objects in the Linux kernel [<a href="Report.html#kalloc">2</a>, p. 134].
<h1><a name="SECTION00020000000000000000"></a>Architecture</h1>
The parallel architecture is largely influenced by the design offered by Johnson and Davis in their paper [<a href="Report.html#johnson">3</a>]. I used the POSIX threading library to add parallelism to the allocator. As a deviation from the design offered by Johnson, this design uses templates to prevent internal fragmentation. Templates allow one to pass in the C++ type as an argument to the allocator. The allocator, using templates, dynamically creates blocks of precisely that size. This guaranteeing that allocations will be optimized for that specific size, and multiples of that size. In this way, allocating arrays of similar objects will not result in internal fragmentation.

Interestingly, templates had a bigger affect than just space-efficiency. The templates create compile time generated pointers of the correct block size, regardless of the type. Since transactions are not translated to bytes, the code is more direct, and easier to understand. The templates created a custom block type which simplified manipulating memory blocks instead of raw byte pointers.
<h1><a name="SECTION00030000000000000000"></a>Performance</h1>
I measured the performance of the allocator using 2 metrics: overhead and allocations per second. The former is defined as the number of pending allocation requests, i.e. time spent blocked on a synchronization primitive. This time is an artifact of locking the individual memory levels while another thread allocates memory. This is wasted time and directly detrimental to the performance of the allocator. The latter is defined as raw query speed.

I setup 3 tests using allocators of various sizes. Each allocator requests memory blocks until full see Tests/TestInstrument.cpp for an example of this. As a comparison I ran a similar test against std::new. See Table <a href="#tab:perf">1</a> for results.
<div align="CENTER">

<a name="21"></a>
<table><caption><strong>Table 1:</strong>
Allocation Performance</caption>
<tbody>
<tr>
<td>
<table cellpadding="3">
<tbody>
<tr>
<td align="LEFT">Scheme</td>
<td align="CENTER">Allocation Speed (ms)</td>
<td align="RIGHT">GB/Sec</td>
</tr>
<tr>
<td align="LEFT">std::new</td>
<td align="CENTER">1.3</td>
<td align="RIGHT">102.9</td>
</tr>
<tr>
<td align="LEFT">Spinlock</td>
<td align="CENTER">5.9</td>
<td align="RIGHT">22.2</td>
</tr>
<tr>
<td align="LEFT">Mutex</td>
<td align="CENTER">12.4</td>
<td align="RIGHT">2.6</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>
&nbsp;
<div align="CENTER">

<a name="fig:speed"></a>

[caption id="attachment_486" align="aligncenter" width="695" caption="Figure 1: Raw Allocation performance."]<a href="http://www.codestrokes.com/wp-content/uploads/2011/11/SpeedComparisons.png"><img class="size-large wp-image-486" title="SpeedComparisons" src="http://www.codestrokes.com/wp-content/uploads/2011/11/SpeedComparisons-1024x768.png" alt="" width="695" height="521" /></a>[/caption]

</div>
To measure overhead in the allocator, I instrumented the request pending queues to track a ``high-water mark''. I tracked this overhead over various sized allocators, and found that the smallest levels never had waiting blocks. I expected this for the smallest levels, yet consistently the smallest 3 levels never requested an allocation to wait (Figure 3). The largest levels have at least 1 pending request, from the initial recursive split. Additionally, regardless of the allocator's native block size, the graph is similar. Block size does not affect the number of pending requests.

[caption id="attachment_481" align="aligncenter" width="695" caption="Figure 3: Pending requests as a measure of overhead."]<a href="http://www.codestrokes.com/wp-content/uploads/2011/11/combined.png"><img class="size-large wp-image-481" title="combined" src="http://www.codestrokes.com/wp-content/uploads/2011/11/combined-1024x768.png" alt="" width="695" height="521" /></a>[/caption]
<h2><a name="SECTION00031000000000000000"></a>
Beating std::new</h2>
<em>new</em> is fast. I wanted to out perform <em>std::new</em>. I was not successful; however more intrigue was the effect pthreads primitives play in the performance of an application. My initial implementation using pthread_mutex_t to synchronize. This resulted in a 10x slow-down over std::new. Simply replacing the mutexes with pthread_spinlock_t resulted in a 2x speedup over mutexes as shown in Figure 2.

[caption id="attachment_482" align="aligncenter" width="695" caption="Figure 2:On a multicore machine, spinlocks result in better performanceover mutexes"]<a href="http://www.codestrokes.com/wp-content/uploads/2011/11/NormalizedSpeedComp.png"><img class="size-large wp-image-482" title="NormalizedSpeedComp" src="http://www.codestrokes.com/wp-content/uploads/2011/11/NormalizedSpeedComp-1024x768.png" alt="" width="695" height="521" /></a>[/caption]

It is important to not however that this trade-off only happens on a multicore machine. Spinlocks are essentially very tight while loops, waiting on some condition. This does not suspend the thread. On a single core machine, spinlocks are very inefficient. The different here is that the average amount of time spent waiting for the lock, is less than cost of a system() call. So on a multicore we can block one core while another core completes the parallel request and releases the lock.
<h1><a name="SECTION00040000000000000000"></a>
Extending the STL</h1>
The Binary Buddy memory allocator is unsuitable as a general purpose STL allocator since it does not maintain the memory interface for all STL containers. For example, the STL vector guarantees that the successive items in the vector will be stored contiguously in memory. In a sense, raw pointers are permitted to access a vector, since the binary buddy does not make this guarantee, it is unsuitable for the vector [<a href="Report.html#cppstl">4</a>, p. 727]. However, the this allocator is sufficient for the STL list, or any container which is only indexed by iterators.

STL Allocators also allow for an interesting performance boost by offering locality hints to the allocator [<a href="Report.html#cppstl">4</a>, p. 733]. These hints allow upper level software to suggest efficient memory locations to lower level allocation algorithms. These hints offered as memory addresses, can boost performance up to 13% over the default FreeBSD allocator[<a href="Report.html#locality">1</a>].

More interestingly than performance, is the additional capabilities one has when using a custom allocator over a default platform one. By manually managing the heap, the developer has access to all memory use by the system. One could serialize that memory to disk, and provide a fast initialization mechanism for application restarts. A sort-of suspend for one's application. Additionally, since the allocator is setup as a gatekeeper for all application memory, its easier to log and track who is requesting what.
While this would hamper performance it is an interesting debugging tool for difficult to reproduce, multi-threaded memory bugs.

Lastly, the allocator can be used as a mock library, improving unit testing. Unlike <em>std::new</em>, the allocator under the developers control. Because of this, it is easier to simulate out of memory errors and other difficult to reproduce situations.
<h1><a name="SECTION00050000000000000000"></a>
Conclusion</h1>
The binary buddy system is a conceptually simple scheme which completely eliminates external fragmentation. When combined with C++ templates, all fragmentation may be eliminated. Offering the application developer space-efficient access to dynamic memory.

Custom allocators are difficult. Difficult to implement, even more difficult to out perform your platforms default allocator. However, the reasons for custom allocators are more than just performance. Interesting debugging tools, fast initialization, and more robust software though better testing are but a few enhancements afforded by custom memory allocators.
<h2><a name="SECTION00060000000000000000"></a>
Bibliography</h2>
<ol>
	<li>Lawerence Rauchwerger Alin Jula. Two memory allocators that use hints to improve locality. <em>Texas A&amp;M University</em>, 2009.</li>
	<li>Mel Gorman. <em>Understanding the Linux Virtual Memory Manager. </em>Prentice Hall, 2004.</li>
	<li>T. Johsson and T. Davis. Space efficient parallel buddy memory management. <em>Proceedings of the Fourth IEEE Internations Conference on
Computing and Information (ICCI'92)</em>, 1992.</li>
	<li>Nicolai M. Josuttis.<em>The C++ Standard Library</em>. Addison-Wesley, 2005.</li>
	<li>J.M.P. van Waveren. From texture virtualizaton to massive parallelization.In <em>id Tech 5 Challenges</em>, 2009. <a name="tex2html4" href="http://mrl.cs.vsb.cz/people/gaura/agu/05-JP_id_Tech_5_Challenges.pdf"></a><a href="http://mrl.cs.vsb.cz/people/gaura/agu/05-JP_id_Tech_5_Challenges.pdf">http://mrl.cs.vsb.cz/people/gaura/agu/05-JP_id_Tech_5_Challenges.pdf</a>.</li>
</ol><!--{NETBLOG_EXPORT} Yzg4ZGI0MzE2YTdmY2M5ODkzMmRiYmU1OGQ1MDcxNDU= -->
