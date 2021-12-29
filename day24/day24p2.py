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
  except TypeError:
    pass
  var1 = variables[var1]
  try:
    var1 = int(var1)
  except ValueError:
    pass
  except TypeError:
    pass
  return (var1, var2)

class Tree(object):
  def __init__(self, op, var1, var2):
    self.op = op
    self.vars = [var1, var2]
    self.Simplify()

  def GetNum(self):
    for x in self.vars:
      if not isinstance(x, int):
        return None
    if self.op == '*':
      total = 1
      for x in self.vars:
        total *= x
      return total
    if self.op == '+':
      total = 0
      for x in self.vars:
        total += x
      return total
    return None

  def StrNoParen(self):
    output = ''
    for i in range(0, len(self.vars)):
      if i != 0:
        output += self.op
      if (self.op == '+' and
          isinstance(self.vars[i], Tree) and
          self.vars[i].op == '*'):
        output += self.vars[i].StrNoParen()
      elif (self.op == '+' and
          isinstance(self.vars[i], Tree) and
          self.vars[i].op == '*'):
        output += self.vars[i].StrNoParen()
      else:
        output += str(self.vars[i])
    return output

  def __str__(self):
    return '(' + self.StrNoParen() + ')'

  def Simplify(self):
    if (self.op == '%' and isinstance(self.vars[1], int) and
        self.vars[1] == 26):
      print('simplifying ' + str(self))
      if not isinstance(self.vars[0], Tree):
        print(self.vars[0] + ' is not a Tree')
        return
      add = self.vars[0]
      if add.op == '+':
        cur = add.vars[0]
        if (isinstance(cur, Tree) and cur.op == '*' and
            isinstance(cur.vars[1], int) and cur.vars[1] == 26):
          print('is mult by 26')
          self.vars[0] = add.vars[1]
    if False and (self.op == '+' and
        isinstance(self.vars[0], Tree) and
        isinstance(self.vars[1], Tree) and
        self.vars[0].op == '*' and self.vars[0].vars[1] == 26 and
        self.vars[1].op == '*' and self.vars[1].vars[1] == 26):
      replace_me = Tree(
          '*', Tree('+', self.vars[0].vars[0], self.vars[1].vars[0]), 26)
      self.op = replace_me.op
      self.vars = replace_me.vars
    if False and (self.op == '*' and
        isinstance(self.vars[0], Tree) and
        isinstance(self.vars[1], int) and
        self.vars[0].op == '+'):
      replace_me = Tree(
          '+', Tree('*', self.vars[0].vars[0], self.vars[1]),
               Tree('*', self.vars[0].vars[1], self.vars[1]))
      self.op = replace_me.op
      self.vars = replace_me.vars
    if False and (self.op == '*' and
        isinstance(self.vars[0], Tree) and
        isinstance(self.vars[1], int) and
        self.vars[0].op == '*' and
        isinstance(self.vars[0].vars[1], int)):
      print('####################################before')
      print(str(self))
      replace_me = Tree(
          '*', self.vars[0].vars[0],
               self.vars[0].vars[1] * self.vars[1])
      self.op = replace_me.op
      self.vars = replace_me.vars
      print('####################################after')
      print(str(self))
        

