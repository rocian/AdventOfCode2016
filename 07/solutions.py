#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to
figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An
ABBA is any four-character sequence which consists of a pair of two different
characters followed by the reverse of that pair, such as xyyx or abba. However,
the IP also must not have an ABBA within any hypernet sequences, which are
contained by square brackets.

For example:

    abba[mnop]qrst supports TLS
     (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS
     (bddb is within square brackets, even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS
     (aaaa is invalid; the interior characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS
     (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?

--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the
supernet sequences (outside any square bracketed sections), and a corresponding
Byte Allocation Block, or BAB, anywhere in the hypernet sequences. An ABA is any
three-character sequence which consists of the same character twice with a
different character between them, such as xyx or aba. A corresponding BAB is the
same characters but in reversed positions: yxy and bab, respectively.

For example:

    aba[bab]xyz supports SSL
     (aba outside square brackets with corresponding bab within square brackets).
    xyx[xyx]xyx does not support SSL
     (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL
     (eke in supernet with corresponding kek in hypernet;
      the aaa sequence is not related, because the interior character must
      be different).
    zazbz[bzb]cdb supports SSL
     (zaz has no corresponding aza, but zbz has a corresponding bzb,
       even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?

"""

import re
# (?=...) is a lookahead assertion:
# Matches but doesn’t consume any part of the string.
# In this way we can handle overlapping match


def read_input():
    "Read all rows as a list of encrypted rooms."
    f = open('input', 'r')
    string = f.read()
    f.close()
    # remove the last void one
    # (it can be better than this)
    return(string.split("\n")[:-1])


def count_abba(l):
    "Return number of ABBA ip."
    count = 0

    for ip in l:
        supernet = re.findall(r"(.*?)(?:\[.*?\]|$)", ip)
        hypernet = re.findall(r"\[([^\]]+)\]", ip)

        rf = False
        for first in supernet:
            # handle overlapping match
            grf = re.findall(r"(?=(.)(.)\2\1)", first)
            # It is true only if the two group are there and are different
            for i in grf:
                if i[0] != i[1]:
                    rf = True

        rh = False
        for second in hypernet:
            # handling overlapping match
            grh = re.findall(r"(?=(.)(.)\2\1)", second)
            # It is true only if the two group are there and are different
            for i in grh:
                if i[0] != i[1]:
                    rh = True

        # It is an ABBA only if ABBA is in supernet part and not in
        # hypernet
        if (rf & (not rh)):
            count += 1
    return(count)


def count_ssl(l):
    "Return number of SSL ip."
    count = 0

    for ip in l:
        supernet = re.findall(r"(.*?)(?:\[.*?\]|$)", ip)
        hypernet = re.findall(r"\[([^\]]+)\]", ip)
        rf = False

        for first in supernet:
            # handle overlapping match
            grf = re.findall(r"(?=(.)(.)\1)", first, flags=0)
            # It is true only if the two group are there and are different
            for i in grf:
                if i[0] != i[1]:

                    for second in hypernet:
                        ssl = "".join([i[1], i[0], i[1]])
                        grh = re.findall(ssl, second, flags=0)
                        for k in grh:
                            rf = True

        # It is an SSL only if ABA is in supernet part and BAB in hypernet
        if rf:
            count += 1
    return(count)


l = read_input()
print("Day 7. Solution of part 1: {}".format(count_abba(l)))
print("Day 7. Solution of part 2: {}".format(count_ssl(l)))
