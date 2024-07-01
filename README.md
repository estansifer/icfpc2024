# Panicked Albatross -- icfpc2024

We are a two person team working in Python and C

## lambdaman

The idea here is to use a random number generator to generate the list of
directions for lambdaman to move in.  By trying a bunch of seeds, we can find
either a seed which generates a solution directly, or, failing that, a seed that
gets lambdaman as close to solving the maze as possible.  In the latter case, we
find a new best seed for the next sequence of moves, and so on.

To encode a list of seeds, there are two strategies used.  The first generates
an expression like f(seed1) @ f(seed2) @ f(seed3) ..., which has some overhead
for the repeated references to f and concatenation operations.  The second
creates a function which can be called with each seed in sequence, like
f(seed1)(seed2)(seed3)....  To end the sequence, a terminator value different
from any seed is picked.  The fixed overhead of this mechanism is higher, but it
scales better to large numbers of seeds.

## spaceship

The most interesting thing here is the distance() function, which determines how
many steps it takes to get from one point to another with a given starting
velocity.  The insight is that all points between the curve of constant
acceleration and the curve of constant deceleration are accessible.  Both of
these curves are parabolas, so you can solve a quadratic equation to find the
accessible ranges -- then intersect them to find the minimum point that's in
both the x range and the y range.

From there, the code does a greedy search using a weighted combination of this
distance function and the simple manhattan distance function that ignores
velocity.  It could probably be improved by separating route planning and
velocity management.  As-is, the code simply accelerates to get to the next
point as soon as it can.

## sine function

While maybe not the best use of time for getting a good standing overall, I made
it a mission to have the smallest volume entry that computes sine, ultimate getting
down to 21978 -- about double the size of my factorial implementation! I'll break
down how it works.

First, how do we compute sine? We use a truncated Taylor series:

    sin(x) = x - x^3 / 3! + x^5 / 5! - x^7 / 7! + ...

which, if x = A / F for integer A and a large constant F = 10^9,

    F * sin(x) = A - A^3 / 3! / F^2 + ...

[I explored a variety of alternative approaches for calculating sine but the final
version used the most obvious one!]

To compute each term, we need to compute A^n, F^n, and n!, each of which can be done
iteratively. I first implemented the sine calculator in python to verify that it
was computing the correct result, designed to mimic what the 3d code was doing, and
verified it gave the same answers as my simulation of the 3d code also:

    def sin(A, F = 10 ** 9):
        a = 1       # n + 1 (iteration counter)
        b = 1       # A^n
        c = 1       # F, after the first iteration
        d = 1       # F^(n - 1)
        e = 1       # n!
        f = 0       # accumulator
        g = 0       # other accumulator

        while a <= 20:
            f, g = g, b * (-17) // (e * d) - f
            e = a * e
            d = c * d
            c = F
            b = A * b
            a = a + 1

        return g // 17

Note that I compute both odd and even terms, but by switching accumulators every
iteration all the odd terms go into one accumulator and all the even terms go into the
other; thus we are computing both sine and cosine. This was an accidental innovation
that *also* means that by subtracting the accumulator I get alternating + and -
automatically. Previously I was computing (n % 2) * ((n % 4) - 2) to get signs, which
was space consuming, time consuming, and meant I needed more copies of n to be updated.

Note that computing F is non-trivial (we can't put in literals bigger than 99).

Here are each of the pieces.

Compute 1000000000 (c := 1000000000):

     . 25  .  .  .  .
    40  *  .  >  .  .
     .  .  *  .  *  .
     .  .  .  .  .  .
     .  .  .  9  @  8
     .  .  .  .  3  .

Hard-code several answers (saved almost 2000 volume!):

     .  A
     1  =
     .  S

     .  .
     .  A
     0  =
     .  S
     .  .
     .  A
    -1  =
     .  S

Compute factorial (e := a * e):

    a  >  .  .  .  .  .
    .  .  *  .  .  .  .
    .  ^  .  >  .  .  .
    .  e  .  3  @  0  .
    .  .  .  .  3  .  .

I have labelled a, b, c, d, e, f, g the appropriate cells. In the actual
submission those were replaced with a = b = c = d = e = 1 and f = g = 0.

Increment a (a := a + 1):

    .  .  1  .  .  <  a
    .  .  #  .  +  .  .
    .  ^  .  .  3  >  .
    .  7  . -2  @  3  v
    .  .  .  .  .  <  .

The part at left is to delay the + being triggered so that the
answer is not pulled away by the >.

Check for completion:

    . 20  .  .  .  .  .
    .  =  .  >  .  .  .
    ^  .  .  6  @ -10 .
    a  .  .  .  3  .  .

Compute F^(n - 1) (d := c * d):

    .  .  .  <  .  <  d
    .  c  *  .  .  .  .
    .  .  .  .  .  .  .
    . -4  @  3  .  .  .
    .  .  3  .  .  .  .

Accumulator (g := b * (-17) // (e * d) - f):

    .  .  .  e  .  .  .
    .  .  d  *  .  .  .
    . -17 .  .  .  f  .
    b  *  .  /  .  -  .
    .  .  .  .  .  .  .
    .  .  .  .  8  @ -4
    .  .  .  .  .  3  .

Swap accumulator, and output (f := g):

    .  .  .  .  .
    .  .  >  .  /
    .  ^  .  v  S
    .  g  .  .  .
    .  . -6  @  8
    .  .  >  .  .
    .  ^  .  .  .
    .  .  .  .  .
    .  ^  .  .  .
    .  3  .  .  .

Compute A^n (b := A * b):

    b  .  .  .
    v  .  .  .
    .  >  .  .
    .  A  *  .
    .  .  .  .
    .  2  @  .
    .  .  3  ^
    .  5  >  .

Note depending on which iteration you output modulo 4, you will get
either sine, cosine, -sine, or -cosine.

All together:

    .  .  .  .  .  .  .  .  .  .  .  .  .
    .  .  .  .  .  .  . 20  .  .  .  .  .
    .  .  .  A  .  .  .  =  .  >  .  .  .
    .  .  1  =  .  .  ^  .  .  6  @ -10 .
    .  .  1  S  .  <  a  >  .  .  3  .  .
    .  .  #  .  +  .  .  .  *  .  .  .  .
    .  ^  .  .  3  >  .  ^  .  >  .  .  .
    .  7  . -2  @  3  v  e  .  3  @  0  .
    .  .  .  <  .  <  d  *  .  .  3  A  .
    .  c  *  .  . -17 .  .  .  f  0  =  .
    .  .  .  .  b  *  .  /  .  -  .  S  .
    . -4  @  3  v  .  .  .  .  .  .  .  .
    .  .  3  .  .  >  .  .  8  @ -4  A  .
    .  .  .  .  .  A  * 25  .  3 -1  =  .
    .  .  >  .  /  . 40  *  .  >  .  S  .
    .  ^  .  v  S  2  @  .  *  .  *  .  .
    .  g  .  .  .  .  3  ^  .  .  .  .  .
    .  . -6  @  8  5  >  .  .  9  @  8  .
    .  .  .  3  .  .  .  .  .  .  3  .  .
    .  .  .  .  .  .  .  .  .  .  .  .  .
