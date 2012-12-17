import gaproject.run
from numpy import average
from gaproject.tools.results import Results, RunTable


class Launcher(object):
    'Class to launch a list of jobs and plot/print the resuts.'

    def clear(self):
        self.store = gaproject.store.Store()
        self.store.runs.remove({})
        self.store.jobs.remove({})

    def load_data(self, data):
        self.data = data

    def launch_queue(self, jobs, plot_all):
        'Launches a queue of jobs and returns the best result.'
        self.store.runs.remove({})
        self.store.jobs.remove({})

        for job in jobs:
            self.store.jobs.insert(job)

        # 3.
        gaproject.run.main(self.data)

        # 4.
        results = Results()
        results.print_()
        if plot_all:
            results.plotDifferentRuns()

        best = results.find_one()
        best_avg = average(best['fitness'])
        for run in results.find():
            run_avg = average(run['fitness'])
            if run_avg < best_avg:
                best = run
                best_avg = run_avg

        print 'Best run so far:'
        table = RunTable()
        table.add_run(best)
        print table

        return best
