#!/usr/bin/python3

import re
import numpy as np

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

total = 0

decoded_to_num = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,}

for line in lines:
  sequences = line.split(' ')
  assert sequences[10] == '|'
  observations = sequences[:10]
  output_seq = sequences[11:]
  assert len(output_seq) == 4
  
  observations.sort(key=len)

  candidate_cf = list()
  candidate_a = list()
  candidate_bd = list()
  candidate_d = list()
  candidate_b = list()
  candidate_g = list()
  candidate_f = list()
  candidate_c = list()
  candidate_e = list()

  for letter in observations[0]:
    candidate_cf.append(letter)
  for letter in observations[1]:
    if letter not in candidate_cf:
      candidate_a = [letter]
  for letter in observations[2]:
    if letter not in candidate_cf:
      candidate_bd.append(letter)

  for i in [3, 4, 5]:
    num_match_cf = 0
    num_match_a = 0
    num_match_none = 0
    for letter in observations[i]:
      if letter in candidate_cf:
        num_match_cf += 1
      elif letter in candidate_a:
        num_match_a += 1
      else:
        num_match_none += 1
    if num_match_cf == 2 and num_match_a == 1 and num_match_none == 2:
      # This is number 3.
      for letter in observations[i]:
        if letter in candidate_cf:
          pass
        elif letter in candidate_a:
          pass
        else:
          if letter in candidate_bd:
            candidate_d = [letter]
            for bd in candidate_bd:
              if bd != letter:
                candidate_b = [bd]
          else:
            candidate_g = [letter]

  for i in [3, 4, 5]:
    num_match_a = 0
    num_match_b = 0
    num_match_d = 0
    num_match_g = 0
    num_match_none = 0
    for letter in observations[i]:
      if letter in candidate_a:
        num_match_a += 1
      elif letter in candidate_b:
        num_match_b += 1
      elif letter in candidate_d:
        num_match_d += 1
      elif letter in candidate_g:
        num_match_g += 1
      else:
        none_letter = letter
        num_match_none += 1
    if (num_match_a == 1 and num_match_b == 1 and num_match_d == 1 and
        num_match_g == 1 and num_match_none == 1):
      # This is number 5.
      candidate_f = [none_letter]
      for cf in candidate_cf:
        if cf != none_letter:
          candidate_c = [cf]

  for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
    if letter not in (
        candidate_a + 
        candidate_b + 
        candidate_c + 
        candidate_d + 
        # e is missing.
        candidate_f + 
        candidate_g):
      candidate_e = [letter]

  mapping = {
    candidate_a[0]: 'a',
    candidate_b[0]: 'b',
    candidate_c[0]: 'c',
    candidate_d[0]: 'd',
    candidate_e[0]: 'e',
    candidate_f[0]: 'f',
    candidate_g[0]: 'g'}

  output = 0
  for i, code in enumerate(output_seq):
    new_code = list()
    for letter in code:
      new_code.append(mapping[letter])
    new_code.sort()
    new_code_string = ''.join(new_code)
    val = decoded_to_num[new_code_string]
    output += (10 ** (3-i)) * val
    print((code, new_code_string, val))
  total += output
  print(output)
  


print(total)


