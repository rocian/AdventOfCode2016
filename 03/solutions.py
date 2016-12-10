#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways
and office furniture that makes up this part of Easter Bunny HQ. This must be a
graphic design department; the walls are covered in specifications for
triangles.

Or are they?

The design document gives the side lengths of each triangle it describes,
but... 5 10 25? Some of these aren't triangles. You can't help but mark the
impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining
side. For example, the "triangle" given above is impossible, because 5 + 10 is
not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you
that triangles are specified in groups of three vertically. Each set of three
numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds
digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed
triangles are possible?

"""


def read_input():
    "Read all rows of input file as tuple of three numbers."
    f = open('input', 'r')
    alltern = [line.strip().split() for line in f]
    f.close()
    return(alltern)


def process(tern):
    "Return the number of rows that can be interpreted three side of a triangle"
    num = 0
    for a, b, c in tern:
        a = int(a)
        b = int(b)
        c = int(c)
        if ((a + b) > c) & ((a + c) > b) & ((b + c) > a):
            num += 1
    return (num)


def quasitranspose(l):
    "Transpose the tuple of three number. And stack them again in group of three."
    t = []
    for i in zip(*l):
        for k in range(0, len(i), 3):
            t.append(list(i)[k:k + 3])
    return(t)

# list of numbers
l = read_input()
# list of numbers transposed
t = quasitranspose(l)

# Number of triangle by rows
print("Day 3. Solution of part 1: {}".format(process(l)))
# Number of triangle by columns
print("Day 3. Solution of part 2: {}".format(process(t)))
