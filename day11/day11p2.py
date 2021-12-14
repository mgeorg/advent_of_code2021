#!/usr/bin/python3

import re
import numpy as np
import collections

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

kMaxRange = 10

class Board(object):
  def __init__(self, lines):
    self.board = list()
    for line in lines:
      self.board.append([int(x) for x in line.strip()])
      assert len(self.board[-1]) == kMaxRange
    assert len(self.board) == kMaxRange

  def Iterate(self):
    for i, row in enumerate(self.board):
      for j, val in enumerate(row):
        self.board[i][j] += 1

    changed = True
    flashed_count = 0
    while changed:
      changed = False
      for i, row in enumerate(self.board):
        for j, val in enumerate(row):
          if val > 9:
            self.board[i][j] = 0
            flashed_count += 1
            changed = True
            for i_offset in [-1, 0, 1]:
              for j_offset in [-1, 0, 1]:
                if (i + i_offset >= 0 and j + j_offset >= 0 and
                    i + i_offset < kMaxRange and j + j_offset < kMaxRange):
                  if self.board[i+i_offset][j+j_offset] != 0:
                    self.board[i+i_offset][j+j_offset] += 1
    return flashed_count

  def __str__(self):
    return repr(self)

  def __repr__(self):
    output = ''
    for row in self.board:
      output += '  \'' + ''.join([str(x) for x in row]) + '\'\n'
    return f'Board(\n{output})'

b = Board(lines)
print(b)
total_flashes = 0
for num in range(1000):
  flash_count = b.Iterate()
  total_flashes += flash_count
  print(num)
  print(b)
  if flash_count == 100:
    print(num+1)
    break

print(total_flashes)
