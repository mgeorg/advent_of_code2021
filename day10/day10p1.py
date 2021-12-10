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

print(score)
