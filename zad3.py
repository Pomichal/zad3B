import json
import random as rand
from functools import reduce
import matplotlib.pyplot as plt


with open('config.json') as data_file:
    data = json.load(data_file)
    row = data["map"]["rows"]
    col = data["map"]["columns"]
    startx = data["map"]["startx"]
    starty = data["map"]["starty"]
    no_treasures = data["map"]["number_of_treasures"]
    generation_size = data["NoOfChildren"]
    treasures = data["map"]["treasures"]
    instruction_count = data["inst_count"]
    score_per_treasure = data["score_per_treasure"]
    score_per_step = data["score_per_step"]
    mutation1_prob = data["mutation1_prob"]
    mutation2_prob = data["mutation2_prob"]
    mutation3_prob = data["mutation3_prob"]
    survivers_count = data["survive"]


def fitness(original_code):
    code = original_code.copy()
    counter = 0
    pc = 2
    position = [startx, starty]
    place_of_treasures = treasures.copy()
    code[0] = 0
    code[1] = []

    def inc():
        if code[address] < 255:
            code[address] += 1
        else:
            code[address] = 0

    def dec():
        if code[address] == 0:
            code[address] = 255
        else:
            code[address] -= 1

    def check_treasures(place):
        if len(list(filter(lambda pl: pl != place, place_of_treasures))) < len(place_of_treasures):
            place_of_treasures.remove(next(filter(lambda pl: pl == place, place_of_treasures)))
            return score_per_treasure
        else:
            return 0

    def print_result():
        step = str(bin(code[address]))[2:].count('1')
        if step < 3:
            position[1] -= 1
            if position[1] < 0:
                return False
            else:
                code[1].append('H')
        elif step < 5:
            position[1] += 1
            if position[1] >= row:
                return False
            else:
                code[1].append('D')
        elif step < 7:
            position[0] += 1
            if position[0] >= col:
                return False
            else:
                code[1].append('P')
        else:
            position[0] -= 1
            if position[0] < 0:
                return False
            else:
                code[1].append('L')
        code[0] += check_treasures(position)
        if len(place_of_treasures) < len(treasures):
            code[0] += score_per_step * len(place_of_treasures)
        else:
            code[0] -= score_per_step
        if len(place_of_treasures) == 0:
            return False
        return True

    while counter < 501 and pc < instruction_count:
        instruction = code[pc] >> 6
        address = (code[pc] & int("00111111", 2)) + 2
        pc += 1
        if instruction == 0:
            inc()
        elif instruction == 1:
            dec()
        elif instruction == 2:
            pc = address + 2
        elif instruction == 3:
            if not print_result():
                return code[:2] + original_code[2:]
        counter += 1
    return code[:2] + original_code[2:]


def select(generation):
    selected = rand.choices(generation, weights=[(w / generation_size) / 2 for w in range(len(generation), 0, -1)])[0]
    return selected


def mutate(child):
    if rand.random() < mutation1_prob:
        child = [0,[]] + [child[ind + 2] ^ (1 << rand.randint(0,7)) if rand.randint(0,20) == 1 else child[ind + 2] for ind in range(0,instruction_count)]
    elif rand.random() < mutation2_prob:
        child = [0,[]] + list((rand.randint(0, 255) for x in range(0, instruction_count)))
    elif rand.random() < mutation3_prob:
        child[rand.randint(0,63) + 2] = rand.randint(0,255)
    child = fitness(child)
    return child


def crossover(generation):
    parent1 = select(generation)
    parent2 = select(generation)
    while parent1 == parent2:
        parent2 = select(generation)
    # cross_points = [rand.randint(0,1) for _ in range(instruction_count)]
    cross_points = [1 if index < instruction_count / 2 else 0 for index in range(instruction_count)]
    child = [parent1[ind + 2] if cross_points[ind] == 0 else parent2[ind + 2] for ind in range(instruction_count)]
    child = [0,[]] + child
    child = fitness(child)
    child = mutate(child)
    return child


def evolution(codes,steps):
    # codes = [list((rand.randint(0, 255) for x in range(0, instruction_count))) for y in range(generation_size)]
    codes = list(map(lambda x: [0,[]] + x,codes))
    codes = list(map(lambda c: fitness(c), codes))
    codes.sort(key=lambda x: x[0],reverse=True)

    x_axis = []
    y_axis = []

    for No in range(steps):
        winners = list(filter(lambda solution: solution[0] > (no_treasures - 1) * score_per_treasure,codes))
        if len(winners) > 0:
            print("solution found, in generation %d:" % No)
            # plt.show()
            return [win[1] for win in winners]
        avg = reduce(lambda a,b:a+b,[x[0] for x in codes]) / generation_size
        # x_axis.append(No)
        # y_axis.append(avg)
        # plt.plot(x_axis, y_axis,color='g')
        # plt.pause(0.0001)
        # plt.show(block=False)
        new_g = codes[:survivers_count].copy()
        for a in range(survivers_count,generation_size):
            child = crossover(codes)
            new_g.append(child)
        codes = new_g.copy()
        codes.sort(key=lambda key: key[0], reverse=True)

    print("solution does not found, the best:")
    print(codes[0])
    print([x[0] for x in codes])
    # plt.show()
    return False