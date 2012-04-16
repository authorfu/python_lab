#!/usr/bin/env python
#-*- coding:utf-8 -*-

import threading
import inspect
import ctypes
import time

def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                  ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")
        
class Worker(threading.Thread):
    '''工人，负责完成任务列表中的任务'''

    def __init__(self, boss):
        threading.Thread.__init__(self)
        self.boss = boss
        self._stop_signal = threading.Event()
        self.working = False
        
    def run(self):
        while True:
            if self._stop_signal.isSet():
                break

            self.job = self.boss.dispatch_job()
            if self.job:
                self.working = True
                self.job.do()
                self.working = False
                self.boss.finish_one_job()
                self.job = None

    def stop(self):
        self._stop_signal.set()

    def is_working(self):
        return self.working

    def is_doing_long_job(self, expected):
        return (time.time() - self.job.start_at) > expected 

    def report_and_quit(self):
        print 'cost time %f' %(time.time() - self.job.start_at)
        print self.job

class KillableWorker(Worker):
    '''工人，负责完成任务列表中的任务'''
    def __worker_id(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")
        
    def killme(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        _async_raise( self.__worker_id(), exctype )



