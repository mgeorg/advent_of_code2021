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

random_numbers = [int(x) for x in lines[0].split(',')]

boards = list()

for i in range(1, len(lines), 6):
  m = re.match(r'\s*$', lines[i])
  boards.append(Board(lines[i+1:i+6]))

won = None
winning_rand = None
lost = None
losing_rand = None
for rand in random_numbers:
  if won is None:
    for i, b in enumerate(boards):
      b.Mark(rand)
      if b.CheckWin():
        b.SetDone()
        won = i
        winning_rand = rand
  elif lost is None:
    loser_sum = 0
    for i, b in enumerate(boards):
      if b.IsDone():
        continue
      b.Mark(rand)
      if b.CheckWin():
        b.SetDone()
      else:
        loser_candidate = i
        loser_sum += 1
    if loser_sum == 1:
      lost = loser_candidate
  else:
    boards[lost].Mark(rand)
    if boards[lost].CheckWin():
      boards[lost].SetDone()
      losing_rand = rand
      break

print(boards)

print(won)
print(boards[won])

print(boards[won].Score(winning_rand))
# 3164 too low
print(boards[lost].Score(losing_rand))


