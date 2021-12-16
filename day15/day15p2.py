#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Cave(object):
  def __init__(self, lines):
    self.map = list()
    for line in lines:
      self.map.append([int(x) for x in line.strip()])
      assert len(self.map[-1]) == len(self.map[0])
    assert len(self.map[0]) == len(self.map)
    self.max_size = len(self.map)
    new_map = list()
    for i in range(5*self.max_size):
      new_map.append([0] * 5*self.max_size)
    for i in range(5):
      for j in range(5):
        for x in range(self.max_size):
          for y in range(self.max_size):
            new_map[x+i*self.max_size][y+j*self.max_size] = (
                self.map[x][y] + i + j - 1) % 9 + 1
    self.map = new_map
    self.max_size = len(new_map)
    for i in range(self.max_size):
      print(''.join([str(x) for x in self.map[i]]))
        

  def FindPath(self):
    q = queue.PriorityQueue()
    found_paths = dict()
    q.put((0, (0,0)))
    while not q.empty():
      cost, coordinate = q.get()
      neighbors = [(coordinate[0]-1, coordinate[1]),
                   (coordinate[0], coordinate[1]-1),
                   (coordinate[0]+1, coordinate[1]),
                   (coordinate[0], coordinate[1]+1)]
      for new_x, new_y in neighbors:
        if (new_x < 0 or new_x >= self.max_size or
            new_y < 0 or new_y >= self.max_size):
          continue
        if (new_x, new_y) in found_paths:
          continue
        new_cost = cost + self.map[new_x][new_y]
        q.put((new_cost, (new_x, new_y)))
        found_paths[(new_x, new_y)] = new_cost
    # print(found_paths)
    print(found_paths[(self.max_size-1, self.max_size-1)])

c = Cave(lines)
c.FindPath()


