#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away from you
for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere near the
North Pole, much too far to deliver these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the
sleigh doesn't need the stars, exactly; it needs the timing data they provide,
and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the
antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and quickly
explain the situation. "I'm not sure what kind of equipment you have connected
over there," he says, "but you need a clock signal." You try to explain that
this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how
to read the data you're sending it. An endless, alternating pattern of 0, 1, 0,
1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need
to use for the data from the stars. "There's no way it can! The only antenna
we've installed capable of that is on top of a top-secret Easter Bunny
installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your
puzzle input); it looks mostly compatible with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

    out x transmits x (either an integer or the value of a register) as the next
    value for the clock signal.

The code takes a value (via register a) that describes the signal to generate,
but you're not sure how it's used. You'll have to find the input to produce the
right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a
and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?

--- Part Two ---

The antenna is ready. Now, all you need is the fifty stars required to generate
the signal for the sleigh, but you don't have enough.

You look toward the sky in desperation... suddenly noticing that a lone star has
been installed at the top of the antenna! Only 49 more to go.

If you like, you can

[retransmit the signal]


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
        
            
def process(instruction, maxloop=10, r={}):
    """Process the instructions."""

    register = {'a':0,'b':0,'c':0,'d':0,'e':0, 'pc':0}

    result = [0,1]
    
    # get register values from argument
    for i in r.keys():
        register[i] = r[i]
    # s = 0
    stop = False
    
    while (register['pc'] in range(0,len(instruction))) and (not stop):

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
        elif opcode == 'out':
            result.append(register[op[0]])            
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

        if (len(result) > maxloop) or (result[-1] == result[-2]):
            stop = True
        
    return("".join([str(x) for x in result[2:]]))



instructions = read_input()
found = False
aforsig = 0
maxloop = 100
tocheck = '01'*maxloop
while not found:
    res = process(instructions, maxloop=maxloop, r={'a':aforsig})
    if res == tocheck[:maxloop-1]:
        found = True
    else:
        aforsig += 1
        
print("Day 25. Solution of part 1: {}".format(aforsig))
print("Day 25. Solution of part 2: {}".format(aforsig))

