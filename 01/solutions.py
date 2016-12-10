#!/usr/bin/env python3
"""

https://adventofcode.com/2016

--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the
clock's oscillator is regulated by stars. Unfortunately, the stars have been
stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve
all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near",
unfortunately, is as close as you can get - the instructions on the Easter Bunny
Recruiting Document the Elves intercepted start here, and nobody had time to
work them out further.

The Document indicates that you should start at the given coordinates (where you
just landed) and face North. Then, follow the provided sequence: either turn
left (L) or right (R) 90 degrees, then walk forward the given number of blocks,
ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you
take a moment and work out the destination. Given that you can only walk on the
street grid of the city, how far is the shortest path to the destination?

For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is
               2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.

How many blocks away is Easter Bunny HQ?

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting
Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you
visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?

"""

walk = 0
direction = 1j
firstcross = None
points = []


def read_input():
    f = open('input', 'r')
    string = f.read()
    f.close()
    return(string.replace('\n', '').replace(' ', '').split(","))


# http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C):
    return (C.imag - A.imag) * (B.real - A.real) > (B.imag - A.imag) * (C.real - A.real)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def iscrossing(a, b, direc, poin):
    if (len(poin) < 3):
        return(None)

    for i in range(0, len(poin) - 2):
        z1 = poin[i]
        z2 = poin[i + 1]

        if intersect(a, b, z1, z2):
            if a.real == b.real:
                intersection = a.real + z1.imag * 1j
            else:
                intersection = z1.real + a.imag * 1j
            return (intersection)

    return(None)


instruction = read_input()

for i in instruction:
    turn = i[0]
    if turn == 'L':
        mult = -1j
    else:
        mult = 1j
        direction *= mult

    oldwalk = walk
    walk += direction * int(i[1:])

    if firstcross is None:
        firstcross = iscrossing(oldwalk, walk, direction, points)

    points.append(walk)

print("Day 1. Solution of part 1: {}".format(int(abs(walk.real) + abs(walk.imag))))
print("Day 1. Solution of part 2: {}".format(int(abs(firstcross.real) + abs(firstcross.imag))))
