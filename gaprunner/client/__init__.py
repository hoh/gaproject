'''
Used in the Queue system to add new jobs to the queue.
'''

import logging

from gaproject.store import Store

logging.basicConfig(level=logging.DEBUG)


class Client(object):

    _default = {
        'operators': {
            'name': 'default',
            'evaluate': 'eval_simple',
            # 'mutate': ('insert_mut', {'indpb': 0.05}),
            'mutate': ('meta_insert', {'indpb': 0.05}),
            'mate': 'cxNull',
            'population': 20,
            'generations': 1000,
            'select': ('selTournament', {'tournsize': 1}),
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
        id_ = self.queue.insert(job)
        logging.debug('insertion done')
        return id_

    def validate(self, job):
        'Checks if the required keys are present in the job.'
        operators = job['operators']
        for key in ('population', 'generations'):
            if key not in operators:
                raise ValueError('Validation failed on {}'.format(key))

    def input_job(self):
        "Asks for a job using raw_input."
        # Creating new job:
        job = self._default.copy()

        # Getting user-defined operators:
        ops = self._default['operators']
        operators = {}

        for key in ops:
            val = ops[key]
            typ = type(val)

            # Allows input for base types:
            if typ in (str, int, float, long):
                while 1:
                    try:
                        value = raw_input('{} [{}]: '.format(key, val))
                        operators[key] = typ(value) if value else val
                        break
                    except ValueError, error:
                        print 'Error:', error

        job['operators'] = operators
        self.add_job(job)

