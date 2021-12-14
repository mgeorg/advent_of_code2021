#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

initial_crabs = [int(x) for x in lines[0].split(',')]

crab_hist = [0] * (max(initial_crabs) + 1)
for f in initial_crabs:
  crab_hist[f] += 1

fuels = [0] * len(crab_hist)
min_fuel = None
min_fuel_i = None
for i in range(len(crab_hist)):
  fuel = 0
  for j in range(len(crab_hist)):
    fuel += abs(j - i) * crab_hist[j]
  if min_fuel is None or min_fuel > fuel:
    min_fuel = fuel
    min_fuel_i = i
    print('MIN!!!')
  print((i, fuel))

print()
print((min_fuel_i, min_fuel))


