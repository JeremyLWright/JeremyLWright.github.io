---
author: Jeremy
date: 2015-07-05 00:00:00+00:00
slug: property_driven_design_minmax
title: "Property Driven Design: MinMax"
draft: false
categories:
- C++
- "Property Driven Design"
tags:
- property-testing
- example
- tutorial
series: "Property Driven Design"
---

I wrote an article on Property Driven Design about a year ago
(http://www.codestrokes.com/2014/09/property-testing-in-c/). Isocpp.org even
linked to it at one time (https://isocpp.org/blog/2014/12/property-testing)
which was pretty cool. Recently, I uncovered a fantastic talk by Jessica Kerr
about property testing (https://www.youtube.com/watch?v=shngiiBfD80). Kerr's
talk reinvigorated my passion in generated testing. Kerr presented the idea
(novel to me) that properties don't have to verify that an answer is correct.
Properties simply must reduce the size of the incorrect space. This may seem like
semantics, but sometimes it's much easier to verify something is not
a wild-ass-guess that if it is correct. 
![sometimes_code_gives_you_a_wtf](/img/properties_solution_space.png)
Following Kerr's
references, I found a set of projects for a predicate-logic class
(http://www.cs.ou.edu/~rlpage/SEcollab/20projects/). The class provides 20
projects. Each project breaks down the requirements and predicates the
functions should provide. This step-by-step example clarified many points
I misunderstood about property testing. This post will step through the design
of the first project minmax (http://www.cs.ou.edu/~rlpage/SEcollab/20projects/minmax.htm) using C++. My primary goal for this article is to address a concern raised by a colleague, "Does pulling in more complexity in terms of a fancy test generator actually increase quality?" I believe it does when exercised properly.  All the code is available at [github](https://github.com/JeremyLWright/property_driven_design/tree/master/01_minmax), if you would like to follow along. 

<!--more-->

In her presentation, Kerr stated, "..what is this answer? I don't know but
I can put a box around it!" While this statement was made in jest it is quite
inspired. Example tests &mdash; the test typically used in unit tests (the FPGA/ASIC
guys call these Directed Tests) &mdash; draw individual points within the
correct region of the solution space. There are excellent structures for
drawing points in intelligent places, such as structured testing using McCabe
complexity, but in the end you are still drawing points. Properties on the
other hand draw boxes around the solution space. Notice that the properties do
not exclude all incorrect solutions. While this may seem as a defect to
property driven design, it is a simplification that makes properties resilient
to refactoring and maintenance cycles. Structured testing, for example, is
a whitebox method that looks as what test data will induce 100% block
coverage. As the code grows and changes over time, the predicates and
conditionals that influence the code coverage change. In a sense the points in
the correct solution place are always moving around. Properties however
operate at a higher level of abstraction. Properties allow one to say
"solutions of _approximately this form_ are likely correct." Properties then
can be made closer and closer to describe the overall shape of the correct
solution space. Its a powerful technique that I am increasingly enjoying in my
design work. 

# Implementing MinMax with Properties

Before we get started the term measure used in this problem statement means as
the ancient Greeks meant it, a segment which describes an integer number of
divisions of another number. Today we might use the word common-multiple.

Inspired by test-driven-design we'll start with defining a property for our
maximum function.

1. Define a function, _maximum_, that delivers the largest value in a non-empty list of rational numbers.

Using the autocheck library we can express this requirement as follows:

```cpp
struct prop_max_element_t
{
	template<
		typename SinglePassRange>
	bool operator()(const SinglePassRange& xs)
	{
		auto ref_max = std::max_element(std::cbegin(xs), std::cend(xs));
		const auto test_max = minmax::maximum(xs);
		return *ref_max == test_max;
	}
	
};

TEST(minmax, maximum_prop)
{
	autocheck::gtest_reporter rep;

	auto arbitrary = 
		autocheck::discard_if([](const std::vector<size_t>& xs) -> bool { return xs.size() == 0; },
		autocheck::make_arbitrary<std::vector<size_t>>());
		
	autocheck::check<std::vector<size_t>>(
			prop_max_element_t(),
			100,
			arbitrary,
			rep);
}
```

Lets start with the definition of the arbitrary generator:

```cpp
	auto arbitrary = 
		autocheck::discard_if([](const std::vector<size_t>& xs) -> bool { return xs.size() == 0; },
		autocheck::make_arbitrary<std::vector<size_t>>());
```

The signature of an arbitrary generator is best read bottom to top.  The first
step generates a random vector of random length. The line above it throws away
vectors who's size is equal to zero. We will see later how to generate data
that meets our requirements, but sometimes its easier to just throw away some
data rather than try to generate only valid data.

With this property we can test our stub function:

```cpp
namespace minmax
{

template <typename SinglePassRange>
typename SinglePassRange::value_type maximum(const SinglePassRange& range)
{
	return 0; 
}
}
```
This generates a failed output as we expected

```bash
[ RUN      ] minmax.maximum_prop
d:\property_driven_design\build\thirdparty\src\autocheck\include\autocheck\reporter.hpp(91): error: Value of: AUTOCHECK_SUCCESS
  Actual: false
Expected: true
Falsifiable, after 3 tests:
([2, 0])

[  FAILED  ] minmax.maximum_prop (3 ms)
```

From this we can implement our method 

```cpp
namespace minmax
{

template <typename SinglePassRange>
typename SinglePassRange::value_type maximum(const SinglePassRange& range)
{
	//First Implementation
	//return 0; 
	return *std::max_element(
			std::begin(range),
			std::end(range));
}

}
```

and rerun our property

```bash
[ RUN      ] minmax.maximum_prop
OK, passed 100 tests.
[       OK ] minmax.maximum_prop (14 ms)
```

This demonstrates another useful property of properties :-). The data passing
through our property test is randomly generated. Each time the test runs we
get different tests. Typing _make test_ multiple times is actually a useful
thing, not just something you do to procrastinate at 4:45pm when you've found
a new bug. 

Also there is something viscerally satisfying about writing a single property
and seeing 100 tests passing. 

Next we can verify the property given to us in the [problem statement](http://www.cs.ou.edu/~rlpage/SEcollab/20projects/minmax.htm)

1. If xs is a non-empty true-list of rational numbers, then (maximum xs) is a rational number.

Since C++ is a statically typed language this property may appear to be self
evident. However this demonstrates another benefit of property driven design.
We can document that we intend to only work with rational numbers. Then since
C++ is statically type we can validate the property statically, and any
maintenance programmer will fail to compile without modifying the test.

We can express this property as so

```cpp
struct prop_maximum_should_give_rational_number_t
{
	template<typename SinglePassRange>
	bool operator()(const SinglePassRange& xs)
	{
		static_assert(std::is_integral<decltype(minmax::maximum(xs))>::value, "Maximum only works on rational numbers.");
		return std::is_integral<decltype(minmax::maximum(xs))>::value;
	}
};
```

This shows another pattern of testing I picked up from [Bruce Tate](https://www.youtube.com/watch?v=sDMngNP7pOw), tests should be named as a should-statement. This property here says: My property for maximum _should_ give rational numbers. If this is ever falsified our test the static\_assert() will fail compilation. 

We can add another property that demonstrates the blackbox nature of property
testing. 

&#50;. The value (maximum xs) occurs in the list xs

Properties as basic as this seem silly at first, but they serve a very useful
purpose. Recall the poorly drawn graphic from above. We are searching for bugs
in our program by defining bounds around the solution space. This property
states something very profound about our function. The output of our function
is dependent on the input. This trends the function toward referential
transparency. At a more basic level though, this might be a property one
starts with. Notice that if we implemented this property first, with our stub
function in place, our random generator would have falsified it easily with
any list where 0 was not a member. 

We can express this property with autocheck as:

```cpp
struct prop_maximum_should_return_a_value_from_the_list_t
{
	template <typename SinglePassRange>
	bool operator()(const SinglePassRange& xs)
	{
		const auto m = minmax::maximum(xs);
		const auto is_present = std::find(
				std::begin(xs),
				std::end(xs),
				m);
		return is_present != std::end(xs);
	}
};
```

Simply put, if minmax::maximum returns some value m, that value must be
present in the list.  Notice again that m may be the minimum value in the
list. This property isn't checking for the complete correctness of the
function. It is testing one small aspect of the function's possible solution
space. 

Next we can move on to our next function, _minimum\_pair_, which we can
implement with a stub to always return the first element:

```cpp
template <typename SinglePassRange>
measure_pair_t minimum_pair(const SinglePassRange& xs)
{
	return *std::begin(xs);
}
```
To property test this function we'll need to teach autocheck how to generate
a _measure\_pair\_t_. We do this by specializing the generator function in the
autocheck namespace.

```cpp
namespace autocheck
{

//Tell autocheck how to generate a measure_pair_t
template <>
class generator<minmax::measure_pair_t>
{
	public:
	using result_type = minmax::measure_pair_t;

	result_type operator()()
	{
		return this->operator()(0);
	}

	result_type operator()(size_t size)
	{
		auto rational_gen = generator<std::size_t>();
		return std::make_pair(rational_gen(size), rational_gen(size));
	}
};

//Tell autocheck how to display a measure_pair_t
std::ostream& operator<<(std::ostream& os, const minmax::measure_pair_t& p)
{
	os << "{" << p.first << ", " << p.second << "}";
	return os;
}
}
```

Now autocheck can generate and display our specific type. Setup a property to
check. 

&#52;. If xs is a non-empty true-list of measure pairs, then (minimum-pair xs) is a measure-pair.

To express this property we must first have a definition of a measure pair
(We'll see how this definition is not quite correct, but our properties will
sus that out quite quickly):

```cpp
using measure_pair_t = std::pair<std::size_t, std::size_t>;

///Provided definition: measure pair: a two-element list whose first element, a rational number, is the measure of its other element
bool is_measure_pair(const measure_pair_t& x)
{
	//A measure pair is a two element list, who's first element (a rational
	//number), is the measure of its other element
	const auto first_element_is_rational = std::is_integral<decltype(x.first)>::value;

	const auto other_element_is_measure_of_first = 
		//To be a measure the first value must be less-than the second.
		(x.first < x.second)
		//And the second element must evenly divide the first element.
		&& (x.second % x.first == 0);
	return first_element_is_rational
		&& other_element_is_measure_of_first;
}
```

And our property to check that the return value from minimum pair should meet
the definition of a measure pair.

```cpp
struct prop_minimum_pair_should_return_a_measure_pair_t
{
	bool operator()(const std::vector<minmax::measure_pair_t>& xs) const
	{
		using namespace minmax;
		const auto test_pair = minimum_pair(xs);
		return is_measure_pair(test_pair);
	}
};
```

Executing this gives us, as expected due to our stub, a falsifiable case. 

```bash
[ RUN      ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair
unknown file: error: SEH exception with code 0xc0000094 thrown in the test body.

[  FAILED  ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair (1 ms)
```

Error 0xc0000094 is a divide by zero. Ah! Good catch autocheck. I know
I personally would not have exercised this using a directed test. This is
another strength of random testing. The random generators are not biased with
programmer intuition. Our requirements state that a measure-pair is always
non-zero so we will update the generator to exclude zero values.

```cpp
namespace autocheck
{
template <>
class generator<minmax::measure_pair_t>
{
	public:
	using result_type = minmax::measure_pair_t;

	result_type operator()()
	{
		return this->operator()(0);
	}

	result_type operator()(const size_t size)
	{
		const auto non_zero_gen = [size]()
		{
			auto rational_gen = generator<std::size_t>();
			auto temp = rational_gen(size);
			if(temp == 0) //Skip over zero!
				return temp + 1;
			return temp;
		};
		const auto measure = non_zero_gen();
		const auto factor = non_zero_gen();
		return std::make_pair(measure*factor, measure);
	}
};
}
```
Now with zero values excluded we'll get a falsifiable test case:

```bash
[ RUN      ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair
d:\property_driven_design\build\thirdparty\src\autocheck\include\autocheck\reporter.hpp(91): error: Value of: AUTOCHECK_SUCCESS
  Actual: false
Expected: true
Falsifiable, after 1 tests:
([{1, 1}])

[  FAILED  ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair (1 ms)
```

This test case demonstrates that our understand of the word measure wasn't
quite right when we implemented the _is\_measure\_pair_ predicate. A value can
always be a measure of itself, i.e., a number always measures itself one time.
Notice that we still have a stub for our function. One school of thought is
that we are wasting time writing, and rewriting, test code before we've even
worked on the code we're getting paid to write. But this failing test case is
evidence for a different perspective. The test code is working out our concept
of what the code needs to do. We the author would have written the function
incorrection the first time, considering we didn't implement the definition
correctly, e.g., we could translate a definition into C++ correctly, we
probably wouldn't have written some that that manipulates that definition
correctly. Nor, in our limited understanding of the problem, defined any

useful test data for our directed tests. John Hughes [put it
best](https://www.youtube.com/watch?v=FnjutUoNSmg) when he state that property
testing is about comparing the specification to the code. The properties
encode the specification. The code does what it does. When the checker finds
a discrepancy it is the engineer's job to find where the defect lies. This is
very powerful. We, the engineer, aren't relegated to imagining test data for
our functions what will make it blow up. We simply describe concepts
(properties) of what we believe the specification is telling us to do. Then we
implement the code. If the two match then we the code probably matches the
specification. Its raises our level of thinking out of individual numbers, and
code paths to more abstract thinking, which is something humans do best. (I
liken this raising of thought similar to using ranges intead of indexes).

The problem is is that our definition doesn't include self-measures. We can
adjust it easily.

```cpp
bool is_measure_pair(const measure_pair_t& x)
{
	//A measure pair is a two element list, who's first element (a rational
	//number), is the measure of its other element
	const auto first_element_is_rational = std::is_integral<decltype(x.first)>::value;

	const auto other_element_is_measure_of_first = 
		//To be a measure the first value must be equal-to or less-than the second.
		(x.first == x.second) ||
		((x.first < x.second )
		//And the second element must evenly divide the first element.
		&& (x.second % x.first == 0));
	return first_element_is_rational
		&& other_element_is_measure_of_first;
}
```

Executing this generates a new failing case:

```bash
[ RUN      ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair
d:\property_driven_design\build\thirdparty\src\autocheck\include\autocheck\repor
ter.hpp(91): error: Value of: AUTOCHECK_SUCCESS
  Actual: false
Expected: true
Falsifiable, after 3 tests:
([{2, 1}, {2, 2}])

[  FAILED  ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair (1 ms)
```

We can run it again to see if we get a different case:

```bash
[ RUN      ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair
d:\property_driven_design\build\thirdparty\src\autocheck\include\autocheck\reporter.hpp(91): error: Value of: AUTOCHECK_SUCCESS
  Actual: false
Expected: true
Falsifiable, after 7 tests:
([{4, 1}, {4, 2}, {2, 2}, {1, 1}])

[  FAILED  ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair (1 ms)
```

This is awesome! Our failing test case is bigger now. Again to quote John
Hughes, "[This is progress! We are now passing for lists of size 1!](https://www.youtube.com/watch?v=zi0rHwfiX1Q)" Our function is still implemented as a stub, so we can have some confidence that our test code is behaving properly. Let's implement our minimum_pair function:

```cpp
template <typename SinglePassRange>
measure_pair_t minimum_pair(const SinglePassRange& xs)
{
	return *std::min_element(
			std::begin(xs),
			std::end(xs),
			::minmax::operator<);
}
```

Executing our test code:

```bash
D:\property_driven_design\build>01_minmax
Running main() from gtest_main.cc
[==========] Running 7 tests from 3 test cases.
[----------] Global test environment set-up.
[----------] 1 test from minmax
[ RUN      ] minmax.maximum_directed
[       OK ] minmax.maximum_directed (0 ms)
[----------] 1 test from minmax (1 ms total)

[----------] 5 tests from MinMaxFixture
[ RUN      ] MinMaxFixture.prop_maximum_should_give_greatest_value
OK, passed 100 tests.
[       OK ] MinMaxFixture.prop_maximum_should_give_greatest_value (13 ms)
[ RUN      ] MinMaxFixture.prop_maximum_should_give_rational_number
OK, passed 100 tests.
[       OK ] MinMaxFixture.prop_maximum_should_give_rational_number (11 ms)
[ RUN      ] MinMaxFixture.prop_maximum_should_return_a_value_from_the_list
OK, passed 100 tests (2% trivial).
10% 10, odd-length.
10% 20, even-length.
10% 30, odd-length.
10% 40, even-length.
10% 50, odd-length.
10% 60, even-length.
10% 70, odd-length.
10% 80, even-length.
10% 90, odd-length.
9% 0, even-length.
[       OK ] MinMaxFixture.prop_maximum_should_return_a_value_from_the_list (24 ms)
[ RUN      ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair
OK, passed 100 tests.
[       OK ] MinMaxFixture.prop_minimum_pair_should_return_a_measure_pair (20 ms)
[ RUN      ] MinMaxFixture.prop_minimum_pair_should_return_the_smallest_pair
OK, passed 100 tests.
[       OK ] MinMaxFixture.prop_minimum_pair_should_return_the_smallest_pair (23 ms)
[----------] 5 tests from MinMaxFixture (92 ms total)

[----------] 1 test from MinMaxDirected
[ RUN      ] MinMaxDirected.directed_minimum_pair_shouls_return_a_measure_pair
[       OK ] MinMaxDirected.directed_minimum_pair_shouls_return_a_measure_pair (0 ms)
[----------] 1 test from MinMaxDirected (0 ms total)

[----------] Global test environment tear-down
[==========] 7 tests from 3 test cases ran. (96 ms total)
[  PASSED  ] 7 tests.
```

Running this multiple times generates no failing test cases. 

# Conclusion

So a few real-world metrics. I wrote this code and properties in 3 hours. The
requirements were relatively simple, but I suspect that using example tests
would have resulted in a similar completion time. Additionally, I suspect, my
directed tests would have found more defects near the end of my development
rather than the beginning. I felt this affect as an acceleration. I found feel
as I closed each property that I had fewer defects in the code I previously
thought was done. This is a big confidence booster in my opinion.
Additionally, another pattern I learned from John Hughes, that I didn't
explicitly describe here but you can see in the code, save failed tests.
A failing test is gold! When the random generator uncovers something
interesting save it as a directed test. Then fix the failure and leave the
directed test behind. It will be a reminder of a corner case you missed. Plus
some developers like to see examples tests, even random ones.

In this post I walked through a property-driven-design approach to a simple
numerical problem. In intended to show something more interesting that the
_reverse(reverse(list)) == list_ example, and something less contrived than my
previous post on property testing. I look forward to any feedback on this
post.
