#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 17: Two Steps Forward ---

You're trying to access a secure vault protected by a 4x4 grid of small rooms
connected by doors. You start in the top-left room (marked S), and you can
access the vault (marked V) once you reach the bottom-right room:

#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |
####### V

Fixed walls are marked with #, and doors are marked with - or |.

The doors in your current room are either open or closed (and locked) based on
the hexadecimal MD5 hash of a passcode (your puzzle input) followed by a
sequence of uppercase characters representing the path you have taken so far (U
for up, D for down, L for left, and R for right).

Only the first four characters of the hash are used; they represent,
respectively, the doors up, down, left, and right from your current
position. Any b, c, d, e, or f means that the corresponding door is open; any
other character (any number or a) means that the corresponding door is closed
and locked.

To access the vault, all you need to do is reach the bottom-right room; reaching
this room opens the vault and all doors in the maze.

For example, suppose the passcode is hijkl. Initially, you have taken no steps,
and so your path is empty: you simply find the MD5 hash of hijkl alone. The
first four characters of this hash are ced9, which indicate that up is open (c),
down is open (e), left is open (d), and right is closed and locked (9). Because
you start in the top-left corner, there are no "up" or "left" doors to be open,
so your only choice is down.

Next, having gone only one step (down, or D), you find the hash of hijklD. This
produces f2bc, which indicates that you can go back up, left (but that's a
wall), or right. Going right means hashing hijklDR to get 5745 - all doors
closed and locked. However, going up instead is worthwhile: even though it
returns you to the room you started in, your path would then be DU, opening a
different set of doors.

After going DU (and then hashing hijklDU to get 528e), only the right door is
open; after going DUR, all doors lock. (Fortunately, your actual passcode is not
hijkl).

Passcodes actually used by Easter Bunny Vault Security do allow access to the
vault if you know the right path. For example:

    If your passcode were ihgpwlah, the shortest path would be DDRRRD.
    With kglvqrro, the shortest path would be DDUDRLRRUDRD.
    With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.

Given your vault's passcode, what is the shortest path (the actual path, not
just the length) to reach the vault?

Your puzzle input is udskfozm.

--- Part Two ---

You're curious how robust this security solution really is, and so you decide to
find longer and longer paths which still provide access to the vault. You
remember that paths always end the first time they reach the bottom-right room
(that is, they can never pass through it, only end in it).

For example:

    If your passcode were ihgpwlah, the longest path would take 370 steps.
    With kglvqrro, the longest path would be 492 steps long.
    With ulqzkmiv, the longest path would be 830 steps long.

What is the length of the longest path that reaches the vault?

Your puzzle input is still udskfozm.

"""


import hashlib


def md5hash(s):
    "MD5 of string s, hex lowercase output."
    return(hashlib.md5(s.encode('utf-8')).hexdigest())


def is_path(path, starthash, XYmax):
    """Check if the path writthen as starthash followed by one or more U D L R is a
    path, that is to say follow the rule of the maze, don't go through wall,
    pass through open door, reach the goal of the (3, 3) vault position. Returns
    0 if reach the vault, 1 if is a path, -1 if it stops on walls.

    """

    # get the direction instructions from path
    followed = path[len(starthash):]

    # starting position
    x, y = (0, 0)

    # delta based on direction
    dxy = {'U': (0, -1), 'D': (0, 1), 'R': (1, 0), 'L': (-1, 0)}

    for direction in followed:

        dx, dy = dxy[direction]
        x += dx
        y += dy

        if (x < 0) or (y < 0) or (x >= XYmax) or (y >= XYmax):
            # it is outside maze
            return(-1)

        if (x == (XYmax - 1)) and (y == (XYmax - 1)):
            # it reaches the vault
            return(0)

    # otherwise is a standard path
    return(1)


def get_newhash(hash, basehash, XYmax):
    """Get new direction from here as a path."""

    # all possible direction
    dirvalue = ['U', 'D', 'L', 'R']

    # we can follow the direction if the relativa hash char
    # is one of the following
    hashok = ['b', 'c', 'd', 'e', 'f']
    result = []

    # get first 4 char from MD5 hash
    directions = md5hash(hash)[0:4]

    for i in range(0, len(directions)):
        if directions[i] in hashok:
            # got a direction
            newdirection = hash + dirvalue[i]

            if is_path(newdirection, basehash, XYmax) >= 0:
                # the direction may be followed
                result.append(hash + dirvalue[i])

    return(result)


def get_shortest(hash, XYmax):
    """Return the shortest path to the vault as a string of directions.  Starting
    from the shortest path (no move), whe add all possible directions and stop
    when we reach the vault. As we start from the shortest path and increase the
    new one, the first founded path to the vault is the shortest.

    """

    queue = [hash]
    newhash = queue.pop(0)

    while is_path(newhash, hash, XYmax) != 0:

        vertex = get_newhash(newhash, hash, XYmax)
        if len(vertex) > 0:
            queue = queue + vertex

        # We don't assume that the maze has a solution
        # so if we have not yet find a solution and there aren't other
        # path to explore we stop
        if len(queue) == 0:
            return(None)

        newhash = queue.pop(0)

    return(newhash[len(hash):])


def get_longest_len(hash, XYmax):
    """Return the len of the longest path to te vault."""

    queue = [hash]
    result = 0

    while queue:
        newhash = queue.pop(0)
        value = is_path(newhash, hash, XYmax)

        if value == 0:
            # it is a path to the vault
            # we get the longest len between
            # this one and the previous
            result = max(result, len(newhash) - len(hash))

        if value > 0:
            # if the new vertex are possible path
            # we explore them
            vertex = get_newhash(newhash, hash, XYmax)
            if len(vertex) > 0:
                queue = queue + vertex

    return(result)

# start hash
shash = "udskfozm"

# number of rows and cols in the maze
xymax = 4

shortest = get_shortest(shash, xymax)
longestlen = get_longest_len(shash, xymax)

print("Day 17. Solution of part 1: {}".format(shortest))
print("Day 17. Solution of part 2: {}".format(longestlen))
