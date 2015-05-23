+++
date = "2012-01-22T10:53:00-07:00"
draft = false
title = "Abusing Ram"
slug = "abusing-ram"
tags = ["c++"]

+++
My system has 16GB of RAM, but since I run Linux I rarely use more than about 3GB.  So how do I justify such a extreme amounts of memory? Ramdisks.

<!--more-->

I run Lubuntu<sup><a href="#footnote_1">1</a></sup>, but hopefully this works for you too. Basically, I create a ramdisk and mount it in /mnt/ramdisk, then I setup the login/logout scripts to transfer to and from the ramdisk.
<h3>Step 1: Create a ramdisk</h3>
Add this line to your fstab:
<pre lang="bash" escaped="true">none /mnt/ramdisk tmpfs defaults 0 0</pre>

By default a tmpfs will initialize to half of the total system RAM. If this is not desirable, you may use the size option to override the default.

<h3>Step 2: Modify .profile</h3>
<em>.profile</em> gets executed when a user logs in on a Ubuntu based system. .bash_profile will work for bash only shells. Add this script segment to .profile:
<pre lang="bash" escaped="true">
#Setup the RAM disk Cache, if it doesn't exist
if [ ! -d "/mnt/ramdisk/$USERNAME" ] ; then
    mkdir /mnt/ramdisk/$USERNAME
    cp -a $HOME/.cache /mnt/ramdisk/$USERNAME/
    rm -rf $HOME/.cache 
    ln -s /mnt/ramdisk/$USERNAME/.cache $HOME/.cache
fi</pre>

This script snippet will create a folder in the ramdisk to house your .cache folder, then create a symbolic link into it. I saw a significant speed improvement for internet browsing over a disk based cache.

<h3>Step 3: Modify .bash_logout</h3>
<em>.bash_logout</em> gets executed when a user logs out of a Ubuntu based system. Add this script segment to .bash_logout:
<pre lang="bash" escaped="true">
# If the RAM disk cache exists, copy it back to non-volatile
if [ -d "/mnt/ramdisk/$USERNAME/.cache" ] ; then
    rm -f .cache
    cp -a /mnt/ramdisk/$USERNAME/.cache $HOME
fi</pre>

this script snipped will copy your .cache bask to disk when you logout. This does 2 things. Firstly, it preserves your cache between reboots, which helps maintain high performance. Secondly, it reduces the ram usage if multiple people use the system. 

<h3>Step 4: Enjoy</h3>
Enjoy, as application now run faster. But you are not done, you still have piles of empty RAM bits waiting to be used; find other folders on the system begging to be mounted to ram. tmp, /var/run, /var/lock are sexy options<sup><a href="#footnote_2">2</a></sup>. 

<h5>Footnotes</h5>
<ol>
<li><a id="footnote_1"></a>I hate Unity.</li>
<li><a id="footnote_2"/></a>Reference: <a href="https://wiki.archlinux.org/index.php/Fstab#tmpfs">https://wiki.archlinux.org/index.php/Fstab#tmpfs</a></li>
