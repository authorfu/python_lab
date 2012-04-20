#!/usr/bin/python
# coding:utf-8

import Queue
import time

import workers 
import logger

class Job(object):

    def __init__(self, process, *args, **kwargs):
        self.process = process
        self.args = args
        self.kwargs = kwargs

    def do(self):
        try:
            self.start_at = time.time()
            self.result = self.process(*self.args, **self.kwargs)
            self.duration = time.time() - self.start_at
        except Exception, e:
            self.handle_exception(e) 

    def handle_exception(self, exception):
        print exception
    
    @property
    def to_now(self):
        return time.time() - self.start_at

class NoIdleWorkerException(Exception):pass        

class NormalManager(object):
    
    worker_class = workers.Worker
    
    def __init__(self, num_of_workers=10, job_size = 30, poll=5, max_wait_time=100):
        self._num_of_workers = num_of_workers
        self._job_queue = Queue.Queue(job_size) 
        self._job_in_process = Queue.Queue()
        self.workers = []
        self.poll = poll
        self.max_wait_time = max_wait_time
        
        for i in range(self._num_of_workers):
            self.workers.append(self.worker_class(self))
        
        logger.info('''A worker manager is created, %d workers supplied,\n
                a job's max wait time is %f, poll time is %f''' 
                %(len(self.workers), self.max_wait_time, self.poll))

    def put_job(self, job, block=True, timeout=10):
        #todo : job类型检查，确定是Job的子类
        try:
            self._job_queue.put(job, block, timeout)
        except Queue.Full, e:
            logger.warning('All workers are busy now, more workers are needed!')
            raise NoIdleWorkerException('There is no idle worker now!')

    def getback_failed_job(self, job, block=True, timeout=10):
        self.put_job(job, block, timeout)

    def dispatch_job(self, block=True, timeout=10):
        try:
            job = self._job_queue.get(block, timeout)
            self._job_in_process.put(1)
            return job
        except Queue.Empty:
            logger.info('There is no job')
            return None

    def finish_one_job(self):
        try:
            self._job_in_process.get_nowait()
        except Queue.Empty:
            pass

    def start(self):
        logger.info('%d workers will start working' %len(self.workers))

        for worker in self.workers:
            worker.start()

        while True:
            try:
                logger.debug('there is %d jobs' %self._job_in_process.qsize())
                time.sleep(self.poll)
                self.check_terrible_worker()
                if self._job_in_process.empty():
                    self.stop()
                    break
            except:
                raise
    
    def check_terrible_worker(self):
        count = 1
        for worker in self.workers:
            if(worker.is_working() and worker.is_doing_long_job(self.max_wait_time)):
                self.handle_terrible_worker(worker)
                count += 1
        logger.warning('有%d个工作者超时工作，最长期望时间为%f' %(count, self.max_wait_time))

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