def DoOperation(variables, operation, var1, var2):
  global extra_index
  global equations
  simp1, simp2 = Parse(variables, var1, var2)
  if operation != '==' and isinstance(simp1, int) and isinstance(simp2, int):
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
    str1 = str(simp1)
    str2 = str(simp2)
    if operation == '*' and (str1 == '0' or str2 == '0'):
      variables[var1] = 0
    elif operation == '*' and str1 == '1':
      variables[var1] = simp2
    elif operation == '*' and str2 == '1':
      variables[var1] = simp1
    elif operation == '/' and str2 == '1':
      variables[var1] = simp1
    elif operation == '+' and str1 == '0':
      variables[var1] = simp2
    elif operation == '+' and str2 == '0':
      variables[var1] = simp1
   #elif (operation == '==' and
   #      isinstance(simp1, int) and not isinstance(simp2, int) and
   #      len(str2) == 1 and
   #      (simp1 > 9 or simp1 < 1)):
   #    variables[var1] = 0
   #elif (operation == '==' and
   #      isinstance(simp2, int) and not isinstance(simp1, int) and
   #      len(str1) == 1 and
   #      (simp2 > 9 or simp2 < 1)):
   #    variables[var1] = 0
    elif operation == '==' and simp2 == 0:
      variables[var1] = 0
      m = re.match(r'^(.*)==([^()]+\))$', str1)
      if m:
        new_var = extra_vars[extra_index]
        extra_index += 1
        equation = m.group(1) + '!=' + m.group(2)
        equations.append(f'{new_var} = {equation}')
        variables[var1] = new_var
        m = re.match(r'^(?:.*)%26\)\+(-?\d+)\)!=([a-zA-Z])\)$', equation)
        if m and int(m.group(1)) > 9:
          variables[var1] = 1
          equations[-1] = equations[-1] + ' which is 1'
        m = re.match(r'\((-?\d+)!=(\-?\d+)\)$', equation)
        if m:
          variables[var1] = int(int(m.group(1)) != int(m.group(2)))
          equations[-1] = equations[-1] + ' which is ' + str(variables[var1])
        m = re.match(r'\((-?\d+)!=([a-zA-Z])\)$', equation)
        if m and (int(m.group(1)) > 9 or int(m.group(1)) < 1):
          variables[var1] = 1
          equations[-1] = equations[-1] + ' which is 1'
        if new_var in ['F', 'I', 'K', 'L', 'M', 'N', 'O']:
          variables[var1] = 0
          equations[-1] = equations[-1] + ' set to 0'
        # if new_var == 'M':
          # either M == 1 and m+12 < 26 or M == 0 and you get two divisions by 26
          # variables[var1] = 0
          # equations[-1] = equations[-1] + ' which MUST BE 0'
    # elif operation == '==' and simp1 == '(a+21)' and simp2 == 'b':
      # variables[var1] = 'a-b+21 ==%26 0'
    # elif (operation == '==' and
          # simp1 == '(((((a+6)*26)+(b+7))%26)+15)' and simp2 == 'c'):
      # variables[var1] = '0'
    # elif (operation == '==' and
          # simp1 == '(((((((a+6)*26)+(b+7))*26)+(c+10))%26)+11)' and
          # simp2 == 'd'):
      # variables[var1] = '0'
    # elif (operation == '%' and
          # simp1 == '(((((((a+6)*26)+(b+7))*26)+(c+10))*26)+(d+2))' and
          # simp2 == 26):
      # variables[var1] = '(d+2)'
    # elif (operation == '/' and
          # simp1 == '(((((((a+6)*26)+(b+7))*26)+(c+10))*26)+(d+2))' and
          # simp2 == 26):
      # variables[var1] = '(((((a+6)*26)+(b+7))*26)+(c+10))'
    else:
      v = Tree(operation, simp1, simp2)
      val = v.GetNum()
      if val is None:
        variables[var1] = v
      else:
        variables[var1] = val
  
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
      if op[0] == 'inp':
        print(f'input {data[data_index]}')
        if code[data_index] != 'x':
          variables[op[1]] = int(code[data_index])
        else:
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
      print((op, str(variables['w'])[:100], str(variables['x'])[:100],
             str(variables['y'])[:100], str(variables['z'])[:100]))
    return variables['z']

def ExpandEquation(equation):
  output = ''
  indent = 0
  for char in equation:
    if char == '(':
      indent += 1
      # output += char + '\n' + ' '*indent
      output += char
      continue
    if char == ')':
      indent -= 1
      # output += '\n' + ' '*indent + char
      output += char
      continue
    output += char
  if equation[0] in ['F', 'I', 'K', 'L', 'M', 'N', 'O']:
    output += ' MUST BE 0'
  return output

instance = Run(prog)
data = [chr(ord('a')+i) for i in range(14)]
code = 'xxxxxxxxxxxxxx'
code = '9999499599998x'
code = 'xxxxxxxxxxxxxx'
code = '99994995799xxx'
code = '39494195799979'  # Largest
code = 'abcdefghijklmn'
code = '111611511xxxxx'
code = '13161151139617'
extra_vars = [chr(ord('B')+i) for i in range(20)]
extra_index = 0
equations = list()
print(data)
val = instance.Run(data)
print(val)
print('\n'.join([ExpandEquation(x) for x in equations]))
print(sum([' which is 1' in ExpandEquation(x) for x in equations]))

