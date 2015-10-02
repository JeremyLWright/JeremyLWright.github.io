---
author: Jeremy
comments: true
date: 2011-08-12 06:00:18+00:00
layout: post
slug: hijacking-system-programs
title: Hijacking System Programs
wordpress_id: 268
categories:
- Productivity
tags:
- command line
- customize
- vim
---

Let's say for a moment that you are a graduate student, with shell access to your schools server. The server maintains a number of tools you need for classes, and research.  All is well, except the stock editor on the server is wicked old.  Like an eternity old.  Well that happened to me. I am fully addicted to [my custom vim configuration](https://bitbucket.org/jwright/vim-configuration), but it requires vim7.3.  My school's server only has 7.0.  So, how does one install their own application with root privledges?  You create a private root.

<!-- more -->The goal is to install a custom application which either is not available on they system, or the version available is tool old.  Essentially, you just need to install the program to your home folder, and add the new binary to your path.  Here is how I did just that:




	
    1. Download your program of choice (vim in my case):

    
    -bash-3.2$ wget ftp://ftp.vim.org/pub/vim/unix/vim-7.3.tar.bz2




	
    2. untar the application to build it:

    
    -bash-3.2$ tar -jxf vim-7.3.tar.bz2




	
    3. Make a folder to hold your new custom applications:

    
    -bash-3.2$ mkdir ~/prvt-root




	
    4. Configure the application with a custom prefix: (Notice the backtick.  --prefix requires an absolute directory. The backtick requests the shell to expand your home directory prior to calling configure.)

    
    -bash-3.2$ cd vim73
    -bash-3.2$ ./configure --prefix=`~/prvt-root/` --with-features=huge




	
    5. Make and install the app to your Private Root:

    
    -bash-3.2$ make && make install




	
    6. Modify your path to include your new root:

    
    -bash-3.2$ nano ~/.bash_profile
    #Add the following lines to .bash_profile
    PATH=~/prvt-root/bin:$PATH #Notice that your bin directory is BEFORE the system's default. This will allow your bin to be search first!
    export PATH




	
    7. Exit and log back in to use your new application!





[![](http://www.codestrokes.com/wp-content/uploads/2011/08/CustomVim7.3.png)](http://www.codestrokes.com/wp-content/uploads/2011/08/CustomVim7.3.png)
