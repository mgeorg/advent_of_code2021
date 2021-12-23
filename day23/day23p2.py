#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

routes = {
    (0, 7): 3,
    (1, 7): 2,
    (0, 11): 4,
    (1, 11): 3,
    (0, 8): 5,
    (1, 8): 4,
    (0, 12): 6,
    (1, 12): 5,
    (0, 9): 7,
    (1, 9): 6,
    (0, 13): 8,
    (1, 13): 7,
    (0, 10): 9,
    (1, 10): 8,
    (0, 14): 10,
    (1, 14): 9,
    (2, 7): 2,
    (2, 11): 3,
    (2, 8): 2,
    (2, 12): 3,
    (2, 9): 4,
    (2, 13): 5,
    (2, 10): 6,
    (2, 14): 7,
    (3, 7): 4,
    (3, 11): 5,
    (3, 8): 2,
    (3, 12): 3,
    (3, 9): 2,
    (3, 13): 3,
    (3, 10): 4,
    (3, 14): 5,
    (4, 7): 6,
    (4, 11): 7,
    (4, 8): 4,
    (4, 12): 5,
    (4, 9): 2,
    (4, 13): 3,
    (4, 10): 2,
    (4, 14): 3,
    (5, 7): 8,
    (5, 11): 9,
    (5, 8): 6,
    (5, 12): 7,
    (5, 9): 4,
    (5, 13): 5,
    (5, 10): 2,
    (5, 14): 3,
    (6, 7): 9,
    (6, 11): 10,
    (6, 8): 7,
    (6, 12): 8,
    (6, 9): 5,
    (6, 13): 6,
    (6, 10): 3,
    (6, 14): 4,
}

new_routes = dict()
for i_j, cost in routes.items():
  i = i_j[0]
  j = i_j[1]
  if j >= 11:
    new_routes[(i, j+4)] = cost + 1
    new_routes[(i, j+8)] = cost + 2

routes.update(new_routes)

class Board(object):
  def __init__(self, locations, cost):
    self.locations = locations
    self.cost = cost
    self.history = None

  def CheckColumn(self, base, target):
    for check in [base, base+4, base+8, base+12]:
      if target == check:
        return True
      if self.locations[check] != ' ':
        return False
    return False

#############
#01.2.3.4.56#
###7#8#9#0###
  #1#2#3#4#
  def PathClear(self, i, j):
    if i == 0:
      if self.locations[1] != ' ':
        return False
      return self.PathClear(1, j)
    if i == 6:
      if self.locations[5] != ' ':
        return False
      return self.PathClear(5, j)
    if i == 1:
      base = 7
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[2] != ' ':
        return False
      base = 8
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[3] != ' ':
        return False
      base = 9
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[4] != ' ':
        return False
      base = 10
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      assert False, (i, j)
    if i == 2:
      base = 7
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      base = 8
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[3] != ' ':
        return False
      base = 9
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[4] != ' ':
        return False
      base = 10
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      assert False, (i, j)
    if i == 3:
#01.2.3.4.56#
###7#8#9#0###
  #1#2#3#4#
      base = 7
      if j in [base, base+4, base+8, base+12]:
        if self.locations[2] != ' ':
          return False
        return self.CheckColumn(base, j)
      base = 8
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      base = 9
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[4] != ' ':
        return False
      base = 10
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
    if i == 5:
#01.2.3.4.56#
###7#8#9#0###
  #1#2#3#4#
      base = 10
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[4] != ' ':
        return False
      base = 9
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[3] != ' ':
        return False
      base = 8
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[2] != ' ':
        return False
      base = 7
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      assert False, (i, j)
    if i == 4:
#01.2.3.4.56#
###7#8#9#0###
  #1#2#3#4#
      base = 10
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      base = 9
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[3] != ' ':
        return False
      base = 8
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      if self.locations[2] != ' ':
        return False
      base = 7
      if j in [base, base+4, base+8, base+12]:
        return self.CheckColumn(base, j)
      assert False, (i, j)

  def LowestAvailable(self, base, correct_char):
    if self.locations[base+12] == ' ':
      return base+12
    if self.locations[base+12] != correct_char:
      return None
    if self.locations[base+8] == ' ':
      return base+8
    if self.locations[base+8] != correct_char:
      return None
    if self.locations[base+4] == ' ':
      return base+4
    if self.locations[base+4] != correct_char:
      return None
    if self.locations[base] == ' ':
      return base
    return None
    
  def NextMoves(self):
