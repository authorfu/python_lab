#!/usr/bin/python
# coding:utf-8

import threading
import Queue
import time

import workers 

class Job(object):

    def __init__(self, process, *args, **kwargs):
        self.process = process
        self.args = args
        self.kwargs = kwargs

    def do(self):
        try:
            self.result = self.process(*self.args, **self.kwargs)
        except Exception, e:
            self.handle_exception(e) 

    def handle_exception(self, exception=None):
        print exception

class NormalManager(object):
    
    worker_class = workers.Worker
    
    def __init__(self, num_of_workers=10, job_size = 30, poll=5, max_wait_time=100):
        self._num_of_workers = num_of_workers
        self._job_queue = Queue.Queue(job_size) 
        self._job_in_process = Queue.Queue()
        self.workers = []
        self.poll = 5
        self.max_wait_time = max_wait_time
        
        for i in range(self._num_of_workers):
            self.workers.append(self.worker_class(self))

    def put_job(self, job, block=True, timeout=10):
        #todo : job类型检查，确定是Job的子类
        self._job_queue.put(job, block, timeout)

    def getback_failed_job(self, job, block=True, timeout=10):
        self.put_job(job, block, timeout)

    def dispatch_job(self, block=True, timeout=10):
        try:
            job = self._job_queue.get(block, timeout)
            self._job_in_process.put(1)
            return job
        except Queue.Empty:
            return None

    def finish_one_job(self):
        try:
            self._job_in_process.get_nowait()
        except Queue.Empty:
            pass

    def start(self):
        for worker in self.workers:
            worker.start()
        while True:
            try:
                print 'there is %d jobs' %self._job_in_process.qsize()
                print 'there is %d busy worker' %len([w for w in self.workers if w.is_working()])
                time.sleep(self.poll)
                self.check_terrible_worker()
                if self._job_in_process.empty():
                    self.stop()
                    break
            except:
                raise
    
    def check_terrible_worker(self):

        for worker in self.workers:
            if(worker.is_working() and worker.is_doing_long_job(self.max_wait_time)):
                self.handle_terrible_worker(worker)
                
    def handle_terrible_worker(self, worker):
        worker.report_and_quit()
                    
    def stop(self):
        for worker in self.workers:
            worker.stop()


class CrudeManager(NormalManager):
    worker_class = workers.KillableWorker
    
    def handle_terrible_worker(self, worker):
        
        while worker.isAlive():
            time.sleep(0.2)
            worker.raiseExc(Exception)

def test():
    worker_manager = CrudeManager(20)
    def just_print(num):
        print 'just print %d' %num

    jobs = []
    for i in range(10):
        jobs.append(Job(just_print, i))
    
    for job in jobs:
       worker_manager.put_job(job)

    worker_manager.start()

if __name__ == '__main__':
    test()
