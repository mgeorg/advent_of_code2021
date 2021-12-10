#!/usr/bin/python3

import re
import numpy as np

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


