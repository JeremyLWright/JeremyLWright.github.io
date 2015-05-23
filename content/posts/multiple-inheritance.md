+++
date = "2011-09-21T23:00:00-07:00"
draft = true
title = "Multiple Inheritance: Dangerous Elegance"
slug = "multiple-inheritance-dangerous-elegance"
tags = ["c++", "practicum", "productivity", "Python", "Tools"]

+++
Object-Orientation permits one to model software components in a very natural way.  By decomposing properties of some model into objects one may compose very complex entities in a simple, usable fashion. C++ expands these powerful object composition techniques with multiple inheritance.  Yet multiple inheritance introduces a new subtle problem, called the diamond problem which very easily finds its way into real-world programs.  When composing inheritance trees of any depth, one must be cognizant of this problem.

<!--more-->
The Diamond Problem is a subtle manifestation from using inheritance in C++. Typically, languages such as Java avoid this issue by only allowing one to inherit from multiple interfaces, not multiple classes.  Yet C++ is lax in its definition of abstract/interfaces classes. Since C++ doesn't explicitly define abstract classes, allow me to define a common vocabulary.

Abstract Class: Any class in C++ is any class which contains at least 1 pure-virtual function.

Interface Class: Any class in C++ which defines <strong>only </strong>pure-virtual functions.

<a href="http://en.wikipedia.org/wiki/Virtual_function#Abstract_classes_and_pure_virtual_functions">Pure-Virtual Function</a>: A member function who provides no implementation and thereby requires a subclass to override it's behavior.

Consider the following diagram:
<p style="text-align: center;"><a href="http://en.wikipedia.org/wiki/Diamond_problem"><img class="aligncenter" title="Diamond Problem" src="http://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Diamond_inheritance.svg/220px-Diamond_inheritance.svg.png" alt="Diamond Problem diagram from wikipedia" width="220" height="330" /></a></p>
If class A implements some function myMethod() and class C overrides myMethod(), providing different behavior.  From who does class D inherit myMethod()?  This example seems quite contrived, but this happens suprisingly easily when modeling real behavior.

While working on problem 2 for the C++ Practicum I inadvertently created such a situation. I was writing a parser to recognize a simple grammar.  I needed to recognize simple verb phrases such as: look north, and walk east.  At the top level I defined an Expression Interface to generalize all sub expressions. Underneath I defined a Direction object, and a verb
