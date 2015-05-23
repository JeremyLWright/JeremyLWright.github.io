+++
date = "2012-08-27T12:22:31-07:00"
draft = false
title = "The Turbulent History of Managed Code"
slug = "the-turbulent-history-of-managed-code"
tags = ["Java", "Managed Code"]
+++

Managed Code is a fascinating technology; Just-In-Time compilation provides advanced run-time optimization and strong type safety can <a href="http://channel9.msdn.com/Shows/Going+Deep/Singularity-III-Revenge-of-the-SIP">render the hardware MMU obsolete</a>. However the managed code renaissance is again in decline, and interestingly more than technology, business is changing the managed/native landscape. More than any other other metric, managed code is about maximizing programmer productivity.

<!--more-->

In 1977, Infocom released Zork. Zork was an innovative game. Its <a href="http://www.inform-fiction.org/manual/html/s34.html">sophisticated</a> linguistics made for an immersive experience for its adventurers.  Language wasn't the only innovation made by Infocom. Infocom released Zork on a custom virtual machine called the Z-Machine. Z-Machine functioned as an abstraction layer to the hardware, allowing one code base to run on multiple separate architectures. The Z-Machine was a major technical advancement, but more than that it allowed programmers to work on a single code base rather than writing duplicate code for differing architectures.

The Z-Machine afforded enormous financial benefit by allowing simultaneous release to multiple architectures. However, as Infocom discovered during the development of Cornerstone, Z-Machine did have an enormous performance overhead. Cornerstone was a business database application. Infocom decided early in development that the flexibility Z-Machine afforded Zork, would benefit Cornerstone. Cornerstone however, was not the slow paced text adventure game of Zork. Cornerstone was a serious business class application designed to compete with dBase and FoxPro. Z-Machine permitted more productive programmers but at the cost of performance. Performance Cornerstone direly required.

The Java programming language, arguably the most popular language in the world, was <a href="http://en.wikipedia.org/wiki/Write_once,_run_anywhere">solely designed</a> to optimize programmer's productivity. Sun first touted this noble goal with the statement, "Write once, run anywhere". Java makes many compromises in the name of <em>safety from the programmer</em>. The managed coder is prevented from low level access to hardware in the name of safety. If the coder cannot segfault, program will be more stable. Java automatically range checks all arrays, and provides a periodic garbage collector, all in the name of stability, security and productivity. Performance is not a metric for this target.

When Java was release, the hardware at the time was advancing rapidly. Clockspeeds were accelerating at an alarming rate. Hardware engineer's enormous effort allowed software engineers to trade performance. Simultaneously, business applications were growing ever larger. Larger applications meant larger teams. These large teams leveraged Java to help manage some of the preceived <em></em><em> problems</em> with native code. Simultaneously, this trade of performance afforded the businesses to target multiple architectures from a single code base. Managed code was making a huge surge.

In 2002, Microsoft was working on Longhorn, and Microsoft started down the same perilous road as Infocom. Jim Allchin released an edict stating that all OS interfaces shall be M<em>anaged Interfaced</em>.<em> </em>The question of the time was, "Can Managed Code solve all important problems?", leaving native code only to device drivers. Those who touch the metal.  Native interfaces were permitted, but never in place of managed ones. Microsoft saw the productivity managed interfaces afforded programmers. This meant a healthier bottom line. Microsoft attempted to leverage this harder than anyone had before.  Infocom build a database on managed technologies. Microsoft wanted to build an operating system! Longhorn had an ambitious list of features and managed code was at the center of it all. Eventually, Microsoft forwent managed code and quickly released Vista. Microsoft discovered what Infocom discovered years prior, there are certain limits to managed code's capabilities.

Fast forward to the era of cloud computing, which is simply a re-branding of yesteryear's time-share systems. Processing time is once again premium to programmer's time. On the hardware side, we've hit a limit with clock speeds. Increasing the performance of our software applications is no longer up to the hardware engineers, its now our responsibility. We no longer have the luxury of managed code.  Our responsibility is to compute some result and release the systems' resources, or for battery powered devices return to low power mode. Native code is the only tool we currently have to leverage the hardware and meet our performance goals.

Embedded systems are now ubiquitous, where the name of the game is battery life, and immersive apps. Nothing permits us to leverage the advanced features of these embedded processors like native code does. Managed code is faster now too, and will always have a place in application development. However when there is a linear relationship between cost and runtime, Native code is king.
<h4>References</h4>
<ul>
	<li><a href="http://msdn.microsoft.com/en-us/library/ms993883.aspx">http://msdn.microsoft.com/en-us/library/ms993883.aspx</a></li>
	<li><a href="http://www.theinquirer.net/inquirer/news/1004218/longhorn-to-have-managed-interfaces">http://www.theinquirer.net/inquirer/news/1004218/longhorn-to-have-managed-interfaces</a></li>
	<li><a href="http://en.wikipedia.org/wiki/Z-machine">http://en.wikipedia.org/wiki/Z-machine</a></li>
	<li><a href="http://en.wikipedia.org/wiki/Zork">http://en.wikipedia.org/wiki/Zork</a></li>
	<li><a href="http://www.inform-fiction.org/zmachine/standards/index.html">http://www.inform-fiction.org/zmachine/standards/index.html</a></li>
	<li><a href="http://en.wikipedia.org/wiki/Java_performance">http://en.wikipedia.org/wiki/Java_performance</a></li>
	<li><a href="http://en.wikipedia.org/wiki/Jim_Allchin">http://en.wikipedia.org/wiki/Jim_Allchin</a></li>
	<li><a href="http://channel9.msdn.com/Events/Lang-NEXT/Lang-NEXT-2012/-Not-Your-Father-s-C-?format=html5">http://channel9.msdn.com/Events/Lang-NEXT/Lang-NEXT-2012/-Not-Your-Father-s-C-?format=html5</a></li>
	<li><a href="http://herbsutter.com/2012/04/02/reader-qa-when-will-better-jits-save-managed-code/">http://herbsutter.com/2012/04/02/reader-qa-when-will-better-jits-save-managed-code/</a></li>
	<li><a href="http://www.gotw.ca/publications/concurrency-ddj.htm">http://www.gotw.ca/publications/concurrency-ddj.htm</a></li>
	<li><a href="http://herbsutter.com/welcome-to-the-jungle/">http://herbsutter.com/welcome-to-the-jungle/</a></li>
</ul>
