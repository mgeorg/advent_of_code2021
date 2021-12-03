#!/usr/bin/python3

import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

chars_list = []
for line in lines:
  chars_list.append(line.strip())

num_digits = len(chars_list[0])

one_counts = [0] * num_digits

for chars in chars_list:
  for i, char in enumerate(chars):
    if char == '1':
      one_counts[i] += 1

total = len(chars_list)
gamma = [None] * num_digits
epsilon = [None] * num_digits
for i, count in enumerate(one_counts):
  if count > total - count:
    gamma[i] = '1'
    epsilon[i] = '0'
  else:
    gamma[i] = '0'
    epsilon[i] = '1'

print('gamma: ' + ''.join(gamma))
print('epsilon: ' + ''.join(epsilon))

gamma_int = int(''.join(gamma), 2)
epsilon_int = int(''.join(epsilon), 2)

print(gamma_int * epsilon_int)

# oxygen generator (most common or 1)

cur_list = chars_list[:]
for i in range(num_digits):
  cur_ones_count = 0
  for chars in cur_list:
    char = chars[i]
    if char == '1':
      cur_ones_count += 1
  if cur_ones_count >= len(cur_list) - cur_ones_count:
    select = '1'
  else:
    select = '0'
  new_cur_list = []
  for chars in cur_list:
    if chars[i] == select:
      new_cur_list.append(chars)
  cur_list = new_cur_list
  assert len(cur_list) > 0
  if len(cur_list) == 1:
    break
oxygen_generator_rating = int(cur_list[0], 2)

# co2 scrubber
cur_list = chars_list[:]
for i in range(num_digits):
  cur_ones_count = 0
  for chars in cur_list:
    char = chars[i]
    if char == '1':
      cur_ones_count += 1
  if cur_ones_count >= len(cur_list) - cur_ones_count:
    select = '0'
  else:
    select = '1'
  new_cur_list = []
  for chars in cur_list:
    if chars[i] == select:
      new_cur_list.append(chars)
  cur_list = new_cur_list
  assert len(cur_list) > 0
  if len(cur_list) == 1:
    break
co2_scrubber_rating = int(cur_list[0], 2)

print(oxygen_generator_rating * co2_scrubber_rating)

