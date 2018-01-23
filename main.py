from prettytable import PrettyTable

def get_size(relations_list, relation, variable):
    return relations_list[relation]['SIZE', variable]

def get_

class Relation:
    def __init__(self, id, cardinal):
        self.relation_table_schema = {
            'rows_identifiers': ['SIZE', 'VAL'],
            'columns_identifiers': ['Property', 'A', 'B']
        }
        self.id = id
        self.table = {}
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
        self.hash_table.table[key] = value

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



R1 = Relation('R1', 1000)
R1.populate_table([[4, 4], [200, 50]])
#R1.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 200, 50]])
# R1.__repr__()

R2 = Relation('R2', 1000)
R2.populate_table([[4, 4], [40, 100]])
#R2.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 40, 100]])
# R2.__repr__()

R3 = Relation('R3', 2000)
R3.populate_table([[4, 4], [400, 100]])
#R3.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 400, 100]])
# R3.__repr__()

R4 = Relation('R4', 1000)
R4.populate_table([[4, 4], [200, 50]])
#R4.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 200, 50]])
# R4.__repr__()

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
factors = HashTable(in_attributes, ['Atrybut', 'SF'])

factors_to_populate = []
for attribute in in_attributes:
    rel_id = attribute.split('.')[0]
    rel_field = attribute.split('.')[1]
    factors_to_populate.append([relations[rel_id]['VAL', rel_field] / in_domains[rel_field]])

    relations[rel_id][attribute, 'SF'] = relations[rel_id]['VAL', rel_field] / in_domains[rel_field]
factors.populate(factors_to_populate)
print(factors)

in_semi_joins_codes = ['R1 A R2',
                 'R2 A R1',
                 'R2 B R3',
                 'R3 B R2',
                 'R2 B R4',
                 'R4 B R2',
                 'R3 B R4',
                 'R4 B R3']

semi_joins = HashTable(in_semi_joins_codes, ['Join', 'KOSZT', 'EFEKT', 'ZYSK'])
semi_joins_rows = []
for element in in_semi_joins_codes:
    rel_left = element.split(' ')[0]
    rel_right = element.split(' ')[2]
    variable = element.split(' ')[1]

    koszt = get_size(relations, rel_right, variable) * relations[rel_right].cardinal
    efekt



#######################

# table = {}
# rows = ['SIZE', 'VAL']
# columns = ['Property', 'A', 'B']
# data = [
#     [4, 4],
#     [40, 100]
# ]
# hash_table = HashTable(rows, columns)
# hash_table.populate(data)
# hash_table.__repr__()
# print()

#######################







