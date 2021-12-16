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
    self.pair_counts = dict()
    for i in range(len(initial)-1):
      pair = initial[i:i+2]
      self.pair_counts[pair] = self.pair_counts.get(pair, 0) + 1
    self.first_char = initial[0]
    self.last_char = initial[-1]

  def AddRule(self, pair, insertion):
    self.rules[pair] = insertion

  def Iterate(self):
    new_counts = dict()
    for pair, count in self.pair_counts.items():
      insertion = self.rules.get(pair, None)
      assert insertion, (self.rules, pair)
      pair1 = pair[0] + insertion
      pair2 = insertion + pair[1]
      new_counts[pair1] = new_counts.get(pair1, 0) + count
      new_counts[pair2] = new_counts.get(pair2, 0) + count
    self.pair_counts = new_counts

  def Score(self):
    counts = dict()
    for pair, count in self.pair_counts.items():
      counts[pair[0]] = counts.get(pair[0], 0) + count
      counts[pair[1]] = counts.get(pair[1], 0) + count
    counts[self.first_char] += 1
    counts[self.last_char] += 1
    final_counts = dict()
    for char, count in counts.items():
      final_counts[char] = count//2
    sorted_counts = sorted(final_counts.items(), key=lambda x: (x[1], x[0]))
    print(sorted_counts)
    print(sorted_counts[-1][1] - sorted_counts[0][1])
    return sorted_counts[-1][1] - sorted_counts[0][1]


p = Polymer()

p.SetInitial(lines[0].strip())
assert lines[1].strip() == ''

for line in lines[2:]:
  m = re.match(r'^(\w{2}) -> (\w)$', line)
  assert m
  p.AddRule(m.group(1), m.group(2))

for i in range(40):
  print((i, p.pair_counts, p.Score()))
  p.Iterate()

print(p.Score())

