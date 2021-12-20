#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

all_rotations = list()
for a in [1, -1]:
  for b in [1, -1]:
    for c in [1, -1]:
      arr = np.array(((a, 0, 0),
                      (0, b, 0),
                      (0, 0, c)))
      if np.linalg.det(arr) == 1:
        all_rotations.append(arr)
      arr = np.array(((a, 0, 0),
                      (0, 0, c),
                      (0, b, 0)))
      if np.linalg.det(arr) == 1:
        all_rotations.append(arr)
      arr = np.array(((0, b, 0),
                      (a, 0, 0),
                      (0, 0, c)))
      if np.linalg.det(arr) == 1:
        all_rotations.append(arr)
      arr = np.array(((0, 0, c),
                      (a, 0, 0),
                      (0, b, 0)))
      if np.linalg.det(arr) == 1:
        all_rotations.append(arr)
      arr = np.array(((0, b, 0),
                      (0, 0, c),
                      (a, 0, 0)))
      if np.linalg.det(arr) == 1:
        all_rotations.append(arr)
      arr = np.array(((0, 0, c),
                      (0, b, 0),
                      (a, 0, 0)))
      if np.linalg.det(arr) == 1:
        all_rotations.append(arr)

class Scanner(object):
  def __init__(self):
    self.coords = list()

  def AddBeacon(self, x, y, z):
    self.coords.append((x,y,z))

  def SetOrientation(self, orientation_index):
    self.current_coords = list()
    for c in self.coords:
      self.current_coords.append(
          np.matmul(all_rotations[orientation_index], c))
    self.offset_map = set()
    for i1, c1 in enumerate(self.current_coords):
      for i2, c2 in enumerate(self.current_coords):
        if i1 == i2:
          continue
        self.offset_map.add(tuple(c1 - c2))

  def __str__(self):
    return '\n'.join(str(list(x)) for x in self.current_coords)

scanners = list()
for line in lines:
  m = re.match(r'--- scanner \d+ ---$', line)
  if m:
    scanners.append(Scanner())
    continue
  if line.strip() == '':
    continue
  m = re.match(r'([\d-]+),([\d-]+),([\d-]+)$', line)
  assert m
  scanners[-1].AddBeacon(int(m.group(1)),int(m.group(2)),int(m.group(3)))
  
scanners[0].SetOrientation(0)
# print(str(scanners[0]))

def MatchScanners(ref, other):
  huristic = 0
  for offset_huristic in other.offset_map:
    if offset_huristic in ref.offset_map:
      huristic += 1
  if huristic <= 12:
    return (False, None)
  for i in range(len(ref.current_coords)-11):
    for j in range(len(other.current_coords)-11):
      # Match up beacon i in ref with beacon j in other and see how many
      # other beacons match.
      a = ref.current_coords[i]
      b = other.current_coords[j]
      offset = b - a
      match_count = 0
      for ref_beacon in ref.current_coords:
        for other_beacon in other.current_coords:
          if (ref_beacon + offset == other_beacon).all():
            match_count += 1
      if match_count > 1:
        print(match_count)
      if match_count >= 12:
        return (True, offset)
  return (False, None)

scanner_parameters = [None] * len(scanners)
scanner_parameters[0] = (0, 0, np.array([0,0,0]))
scanner_index_queue = collections.deque([0])
# while False:
while scanner_index_queue:
  ref_scanner_index = scanner_index_queue.popleft()
  ref_scanner = scanners[ref_scanner_index]
  for search_scanner_index in range(len(scanners)):
    if scanner_parameters[search_scanner_index] is not None:
      continue
    if search_scanner_index == ref_scanner_index:
      continue
    for orientation_index in range(24):
      print(f'trying {search_scanner_index} vs {ref_scanner_index} with '
            f'orientation {orientation_index}')
      scanners[search_scanner_index].SetOrientation(orientation_index)
      matched, offset = MatchScanners(
          ref_scanner, scanners[search_scanner_index])
      if matched:
        print(f'matched {search_scanner_index} vs {ref_scanner_index} with '
              f'orientation {orientation_index} and offset {offset}')
        scanner_parameters[search_scanner_index] = (
            ref_scanner_index, orientation_index,
            scanner_parameters[ref_scanner_index][2] - offset)
        scanner_index_queue.append(search_scanner_index)
        # Leave the scanner in the matched orientation.
        break

print(scanner_parameters)

for i, s in enumerate(scanners):
  s.SetOrientation(scanner_parameters[i][1])

beacons = set()
for i in range(len(scanners)):
  offset = scanner_parameters[i][2]
  for c in scanners[i].current_coords:
    beacons.add(tuple(c + offset))

print(beacons)
print(len(beacons))

max_dist = 0
for i in range(len(scanners)):
  for j in range(i+1, len(scanners)):
    dist = sum(abs(scanner_parameters[i][2] - scanner_parameters[j][2]))
    if dist > max_dist:
      max_dist = dist

print(max_dist)
