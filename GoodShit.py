import copy
from HashTable import HashTable


def get_size(relations_list, relation, variable):
    return relations_list[relation]['SIZE', variable]


def get_sf(relation, variable, sf_table):
    return sf_table[relation + '.' + variable, 'SF']


def get_val(relations_list, relation, variable):
    return relations_list[relation]['VAL', variable]


class GoodShit:
    def __init__(self, relations, domains, sigma_attributes, semi_joins):
        self.relations = relations
        self.domains = domains
        self.sigma_attributes = sigma_attributes
        self.semi_joins = semi_joins

    def loop_iterations(self, max_iteration_number: int):
        excluded_indexes = []
        for iteration in range(1, max_iteration_number + 1):
            sigmas = HashTable(self.sigma_attributes, ['Atrybut', 'SF'])
            factors_population = []
            for attribute in self.sigma_attributes:
                rel_id = attribute.split('.')[0]
                rel_field = attribute.split('.')[1]
                factors_population.append([self.relations[rel_id]['VAL', rel_field] / self.domains[rel_field]])

            sigmas.populate(factors_population)
            for element in sorted(set(x.split('.')[0] for x in self.sigma_attributes)):
                print(self.relations[element])
            print(sigmas)

            semi_joins_in_iteration = HashTable(self.semi_joins, ['Join', 'KOSZT', 'EFEKT', 'ZYSK'])
            semi_joins_data = []
            for i, element in enumerate(self.semi_joins):
                rel_left = element.split(' ')[0]
                rel_right = element.split(' ')[2]
                variable = element.split(' ')[1]

                # Breaking english naming conventions for for easy switching between test naming notion and code
                koszt = get_size(self.relations, rel_right, variable) * get_val(self.relations, rel_right, variable)
                efekt = get_sf(rel_right, variable, sigmas) * self.relations[rel_left].cardinal
                if i in excluded_indexes:
                    efekt = self.relations[rel_left].cardinal
                zysk = self.relations[rel_left].cardinal - efekt

                semi_joins_data.append([koszt, efekt, zysk])

            semi_joins_in_iteration.populate(semi_joins_data)
            print(semi_joins_in_iteration)

            print('Wpisz indeks wiersza o najwiekszej wartosci zysku. Indeksacja od zera.')
            excluded_index = int(input())
            excluded_indexes.append(excluded_index)
            winner_full_code = self.semi_joins[excluded_index]
            winner_left = winner_full_code.split(' ')[0]
            winner_right = winner_full_code.split(' ')[2]
            winner_variable = winner_full_code.split(' ')[1]

            winner_relation = copy.copy(self.relations[winner_left])
            winner_relation.id = winner_relation.id + '|'

            # Updating values
            # if iteration != 3:
            print(winner_full_code + ' -> ' + winner_full_code.split(' ')[0] + 'I')
            winner_relation.cardinal = semi_joins_in_iteration[winner_full_code, 'EFEKT']
            # temp = get_sf(winner_left, winner_variable, sigmas) * get_val(self.relations, winner_right, winner_variable)
            # val update
            winner_relation['VAL', winner_variable] = \
                get_sf(winner_left, winner_variable, sigmas) * get_val(self.relations, winner_right,
                                                                        winner_variable)

            new_sigma = winner_relation.hash_table.table['VAL'][winner_variable] / self.domains[winner_variable]

            other = list(filter(lambda x: winner_variable not in x, winner_relation.hash_table.column_identifiers[1:]))
            print("Other variables ")
            print(other)
            # else:
            for i in other:
                # yao
                temp_cardinal = winner_relation.cardinal
                n = temp_cardinal
                winner_relation.cardinal = semi_joins_in_iteration[winner_full_code, 'EFEKT']
                m = winner_relation['VAL', i]
                r = winner_relation.cardinal

                approx = 0
                if r < m / 2:
                    approx = r
                elif m / 2 <= r < 2 * m:
                    approx = (r + m) / 3
                elif r >= 2 * m:
                    approx = m

                winner_relation['VAL', i] = approx

            self.relations[winner_left + 'I'] = winner_relation
            for i, element in enumerate(self.sigma_attributes):
                self.sigma_attributes[i] = element.replace(winner_left, winner_left + 'I')

            for i, element in enumerate(self.semi_joins):
                self.semi_joins[i] = element.replace(winner_left, winner_left + 'I')

            print('******************************************************************')
            print('Moving from iteration ' + str(iteration) + ' to ' + str(iteration + 1))