#01.2.3.4.56#
###7#8#9#0###
  #1#2#3#4#
    output = list()
    # print(f'locations {self.locations}')
    for i, char in enumerate(self.locations):
      # print((i, char))
      if char == ' ':
        continue
      if i < 7:
        if char == 'A':
          target = self.LowestAvailable(7, 'A')
          if target is None:
            continue
          if self.PathClear(i, target):
            new_locations = [x for x in self.locations]
            new_locations[i] = ' '
            new_locations[target] = 'A'
            b = Board(''.join(new_locations), self.cost + routes[(i, target)])
            b.history = self
            output.append(b)
        if char == 'B':
          target = self.LowestAvailable(8, 'B')
          if target is None:
            continue
          if self.PathClear(i, target):
            new_locations = [x for x in self.locations]
            new_locations[i] = ' '
            new_locations[target] = 'B'
            b = Board(''.join(new_locations),
                      self.cost + 10*routes[(i, target)])
            b.history = self
            output.append(b)
        if char == 'C':
          target = self.LowestAvailable(9, 'C')
          if target is None:
            continue
          if self.PathClear(i, target):
            new_locations = [x for x in self.locations]
            new_locations[i] = ' '
            new_locations[target] = 'C'
            b = Board(''.join(new_locations),
                      self.cost + 100*routes[(i, target)])
            b.history = self
            output.append(b)
        if char == 'D':
          target = self.LowestAvailable(10, 'D')
          if target is None:
            continue
          if self.PathClear(i, target):
            new_locations = [x for x in self.locations]
            new_locations[i] = ' '
            new_locations[target] = 'D'
            b = Board(''.join(new_locations),
                      self.cost + 1000*routes[(i, target)])
            b.history = self
            output.append(b)
      else:
#01.2.3.4.56#
###7#8#9#0###
  #1#2#3#4#
        locked = False
        for correct_char, base in [('A', 7), ('B', 8), ('C', 9), ('D', 10)]:
          if char == correct_char and i in [base, base+4, base+8, base+12]:
            if i == base+12:
              locked = True
              break
            if self.locations[base+12] != correct_char:
              break
            if i == base+8:
              locked = True
              break
            if self.locations[base+8] != correct_char:
              break
            if i == base+4:
              locked = True
              break
            if self.locations[base+4] != correct_char:
              break
            locked = True
            break

        if locked:
          continue
          
        cost_multiplier = 1
        if char == 'B':
          cost_multiplier = 10
        elif char == 'C':
          cost_multiplier = 100
        elif char == 'D':
          cost_multiplier = 1000

        for target in range(7):
          if self.locations[target] == ' ' and self.PathClear(target, i):
            new_locations = [x for x in self.locations]
            new_locations[i] = ' '
            new_locations[target] = char
            b = Board(''.join(new_locations),
                      self.cost + cost_multiplier * routes[(target, i)])
            b.history = self
            output.append(b)
    return output

  def __repr__(self):
    if self.history:
      return 'Board' + repr((self.locations, self.cost, self.history))
    return 'Board' + repr((self.locations, self.cost))

final = '       ABCDABCDABCDABCD'
initial_locations = '       DBCCDCBADBACDABA' # input
# initial_locations = '       BCBDDCBADBACADCA'  # Example
init = Board(initial_locations, 0)
q = queue.PriorityQueue()
added_index = 0
q.put((init.cost, added_index, init))
added_index += 1
all_seen = set()
while not q.empty():
  cost, unused_index, current = q.get()
  if current.locations in all_seen:
    continue
  print((cost, current.locations))
  all_seen.add(current.locations)
  if current.locations == final:
    break
  next_moves = current.NextMoves()
  for move in next_moves:
    q.put((move.cost, added_index, move))
    added_index += 1

print(current)
if current.locations != final:
  print('FAILED')
print(cost)
