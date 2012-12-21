'''
Used in the Queue system to add new jobs to the queue.
'''

import logging

from gaproject.store import Store

logging.basicConfig(level=logging.DEBUG)


class Client(object):

    _default = {
        'operators': {
            'population': 100,
            },

        'status': 'available',
        'data': 'belgiumtour.tsp',
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
        assert 'population' in job['operators']

    def input_job(self):
        "Asks for a job using raw_input."
        # Creating new job:
        job = self._default.copy()

        # Getting user-defined operators:
        ops = self.default['operators']
        operators = {}

        for key in ops:
            val = ops[key]
            typ = type(val)
            while 1:
                try:
                    value = raw_input('{} [{}]: '.format(key, val))
                    operators[key] = typ(value) if value else val
                    break
                except ValueError, error:
                    print 'Error:', error

        job['operators'] = operators
        self.add_job(job)

if __name__ == '__main__':
    client = Client()
    client.input_job()
