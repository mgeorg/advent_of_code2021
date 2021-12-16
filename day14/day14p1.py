#!/usr/bin/python3

import collections
import copy
import numpy as np
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()


class Polymer(object):
  def __init__(self):
    self.rules = dict()

  def SetInitial(self, initial):
    self.current = initial

  def AddRule(self, pair, insertion):
    self.rules[pair] = insertion

  def Iterate(self):
    new = list()
    for i in range(len(self.current)-1):
      pair = self.current[i:i+2]
      insertion = self.rules.get(pair, None)
      assert insertion, (self.rules, pair)
      new.append(self.current[i])
      new.append(insertion)
    new.append(self.current[-1])
    self.current = ''.join(new)

  def Score(self):
    counts = dict()
    for char in self.current:
      counts[char] = counts.get(char, 0) + 1
    sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]))
    print(sorted_counts)
    print(sorted_counts[-1][1] - sorted_counts[0][1])

p = Polymer()

p.SetInitial(lines[0].strip())
assert lines[1].strip() == ''

for line in lines[2:]:
  m = re.match(r'^(\w{2}) -> (\w)$', line)
  assert m
  p.AddRule(m.group(1), m.group(2))

for i in range(10):
  if len(p.current) < 5*80:
    print(p.current)
  print(len(p.current))
  p.Iterate()

print(len(p.current))
p.Score()

