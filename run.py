from main import Relation
from prettytable import PrettyTable
from GoodShit import GoodShit

R1 = Relation('R1', 1000, {
            'rows_identifiers': ['SIZE', 'VAL'],
            'columns_identifiers': ['Property', 'A', 'B']
        })
R1.populate_table([[4, 4], [200, 50]])

R2 = Relation('R2', 1000, {
            'rows_identifiers': ['SIZE', 'VAL'],
            'columns_identifiers': ['Property', 'A', 'B']
        })
R2.populate_table([[4, 4], [40, 100]])

R3 = Relation('R3', 2000, {
            'rows_identifiers': ['SIZE', 'VAL'],
            'columns_identifiers': ['Property', 'B', 'D']
        })
R3.populate_table([[4, 4], [400, 100]])

R4 = Relation('R4', 1000, {
            'rows_identifiers': ['SIZE', 'VAL'],
            'columns_identifiers': ['Property', 'B', 'E']
        })
R4.populate_table([[4, 4], [200, 50]])

relations = {
    'R1': R1,
    'R2': R2,
    'R3': R3,
    'R4': R4
}

domains = {
    'A': 400,
    'B': 500
}

sigma_attributes = ['R1.A', 'R2.A', 'R2.B', 'R3.B', 'R4.B']


semi_joins = \
                ['R1 A R2',
                 'R2 A R1',
                 'R2 B R3',
                 'R3 B R2',
                 'R3 B R4',
                 'R4 B R3',
                 'R2 B R4',
                 'R4 B R2']

good = GoodShit(relations, domains, sigma_attributes, semi_joins)
good.loop_iterations(5)