'''
Used in the Queue system to analyze results.

The method 'process' of the Collector receives all new jobs that
have finished running. This is the entry point for analysis.
'''

import time
import thread
import logging

from gaproject.store import Store

logging.basicConfig(level=logging.DEBUG)


class Collector(object):

    # Seconds between each job search
    DELAY = 0.5

    def __init__(self, callback=None, filters=({'status': 'done'},), stop=True):
        '''
        * callback : function be called with the job
        * filter : filter to select elements to be processed
        * stop : stops after len(filters) results
        '''
        self.store = Store()
        self.queue = self.store.queue
        self.callback = callback
        self.filters = filters

        self.counter = len(filters) if stop else -1

    def find_jobs(self, filter):
        "Finds a completed job in the queue."
        cursor = self.queue.find(filter)
        return cursor

    def update_job(self, job):
        "Updates the job to the new value in the DB."
        # job['status'] = 'collected'
        self.queue.save(job)

    def run(self):
        for filter in self.filters:
            for job in self.find_jobs(filter):
                if job is None:
                    continue

                logging.info('job collected')

                if self.callback:
                    job_callback = self.callback(job)
                    if job_callback is None:
                        job['status'] = 'collected'
                    else:
                        job = job_callback
                else:
                    job['status'] = 'collected'

                self.update_job(job)

                logging.info('counter = {}'.format(self.counter))
                self.counter -= 1
                if self.counter == 0:
                    return False  # Should stop
        return True  # Should keep trying

    def loop(self, bg=False):
        'Main loop during which the worker searches for a job.'
        logging.info('Collector started...')

        def loop():
            logging.debug('started loop')
            keep_running = self.run()
            while keep_running:
                time.sleep(self.DELAY)
                keep_running = self.run()

        if not bg:
            logging.debug('background = False')
            loop()
        else:
            logging.debug('background = True')
            thread.start_new_thread(loop, tuple())
