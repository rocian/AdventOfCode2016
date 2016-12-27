#!/usr/bin/env python3
"""https://adventofcode.com/2016

--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back
into the network later. However, the corporate firewall only allows
communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems
to be messy and poorly maintained, and it's not clear which IPs are
allowed. Also, rather than being written in dot-decimal notation, they are
written as plain 32-bit integers, which can have any value from 0 through
4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you
retrieved the following blacklist:

5-8
0-2
4-7

The blacklist specifies ranges of IPs (inclusive of both the start and end
value) that are not allowed. Then, the only IPs that this firewall allows are 3
and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle
input), what is the lowest-valued IP that is not blocked?

"""

def read_input():

    f = open('input', 'r')
    string = f.read()
    f.close()

    return(string.strip().split("\n"))

def fuseranges(srange, newrange):

    L, H = newrange

    for r in range(len(srange)):

        l ,h = srange[r]
        if (h == H) and (l == L):
            continue
        
        if (h < (L - 1)) and (r < (len(srange) - 1)):
            continue

        elif (h < (L - 1)) and (r == (len(srange) - 1)):
            srange.append((L, H))
            break

        
        elif (((l - L) >= 1) and ((l - H) <= 1)) or (((L - l) >= 1) and ((L - h) <= 1)):
            srange[r] = (min(l,L,h,H), max(l,L,h,H))
            break
        else:
            srange.insert(r, (L, H))
            break
        
            
    if len(srange) == 0:
        srange.append((L, H))

        
        
blocked = read_input()
srange = []

for i in blocked:
    low, high = i.split('-')
    low = int(low)
    high = int(high)
    fuseranges(srange,(low,high))
    
qrange = []
qrange.append(srange[0])

for i in srange[1:]:
    fuseranges(qrange,i)
    
count = 0
prev = -1 
for r in range(len(qrange)):
    count += qrange[r][0] - prev - 1
    prev = qrange[r][1]

count += 4294967295 - srange[-1][1]

lowest = 0
changed = True
while changed:
    lowtmp = lowest
    
    for i in blocked:
        low, high = i.split('-')
    
        if int(low) <= lowest:
            lowest = max(int(high) + 1, lowest)        

    if lowest != lowtmp:
        changed = True
    else:
        changed = False
        
print("Day 20. Solution of part 1: {}".format(lowest))
print("Day 20. Solution of part 2: {}".format(count))
