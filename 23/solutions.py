#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's
private office is here, complete with a safe hidden behind a painting, and who
wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry. A sticky note attached
to the safe has a password hint on it: "eggs". The painting is of a large rabbit
coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display; instead,
the keypad comes apart in your hands, apparently having been smashed. Behind it
is some kind of socket - one that matches a connector in your prototype
computer! You pull apart the smashed keypad and extract the logic circuit, plug
it into your computer, and plug your computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the
safe. You extract the assembunny code from the logic chip (your puzzle input).

The code looks like it uses almost the same architecture and instruction set
that the monorail computer used! You should be able to use the same assembunny
interpreter for this as you did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like jnz does:
positive means forward; negative means backward):

    For one-argument instructions, inc becomes dec, and all other one-argument
    instructions become inc.

    For two-argument instructions, jnz becomes cpy, and all other
    two-instructions become jnz.

    The arguments of a toggled instruction are not affected.

    If an attempt is made to toggle an instruction outside the program, nothing
    happens.

    If toggling produces an invalid instruction (like cpy 1 2) and an attempt is
    later made to execute that instruction, skip it instead.

    If tgl toggles itself (for example, if a is 0, tgl a would target itself and
    become inc a), the resulting instruction is not executed until the next time
    it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

    cpy 2 a initializes register a to 2.

    The first tgl a toggles an instruction a (2) away from it, which changes the
    third tgl a into inc a.

    The second tgl a also modifies an instruction 2 away from it, which changes
    the cpy 1 a into jnz 1 a.

    The fourth line, which is now inc a, increments a to 3.

    Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions
    ahead, skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number of eggs,
7) in register a, run the code, and then send the value left in register a to
the safe.

What value should be sent to the safe?

--- Part Two ---

The safe doesn't open, but it does make several angry noises to express its
frustration.

You're quite sure your logic is working correctly, so the only other thing
is... you check the painting again. As it turns out, colored eggs are still
eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to
overheat. You wonder what's taking so long, and whether the lack of any
instruction more powerful than "add one" has anything to do with it. Don't
bunnies usually multiply?

Anyway, what value should actually be sent to the safe?

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


def opchange(instruction, pc, a):
    npc = pc + a
    try:
        opv = instruction[npc].split(" ")
        if len(opv) == 2:
            if opv[0] == 'inc':
                opv[0] = 'dec'
            else:
                opv[0] = 'inc'
        else:
            if opv[0] == 'jnz':
                opv[0] = 'cpy'
            else:
                opv[0] = 'jnz'

        instruction[npc] = " ".join(opv)
    except:
        pass
        
            
def process(instruction, r={}):
    """Process the instructions."""

    register = {'a':0,'b':0,'c':0,'d':0,'e':0, 'pc':0}

    # get register values from argument
    for i in r.keys():
        register[i] = r[i]
    # s = 0
    while register['pc'] in range(0,len(instruction)):

        operation = instruction[register['pc']]

        opcode, *op = operation.split(" ")
                    
        if op[0] in register.keys():
            opv = int(register[op[0]])
        else:
            opv = int(op[0])

        try :
            if op[1] in register.keys():
                opw = int(register[op[1]])
            else:
                opw = int(op[1])
        except:
            pass
            
        if opcode == 'cpy':
            register[op[1]] = opv
        elif opcode == 'inc':
            register[op[0]] += 1
        elif opcode == 'mul':
            register[op[0]] = (register[op[0]] + register[op[1]]) * register[op[2]]
        elif opcode == 'add':
            register[op[0]] += register[op[1]]             
        elif opcode == 'nop':
            pass
        elif opcode == 'tgl':
            opchange(instruction, register['pc'], register[op[0]])            
        elif opcode == 'dec':
            register[op[0]] -= 1                
        elif opcode == 'jnz':
            if opv != 0:
                register['pc'] += opw -1

        register['pc'] += 1

    return(register['a'])



instructions = read_input()

print("Day 23. Solution of part 1: {}".format(process(instructions, r={'a':7})))

instructions = read_input()
instructions[13] = 'add c d'
instructions[14] = 'cpy 0 d'
instructions[5] = 'mul a c d'
instructions[6] = 'cpy 0 c'
instructions[8] = 'cpy 0 d'

print("Day 23. Solution of part 2: {}".format(process(instructions, r={'a':12})))
