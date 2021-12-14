#!/usr/bin/python3

import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

commands = []
for line in lines:
  m = re.match(r'^(\w+)\s+(\d+)$', line)
  assert m
  command = m.group(1)
  num = int(m.group(2))
  commands.append((command, num))

cur_depth = 0
cur_aim = 0
cur_pos = 0
for command, num in commands:
  if command == 'forward':
    cur_pos += num
    cur_depth += num * cur_aim
  elif command == 'down':
    cur_aim += num
  elif command == 'up':
    cur_aim -= num

print(cur_depth * cur_pos)
