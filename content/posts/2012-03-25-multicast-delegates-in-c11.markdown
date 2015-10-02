---
author: Jeremy
comments: true
date: 2012-03-25 05:32:43+00:00
layout: post
slug: multicast-delegates-in-c11
title: Multicast Delegates in C++11
wordpress_id: 573
tags:
- C++
- C++11
---

C# has a wonderfully flexible delegate system capable of multicast events.  This simple tool makes event driven software easier to write, and reduces coupling between objects. In 2003 Herb Sutter implemented a general form of the Observer pattern [1].  He called this the multi_function. It uses a mixture of TR1 and boost components to build a multi-cast delegate similar to C#'s.  Fast-forward 9 years, and we now have variadic-templates thanks to C++11.  Variadic-Templates allow us to patch a missing component in Sutter's multi_function. 
<!-- more -->

Variadic Templates sound like a overwhelming cacophony. Templates are complex enough already, why do we need to add more complexity to the issue? However, Variadic Templates don't have to be as difficult as they could be.  Variadic Templates have the potential to destroy readability. They are extremely abstract tools. At a recent conference, Andrei Alexandrescu, not wanting to disappoint, defined the variadic-variadic-template-template [3]. Templates can be abused, and the varadic is no exception. However, when used judiciously varadic templates are just a tool that can solve some very real-world issues.

We are going to use the type expansion effects of variadic templates to consolidate some code. Sutter uses a template to implement to operator() of his multi_function. When one calls this operator, multi_function in-turn calls the operator() of each stored function. Hence, the multi-cast behavior.

    
    void operator()() const {
        for( std::list<tr1::function<F> >::const_iterator i = l_.begin(); i != l_.end(); ++i )
          (*i)();
      }
    
      template<typename T1>
      void operator()( T1 t1 ) const {
        for( std::list<tr1::function<F> >::const_iterator i = l_.begin(); i != l_.end(); ++i )
          (*i)( t1 );
      }
    
      template<typename T1, typename T2>
      void operator()( T1 t1, T2 t2 ) const {
        for( std::list<tr1::function<F> >::const_iterator i = l_.begin(); i != l_.end(); ++i )
          (*i)( t1, t2 );
      }
    
      template<typename T1, typename T2, typename T3>
      void operator()( T1 t1, T2 t2, T3 t3 ) const {
        for( std::list<tr1::function<F> >::const_iterator i = l_.begin(); i != l_.end(); ++i )
          (*i)( t1, t2, t3 );
      }
    
      // etc.


The _etc _is the point.  This implementation is quite limiting, one has to implement the operator() for every possible number of operands in the target function. Google Mock also has a similar issue [4]. Google fixes it by using a code generator that implements the method up to a large number of parameters. C++11 fixes this.

Templates are designed to generate code at compile time to leverage source code reuse. Alexandrescu says that templates are source-code reuse, while inheritance is binary reuse. Since source code is more general than binary, templates are more general than inheritance.  Variadic templates allow the compiler to accept a variable number of arguments then at compile time, special syntax is used to expand the expressions.  Here is the above code consolidated into a variadic.

    
    template<typename... Ts> //Expand all the Types into a comma separated list
    void operator()(Ts... vs) const {
    
        for(auto i = begin(l_); i != end(l_); ++i) //Iterator over the callbacks
        {
            (*i)(vs...); //Expand all the values into a comma separated list
        }
    }


Simpler, right? Sadly, gcc currently has a bug which prevents variadics and lambdas from playing nicely together [2].  The power of this expression is the new ... syntax.  I follow Alexandrescu's cue to pluralize the template arguments, Ts and vs respectively. Ts are Types, and vs are Values.  The compiler will accept any number arguments, and type-safely expand the argument list. This vastly expands to generality of this class, without drastically increasing the complexity. This is certainly simpler than using separate code-generation phase to expand the type lists prior to compilation.

Variadic Templates are a powerful tool; there is certainly the potential to create some very obsucated code with this tool. However with judicious use, very useful and extensive interfaces are possible.

Thank you to the stackoverflow community for guidance on this, and a massive thank you to Herb Sutter for implementing the original multi_function.



* * *






	
  1. [http://drdobbs.com/cpp/184403873?pgno=3](http://drdobbs.com/cpp/184403873?pgno=3)

	
  2. [http://stackoverflow.com/questions/9856859/variadic-template-lambda-expansion](http://stackoverflow.com/questions/9856859/variadic-template-lambda-expansion)


	
    1. [http://gcc.gnu.org/bugzilla/show_bug.cgi?id=41933](http://gcc.gnu.org/bugzilla/show_bug.cgi?id=41933)


	
  3. [http://channel9.msdn.com/Events/GoingNative/GoingNative-2012/Variadic-Templates-are-Funadic](http://channel9.msdn.com/Events/GoingNative/GoingNative-2012/Variadic-Templates-are-Funadic)

	
  4. [http://code.google.com/p/googlemock](http://code.google.com/p/googlemock)


