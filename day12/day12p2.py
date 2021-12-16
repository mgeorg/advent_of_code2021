#!/usr/bin/python3

import collections
import copy
import numpy as np
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()


class Graph(object):
  def __init__(self):
    self.nodes = set()
    self.edges = list()

  def AddEdge(self, loc1, loc2):
    self.edges.append(tuple(sorted([loc1, loc2])))
    self.nodes.add(loc1)
    self.nodes.add(loc2)

  def MakeMaps(self):
    self.node_map = dict()
    for edge in self.edges:
      if edge[0] not in self.node_map:
        self.node_map[edge[0]] = list()
      self.node_map[edge[0]].append(edge[1])
      if edge[1] not in self.node_map:
        self.node_map[edge[1]] = list()
      self.node_map[edge[1]].append(edge[0])

  def GetPaths(self):
    self.MakeMaps()
    path_stack = collections.deque()
    path_stack.append((['start'], set(['start']), None))
    completed_paths = list()
    while len(path_stack) > 0:
      path, visited, extra = path_stack.popleft()
      for next_node in self.node_map[path[-1]]:
        if next_node == 'end':
          completed_paths.append(path + [next_node])
          continue
        if next_node == 'start':
          continue
        if re.match(r'^[a-z]+$', next_node):
          # next_node is small
          if next_node not in visited:
            # Not yet visited this one.
            new_visited = copy.copy(visited)
            new_visited.add(next_node)
            path_stack.append((path + [next_node], new_visited, extra))
          elif extra is None:
            # Choose to visit this small cave twice.
            path_stack.append((path + [next_node], visited, next_node))
        else:
          # large nodes can be visited regardless.
          path_stack.append((path + [next_node], visited, extra))
    for path in sorted(completed_paths):
      print(','.join(path))
    print(len(completed_paths))

g = Graph()

for line in lines:
  m = re.match(r'^([^-]+)-([^-]+)$', line)
  assert m
  loc1 = m.group(1)
  loc2 = m.group(2)
  g.AddEdge(loc1, loc2)

g.GetPaths()

