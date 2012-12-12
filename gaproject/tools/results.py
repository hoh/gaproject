
from prettytable import PrettyTable
from gaproject.store import Store


class Results(object):

    def __init__(self):
        self.s = Store()

    def print_(self):
        '''Prints all elements in the DB (limiting printed keys to a subset).
        '''

        table = PrettyTable([
            'name', 'fitness', 'population', 'generations'
            ])

        for run in self.s.runs.find():
            table.add_row([
                run['set']['name'],
                run['fitness'],
                run['set']['population'],
                run['set']['generations'],
                ])

        print table


