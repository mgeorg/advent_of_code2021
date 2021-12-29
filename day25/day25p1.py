#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Board(object):
  def __init__(self, lines):
    self.east = dict()
    self.south = dict()
    for row, line in enumerate(lines):
      for col, char in enumerate(line.strip()):
        if char == '.':
          continue
        elif char == '>':
          self.east[(row, col)] = True
        elif char == 'v':
          self.south[(row, col)] = True
    self.row_mod = row+1
    self.col_mod = col+1

  def Step(self):
    num_move = 0
    move = dict()
    for cucumber, unused in self.east.items():
      row, col = cucumber
      new_pos = (row, (col+1)%self.col_mod)
      if new_pos not in self.east and new_pos not in self.south:
        move[cucumber] = new_pos
    for pos, new_pos in move.items():
      del self.east[pos]
      self.east[new_pos] = True
    num_move += len(move)
    # And now south
    move = dict()
    for cucumber, unused in self.south.items():
      row, col = cucumber
      new_pos = ((row+1)%self.row_mod, col)
      if new_pos not in self.east and new_pos not in self.south:
        move[cucumber] = new_pos
    for pos, new_pos in move.items():
      del self.south[pos]
      self.south[new_pos] = True
    num_move += len(move)
    return num_move

  def __str__(self):
    output = ''
    for row in range(self.row_mod):
      for col in range(self.col_mod):
        if (row, col) in self.east:
          output += '>'
        elif (row, col) in self.south:
          output += 'v'
        else:
          output += '.'
      output += '\n'
    return output

b = Board(lines)
i = 0
num_move = 1
while num_move > 0:
  print(f'i = {i}')
  print(str(b).strip())
  num_move = b.Step()
  i += 1
  print(f'num_move = {num_move}')
print(str(b))
print(num_move)
print(i)
