#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

initial_fish = [int(x) for x in lines[0].split(',')]

fish_hist = [0] * 9
for f in initial_fish:
  fish_hist[f] += 1

for i in range(256):
  new_fish_hist = fish_hist[1:] + [fish_hist[0]]
  new_fish_hist[6] += fish_hist[0]
  fish_hist = new_fish_hist
  print((i+1, fish_hist, sum(fish_hist)))

print(sum(fish_hist))


