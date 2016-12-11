#!/usr/bin/env python3
"""

https://adventofcode.com/2016

--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an
implementation of two-factor authentication after a long game of requirements
telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a
nearby desk). Then, it displays a code on a little screen, and you type that
code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken
everything apart and figured out how it works. Now you just have to work out
what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for
the screen; these instructions are your puzzle input. The screen is 50 pixels
wide and 6 pixels tall, all of which start off, and is capable of three somewhat
peculiar operations:

    rect AxB turns on all of the pixels in a rectangle at the top-left of the
    screen which is A wide and B tall.

    rotate row y=A by B shifts all of the pixels in row A (0 is the top row)
    right by B pixels. Pixels that would fall off the right end appear at the
    left end of the row.

    rotate column x=A by B shifts all of the pixels in column A (0 is the left
    column) down by B pixels. Pixels that would fall off the bottom appear at
    the top of the column.

For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel,
    causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

As you can see, this display technology is extremely powerful, and will soon
dominate the tiny-code-displaying-screen market. That's what the advertisement
on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display:
after you swipe your card, if the screen did work, how many pixels should be
lit?

--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the
font it uses, each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?

"""

import re
import numpy as np


def read_input():
    """ This function read the instruction from the input file and
    return a clean list of instruction."""

    f = open('input', 'r')
    string = f.read()

    lstring = string.split("\n")
    # we remove the last void instruction
    # this could be made in a safer way
    lstring = lstring[:-1]

    return(lstring)


def array_roll(a, index, by, axis):
    "Roll array row/coll by specified amount by."

    if axis:
        # if move by columns axis = 1, transpose array
        a = np.transpose(a)

    # roll row of `by` position
    a[index] = np.roll(a[index], by)

    if axis:
        # if move by columns axis = 1, transpose again array
        a = np.transpose(a)

    return(a)


def process(monitor, instruction):
    """Process the instructions on the monitor and return the final monitor state."""

    # create the opportune regex to capture instruction of operation
    rect = re.compile(r"(\d+)x(\d+)")
    rowr = re.compile(r"y=(\d+) by (\d+)")
    colr = re.compile(r"x=(\d+) by (\d+)")

    for operation in instruction:
        if operation.startswith("rect"):
            # fill rect dx x dy with 1
            dx, dy = re.findall(rect, operation)[0]
            monitor[0:int(dy), 0:int(dx)] = 1

        elif operation.startswith("rotate column"):
            # roll column `index` by `dy`
            index, dy = re.findall(colr, operation)[0]
            monitor = array_roll(monitor, int(index), int(dy), 1)

        elif operation.startswith("rotate row"):
            # roll row `index` by `dx`
            index, dx = re.findall(rowr, operation)[0]
            monitor = array_roll(monitor, int(index), int(dx), 0)

    return(monitor)


def to_shape(monitor, nrow, ncol, by, voidc, fillc):
    "Create shape letters from array"
    # add 0 filled column to space letters
    for c in range(ncol - by, 0, -by):
        monitor = np.insert(monitor, c, 0, axis=1)
        # replace 0 by `voidc` and 1 by `fillc`
        # to iter tranform in a list and then agai in ndarray
    monitor = [fillc if i else voidc for i in np.nditer(monitor, op_flags=['readwrite'])]
    monitor = np.array(monitor).reshape(nrow, len(monitor) // nrow)

    # create a string from array
    string = "\n\n\t"
    for row in monitor:
        string += ''.join(row)
        string += "\n\t"
    return(string)

# number of rows and columns in monitor
nrow = 6
ncol = 50

# number of columns in a letter block
nby = 5

# chars for void and fill in a letter block
voidc = ' '
fillc = '█'  # Unicode FULL BLOCK

# create the monitor as array
monitor = [0] * (nrow * ncol)
monitor = np.array(monitor).reshape(nrow, ncol)

# process instructions
monitor = process(monitor, read_input())

print("Day 8. Solution of part 1: {}".format(sum(sum(monitor))))
print("Day 8. Solution of part 2: {}".format(to_shape(monitor, nrow, ncol,
                                                      5, voidc, fillc)))
