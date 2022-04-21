---
layout: post
author: admin
comments: true
date: 2014-08-28 05:58:26+00:00
layout: post
slug: what-is-a-unit-test
title: What is a Unit Test?
wordpress_id: 1312
tags:
- Testing
---

I'm taking a Software Testing and Verification course as part of my Master's work. Our first assignment was to write a short paper describing a unit test, then implement selection sort and test it under that philosophy. Sarcastically, I commented to my colleagues the triviality of this question. The first response was, "Wow, I don't think that is such an easy question." A technical discussion ensued. This is that log.
<!--more-->


<blockquote>Definition 1:
Given a function in the mathematical sense, i.e. no side-effect, a unit test treats the function as a black box and passes it input and expects a given output. Conversely, an integration test tests entites which are not pure functions using a mock to control state.</blockquote>




<blockquote>Definition 2:
A unit test de-tangles dependencies so one can test a submodules prior to merging ([complecting](http://www.infoq.com/presentations/Simple-Made-Easy)) it's functionality with another module.</blockquote>




<blockquote>[Wikipedia](http://en.wikipedia.org/wiki/Unit_testing):
In computer programming, unit testing is a software testing method by which individual units of source code, sets of one or more computer program modules together with associated control data, usage procedures, and operating procedures are tested to determine if they are fit for use</blockquote>



I proposed the first definition above, which is mostly influence from my Haskell QuickCheck experience.  During lecture today the professor presented levels of testing.

Unit Testing
Integration Testing
System Testing
Alpha Testing
Beta Testing

The theme here? Each successive layer of testing include more modules and more functionality. Unit testing is the most basic. It doesn't  have to provide a pure interface, it can be dirty, it can have side effects, but before I promote some software module to the next stage, I want some confidence its working. The professor went on to ask, "What if we had a test team, a separately paid person to write the unit tests? Would that work? Would that be a good idea?" 

My initial response was, "No! those tests are mine!" This is my definition of a unit test, private tests. 

Definition I hold now:
A unit test is a test to provide the developer some confidence a region of code works as intended before other people see the code and the developer is open to mockery and scandal. 

This definition supposed unit tests are more emotional, or egocentric than technical, but when I think about how, and where I choose to unit test heavily, and where I choose to test more lightly it centers around areas of code I would be embarrassed to get wrong. To get back to the homework assignment, the first goal was to implement selection sort: 

Unit under test

    
    #include <iterator>
    #include <iostream>
    #include <algorithm>
    
    template <typename InputIterator>
    void selection_sort(InputIterator b, InputIterator e)
    {
        for(InputIterator c = b; c != e ; ++c){
            auto m = std::min_element(c, e);
            std::swap(*m, *c);
        }
    }
    



Selection sort is pretty naive (O(n^2)) but its straight-forward to implement, and std::algorithms make it even easier to understand. As a side note, this is the real strength of the STL algorithms: clarity. This code has very few opportunities for bugs because of the reliance on STL algorithms. Additionally, it's readable! Additionally, it's templated so everyone will think you are a badass (unless there is a bug in it, in which case they judge you every time you whip out the _typename_). To prevent this horrific alternate future we can unit test.  Furthermore, we can take a page from the FPGA/ASIC guys and use randomized tests. (As opposed to direct tests).

Randomized tests construct random input and feed it through the unit under test.  A secondary implementation of the function verifies the result. In this case we are luck that the invariant of a "sorted list" is easy to check.  In fact there is a standard algorithm for it: std::is_sorted().  

Using GTest we construct a parameterized test. We then construct a list of random vectors and instantiate the test with the 10000 separate vectors. GTest provides a lot of value here.  If a single test fails, GTest will print out the parameter value when that particular test failed the build. Since we are using random data, this is critical so we can setup regression tests.


    
    #include "sort.hpp"
    #include "gtest/gtest.h"
    #include <vector>
    #include <random>
    #include <limits>
    #include <cassert>
    #include <iostream>
    
    using TestInput = std::vector<int>;
    
    class RandomizedTest : public testing::TestWithParam<TestInput> {};
    TEST_P(RandomizedTest, Sorting)
    {
       auto vs = GetParam();
       selection_sort(std::begin(vs), std::end(vs));
       ASSERT_TRUE(std::is_sorted(std::begin(vs), std::end(vs)));
    }
    
    std::vector<std::vector<int>> GenerateTestCases()
    {
     std::vector<TestInput> test_cases;
     std::numeric_limits<int> limits;
    
     std::mt19937 engine(time(0)); // Fixed seed of 0
     std::uniform_int_distribution<int> range_dist(0,1500);
     std::uniform_int_distribution<int> element_dist(0, limits.max());
    
     size_t n = 10000;
     auto f = [&](){return element_dist(engine);};
     std::generate_n(std::back_inserter(test_cases), n, 
         [&](){ 
             TestInput vs;
             std::generate_n(std::back_inserter(vs), range_dist(engine), f);
             return vs;
         });
     return test_cases;
    }
    
    INSTANTIATE_TEST_CASE_P(
     GeneralAndSpecial,
     RandomizedTest,
     testing::ValuesIn(GenerateTestCases()));



Build Script

    
    
    project(hw1)
    
    include(ExternalProject)
    ExternalProject_Add(
        GTest 
        URL http://googletest.googlecode.com/files/gtest-1.7.0.zip
        INSTALL_COMMAND ""
        )
    
    ExternalProject_Get_Property(GTest source_dir)
    include_directories(${source_dir}/include)
    
    
    ExternalProject_Get_Property(GTest binary_dir)
    link_directories(${binary_dir})
    
    
    set(CMAKE_CXX_FLAGS "-O3 -std=gnu++11")
    add_executable(hw1 main.cpp)
    add_executable(test test.cpp)
    add_dependencies(test GTest)
    target_link_libraries(test gtest gtest_main pthread rt)
    



These tests take nearly 5 seconds to run, but randomization gives us another cool feature. Typically with directed tests, once the tests pass the probability of that test failing int he future is pretty low. Randomized tests are different every time you run them. While the invariant of the input are constant the input itself changes greatly, and exercises code in ways a human may not imagine. 

tldr; 
- Unit tests help you save face.
- Random tests kick directed tests' teeth in. 
