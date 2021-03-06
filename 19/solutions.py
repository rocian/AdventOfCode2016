#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 19: An Elephant Named Joseph ---

The Elves contact you over a highly secure emergency channel. Back at the North
Pole, the Elves are busy misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with
position 1. Then, starting with the first Elf, they take turns stealing all the
presents from the Elf to their left. An Elf with no presents is removed from the
circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3

    Elf 1 takes Elf 2's present.
    Elf 2 has no presents and is skipped.
    Elf 3 takes Elf 4's present.
    Elf 4 has no presents and is also skipped.
    Elf 5 takes Elf 1's two presents.
    Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
    Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all the
presents.

With the number of Elves given in your puzzle input, which Elf gets all the
presents?

Your puzzle input is 3005290.

--- Part Two ---

Realizing the folly of their present-exchange rules, the Elves agree to instead
steal presents from the Elf directly across the circle. If two Elves are across
the circle, the one on the left (from the perspective of the stealer) is stolen
from. The other rules remain unchanged: Elves with no presents are removed from
the circle entirely, and the other elves move in slightly to keep the circle
evenly spaced.

For example, with five Elves (again numbered 1 to 5):

    The Elves sit in a circle; Elf 1 goes first:

      1
    5   2
     4 3

    Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the
    one to the left. Elf 3 leaves the circle, and the rest of the Elves move in:

      1           1
    5   2  -->  5   2
     4 -          4

    Elf 2 steals from the Elf directly across the circle, Elf 5:

      1         1
    -   2  -->     2
      4         4

    Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

     -          2
        2  -->
     4          4

    Finally, Elf 2 steals from Elf 4:

     2
        -->  2
     -

So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input, which Elf now gets all the presents?

Your puzzle input is still 3005290.

"""

start = 3005290

# For part 1
c = list(range(1, start + 1))

while len(c) > 1:
    while (len(c) % 2 == 0) and (len(c) > 1):
        c = c[::2]

    while (len(c) % 2 == 1) and (len(c) > 1):
        c = c[::2]
        _ = c.pop(0)

# c[0] contains the solution of part 1


# For part 2
d = list(range(1, start + 1))

while len(d) > 1:
    while (len(d) % 2 == 0) and (len(d) > 2):
        a = d[len(d) // 2 + 2::3]
        k = (d.index(a[-1]) + 3) % len(d)
        b = d[k:len(d) // 2 + 2:3]
        d = b + a

    while (len(d) % 2 == 1) and (len(d) > 2):
        a = d[len(d) // 2 + 1::3]
        k = (d.index(a[-1]) + 3) % len(d)
        b = d[k:len(d) // 2 + 1:3]
        d = b + a

    if len(d) == 2:
        _ = d.pop(1)

# d[0] contains the solution of part 2

print("Day 19. Solution of part 1: {}".format(c[0]))
print("Day 19. Solution of part 2: {}".format(d[0]))
