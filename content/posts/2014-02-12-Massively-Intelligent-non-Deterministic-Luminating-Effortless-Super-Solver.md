+++
date = "2014-02-12T08:50:00-07:00"
draft = false
title = "Massively Intelligent Non-Deterministic Luminating Effortless Super Solver"
slug = "cracking-subciphercpp"
tags = ["c++", "c++11", "cipher", "cryptogram", "crytography",
"monoalphabetic", "substitution cipher"]

+++
I worked the title of this article several times before I finally settled on the subtly epic heading you see above. Hopefully this title will funnel people off google into my blog (delicious SEO). I wanted to push the A.I. component of my solution because A.I. is awesome and mysterious, and cool (and can like solve jeopardy). I was quickly disillusioned however. Really, A.I. isn't magic, rather it's just the same thing computers have been doing for a long time: computing. Sadly this realization took several months in an A.I. class before I was sufficiently crestfallen. A.I. patterns including the hill climbing algorithm used here are indeed "intelligent" but really it a reflecting of the algorithm designer, not the entity executing the algorithm. So I built a substitution cipher solver in C++. It's fast it uses random numbers i.e. non-deterministic, it uses an A.I. algorithm i.e. Intelligent, it uses threads i.e. Massively, it deciphers i.e. luminates the text and it solves super stuff therefore the title is completely justified. I give you my Massively Intelligent Non-Deterministic Luminating Effortless Super Solver (MINDLESS). If none of that interests you then please stick around and follow the side quest of looking for <a href="http://justenoughcraig.blogspot.com/2014/01/just-say-no-to-passive-aggressive.html">emotionally charged parenthesis</a>.

<!--more-->

Cracking substitution ciphers were a fun puzzle I pursued as a child. Substitution ciphers are monoalphabetic ciphers. Meaning a single letter maps to a single letter and that mapping is static. This is opposed to polyalphabetic ciphers where the mapping of letters changes throughout the message. Vigenère Cipher is an example. Given a substitution cipher what are tools are available to the "cryptanalyst" (the person to breaks ciphers). Firstly, frequency analysis. Frequency analysis supposes the the distribution of letters within the message is essentially the same as the distribution of letters in the English language (http://en.wikipedia.org/wiki/Frequency_analysis). However if the message is short, or if the message is intentionally written to skew the letter distribution this technique is difficult. This post looks at a different approach, an artificial intelligence technique called hill climbing.

Hill Climbing is simply a search technique that uses a "fitness" measurement (fancy word for number or quality) to determine if the current search path is a useful one.

First step in building the substitution solver is to assemble some functions that will perform the substitution. I love the string functions in Python to I ported str.translate() to a form useful for my needs
<pre lang="cpp" escaped="true">std::string translate( cost std::string &amp; str, const std::string &amp; table)
{
    std::string s(str);
    std::string::size_type len = str.size();

    if ( table.size() != 256 )
    {
        throw std::runtime_error("Improper table size. Size must be 256 chars");
    }

    for ( std::string::size_type i = 0; i &lt; len; ++i )
    {
        s[i] = table[ s[i] ];
    }
    return s;
}

std::string maketrans(std::string key)
{
    char t1data[256];
    std::iota(std::begin(t1data), std::end(t1data), 0);
    size_t i = 'A';
    size_t d = 'a' - 'A';

    for(auto k = std::begin(key); k != std::end(key); ++i, ++k)
    {
        t1data[i] = *k;
        t1data[i+d] = std::tolower(*k);
    }
    return std::string(t1data, 256);
}</pre>
This leverages the fact that in C/C++, characters are simply numbers in ascii. Given a key, we can translate any text:
<pre lang="cpp" escaped="true">std::string substitute(std::string text, std::string key)
{
    auto t1 = pystring::maketrans(key);
    return pystring::translate(text, t1);
}</pre>
Now we need a fitness measurement. Ngrams are a useful tool here. Ngrams are partial words, and since we are more likely to find partial words in our search than full words, we need to give the program a mechanism for measuring this. This <a href="http://www.codestrokes.com/wp-content/uploads/2014/02/quadgrams.7z">ngram</a> database is a list of quadgrams and their relative frequency in the English language.

<pre lang="cpp" escaped="false">#include <map>
#include <istream>
#include <string>
#include <ctgmath>
#include <iostream>
struct ngram_score 
{
    struct ngram_datum {
        int freq;
        double weight;
    };
    std::map<std::string, ngram_datum> ngrams;
    double floor;
    size_t l;
    size_t n{0};
    ngram_score(std::istream& in)
    {
        std::string line;
        while(in)
        {
            std::string ngram;
            int freq;
            in >> ngram;
            in >> freq;
            ngrams[ngram].freq = freq;
            n += freq;
        }

        for(auto& i : ngrams)
        {
            i.second.weight = std::log10((double)(i.second.freq)/n);
        }
        floor = std::log10(0.01/n);
        l = 4; //for quadgrams.
    }

    double score(std::string text)
    {
        double score{0};
        auto c = std::begin(text);
        auto e = std::end(text);
        for(; c+l-1 != e; ++c)
        {
            //Get a string of correct length
            std::string ngram(c, c+l);
            auto it=ngrams.find(ngram);
            if(it != ngrams.end())
                score += it->second.weight;
            else
                score += floor;
        }
        return score;
    }
};</pre>

We can use this as a scorer for a length of text.
<pre lang="cpp" escaped="false">std::ifstream fin("../quadgrams.txt");
ngram_score fitness(fin);
auto score = fitness.score(plaintext);</pre>
 
We now have a substitution tool to make substitutions, and we have a numerical way of measuring the resultant quality. Next is to implement the search, this is the mystical artificial intelligence in the program. 
<pre lang="cpp" escaped="false">
struct cipher {
    std::string key;
    double score;
    std::string plaintext;
    friend std::ostream& operator<<(std::ostream& os, cipher const & c);
};


cipher break_substitution(std::string cipher_text, std::string skey)
{
    std::transform(std::begin(cipher_text), std::end(cipher_text), std::begin(cipher_text), ::toupper);
    std::uniform_int_distribution<int> distribution(0,25); 
    
    cipher p;
    p.key = skey;
    p.plaintext = substitute(cipher_text, p.key);
    p.score = fitness.score(p.plaintext); 
    for(size_t i = 0; i < 1000; ++i) //Look at that intelligent for loop
    {
        cipher c(p);
        auto a = distribution(g);
        auto b = distribution(g);
        std::iter_swap(std::begin(c.key)+a, std::begin(c.key)+b); //randomly tweak our key
        c.plaintext = substitute(cipher_text, c.key);
        c.score = fitness.score(c.plaintext);  //Measure the quality of the new key.
        if(c.score > p.score)
        {
            p = c; //update the parent
            i = 0; //We've made an improvement
        }
    }
    return p;
}
</pre>

So artificial intelligence, it's just computation.  The trick is that we are a little more intelligent that brute force.  Our algorithm is to generate a random key, substitute the cipher text with that key and measure the quality of the result, i.e., how many partial words are in the result.  Now swap 2 characters, and measure it again. If the result is better continue swapping with that key, if the result is worse throw away that key (branch of the search tree), and return to the previous key (p in this example).

In this post we looked at how MINDLESS can break substitution ciphers using hill climbing.  If you were following the side-quest, I hope you enjoyed yourself (or rather are overwhelming cross (because of the parenthesis), but be thankful they are balanced).
