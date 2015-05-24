---
author: admin
comments: true
date: 2013-11-24 22:14:50+00:00
layout: post
slug: sean-parent-no-raw-loops
title: 'Sean Parent: No Raw Loops'
wordpress_id: 1230
categories:
- Productivity
tags:
- C++
- C++11
- Stepanov
- STL
---

A group of colleagues and I watched Sean Parent's Going Native Talk on "[C++ Seasoning](http://channel9.msdn.com/Events/GoingNative/2013/Cpp-Seasoning)". Parent takes some extreme views on how to use C++, but his examples for using the STL to simplify code are phenomenal. For a recent AI project I decided to apply Parent's _goal_ of "no raw loops", I was blown away by the transformation... err std::transformation this had on my code. In this post I indented to demonstrate several complex code blocks, or overly specific code blocks what were replaced by some STL magic. Alexander Stepanov says, "[...code is a liability.](http://www.youtube.com/watch?v=COuHLky7E2Q)" The more code a program has the more likely it contains bugs. The fewer lines of code, the lesser the opportunity for a bug. I haven't quiet decided if I agree with this point, but it does induce thought either way. Sean Parent's methodology seems to agree, for the purposes of this post we'll agree as well.

<!-- more -->

So the assignment statement:


<blockquote>Suppose that you have purchased a bag of candy which has two flavor: cherry (c) and lime (l). We do not know exactly what kind of bag we bought, but we know that it is one of the following types:

> 
> 
	
>   1. 100% cherry (10% likely)
> 
	
>   2. 75% cherry (20% likely)
> 
	
>   3. 50% cherry (40% likely)
> 
	
>   4. 25% cherry (20% likely)
> 
	
>   5. 0% cherry (10% likely)
> 

You take 11 pieces of candy, all happen to be lime. What bag do you most likely have, and what is the probability the next candy will be a lime?</blockquote>


So lets start with encoding our data.  First we have 2 types of candy: cherry and lime.  Lets represent that:

    
    class lime_type{};
    class cherry_type{};


We might expand this later, but for now we just need a way to overload functions on lime candies or cherry candies. This will work just fine.

Next we have some bags, and associated probabilities

    
    enum Bag {
    Bag1 =1,
    Bag2,
    Bag3,
    Bag4,
    Bag5};
    
    std::vector<Bag> const bags{Bag1, Bag2, Bag3, Bag4, Bag5};
    
    map<Bag, double> apriori{
    {Bag1, 0.1},
    {Bag2, 0.2},
    {Bag3, 0.4},
    {Bag4, 0.2},
    {Bag5, 0.1}
    };
    
    map<Bag, std::pair<double, double>> candy_dist{
    {Bag1, {1.00, 0.00}},
    {Bag2, {0.75, 0.25}},
    {Bag3, {0.50, 0.50}},
    {Bag4, {0.25, 0.75}},
    {Bag5, {0.00, 1.00}}
    };


Again, pretty straight forward, but the magic is about to happen...

Next we have to consume data from a file. Each data set is represented by a series of l or c on a single line. We need to print a graph for each line.  Our example data file looks like this:

    
    jwright@jwright-LinuxAwesome:~/workspaces/school/cse471/hw15$ cat data1.txt
    l l
    l l l l l l l l l l l l


