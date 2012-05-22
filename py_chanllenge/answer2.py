#!/usr/bin/python
# coding:utf-8

import os

print __file__

cwd = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(cwd, 'mess.txt'), 'r') as f:
    s = f.readlines()

s = ''.join(s)

counter = {}

for c in s:
    if c not in counter:
        counter[c] = 0
    counter[c] += 1 


