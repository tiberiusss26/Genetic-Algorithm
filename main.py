import copy
import math
import random
import numpy as np
import numpy.random


def binary_search(left, right, x, list):
    mid = (left + right) // 2
    if left >= (right - 1):
        if list[right] == x:
            return right
        else:
            return left
    else:
        if list[mid] == x:
            return mid
        elif list[mid] < x:
            return binary_search(mid + 1, right, x, list)
        else:
            return binary_search(left, mid - 1, x, list)


f = open("input.in", "r")

n = int(f.readline())
x = int(f.readline())
y = int(f.readline())
a, b, c = [float(nr) for nr in f.readline().split()]
precision = float(f.readline())
rec_probability = float(f.readline())
mut_probability = float(f.readline())
iterations = int(f.readline())


def function(x):
    return a * (x ** 2) + b * x + c


l = math.ceil(math.log2((y - x) * (10 ** precision)))

population = [np.random.randint(0, 2, l).tolist() for _ in range(n)]

d = (y - x) / (2 ** l - 1)

intervals = [(x + d * i, x + d * (i + 1)) for i in range((2 ** l)-1)]

finals = []
elitists = []
selected_population = []


for iterr in range(iterations):
    if iterr >= 1:
        population = copy.deepcopy(selected_population)
    F = 0
    p = []
    X = []
    f = []
    elitist = 0
    index = 1

    for chromosome in population:
        x = 0
        for i in range(l):
            x += (2 ** (l - i - 1)) * chromosome[i]
        if iterr == 0: print(bin(x), intervals[x][0], function(intervals[x][0]))
        elitist = max(elitist, function(intervals[x][0]))
        X.append(intervals[x][0])
        f.append(function(intervals[x][0]))
        F += function(intervals[x][0])

    if iterr == 0: print()

    for x in X:
        p.append(x / F)

    for i in range(len(p)):
        if iterr == 0: print(f"Cromozomul {i + 1} are probabilitatea {p[i]}")

    probability_interval = [0]

    for i in range(len(p)):
        s = 0
        for j in range(i + 1):
            s += f[j]
        probability_interval.append(s / F)

    if iterr == 0: print("Intervale probabilitati selectie:")
    if iterr == 0: print(probability_interval)

    selected_population = copy.deepcopy([])

    for i in range(n):
        u = numpy.random.uniform(0, 1)
        num = binary_search(0, len(probability_interval) - 1, u, probability_interval)
        if iterr == 0: print(
            f"Pentru u = {u} selectam cromozomul: {num}")
        selected_population.append(population[num - 1])

    if iterr == 0: print("Dupa selectie: ")
    index = 1
    for chromosome in selected_population:
        x = 0
        for i in range(l):
            x += (2 ** (l - i - 1)) * chromosome[i]
        if iterr == 0: print(index, ": ", bin(x), intervals[x][0], function(intervals[x][0]))
        index += 1

    if iterr == 0: print("Probabilitate de incrucisare: {}".format(rec_probability / 100))

    rec_probabilities = numpy.random.uniform(0, 1, n)

    if iterr == 0: print(rec_probabilities)

    rec_chromosomes = []

    for i in range(len(rec_probabilities)):
        if rec_probabilities[i] < rec_probability / 100:
            if iterr == 0: print(f"Cromozomul {i} participa")
            rec_chromosomes.append(i)
        else:
            if iterr == 0: print(f"Cromozomul {i} nu participa")

    for ind in range(0, len(rec_chromosomes), 2):
        if ind + 1 == len(rec_chromosomes):
            break
        else:
            point = random.randint(0, 22)
            if iterr == 0: print(ind, ind + 1, "--", selected_population[rec_chromosomes[ind]],
                                 selected_population[rec_chromosomes[ind + 1]], "punctul: ",
                                 point)
            selected_population[rec_chromosomes[ind]][point:], selected_population[rec_chromosomes[ind + 1]][point:] = \
                selected_population[
                    rec_chromosomes[
                        ind + 1]][
                point:], selected_population[
                             rec_chromosomes[
                                 ind]][
                         point:]
            if iterr == 0: print(population[rec_chromosomes[ind]], population[rec_chromosomes[ind + 1]])
    index = 1
    if iterr == 0: print("Dupa recombinare: ")
    for chromosome in selected_population:
        x = 0
        for i in range(l):
            x += (2 ** (l - i - 1)) * chromosome[i]
        if iterr == 0: print(index, ": ", bin(x), intervals[x][0], function(intervals[x][0]))
        index += 1

    if iterr == 0: print("Probabilitate de mutatie: {}".format(mut_probability / 100))

    mut_probabilities = numpy.random.uniform(0, 1, n)

    if iterr == 0: print(mut_probabilities)

    mut_chromosomes = []

    for i in range(len(mut_probabilities)):
        if mut_probabilities[i] < mut_probability / 100:
            if iterr == 0: print(f"Cromozomul {i} PARTICIPA")
            mut_chromosomes.append(i)
        else:
            if iterr == 0: print(f"Cromozomul {i} nu participa")

    for ind in mut_chromosomes:
        poz = numpy.random.randint(0, 22)
        selected_population[ind][poz] = (selected_population[ind][poz] + 1) % 2

    if iterr == 0: print("Dupa mutatie: ")
    index = 1
    if iterr > 0:
        final = finals[len(finals) - 1]
    else:
        final = elitist
    for chromosome in selected_population:
        x = 0
        for i in range(l):
            x += (2 ** (l - i - 1)) * chromosome[i]
        if iterr == 0: print(index, ": ", bin(x), intervals[x][0], function(intervals[x][0]))
        final = max(final, function(intervals[x][0]), elitist)
        index += 1

    finals.append(final)
    elitists.append(elitist)

for fin in finals:
    print(fin)
# print("---------------------------------------")
# for elit in elitists:
#     print(elit)
