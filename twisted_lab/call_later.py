#!/usr/bin/python
# coding:utf-8

from twisted.internet import reactor

import time

def print_time():
    print 'Current time is ', time.strftime('%H:%M:%S')

def stop_reactor():
    print 'Stopping reactor'
    reactor.stop()

for i in range(1, 4):
    reactor.callLater(i, print_time)

reactor.callLater(5, stop_reactor)

print 'Running the reactor...'

reactor.run()

print 'Reactor stopped.'
