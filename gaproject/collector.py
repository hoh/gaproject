'''
Used in the Queue system to analyze results.
'''

import time
import logging

from gaproject.store import Store

logging.basicConfig(level=logging.DEBUG)


class Collector(object):

    # Seconds between each job search
    DELAY = 0.5

    def __init__(self):
        self.store = Store()
        self.queue = self.store.queue

    def process(self, job):
        print 'Awesome, we got a result !'

    def find_jobs(self):
        "Finds a completed job in the queue."
        cursor = self.queue.find({'status': 'done'})
        return cursor

    def commit_job(self, job):
        "Sets the status of the job as committed."
        job['status'] = 'collected'
        self.queue.save(job)

    def run(self):
        for job in self.find_jobs():
            logging.info('job collected')
            self.process(job)
            self.commit_job(job)

    def loop(self):
        'Main loop during which the worker searches for a job.'
        logging.info('Collector started...')

        while 1:
            self.run()
            time.sleep(self.DELAY)

if __name__ == '__main__':
    collector = Collector()
    collector.loop()
