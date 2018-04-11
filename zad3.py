import json
import random as rand
from functools import reduce
import matplotlib.pyplot as plt

#load parameters
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
    mutation_stagnation = data["Stagnation_len"]
    stagnation_range = data["Stagnation_range"]

#get fitness for code
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
            if len(place_of_treasures) == no_treasures - 1:
                code[0] -= len(code[1])
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
            code[0] += score_per_step
        else:
            code[0] -= score_per_step
        if len(place_of_treasures) == 0:
            return False
        return True

    #goes throught the code
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

#select a parent with rulete
def select(generation):
    selected = rand.choices(generation, weights=[(w / generation_size) / 2 for w in range(len(generation), 0, -1)])[0]
    # selected = rand.choices(generation, weights=[(generation[w - 1][0] + 1) / len(generation) for w in range(len(generation), 0, -1)])[0]
    return selected


def mutate(child):
    if rand.random() < mutation3_prob:
        child[rand.randint(0, 63) + 2] = rand.randint(0, 255)
    elif rand.random() < mutation1_prob:
        child = [0,[]] + [child[ind + 2] ^ (1 << rand.randint(0,7)) if rand.randint(0,20) == 1 else child[ind + 2] for ind in range(0,instruction_count)]
    elif rand.random() < mutation2_prob:
        child = [0, []] + list((rand.randint(0, 255) for x in range(0, instruction_count)))
    return child

#create a child
def crossover(generation):
    parent1 = select(generation)
    parent2 = select(generation)
    while parent1 == parent2:
        parent2 = select(generation)
    cross_points = [rand.randint(0,1) for _ in range(instruction_count)]
    # cross_points = [1 if index < instruction_count / 2 else 0 for index in range(instruction_count)]
    child = [parent1[ind + 2] if cross_points[ind] == 0 else parent2[ind + 2] for ind in range(instruction_count)]
    # child = [parent1[ind + 2] if ind % 2 == 0 else parent2[ind + 2] for ind in range(instruction_count)]
    child = [0,[]] + child
    child = mutate(child)
    child = fitness(child)
    return child


def evolution(gens,steps, draw = 0, mut = 0, cont = 0):
    codes = list(map(lambda x: [0,[]] + x,gens))
    codes = list(map(lambda c: fitness(c), codes))
    codes.sort(key=lambda x: x[0],reverse=True)

    if draw != 0:
        x_axis = []
        y_axis = []

    maxi = []
    maxi_counter = 0
    top = 0
    avgs= []
    cyklus = 0

    No = 0
    while No < steps:
        winners = list(filter(lambda solution: solution[0] > (no_treasures - 1) * score_per_treasure,codes))
        avg = reduce(lambda a, b: a + b, [x[0] for x in codes]) / generation_size

        if codes[0][0] != top:
            maxi_counter = 0
            top = codes[0][0]
        else:
            maxi_counter += 1

        maxi.append(top)
        avgs.append(avg)

        #draw graph
        if draw != 0:
            x_axis.append(No + cyklus * steps)
            y_axis.append(avg)
            plt.plot(x_axis, y_axis, color='g')
            plt.plot(x_axis, maxi, color='r')
            plt.pause(0.0001)
            plt.show(block=False)

        #controll solution
        if len(winners) > 0:
            # print("solution found, in generation %d:" % No)
            if draw != 0:
                plt.show()
            return [win[1] for win in winners]

        #in case of stagnation
        if mut != 0:
            if len(avgs) >= mutation_stagnation:
                avgs.pop(0)
                difference = list(map(lambda old_avg: abs(old_avg - avg),avgs))
                if reduce(lambda first, second: first and second,[True if dif < stagnation_range else False for dif in difference]) and maxi_counter >= mutation_stagnation:
                    codes = [fitness([0, []] + list(rand.randint(0, 255) for x in range(instruction_count))) if code[0] == codes[0][0] else code for code in codes]

        #create the new generation
        new_g = codes[:survivers_count].copy()
        for a in range(survivers_count,generation_size):
            child = crossover(codes)
            new_g.append(child)
        codes = new_g.copy()
        codes.sort(key=lambda key: key[0], reverse=True)

        #continue searching
        if No == steps - 1:
            print("solution does not found, the best:")
            print(codes[0])
            print([x[0] for x in codes])
            if cont != 0:
                text = input("continue searching?(y/n)")
                if text == 'y':
                    cyklus += 1
                    No = 0
        No += 1

    if draw != 0:
        plt.show()
    return False

#compare two modes of evolution
def compare():
    count1 = 0
    count2 = 0
    firstandnotsecond = 0
    secondandnotfirst = 0
    draw_it = []
    draw_it_m = []
    axis_x = []
    for x in range(100):
        codes = [list((rand.randint(0, 255) for c in range(instruction_count))) for y in range(generation_size)]
        tmp = evolution(codes.copy(),500)
        tmp2 = evolution(codes.copy(),500,mut=1)
        if tmp:
            count1 += 1
            if not tmp2:
                firstandnotsecond += 1
        if tmp2:
            count2 += 1
            if not tmp:
                secondandnotfirst += 1
        axis_x.append(x)
        draw_it.append(count1 / (x + 1) * 100)
        draw_it_m.append(count2 / (x + 1) * 100)
        plt.plot(axis_x, draw_it, color='g')
        plt.plot(axis_x, draw_it_m, color='r')
        plt.pause(0.0001)
        plt.show(block=False)
    print(count1)
    print(firstandnotsecond)
    print(count2)
    print(secondandnotfirst)
    plt.show()

# codes = [list((rand.randint(0, 255) for c in range(instruction_count))) for y in range(generation_size)]
#
# print(evolution(codes,500,draw=1,mut=1))