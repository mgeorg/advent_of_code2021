#!/usr/bin/python3

with open('input1.txt', 'r') as f:
  lines = f.read().splitlines()

count = 0
prev = None
for line in lines:
  line = line.strip()
  num = int(line)
  if prev is not None:
    if num - prev > 0:
      count += 1
  prev = num

print(count)
