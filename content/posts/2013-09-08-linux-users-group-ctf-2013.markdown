---
author: admin
comments: true
date: 2013-09-08 21:58:06+00:00
layout: post
slug: linux-users-group-ctf-2013
title: Linux User's Group CTF 2013
wordpress_id: 1187
categories:
- CTF
- Security
tags:
- Contest
- cracking
- CTF
- hack-a-thon
- hacking
- Security
---

This past weekend we held another capture the flag event at the Arizona State University's Linux User's Group. It had more of a system admin focus than security cracking exploits, but it was fun an nontheless a diverse learning experience for all those involved. However, almost immediately, I realized the number one rule in CTF, nothing is off limits!
<!-- more -->
The game was organized into two parts, a game server which collected the the scores and displayed the point totals of all teams in real-time, and the virtual servers (hosted on Amazon EC2) which contained the actual games. Players were encouraged to break into teams, and register themselves on the game server. The game server would assign the team a virtual machine, and the team could log in via SSH to behind hacking. Five minutes into the registration process, one team attempted a SQL injection attack against the game server.

[caption id="attachment_1189" align="aligncenter" width="700"][![Notice the SQL Injection attempt](http://www.codestrokes.com/wp-content/uploads/2013/09/Final-Score-1024x429.png)](http://www.codestrokes.com/wp-content/uploads/2013/09/Final-Score.png) Notice the SQL Injection attempt[/caption]

I wrote the game server as a django webapp, to collect points, and serve as a dashboard for the players. We logged in at the front of the room and displayed the graph on the front projector. It was a very motivating aspect of the game, however I never planned on it being part of the game itself.  First lesson learned in capture the flag, nothing is off limits. Luckily, django does the right thing, and sanitizes form data automatically. The server was unscathed, the failed injection attempt was displayed for all the teams to see. I'm currently compiling additional aspects of what worked and what didn't so check back soon. The CTF was a fantastic event this year, and really motivated newbies, and elites a like. 



