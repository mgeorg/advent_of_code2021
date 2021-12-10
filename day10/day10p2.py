#!/usr/bin/python3

import re
import numpy as np
import collections

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

error_value = {
  ')': 3,
  ']': 57,
  '>': 25137,
  '}': 1197,
}

auto_value = {
  '(': 1,
  '[': 2,
  '<': 4,
  '{': 3,
}

auto_vals = list()
score = 0
for line in lines:
  stack = list()
  for char in line.strip():
    if char in ['(', '[', '<', '{']:
      stack.append(char)
    elif char in [')', ']', '>', '}']:
      match = stack.pop()
      error = False
      if match == '(':
        if char != ')':
          error = True
      elif match == '[':
        if char != ']':
          error = True
      elif match == '<':
        if char != '>':
          error = True
      elif match == '{':
        if char != '}':
          error = True
      if error:
        score += error_value[char]
        break
  if not error:
    cur_auto_val = 0
    while len(stack) > 0:
      match = stack.pop()
      cur_auto_val *= 5
      cur_auto_val += auto_value[match]
    auto_vals.append(cur_auto_val)

auto_vals.sort()

print(auto_vals[len(auto_vals)//2])
