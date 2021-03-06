#Implementing The Art of Computer Programming algorithms

##Rationale

I've recently started reading The Art of Computer Programming (TAoCP for short), and one of the things that struck me is how the algorithms are presented. 
In the 3rd edition, they are written in MIX, a pseudo-assembly, low-level language. 
I find it hard to wrap my head around how an algorithm *actually works* by staring at jump instructions and register arithmetic.

So I decided to implement the algorithms in a higher-level language - Python to start with. I may also use this exercise as a way to learn new languages... We'll see how that goes.

##Coding style

The original algorithms do not always lend themselves readily to a Pythonic coding style.
Where possible, I try to use idiomatic Python. However, sometimes it's necessary to stay close to the original code structure, which implies `while True` loops and juggling with counters.
However, I draw the line at using `goto` statements (good thing Python doesn't have them).

##Completeness

I don't plan to implement all of the algorithms in TAoCP. Some (not that many!) are too simple to warrant writing them again. 
Some algorithms make heavy use of MIX concepts which don't really make sense in Python, such as pointer manipulation. 
And some are huge, intimidating beasts that I don't think I can tackle comfortably with the limited time I've allocated to this project (elevator simulation, I'm looking at you).
