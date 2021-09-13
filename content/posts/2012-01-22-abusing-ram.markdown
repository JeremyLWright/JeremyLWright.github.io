---
author: admin
comments: true
date: 2012-01-22 17:53:43+00:00
layout: post
slug: abusing-ram
title: Abusing RAM
wordpress_id: 499
expiryDate: 2020-01-01T00:00:00+00:00
tags:
- productivity
---

My system has 16GB of RAM, but since I run Linux I rarely use more than about 3GB.  So how do I justify such a extreme amounts of memory? Ramdisks.

<!--more-->

I run Lubuntu1, but hopefully this works for you too. Basically, I create a ramdisk and mount it in /mnt/ramdisk, then I setup the login/logout scripts to transfer to and from the ramdisk.


### Step 1: Create a ramdisk


Add this line to your fstab:

    
    none /mnt/ramdisk tmpfs defaults 0 0



By default a tmpfs will initialize to half of the total system RAM. If this is not desirable, you may use the size option to override the default.



### Step 2: Modify .profile


_.profile_ gets executed when a user logs in on a Ubuntu based system. .bash_profile will work for bash only shells. Add this script segment to .profile:

    
    
    #Setup the RAM disk Cache, if it doesn't exist
    if [ ! -d "/mnt/ramdisk/$USERNAME" ] ; then
        mkdir /mnt/ramdisk/$USERNAME
        cp -a $HOME/.cache /mnt/ramdisk/$USERNAME/
        rm -rf $HOME/.cache 
        ln -s /mnt/ramdisk/$USERNAME/.cache $HOME/.cache
    fi



This script snippet will create a folder in the ramdisk to house your .cache folder, then create a symbolic link into it. I saw a significant speed improvement for internet browsing over a disk based cache.



### Step 3: Modify .bash_logout


_.bash_logout_ gets executed when a user logs out of a Ubuntu based system. Add this script segment to .bash_logout:

    
    
    # If the RAM disk cache exists, copy it back to non-volatile
    if [ -d "/mnt/ramdisk/$USERNAME/.cache" ] ; then
        rm -f .cache
        cp -a /mnt/ramdisk/$USERNAME/.cache $HOME
    fi



this script snipped will copy your .cache bask to disk when you logout. This does 2 things. Firstly, it preserves your cache between reboots, which helps maintain high performance. Secondly, it reduces the ram usage if multiple people use the system. 



### Step 4: Enjoy


Enjoy, as application now run faster. But you are not done, you still have piles of empty RAM bits waiting to be used; find other folders on the system begging to be mounted to ram. tmp, /var/run, /var/lock are sexy options2. 



##### Footnotes






  1. I hate Unity.


  2. Reference: [https://wiki.archlinux.org/index.php/Fstab#tmpfs](https://wiki.archlinux.org/index.php/Fstab#tmpfs)
