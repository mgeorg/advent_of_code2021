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
  print((turn_on, x1, x2, y1, y2, z1, z2))
  for x in range(x1, x2+1):
    for y in range(y1, y2+1):
      for z in range(z1, z2+1):
        board[x][y][z] = turn_on

total = 0
for x in range(-50, 51):
  for y in range(-50, 51):
    for z in range(-50, 51):
      total += board[x][y][z]

print(total)

class Cube(object):
  def __init__(self, x1, x2, y1, y2, z1, z2, turn_on):
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2
    self.z1 = z1
    self.z2 = z2
    self.turn_on = turn_on

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
      return Cube(new_x1, new_x2, new_y1, new_y2, new_z1, new_z2, other.turn_on)
    return None

  def Area(self):
    return (self.x2-self.x1+1)*(self.y2-self.y1+1)*(self.y2-self.y1+1)

  def __repr__(self):
    return 'Cube' + repr((self.x1, self.x2, self.y1, self.y2,
                          self.z1, self.z2, self.turn_on))

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

def HigherOrderIntersections(intersection, intersections, i, j):
  count = 0
  for k in range(i+1, j):
    extra = intersections[i].Intersect(intersections[k])
    if extra is not None:
      count += (extra.Area() -
                HigherOrderIntersections(extra, intersections, i, k))
  return count

# cubes.reverse()
count = 0
for i in range(len(cubes)):
  if cubes[i].turn_on:
    count += cubes[i].Area()
  intersections = list()
  for j in range(i):
    intersection = cubes[i].Intersect(cubes[j])
    if intersection is not None:
      print((i, j, intersection))
      if cubes[j].turn_on:
        count -= intersection.Area()
      intersections.append(intersection)
  # Handle higher order issues.
  for i in range(len(intersections)-1):
    count += HigherOrderIntersections(
        intersections[i], intersections, i, len(intersections))

print(count)

