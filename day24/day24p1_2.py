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
    
def Parse(variables, var1, var2):
  if not isinstance(var2, int):
    var2 = variables[var2]
  try:
    var2 = int(var2)
  except ValueError:
    pass
  var1 = variables[var1]
  try:
    var1 = int(var1)
  except ValueError:
    pass
  return (var1, var2)

def DoOperation(variables, operation, var1, var2):
  simp1, simp2 = Parse(variables, var1, var2)
  if isinstance(simp1, int) and isinstance(simp2, int):
    if operation == '+':
      variables[var1] = simp1+simp2
    elif operation == '*':
      variables[var1] = simp1*simp2
    elif operation == '/':
      assert simp2 != 0
      variables[var1] = int(simp1/simp2)
    elif operation == '%':
      assert simp1 >= 0 and simp2 > 0, (var1, var2)
      variables[var1] = simp1 % simp2
    elif operation == '==':
      variables[var1] = int(simp1 == simp2)
    else:
      assert False
  else:
    if operation == '*' and (simp1 == 0 or simp2 == 0):
      variables[var1] = 0
    elif operation == '*' and simp1 == 1:
      variables[var1] = simp2
    elif operation == '*' and simp2 == 1:
      variables[var1] = simp1
    elif operation == '/' and simp2 == 1:
      variables[var1] = simp1
    elif operation == '+' and simp1 == 0:
      variables[var1] = simp2
    elif operation == '+' and simp2 == 0:
      variables[var1] = simp1
    elif (operation == '==' and
          isinstance(simp1, int) and not isinstance(simp2, int) and
          len(simp2) == 1 and
          (simp1 > 9 or simp1 < 1)):
        variables[var1] = 0
    elif (operation == '==' and
          isinstance(simp2, int) and not isinstance(simp1, int) and
          len(simp1) == 1 and
          (simp2 > 9 or simp2 < 1)):
        variables[var1] = 0
    elif operation == '%' and simp1 == '(a+6)' and simp2 == 26:
      variables[var1] = simp1
    elif operation == '+' and simp1 == '(a+6)' and simp2 == 15:
      variables[var1] = '(a+21)'
    elif operation == '==' and simp1 == '(a+21)' and simp2 == 'b':
      variables[var1] = '0'
    elif (operation == '==' and
          simp1 == '(((((a+6)*26)+(b+7))%26)+15)' and simp2 == 'c'):
      variables[var1] = '0'
    elif (operation == '==' and
          simp1 == '(((((((a+6)*26)+(b+7))*26)+(c+10))%26)+11)' and
          simp2 == 'd'):
      variables[var1] = '0'
    elif (operation == '%' and
          simp1 == '(((((((a+6)*26)+(b+7))*26)+(c+10))*26)+(d+2))' and
          simp2 == 26):
      variables[var1] = '(d+2)'
    elif (operation == '/' and
          simp1 == '(((((((a+6)*26)+(b+7))*26)+(c+10))*26)+(d+2))' and
          simp2 == 26):
      variables[var1] = '(((((a+6)*26)+(b+7))*26)+(c+10))'
    elif (operation == '==' and
          simp1.endswith('%26)+10)') and simp2 in ['f', 'g']):
      variables[var1] = '0'
    else:
      variables[var1] = f'({simp1}{operation}{simp2})'
  
class Run(object):
  def __init__(self, prog):
    self.prog = prog

  def Run(self, data):
    variables = dict()
    variables['w'] = '0'
    variables['x'] = '0'
    variables['y'] = '0'
    variables['z'] = '0'
    data_index = 0
    for op in prog:
      print((op, str(variables['w'])[:100], str(variables['x'])[:100],
             str(variables['y'])[:100], str(variables['z'])[:100]))
      if op[0] == 'inp':
        variables[op[1]] = data[data_index]
        data_index += 1
      elif op[0] == 'add':
        DoOperation(variables, '+', op[1], op[2])
      elif op[0] == 'mul':
        DoOperation(variables, '*', op[1], op[2])
      elif op[0] == 'div':
        DoOperation(variables, '/', op[1], op[2])
      elif op[0] == 'mod':
        DoOperation(variables, '%', op[1], op[2])
      elif op[0] == 'eql':
        DoOperation(variables, '==', op[1], op[2])
    return variables['z']

instance = Run(prog)
data = [chr(ord('a')+i) for i in range(14)]
val = instance.Run(data)
print(val)
