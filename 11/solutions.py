#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 11: Radioisotope Thermoelectric Generators ---

You come upon a column of four floors that have been entirely sealed off from
the rest of the building except for a small dedicated lobby. There are some
radiation warnings and a big sign which reads "Radioisotope Testing Facility".

According to the project status board, this facility is currently being used to
experiment with Radioisotope Thermoelectric Generators (RTGs, or simply
"generators") that are designed to be paired with specially-constructed
microchips. Basically, an RTG is a highly radioactive rock that generates
electricity through heat.

The experimental RTGs have poor radiation containment, so they're dangerously
radioactive. The chips are prototypes and don't have normal radiation shielding,
but they do have the ability to generate an elecromagnetic radiation shield when
powered. Unfortunately, they can only be powered by their corresponding RTG. An
RTG powering a microchip is still dangerous to other microchips.

In other words, if a chip is ever left in the same area as another RTG, and it's
not connected to its own RTG, the chip will be fried. Therefore, it is assumed
that you will follow procedure and keep chips connected to their corresponding
RTG when they're in the same room, and away from other RTGs otherwise.

These microchips sound very interesting and useful to your current activities,
and you'd like to try to retrieve them. The fourth floor of the facility has an
assembling machine which can make a self-contained, shielded computer for you to
take with you - that is, if you can bring it all of the RTGs and microchips.

Within the radiation-shielded part of the facility (in which it's safe to have
these pre-assembly RTGs), there is an elevator that can move between the four
floors. Its capacity rating means it can carry at most yourself and two RTGs or
microchips in any combination. (They're rigged to some heavy diagnostic
equipment - the assembling machine will detach it for you.) As a security
measure, the elevator will only function if it contains at least one RTG or
microchip. The elevator always stops on each floor to recharge, and this takes
long enough that the items within it and the items on that floor can irradiate
each other. (You can prevent this if a Microchip and its Generator end up on the
same floor in this way, as they can be connected while the elevator is
recharging.)

You make some notes of the locations of each component of interest (your puzzle
input). Before you don a hazmat suit and start moving things around, you'd like
to have an idea of what you need to do.

When you enter the containment area, you and the elevator will start on the
first floor.

For example, suppose the isolated area has the following arrangement:

The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.

As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L for
Lithium, M for Microchip, and G for Generator), the initial state looks like
this:

F4 .  .  .  .  .
F3 .  .  .  LG .  
F2 .  HG .  .  .  
F1 E  .  HM .  LM 

Then, to get everything up to the assembling machine on the fourth floor, the
following steps could be taken:

    Bring the Hydrogen-compatible Microchip to the second floor, which is safe
    because it can get power from the Hydrogen Generator:

    F4 .  .  .  .  .
    F3 .  .  .  LG .
    F2 E  HG HM .  .
    F1 .  .  .  .  LM

    Bring both Hydrogen-related items to the third floor, which is safe because
    the Hydrogen-compatible microchip is getting power from its generator:

    F4 .  .  .  .  .
    F3 E  HG HM LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  LM

    Leave the Hydrogen Generator on floor three, but bring the
    Hydrogen-compatible Microchip back down with you so you can still use the
    elevator:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 E  .  HM .  .
    F1 .  .  .  .  LM

    At the first floor, grab the Lithium-compatible Microchip, which is safe
    because Microchips don't affect each other:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 .  .  .  .  .
    F1 E  .  HM .  LM

    Bring both Microchips up one floor, where there is nothing to fry them:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 E  .  HM .  LM
    F1 .  .  .  .  .

    Bring both Microchips up again to floor three, where they can be temporarily
    connected to their corresponding generators while the elevator recharges,
    preventing either of them from being fried:

    F4 .  .  .  .  .
    F3 E  HG HM LG LM
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Microchips to the fourth floor:

    F4 E  .  HM .  LM
    F3 .  HG .  LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Leave the Lithium-compatible microchip on the fourth floor, but bring the
    Hydrogen-compatible one so you can still use the elevator; this is safe
    because although the Lithium Generator is on the destination floor, you can
    connect Hydrogen-compatible microchip to the Hydrogen Generator there:

    F4 .  .  .  .  LM
    F3 E  HG HM LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Generators up to the fourth floor, which is safe because you can
    connect the Lithium-compatible Microchip to the Lithium Generator upon
    arrival:

    F4 E  HG .  LG LM
    F3 .  .  HM .  .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring the Lithium Microchip with you to the third floor so you can use the
    elevator:

    F4 .  HG .  LG .
    F3 E  .  HM .  LM
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Microchips to the fourth floor:

    F4 E  HG HM LG LM 
    F3 .  .  .  .  .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

