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

from sys import stdin

# complex variable containing the point where you are
# as if you where in a complex world.
# Obviously your first position is the origin of the complex plane (0,0j) i.e. 0
# As requested you start are facing north i.e. 1j direction
direction = 1j

# and you have not yet walked
walk = 0

# In the second part we need to store the first time we cross our walk. Before
# calculating it, it is None
firstcross = None

# To solve the second part of this puzzle we need to store locations. We
# choose to store them as list of points in the complex plane.
points = []


def read_input():  # fname):
    """ This function read the instruction from the input file and
    return a clean list of instruction. Each elements of the returned
    list is of the form Dn, where D is one of L,R (turn left right) and
    n is the number of block to walk."""

    # we need to remove space and carriage return to clean the input list
    instructions = stdin.read().strip().replace(' ', '').split(",")
    return(instructions)


# The following two function resolve a general problem on the intersection
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
    #
    #   (1)                  (2)
    #
    #    D                    D
    #    |                    |
    # A--+--B    or   A-----B |
    #    |                    |
    #    C                    C
    #
    # In the first case (the two segments intersect) the two couple of
    # three-points ([ACD,BCD] and [ABC,ABD]) have not the same sign of
    # orientation, one is ccw the other is not. In the second case (the two
    # segments doesn't have intersection), the couple of three points has the
    # same sign of orientation. Notice that all the possible cases can be
    # obtained for simmetry by exchanging the segment vertex.
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def iscrossing(A, B, points):
    """This function returns the point of intersection of the segment ab with
    previous segments of the walk (vertex of walk are in the list points).
    It returns None if there were non intersection."""

    # if there are not enough points it is impossible that we can have an
    # intersection (even if returning back on our own step could be interpreted
    # as an intersection, but we can turn only R or L so we need at least 3
    # turns to intersect our own walk).
    if (len(points) < 3):
        return(None)

    # for each segment of our walk we check for an intersection
    # This seems very intensive as computation, but we can trust
    # the puzzle introduction, that says that the intersection happens
    # early in our walk.
    segments = [(points[i], points[i + 1]) for i in range(len(points) - 2)]
    for C, D in segments:
        if intersect(A, B, C, D):

            # (not (xa - xb) * xa)  is  xa if xa == xb
            cross = ((not (A.real - B.real)) * A.real +
                     (not (A.imag - B.imag)) * A.imag +
                     (not (C.real - D.real)) * C.real +
                     (not (C.imag - D.imag)) * C.imag)

            return (cross)

    return(None)

# we read all instruction and place them in a list
instruction = read_input()

# left is a ccw turn, i.e. a multiplication by -j
# right is a cw turn, i.e. a multiplication by j
turn = {'L': -1j, 'R': 1j}

for i in instruction:

    # calculate the new direction
    direction *= turn[i[0]]

    # we need to preserve the old point to calculate the last segment
    # of walk
    oldpoint = walk

    # then we reach a new point
    walk += direction * int(i[1:])

    # if we have already calculated the first intersection we don't need
    # to calculate the new ones.
    if firstcross is None:
        firstcross = iscrossing(oldpoint, walk, points)

    # anyway we store in the points list the new vertex of our walk
    points.append(walk)

# the last walk point contains the Manhattan distance from our starting point
print("Day 1. Solution of part 1: {}".format(int(abs(walk.real) + abs(walk.imag))))
# the value of firstcross is the first points of intersection
print("Day 1. Solution of part 2: {}".format(int(abs(firstcross.real) + abs(firstcross.imag))))
