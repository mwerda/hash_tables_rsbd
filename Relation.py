from HashTable import HashTable


class Relation:
    def __init__(self, id, cardinal, relation_table_schema):
        self.relation_table_schema = relation_table_schema
        self.id = id
        self.cardinal = cardinal
        self.hash_table = HashTable(self.relation_table_schema['rows_identifiers'],
                                    self.relation_table_schema['columns_identifiers'])

    def populate_table(self, data):
        self.hash_table.populate(data)

    def __getitem__(self, item):
        row, col = item
        return self.hash_table.table[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.hash_table.table[row][col] = value

    def __str__(self):
        return str(self.id + '\n' + self.hash_table.__str__() + '\n' + 'Cardinality: ' + str(self.cardinal))
