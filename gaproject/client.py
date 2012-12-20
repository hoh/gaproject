'''
Used in the Queue system to add new jobs to the queue.
'''

import logging

from gaproject.store import Store

logging.basicConfig(level=logging.DEBUG)


class Client(object):

    default = {
        'population': 100,
    }

    def __init__(self):
        self.store = Store()
        self.queue = self.store.queue

    def add_job(self, job):
        self.validate(job)
        logging.debug('validation passed')
        self.queue.insert(job)
        logging.debug('insertion done')

    def validate(self, job):
        assert 'population' in job

    def input_job(self):
        "Asks for a job using raw_input."
        job = {}
        for key in self.default:
            typ = type(self.default[key])
            while 1:
                try:
                    job[key] = typ(raw_input('{}: '.format(key)))
                    break
                except ValueError, error:
                    print 'Error:', error
        self.add_job(job)

if __name__ == '__main__':
    client = Client()
    client.input_job()
