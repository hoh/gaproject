
from gaprunner.client import Client
from gaprunner.collector import Collector


class Coach(object):
    """Helps running jobs on different machines and calls a callback when it's finished."""

    def __init__(self, jobs, on_result=None):
        '* on_result: callback when a new result is available.'
        self.jobs = jobs
        self.on_result = on_result
        self.results = []

        self.job_ids = []

        client = Client()
        for job in jobs:
            _id = client.add_job(job)
            self.job_ids.append(_id)

    def loop(self, bg=False):
        'bg: executing in the background, in a new Python thread.'
        filters = [{'_id': _id, 'status': 'done'} for _id in self.job_ids]
        collector = Collector(self.job_collected, filters=filters)
        collector.loop(bg=bg)
        return self.results

    def job_collected(self, job):
        'Callback function when a job is collected.'
        print 'Job collected', job
        self.results.append(job)
        if self.on_result:
            self.on_result(job)
