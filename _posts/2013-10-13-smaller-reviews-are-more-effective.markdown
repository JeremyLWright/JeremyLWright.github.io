---
author: admin
comments: true
date: 2013-10-13 23:00:23+00:00
layout: post
slug: smaller-reviews-are-more-effective
title: '"Smaller" Reviews are More Effective'
wordpress_id: 1158
tags:
- Review
---

I was reviewing a new software module for work today, and discovered that when the class fit on a single screen my comments were more meaningful, than when the class was larger.  My comments for spatially larger classes were mostly focused on syntactic, and idiomatic details. It was an interesting self-observation, but this certainly isn't new information.

<!--more-->

I've heard the adage that smaller reviews are more effective than larger ones. At a conference I attended hosted by Atlassian: The JIRA team noted several instances where the time per file decreased with the number of files in the review. This is an interesting observation, and certainly is intuitive thinking about corporate programming and the culture that invites. However, I think of this metric as the extra-dependency size. Where extra is the logical dependency between components of the different files. This is translatable to the system review, and I feel code is the wrong place to be finding system bugs.

Instead code reviews are supposed to look at the coding faults introduced by the coder themselves. I there there should be a new metric I'm calling the "inter-dependency" size. It is the worst case distance (In number of lines) between a bug, and its inputs. For instance:

    
    int add(int a, int b) const
     {
     return a - b;
     }


This snippet has an inter-dependency size of 2. The function call brings in the inputs, to the computation performed on those inputs. This is much easier to catch in practice than a very large function with lots of mutation. When I setup a review for my own code, I relish, even dare my co-workers to find errors. It saves me a lot of trouble to find the bug now, instead of the night of my daughter's ballet recital. I define revies as a process to maximize the probability my team will find mistakes. I then posit to design my reviews with as much care as I design the code itself, and minimize the inter-dependency size for my functions.
