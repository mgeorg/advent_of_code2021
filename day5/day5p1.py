#!/usr/bin/python3

import re
import numpy as np

class Board(object):
  def __init__(self, lines):
    self.done = False
    self.marked = np.zeros((5,5), np.int8)
    self.board = np.zeros((5,5), np.int64)
    for j in range(5):
      m = re.match(
          r'\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$', lines[j])
      assert m, (j, lines)
      for k in range(5):
        self.board[j, k] = int(m.group(1 + k))

  def Mark(self, num):
    for j in range(5):
      for k in range(5):
        if self.board[j, k] == num:
          self.marked[j, k] = 1

  def CheckWin(self):
    max_col_sum = max(sum(self.marked))
    max_row_sum = max(sum(np.transpose(self.marked)))
    if max_col_sum == 5 or max_row_sum == 5:
      return True
    return False

  def SetDone(self):
    self.done = True

  def IsDone(self):
    return self.done

  def Score(self, final_rand):
    unmarked_sum = sum(sum(self.board * (1 - self.marked)))
    return final_rand * unmarked_sum

  def __str__(self):
    return str(self.board + 1000 * self.marked)

  def __repr__(self):
    return repr(self.board + 1000 * self.marked)

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

sea_floor = dict()
for line in lines:
  m = re.match(r'^(\d+),(\d+) -> (\d+),(\d+)$', line)
  assert m
  x1 = int(m.group(1))
  y1 = int(m.group(2))
  x2 = int(m.group(3))
  y2 = int(m.group(4))

  if x1 == x2:
    if y1 < y2:
      a = y1
      b = y2
    else:
      a = y2
      b = y1
    for cur_y in range(a, b + 1):
      sea_floor[(x1, cur_y)] = sea_floor.get((x1, cur_y), 0) + 1
  elif y1 == y2:
    if x1 < x2:
      a = x1
      b = x2
    else:
      a = x2
      b = x1
    for cur_x in range(a, b + 1):
      sea_floor[(cur_x, y1)] = sea_floor.get((cur_x, y1), 0) + 1
  else:
    pass

total = 0
for pos, count in sea_floor.items():
  if count >= 2:
    total += 1

print(total)


