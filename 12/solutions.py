#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass
ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt
some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a
collection of buildings in the nearby area. They're all connected by a local
monorail, and there's another building not far from here! Unfortunately, being
night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot
sequence expects a password. The password-checking logic (your puzzle input) is
easy to extract, but the code it uses is strange: it's assembunny code designed
for the new computer you just assembled. You'll have to execute the code and get
the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d)
that start at 0 and can hold any integer. However, it seems to make use of only
a few instructions:

    cpy x y copies x (either an integer or the value of a register) into
            register y.
    inc x increases the value of register x by one.
    dec x decreases the value of register x by one.
    jnz x y jumps to an instruction y away (positive means forward; negative
            means backward), but only if x is not zero.

The jnz instruction moves relative to itself: an offset of -1 would continue at
the previous instruction, while an offset of 2 would skip over the next
instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2, decrease its
value by 1, and then skip the last dec a (because a is not zero, so the jnz a 2
skips it), leaving register a at 42. When you move past the last instruction,
the program halts.

After executing the assembunny code in your puzzle input, what value is left in
register a?

--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't start;
register c needs to be initialized to the position of the ignition key.

If you instead initialize register c to be 1, what value is now left in register
a?

"""

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


def process(instruction, r={}):
    """Process the instructions."""

    register = {'a':0,'b':0,'c':0,'d':0,'e':0, 'pc':0}

    # get register values from argument
    for i in r.keys():
        register[i] = r[i]
        
    while register['pc'] in range(0,len(instruction)):

        operation = instruction[register['pc']]
        opcode, *op = operation.split(" ")
                    
        if op[0] in register.keys():
            opv = int(register[op[0]])
        else:
            opv = int(op[0])
            
        if opcode == 'cpy':
            register[op[1]] = opv
        elif opcode == 'inc':
            register[op[0]] += 1
        elif opcode == 'dec':
            register[op[0]] -= 1                
        elif opcode == 'jnz':
            if opv != 0:
                register['pc'] += int(op[1]) -1

        register['pc'] += 1

    return(register['a'])


print("Day 12. Solution of part 1: {}".format(process(read_input())))
print("Day 12. Solution of part 2: {}".format(process(read_input(),r={'c':1})))

