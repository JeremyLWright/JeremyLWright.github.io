+++
date = "2012-02-24T09:38:00-07:00"
draft = false
title = "Duplicating SD Cards for Beagleboard"
slug = "duplicating-sd-cards-for-beagleboard"
tags = ["hardware"]
+++
The ASU Linux User's group is building a Beagleboard cluster. This requires each compute node to have an identical system image, with the exception of the hostname and ipaddress. The easiest way, I found to do this, is to configure one compute node, then duplicate the SD cards across the other nodes. Here is how I did that.

<!--more-->

Save the partitions to an image file using part image
<pre lang="bash" escaped="true">partimage save /dev/sdb1 beagle-cluster-boot.000 beagleboard-cluster-boot.000
partimage save /dev/sdb2 beagle-cluster-boot.000 beagleboard-cluster-rootfs.000</pre>
Save the partitions table to a file
<pre lang="bash" escaped="true">sudo sfdisk -d /dev/sdb &gt; beagleboard-cluster-partitions.sfdisk</pre>
Eject the card, and put in a blank card.

Unmount the partitions
<pre lang="bash" escaped="true">umount /dev/sdb2
umount /dev/sdb1</pre>
Copy the partition table to the new card
<pre lang="bash" escaped="true">sudo sfdisk --force /dev/sdb &lt; beagleboard-cluster-partitions.sfdisk</pre>
Copy the partition images to the new card
<pre lang="bash" escaped="true">sudo partimage restore /dev/sdb1 beagleboard-cluster-boot.000
sudo partimage restore /dev/sdb2 beagleboard-cluster-rootfs.000
sync</pre>
Boot it up!
[suffusion-adsense client='ca-pub-6284398857369558' slot='1495369305' width='728' height='90']
