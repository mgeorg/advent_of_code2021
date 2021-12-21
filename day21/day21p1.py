#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Dice(object):
  def __init__(self):
    self.current_num = 1
    self.roll_id = 0

  def GetNum(self):
    ret = self.current_num
    self.current_num += 1
    self.roll_id += 1
    if self.current_num >= 101:
      self.current_num = 1
    return ret

  def RollId(self):
    return self.roll_id

class Game(object):
  def __init__(self, p1_init, p2_init):
    self.dice = Dice()
    self.p1_loc = p1_init
    self.p2_loc = p2_init
    self.p1_score = 0
    self.p2_score = 0

  def PlayRound(self):
    self.p1_loc += self.dice.GetNum() + self.dice.GetNum() + self.dice.GetNum()
    self.p1_loc = self.p1_loc % 10
    self.p1_score += 10 if self.p1_loc == 0 else self.p1_loc
    if self.p1_score >= 1000:
      return True
    self.p2_loc += self.dice.GetNum() + self.dice.GetNum() + self.dice.GetNum()
    self.p2_loc = self.p2_loc % 10
    self.p2_score += 10 if self.p2_loc == 0 else self.p2_loc
    if self.p2_score >= 1000:
      return True
    return False

  def LosingScore(self):
    if self.p1_score > self.p2_score:
      return self.p2_score
    return self.p1_score

  def Play(self):
    while not self.PlayRound():
      pass
    return self.LosingScore() * self.dice.RollId()

g = Game(7, 8)
print(g.Play())
