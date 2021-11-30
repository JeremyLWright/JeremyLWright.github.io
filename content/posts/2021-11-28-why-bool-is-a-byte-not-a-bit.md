---
title: "Why is bool one byte: Wasting space to save time" 
date: 2021-11-28T00:00:00-07:00
draft: false
slug: why-bool-is-one-byte
languages:  
- C
tags:
- hardware
- low-level
---


Boolean carries 1 bit of information. The canonical example of binary, On/Off,
True/False. Yet, the bool type in C and C++ is 1 byte large, 8 bits of
information. Carrying thus $$2^8 = 256$$ representable values. This may not sound like much, but consider an array of bools (a common misunderstanding beginning C++ students make trying to formulate a bit-field): ``bool fatBitField[8]`` 

This _wasted_ space however has a useful purpose. It a common reason in many optimizations we make in data structures, we trade space for time. In this instance we're trading space for a hardware design principle, addressable memory.  

<!-- more -->

```c
#include <stdio.h>
#include <stdbool.h>

int main(int argc, const char *argv[])
{
	bool b;
	bool fatBitField[8];
	printf("%lu\n", sizeof(b));           // prints 1
	printf("%lu\n", sizeof(fatBitField)); // prints 8
	return 0;
}
```

Outputs
```shell
➜  clang -std=c11 byte.c
➜  ./a.out
1
8
```

x86 based machines and most microprocessors except for some uniquely specialized Digital Signal Processors (DSPs) [^1] byte addressable. Thus if you wanted to make a bit-field, to pack bools as tight as possible, how would you do so?

How do you mutate a single bit in C?



## Simple Bool

```c
#include <stdbool.h>

int main(int argc, const char *argv[])
{
	bool anInt = false;
	anInt = true;
	return 0;
}
```

Plug this into [Compiler Explorer]()

{{< figure src="/img/bit-bool/simple-bit-bool.png" title="Compiler Explorer Simple Bool" >}}

We can see the source lines 5, and 6 correspond to just two instructions, lines 6 and 7 in in the output assembly. 

Let's compare this, the simplest case to manual bit masking

# Manual Bit Masking

```c
#include <stdio.h>

int main(int argc, const char *argv[])
{
	int anInt = 0;

	anInt = anInt ^ 0b1;

	return 0;
}
```

Outputs 
```shell
➜  clang -std=c11 bitmask.c # Add a printf to get output. Leave it out to get simpler assembly
➜  ./a.out
2
```


Again inspect the assembly with Compiler Explorer[^2]
{{< figure src="/img/bit-bool/bit-mask.png" title="Compiler Explorer Bit Mask" >}}

Notice again how simple the instructions are. The corresponding mutation (grey lines) are short and single instruction. Now let's try to make a fully packed bool, using all 8 bits independently addressable.
# C BitFields and Unions to preserve space
```c
#include <stdio.h>

#pragma pack(1)
typedef struct _bitfield {
	int one:1;
	int two:1;
	int three:1;
	int four:1;
	int five:1;
	int six:1;
	int seven:1;
	int eight:1;
} bitfield;

typedef union _asInt {
	int asInt;
	bitfield asField;
} BitFieldAsInt;


int main(int argc, const char *argv[])
{
	BitFieldAsInt field;
	field.asInt = 0;

	field.asField.two = 1; 

	//printf("%X\n", field.asInt);
	return 0;
}

```

Again compare in compiler explorer
{{< figure src="/img/bit-bool/fully-packed.png" title="Compiler Explorer Fully Packed bitfield" >}}

Notice the source line 8. Here you can see it or's a 2.  This is the compiler recognizing we are trying to mutate a single bit. We did an assignment and the compiler changed this to an ``or`` instruction. However, even though the compiler recognized our assignment can be implemented as an ``or``, it still takes three instructions to do the same and the previous examples. Thus by trying to save space, we are causing the CPU to work more performing extra instructions. 

# Well, why isn't the computer bit addressable then?

The short answer, bit access isn't that common, thus the hardware is optimized for the more common access of bytes. Although due to various levels of cache and the time required to pull objects from different levels of the memory hierarchy (e.g. CPU caches, Main Memory, Durable Storage, Network, etc), multiple blocks of memory are pulled at a time.

A related question is "what does 64-bit computing mean?"

{{< figure src="/img/bit-bool/64bit-meme.jpg" title="64-bit Compute Meme" >}}

The more detailed answer comes from understanding that 64-bit computing means. 

Now consider that bool by default stored only 1 bit (instead of a byte). The apocryphal story of "...640KB is enough for everybody..."[^3] is also related to this point...addressable memory.

You may remember when 32-bit addresses were common. Before that computers were 16-bit and even 8-bit addressable. Many microcontrollers (the things that make your fridge and oven work) are still 8-bit. It's all that needed for those use cases. What this means that given an memory address, how many bytes will be pulled from main memory? This is a hardware level concept. Literally there are ~64 individual wires on the board. These wires signal a stream of bits ``0b0111010101...`` to the RAM. The RAM returns the values represented by that address. 

> Thus, the maximum amount of addressable memory is bounded by the size of the address. In 32 bits, this was 4GB. 

$$2^{32} = 4294967296$$
$$ 4294967296 / 2^{30} = 4 GB $$

In 64 bits, 
$$2^{64} = 18446744073709551615 bytes$$ 
$$2^{64} / 2^{50} = 16384 Petabytes $$

If instead we decided that each address represented a single bit, in order to get even 4 GB from our 32-bit computing days we'd need CPUs with  35-bit computers

$$ (2^{35} / 8) / 2^{30} = 4GB $$

Thus making a bit addressable memory, requires more hardware. However are those resources worthwhile? It's all about access patterns. How is most memory utilized? Again it largely depends on the domain, which is why some processors have special addressing modes. However on most computing, we want to fetch large blocks of time to amortize the cost of fetching from the next level in the memory cache. "Paying" the time to fetch from the next physical location with wasteful for single bits. 


# References

[^1]: Microchip. _dsPIC33F/PIC24H Data Memory_. http://ww1.microchip.com/downloads/en/DeviceDoc/70202C.pdf
[^2]: You can generate the assembly yourself with your own compiler using the ``-S`` option ``➜  clang -std=c11 -S bitmask.c``
[^3]: Katz, Jon. _Did Gates Really Say 640K is Enough For Anyone?_ https://www.wired.com/1997/01/did-gates-really-say-640k-is-enough-for-anyone/