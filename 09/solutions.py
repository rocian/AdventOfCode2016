#!/usr/bin/env python3
"""

https://adventofcode.com/2016

--- Day 9: Explosives in Cyberspace ---

Wandering around a secure area, you come across a datalink port to a new part of
the network. After briefly scanning it for interesting files, you find one file
in particular that catches your attention. It's compressed with an experimental
format, but fortunately, the documentation for the format is nearby.

The format compresses a sequence of characters. Whitespace is ignored. To
indicate that some sequence should be repeated, a marker is added to the file,
like (10x2). To decompress this marker, take the subsequent 10 characters and
repeat them 2 times. Then, continue reading the file after the repeated
data. The marker itself is not included in the decompressed output.

If parentheses or other characters appear within the data referenced by a
marker, that's okay - treat it like normal data, not a marker, and then resume
looking for markers after the decompressed section.

For example:

    ADVENT contains no markers and decompresses to itself with no changes,
    resulting in a decompressed length of 6.

    A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a
    decompressed length of 7.

    (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.

    A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a
    decompressed length of 11.

    (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but
    because it's within a data section of another marker, it is not treated any
    differently from the A that comes after it. It has a decompressed length of
    6.

    X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of
    18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is
    skipped and not processed further.

What is the decompressed length of the file (your puzzle input)? Don't count
whitespace.

--- Part Two ---

Apparently, the file actually uses version two of the format.

In version two, the only difference is that markers within decompressed data are
decompressed. This, the documentation explains, provides much more substantial
compression capabilities, allowing many-gigabyte files to be stored in only a
few kilobytes.

For example:

    (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no
    markers.

    X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed data
    from the (8x2) marker is then further decompressed, thus triggering the
    (3x3) marker twice for a total of six ABC sequences.

    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated
    241920 times.

    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445
    characters long.

Unfortunately, the computer you brought probably doesn't have enough memory to
actually decompress the file; you'll have to come up with another way to get its
decompressed length.

What is the decompressed length of the file using this improved format?

"""


def read_input():
    """ This function read the compressed string from the input file and
    return a clean string without space."""

    f = open('input', 'r')
    string = f.read()
    string = string.replace("\n", "").replace(" ", "")
    return(string)


def count_decompress(strarg):
    """Count size of decompressed strarg."""

    index = 0
    count = 0
    while index < len(strarg):
        # find the first occurence of `(` `)` and `x` within the two
        start = strarg[index:].find('(')
        end = strarg[index:].find(')')
        timesp = strarg[index:].find('x')

        # grab the two int of the form (NxM)
        if (start >= 0) & (end >= 0) & (timesp >= 0):
            N = int(strarg[index + start + 1:index + timesp])
            M = int(strarg[index + timesp + 1:index + end])

            # add the len of string before marker
            count += len(strarg[index:index + start])

            # add the decompressed len
            count += len(strarg[index + end + 1:index + N + end + 1] * M)

            # move index at the end of mark
            index = index + end + N + 1
        else:
            count += len(strarg[index:])
            index = len(strarg)
    return(count)


def count_decompress2(strarg):
    """Count size of decompressed strarg."""

    index = 0
    count = 0
    while index < len(strarg):
        # find the first occurence of `(` `)` and `x` within the two
        start = strarg[index:].find('(')
        end = strarg[index:].find(')')
        timesp = strarg[index:].find('x')

        # grab the two int of the form (NxM)
        if (start >= 0) & (end >= 0) & (timesp >= 0):
            N = int(strarg[index + start + 1:index + timesp])
            M = int(strarg[index + timesp + 1:index + end])

            # add the len of string before marker
            count += len(strarg[index:index + start])

            # add the decompressed len
            count += count_decompress2(strarg[index + end + 1:index + N + end + 1]) * M

            # move index at the end of mark
            index = index + end + N + 1
        else:
            count += len(strarg[index:])
            index = len(strarg)
    return(count)


#  Test function for debug purpose
def decompress(strarg):
    """Decompress strarg."""

    index = 0
    result_string = ""
    while index < len(strarg):
        # find the first occurence of `(` `)` and `x` within the two
        start = strarg[index:].find('(')
        end = strarg[index:].find(')')
        timesp = strarg[index:].find('x')

        # grab the two int of the form (NxM)
        if (start >= 0) & (end >= 0) & (timesp >= 0):
            N = int(strarg[index + start + 1:index + timesp])
            M = int(strarg[index + timesp + 1:index + end])

            # add the string before marker to result_string
            result_string += strarg[index:index + start]

            # add decompressed strarg
            result_string += strarg[index + end + 1:index + N + end + 1] * M

            # move index at the end of mark
            index = index + end + N + 1
        else:
            result_string += strarg[index:]
            index = len(strarg)
    return(result_string)

string = read_input()

print("Day 9. Solution of part 1: {}".format(count_decompress(string)))
print("Day 9. Solution of part 2: {}".format(count_decompress2(string)))
