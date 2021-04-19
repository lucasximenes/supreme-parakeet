# Código baseado nos seguintes links:
# https://www.youtube.com/watch?v=uQj5UNhCPuo&ab_channel=KieCodes
# https://www.youtube.com/watch?v=nhT56blfRpE&ab_channel=KieCodes
# https://github.com/kiecodes/genetic-algorithms

from random import choices, randint, randrange, random, seed, sample
from typing import List, Optional, Callable, Tuple
from functools import partial
from collections import namedtuple

seed(10)

Genome = List[int]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]
Pokemon = namedtuple("Pokemon", ["name","power"])
Gyms = List[float]

pokemons = [
    Pokemon("Weedle",1.1),
    Pokemon("Caterpie",1.2),
    Pokemon("Rattata",1.3),
    Pokemon("Bulbassauro",1.4),
    Pokemon("Pikachu",1.5)
]

gyms = [
    55,
    60,
    65,
    70,
    75,
    80,
    85,
    90,
    95,
    100,
    110,
    120
]

def generate_genome(length: int) -> Genome:
    p = sample(range(length), 24)
    r = [0]*length
    for i in p:
        r[i] = 1
    return r
    #return (choices([0, 1], k=length))

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def fitness(genome: Genome, pokemons:[Pokemon], energy_limit: int, gyms: [Gyms]) -> int:
    if len(genome) != len(gyms)*len(pokemons):
        raise ValueError("O tamanho do genoma deve ser do mesmo tamanho de gyms*pokemons)")

    energy = [energy_limit,energy_limit,energy_limit,energy_limit,energy_limit]
    step = -1
    time_spent = 0
    soma = 0
    for i,val in enumerate(genome):
        if i % 5 == 0:
            step += 1
        if val == 1:
            id_energy = i - (step * 5)
            energy[id_energy] -= 1
            soma += 1
            if energy[id_energy] == -1 or soma > 24:
                return 0

        #Ja olhou os 5 pokemons possiveis na batalha de um ginasio
        if (step + 1) * 5 - i == 1:
            s = sum_power(genome[i - 4:i + 1], pokemons)
            if s == 0:
                return 0
            else:
                time_spent += gyms[step]/ sum_power(genome[i - 4:i + 1], pokemons)

    return 1/time_spent

def sum_power(step: List[int], pokemons:[Pokemon]) -> float:
    total_power = 0
    for i,val in enumerate(step):
        if val == 1:
            total_power += pokemons[i].power
            #print(total_power)
    return total_power

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    #teste1
    '''
    for _ in range(num):
        index_1 = randrange(len(genome))
        index_2 = randrange(len(genome))
        if random() < probability:
            genome[index_1] = abs(genome[index_1] - 1)
            genome[index_2] = abs(genome[index_2] - 1)
        #genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome
    '''
    #teste2
    '''
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome
    '''
    #teste3

    for _ in range(num):
        index_1 = randrange(len(genome))
        step = randrange(12)
        index_1_step = (index_1 + 5)%5
        if random() < probability:
            genome[index_1] = abs(genome[index_1] - 1)
            genome[index_1_step*step] = abs(genome[index_1] - 1)
        
    return genome

def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)

def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])

def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))

def print_stats(population: Population, generation_id: int, fitness_func: FitnessFunc):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Population: [%s]" % ", ".join([genome_to_string(gene) for gene in population]))
    print("Avg. Fitness: %f" % (population_fitness(population, fitness_func) / len(population)))
    sorted_population = sort_population(population, fitness_func)
    print(
        "Best: %s (%f)" % (genome_to_string(sorted_population[0]), fitness_func(sorted_population[0])))
    print("Worst: %s (%f)" % (genome_to_string(sorted_population[-1]),
                              fitness_func(sorted_population[-1])))
    print("")

    return sorted_population[0]

def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100,
        printer: Optional[PrinterFunc] = None) \
        -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a,2,0.7)
            offspring_b = mutation_func(offspring_b,2,0.7)
            next_generation += [offspring_a, offspring_b]

        population = next_generation
        print_stats(population = population,generation_id = i,fitness_func=partial(
        fitness, pokemons=pokemons, energy_limit = 5, gyms = gyms))

    population = sorted(
        population,
        key = lambda genome: fitness_func(genome),
        reverse = True
    )
    return population, i

population, generations = run_evolution(
    populate_func = partial(
        generate_population, size=200, genome_length=12*5
    ),
    fitness_func = partial(
        fitness, pokemons=pokemons, energy_limit = 5, gyms = gyms
    ),
    fitness_limit = 1000,
    generation_limit = 2000
)

print(f"number of generations: {generations}")
print(f"best solution: {population[0]}")
energy = [0,0,0,0,0]
pop = []
step = 0
for i,val in enumerate(population[0]):
    pop.append(val)
    if (i+1) % 5 == 0:
        print(population[0][i - 4:i + 1],"gym_d: ",gyms[step],"sum_p: ",sum_power(population[0][i - 4:i + 1], pokemons), "tempo: ",gyms[step]/ sum_power(population[0][i - 4:i + 1], pokemons))
        pop = []
        step += 1
    if val == 1:
        energy[i - (step*5)] += 1
print(energy)
print(f"best time: {1/fitness(population[0],pokemons = pokemons, energy_limit = 5, gyms = gyms)}")

