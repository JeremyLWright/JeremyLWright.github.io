+++
date = "2012-07-21T12:24:00-07:00"
draft = false
title = "Know its Name"
slug = "know-its-name"
tags = ["c++", "Haskell"]
+++
Programming is at it's heart an struggle in communication. Source code is the communication medium with the processor; Comment the medium to other coders, and UML the medium to higher-level communication. Computer Scientists have the stereotype of being poor communicators, but in our own mediums, we're phenomenal. This fact is no where more apparent, than trying to explain source code to someone else. How does one read source code? I'm currently, learning Haskell, and my first goal is to understand this question. How can I read (out loud):
<pre lang="haskell" escaped="true">[ x * x | x &lt;- nums, x &lt; 7]</pre>
(<a href="http://www.haskell.org/haskellwiki/Haskell_Tutorial_for_C_Programmers">Reference</a>)

After some searching I found a primer to <a href="http://stackoverflow.com/questions/7746894/are-there-pronounceable-names-for-common-haskell-operators">Haskell Vocabulary</a>. Even at this basic level I see the connection to Mathematics. Therefore I'd read this statement as:

"X" times "X",  Given That, "X" takes nums, where x is greater-than 7

One of my favorite quotes about C++ goes like: "Except for the syntax, C++ is awesome.".  And in C++ it's even more critical to be able to read source code to someone. Therefore, I post a project to you, study some code you've written. Then try to read this code to someone else. It will be an interesting, and useful exercise for both of you.
