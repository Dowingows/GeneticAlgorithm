# algoritmo para solucionar o seguinte problema:
# x + y + z  = 3
# 0 <= x <= 3
import random
import math

#mudar função objetivo para igual e criar função para saber se o cromossomo é valido!!!!!!!!!!

SURVIVAL_RATE = 0.2
CROSSOVER_RATE = (1 - SURVIVAL_RATE)
MUTATION_RATE = 0.07

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

        # verifica se é um cromossomo válido, ou seja, dentro das restrições impostas pelo problema
        if is_valid_chromosome(individual):
            numb = numb + 1
            population.append(individual)

    return population


def chromosome_breaker(chromosome):
    x = chromosome[0:BINARY_SIZE]
    y = chromosome[BINARY_SIZE:BINARY_SIZE*2]
    z = chromosome[BINARY_SIZE*2:BINARY_SIZE*3]
    w = chromosome[BINARY_SIZE*3:BINARY_SIZE*4]

    return int(bin2dec(x)), int(bin2dec(y)), int(bin2dec(z)), int(bin2dec(w))


def is_valid_chromosome(chromosome):
    x, y, z, w = chromosome_breaker(chromosome)

    cond1, cond2 = operation(x, y, z, w)

    if cond1 <= 185 and cond2 <= 15:
        return True
    else:
        return False


def goal(x, y, z, w):
    cond1, cond2 = operation(x, y, z, w)

    if cond1 == 185 and cond2 == 15:
        return True
    else:
        return False


def operation(x, y, z, w):
    return int(x)**3 + int(y)**2 + int(z) + 5 * int(w), int(x) + int(y) + int(z) + int(w)


def fitness(chromossome):

    x, y, z, w = chromosome_breaker(chromossome)

    goal_val = 185
    goal_val_2 = 15

    op = operation(x, y, z, w)

    distance1 = goal_val - op[0]
    distance2 = goal_val_2 - op[1]

    weight2 = round((20-distance2) * 0.7)

    fitness_value = (200 - distance1) + weight2

    return fitness_value


def print_chrom2number(chromossome):

    x, y, z, w = chromosome_breaker(chromossome)

    print("({0}, {1}, {2}, {3}) = {4}".format(x, y, z, w, operation(x, y, z, w)))


def greater_fitness(a):
    return fitness(a)


def get_survivors(population):

    number_individuals = round(POPULATION_NUMBER * SURVIVAL_RATE)

    # ordena os valores da populacao de maneira decrescente pelo valor do fitness para a seleção
    population = sorted(population, key=greater_fitness,reverse= True)

    survivors = []

    for i in range(number_individuals):
        survivors.append(population[i])

    return survivors


def roulette_wheel(population):

    number_individuals = round(POPULATION_NUMBER * CROSSOVER_RATE)

    total_sum = 0

    # ordena os valores da populacao de maneira crescente pelo valor do fitness para a seleção
    population = sorted(population, key=greater_fitness)

    # calcula o somatório do fitness de todos os individuos
    for index in range(len(population)):
        total_sum += fitness(population[index])

    individuals = []
    selected_individuals_indexes = []
    n_individuas_current = 0
    # seleciona o número de individuos que irão fazer o crossover
    while n_individuas_current < number_individuals:
        # sorteia um número aleatório entre 0 e o somatório do fitness

        random_number = random.randint(0, total_sum)

        fitness_acum = 0

        for index in range(len(population)):
            fitness_acum += fitness(population[index])

            # Indivíduo selecionado é o primeiro com aptidão acumulada maior que o número aleatório gerado
            if fitness_acum > random_number and (index not in selected_individuals_indexes):
                individuals.append(population[index])
                selected_individuals_indexes.append(index)
                n_individuas_current += 1
                break

    return sorted(individuals, key=greater_fitness, reverse=True)


def one_point_crossover(parent_1, parent_2):
    length = len(parent_1)
    cut_point = random.randint(0, length - 1)

    son_1 = str(parent_1[0:cut_point]) + str(parent_2[cut_point: length])

    return son_1


