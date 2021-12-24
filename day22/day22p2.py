#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('example1.txt', 'r') as f:
  lines = f.read().splitlines()

board = dict()
for x in range(-50, 51):
  board[x] = dict()
  for y in range(-50, 51):
    board[x][y] = dict()
    for z in range(-50, 51):
      board[x][y][z] = False

def CountBoard(board):
  total = 0
  for x in range(-50, 51):
    for y in range(-50, 51):
      for z in range(-50, 51):
        total += board[x][y][z]
  return total

ground_truth = list()
count = 0
for line in lines:
  m = re.match(r'^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),'
               r'z=(-?\d+)\.\.(-?\d+)$', line)
  assert m, line
  turn_on = m.group(1) == 'on'
  x1 = int(m.group(2))
  x2 = int(m.group(3))
  y1 = int(m.group(4))
  y2 = int(m.group(5))
  z1 = int(m.group(6))
  z2 = int(m.group(7))
  if x2 < -50 or x1 > 50 or y2 < -50 or y1 > 50 or z2 < -50 or z1 > 50:
    continue
  # print((turn_on, x1, x2, y1, y2, z1, z2))
  for x in range(x1, x2+1):
    for y in range(y1, y2+1):
      for z in range(z1, z2+1):
        board[x][y][z] = turn_on
  last = count
  count = CountBoard(board)
  ground_truth.append((count, count-last))
  # print((count, count-last))

print(CountBoard(board))

class Cube(object):
  def __init__(self, x1, x2, y1, y2, z1, z2, turn_on, name=None):
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2
    self.z1 = z1
    self.z2 = z2
    self.turn_on = turn_on
    self.name = name

  def Intersect(self, other):
    new_x1 = None
    new_y1 = None
    new_z1 = None
    if other.x1 <= self.x2 and other.x2 >= self.x1:
      new_x1 = max(self.x1, other.x1)
      new_x2 = min(self.x2, other.x2)
    if other.y1 <= self.y2 and other.y2 >= self.y1:
      new_y1 = max(self.y1, other.y1)
      new_y2 = min(self.y2, other.y2)
    if other.z1 <= self.z2 and other.z2 >= self.z1:
      new_z1 = max(self.z1, other.z1)
      new_z2 = min(self.z2, other.z2)
    if new_x1 is not None and new_y1 is not None and new_z1 is not None:
      new_name = None
      if self.name and other.name:
        new_name = ''.join(sorted(set([x for x in self.name+other.name])))
      return Cube(new_x1, new_x2, new_y1, new_y2, new_z1, new_z2,
                  other.turn_on, new_name)
    return None

  def Area(self):
    return (self.x2-self.x1+1)*(self.y2-self.y1+1)*(self.z2-self.z1+1)

  def __repr__(self):
    return 'Cube' + repr((self.x1, self.x2, self.y1, self.y2,
                          self.z1, self.z2, self.turn_on, self.name))

cubes = list()
for line in lines:
  m = re.match(r'^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),'
               r'z=(-?\d+)\.\.(-?\d+)$', line)
  assert m, line
  turn_on = m.group(1) == 'on'
  x1 = int(m.group(2))
  x2 = int(m.group(3))
  y1 = int(m.group(4))
  y2 = int(m.group(5))
  z1 = int(m.group(6))
  z2 = int(m.group(7))
  if (x2 < -50 or x1 > 50 or y2 < -50 or y1 > 50 or z2 < -50 or z1 > 50):
    continue
  # print((turn_on, x1, x2, y1, y2, z1, z2))
  cubes.append(Cube(x1, x2, y1, y2, z1, z2, turn_on))

# print('\n'.join([str(c) for c in cubes]))

def HigherOrderIntersections(intersection, intersections, sign, i, j):
  global added_string
  if i == j:
    return 0
  print(f'  Higher({intersection.name}, ..., {sign}, {i}, {j})')
  count = 0
  if sign == 1:
    for k in range(i, j):
      extra = intersection.Intersect(intersections[k])
      if extra is not None:
        print('  ' + repr((i, k, j, '+' + extra.name, extra.Area())))
        added_string.append('+' + extra.name)
        count += (sign * extra.Area() +
            HigherOrderIntersections(extra, intersections, -sign, i, k))
  else:
    for k in range(j-1, i-1, -1):
      extra = intersection.Intersect(intersections[k])
      if extra is not None:
        print('  ' + repr((i, k, j, '-' + extra.name, extra.Area())))
        added_string.append('-' + extra.name)
        count += (sign * extra.Area() +
            HigherOrderIntersections(extra, intersections, -sign, k+1, j))
  print(f'  ENDED Higher({intersection.name}, ..., {sign}, {i}, {j}) = {count}')
  return count

for i in range(len(cubes)):
  cubes[i].name = chr(ord('A') + i)

# cubes.reverse()
count = 0
for j in range(len(cubes)):
  added_string = list()
  last = count
  if cubes[j].turn_on:
    count += cubes[j].Area()
    added_string.append('+' + cubes[j].name)
  intersections = collections.deque()
  for i in range(j-1, -1, -1):
    intersection = cubes[i].Intersect(cubes[j])
    if intersection is not None:
      print((i, j, intersection, intersection.Area()))
      if cubes[i].turn_on:
        added_string.append('-' + intersection.name)
        count -= intersection.Area()
        count += HigherOrderIntersections(
            intersection, intersections, 1, 0, len(intersections))
      intersections.appendleft(intersection)
  print(' '.join(added_string))
  prefix = ''
  if count != ground_truth[j][0]:
    prefix = 'MISTAKE!!! '
  print(prefix + repr((j, count, ground_truth[j][0],
                       count-last, ground_truth[j][1],
                       ground_truth[j][1]-count+last)))

print(count)