So for our first STL use case. (Actually Boost here, since gcc 4.7.1 doesn't support regex yet, but this functionality will work in gcc 4.9.1).

The before:

    
    std::ifstream fin(filename);
        string line;
        while(fin >> line)
        {
            if(line == "l")
                cout << "Lime" << endl;
            if(line == "c")
                cout << "cherry" << endl;
        }


What's wrong with this code block? Consider if our ls and cs aren't white space delimited. Sensor data is noisy/messy all the time. It would be prudent to deal with this case. This code doesn't block on newlines, and streams all the newlines together. We could wrap this code block with a std::getline() loop, but that's going the wrong direction. No raw loops... What does the STL provide to deal with this? Essentially we want to tokenize each line with _c_s or _l_s as tokens.

    
    boost::regex reg("c|l"); //Construct the regular expression here, since it's expensive
    while(std::getline(fin,line))
    { 
        boost::sregex_token_iterator pos(begin(line), end(line), reg);
        boost::sregex_token_iterator end;
        std::for_each(pos, end, [](boost::sregex_token_iterator tok)
        {
            process(tok->str());
        });
    }


This code isn't directly shorter, but it is certainly more robust. We can deal with extra noise in our data file, and the regex will skip over it gracefully calling our process function once for each l and c it finds on each line.

Now that we're warmed up, lets check out some better examples. Conditional probabilities have lots of summations, and product chains in them. My initial hack unrolled all these summations. This is both verbose, which can hide errors, but if we can reduce the number of lines we will increase our reliability. First up.

$$ P( Candy = Lime | Data) = \Sigma_{Bags}(P(lime, Bag_i | Data) $$

My first hack, looks like something that congealed in a gutter:

    
    double p(cherry_type, data_type)
    {
    //
    // \sigma_bags(p(lime, Bag_i | data))
    //
    double a =
    p(lime_type(), Bag1)*p(Bag1, data_type()) +
    p(lime_type(), Bag2)*p(Bag2, data_type()) +
    p(lime_type(), Bag3)*p(Bag3, data_type()) +
    p(lime_type(), Bag3)*p(Bag4, data_type()) +
    p(lime_type(), Bag5)*p(Bag5, data_type());
    
    return a;
    }


This version is has the sad property that a C programmer might say, "Awesome, he unrolled the loops. That code will be fast." Stephan T. Lavavej says , "[Don't help the compiler](http://channel9.msdn.com/Events/GoingNative/2013/Don-t-Help-the-Compiler)". I agree. -funroll-loops will unroll the loops much better than I can.In fact this code as a bug in it. See it?

    
    double p(cherry_type, data_type)
    {
    //
    // \sigma_bags(p(lime, Bag_i | data))
    //
    double a =
    p(lime_type(), Bag1)*p(Bag1, data_type()) +
    p(lime_type(), Bag2)*p(Bag2, data_type()) +
    p(lime_type(), Bag3)*p(Bag3, data_type()) +
    p(lime_type(), Bag3)*p(Bag4, data_type()) + //Boom, check out that hot copy-paste error.
    p(lime_type(), Bag5)*p(Bag5, data_type());
    
    return a;
    }


Corrected, but still not "correct"

    
    double p(lime_type, data_type)
    {
    //
    // \sigma_bags(p(lime, Bag_i | data))
    //
    double a =
    p(lime_type(), Bag1)*p(Bag1, data_type()) +
    p(lime_type(), Bag2)*p(Bag2, data_type()) +
    p(lime_type(), Bag3)*p(Bag3, data_type()) +
    p(lime_type(), Bag4)*p(Bag4, data_type()) + //Boom, check out that hot copy-paste error.
    p(lime_type(), Bag5)*p(Bag5, data_type());
    
    return a;
    }


Beside being verbose, and prone to error. It isn't generate. If we grow our dataset, the loop is not wrong. Can we be sure that we'll find every unrolled loop, and fix it? We can do better.

    
    double p(lime_type, data_type)
    {
        //
        // \sigma_bags(p(lime, Bag_i | data))
        //   
        std::vector<double> partials(bags.size());
        std::transform(begin(bags), end(bags), begin(partials), [](Bag b){ return p(lime_type(), b)*p(b, data_type()); });
        double a = std::accumulate(begin(partials), end(partials), 0.0 ); //Gotcha 0.0 instead of 0. 0 will cast the result to an int
        return a;
    }


This version is shorter. The compiler is free to optimize the STL algorithms as needed even unrolling the loops if the compiler deems it will improve the code. This code is readable, but futhermore we can explain this code to a mathematician. Stroustroup says, "Express abstracts as the expert in the field does." This function does exactly that. The first step is to compute partial products of $$ P( Lime, Bag_i) * P(Bag_i | Data) $$. Then add the products together. We are agnostic to the number of bags.

Next what about debugging. I'm searching for a bug, and sometimes print statements are the best way to work it out. Lets print out a vector.

    
    vector prob;
    //...
    cout << "{";
    for(auto& p : prob)
        cout << p << ", ";
    cout << "}";


This cannot be bad right? We used the new, shiny range-based for. What can one complain about.

    
    vector prob;
    //...
    cout << "{";
    std::copy(std::begin(prob), std::end(prob), std::ostream_iterator<double>(cout, ", "));
    cout << "}";


However we can do [even better](https://github.com/louisdx/cxx-prettyprint):

    
    #include 
    cout << prob;



Even though this program was small, the opportunity to improve quality, and robustness, is ever present. C++ is a growing language, and it's new capabilities are really improving the corner cases in software. One key tool in doing so is learning the STL.  I encourage you to study the STL.
