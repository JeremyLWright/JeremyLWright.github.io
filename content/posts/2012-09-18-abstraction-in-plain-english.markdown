---
author: admin
comments: true
date: 2012-09-18 23:11:51+00:00
layout: post
slug: abstraction-in-plain-english
title: Abstraction in Plain English
wordpress_id: 750
tags:
- System
- explaination
- explanation
- newbie
---

Abstraction is an interesting concept. For me personally, abstraction was never clearly explained. I left school and entered my first job knowing I should abstract things, but I realize now my understanding of abstraction amounted to obscurity.

<!--more-->

Abstraction to me meant, “Don’t use that thing directly, _abstract it_ and use some interface instead." "That’s what _good_ programmers do," I told myself. I taught myself a lot about function pointers, and advanced OO techniques using pure virtual classes all to avoid using something directly. This is wrong. My entire prespective on abstraction was wrong. A few days ago I was watching a [lecture from Bjarne Stroustrup](http://channel9.msdn.com/Events/GoingNative/GoingNative-2012/Keynote-Bjarne-Stroustrup-Cpp11-Style), comically, one I’ve watch before and it finally clicked.


<blockquote>Express notions as the expert in the field understands them. — Bjarne Stroustroup.</blockquote>


Wow, that is simple. Abstraction is not about creating layers or separating the programmer from anything, in fact abstraction has nothing to do with the programmer at all. Abstraction is about creating entities, may they be objects, functions or simply variables which describe the system as an expert would describe the system.

For example think of building a blackjack game. In blackjack the dealer is our expert, so we need to describe the objects in our system in a vernacular which makes sense to her. First, let us describe a bad example of abstraction with respect to the deck used for dealing cards to the players. This bad example starts with the programmer’s perspective. To a programmer, a deck looks like an array. We’ve been taught that it is not good to allocate a bunch of memory into an array so we hold an array of pointers to cards which are allocated in the heap. Okay so now we have a container to hold the cards std::vector<Card*>. For this article lets ignore the ownership issues, and continue.

What does dealing look like? Oh that’s simple, just index over the vector to give a pointer of each card to the Player.  Your code might look like this:

    
    void DealCardsToPlayer(size_t cards_to_deal, Player* p)
    {
        for(int i = 0; i < cards_to_deal; ++i)
        {
            p->AcceptCard(deck.back()); //deal from back, because dealing from front will invalidate pointers...
            deck.pop_back();
        }
    }


Now try to explain to an actual dealer what this code is doing. Firstly, you'll never be able to justify dealing from the back of the deck, [its cheating](http://en.wikipedia.org/wiki/Cheating_(casino)). The problem here isn't functional. The code will probably work. the problem is perspective. Lets reevaluate this from a dealer's perspective. A dealer has a box, called the Shoe. In the shoe are all the decks. The dealer draws from the Shoe, and give the card to the player. With the dealer’s perspective in mind the code might look like this:

    
    void DealInitialHand(Player* p)
    {
        //The rules of blackjack are defined there is no reason to make this code
        //more complex than this. The Initial hand consists of 2 cards. period.
        p->AcceptCard(Shoe->DrawCard());
        p->AcceptCard(Shoe->DrawCard());
    }


Notice we didn't use a loop. There's no reason to abstract the number of cards being dealt. The runs of blackjack are known. Is is actually an conscience decision. In Software Product Lines, this opportunity is called a variation point. It is a single point in the software where one could offer differing behavior. However, offering differing behavior is a game with defined rules is cheating. Thus unless there are other requirements to implement a variation point, keep it simple.

Functionally the code does the same thing. After either function call, the Player has 2 cards in their hand and dealer’s deck has 2 fewer cards. The difference is the perspective. The program should always follow the perspective of the “expert in the field”. There is a reason experts, in any field, have a specialized language, and specialized methods. For the most part, the principles and practices are worked out over a great deal of time to define the most efficient and accurate way to convey information.

As a programmer, steal that knowledge. Leverage all the work someone else did already, and just use the vernacular that field leverages. Doing so will make your code more readable, your programs more accurate. Furthermore, the maintenance on a system is easier. If you ever have to call an expert in to consult for the project, you’ll have objects and call flows which model the expert’s thought process. You’ll get a better response from your expert.

References:



	
  * [http://www.artima.com/intv/abstreffi.html](http://www.artima.com/intv/abstreffi.html)

	
  * [http://www.artima.com/intv/modern.html](http://www.artima.com/intv/modern.html)

	
  * [http://www.artima.com/intv/goldilocks.html](http://www.artima.com/intv/goldilocks.html)


