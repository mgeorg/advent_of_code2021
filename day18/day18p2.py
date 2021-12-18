#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class SnailNumber(object):
  def __init__(self, line):
    if isinstance(line, list):
      self.nest = line
      self.Reduce()
      return

    self.nest = []

    container = list()
    list_stack = list()
    list_stack.append(container)
    for char in line.strip():
      if char == '[':
        list_stack[-1].append(list())
        list_stack.append(list_stack[-1][-1])
      elif char == ',':
        pass
      elif char == ' ':
        pass
      elif char == ']':
        list_stack.pop()
      else:
        num = int(char)
        list_stack[-1].append(num)
    if container:
      self.nest = container[0]
    self.Reduce()
        
  def Add(self, other):
    return SnailNumber([copy.deepcopy(self.nest), copy.deepcopy(other.nest)])

  def AddExplodeRight(self, number, explode_val):
    if isinstance(number[0], list):
      applied = self.AddExplodeRight(number[0], explode_val)
      if applied:
        return True
    else:
      number[0] = number[0] + explode_val
      return True
    if isinstance(number[1], list):
      applied = self.AddExplodeRight(number[1], explode_val)
      if applied:
        return True
    else:
      number[1] = number[1] + explode_val
      return True
    return False

  def AddExplodeLeft(self, number, explode_val):
    if isinstance(number[1], list):
      applied = self.AddExplodeLeft(number[1], explode_val)
      if applied:
        return True
    else:
      number[1] = number[1] + explode_val
      return True
    if isinstance(number[0], list):
      applied = self.AddExplodeLeft(number[0], explode_val)
      if applied:
        return True
    else:
      number[0] = number[0] + explode_val
      return True
    return False

  def Split(self, number):
    # print(f'Split({number})')
    for i in range(2):
      if isinstance(number[i], list):
        if self.Split(number[i]):
          return True
      elif number[i] > 9:
        number[i] = [number[i]//2, number[i] - (number[i] // 2) ]
        return True
    return False

  def Explode(self, number, depth):
    # print(f'Explode({number}, {depth})')
    if depth == 4:
      if isinstance(number, list):
        # print('Got to depth!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return (2, number[0], number[1])
    else:
      if isinstance(number[0], list):
        exploded, explode_left, explode_right = self.Explode(number[0], depth+1)
        if exploded > 0:
          if exploded == 2:
            number[0] = 0
          # print(f'left exploded! {exploded}, {explode_left}, {explode_right}')
          if isinstance(number[1], list):
            applied = self.AddExplodeRight(number[1], explode_right)
          else:
            number[1] = number[1] + explode_right
            applied = True
          if applied:
            explode_right = 0
          # print(f'{number}')
          return (1, explode_left, explode_right)
      if isinstance(number[1], list):
        exploded, explode_left, explode_right = self.Explode(number[1], depth+1)
        if exploded > 0:
          # print(f'right exploded! {exploded}, {explode_left}, {explode_right}')
          if exploded == 2:
            number[1] = 0
          if isinstance(number[0], list):
            applied = self.AddExplodeLeft(number[0], explode_left)
          else:
            number[0] = number[0] + explode_left
            applied = True
          if applied:
            explode_left = 0
          # print(f'{number}')
          return (1, explode_left, explode_right)
    return (0, 0, 0)

  def Reduce(self):
    already_reduced = True
    while True:
      exploded, explode_left, explode_right = self.Explode(self.nest, 0)
      if exploded > 0:
        already_reduced = False
        print(f'exploded: {self}')
        continue
      split = self.Split(self.nest)
      if split:
        already_reduced = False
        print(f'split: {self}')
        continue
      break
    return already_reduced

  def Magnitude(self):
    return self.MagnitudeRecurse(self.nest)

  def MagnitudeRecurse(self, number):
   if isinstance(number[0], list):
     mag_left = self.MagnitudeRecurse(number[0])
   else:
     mag_left = number[0]
   if isinstance(number[1], list):
     mag_right = self.MagnitudeRecurse(number[1])
   else:
     mag_right = number[1]
   return 3*mag_left + 2*mag_right

  def __str__(self):
    return repr(self)

  def __repr__(self):
    return f'SnailNumber({self.nest})'

number_list = list()
for line in lines:
  number_list.append(SnailNumber(line))


res = [[None]*len(number_list) for x in range(len(number_list))]
mag = [[None]*len(number_list) for x in range(len(number_list))]
for i, s1 in enumerate(number_list):
  for j, s2 in enumerate(number_list):
    if i == j:
      res[i][j] = None
      mag[i][j] = 0
      continue
    res[i][j] = s1.Add(s2)
    mag[i][j] = res[i][j].Magnitude()

print('\n'.join([str(row) for row in mag]))
print(max([max(row) for row in mag]))


# s1 = SnailNumber('[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]')
# s2 = SnailNumber('[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]')
# out = s1.Add(s2)
# print(out)
# print(out.Magnitude())


