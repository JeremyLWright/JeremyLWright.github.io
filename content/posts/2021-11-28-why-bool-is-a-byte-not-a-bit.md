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


Now consider that bool by default stored only 1 bit (instead of a byte). This means that all your code the compiler generates MUST do bit masking. The extra bytes are fetched anyway because the hardware is word oriented and byte addressable. This the CPU cannot even fetch a single bit from the memory even if it wanted to. So, the CPU fetches extra bytes, performs masking, mutates the bool, puts all the bytes back. All ready that sounds like extra work just to "save" three bits of memory per bool. So the wasted space is actually performing a value. Its offloading space for time. It's "wasting" a little space in order to save A LOT of time.

But the time argument gets even worse!

CPU's pipeline (hyper-thread is and example of Intel's branded style of this) The most expensive thing is when a pipeline has to stall waiting for a fetch from main memory (or a write conflict). Now consider the following code;

bool one;

bool two;

one = true;

two = false;

Consider bool is 1-bit (in order to save the most amount of space), now one and two are sharing the same addressable memory (they are both in a single byte). Thus the write to two MUST wait for the write to one. If you are in a multi-core environment, the caches for each CPU stall in order to assure that one finishes before two (because the store of two will affect the store of one)

Now, consider instead each are in separate addressable sections. one and two could be written at the same time because each is independently addressable!

# References

[^1]: Microchip. _dsPIC33F/PIC24H Data Memory_. http://ww1.microchip.com/downloads/en/DeviceDoc/70202C.pdf
[^2]: You can generate the assembly yourself with your own compiler using the ``-S`` option ``➜  clang -std=c11 -S bitmask.c``