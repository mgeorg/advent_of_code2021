#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
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
