import copy
from prettytable import PrettyTable

from GoodShit import GoodShit
from Relation import Relation


def get_size(relations_list, relation, variable):
    return relations_list[relation]['SIZE', variable]

def get_sf(relation, variable, sf_table):
    return sf_table[relation + '.' + variable, 'SF']

def get_val(relations_list, relation, variable):
    return relations_list[relation]['VAL', variable]

class Relation:
    def __init__(self, id, cardinal, relation_table_schema):
        self.relation_table_schema = relation_table_schema
        self.id = id
        self.cardinal = cardinal
        self.hash_table = HashTable(self.relation_table_schema['rows_identifiers'],
                               self.relation_table_schema['columns_identifiers'])

    def populate_table(self, data):
        self.hash_table.populate(data)

    # def build_table(self, columns, rows):
    #     self.table = PrettyTable(columns)
    #     for row in rows:
    #         self.table.add_row(row)

    def __getitem__(self, item):
        row, col = item
        return self.hash_table.table[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.hash_table.table[row][col] = value

    def __str__(self):
        return str(self.id + '\n' + self.hash_table.__str__() + '\n')

    #def get(self, row, column):

class HashTable:
    def __init__(self, row_identifiers, column_identifiers):
        self.row_identifiers = row_identifiers
        self.column_identifiers = column_identifiers
        self.table = {}

        for row_name in row_identifiers:
            self.table[row_name] = {}


    def populate(self, data):
        for values_list, row_name in zip(data, self.row_identifiers):
            for value, column_name in zip(values_list, self.column_identifiers[1:]):
                self.table[row_name][column_name] = value

    def __str__(self):
        pretty_table = PrettyTable(self.column_identifiers)
        for row_name in self.row_identifiers:
            row = [row_name]
            for column_name in self.column_identifiers[1:]:
                row.append(self.table[row_name][column_name])
            pretty_table.add_row(row)
        return str(pretty_table)

    def __getitem__(self, item):
        row, col = item
        return self.table[row][col]

    def __setitem__(self, key, value):
        self.table[key] = value


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

in_domains = {
    'A': 400,
    'B': 500
}

in_attributes = ['R1.A', 'R2.A', 'R2.B', 'R3.B', 'R4.B']


in_semi_joins_codes = \
                ['R1 A R2',
                 'R2 A R1',
                 'R2 B R3',
                 'R3 B R2',
                 'R3 B R4',
                 'R4 B R3',
                 'R2 B R4',
                 'R4 B R2']

excluded_indexes = []
while True:
    factors = HashTable(in_attributes, ['Atrybut', 'SF'])
    factors_to_populate = []
    for attribute in in_attributes:
        rel_id = attribute.split('.')[0]
        rel_field = attribute.split('.')[1]
        factors_to_populate.append([relations[rel_id]['VAL', rel_field] / in_domains[rel_field]])

        # relations[rel_id][attribute, 'SF'] = relations[rel_id]['VAL', rel_field] / in_domains[rel_field]
    factors.populate(factors_to_populate)
    print(factors)
    sigmas = factors

    semi_joins = HashTable(in_semi_joins_codes, ['Join', 'KOSZT', 'EFEKT', 'ZYSK'])
    semi_joins_rows = []
    for i, element in enumerate(in_semi_joins_codes):
        rel_left = element.split(' ')[0]
        rel_right = element.split(' ')[2]
        variable = element.split(' ')[1]

        koszt = get_size(relations, rel_right, variable) * get_val(relations, rel_right, variable)
        efekt = get_sf(rel_right, variable, sigmas) * relations[rel_left].cardinal
        if i in excluded_indexes:
            efekt = relations[rel_left].cardinal
        zysk = relations[rel_left].cardinal - efekt

        semi_joins_rows.append([koszt, efekt, zysk])

    semi_joins.populate(semi_joins_rows)
    print(semi_joins)


    nullified = int(input())
    excluded_indexes.append(nullified)
    winner__full_code = in_semi_joins_codes[nullified]
    winner_left = winner__full_code.split(' ')[0]
    winner_right = winner__full_code.split(' ')[2]
    winner_variable = winner__full_code.split(' ')[1]

    winner_relation = copy.copy(relations[winner_left])

    print(winner__full_code + ' -> ' + winner__full_code.split(' ')[0] + 'I')
    winner_relation.cardinal = semi_joins[winner__full_code, 'EFEKT']
    temp = get_sf(winner_left, winner_variable, sigmas) * get_val(relations, winner_right, winner_variable)
    winner_relation['VAL', winner_variable] = \
        get_sf(winner_left, winner_variable, sigmas) * get_val(relations, winner_right, winner_variable)

    new_sigma = winner_relation.hash_table.table['VAL'][winner_variable] / in_domains[winner_variable]
    # del(sigmas[winner_left + '.' + winner_variable, 'SF'])
    # sigmas[winner_left + '.' + winner_variable, 'SF'] = new_sigma


    relations[winner_left + 'I'] = winner_relation
    for i, element in enumerate(in_attributes):
        in_attributes[i] = element.replace(winner_left, winner_left + 'I')

    for i, element in enumerate(in_semi_joins_codes):
        in_semi_joins_codes[i] = element.replace(winner_left, winner_left + 'I')

    print()


# R1 = Relation('R1', 1000, {
#             'rows_identifiers': ['SIZE', 'VAL'],
#             'columns_identifiers': ['Property', 'A', 'B']
#         })
# R1.populate_table([[4, 4], [200, 50]])
#
# R2 = Relation('R2', 1000, {
#             'rows_identifiers': ['SIZE', 'VAL'],
#             'columns_identifiers': ['Property', 'A', 'B']
#         })
# R2.populate_table([[4, 4], [40, 100]])
#
# R3 = Relation('R3', 2000, {
#             'rows_identifiers': ['SIZE', 'VAL'],
#             'columns_identifiers': ['Property', 'B', 'D']
#         })
# R3.populate_table([[4, 4], [400, 100]])
#
# R4 = Relation('R4', 1000, {
#             'rows_identifiers': ['SIZE', 'VAL'],
#             'columns_identifiers': ['Property', 'B', 'E']
#         })
# R4.populate_table([[4, 4], [200, 50]])
#
# relations = {
#     'R1': R1,
#     'R2': R2,
#     'R3': R3,
#     'R4': R4
# }
#
# domains = {
#     'A': 400,
#     'B': 500
# }
#
# sigma_attributes = ['R1.A', 'R2.A', 'R2.B', 'R3.B', 'R4.B']
#
#
# semi_joins = \
#                 ['R1 A R2',
#                  'R2 A R1',
#                  'R2 B R3',
#                  'R3 B R2',
#                  'R3 B R4',
#                  'R4 B R3',
#                  'R2 B R4',
#                  'R4 B R2']
#
# good = GoodShit(relations, domains, sigma_attributes, semi_joins)
# good.loop_iterations(5)






