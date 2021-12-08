#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

total_known = 0
for line in lines:
  sequences = line.split(' ')
  assert sequences[10] == '|'
  observations = sequences[:10]
  output_seq = sequences[11:]
  assert len(output_seq) == 4
  print(' '.join(output_seq))
  for code in output_seq:
    if len(code) in [2, 4, 3, 7]:
      total_known += 1

print(total_known)


