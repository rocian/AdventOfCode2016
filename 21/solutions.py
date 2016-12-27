#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 21: Scrambled Letters and Hash ---

The computer system you're breaking into uses a weird scrambling function to
store its passwords. It shouldn't be much trouble to create your own scrambled
password so you can add it to the system; you just have to implement the
scrambler.

The scrambling function is a series of operations (the exact list is provided in
your puzzle input). Starting with the password to be scrambled, apply each
operation in succession to the string. The individual operations behave as
follows:

    swap position X with position Y means that the letters at indexes X and Y
    (counting from 0) should be swapped.

    swap letter X with letter Y means that the letters X and Y should be swapped
    (regardless of where they appear in the string).

    rotate left/right X steps means that the whole string should be rotated; for
    example, one right rotation would turn abcd into dabc.

    rotate based on position of letter X means that the whole string should be
    rotated to the right based on the index of letter X (counting from 0) as
    determined before this instruction does any rotations. Once the index is
    determined, rotate the string to the right one time, plus a number of times
    equal to that index, plus one additional time if the index was at least 4.

    reverse positions X through Y means that the span of letters at indexes X
    through Y (including the letters at X and Y) should be reversed in order.

    move position X to position Y means that the letter which is at index X
    should be removed from the string, then inserted such that it ends up at
    index Y.

For example, suppose you start with abcde and perform the following operations:

    swap position 4 with position 0 swaps the first and last letters, producing
    the input for the next step, ebcda.

    swap letter d with letter b swaps the positions of d and b: edcba.

    reverse positions 0 through 4 causes the entire string to be reversed,
    producing abcde.

    rotate left 1 step shifts all letters left one position, causing the first
    letter to wrap to the end of the string: bcdea.

    move position 1 to position 4 removes the letter at position 1 (c), then
    inserts it at position 4 (the end of the string): bdeac.

    move position 3 to position 0 removes the letter at position 3 (a), then
    inserts it at position 0 (the front of the string): abdec.

    rotate based on position of letter b finds the index of letter b (1), then
    rotates the string right once plus a number of times equal to that index
    (2): ecabd.

    rotate based on position of letter d finds the index of letter d (4), then
    rotates the string right once, plus a number of times equal to that index,
    plus an additional time because the index was at least 4, for a total of 6
    right rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the
system. Given the list of scrambling operations in your puzzle input, what is
the result of scrambling abcdefgh?

--- Part Two ---

You scrambled the password correctly, but you discover that you can't actually
modify the password file on the system. You'll need to un-scramble one of the
existing passwords by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?

"""

import re

op = {'mov': re.compile(r"move position (\d+) to position (\d+)"),
      'rev': re.compile(r"reverse positions (\d+) through (\d+)"),
      'rotate b': re.compile(r"rotate (based) on position of letter (.)"),
      'rotate l': re.compile(r"rotate (left) (\d+) step.*"),
      'rotate r': re.compile(r"rotate (right) (\d+) step.*"),      
      'swap l': re.compile(r"swap letter (.) with letter (.)"),
      'swap p': re.compile(r"swap position (\d+) with position (\d+)")}


def opmove(string, pos1, pos2, reverse=False):

    if reverse:
        return(opmove(string, pos2, pos1))
    
    first = int(pos1)
    second = int(pos2)

    if first > second:
        # print("s = string[0:second] + string[second+1:first+1] + string[second] + string[first+1:]")
        # print("first={}, second={}".format(first,second))
        s = string[0:second] + string[first] + string[second:first] + string[first+1:]        
    else:
        s = string[0:first] + string[first+1:second+1] + string[first] + string[second+1:]
        
    return(s)

def opreverse(string, pos1, pos2, reverse=False):
    first = int(pos1)
    second = int(pos2)

    if first > second:
        f = first
        first = second
        second = f    

    r = string[first:second+1]
    r = r[::-1]
    s = string[0:first] + r + string[second+1:]
    return(s)


def oprotate_based(string, pos1, pos2, reverse=False):
    second = string.find(pos2)
    if reverse:
        if second == 0:
            return(oprotate_left(string, "", "1"))
        if second == 2:
            return(oprotate_right(string, "",  "2"))
        if second == 4:
            return(oprotate_right(string, "",  "1"))        
        if second % 2 == 1:
            return(oprotate_left(string, "",  str(int((second-1)/2)+1)))

        return(string)
    else:
        if second > 3:
            second += 1
        second += 1
        second = second % len(string)
        return(oprotate_right(string, "", str(second)))


def oprotate_left(string, pos1, pos2, reverse=False):
    if reverse:
        return(oprotate_right(string, pos1, pos2))
    
    second = int(pos2)
    return(string[second:] + string[:second])


def oprotate_right(string, pos1, pos2, reverse=False):
    if reverse:
        return(oprotate_left(string, pos1, pos2))
    
    second = int(pos2)
    second = second % len(string)
    return(oprotate_left(string, "", str(-second)))

def opswap_letter(string, pos1, pos2, reverse=False):
    first = string.find(pos1)
    second = string.find(pos2)

    if first > second:
        f = first
        first = second
        second = f
        
    s = string[0:first] + string[second] + string[first+1:second] + string[first] + string[second+1:]
    return(s)


def opswap_position(string, pos1, pos2, reverse=False):
    first = int(pos1)
    second = int(pos2)

    if first > second:
        f = first
        first = second
        second = f
        
    s = string[0:first] + string[second] + string[first+1:second] + string[first] + string[second+1:]
    return(s)

execop = {'mov': opmove,
          'rev': opreverse, 
          'rotate b': oprotate_based,
          'rotate l': oprotate_left,
          'rotate r': oprotate_right,
          'swap l': opswap_letter,
          'swap p': opswap_position}

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


def process(instruction, operations, string):
    """Process the instructions."""

    for opc in operations:
        if instruction.startswith(opc):
            mrx = re.search(operations[opc], instruction)
            (op1, op2) = mrx.groups(0)
            return(execop[opc](string, op1, op2))


    return(None)

def descramble(password, instructions, operations):
    instr = instructions.copy()
    instr.reverse()

    start = password
    
    for instruction in instr:
        for opc in operations:
            if instruction.startswith(opc):
                mrx = re.search(operations[opc], instruction)
                (op1, op2) = mrx.groups(0)
                start = execop[opc](start, op1, op2, reverse=True)

    return(start)

start = "abcdefgh"

string = start
instructions = read_input()
for i in instructions:
    string = process(i, op, string)

password = "fbgdceah"

descrambled = descramble(password, instructions, op)


"""
# a = "*-------"

# for i in range(0,8):
#     q = oprotate_right(a, "", str(i))
#     f = oprotate_based(q, "based", "*")
#     print(q+"  ->  "+f)

studio for reverse of rotate based
*-------  ->  -*------
-*------  ->  ---*----
--*-----  ->  -----*--
---*----  ->  -------*
----*---  ->  --*-----
-----*--  ->  ----*---
------*-  ->  ------*-
-------*  ->  *-------

if i 0
old pos = len
if i odd
old pos = (i-1)/2
else
old pos = (i+len)/2 - 1
"""
    
print("Day 21. Solution of part 1: {}".format(string))
print("Day 21. Solution of part 2: {}".format(descrambled))
