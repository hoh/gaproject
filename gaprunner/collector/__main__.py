
from gaprunner.collector.__init__ import Collector

if __name__ == '__main__':

    def print_job(job):
        'Example of callback function.'
        # Doing random stuff:
        print 'Job =', job

        # Updating the status of the job:
        job['status'] = 'collected'
        return job

    collector = Collector(callback=print_job)
    collector.loop()
