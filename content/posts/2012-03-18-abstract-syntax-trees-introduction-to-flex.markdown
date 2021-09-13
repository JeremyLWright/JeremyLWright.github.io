---
author: Jeremy
comments: true
date: 2012-03-18 05:36:51+00:00
layout: post
slug: abstract-syntax-trees-introduction-to-flex
title: 'Abstract Syntax Trees: Introduction to Flex'
wordpress_id: 570
---

Bison is an incredibly powerful parser generator tool. However most of the examples, and tutorials demonstrate Bison's parsing ability, using on-the-fly computation instead of building a Syntax Tree. Bison is fully capable to generate the front-end of a simple compiler, but to do so, we have to build a syntax tree. Come to find out, building a syntax tree with Bison isn't that difficult, and the key is how one leverages the semantic actions. In this post, we'll look at a basic introduction to bison, then how to build a parse tree for a simple in-fix algebraic statement.

<!--more-->

Bison is a parser generator, and when combined with Flex (which we look at in a future post), can generate a very powerful, and very fast parser, and syntatic analyzer. Semantic analysis is still the responsibly of the language implementer.  These tools have different [computational power](http://en.wikipedia.org/wiki/Chomsky_hierarchy). Flex recognizes the simplest languages1, the regular languages. Regular languages are those which can be recognized with a finite-state machine, i.e. languages which do not require memory. Flex forms the tokenizer, or lexer of the compiler. It breaks the stream of characters into groups of identifiers called Tokens.

Flex is very easy to use. It consists of 3 sections. Each section is separated by a "%%" token. The first section setups up options. The next section defines all the tokens and their mapping to Non-Terminals. The last section is for raw C code to define helper, and other useful functions.

    
    %option noyywrap yylineno
    %{
    #include <iostream>
    using namespace std;
    #include "XParser.hpp" //Include the Bison file.
    extern "C"
    {
    int yylex();
    }
    
    %}
    
    %% 
    [ \t\n] ; //Ignore White Space
    "loop" { return LOOP_KEYWORD; };
    [a-zA-Z_][a-zA-Z0-9_]* { return IDENTIFIER; }



    
    %%



    
    /* Put other C Code */


This simple fragment of flex code will parse the input stream, and recognize the word "loop" as a keyword, and using he regular expression, will recognize any combination of letters and numbers, and return that value as an Non-Terminal denoted as IDENTIFIER.

In the next post I'll show Bison will consume these tokens and build the parse tree.



* * *






	
  1. This isn't entirely true. Flex implements POSIX regular expressions, which have more computational power than regular languages. However, for the sake of simplcity, we'll say Flex recognizes regular languages.


