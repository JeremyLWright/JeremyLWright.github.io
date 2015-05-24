---
author: admin
comments: true
date: 2013-02-24 16:38:11+00:00
layout: post
slug: duplicating-sd-cards-for-beagleboard
title: Duplicating SD Cards for Beagleboard
wordpress_id: 831
---

The ASU Linux User's group is building a Beagleboard cluster. This requires each compute node to have an identical system image, with the exception of the hostname and ipaddress. The easiest way, I found to do this, is to configure one compute node, then duplicate the SD cards across the other nodes. Here is how I did that.

<!-- more -->

Save the partitions to an image file using part image

    
    partimage save /dev/sdb1 beagle-cluster-boot.000 beagleboard-cluster-boot.000
    partimage save /dev/sdb2 beagle-cluster-boot.000 beagleboard-cluster-rootfs.000


Save the partitions table to a file

    
    sudo sfdisk -d /dev/sdb > beagleboard-cluster-partitions.sfdisk


Eject the card, and put in a blank card.

Unmount the partitions

    
    umount /dev/sdb2
    umount /dev/sdb1


Copy the partition table to the new card

    
    sudo sfdisk --force /dev/sdb < beagleboard-cluster-partitions.sfdisk


Copy the partition images to the new card

    
    sudo partimage restore /dev/sdb1 beagleboard-cluster-boot.000
    sudo partimage restore /dev/sdb2 beagleboard-cluster-rootfs.000
    sync


Boot it up!
[suffusion-adsense client='ca-pub-6284398857369558' slot='1495369305' width='728' height='90']
