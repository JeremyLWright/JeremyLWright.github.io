---
author: admin
comments: true
date: 2013-10-27 23:00:17+00:00
layout: post
slug: a-thunk-on-laziness
title: A Thunk on Laziness
wordpress_id: 1107
categories:
- Security
---

I originally approached Haskell excited, and wide-eyed mystified by the type theory. Type became my golden hammer. In my C programs I typedef'd everything so it'd have a "unique" type. I was cautious with my casting. I was hooked. I had an intuitive understanding of laziness, as implemented by Haskell, that would allow one to write"streaming" algorithms. That is programs that deal with data in an online way to process data as it streams through. While that maybe true, you know what else can do that? C.
<!-- more -->
I recently has a problem to extract logs from a product at work. The existing solution e.g. the solution I wrote the week before, was exponential in time. We had a problem. We had to extract the logs, and separate them by an sentinel in the file, encrypt the files, compress them, then copy the output to a thumbdrive. The only problem we didn't have enough RAM to store the entire file in memory, and we didn't have enough flash to create temporary files.  I needed a streaming algorithm.  

My first approach was to use UNIX pipes and filter data through sed | gzip | openssl. This worked, but required multiple workarounds to generate the sed expressions, eventually resulting in exponential time.  The second time, I was discussing with my co-worker, the virtues of compiled code versus shell scripts. In that vain I started looking into openssl as a library rather than an executable. You know who has streaming algorithms? OpenSSL. OpenSSL, has a fantastic abstraction called BIO_, Basic Input/Output. Which are simply functions you connect together in a chain to process data. The BIO interface is designed to allow one to work with SSL encrypted sockets in an intuitive way. For our use case we simply connected an zlib BIO -> AES BIO -> file sink. Write to the zlib, and watch the data compress, and write to the thumbdrive in one swoop, no laziness, thunking, or fancy data structure fusion required. The result: linear time. 

So the lesson here isn't a technological one, but a personal one about myself. Don't reach for a new technology to solve something. Look deeper into the root of the problem, and even a language as "dumb" and "simple", and "old" as C, can provide the fastest, optimal solution. 
