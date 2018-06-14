# algoritmo para solucionar o seguinte problema:
# x + y + z  = 3
# 0 <= x <= 3
import random
import math


SURVIVAL_RATE = 0.2
CROSSOVER_RATE = (1 - SURVIVAL_RATE)
MUTATION_RATE = 0.01

GENERATIONS_NUMBER = 3
POPULATION_NUMBER = 8

BINARY_SIZE = 2
GENOTYPES_NUMBER = 3


def dec2bin(decimal):

    x = bin(decimal)
    x = x.split("b")[1]

    for index in range(BINARY_SIZE - x.__len__()):
        x = '0' + x

    return x


def bin2dec(number):
    decimal = 0
    number = str(number)
    number = number[::-1]

    for i in range(len(number)):
        if number[i] == "1":
            decimal = decimal + 2**i

    return decimal


def create_individual():

    individual = "";

    for i in range(GENOTYPES_NUMBER):
        individual += (dec2bin(random.randint(0, 3)) + "")

    return individual


def create_population(individuals_number):

    population = []

    for i in range(individuals_number):
        population.append(create_individual())

    return population


def chromosome_breaker(chromosome):
    x = chromosome[0:BINARY_SIZE]
    y = chromosome[BINARY_SIZE:BINARY_SIZE*2]
    z = chromosome[BINARY_SIZE*2:BINARY_SIZE*4]

    return x, y, z


def goal(x, y, z):

    if (x + y + z) == 6:
        return True
    else:
        return False


def operation(x, y, z):
    return int(x) + int(y) + int(z)


def fitness(chromossome):
    x, y, z = chromosome_breaker(chromossome)
    x = bin2dec(x)
    y = bin2dec(y)
    z = bin2dec(z)
    #print("Cromossomo: "+str(chromossome))

    goal_value = 6

    op = operation(x, y, z)
    #print("X ({0}) + Y({1}) + Z({2})  = {3}".format(x,y,z,op))

    if op > goal_value:
        return 1

    distance = goal_value - op
    fitness_value = 10 - distance



    return fitness_value


def print_chrom2number(chromossome):

    x, y, z = chromosome_breaker(chromossome)
    x = bin2dec(x)
    y = bin2dec(y)
    z = bin2dec(z)

    print("({0}, {1}, {2}) = {3}".format(x, y, z,operation(x,y,z)))


def greater_fitness(a):
    return fitness(a)


def get_survivors(population):

    number_individuals = round(POPULATION_NUMBER * SURVIVAL_RATE)

    # ordena os valores da populacao de maneira decrescente pelo valor do fitness para a seleção
    population = sorted(population, key=greater_fitness)

    survivors = []

    for i in range(number_individuals):
        survivors.append(population[len(population)-i-1])

    return survivors


def roulette_wheel(population):

    number_individuals = round(POPULATION_NUMBER * CROSSOVER_RATE)

    total_sum = 0

    # ordena os valores da populacao de maneira decrescente pelo valor do fitness para a seleção
    population = sorted(population, key=greater_fitness)

    # calcula o somatório do fitness de todos os individuos
    for index in range(len(population)):
        total_sum += fitness(population[index])

    individuals = []
    selected_individuals_indexes = []

    # seleciona o número de individuos que irão fazer o crossover
    for j in range(number_individuals):
        # sorteia um número aleatório entre 0 e o somatório do fitness

        random_number = random.randint(0, total_sum)

        fitness_acum = 0

        for index in range(len(population)):
            fitness_acum += fitness(population[index])

            # Indivíduo selecionado é o primeiro com aptidão acumulada maior que o número aleatório gerado
            if fitness_acum > random_number and (index not in selected_individuals_indexes):
                individuals.append(population[index])
                selected_individuals_indexes.append(index)

                break

    return individuals


def one_point_crossover(parent_1, parent_2):
    length = len(parent_1)
    cut_point = random.randint(0, length)

    son_1 = str(parent_1[0:cut_point]) + str(parent_2[cut_point: length])

    return son_1


def crossover(population):
    sons = []

    random.shuffle(population)

    for index in range(len(population)):

        i_1 = random.randint(0, len(population) - 1)
        i_2 = random.randint(0, len(population) - 1)

        sons.append(one_point_crossover(population[i_1], population[i_2]))

    return sons


def mutation(population):
    return population


def prinIdvs(population):
    print("Population: ")
    for i in range(len(population)):
        x, y, z = chromosome_breaker(population[i])
        print("({0} + {1} + {2} = {3} )".format(bin2dec(x),bin2dec(y),bin2dec(z),operation(bin2dec(x),bin2dec(y),bin2dec(z))),end =" ")

    print("")



# início do algoritmo genético
new_population = create_population(POPULATION_NUMBER)
print("População inicial...")
print(new_population)
prinIdvs(new_population)

for i in range(GENERATIONS_NUMBER):

    print("* * * GERAÇÃO {0} * * *".format(i+1))
    # selecao dos individuos para a reproducao
    selected_individuals = roulette_wheel(new_population)
    print("Individuos selecionados...")
    print(selected_individuals)
    prinIdvs(selected_individuals)
    # realiza o cruzamento
    n_sons = crossover(selected_individuals)
    print("Filhos do cruzamento...")
    print(n_sons)
    prinIdvs(n_sons)
    # chance de mutação
    n_sons = mutation(n_sons)
    print("Mutação?...")
    print(n_sons)
    #pega os sobreviventes
    survivavors = get_survivors(new_population)
    print("Sobreviventes...")
    print(survivavors)
    prinIdvs(survivavors)

    #nova população
    new_population = (survivavors + n_sons)



print("Nova população: ")
print(new_population)
prinIdvs(new_population)

print("Fim")


