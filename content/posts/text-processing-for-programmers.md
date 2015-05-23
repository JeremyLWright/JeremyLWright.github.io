+++
date = "2012-02-17T12:53:00-07:00"
draft = false
title = "Text Processing for Programmers"
slug = "text-processing-for-programmers"
tags = ["unix"]
+++
I was reading a <a href="https://sites.google.com/site/steveyegge2/five-essential-phone-screen-questions">blog </a>about coding interviews, and one comment made near the bottom struck me, "..."Um... grep?" then they're probably OK..."  As I read that comment, I realized I'd never answer that way, and I agreed with the author that was a problem. That began my dabble in grep, awk and sed, and these tools will change your workflow and even how you think about profiling code.  Grep has even become a verb in my daily life, "Is this <em>greppable?</em>" is my mantra.  Flash forward a few months and once again I had a task for these powerful text processing tools, convert a mysql database to sqlite. Sounds easy, but with file sizes of &gt;700MB, you have to be efficient.

<!--more-->
As part of a machine learning project for a graduate class I'm using the enron email <a href="http://aws.amazon.com/publicdatasets/">public dataset</a>. This dataset has been further processed and cleaned at <a href="http://www.cs.cmu.edu/~enron/">Carnagie Mellon</a>. This dataset is so valuable because it is real world email from a functioning orginazation. This dataset is used in human factors research, machine learning, and as in my usecase, data security. I downloaded the mysql version and since I intended to use Python to do my processing I wanted to convert it to sqlite.
[suffusion-adsense client='ca-pub-6284398857369558' slot='8519108503' width='300' height='250']


My basic process is:

<ol>
	<li>Import the dataset into a mysql database</li>
	<li>Use this <a href="https://gist.github.com/esperlu/943776">gist</a> to dump the database into sqlite.</li>
</ol>
Cool. So Step 1.
<pre lang="bash" escaped="true">jwright@ubuntu:~$ mysql -u root -p -h localhost enron &lt; enron-mysqldump.sql 
Enter password: 
ERROR 1064 (42000) at line 10: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'TYPE=MyISAM' at line 8
jwright@ubuntu:~$ grep enron-mysqldump.sql 'TYPE-MyISAM'
grep: TYPE-MyISAM: No such file or directory</pre>
Damn. Well, lets see what the problem is... Remember this file is &gt;700 MB so I don't want to just open it in notepad.
<pre lang="bash" escaped="true">jwright@ubuntu:~$ grep 'TYPE=MyISAM' enron-mysqldump.sql
 ) TYPE=MyISAM;
 ) TYPE=MyISAM;
 ) TYPE=MyISAM;
 ) TYPE=MyISAM;
 jwright@ubuntu:~$</pre>
Oh. That's <em>greppable</em>, awesome.
<pre lang="bash" escaped="true">sed 's/TYPE=MyISAM/engine=myisam/g' enron-mysqldump.sql &gt; enron-mysqldump_filtered.sql</pre>
Now we have a clean file for import.
<pre lang="bash" escaped="true">mysql -u root -p -h localhost enron &lt; enron-mysqldump_filtered.sql
./mysql2sqlite.sh -u root -p enron | sqlite3 enron.db</pre>
732MB database converted in just a few minutes. Mostly just I/O time. I believe all good programmers show know these tools. I know personally, when I have to export data for profiling or metrics, I do it in a way that I can easily filter with awk, or sed to a format octave can process. Automating measurements will dreastically decrease your cycle time and reduce mistakes.

So "Um... grep?"

Hell yes grep!