def two_point_crossover(parent_1, parent_2):
    length = len(parent_1)
    start_cut_point = random.randint(0, length - 3)
    end_cut_point = start_cut_point + random.randint(1, BINARY_SIZE)

    son_1 = list(parent_1)
    parent_2 = list(parent_2)
    son_1[start_cut_point:end_cut_point] = parent_2[start_cut_point: end_cut_point]

    return "".join(son_1)


def crossover(population):
    sons = []
    length = len(population)
    _cross = 2
    while len(sons) < length:

        i_1 = random.randint(0, len(population) - 1)
        i_2 = random.randint(0, len(population) - 1)

        if i_1 == i_2:
            continue
        if _cross == 1:
            new_son = one_point_crossover(population[i_1], population[i_2])
        else:
            new_son = two_point_crossover(population[i_1], population[i_2])

        if is_valid_chromosome(new_son):
            sons.append(new_son)

    return sons


def change_gene(individual, index):

    new_ind = list(individual)

    if new_ind[index] == '0':
        new_ind[index] = '1'
    else:
        new_ind[index] = '0'

    return "".join(new_ind)


def mutation_gene(individual):

    length = len(individual)
    #numero de genes que serão mutados entre 1 e 3
    num_mutacoes = random.randint(1, 3)

    for i in range(num_mutacoes):
        cut_point = random.randint(0, length - 1)
        individual = change_gene(individual, cut_point)

    return individual


def mutation(population):

    number_random = random.randint(0, 100)

    # mutação acontece?
    #if number_random <= MUTATION_RATE * 100:
    if True:
        print("Mutação aconteceu! ")
        #escolhe aleatoriamente o individuo
        index = random.randint(0, len(population)-1)
        new_ind = mutation_gene(population[index])

        #se a mutação não gerar um descendente válido, realiza mutações até encontrar
        while not is_valid_chromosome(new_ind):
            index = random.randint(0, len(population) - 1)
            new_ind = mutation_gene(population[index])

        population[index] = new_ind

    else:
        print("Mutação não aconteceu. :( ")

    return population


# Verifica se encontrou pelo menos uma solução
def evaluate(population):

    for p_index in range(len(population)):
        x, y, z, w = chromosome_breaker(population[p_index])
        if goal(x, y, z, w):
            return True

    return False


def prinIdvs(population):
    print("Ints: ", end=" ")
    for i in range(len(population)):
        x, y, z, w = chromosome_breaker(population[i])
        print("[{0}, {1}, {2}, {3} = {4} ]".format(x, y, z, w, operation(x, y, z, w)), end=" ")

    print("")


# início do algoritmo genético
new_population = create_population(POPULATION_NUMBER)
print("===> População inicial <===")
prinIdvs(new_population)
#print("Binários:")
print(new_population)

current_generation = 1
result_evaluate = False

while not result_evaluate or current_generation <= GENERATIONS_NUMBER:

    print("* * * GERAÇÃO {0} * * *".format(current_generation))
    # selecao dos individuos para a reproducao
    print("Seleção...")
    selected_individuals = roulette_wheel(new_population)
    prinIdvs(selected_individuals)
    # realiza o cruzamento
    print("Crossover...")
    n_sons = crossover(selected_individuals)
    prinIdvs(n_sons)
    # chance de mutação
    print("Mutação?...")
    n_sons = mutation(n_sons)
    prinIdvs(n_sons)
    # pega os sobreviventes
    survivavors = get_survivors(new_population)
    print("Sobreviventes...")
    prinIdvs(survivavors)

    # nova população
    new_population = (survivavors + n_sons)
    print("* * * Nova população * * * ")
    prinIdvs(new_population)
    #print("* * * * * * * * * * *")

    result_evaluate = evaluate(new_population)
    if result_evaluate:
        break

    current_generation += 1

print("");
print("+ - - - - - - - - - - RESULTADO : - - - - - - - - - - +")

if result_evaluate:
    print("Encontrou solução na geração: {0}".format(str(current_generation-1)))
else:
    print("Não encontrou solução")

new_population = sorted(new_population, key=greater_fitness, reverse=True)
print(new_population)
prinIdvs(new_population)

print("Fim")