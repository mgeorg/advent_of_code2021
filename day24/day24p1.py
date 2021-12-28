#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

prog = list()
for line in lines:
  m = re.match(r'(\w{3})\s+(\w+)\s+([\w-]+)$', line)
  if m:
    if m.group(3) in ['w', 'x', 'y', 'z']:
      prog.append((m.group(1), m.group(2), m.group(3)))
    else:
      prog.append((m.group(1), m.group(2), int(m.group(3))))
  else:
    m = re.match(r'(inp)\s+(\w+)$', line)
    assert m, line
    prog.append((m.group(1), m.group(2)))
    

class Run(object):
  def __init__(self, prog):
    self.prog = prog

  def Run(self, data):
    variables = dict()
    variables['w'] = 0
    variables['x'] = 0
    variables['y'] = 0
    variables['z'] = 0
    data_index = 0
    for op in prog:
      if op[0] == 'inp':
        variables[op[1]] = data[data_index]
        data_index += 1
      elif op[0] == 'add':
        if isinstance(op[2], int):
          variables[op[1]] = variables[op[1]] + op[2]
        else:
          variables[op[1]] = variables[op[1]] + variables[op[2]]
      elif op[0] == 'mul':
        if isinstance(op[2], int):
          variables[op[1]] = variables[op[1]] * op[2]
        else:
          variables[op[1]] = variables[op[1]] * variables[op[2]]
      elif op[0] == 'div':
        if isinstance(op[2], int):
          denom = op[2]
        else:
          denom = variables[op[2]]
        if denom == 0:
          return (None, data_index)
        variables[op[1]] = int(variables[op[1]] / denom)
      elif op[0] == 'mod':
        if variables[op[1]] < 0:
          return (None, data_index)
        if isinstance(op[2], int):
          denom = op[2]
        else:
          denom = variables[op[2]]
        if denom <= 0:
          return (None, data_index)
        variables[op[1]] = variables[op[1]] % denom
      elif op[0] == 'eql':
        if isinstance(op[2], int):
          var = op[2]
        else:
          var = variables[op[2]]
        variables[op[1]] = int(variables[op[1]] == var)
    return (variables['z'], data_index)

def Decrement(data, data_index):
  if data_index == 14:
    data_index = 13
  for i in range(data_index+1, 14):
    data[i] = 9
  while data_index >= 0:
    data[data_index] -= 1
    if data[data_index] == 0:
      data[data_index] = 9
      data_index -= 1
    else:
      return data
  
instance = Run(prog)
data = [9] * 14
while True:
  val, data_index = instance.Run(data)
  print(data, val, data_index)
  if val == 0:
    print(data)
    break
  Decrement(data, data_index)
