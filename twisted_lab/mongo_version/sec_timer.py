#!/usr/bin/python
# coding:utf-8

from time import time

def loop_in_sec(duration = 1):
    start = time()
    count = 1
    while (time() - start) < duration:
        yield count
        count += 1

