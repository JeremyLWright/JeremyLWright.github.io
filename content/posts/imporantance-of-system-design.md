+++
date = "2012-07-15T10:00:00-07:00"
draft = false
title = "The Importance of System Design"
slug = "the-importance-of-system-design"
tags = ["top-down", "bottom-up"]
+++

For the small programs we tend to implement as part of a semester project, or the simple "one-off/get-it-done" programs at work, system design rarely plays a part. However, even in the smallest problems a top-level system design is critical for consistency and ease of use. Class components, regardless of how precise and accurate they are in their own internal design, if they aren't externally consistent with other objects, the system will be brittle, and difficult to use.

<!--more-->

In a recent project, I used a bottom-up approach. I designed each class in isolation. I was very diligent to define the ownership semantics, and use each smart pointer and r-value reference type correctly. Despite all the time spent on the details of each object, when I tried to use the objects together, their interfaces were so inconsistent the individual objects were unusable. Case in point:
<pre lang="cpp" escaped="true">for(auto playersHand : player)
{
    if(playersHand-&gt;Value() &gt; dealersHand-&gt;Value())
    {
        player.Win(*playersHand-&gt;GetBet().get()); //&lt;-- This is a red-flag
    }
}</pre>
If you have to retrieve the raw pointer from the smart_pointer container, you are doing something wrong.

Here the Player wants a reference to the winning Bet. The player doesn't own the bet, nor does it modify it, it just wants a reference, so I used the <em>passing by const-to-reference</em> idiom. The Hand however shares a reference between the Table, and the Player. So I used a shared_ptr&lt;Bet&gt;.  shared_ptr implies that it owns and entirely manages the underlying pointer. Smart pointers can reduce or eliminate raw pointers in your system, making it safer. Fetching the raw pointer from such a container invites even bigger problems than managing the raw pointer yourself. Now you have two entities claiming ownership of a raw pointer. This is a fast way to a double-delete problem or more likely a memory leak.

C++11 contains a powerful number of tools to allow more general components in our designs. This is however, a two-edge sword. Generic components are great. They enable tested code to be reused across multiple projects. This alone improve quality, and reduces time-to-market. Derisking our projects is a very positive thing, and we should continue doing so.
<blockquote class="pullquote">Time-to-market is an important metric for academic projects as well. Reducing time-to-market, derisks your ability to complete the project before the due date. This allows you to tackle a more ambitious solution...</blockquote>
C++11's generalization tools also allow code to be more easily refactored. Take for instance the following C++98 code:
<pre lang="cpp" escaped="true"> for(vector&lt;shared_ptr &gt;::iterator player = players_.begin(); 
    player != players_.end();
    ++player)
{
    for(vector&lt;shared_ptr &gt;::iterator playersHand = player.begin();
            playersHand != player.end();
            ++playersHand)
    {
        /** ... Other Code Here ... */
    }
}</pre>
Compared to the equivalent C++11 code.
<pre lang="cpp" escaped="false">for(auto player : players_)
{
    for(auto playersHand : player)
    {
        /** ... Other Code Here ... */
    }
}</pre>
Now, typedefs can help here, but the C++11 version is still far more general. There are no types explicitly called out in the for loops. This is immensely powerful. It allows one to change the underlying container in each type, and the for loop simply iterates over the new type. This makes refactoring easier, but making the code more general also makes a system design more important than ever. As our code becomes more general its more important that types behave consistantly. For example, look at the C++98 version above. By looking at the iterator declaration, we know that we're iterating over a shared pointer, ergo we'll use the -&gt; operator. However in the C++11 version we have no idea what type player is. Its declared with auto, and fed by our user defined type. Where C++98 used declarations to state the interface, C++11 requires consistency.

Within a program, the designer must make broad statements over the objects' behavior. If all objects within a system behave the same, then the users of those components can expect a certain level consistency. It becomes clear which use cases of an object are correct and which are not. This follows from Joel Spolsky's idiom <a href="http://www.joelonsoftware.com/articles/Wrong.html">Make Wrong Code Look Wrong</a>.  The compiler can tell us we are using the wrong operator, but this is a sign that we're lacking a consistent interface with our objects. Notice however that the compiler cannot tell us if we are using the object in a semantically incorrect way. Just because it compiles, doesn't mean its right. Scott Meyers puts this as: "Make interfaces easy to use correctly and hard to use incorrectly."

Use the new generalization tools in C++11. It will make your code better. Our programs have always needed a system-design; it's simply more apparent now. C++11 enables you to make better quality systems by forcing consistency across your objects and simultaneously making your code more general <a href="http://tirania.org/blog/archive/2012/Apr-04.html">without sacrificing performance</a>.

&nbsp;
