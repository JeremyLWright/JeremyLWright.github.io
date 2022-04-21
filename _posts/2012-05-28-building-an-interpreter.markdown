---
author: admin
comments: true
date: 2012-05-28 17:03:55+00:00
layout: post
slug: building-an-interpreter
title: Building an Interpreter
wordpress_id: 630
tags:
- Compilation
- AST
- Bison
- C++
- compiler
- Flex
---

When I started programming, I thought that compilers where these magic behemoths; Oracles which consumed your source code, and prophesied  the resulting program.  I thought that the compiler was an integral part of the "system". I was excited to realize that the compiler is simply another program. A program you can write yourself. You can write a compiler, for your very own language.  Go ahead, make up a language, I'll wait...

[![](http://www.codestrokes.com/wp-content/uploads/2012/05/hourglass.gif)](http://www.codestrokes.com/wp-content/uploads/2012/05/hourglass.gif)

Seriously though, making your own language is a very difficult task, and implementing a language useful enough for non-trivial problems is even more difficult. There is however, a very approachable goal here: Domain Specific Languages (DSLs).  DSLs are focused languages useful to a limited group of people for a limited purpose.

I like to think of DSLs as tools. For example, sometimes one needs to automate a task, its might be easier to write a small program that helps with that task. But it might be even more useful to write a language that allows you to describe the problem better, then one can write a program using the new language to finish the task in an efficient and repeatable way.  The program has limited usefulness beyond its initial application, but for the application at hand, its perfect. SQL is the canonical example. In this post we'll start with a basic grammar in EBNF. We'll translate that to a flex lexer, and connect that to a bison parser. We'll end up with a syntax tree which we'll execute to calculate a result.

<!--more-->

The first step in writing a language is creating the grammar. This is horrifically difficult, however for this example we'll assume we already have a grammar.

    
    Program → Block
    Block → {Declaration} {Statement}
    Declaration → VariableDeclaration | ConstantDeclaration
    VariableDeclaration → var Id {‘,’ Id}
    ConstantDeclaration → const Id ‘=’ Number
    Statement → Assignment | PrintStmt | IfStmt | DoStmt
    Assignment → Id ‘:=’ Expression
    PrintStmt → print Expression
    IfStmt → if {do Expression ‘->’ Block end} end
    DoStmt → loop {do Expression ‘->’ Block end} end
    Expression → Simple [ Relop Simple ]
    Simple → UniTerm {Ampop UniTerm}
    UniTerm → Perop UniTerm | Term
    Term → Factor [Atop Term]
    Factor → ‘(’ Expression ‘)’ | Number | Id
    Relop → ‘=’ | ’<’ | ’>’ | ‘/=’ | ‘<=’ | ‘>=’
    Ampop → ‘&’
    Perop → ‘%’
    Atop → ‘@’


Now we have a grammar, and we can think up some simple test cases. These will be used to evaluate the compiler we're building. This is infinitely important. Compilers are built on the principles of Context-Free-Languages, which by definition are infinite, ergo testing is critically important. Since you cannot possible think of every test case, directed test maybe insufficient, but this discussion is beyond the scope of the post.

To use Bison to parse this, we need make sure that the grammar is LL(k). Bison is not capable of parsing the entire CFL space, furthermore, [bison prefers left-recursion](http://dinosaur.compilertools.net/bison/bison_6.html#SEC42). Many compiler books encourage right-recursion since[ recursive-decent prefers it](http://stackoverflow.com/questions/847439/why-cant-a-recursive-descent-parser-handle-left-recursion). LL(k) is a different animal.  To prove that this grammar is LL(k) compatible, is beyond the scope of this post, but it entails calculating the _First_ and _Follow _sets for each grammar rule.


## Converting to BNF


Our grammar is in EBNF right now. I've found it easier to write the bison grammar from the BNF form. I found [a few tricks](http://lampwww.epfl.ch/teaching/archive/compilation-ssc/2000/part4/parsing/node3.html) to help. Following these tricks blindly will result in a grammar which is a bit bigger than necessary e.g. the grammar will not be minimum. For our simple grammar this is not a big issue. However, for a production compiler, a minimum grammar is very important.

    
     Program → Block
     Block → ε | Block Declaration | Block Statement
     Declaration → VariableDeclaration | ConstantDeclaration
     VariableDeclaration → 'var' TIDENTIFIER | ',' TIDENTIFIER
     ConstantDeclaration → 'const' TIDENTIFIER '=' TNUMBER
     Statement → Assignment | PrintStmt | IfStmt | DoStmt
     Assignment → TIDENTIFIER TASSIGN Expression
     PrintStmt → 'print' Expression
     IfStmt → 'if' Condition 'end'
     DoStmt → 'loop' Condition 'end'
     Condition → ε | Condition do Expression '->' Block 'end'
     Expression → Simple | Simple RELOP Simple | Simple TEQ Simple
     Simple → UniTerm | Simple TAMPOP UniTerm
     UniTerm → TPEROP UniTerm | Term
     Term → Factor | Factor TATOP Term
     Factor → LPAREN Expression RPAREN | TNUMBER | TIDENTIFIER


Notice that a few rules appear missing. Actually during translation we noted which items can be recognized by the lexer. These tokens are captured by flex/lex, and simplify how much work Bison needs to do. As a general rule the sooner you can translate something the better. This allows your deeper layer to be more abstract e.g. replacing strings in favor of tokens.  (Get [Bison-Flex](http://www.codestrokes.com/wp-content/uploads/2012/05/Bison-Flex.7z) Files). Now that we have the lexer, and syntax analyzer, we can work on **semantic** analysis. This is an important point that took me a while to understand: syntax is orthogonal to semantics. Said another way, _how something is said is separate to what is said_.  Bison will parse the syntax and give use the terminal tokens in the correct order, but it is our responsibility to translate that to actual code.


## Syntax-Directed Translation


[Syntax-Directed Transalation](http://en.wikipedia.org/wiki/Syntax-directed_translation), is one method for attaching semantic actions to the rules of a grammar. I image that the grammar rule is  the line to the constructor of a C++ class. For example, take the _Assignment _rule:

    
    Assignment → TIDENTIFIER TASSIGN Expression


This rule has 2 important parts, TIDENTIFIER and the Expression. The TASSIGN token is implied by the rule itself. This allows us to write a class as follows:

    
    struct Assignment {
    
        Assignment(string id, Expression* rhs):
        _rhs(rhs),
        _identifier(id)
        {
        }
    
        virtual string ToString()
        {
            return "Assignment:: ";
        }
    
        virtual void Execute()
        {
            int value = _rhs->Execute();
            programSymbolTable->GetSymbol(_identifier)->SetValue(_rhs->Execute());
        }
    
      Expression* _rhs;
      string const _identifier;
    };


Following in this way we can complete semantic actions for each rule. To finish our interpreter we simply need to leverage the Bison PDA to link all the objects together.


## The Abstract Syntax Tree


Behind the scenes, Bison uses a very efficient table driven parser. For this project, I've found its easier to treat Bison parser as a black-box, and independent of how is actually implemented, imagine Bison uses a theoretical Push-down Automata.

[caption id="" align="aligncenter" width="340" caption="PDA from Wikipedia.org"][![PDA from wikipedia](http://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Pushdown-overview.svg/340px-Pushdown-overview.svg.png)](http://en.wikipedia.org/wiki/Pushdown_automaton)[/caption]

From this picture Bison's _$$_ token represents the A. The input tape is preprocessed by flex. Ergo, at this point the input tape, is a_ string of tokens_, not a string of characters. We mentioned earlier that Bison prefers left-recursion, this is directly attributed to the PDA architecture it uses. Bison's method of matching the stack allows right-recursion to use bounded stack space. We've discussed before how [memory allocation](http://www.codestrokes.com/2011/11/parallel-binary-buddy-the-friendly-memory-manager/) is one of the slowest operations a program can perform, therefore limiting the memory usage is always a meaningful performance enhancement.

Bison's will now parse the input tokens for use, and as it matches each rule, automatically recurse through the rules until it reaches a terminal. This in turn will call your semantic actions in the reverse order to compose your tree. By returning each new node of the tree into the $$, Bison will pass the chain of objects back up the parse tree. Let's see an example:

    
    N := i & 1


This is an assignment. the bison follows our rules in the following order:

    
    Assignment : TIDENTIFIER TASSIGN Expression
    TIDENTIFIER = 'N', matched by flex
    TASSIGN = ':=' matched by flex


Expression is a non-terminal so keep parsing
Our stack at this point has the following items in it:

    
    TIDENTIFIER:'N'
    TASSIGN:':='


Now Bison has to resolve the Expression rule into terminals, so bison jumps to the Expression Rule:

    
    Expression : Simple
               | Simple RELOP Simple
               | Simple TEQ Simple


Simple matches, so keep parsing.

    
    Simple: UniTerm
               | Simple TAMPOP UniTerm
    TAMPOP = '&'


UniTerm matches so keep parsing. Following in this way, we eventually reach the Factor rule:

    
    Factor : LPAREN Expression RPAREN { $$ = $2; }
            | TNUMBER { $$ = new Factor($1); } <-- Runs this one for the '1'
            | TIDENTIFIER { $$ = new Factor(*$1); } <-- Runs this for the 'i'
    TNUMBER = '1'
    TIDENTIFIER = 'i'


Now we return up the parse tree, at each semantic action we pass the newly created object into the $$ token. The power of Bison, is how it calls the rules in the correct order allowing you to compose your tree correctly, or recognize a syntax error if rules don't match.

At this point there a fork in the road. We can either execute our tree directly, which makes our interpreter complete, or we can move on to code-generation. Code generation will translate the AST we built into some other language. This target language is frequently C for DSLs. C allows for massive flexibility, while retaining platform portability. Every platform has a C compiler, there by targeting C, your language also runs on every platform. This difference between interpreter and compiler is subtle, since some interpreters include virtual machines, and translate the source code to an intermediate form which the internal virtual machine executes. Python is one such example of this.


## Conclusion


Bison is a powerful tool, combined with Syntax-Directed translation, we have a powerful tool for matching languages. Bison can parse streaming data as well, by combining these techniques, one can recognize a stream of commands sent over a network, or other dynamic source. For the embedded spaces this offers a very powerful way of interfacing with downstream sensors and ECUs. Bison is also extremely efficient and uses a bounded memory stack, allowing use in the smallest of microcontrollers.
