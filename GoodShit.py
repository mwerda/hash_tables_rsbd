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

    def loop_iterations(self, max_iterations: int):
        excluded_indexes = []
        semi_joins_in_iteration = HashTable(self.semi_joins, ['Join', 'KOSZT', 'EFEKT', 'ZYSK'])
        for i in range(max_iterations):
            sigmas = HashTable(self.sigma_attributes, ['Atrybut', 'SF'])
            factors_population = []
            for attribute in self.sigma_attributes:
                rel_id = attribute.split('.')[0]
                rel_field = attribute.split('.')[1]
                factors_population.append([self.relations[rel_id]['VAL', rel_field] / self.domains[rel_field]])

                # self.relations[rel_id][attribute, 'SF'] = self.relations[rel_id]['VAL', rel_field] / in_domains[rel_field]
            sigmas.populate(factors_population)
            print(sigmas)

            semi_joins_in_iteration = HashTable(self.semi_joins, ['Join', 'KOSZT', 'EFEKT', 'ZYSK'])
            semi_joins_data = []
            for i, element in enumerate(self.semi_joins):
                rel_left = element.split(' ')[0]
                rel_right = element.split(' ')[2]
                variable = element.split(' ')[1]

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

            print(winner_full_code + ' -> ' + winner_full_code.split(' ')[0] + 'I')
            winner_relation.cardinal = semi_joins_in_iteration[winner_full_code, 'EFEKT']
            temp = get_sf(winner_left, winner_variable, sigmas) * get_val(self.relations, winner_right, winner_variable)
            winner_relation['VAL', winner_variable] = \
                get_sf(winner_left, winner_variable, sigmas) * get_val(self.relations, winner_right, winner_variable)

            new_sigma = winner_relation.hash_table.table['VAL'][winner_variable] / self.domains[winner_variable]
            # del(sigmas[winner_left + '.' + winner_variable, 'SF'])
            # sigmas[winner_left + '.' + winner_variable, 'SF'] = new_sigma


            self.relations[winner_left + 'I'] = winner_relation
            for i, element in enumerate(self.sigma_attributes):
                self.sigma_attributes[i] = element.replace(winner_left, winner_left + 'I')

            for i, element in enumerate(self.semi_joins):
                self.semi_joins[i] = element.replace(winner_left, winner_left + 'I')

            print('Moving from iteration' + str(i) + ' to ' + str(i + 1))