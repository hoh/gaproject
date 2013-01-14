

import copy
import json

from os.path import expanduser, join

from gaprunner.coach import Coach
import gaproject.shared as shared
from gaproject.tools.results import RunTable


def make_job(base, new_operators):
    '''Returns a copy of the 'base' job, updated with the
    new_operators given.
    '''
    job = copy.deepcopy(base)
    # Resetting the status of the job, in case we reuse a result:
    job['status'] = 'available'
    job['operators'].update(new_operators)
    return job


def job_data(job):
    # Directory where the results have been saved:
    data_path = join(shared.settings.filesDir, str(job['_id']), 'data.json')
    return json.load(open(data_path))


class Analyzer(object):
    '''Abstract class for Analyzers.
    Provides launch(jobs) and print_job(job, data).
    '''

    def launch(self, jobs, on_result=None):
            coach = Coach(jobs, on_result)
            return coach.loop(bg=False)

    def print_job(self, job, data):
        print 'Best run so far:'
        table = RunTable()
        table.add_run(job, data)
        print table
