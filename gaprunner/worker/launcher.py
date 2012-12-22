'''
Used in the Queue system to launch a job within a worker.

Aims at replacing run.py.
'''

import logging

import gaproject.sets
import gaproject.run

from gaproject.data import Box
import gaproject.shared as shared


def process(job):
    "Launches the given job."

    logging.info('running job {}'.format(job))

    box = Box('data/TSPBenchmark')
    shared.data = box.get(job['data'])

    if 'metaGA' in job:
        shared.settings.metaGA = job['metaGA']

    # TODO: Refactor the following:
    shared.orderedSequenceOfNodes = shared.data.nodesOrderedByMedian(shared.data.dist_matrix())

    operators = gaproject.sets.evaluate(job['operators'])
    result = gaproject.run.run(shared.data, operators)

    return result
