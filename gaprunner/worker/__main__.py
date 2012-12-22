'''
Used in the Queue system to process jobs from the queue.

A worker will search for new jobs to execute and launch them,
then put the result in the database.
'''

import os
import json
import time
import logging
import random

from gaproject.store import Store
import gaprunner.worker.launcher as launcher

logging.basicConfig(level=logging.DEBUG)

# Directory where the results will be saved:
RESULTS_DIRECTORY = os.path.expanduser('~/GAP_results')

# Creating output directory if it does not exist:
if not os.path.isdir(RESULTS_DIRECTORY):
    os.mkdir(RESULTS_DIRECTORY)


class Worker(object):

    # Seconds between each job search
    DELAY = 0.5

    def __init__(self):
        self.store = Store()
        self.queue = self.store.queue

    def worker_name(self):
        "Returns the worker's name (machine name + pid)."
        name = '{}-{}'.format(os.uname()[1], os.getpid())
        logging.debug('name: {}'.format(name))
        return name

    def find_job(self):
        "Finds a job in the queue."
        job = self.queue.find_one({'status': 'available'})
        return job

    def lock_job(self, job):
        "Assigns this worker for the job in the queue."
        job['status'] = 'running'
        job['worker'] = self.worker_name()
        self.queue.save(job)

    def commit_job(self, job):
        "Sets the status of the job as committed."
        job['status'] = 'done'
        self.queue.save(job)

    def save_result(self, job, result):
        "Pushes the result of a run in the DB."
        out_dir = os.path.join(RESULTS_DIRECTORY, unicode(job['_id']))
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)

        # Saving results as JSON file on disk:
        data_out = open(os.path.join(out_dir, 'data.json'), 'w')
        json.dump(result, data_out)

        # Saving job as JSON file on disk:
        job_out = open(os.path.join(out_dir, 'job.json'), 'w')
        # Converting job _id to string:
        jobb = job.copy()
        jobb['_id'] = str(job['_id'])
        json.dump(jobb, job_out)

    def process(self, job):
        "Processes the given job."
        result = launcher.process(job)
        logging.info('processed')
        return result

    def run(self):
        job = self.find_job()
        if job:
            logging.info('job found')
            self.lock_job(job)
            result = self.process(job)
            self.save_result(job, result)
            self.commit_job(job)

    def loop(self):
        'Main loop during which the worker searches for a job.'
        logging.info('Worker started...')

        # Sleeping a random duration to limit concurrent DB access:
        time.sleep(random.random())

        while 1:
            self.run()
            time.sleep(self.DELAY)


if __name__ == '__main__':
    worker = Worker()
    worker.loop()
