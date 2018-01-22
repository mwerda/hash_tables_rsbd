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

R1 = Relation(1, 1000)
R1.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 200, 50]])
R1.__repr__()

R2 = Relation(2, 1000)
R2.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 40, 100]])
R2.__repr__()

R3 = Relation(3, 2000)
R3.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 400, 100]])
R3.__repr__()

R4 = Relation(4, 1000)
R4.build_table(['Property', 'A', 'B'], [['SIZE', 4, 4], ['VAL', 200, 50]])
R4.__repr__()

in_domains = {
    'A': 400,
    'B': 500
}

in_attributes = ['R1.A', 'R2.A', 'R2.B', 'R3.B', 'R4.B']

#######################

table = {}
rows = ['SIZE', 'VAL']
columns = ['A', 'B']
data = [
    [4, 4],
    [40, 100]
]
for row in rows:
    table[row] = {}


for values_list, row in zip(data, rows):
    for value, column in zip(values_list, columns):
        table[row][column] = value

print()

#######################



factors_table = PrettyTable(['Atrybut', 'SF'])
PrettyTable()
for element in in_attributes:
    #
    factors_table.get_string()
    #factors_table.add_row(element, in_domains[element.split('.')])


