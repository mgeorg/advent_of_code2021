#!/usr/bin/python3

import collections
import copy
import numpy as np
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()


class Paper(object):
  def __init__(self):
    self.dots = list()

  def AddDot(self, x, y):
    self.dots.append((x, y))

  def Fold(self, x_or_y, val):
    if x_or_y == 'x':
      self.FoldX(val)
    else:
      self.FoldY(val)

  def FoldX(self, x):
    new_dots = set()
    for dot in self.dots:
      if dot[0] > x:
        new_dots.add((2*x - dot[0], dot[1]))
      else:
        new_dots.add(dot)
    self.dots = sorted(list(new_dots))

  def FoldY(self, y):
    print('FoldY')
    new_dots = set()
    for dot in self.dots:
      if dot[1] > y:
        new_dots.add((dot[0], 2*y - dot[1]))
      else:
        new_dots.add(dot)
    self.dots = sorted(list(new_dots))

  def PrettyPrint(self):
    maxX = 0
    maxY = 0
    for dot in self.dots:
      if dot[0] > maxX:
        maxX = dot[0]
      if dot[1] > maxY:
        maxY = dot[1]
    output = ''
    for y in range(maxY+1):
      for x in range(maxX+1):
        if (x, y) in self.dots:
          output += '#'
        else:
          output += '.'
      output += '\n'
    print(output)

p = Paper()

process_coordinates = True
for line in lines:
  if line.strip() == '':
    process_coordinates = False
    continue
  if process_coordinates:
    m = re.match(r'^([\d]+),([\d]+)$', line)
    assert m
    p.AddDot(int(m.group(1)), int(m.group(2)))
  else:
    m = re.match(r'^fold along ([xy])=(\d+)$', line)
    assert m
    print(len(p.dots))
    p.Fold(m.group(1), int(m.group(2)))
    print(len(p.dots))

p.PrettyPrint()
# EPZGKCHU
