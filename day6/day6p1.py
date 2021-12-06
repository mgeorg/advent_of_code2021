#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

initial_fish = [int(x) for x in lines[0].split(',')]

cur_fish = initial_fish[:]
for i in range(80):
  num_new_fish = 0
  new_fish = list()
  for f in cur_fish:
    if f > 0:
      new_fish.append(f-1)
    else:
      new_fish.append(6)
      num_new_fish += 1
  cur_fish = new_fish + [8] * num_new_fish
  print((i+1, cur_fish))

print(len(cur_fish))


