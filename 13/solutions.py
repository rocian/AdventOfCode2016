#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much less
welcoming environment than the shiny atrium of the last one. Instead, you are in
a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers
(x,y). Each such coordinate is either a wall or an open space. You can't move
diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward
positive x and y; negative values are invalid, as they represent a location
outside the building. You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is
actually quite logical. You can determine whether a given x,y coordinate will be
a wall or an open space using a simple system:

    Find x*x + 3*x + 2*x*y + y + y*y.

    Add the office designer's favorite number (your puzzle input).

    Find the binary representation of that sum; count the number of bits that
    are 1.

        If the number of bits that are 1 is even, it's an open space.

        If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing walls as
# and open spaces as ., the corner of the building containing 0,0 would look
like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could take is
marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current
location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

To play, please identify yourself via one of these services:

Your puzzle input is 1358.

--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location)
can you reach in at most 50 steps?

"""


def wall_design(x, y, odfavorite, XYmax):
    """Wall design. Implement function that return the element (wall, or space) at
    position (x, y) of the map. Each position outside map is seen as wall.

    """

    if (x < 0) or (y < 0) or (x > XYmax) or (y > XYmax):
        return('#')

    wall = ['.', '#']
    temp = x * x + 3 * x + 2 * x * y + y + y * y + odfavorite
    binary = list(bin(temp)[2:])
    ones = binary.count('1') % 2
    return(wall[ones])


def get_walls(XYmax, odfavorite):
    "Print map of walls and spaces."

    row = ""
    for y in range(0, XYmax):
        for x in range(0, XYmax):
            row += wall_design(x, y, odfavorite, XYmax)
        row += "\n"
    return(row)


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


# breath depth
def maxlen_paths(graph, start, maxlen):
    queue = [(start, [start])]

    while queue:
        (vertex, path) = queue.pop(0)
        if len(graph[vertex] - set(path)) != 0:
            for next in graph[vertex] - set(path):
                if len(path) >= (maxlen - 1):
                    yield path + [next]

                else:
                    queue.append((next, path + [next]))

        else:
            yield path


def shortest_path(graph, start, goal):

    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


def generate_graph(XYmax, odfavorite):
    graph = {}
    for x in range(0, XYmax):
        for y in range(0, XYmax):

            up = wall_design(x, y - 1, odfavorite, XYmax)
            do = wall_design(x, y + 1, odfavorite, XYmax)
            le = wall_design(x - 1, y, odfavorite, XYmax)
            ri = wall_design(x + 1, y, odfavorite, XYmax)

            graph[(x, y)] = set()

            if up != '#':
                graph[(x, y)].add((x, y - 1))

            if do != '#':
                graph[(x, y)].add((x, y + 1))

            if le != '#':
                graph[(x, y)].add((x - 1, y))

            if ri != '#':
                graph[(x, y)].add((x + 1, y))

    return(graph)


graph = generate_graph(170, 1358)
shortest = shortest_path(graph, (1, 1), (31, 39))
l1 = len(shortest) - 1

graph = generate_graph(53, 1358)
paths = maxlen_paths(graph, (1, 1), 51)
all = set()
for p in paths:
    for i in p:
        all.add(i)

l2 = len(all)

print("Day 13. Solution of part 1: {}".format(l1))
print("Day 13. Solution of part 2: {}".format(l2))
