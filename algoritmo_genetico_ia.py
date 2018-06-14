# algoritmo para solucionar o seguinte problema:
# x + y + z  = 3
# 0 <= x <= 3
import random
import math


SURVIVAL_RATE = 0.2
CROSSOVER_RATE = (1 - SURVIVAL_RATE)
MUTATION_RATE = 0.1

GENERATIONS_NUMBER = 30
POPULATION_NUMBER = 6


BINARY_SIZE = 3
GENOTYPES_NUMBER = 4


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

    individual = ""

    for index in range(GENOTYPES_NUMBER):
        if index == 0:
            n_number = random.randint(0, 6)
        else:
            n_number = random.randint(0, 7)
        individual += str(dec2bin(n_number))

    return individual


def create_population(individuals_number):

    population = []
    numb = 0

    while numb < individuals_number:
        individual = create_individual()
        x, y, z, w = chromosome_breaker(individual)
        x = bin2dec(x)
        y = bin2dec(y)
        z = bin2dec(z)
        w = bin2dec(w)

        #print(individual)
        #print(chromosome_breaker(individual))
        #print(operation(x, y, z, w))

        if goal(x, y, z, w):
            numb = numb + 1
            population.append(individual)

    return population


def chromosome_breaker(chromosome):
    x = chromosome[0:BINARY_SIZE]
    y = chromosome[BINARY_SIZE:BINARY_SIZE*2]
    z = chromosome[BINARY_SIZE*2:BINARY_SIZE*3]
    w = chromosome[BINARY_SIZE*3:BINARY_SIZE*4]

    return x, y, z, w


def goal(x, y, z, w):
    cond1, cond2 = operation(x,y,z,w)

    if cond1 <= 185 and cond2 <= 15:
        return True
    else:
        return False


def operation(x, y, z, w):
    return int(x)**3 + int(y)**2 + int(z) + 5 * int(w), int(x) + int(y) + int(z) + int(w)


def fitness(chromossome):

    x, y, z, w = chromosome_breaker(chromossome)

    x = bin2dec(x)
    y = bin2dec(y)
    z = bin2dec(z)
    w = bin2dec(w)

    goal_val = 185
    goal_val_2 = 15

    op = operation(x, y, z, w)

    distance1 = goal_val - op[0]
    distance2 = goal_val_2 - op[1]

    fitness_value = (200 - distance1) + (20-distance2)

    return fitness_value


def print_chrom2number(chromossome):

    x, y, z, w = chromosome_breaker(chromossome)

    x = bin2dec(x)
    y = bin2dec(y)
    z = bin2dec(z)
    w = bin2dec(w)

    print("({0}, {1}, {2}, {3}) = {4}".format(x, y, z, w, operation(x, y, z, w)))


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

    return sorted(individuals, key=greater_fitness,reverse=True)


def one_point_crossover(parent_1, parent_2):
    length = len(parent_1)
    cut_point = random.randint(0, length - 1)

    son_1 = str(parent_1[0:cut_point]) + str(parent_2[cut_point: length])

    return son_1


def crossover(population):
    sons = []

    for index in range(len(population)):

        i_1 = random.randint(0, len(population) - 1)
        i_2 = random.randint(0, len(population) - 1)

        sons.append(one_point_crossover(population[i_1], population[i_2]))

    return sons


def mutation_gene(individual):

    length = len(individual)
    cut_point = random.randint(0, length - 1)

    newInd = list(individual)

    if newInd[cut_point] == '0':
        newInd[cut_point] = '1'
    else:
        newInd[cut_point] = '0'

    return individual


def mutation(population):

    number_random = random.randint(0,100)

    # mutação acontece
    if number_random <= MUTATION_RATE * 100:
        #escolhe aleatoriamente o individuo
        index = random.randint(0, len(population)-1)
        population[index] = mutation_gene(population[index])

    return population


def prinIdvs(population):
    print("Inteiros: ")
    for i in range(len(population)):
        x, y, z, w = chromosome_breaker(population[i])
        print("[{0}, {1}, {2}, {3} = {4} ]".format(bin2dec(x),bin2dec(y),bin2dec(z),bin2dec(w),operation(bin2dec(x),bin2dec(y),bin2dec(z),bin2dec(w))),end =" ")

    print("")


# início do algoritmo genético
new_population = create_population(POPULATION_NUMBER)
print("===> População inicial <===")
#prinIdvs(new_population)
#print("Binários:")
#print(new_population)


for c_i in range(GENERATIONS_NUMBER):
    #print("* * * GERAÇÃO {0} * * *".format(c_i + 1))
    # selecao dos individuos para a reproducao
    selected_individuals = roulette_wheel(new_population)
    #prinIdvs(selected_individuals)
    # realiza o cruzamento
    #print("Crossover...")
    n_sons = crossover(selected_individuals)
    #prinIdvs(n_sons)
    # chance de mutação
    n_sons = mutation(n_sons)
    #print("Mutação?...")
    #prinIdvs(n_sons)
    # pega os sobreviventes
    survivavors = get_survivors(new_population)
    #print("Sobreviventes...")
    #prinIdvs(survivavors)

    # nova população
    new_population = (survivavors + n_sons)
    #print("* * * * * * * * * * *")

print("Nova população: ")
print(new_population)
prinIdvs(new_population)

print("Fim")