#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

table = lines[0].strip()

assert lines[1].strip() == ''

image = list()
for line in lines[2:]:
  image.append(line.strip())
  assert len(image[0]) == len(image[-1])

assert len(image[0]) == len(image)

def AddBorder(image, fill_pattern='.'):
  new_image = list()
  new_image.append(fill_pattern * (len(image)+4))
  new_image.append(fill_pattern * (len(image)+4))
  for line in image:
    new_image.append((fill_pattern*2) + line + (fill_pattern*2))
  new_image.append(fill_pattern * (len(image)+4))
  new_image.append(fill_pattern * (len(image)+4))
  return new_image

def GetValue(sequence):
  num = 0
  for char in sequence:
    num *= 2
    if char == '#':
      num += 1
  return num


def DoLookup(image):
  new_image = list()
  for i in range(len(image)-2):
    line = list()
    for j in range(len(image)-2):
      line.append(table[
          GetValue(image[i][j:j+3] + image[i+1][j:j+3] + image[i+2][j:j+3])])
    new_image.append(''.join(line))
  return new_image

fill_pattern = '.'
for i in range(50):
  image = AddBorder(image, fill_pattern)
  fill_pattern = table[GetValue(fill_pattern*9)]
  image = DoLookup(image)

print(sum([sum([char == '#' for char in image[i]]) for i in range(len(image))]))

