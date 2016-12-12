#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small
microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two
microchips, and once it does, it gives each one to a different bot or puts it in
a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single
number; the bots must use some logic to decide what to do with each chip. You
access the local control computer and download the bots' instructions (your
puzzle input).

Some of the instructions specify that a specific-valued microchip should be
given to a specific bot; the rest of the instructions indicate what a given bot
should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

    Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2
    chip and a value-5 chip.
    Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and
    its higher one (5) to bot 0.
    Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and
    gives the value-3 chip to bot 0.
    Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in
    output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a
value-2 microchip, and output bin 2 contains a value-3 microchip. In this
configuration, bot number 2 is responsible for comparing value-5 microchips with
value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible
for comparing value-61 microchips with value-17 microchips?

--- Part Two ---

What do you get if you multiply together the values of one chip in each of
outputs 0, 1, and 2?

"""

import re


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


def opappend(lis, value):
    "Append value to list lis if lis has less then 2 items."
    if len(lis) < 2:
        lis.append(value)


def dooperation(otype, params, sbot, sobin, num1, num2, nubot, doing_op):
    "Do operation otype with `params` using bot `sbot` and output `sobin`.
    If a bot compare the two values `num1` and `num2` save the bot index in
    nubot. If no operation is done leave doing_op unchanged.
    Return (doing_op, nubot)."

    if otype.startswith("input"):
        # operation of type input
        microchip, bot_or_bin, index = params
        if bot_or_bin == 'bot':
            lout = sbot
        else:
            lout = sobin

        opappend(lout[int(index)], int(microchip))

    elif otype.startswith("bot"):
        # operation of type bot
        bot, lbot_or_bin, ilow, hbot_or_bin, ihigh = params

        if lbot_or_bin == 'bot':
            lout = sbot
        else:
            lout = sobin

        if hbot_or_bin == 'bot':
            hout = sbot
        else:
            hout = sobin

        if (len(sbot[int(bot)])) < 2:
            # if bot has less than 2 items do noting
            return(doing_op, nubot)
        
        
        if (num1 in sbot[int(bot)]) & (num2 in sbot[int(bot)]):
            nubot = int(bot)
            
        if int(sbot[int(bot)][0]) <= int(sbot[int(bot)][1]):
            opappend(lout[int(ilow)], sbot[int(bot)][0])
            opappend(hout[int(ihigh)], sbot[int(bot)][1])
        else:
            opappend(lout[int(ilow)], sbot[int(bot)][1])
            opappend(hout[int(ihigh)], sbot[int(bot)][0])
        sbot[int(bot)] = []

    return(True, nubot)


def process(instruction, num1, num2):
    """Process the instructions oand monitor bot that confront num1 and num2."""

    # create the opportune regex to capture instruction of operation
    inbin = re.compile(r"value (\d+) goes to (\w+) (\d+)")
    botop = re.compile(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")

    # during first pass we fill the bot
    # after we don't need to fill them
    first_pass = True

    # we stop when don't have any more transfers
    doing_op = True

    # we want to kno wich bot confront num1 and num2
    nubot = None
    nofbot = 230
    sbot = [[] for x in range(nofbot)]
    sobin = [[] for x in range(nofbot)]
    while doing_op:
        doing_op = False

        for operation in instruction:

            if operation.startswith("value") & first_pass:
                matres = re.findall(inbin, operation)[0]
                doing_op, nubot = dooperation("input", matres, sbot, sobin, num1, num2, nubot, doing_op)
                
            elif operation.startswith("bot"):
                matres = re.findall(botop, operation)[0]
                doing_op, nubot = dooperation("bot", matres, sbot, sobin, num1, num2, nubot, doing_op)
        if first_pass:
            first_pass = False
            doing_op = True
    # return which bot perform confront of num1 and num2 and the multiplied contents
    # of the first 3 value in the output
    return(nubot,sobin[0][0] * sobin[1][0] * sobin[2][0])


micro1 = 17
micro2 = 61
sol1, sol2 = process(read_input(), micro1, micro2)
print("Day 10. Solution of part 1: {}".format(sol1))
print("Day 10. Solution of part 2: {}".format(sol2))
