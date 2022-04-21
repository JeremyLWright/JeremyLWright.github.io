---
author: admin
comments: true
date: 2013-09-01 22:35:41+00:00
layout: post
slug: my-first-logic-program
title: My First Logic Program
wordpress_id: 1170
tags:
- AI
---

This semester, I'm taking an introduction to artificial intelligence, and despite this being the second week, I've learned a great deal. Our second assignment was to implement a program in clingo (clasp on gringo) which is a derivative of Prologue. This is my first experience with a logical programming language, and I am intrigued to the possibilities.
<!--more-->
Immediately I was intrigued by the freeform expressiveness of the language. The example we did in class for example was to determine which muppet went to which amusement park. The first step was to name the _atoms_ of our program. As far as I can tell, an atom is a value.

    
    muppet(kermit;piggie;fozzie). %fozzie, piggie,and kermit are muppets
    % Muppet world
    % (From http://www.questionotd.com/2010/11/thinking-of-muppets-today.html)
    % Three of the famous Muppets travel to their favorite amusement parks using either a bike, car, or bus. From the given clues, tell which park each Muppet visited and what kind of transportation each used.
    % Kermit the Frog went to Disneyland.
    % The Muppet who went to Marine World used a bike.
    % Miss Piggy went in a car.
    % Fozzie Bear did not use a bus.
    % Only one Muppet has been to Magic Mountain.
    
    muppet(kermit;piggy;fozzie).
    vehicle(bike;bus;car).
    park(disney;magic;marine).
    



Then we simple create new functions to use as verbs. We didn't have to describe any constrains or any behavior for these "functions" at all. We simple called them as if the already exist. Actually, while seeing this in class, I leaned over and asked my classmate, "is went() a keyword in this language?" No, it isn't we just describe how the functions interact and the solver (or maybe the grounder... I don't understand the stack yet) will resolve the constraints.  With the atoms described, we create some verbs. 

    
    % travel(X,Y): X traveled using Y
    % went(X,Y) : X went to park Y
    
    :- not went(kermit,disney).
    :- muppet(X), went(X,marine), not travel(X,bike).
    :- not travel(piggy,car).
    :- travel(fozzie,bus).
    
    went(X,Y) :- not nwent(X,Y), muppet(X), park(Y).
    nwent(X,Y) :- not went(X,Y), muppet(X), park(Y).
    
    travel(X,Y) :- not ntravel(X,Y), muppet(X), vehicle(Y).
    ntravel(X,Y) :- not travel(X,Y), muppet(X), vehicle(Y).
    
    :- muppet(X), park(Y), park(Z), went(X,Y), went(X,Z), Y !=Z.
    :- muppet(X), vehicle(Y), vehicle(Z), travel(X,Y), travel(X,Z), Y !=Z.
    
    :- park(Y), muppet(U), muppet(V), went(U,Y), went(V,Y), U != V.
    :- vehicle(Y), muppet(U), muppet(V), travel(U,Y), travel(V,Y), U != V.
    
    mwent(X):- muppet(X), park(Y), went(X,Y).
    mrode(X):- muppet(X), vehicle(Y), travel(X,Y).
    
    :- muppet(X), not mwent(X).
    :- muppet(X), not mrode(X).
    
    %For every vehicle Y there is exactly one muppet which traveled in that vehicle.
    %1 { travel(X,Y) : muppet(X) } 1 :- vehicle(Y).
    %1 { travel(X,Y) : vehicle(Y) } 1 :- muppet(X).
    %1 { went(X,Y) : muppet(X) } 1 :- park(Y).
    %1 { went(X,Y) : park(Y) } 1 :- muppet(X).
    
    #hide muppet(X).
    #hide vehicle(X).
    #hide park(X).
    #hide ntravel(X,Y).
    #hide nwent(X,Y).
    #hide mwent(X).
    #hide mrode(X).


Wow! The computer then resolves the constraints and outputs the result. This is entirely new domain for me. I'm eager to learn more. I'd be eager to hear your experiences of logic programming.


