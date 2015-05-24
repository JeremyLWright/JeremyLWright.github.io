+++
date = "2014-09-03T23:00:00-07:00"
draft = false
title = "Property Testing in C++"
slug = "property-testing-in-c"
tags = ["c++", "unit test"]

+++
<p>Currently, I'm on a testing kick. One might say tests are shiny. I don't know if they are really shiny as much as I found another cool use for uniform_int_distribution&lt;&gt;. A use which, as a side effect, might make me appear to be a better software developer. (This assumes a negative bug rate is proportional to better software). I've started playing with Property Testing. Property Testing is a form of unit testing where the programmers defines properties, or invariants about the code. A <del>framework</del> library (ok, seriously its a framework because it calls your code) generates random constrained inputs and calls your test functions. It's pretty cool, and while I was playing around with the framework, I found a real bug, related to my ignorance of C++'s auto type deduction.</p><!--more--><p>Let's steal a simple example from my CSE 565 Software Verification class: a payroll function. Here is the specification:</p> <blockquote> <p>Design a function that calculates payroll for an employee.</p> <h3>Inputs</h3> <p>Employee Id number<br>Number of Hours</p> <h3>Outputs</h3> <p>Amount to pay employee as a floating point value.</p> <h3>Constraints</h3> <p>Pay is calculated at $10 for standard time, $15 for overtime over 40 hours.<br>Overtime starts over 40 hours<br>Maximum number of hours is 100.</p></blockquote> <p>For this demonstration, I’m using a C++ port of Haskell’s QuickCheck, CppQuickCheck (<a title="https://github.com/grogers0/CppQuickCheck" href="https://github.com/grogers0/CppQuickCheck">https://github.com/grogers0/CppQuickCheck</a>, my fork and the examples in this post are available here: <a title="https://github.com/jwright85/CppQuickCheck" href="https://github.com/jwright85/CppQuickCheck">https://github.com/jwright85/CppQuickCheck</a>). QuickCheck was designed by John Hughes who has gone on to support a commercial version of the library for verifying (and validating) automotive requirements for Volvo (<a title="http://vimeo.com/68331689" href="http://vimeo.com/68331689">http://vimeo.com/68331689</a>).&nbsp; His presentations have motivated me to try this testing strategy for my own programs. Lets start with a quick implementation for our payroll function. We'll then apply properties against the function until we are satisfied with the implementation. Although property testing can provide more confidence in an implementation Dijkstra's famous quote still stands, "Testing shows the presence, not the absence of bugs."</p><pre lang="cpp" escaped="true">float payroll(std::array&lt;size_t, 5&gt; person_id, size_t hours)
{
    if(hours &gt; 100)
        throw std::out_of_range("Hours cannot be greater than 100");
    auto overtime = hours - 40;
    return hours * 10 + overtime * 15;
}</pre>
<p>This is obviously wrong, but let's suspend that for a moment and think about properties i.e. invariants we can verify.</p>
<p>The first property verifya that we do not write a negative paycheck. The return type of the function is float, which supports negative values even though the output domain of our specification forbids it. Lets write a property over the valid input range of hours that we don’t generate negative pay.</p><pre lang="cpp" escaped="true">struct PropTestPositivePay: cppqc::Property
{
    PropTestPositivePay() : Property(cppqc::choose(0, 100)) {}
    bool check(const int &amp; hours) const
    {
        std::array&lt;size_t, 5&gt; id{1,2,3,4,5};
        return uut::payroll(id, hours) &gt;= 0;
    }

    std::string name() const
    {
        return "Pay should be positive";
    }
    std::string classify(const int &amp;v) const
    {
        std::ostringstream sstr;
        sstr &lt;&lt; "Hours " &lt;&lt; v;
        return sstr.str();
    }
    bool trivial(const int &amp; v) const
    {
        return v &lt; 40;
    }
};</pre>
<p>Now the input range of this function is small (101 values) so we could run an exhaustive test, but for larger input domains the random generators can really shine. </p>
<p>&nbsp;</p><pre lang="bash" escaped="true">jwright@phaseshift-linux:~/art/CppQuickCheck/b$ ./examples/testPayroll
* Checking property "Pay should be positive" ...
* *** Failed! Falsifiable after 32 tests for input:
*   0: 24
*</pre>
<p>Cool it found that an input of 0 will falsify the test. Lets add some more tests.</p>
<p>&nbsp;</p>
<p>Lets add a property that verifies for the input range of overtime that the function doesn’t pay all hours at the $10 rate nor all the hours at the $15 rate. The correct implementation is some mixture of these two.&nbsp; This brings me to a subtle point when I first heard of property-testing when studying Haskell. In my naiveté I thought to myself, "If I have a model that verifies the unit under test, aren't I duplicating the implementation?" Furthermore, if I duplicate the implementation, how can I be sure I'm not making the same bugs twice. One response I found online, “we test our C code in Erlang. It's unlikely to make the same mistake in two separate languages.” I was wrong however, you don't have to duplicate the functionality. You can steer the generator to generate data within a range over which a simple property will be true. Multiple properties together then test the fuller input domain without requiring 1 single verifier to duplicate behavior. This property doesn’t exactly know what the correct payroll is. It isn’t calculating the correct value, it’s just excluding values that it cannot be. </p><pre lang="cpp" escaped="true">struct PropTestOvertimeRateHigher: cppqc::Property
{
    PropTestOvertimeRateHigher() : Property(cppqc::choose(41, 100)) {}
    bool check(const int &amp; hours) const
    {
        std::array&lt;size_t, 5&gt; id{1,2,3,4,5};
        auto pay = uut::payroll(id, hours);
        return pay &gt; hours * 10 &amp;&amp; pay &lt; hours * 15; //You cannot get paid all overtime or all standard pay
    }

    std::string name() const
    {
        return "You cannot get paid all overtime, or all std time";
    }
    std::string classify(const int &amp;v) const
    {
        std::ostringstream sstr;
        sstr &lt;&lt; "Hours " &lt;&lt; v;
        return sstr.str();
    }
    bool trivial(const int &amp; v) const
    {
        return v == 40;
    }
};</pre>
<p>&nbsp;</p>
<p>Following this thought of excluding a range and testing a simpler property, lets test the payroll without considering overtime. In this case the calculation is simple so we can provide a full implementation.</p>
<p>&nbsp;</p><pre lang="cpp" escaped="true">struct PropTestIgnoreOvertime: cppqc::Property
{
    PropTestIgnoreOvertime() : Property(cppqc::choose(0, 40)) {}
    bool check(const int &amp; hours) const
    {
        std::array&lt;size_t, 5&gt; id{1,2,3,4,5};
        auto pay = uut::payroll(id, hours);
        return pay == hours * 10;
    }

    std::string name() const
    {
        return "Not working overtime makes the math easy.";
    }
    std::string classify(const int &amp;v) const
    {
        std::ostringstream sstr;
        sstr &lt;&lt; "Hours " &lt;&lt; v;
        return sstr.str();
    }
    bool trivial(const int &amp; v) const
    {
        return v == 40;
    }
};</pre>
<p>We run the tests a few times and see the failing test cases. These data are random. Running the test multiple times fails differently, but minimization results in the same or similar values each time to help the programmer debug. So let's fix this code and watch the tests pass to avoid the <a href="http://www.codestrokes.com/2014/08/what-is-a-unit-test/">mockery and scandal of code review</a></p><pre lang="cpp" escaped="true">float payroll(std::array&lt;size_t, 5&gt; person_id, size_t hours)
{
    if(hours &gt; 100)
        throw std::out_of_range("Hours cannot be greater than 100");
    auto overtime = hours - 40;
    if(overtime &gt; 0)
        return hours * 10 + overtime * 15;
    else
        return hours * 10;
}</pre><pre lang="bash" escaped="true">* Checking property "Not working overtime makes the math easy." ...
*** Failed! Falsifiable after 1 test and 1 shrink for input:
0: 0</pre>
<p>To be honest, while setting up the tests for this post I fully expected the tests to start passing and this article would end here. Instead I learned some real value on using these properties as a debugging and design tool. Let's add a printf to the code to get a sense what's happening</p><pre lang="bash" escaped="true">* Checking property "Not working overtime makes the math easy." ...
Overtime: 18446744073709551576 &lt;--- Whoa what happened there?
*** Failed! Falsifiable after 1 test and 1 shrink for input:
0: 0</pre>
<p>Overtime seems to be an unsigned value, and passing in 0 causes the value to wrap around. The rule (http://scottmeyers.blogspot.com/2013/07/when-decltype-meets-auto.html) assures that overtime becomes a size_t since hours is size_t. We can force floating conversion by stating that 40 is a floating point number.</p><pre lang="cpp" escaped="true">float payroll(std::array&lt;size_t, 5&gt; person_id, size_t hours)
{
    if(hours &gt; 100)
        throw std::out_of_range("Hours cannot be greater than 100");
    auto overtime = hours - 40.0; //&lt;-- Force implicit floating point cast
    if(overtime &gt; 0)
        return hours * 10 + overtime * 15;
    else
        return hours * 10;
}</pre><pre lang="bash" escaped="true">* Checking property "Pay should be positive" ...
+++ OK, passed 100 tests (40% trivial).
* Checking property "You cannot get paid all overtime, or all std time" ...
*** Failed! Falsifiable after 1 test and 1 shrink for input:
  0: 60
* Checking property "Not working overtime makes the math easy." ...
+++ OK, passed 100 tests.</pre>
<p>Argh! Still wrong? The property must be wrong. Notice that the properties are quite simple. No single test verifies the full range, but the properties provide useful documentation and make it easy to reason about the code. The properties are probably correct then. ...yeah, it wasn't the property…</p><pre lang="cpp" escaped="true">float payroll(std::array<size_t  5 ,> person_id, size_t hours)
{
    if(hours &gt; 100)
        throw std::out_of_range("Hours cannot be greater than 100");
    auto overtime = hours - 40.0;
    if(overtime &gt; 0)
        return (hours - overtime) * 10 + overtime * 15;
    else
        return hours * 10;
}</pre><pre lang="bash" escaped="true">* Checking property "Pay should be positive" ...
+++ OK, passed 100 tests (40% trivial).
* Checking property "You cannot get paid all overtime, or all std time" ...
+++ OK, passed 100 tests.
* Checking property "Not working overtime makes the math easy." ...
+++ OK, passed 100 tests.</pre>I started this article wanting to post a simple tutorial on Property testing, instead I learned to be a bit more careful using auto, and even when the function is simple, programmers can make mistakes. For the final logic error, the failing input was 60. Thinking about my directed test method, I would divide the input into equivalence domains and test the boundary values. For this input, I would divide standard time to the beginning of overtime. For directed tests I would have written tests for: 0, 39, 40 41, 99, 100, and 101. I would have missed the 60 hours bug, and there is the possibility that I missed typed the numbers on my calculator and type in a wrong expected value. This example is quite simple but still an interesting demonstration of property testing. I’m looking forward to applying property testing to my next project.