In this arrangement, it takes 11 steps to collect all of the objects at the
fourth floor for assembly. (Each elevator stop counts as one step, even if
nothing is added to or removed from it.)

In your situation, what is the minimum number of steps required to bring all of
the objects to the fourth floor?

"""

# Puzzle generalization
#
# Suppose that we have an number N of element X each as Generator XG and as
# Microchip XM. Without loosing generalities we can choose an order for thes
# couple of elements in order to see each Generator just befor the same element
# Microchip: ... XG XM YG YM ...  before these we put the elevator E
# E ... XG XM YG YM ... In this way each floor is a binary number (N+1 bits)
# with a 1 specifing the presence of the generators or microchips, based on its
# position.
#
# If M is the number of floors we have M*(N+1) bits specifing each state.
# But not all the state are possible:
#
# Each state must have on each floor (rule 0):
#    - zero, or more Microchip only if the corrispettive Generators, or no
#      Generators at all are present.
#
# Each state is a M slot of (N+1) bit and the possible subsequent state can be
# obtained by subtracting (N+1) bit (H) in one of the slot (there is no carry) and
# adding to one of the adiacent slot, and verifying that all the slot follow the
# rule 0.
#

sign = lambda a: int((a > 0) - (a < 0))


def check_rule0(state, N, M):
    '''Each state must have on each floor (rule 0):
        - zero, or more Microchip only if the corrispettive Generators, or no
          Generators at all are present.
    '''

    s = state

    # generator and microchip mask
    # without elevator bit
    genmask = 0
    micmask = 0
    #
    for i in range(1, N + 1, 2):
        genmask += 2**(i - 1)
        micmask += 2**(i)

    # for all floor
    for i in range(0, M):

        s = s >> (i * (N + 1))
        mask = (1 << (N + 1)) - 1

        status = (s & mask)

        # all generator
        # excluding the elevator bit
        gen = (status >> 1) & genmask

        # if there are no generators at all
        # then the state is compatible with rule 0
        if gen == 0:
            continue

        # all microchip
        # excluding the elevator bit
        mic = (status >> 1) & micmask

        # if there are no microchip at all
        # then the state is compatible with rule 0
        if mic == 0:
            continue

        # if there is some generator and some
        # microchip we verify than they are coupled
        #
        # G.G...  >>   .G.G..
        #                      AND = .M.M..
        # .M.M..       .M.M..
        #
        coupled = (gen << 1) & mic
        if coupled != mic:
            return (False)

    return (True)


def generate_all_move(N):
    H = set()
    H.add(3)
    for i in range(1, N):
        for j in range(0, N):
            elem = (2**(i - 1) + 2**j) * 2 + 1
            H.add(elem)

    H = sorted(H)
    return(H)


# Now we start from a base state and generate all possible state
# by starting from the base one made of all 1 in floor 0 and
# all 0 in all other floor and applying all possible move H.
# This is a set of ordered tuple

# first we create two comodity function
def link_add(sset, first, second):
    "Add the the tuple (first, second) to set sset, with the tuple ordered."

    if first < second:
        sset.add((first, second))
    else:
        sset.add((second, first))


def base_move(base, m, fl, N, M):
    """Create a new state from base, applying m and verifyng
    that the new state follow rule 0."""

    # first of all we check that is there
    # another floor in the direction of move
    newfl = fl + sign(m)
    if (newfl > M) or (newfl < 0):
        return (False)

    # then we check that the starting status has elevator
    # and all generators and microchip that we are going to
    # move
    mask = 2**(fl * (N + 1)) * int(abs(m))
    if (mask & base) != mask:
        return (False)

    # then we prepare mask 2 for the requested move
    mask2 = int(2**((fl + sign(m)) * (N + 1)) * int(abs(m)))

    # apply the move
    newbase = (base ^ mask) | mask2

    if check_rule0(newbase, N=N, M=M):
        return(newbase)

    return(False)


def generate_all(mstart, H, N, M):
    """Generate all states and link starting from mstart by applying
    all possible moves in H."""

    # all linked states
    sstates = set()

    # all states that need to be visited
    slink = set()

    # all states
    alllink = set()

    # we start from state mstart
    base = mstart

    slink.add(base)
    alllink.add(base)
    while len(slink) > 0:

        base = slink.pop()

        # apply each possible move on
        for m in H:

            # each possible floor
            for i in range(0, M):

                newbase = base_move(base, m, i, N, M)
                if newbase:
                    if newbase not in alllink:
                        slink.add(newbase)
                        alllink.add(newbase)
                    link_add(sstates, base, newbase)

                newbase = base_move(base, -m, i, N, M)
                if newbase:
                    if newbase not in alllink:
                        slink.add(newbase)
                        alllink.add(newbase)
                    link_add(sstates, base, newbase)

    return(sstates)


# then we generate the graf from the edge
def generate_graph(data):
    "Generate graph from edges in data as tuple."

    graph = {}

    for row in data:
        if row[0] in graph.keys():

            graph[row[0]].add(row[1])

            if row[1] not in graph.keys():
                graph[row[1]] = set()
                graph[row[1]].add(row[0])

            else:
                graph[row[1]].add(row[0])

        else:

            graph[row[0]] = set()
            graph[row[0]].add(row[1])

            if row[1] not in graph.keys():
                graph[row[1]] = set()
                graph[row[1]].add(row[0])

            else:
                graph[row[1]].add(row[0])

    return(graph)


# breath depth
def bfs_paths(graph, start, goal):

    queue = [(start, [start])]
    while queue:

        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]

            else:
                queue.append((next, path + [next]))


def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


# comodity
def int_from_conf(string):
    "Generate integer from configuration map"

    s = string.split("\n")
    final = ['0', 'b']

    for flo in s:
        templ = []

        for n in range(0, len(flo) - 1, 3):

            if flo[n:n + 3] == ' . ':
                templ.append('0')
            elif flo[n:n + 3] == ' _ ':
                templ.append('0')
            else:
                templ.append('1')

        templ.reverse()
        final += templ

    return(int(''.join(final), 2))


# split list in chunks
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# configuration map from int
def conf_from_int(number, N, M):

    ordstart = 65
    composer = []
    result = list(bin(number)[2:])

    # we need N+1*M bits
    padd = (N + 1) * M - len(result)
    composer = ['0'] * padd + result

    templ = []
    for flo in chunks(composer, N + 1):
        for n in range(0, len(flo) - 1):
            if flo[n] == '1':
                if n % 2 != 0:
                    templ.append('G' + chr(ordstart + (n - 1) // 2) + ' ')
                else:
                    templ.append('M' + chr(ordstart + n // 2) + ' ')
            else:
                templ.append(' . ')

        if flo[-1] == '1':
            templ.append(' E ')
        else:
            templ.append(' _ ')
        templ.append('\n')
    templ.reverse()

    final = ''.join(templ)
    templ = final.split("\n")
    templ.reverse()
    return('\n'.join(templ))


def remove_max_coupled(start_map, stop_map, nmax, N, M):
    """Remove from start_map and stop_map nmax coupled elements that are on
    foundamental state (at floor 1).

    """

    count = 0
    whichcouples = []

    start_map = start_map.split("\n")
    stop_map = stop_map.split("\n")

    for i in range(1, N + 1, 2):
        flr = [start_map[3][i:i + 3] for i in range(0, len(start_map[3]), 3)]

        if flr[i] != ' . ' and flr[i + 1] != ' . ':
            whichcouples.append(i)
            whichcouples.append(i + 1)
            count += 1

            if (2 * count) == nmax:
                break

    # FIXME: control stop_map, we assume than stop is on final state
    # ie on 4th floor

    whichcouples.reverse()

    for fl in range(0, M):
        start_flr = [start_map[fl][i:i + 3] for i in range(0, len(start_map[3]), 3)]
        stop_flr = [stop_map[fl][i:i + 3] for i in range(0, len(stop_map[3]), 3)]
        for i in whichcouples:
            start_flr.pop(i)
            stop_flr.pop(i)

        start_map[fl] = "".join(start_flr)
        stop_map[fl] = "".join(stop_flr)

    start_map = "\n".join(start_map)
    stop_map = "\n".join(stop_map)

    return(start_map, stop_map, count)


def solve(start_map, stop_map, N, M):
    # so if the step to solve the reduce puzzle are
    startint = int_from_conf(start_map)
    endint = int_from_conf(stop_map)
    H = generate_all_move(N)
    sst = generate_all(startint, H, N, M)
    graph = generate_graph(sst)
    path = shortest_path(graph, startint, endint)
    lenght = len(path) - 1
    return(lenght)


# ------------------------------------------------------------------------------
# first part puzzle
# ------------------------------------------------------------------------------

# initial map
p1start_map = "\n".join([' _  .  .  .  .  .  .  .  .  .  . ',
                         ' _  .  .  .  .  .  .  .  .  .  . ',
                         ' _  . OM  .  .  . PM  .  .  .  . ',
                         ' E OG  . TG TM PG  . RG RM CG CM '])


# final map
p1stop_map = "\n".join([' E OG OM TG TM PG PM RG RM CG CM ',
                        ' _  .  .  .  .  .  .  .  .  .  . ',
                        ' _  .  .  .  .  .  .  .  .  .  . ',
                        ' _  .  .  .  .  .  .  .  .  .  . '])


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# additional puzzle
# ------------------------------------------------------------------------------
# this solve the answere to the question
# how many steps we need to bring any additional couple of elements
# to the last floor.
# Note that the elevator is on the last floor in the initial state.

# initial additional map
astart_map = "\n".join([' E RG RM  .  . ',
                        ' _  .  .  .  . ',
                        ' _  .  .  .  . ',
                        ' .  .  . CG CM '])


# final additional map
astop_map = "\n".join([' E RG RM CG CM ',
                       ' _  .  .  .  . ',
                       ' _  .  .  .  . ',
                       ' _  .  .  .  . '])

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# second part puzzle
# ------------------------------------------------------------------------------

# initial map second puzzle
p2start_map = "\n".join([' _  .  .  .  .  .  .  .  .  .  .  .  .  .  . ',
                         ' _  .  .  .  .  .  .  .  .  .  .  .  .  .  . ',
                         ' _  . OM  .  .  . PM  .  .  .  .  .  .  .  . ',
                         ' E OG  . TG TM PG  . RG RM CG CM EG EM LG LM '])


# final map second puzzle
p2stop_map = "\n".join([' E OG OM TG TM PG PM RG RM CG CM EG EM LG LM ',
                        ' _  .  .  .  .  .  .  .  .  .  .  .  .  .  . ',
                        ' _  .  .  .  .  .  .  .  .  .  .  .  .  .  . ',
                        ' _  .  .  .  .  .  .  .  .  .  .  .  .  .  . '])


# ------------------------------------------------------------------------------


# FIRST PART

# we reduce the puzzle i a simpler one with less elements (`count` couple less)
# the we obtain the solution by adding the reduced steps to `count` times the steps
# of the additional puzzle

# each element occupy 3 char so the number of elements is  the lenght
# of each floor divided by 3 - 1 (the space occupied by the elevator)
n = len(p1start_map.split("\n")[0]) // 3 - 1
m = len(p1start_map.split("\n"))

# obtain reduced map
start_map, stop_map, count = remove_max_coupled(p1start_map, p1stop_map, 8, n, m)
n = n - 2 * count

# calculate the steps to solve the reduced puzzle
reducedlenght = solve(start_map, stop_map, n, m)

# calculate the steps for the additional puzzle
n = len(astart_map.split("\n")[0]) // 3 - 1
m = len(astart_map.split("\n"))
additional = solve(astart_map, astop_map, n, m)

# and ... the steps to solve the entire puzzle
puzzle_one = reducedlenght + count * additional

# SECOND PART

# create a new reduction
n = len(p2start_map.split("\n")[0]) // 3 - 1
m = len(p1start_map.split("\n"))
start_map, stop_map, count = remove_max_coupled(p2start_map, p2stop_map, 12, n, m)
n = n - 2 * count

#obtain the steps needed to solv the reduced puzzle
reducedlenght = solve(start_map, stop_map, n, m)

# and ... obtain the steps to solve the entire puzzle
puzzle_two = reducedlenght + count * additional

print("Day 11. Solution of part 1: {}".format(puzzle_one))
print("Day 11. Solution of part 2: {}".format(puzzle_two))
