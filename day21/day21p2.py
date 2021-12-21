#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class UniverseState(object):
  def __init__(self, p1_loc, p1_score, p2_loc, p2_score):
    self.p1_loc = p1_loc
    self.p1_score = p1_score
    self.p2_loc = p2_loc
    self.p2_score = p2_score

  def __hash__(self):
     return hash((self.p1_loc, self.p1_score, self.p2_loc, self.p2_score))

  def __eq__(self, other):
     return ( (self.p1_loc, self.p1_score, self.p2_loc, self.p2_score) ==
              (other.p1_loc, other.p1_score, other.p2_loc, other.p2_score) )

  def __str_(self):
     return 'UniverseState' + str(
         (self.p1_loc, self.p1_score, self.p2_loc, self.p2_score))

  def __repr__(self):
     return 'UniverseState' + repr(
         (self.p1_loc, self.p1_score, self.p2_loc, self.p2_score))


increase_outcomes = [
  (3, 1),  # 1 1 1
  (4, 3),  # (1 1 2), (1 2 1), (2 1 1),
  (5, 6),  # (1 2 2), (2 1 2), (2 2 1), (1 1 3), (1 3 1), (3 1 1),
  (6, 7),  # (2 2 2), (3 1 2), (3 2 1), (1 3 2), (2 3 1), (1 2 3), (2 1 3),
  (7, 6),  # (3 2 2), (2 3 2), (2 2 3), (3 3 1), (3 1 3), (1 3 3),
  (8, 3),
  (9, 1),
]

class Game(object):
  def __init__(self, p1_init, p2_init):
    self.universes = dict()
    self.universes[UniverseState(p1_init, 0, p2_init, 0)] = 1
    self.p1_wins = 0
    self.p2_wins = 0

  def Play(self):
    while self.universes:
      self.Roll()

  def Roll(self):
    print('Roll')
    new_universes = dict()
    for universe_state, num_univ in self.universes.items():
      print(f'universe_state {universe_state} {num_univ}')
      for increase, increase_univ_factor in increase_outcomes:
        offshoot = copy.copy(universe_state)
        offshoot.p1_loc += increase
        offshoot.p1_loc = offshoot.p1_loc % 10
        new_universes[offshoot] = (
            new_universes.get(offshoot, 0) + increase_univ_factor * num_univ)
    print(f'{new_universes}')
    self.universes = new_universes
    new_universes = dict()
    for universe_state, num_univ in self.universes.items():
      offshoot = copy.copy(universe_state)
      offshoot.p1_score += 10 if offshoot.p1_loc == 0 else offshoot.p1_loc
      if offshoot.p1_score >= 21:
        self.p1_wins += num_univ
      else:
        new_universes[offshoot] = num_univ
    print(f'{new_universes}')
    self.universes = new_universes
    new_universes = dict()
    for universe_state, num_univ in self.universes.items():
      for increase, increase_univ_factor in increase_outcomes:
        offshoot = copy.copy(universe_state)
        offshoot.p2_loc += increase
        offshoot.p2_loc = offshoot.p2_loc % 10
        new_universes[offshoot] = (
            new_universes.get(offshoot, 0) + increase_univ_factor * num_univ)
    self.universes = new_universes
    new_universes = dict()
    for universe_state, num_univ in self.universes.items():
      offshoot = copy.copy(universe_state)
      offshoot.p2_score += 10 if offshoot.p2_loc == 0 else offshoot.p2_loc
      if offshoot.p2_score >= 21:
        self.p2_wins += num_univ
      else:
        new_universes[offshoot] = num_univ
    self.universes = new_universes

# gs = Game(4, 8)
# gs.Play()
# print((gs.p1_wins, gs.p2_wins))

gs = Game(7, 8)
gs.Play()
print((gs.p1_wins, gs.p2_wins))

