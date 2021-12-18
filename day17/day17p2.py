#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Shot(object):
  def __init__(self, vx, vy):
    self.hit = False
    self.target_x = (281, 311+1)
    self.target_y = (-74, -54+1)
    self.initial_vx = vx
    self.initial_vy = vy
    self.vx = vx
    self.vy = vy
    self.x = 0
    self.y = 0
    self.path = [(0, 0)]
    while self.y >= self.target_y[0]:
      self.Iterate()
      self.path.append((self.x, self.y))

  def Iterate(self):
    self.x += self.vx
    self.y += self.vy
    if self.vx == 0:
      pass
    elif self.vx < 0:
      self.vx += 1
    else:
      self.vx -= 1
    self.vy -= 1
    if (self.x >= self.target_x[0] and self.x < self.target_x[1]
        and self.y >= self.target_y[0] and self.y < self.target_y[1]):
      self.hit = True

  def Info(self):
    if self.hit:
      return (f'({self.initial_vx}, {self.initial_vy}) Hit! {self.path}')
    else:
      return (f'({self.initial_vx}, {self.initial_vy}) miss {self.path}')


vx = 0
vy = 0
while False:
  s = Shot(vx,vy)
  print(s.Info())
  next_shot = input('hjkl q> ')
  m = re.match(r'^(\d+)\s+(\d+)\s*$', next_shot)
  if m:
    vx = int(m.group(1))
    vy = int(m.group(2))
  elif next_shot  == 'j':
    vy -= 1
  elif next_shot  == 'k':
    vy += 1
  elif next_shot  == 'h':
    vx -= 1
  elif next_shot  == 'l':
    vx += 1
  elif next_shot  == 'q':
    break

# 24 73
# max height: 2701

hits = list()
for initial_x in range(313):
  for initial_y in range(-75, 75):
    s = Shot(initial_x,initial_y)
    if s.hit:
      hits.append(s)

print('\n'.join([s.Info() for s in hits]))
print(len(hits))


