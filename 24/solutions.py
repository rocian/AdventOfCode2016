#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are
locked tight, and all of the controls and related electronics are
inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to
interface with some of the exposed wires that have been routed through the HVAC
system. If you can direct it to each of those locations, you should be able to
bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired and
create a map with the relevant locations marked (your puzzle input). 0 is your
current location, from which the cleaning robot embarks; the other numbers are
(in no particular order) the locations the robot needs to visit at least once
each. Walls are marked as #, and open passages are marked as .. Numbers behave
like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible, you would have
the robot take the following path:

    0 to 4 (2 steps)
    4 to 1 (4 steps; it can't move diagonally)
    1 to 2 (6 steps)
    2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route. This
path is the fewest steps (in the above example, a total of 14) required to start
at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number
of steps required to visit every non-0 number marked on the map at least once?

--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to
notice.

What is the fewest number of steps required to start at 0, visit every non-0
number marked on the map at least once, and then return to 0?

"""


import numpy as np
from itertools import permutations


def read_input():

    f = open('input', 'r')
    string = f.read()
    f.close()

    return(string.strip().split("\n"))


def wall_design(x, y, tmap):
    """Wall design. Implement function that return the element (wall, or space) at
    position (x, y) of the map. Each position outside map is seen as wall.

    """

    Xmax = len(tmap[0]) - 1
    Ymax = len(tmap) - 1
    if (x < 0) or (y < 0) or (x > Xmax) or (y > Ymax):
        return('#')

    return(tmap[y][x])


# breath depth
def bfs_paths(graph, start, goal):
    seen = []
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                if next not in seen:
                    seen.append(next)
                    queue.append((next, path + [next]))

                
def shortest_path(graph, start, goal):

    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


def generate_graph(tmap):
    graph = {}

    Xmax = len(tmap[0])
    Ymax = len(tmap)
    
    points = {}
    for x in range(0, Xmax):
        for y in range(0, Ymax):

            up = wall_design(x, y - 1, tmap)
            do = wall_design(x, y + 1, tmap)
            le = wall_design(x - 1, y, tmap)
            ri = wall_design(x + 1, y, tmap)

            xy = wall_design(x, y, tmap)
            
            graph[(x, y)] = set()

            if xy not in ['#', '.']:
                points[xy] = (x,y)
            
            if up != '#':
                graph[(x, y)].add((x, y - 1))

            if do != '#':
                graph[(x, y)].add((x, y + 1))

            if le != '#':
                graph[(x, y)].add((x - 1, y))

            if ri != '#':
                graph[(x, y)].add((x + 1, y))

    return(graph, points)


tmap = read_input()
graph, points = generate_graph(tmap)
distance = np.zeros((len(points),len(points)), dtype=int)

for i in points:
    ii = int(i)
    for j in points:
        jj = int(j)
        if jj <= ii:
            continue

        shortest = shortest_path(graph, points[i], points[j])        
        distance[ii][jj] = int(len(shortest) - 1)
        distance[jj][ii] = int(len(shortest) - 1)        


minimum = 100000000
maximum = 0

start = [ points[i] for i in points ]
nstart = start.copy()

nstart.remove(points['0'])

for p in permutations(nstart):
    p = list(p)
    p.insert(0,points['0'])    
    d = 0
    for i in range(0, len(p) - 1):
        x = int(list(points.keys())[list(points.values()).index(p[i])])
        y = int(list(points.keys())[list(points.values()).index(p[i + 1])])        
        d += distance[x][y]

    if minimum > d:
        minimum = d
        path = p

    if maximum < d:
        maximum = d
        mpath = p


print(path)

minimum2 = 100000000
maximum2 = 0

mstart = start.copy()

mstart.remove(points['0'])

for p in permutations(mstart):
    p = list(p)
    p.insert(0,points['0'])
    p.append(points['0'])
    d = 0
    for i in range(0, len(p) - 1):
        x = int(list(points.keys())[list(points.values()).index(p[i])])
        y = int(list(points.keys())[list(points.values()).index(p[i + 1])])        
        d += distance[x][y]

    if minimum2 > d:
        minimum2 = d
        path2 = p

    if maximum2 < d:
        maximum2 = d
        mpath2 = p


print(path2)


print("Day 24. Solution of part 1: {}".format(minimum))
print("Day 24. Solution of part 2: {}".format(minimum2))
