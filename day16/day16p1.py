#!/usr/bin/python3

import collections
import copy
import heapq
import numpy as np
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

binary_for_hex = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

assert len(lines) == 1
binary_sequence = ''.join([binary_for_hex[x] for x in lines[0]])
print(binary_sequence)

def BinaryStringToInt(string):
  num = 0
  for char in string:
    num *= 2
    if char == '1':
      num += 1
  return num
      

class Packet(object):
  def __init__(self, binary_sequence, start_pos):
    self.binary_sequence = binary_sequence
    self.start_pos = start_pos
    self.version = BinaryStringToInt(
        self.binary_sequence[start_pos:start_pos+3])
    self.type_id = BinaryStringToInt(
        self.binary_sequence[start_pos+3:start_pos+6])
    if self.type_id == 4:
      self.current_pos = start_pos+6
      self.literal = 0
      continue_read = True
      while continue_read:
        continue_read = self.binary_sequence[self.current_pos] == '1'
        self.literal *= 16
        self.literal += BinaryStringToInt(
                self.binary_sequence[self.current_pos+1:self.current_pos+5])
        self.current_pos += 5
    else:
      self.current_pos = start_pos+6
      self.length_type = BinaryStringToInt(
          self.binary_sequence[self.current_pos])
      self.current_pos += 1
      if self.length_type == 0:
        self.total_length = BinaryStringToInt(
                self.binary_sequence[self.current_pos:self.current_pos+15])
        self.current_pos += 15
        self.subpackets = list()
        target_last_pos = self.current_pos + self.total_length
        while self.current_pos != target_last_pos:
          self.subpackets.append(Packet(binary_sequence, self.current_pos))
          self.current_pos = self.subpackets[-1].current_pos
      else:
        self.total_packets = BinaryStringToInt(
                self.binary_sequence[self.current_pos:self.current_pos+11])
        self.current_pos += 11
        self.subpackets = list()
        for i in range(self.total_packets):
          self.subpackets.append(Packet(binary_sequence, self.current_pos))
          self.current_pos = self.subpackets[-1].current_pos

  def Info(self):
    if self.type_id == 4:
      return f'{self.start_pos}-{self.current_pos}, {self.version}, {self.type_id}: Literal {self.literal}'
    output = (f'{self.start_pos}-{self.current_pos}, {self.version}, '
              f'{self.type_id}: '
              f'Operator {self.length_type}')
    for subpacket in self.subpackets:
      output += '\n  ' + subpacket.Info().replace('\n', '\n  ')
    return output

  def VersionSum(self):
    if self.type_id == 4:
      return self.version
    total = self.version
    for subpacket in self.subpackets:
      total += subpacket.VersionSum()
    return total

p = Packet(binary_sequence, 0)
print(p.Info())
print(p.VersionSum())

