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

# complex variable containing the point where you are
# as if you where in a complex world.
# Obviously your first position is the origin of the complex plane (0,0j) i.e. 0
walk = 0

# As requested you start are facing north i.e. 1j direction
direction = 1j

# In the second part we need to store the first time we cross our walk. Before
# calculating it, it is None
firstcross = None

# To solve the second part of this puzzle we need to store locations. We
# choose to store them as list of points in the complex plane.
points = []


def read_input():
    """ This function read the instruction from the input file and
    return a clean list of instruction. Each elements of the returned
    list is of the form Dn, where D is one of L,R (turn left right) and
    n is the number of block to walk."""

    f = open('input', 'r')
    string = f.read()
    f.close()

    # we need to remove space and carriage return to clean the input list
    return(string.replace('\n', '').replace(' ', '').split(","))


# To following two function resolve a general problem on the intersection
# of two segments.
# The actual problem is simpler and this approach may be too general.
# Anyway it doesn't cost too much in terms of computation and we
# can accept this solution.
#
# More info on this algorithm on
# http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C):
    """With three points A, B and C. If the slope of
    the line AB is less than the slope of the line AC then the three points are
    listed in a counter-clockwise order."""

    return (C.imag - A.imag) * (B.real - A.real) > (B.imag - A.imag) * (C.real - A.real)


def intersect(A, B, C, D):
    """ Return true if line segments AB and CD intersect """
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def iscrossing(a, b, poin):
    """This function returns the point of intersection of the segment ab with
    previous segments of the walk (vertex of walk are in the list poin).
    It returns None if there were non intersection."""

    # if there are not enough points it is impossible that we can have
    # an intersection
    # (even if returning back on our own step could be interpreted as an intersection)
    if (len(poin) < 3):
        return(None)

    # for each segment of our walk we check for an intersection
    # This seems very intensive as computation, but we can trust
    # the puzzle introduction, that says that the intersection happens
    # early in our walk.
    for i in range(0, len(poin) - 2):
        z1 = poin[i]
        z2 = poin[i + 1]

        if intersect(a, b, z1, z2):
            # if the segment intersects, then
            if a.real == b.real:
                # or last segment is horizontal (and its counterpart vertical)
                intersection = a.real + z1.imag * 1j
            else:
                # or last segment is vertical (and its counterpart horizontal)
                intersection = z1.real + a.imag * 1j
            return (intersection)

    return(None)

# we read all instruction and place them in a list
instruction = read_input()

for i in instruction:
    # turn instruction is the first char
    turn = i[0]
    if turn == 'L':
        # left is a ccw turn, i.e. a multiplication by -j
        mult = -1j
    else:
        # right is a cw turn, i.e. a multiplication by j
        mult = 1j
        # the new direction is a multiplication of the new
        # turn direction with the old one
        direction *= mult

    # we need to preserve the old point to calculate the last segment
    # of walk
    oldwalk = walk
    # then we reach a new point
    walk += direction * int(i[1:])

    # if we have already calculated the first intersection we don't need
    # to calculate the new ones.
    if firstcross is None:
        firstcross = iscrossing(oldwalk, walk, points)

    # anyway we store in the points list the new vertex of our walk
    points.append(walk)

# the last walk point contains the Manhattan distance from our starting point
print("Day 1. Solution of part 1: {}".format(int(abs(walk.real) + abs(walk.imag))))
# the value of firstcross is the first points of intersection
print("Day 1. Solution of part 2: {}".format(int(abs(firstcross.real) + abs(firstcross.imag))))
