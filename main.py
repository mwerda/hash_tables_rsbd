from prettytable import PrettyTable

class Relation:
    def __init__(self, number, card):
        self.id = number
        self.table = {}
        self.card = card

    def build_table(self, columns, rows):
        self.table = PrettyTable(columns)
        for row in rows:
            self.table.add_row(row)

    def __repr__(self):
        print('R' + str(self.id))
        print(self.table)
        print()

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


    def __repr__(self):
        pretty_table = PrettyTable(self.column_identifiers)
        for row_name in self.row_identifiers:
            row = [row_name]
            for column_name in self.column_identifiers:
                row.append(self.table[row_name][column_name])
            pretty_table.add_row(row)
        print(pretty_table)



# R1 = Relation(1, 1000)
# R1.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 200, 50]])
# R1.__repr__()
#
# R2 = Relation(2, 1000)
# R2.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 40, 100]])
# R2.__repr__()
#
# R3 = Relation(3, 2000)
# R3.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 400, 100]])
# R3.__repr__()
#
# R4 = Relation(4, 1000)
# R4.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 200, 50]])
# R4.__repr__()
#
# in_domains = {
#     'A': 400,
#     'B': 500
# }
#
# in_attributes = ['R1.A', 'R2.A', 'R2.B', 'R3.B', 'R4.B']

#######################

table = {}
rows = ['SIZE', 'VAL']
columns = ['Property', 'A', 'B']
data = [
    [4, 4],
    [40, 100]
]
hash_table = HashTable(rows, columns)
hash_table.populate(data)
hash_table.__repr__()
print()

#######################



# factors_table = PrettyTable(['Atrybut', 'SF'])
# PrettyTable()
# for element in in_attributes:
#     #
#     factors_table.get_string()
#     #factors_table.add_row(element, in_domains[element.split('.')])


