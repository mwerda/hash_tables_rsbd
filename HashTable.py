from prettytable import PrettyTable


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
