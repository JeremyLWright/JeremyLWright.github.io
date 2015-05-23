+++
date = "2011-08-11T23:00:00-07:00"
draft = false
title = "Hijacking System Programs"
slug = "hijacking-system-programs"
tags = ["command line", "customize", "vim"]

+++
Let's say for a moment that you are a graduate student, with shell access to your schools server. The server maintains a number of tools you need for classes, and research.  All is well, except the stock editor on the server is wicked old.  Like an eternity old.  Well that happened to me. I am fully addicted to <a href="https://bitbucket.org/jwright/vim-configuration">my custom vim configuration</a>, but it requires vim7.3.  My school's server only has 7.0.  So, how does one install their own application with root privledges?  You create a private root.

<!--more-->The goal is to install a custom application which either is not available on they system, or the version available is tool old.  Essentially, you just need to install the program to your home folder, and add the new binary to your path.  Here is how I did just that:
<ol>
<ol>
	<li>Download your program of choice (vim in my case):
<pre lang="bash" escaped="true">-bash-3.2$ wget ftp://ftp.vim.org/pub/vim/unix/vim-7.3.tar.bz2</pre>
</li>
	<li>untar the application to build it:
<pre lang="bash" escaped="true">-bash-3.2$ tar -jxf vim-7.3.tar.bz2</pre>
</li>
	<li>Make a folder to hold your new custom applications:
<pre lang="bash" escaped="true">-bash-3.2$ mkdir ~/prvt-root</pre>
</li>
	<li>Configure the application with a custom prefix: (Notice the backtick.  --prefix requires an absolute directory. The backtick requests the shell to expand your home directory prior to calling configure.)
<pre lang="bash" escaped="true">-bash-3.2$ cd vim73
-bash-3.2$ ./configure --prefix=`~/prvt-root/` --with-features=huge</pre>
</li>
	<li>Make and install the app to your Private Root:
<pre lang="bash" escaped="true">-bash-3.2$ make &amp;&amp; make install</pre>
</li>
	<li>Modify your path to include your new root:
<pre lang="bash" escaped="true">-bash-3.2$ nano ~/.bash_profile
#Add the following lines to .bash_profile
PATH=~/prvt-root/bin:$PATH #Notice that your bin directory is BEFORE the system's default. This will allow your bin to be search first!
export PATH</pre>
</li>
	<li>Exit and log back in to use your new application!</li>
</ol>
</ol>
<div><a href="http://www.codestrokes.com/wp-content/uploads/2011/08/CustomVim7.3.png"><img class="aligncenter size-full wp-image-271" title="CustomVim7.3" src="http://www.codestrokes.com/wp-content/uploads/2011/08/CustomVim7.3.png" alt="" width="690" height="559" /></a></div>
