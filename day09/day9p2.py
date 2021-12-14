#!/usr/bin/python3

import re
import numpy as np
import collections

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

board = list()
for line in lines:
  board.append([int(x) for x in line.strip()])
  assert len(board[0]) == len(board[-1])

width = len(board[0])
height = len(board)

minimums = list()
for i in range(width):
  for j in range(height):
    val = board[j][i]
    if ( (j-1 < 0 or val < board[j-1][i]) and
         (j+1 >= height or val < board[j+1][i]) and
         (i-1 < 0 or val < board[j][i-1]) and
         (i+1 >= width or val < board[j][i+1]) ):
      minimums.append(((i, j), val))

total = 0
for pos, val in minimums:
  total += val+1

print(total)


def ExpandOne(pos, breadth_queue, seen):
  if pos[0] < 0 or pos[0] >= width:
    return None
  if pos[1] < 0 or pos[1] >= height:
    return None
  if board[pos[1]][pos[0]] == 9:
    return None
  if pos in seen:
    return None
  breadth_queue.append(pos)
  seen.add(pos)
  return True


def ExpandPos(pos, breadth_queue, seen):
  ExpandOne((pos[0]-1, pos[1]), breadth_queue, seen)
  ExpandOne((pos[0]+1, pos[1]), breadth_queue, seen)
  ExpandOne((pos[0], pos[1]-1), breadth_queue, seen)
  ExpandOne((pos[0], pos[1]+1), breadth_queue, seen)


basin_sizes = list()

for pos, val in minimums:
  breadth_queue = collections.deque()
  seen = set()

  breadth_queue.append(pos)
  seen.add(pos)
  while len(breadth_queue) > 0:
    cur_pos = breadth_queue.popleft()
    ExpandPos(cur_pos, breadth_queue, seen)
  basin_sizes.append((pos, val, len(seen)))

print(basin_sizes)
basin_sizes.sort(key=lambda x: -x[2])
print(basin_sizes)

total = 1
for i in range(3):
  total *= basin_sizes[i][2]

print(total)
