#!/usr/bin/python3

import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

chars_list = []
for line in lines:
  chars_list.append(line.strip())

one_counts = [0] * len(chars_list[0])

for chars in chars_list:
  for i, char in enumerate(chars):
    if char == '1':
      one_counts[i] += 1

total = len(chars_list)
gamma = [None] * len(chars_list[0])
epsilon = [None] * len(chars_list[0])
for i, count in enumerate(one_counts):
  if count > total - count:
    gamma[i] = '1'
    epsilon[i] = '0'
  else:
    gamma[i] = '0'
    epsilon[i] = '1'

print(gamma)
print(epsilon)

gamma_int = int(''.join(gamma), 2)
epsilon_int = int(''.join(epsilon), 2)

print(gamma_int * epsilon_int)
