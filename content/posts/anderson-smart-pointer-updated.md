+++
date = "2012-04-29T19:38:00-07:00"
draft = false
title = "Anderson Smart-Pointer Idiom Updated!"
slug = "anderson-smart-pointer-idiom-updated"
tags = ["c++", "c++11", "RAII"]
+++

C++11 provides us with a ton of new tools for expressing complex ideas in an efficient way. C++11 is unique among modern languages in that it provides a productive syntax, while also generating exceptionally fast code. For the first time ever, software engineers are responsible for increasing the performance of software systems. For decades we've been standing on the shoulders of hardware engineers. Hardware engineers have been increasing the clock speeds of our processors, but we've hit a physical limit. It's our turn to pick up the baton in this relay race and get to the finish line. C++11 provides a number of tools to help us get there, and smart pointers are one such tool.
<!--more-->
The <a title="Making C++ like Python: The Anderson Smart Pointer Pattern" href="http://www.codestrokes.com/2011/10/making-c-like-python-the-anderson-smart-pointer-pattern/">Anderson Smart-Pointer idiom</a> is a pattern developed by a <a href="http://www.chrisanderman.com/">colleague of mine</a>. It supplants the constructor of a class with a factory method, to eliminate all raw pointers in a software system. Secondly, it provides typedefs for the smart pointers so one may use a terse type to express a more verbose concept. C++11 provides three tools which allow us to make this pattern more generic, while also increasing its performance.

C++11 allows us to apply the <a href="http://en.wikipedia.org/wiki/Don't_repeat_yourself">DRY</a> principle to the factory method.  Variadic templates allow us to render a completely generic version of the factory method. Until C++11, one was forced to duplicate the parameter list of the constructor in the factor method. This violates DRY, making maintenance more difficult. The factory construct now looks like this:
<pre lang="cpp" line="1" escaped="true">template&lt;typename... Ts&gt;
 static SmartClass::Ptr construct(Ts... vs)
 {
 SmartClass::Ptr c = std::make_shared&lt;SmartClass&gt;(SmartClass(vs...));
 c-&gt;self = c;
 return c;
 }</pre>
Except for the class name, this method never changes. This is powerful since it creates a <a href="http://en.wikipedia.org/wiki/Separation_of_concerns">separation of concerns</a>. The factory method is only concerned with creating a smart-pointer handle to some dynamically created object. Any specific details in the constructor, i.e. the parameters, are forwarded to the actual constructor. This renders thee factory method completely generic.

Line 4 also debuts another C++11 addition: perfect-forwarding. C++11 contains a special non-member constructor for shared pointers. This special constructor leverages the STL's <a href="http://en.cppreference.com/w/cpp/utility/forward">perfect-forwarding</a> to remove as much function-call overhead as possible. This small fragment of code, leverages the massively powerful <a href="http://en.wikipedia.org/wiki/C%2B%2B11#Rvalue_references_and_move_constructors">move-semantics</a> in C++11, generating extremely efficient code.

The last component which rounds out our updated idiom is that the smart pointer templates are now part of the standard namespace. Together the entire pattern looks like this:
<pre lang="cpp" line="1" escaped="true">#include &lt;memory&gt;
#include &lt;iostream&gt;

class SmartClass
{
public:
typedef std::shared_ptr&lt;SmartClass&gt; Ptr;
typedef std::weak_ptr&lt;SmartClass&gt; WeakPtr;
template&lt;typename... Ts&gt;
static SmartClass::Ptr construct(Ts... vs)
{
SmartClass::Ptr c = std::make_shared&lt;SmartClass&gt;(SmartClass(vs...));
c-&gt;self = c;
return c;
}
virtual ~SmartClass();
private:
SmartClass(int param1, char param2);
SmartClass::WeakPtr self;

};

int main(int argc, const char *argv[])
{
SmartClass::Ptr p = SmartClass::construct(2, 'c');
return 0;
}</pre>
Notice two things about the updated pattern. Even though the construct method is a template, we do not have to explicitly enumerate the constructor's types at the call site (line 25). Secondly, even though we're using a template, the entire class does not have to exist in the header file, only the template part, i.e. the construct method needs to be in the header. This is useful since it allows one to hide business logic in the cpp file, while still leveraging a generic template.

The updated Anderson smart-pointer idiom, extends an already powerful pattern into a more generic, high performance pattern. By applying <a href="http://en.wikipedia.org/wiki/Don't_repeat_yourself">DRY</a> to the factory method, we are able to create a completely generic version of the constructor, which improves maintenance and separates the concerns of class construction from the memory management. Secondly, by leveraging the move semantics of <em>make_shared&lt;&gt;()</em>, we create a shared_ptr with almost zero overhead. Lastly, the most powerful piece of this update is that  the public interface if this pattern has zero change. Code which already uses this patterns doesn't have to change. Updating the factory method and recompiling will pull in all the benefits.

&nbsp;

&nbsp;

&nbsp;
