#!/usr/bin/python3

with open('input1.txt', 'r') as f:
  lines = f.read().splitlines()

count = 0
a = None
b = None
c = None
prev = None
num = None
for line in lines:
  line = line.strip()
  c = int(line)
  if a is not None:
    num = a + b + c
  if prev is not None:
    if num - prev > 0:
      count += 1
  a = b
  b = c
  prev = num

print(count)
