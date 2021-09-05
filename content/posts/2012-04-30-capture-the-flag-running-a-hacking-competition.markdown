---
author: admin
comments: true
date: 2012-04-30 02:38:44+00:00
layout: post
slug: capture-the-flag-running-a-hacking-competition
title: Capture the Flag - Running a Hacking Competition
wordpress_id: 611
expiryDate: 2020-01-01T00:00:00+00:00
tags:
- CTF
- Security
- cracking
- event
- hack-a-thon
- hacking
---

Black-Hat hacking in an controlled environment, like this, is an important skill for software developers. The [Art of War](http://en.wikipedia.org/wiki/The_Art_of_War) describes knowing one's enemy, and with the prevalence of internet-enabled applications today, it has never been more critical to know how the "enemy" can take down a system. While capture-the-flag is a fun, and exciting intellectual game, it is serious training for software engineers of all types, and skill levels. I recently setup a small capture the flag event for the [Arizona Linux User's Group](http://asulug.org/), and it was very fun.

To setup a catpure the flag event, here are a few guidelines I found useful:



	
  * Brute-force attacks are no fun. There is no intellect involved, and while one brute forces the box, no one else can have a try.

	
  * Setup a box to provide services to the rest of the network. Clearly define this box as off limits.

	
  * Use virtual machines for target systems. This allows one to restore the system from an image if someone goes too far.

	
  * Physically separate the game from any other networks.

	
  * Provide ISOs of [Backtrack](http://www.backtrack-linux.org/) Linux


<!-- more -->Organizing a hacking event takes time, and planning.

For this event I setup 3 systems:

	
  * A host system which provided DNS, and hosted the virtual machines.

	
  * A Windows 2000 virtual machine.

	
  * A Ubuntu 12.04 virtual machine.


The windows 2000 box has a pile of vulnerabilities. These vulnerabilities have been scripted into hacking applications, which allow automatic take down of the system. This is not necessarily a bad thing however, since it does provide a level of accomplishment, and is conducive to hiding clues. One clue I thought of after this event, was to set the [background](http://en.wikipedia.org/wiki/Steganography) to something with [hidden](http://en.wikipedia.org/wiki/Steganography) data in it. Tools exist to analyse the entropy of an image to determine if it contains data. One could encode the hash of some password into the image, then use a rainbow table to decrypt the hash.






Essentially, break down the event into a series of quests. All quests lead to the same end i.e. network domination and a free round at the happy hour, but some paths are different than others. One quest may have more intellectual clues stenography, SQL injection, riddles which yield a password a la King's Quest. Another path may be fraught with vulnerabilities. The latter requires a encyclopedic knowledge of known vulnerabilities to crack this quest. I recommend making this path longer, since Google skills can shorten it immensely.

Next, determine how the game will be scored and clearly post this information. For the latest event I hosted, I posted all the objectives at the front of the room, and wrote someones name as each objective was acquired. This worked well, but a more interactive system would be far more exciting. Something that showed the dominance and protection of different network factions. Honestly, this is more work, but certainly provides more excitement to the game.

Lastly, make the event fun, and provide other activities for those who don't want to hack. This can be a very fun event, yet still important to learning how to build secure software. Ping me if you have other ideas for a hacking event, or post in the comments :-).


