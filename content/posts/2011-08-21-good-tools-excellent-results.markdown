---
author: Jeremy
comments: true
date: 2011-08-21 07:23:25+00:00
layout: post
slug: good-tools-excellent-results
title: Good Tools, Excellent Results
wordpress_id: 313
categories:
- Coding
tags:
- productivity
- Python
- tools
languages: 
- C++
---

This semester for the C++ practicum we are building a clone of Zork.  Like many games of the genre, Zork is driven by a database.  Our implementation is a JSON database.  I chose JSON for a few reasons, but most importantly because its a human readable format that's simple to understand.  I started by editing JSON files by hand in a text editor, however I found very quickly that investigating in a quick tool greatly improved my quality.

<!-- more -->I chose JSON as a format. Next, I needed a schema.  Currently the schema design is as follows:

    
    "Clearing": {
     "Description": "You are in a clearing. There is a berry bramble to your right.",
     "Exits": {
         "East": "Up a Tree",
         "North": "Grating Room",
         "South": "Clearing",
         "West": ""
     },
     "Items": ["Berries", "Sword"]
     }


If nothing else its simple. So I started to layout the map, editing the JSON database directly in my text editor.  I found that even with such a simple schema, in a simple format such as JSON, it is incredible difficult to manage more than a few rooms.  I needed a better tool, a Map Editor.

Python to the rescue.  Using PyQt and Qt Designer I was able to whip up a dirty little map editor in an evening (totally about 3 hours).

[![](http://www.codestrokes.com/wp-content/uploads/2011/08/Screenshot-Practicum-Game-Editor-1024x786.png)](http://www.codestrokes.com/wp-content/uploads/2011/08/Screenshot-Practicum-Game-Editor.png)With this I can not manage a much larger database, giving my players a much more immersive environment.  Secondly, my students can use and even extend the tool to make even better game play.

I wasted quite a bit of time hand editing JSON files, when such a simple tool could be built in less than half the time.  I took it as just another example of, "Sometimes you have to slow down to speed up."  Take time to make your tools work.  Take time to make the right tools, and it will always pay dividends.

Source Code is available here: [https://bitbucket.org/jwright/gamecomponents](https://bitbucket.org/jwright/gamecomponents)




