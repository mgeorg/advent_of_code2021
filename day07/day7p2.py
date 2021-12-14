#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

initial_crabs = [int(x) for x in lines[0].split(',')]

crab_hist = [0] * (max(initial_crabs) + 1)
for f in initial_crabs:
  crab_hist[f] += 1
print(crab_hist)

fuel_cost = [0]*len(crab_hist)
for i in range(1, len(fuel_cost)):
  fuel_cost[i] = i + fuel_cost[i-1]
print(fuel_cost)

fuels = [0] * len(crab_hist)
min_fuel = None
min_fuel_i = None
for i in range(len(crab_hist)):
  fuel = 0
  for j in range(len(crab_hist)):
    offset = abs(j - i)
    cost = crab_hist[j] * fuel_cost[offset]
    # print((j, offset, crab_hist[j], fuel_cost[offset], cost))
    fuel += cost
  if min_fuel is None or min_fuel > fuel:
    min_fuel = fuel
    min_fuel_i = i
    # print('MIN!!!')
  fuels[i] = fuel
  print((i, fuel))

print()
print((min_fuel_i, min_fuel))


