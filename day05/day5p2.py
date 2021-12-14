#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

sea_floor = dict()
for line in lines:
  m = re.match(r'^(\d+),(\d+) -> (\d+),(\d+)$', line)
  assert m
  x1 = int(m.group(1))
  y1 = int(m.group(2))
  x2 = int(m.group(3))
  y2 = int(m.group(4))

  if x1 == x2:
    if y1 < y2:
      a = y1
      b = y2
    else:
      a = y2
      b = y1
    for cur_y in range(a, b + 1):
      sea_floor[(x1, cur_y)] = sea_floor.get((x1, cur_y), 0) + 1
  elif y1 == y2:
    if x1 < x2:
      a = x1
      b = x2
    else:
      a = x2
      b = x1
    for cur_x in range(a, b + 1):
      sea_floor[(cur_x, y1)] = sea_floor.get((cur_x, y1), 0) + 1
  else:
    if x1 < x2:
      x_dope = 1
      run_length = x2 - x1 + 1
    else:
      x_dope = -1
      run_length = x1 - x2 + 1
    if y1 < y2:
      y_dope = 1
    else:
      y_dope = -1
    for i in range(run_length):
      cur_x = x1 + i * x_dope
      cur_y = y1 + i * y_dope
      sea_floor[(cur_x, cur_y)] = sea_floor.get((cur_x, cur_y), 0) + 1
    pass

total = 0
for pos, count in sea_floor.items():
  if count >= 2:
    total += 1

# 18869 is too high.
print(total)


