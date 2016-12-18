#!/usr/bin/env python3
"""

https://adventofcode.com/2016

--- Day 5: How About a Nice Game of Chess? ---

You are faced with a security door designed by Easter Bunny engineers that seem
to have acquired most of their security knowledge by watching hacking movies.

The eight-character password for the door is generated one character at a time
by finding the MD5 hash of some Door ID (your puzzle input) and an increasing
integer index (starting with 0).

A hash indicates the next character in the password if its hexadecimal
representation starts with five zeroes. If it does, the sixth character in the
hash is the next character of the password.

For example, if the Door ID is abc:

    The first index which produces a hash that starts with five zeroes is
    3231929, which we find by hashing abc3231929; the sixth character of the
    hash, and thus the first character of the password, is 1.  5017308 produces
    the next interesting hash, which starts with 000008f82..., so the second
    character of the password is 8.  The third time a hash starts with five
    zeroes is for abc5278568, discovering the character f.

In this example, after continuing this search a total of eight times, the
password is 18f47a30.

Given the actual Door ID, what is the password?

Your puzzle input is ojvtpuvg.

--- Part Two ---

As the door slides open, you are presented with a second door that uses a
slightly more inspired security mechanism. Clearly unimpressed by the last
version (in what movie is the password decrypted in order?!), the Easter Bunny
engineers have worked out a better solution.

Instead of simply filling in the password from left to right, the hash now also
indicates the position within the password to fill. You still look for hashes
that begin with five zeroes; however, now, the sixth character represents the
position (0-7), and the seventh character is the character to put in that
position.

A hash result of 000001f means that f is the second character in the
password. Use only the first result for each position, and ignore invalid
positions.

For example, if the Door ID is abc:

    The first interesting hash is from abc3231929, which produces 0000015...;
    so, 5 goes in position 1: _5______.  In the previous method, 5017308
    produced an interesting hash; however, it is ignored, because it specifies
    an invalid position (8).  The second interesting hash is at index 5357525,
    which produces 000004e...; so, e goes in position 4: _5__e___.

You almost choke on your popcorn as the final character falls into place,
producing the password 05ace8e3.

Given the actual Door ID and this new method, what is the password? Be extra
proud of your solution if it uses a cinematic "decrypting" animation.

Your puzzle input is still ojvtpuvg.

"""


import hashlib

ststring = "ojvtpuvg"


def md5_input(s):
    "MD5 of string s, hex lowercase output."
    return(hashlib.md5(s.encode('utf-8')).hexdigest())


def get_password(s):
    "Return password as requested by part 1 method."
    finished = 0
    index = 0
    password = []
    while finished < 8:
        md5 = md5_input(s + str(index))
        if md5[0:5] == "00000":
            password.append(md5[5])
            finished += 1
        index += 1

    return "".join(password)


def get_password2(s):
    "Return password as requested by part 2 method."
    finished = 0
    index = 0
    password = list('_' * 8)
    verstring = list('01234567')
    while finished < 8:
        md5 = md5_input(s + str(index))
        if md5[0:5] == "00000":
            position = md5[5]

            if position in verstring:
                password[int(position)] = md5[6]
                verstring.remove(position)
                finished += 1

        index += 1

    return "".join(password)

# Password from hashing of input method 1
print("Day 5. Solution of part 1: {}".format(get_password(ststring)))
# Password from hashing of input method 2
print("Day 5. Solution of part 2: {}".format(get_password2(ststring)))
