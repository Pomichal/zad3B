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
    cross_prob = data["cross_prob"]
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
#                #steps[0] -= score_per_treasure * len(place_of_treasures)
                return code[:2] + original_code[2:]
        counter += 1
#    #steps[0] -= score_per_treasure * len(place_of_treasures)
    return code[:2] + original_code[2:]


# a = VirtualMachine('config.json')
# code2 = [randint(0,255) for x in range(0,64)]
# print(code2)
# code = [198, 70, 10, 247, 57, 235, 12, 36, 235, 63, 88, 240, 247, 93, 201, 191, 135, 126, 238, 2, 42, 23, 20, 144, 64, 184, 230, 181, 238, 168, 201, 216, 130, 55, 26, 203, 174, 61, 168, 56, 146, 83, 244, 251, 16, 109, 153, 15, 61, 9, 250, 16, 22, 26, 17, 12, 233, 193, 31, 30, 244, 162, 248, 170]
# code = [142, 138, 169, 93, 191, 104, 188, 98, 39, 159, 166, 52, 246, 189, 80, 72, 132, 16, 123, 151, 73, 170, 4, 125, 193, 127, 196, 131, 111, 138, 241, 191, 30, 107, 93, 143, 177, 85, 96, 49, 33, 221, 73, 97, 213, 80, 40, 178, 89, 239, 101, 83, 183, 69, 169, 44, 25, 127, 56, 202, 80, 249, 38, 108]
# code = [212, 75, 78, 55, 237, 44, 113, 205, 180, 77, 65, 240, 89, 18, 198, 67, 126, 228, 101, 195, 2, 95, 3, 57, 167, 122, 115, 228, 249, 19, 198, 109, 39, 105, 222, 21, 46, 124, 196, 240, 15, 8, 195, 202, 7, 221, 118, 150, 133, 13, 83, 196, 225, 29, 221, 167, 174, 58, 110, 30, 13, 5, 80, 236]
# code2 = [225, 143, 0, 245, 61, 255, 168, 68, 56, 55, 168, 21, 123, 37, 193, 255, 239, 108, 155, 168, 221, 167, 208, 137, 152, 205, 80, 89, 236, 184, 144, 132, 170, 201, 110, 4, 255, 156, 48, 68, 93, 232, 254, 227, 34, 75, 52, 74, 102, 174, 42, 247, 116, 204, 206, 146, 141, 34, 246, 0, 76, 55, 209, 194]
# code2 = [172, 177, 92, 167, 6, 155, 2, 13, 132, 66, 46, 172, 8, 161, 103, 189, 20, 163, 180, 17, 205, 112, 236, 212, 167, 254, 185, 35, 176, 70, 194, 107, 198, 61, 60, 223, 86, 180, 214, 70, 136, 214, 122, 247, 115, 166, 227, 33, 238, 202, 102, 225, 162, 180, 12, 113, 55, 85, 248, 200, 62, 142, 96, 224]
# code2 = [39, 146, 106, 144, 12, 236, 84, 22, 54, 108, 158, 207, 99, 225, 69, 198, 87, 1, 240, 117, 121, 226, 97, 128, 83, 220, 255, 184, 29, 245, 172, 82, 185, 181, 40, 193, 36, 191, 76, 137, 188, 206, 37, 188, 199, 1, 243, 131, 167, 70, 26, 127, 216, 252, 149, 51, 107, 188, 52, 96, 95, 49, 45, 141]
# code2 = [201, 160, 236, 160, 201, 210, 94, 198, 63, 164, 224, 94, 91, 182, 160, 54, 27, 78, 44, 214, 50, 11, 205, 153, 76, 52, 118, 191, 242, 16, 252, 12, 212, 135, 248, 212, 43, 124, 107, 238, 98, 92, 47, 174, 254, 177, 141, 175, 20, 172, 108, 126, 48, 230, 10, 144, 149, 103, 107, 242, 187, 165, 87, 137]
# code2 = [179, 236, 7, 58, 81, 151, 77, 70, 130, 44, 122, 90, 95, 168, 78, 162, 255, 187, 248, 70, 225, 17, 2, 205, 236, 221, 236, 48, 1, 18, 33, 240, 238, 168, 82, 20, 44, 44, 108, 54, 157, 86, 13, 158, 233, 186, 96, 6, 185, 60, 7, 223, 54, 14, 111, 80, 186, 61, 123, 101, 84, 103, 163, 246]
# code2 = [0,[],94, 63, 104, 143, 202, 111, 115, 112, 246, 161, 50, 64, 20, 176, 231, 135, 103, 52, 8, 247, 249, 36, 100, 144, 221, 241, 243, 179, 231, 195, 231, 146, 72, 93, 66, 137, 15, 35, 149, 198, 52, 124, 91, 238, 116, 87, 192, 11, 39, 213, 10, 9, 30, 87, 195, 32, 108, 251, 44, 166, 25, 170, 24, 169]
# code2 = [0,[],193, 48, 10, 221, 239, 80, 48, 74, 239, 244, 32, 153, 124, 121, 89, 9, 107, 107, 154, 125, 84, 89, 156, 166, 120, 79, 241, 174, 44, 28, 111, 35, 121, 20, 161, 165, 95, 171, 173, 194, 136, 78, 149, 104, 180, 227, 157, 2, 31, 123, 40, 93, 219, 136, 99, 48, 113, 92, 39, 198, 140, 72, 209, 20]
# code2 = fitness(code2)
# code2.insert(0,fitnes[1:])
# code2.insert(0,fitnes[0])
# print(code2)
# print(code2[0])
# print(code2[0][0])


def select(generation):
    s = reduce(lambda first,second: first + second,range(generation_size))
    # if reduce(lambda a,b:a+b,[x[0] for x in generation]) / generation_size < 15:
        # print("a")
    # print([w / generation_size for w in range(len(generation), 0, -1)])
    selected = rand.choices(generation, weights=[(w / generation_size) / 2 for w in range(len(generation), 0, -1)])[0]
    # print([(x-generation[-1][0])/(generation[0][0] - generation[-1][0]) for x in range(len(generation), 0, -1)])
    # return a
    # return rand.choices(generation, weights=[(x-generation[-1][0])/(generation[0][0] - generation[-1][0]) for x in range(len(generation), 0, -1)])[0]
    # else:
    #     print("b")
    #     a =  rand.choices(generation, weights=[x[0] for x in generation])[0]
        # print([x[0] for x in generation])
        # return rand.choices(generation, weights=[x[0] for x in generation])[0]
    # print(generation.index(a))
    return selected


def mutate(child):
    # for x in range(2,instruction_count):
    #     if rand.random() < mutation_prob:
    #         child[x] = ~child[x]
    # old = child[0]
    if rand.random() < mutation1_prob:
        child = [0,[]] + [child[ind + 2] ^ (1 << rand.randint(0,7)) if rand.randint(0,20) == 1 else child[ind + 2] for ind in range(0,instruction_count)]
        # print("child:" + str(child))
        child = fitness(child)
        # if child[0] > old:
        #     print("hura mutacia :" + str(child[0] - old))
        # elif child[0] < old:
        #     print("ajajaj :" + str(child[0] - old))
    elif rand.random() < mutation2_prob:
        # print("heheheheheh")
        num1 = rand.randint(0,63) + 2
        num2 = rand.randint(0,63) + 2
        child[num1],child[num2] = child[num2],child[num1]
    elif rand.random() < mutation3_prob:
        # print("#################")
        child[rand.randint(0,63) + 2] = rand.randint(0,255)
    return child


def crossover(generation):
    parent1 = select(generation)
    parent2 = select(generation)
    while parent1 == parent2:
        parent2 = select(generation)
    # print(parent1)
    # print(parent2)
    cross_points = [rand.randint(0,1) for _ in range(instruction_count)]
    # cross_points = [0 if count < instruction_count / 2 else 1 for count in range(instruction_count)]
    child = [parent1[ind + 2] if cross_points[ind] == 0 else parent2[ind + 2] for ind in range(instruction_count)]
    child = [0,[]] + child
    child = fitness(child)
    child = mutate(child)
    # print(child)
    return child


def evolution():
    codes = [list((rand.randint(0,255) for x in range(0,instruction_count))) for y in range(generation_size)]
    codes = list(map(lambda x: [0,[]] + x,codes))
    codes = list(map(lambda c: fitness(c), codes))
    codes.sort(key=lambda x: x[0],reverse=True)
    # codes = [[0, [], 30, 148, 185, 14, 102, 144, 78, 28, 92, 31, 220, 212, 146, 129, 174, 188, 151, 61, 187, 175, 94, 45, 184, 125, 188, 51, 239, 164, 226, 16, 121, 59, 191, 53, 13, 77, 26, 42, 203, 153, 233, 151, 138, 203, 16, 203, 255, 162, 182, 15, 161, 162, 54, 213, 149, 196, 212, 177, 215, 67, 1, 143, 60, 184],
    #          [0, [], 193, 48, 10, 221, 239, 80, 48, 74, 239, 244, 32, 153, 124, 121, 89, 9, 108, 107, 154, 125, 84, 89, 156, 166, 120, 79, 241, 174, 44, 30, 111, 33, 119, 20, 161, 165, 95, 171, 173, 194, 134, 78, 149, 104, 180, 227, 157, 2, 29, 123, 40, 93, 219, 136, 99, 48, 113, 92, 39, 200, 140, 72, 209, 20], [0, [], 196, 209, 20, 53, 215, 187, 179, 22, 56, 88, 1, 135, 20, 154, 8, 2, 135, 0, 27, 53, 164, 227, 219, 248, 202, 242, 205, 7, 220, 100, 116, 222, 42, 165, 214, 233, 111, 120, 122, 206, 67, 18, 189, 24, 106, 139, 76, 44, 52, 9, 192, 156, 100, 14, 28, 5, 68, 60, 123, 249, 36, 210, 7, 5], [0, [], 192, 243, 177, 173, 133, 135, 203, 134, 165, 141, 147, 234, 185, 89, 196, 242, 26, 238, 174, 13, 226, 127, 193, 54, 53, 206, 130, 114, 35, 75, 115, 47, 19, 110, 101, 13, 204, 38, 114, 30, 13, 120, 16, 203, 29, 46, 208, 152, 208, 76, 32, 50, 111, 228, 48, 176, 112, 76, 147, 12, 62, 18, 147, 12], [0, [], 161, 146, 100, 65, 176, 109, 146, 191, 50, 111, 102, 201, 235, 105, 186, 101, 212, 61, 189, 13, 118, 18, 158, 202, 61, 226, 130, 188, 167, 113, 86, 205, 245, 162, 223, 132, 188, 248, 165, 8, 11, 192, 136, 50, 178, 61, 80, 11, 193, 59, 103, 166, 148, 61, 240, 150, 197, 85, 186, 143, 127, 98, 179, 249], [0, [], 105, 177, 12, 109, 36, 114, 30, 137, 7, 109, 182, 95, 61, 13, 131, 121, 208, 93, 158, 105, 181, 229, 52, 28, 3, 96, 246, 169, 103, 12, 131, 99, 132, 124, 226, 238, 101, 37, 118, 96, 67, 35, 159, 239, 239, 189, 246, 48, 122, 32, 157, 215, 210, 250, 138, 212, 232, 26, 196, 66, 11, 85, 173, 175], [0, [], 14, 185, 122, 81, 168, 17, 61, 76, 191, 235, 124, 103, 208, 222, 229, 13, 35, 155, 234, 125, 194, 247, 68, 20, 217, 64, 252, 220, 103, 170, 250, 141, 200, 229, 19, 193, 138, 92, 183, 211, 94, 202, 255, 180, 108, 236, 59, 131, 57, 250, 216, 5, 25, 89, 59, 205, 194, 102, 193, 149, 209, 32, 121, 83], [0, [], 86, 223, 219, 114, 234, 233, 214, 3, 95, 230, 19, 34, 1, 23, 8, 145, 114, 175, 35, 16, 5, 5, 107, 188, 137, 3, 10, 226, 50, 139, 116, 48, 134, 218, 36, 32, 28, 116, 147, 36, 91, 194, 30, 119, 228, 175, 194, 29, 106, 199, 56, 55, 120, 201, 50, 237, 90, 179, 69, 193, 32, 173, 116, 38], [0, [], 123, 52, 17, 232, 193, 186, 198, 108, 15, 202, 143, 206, 137, 141, 97, 67, 153, 156, 148, 120, 194, 139, 92, 141, 45, 136, 160, 60, 229, 3, 234, 144, 50, 4, 185, 148, 173, 21, 72, 196, 234, 231, 50, 9, 34, 119, 117, 203, 185, 183, 26, 151, 236, 64, 141, 8, 160, 14, 229, 190, 93, 195, 228, 227], [0, [], 226, 100, 135, 78, 56, 95, 166, 142, 240, 101, 144, 127, 187, 130, 240, 126, 22, 192, 69, 113, 193, 189, 28, 201, 190, 59, 30, 113, 208, 148, 129, 238, 189, 92, 39, 15, 209, 213, 41, 217, 15, 206, 19, 97, 229, 14, 179, 30, 131, 154, 66, 164, 23, 85, 30, 206, 215, 65, 142, 219, 252, 174, 85, 236], [0, [], 246, 17, 91, 219, 20, 53, 187, 163, 154, 186, 173, 11, 188, 148, 82, 54, 40, 193, 202, 26, 216, 228, 2, 212, 5, 65, 34, 105, 63, 79, 227, 122, 58, 43, 50, 127, 175, 179, 114, 36, 4, 213, 190, 95, 217, 158, 183, 13, 42, 219, 240, 152, 240, 9, 200, 13, 178, 255, 116, 23, 55, 243, 191, 239], [0, [], 31, 226, 160, 134, 39, 57, 174, 22, 23, 16, 217, 97, 172, 35, 20, 128, 203, 87, 96, 110, 232, 88, 64, 124, 39, 118, 134, 209, 85, 139, 37, 221, 132, 1, 76, 35, 136, 138, 249, 66, 23, 96, 174, 157, 61, 8, 111, 36, 203, 8, 168, 28, 213, 156, 244, 237, 6, 161, 44, 200, 35, 26, 84, 244], [0, [], 16, 10, 61, 154, 93, 231, 77, 160, 69, 233, 164, 147, 117, 242, 21, 98, 164, 126, 118, 156, 247, 253, 248, 13, 80, 47, 46, 196, 196, 47, 239, 119, 243, 65, 148, 173, 240, 254, 215, 80, 63, 117, 98, 210, 181, 63, 237, 186, 31, 224, 91, 186, 221, 182, 181, 90, 9, 0, 135, 18, 83, 3, 35, 62], [0, [], 217, 174, 17, 245, 144, 246, 178, 111, 224, 115, 179, 14, 167, 215, 163, 194, 62, 85, 139, 58, 150, 11, 132, 184, 183, 32, 172, 227, 206, 3, 242, 177, 102, 123, 195, 20, 107, 227, 181, 78, 129, 83, 255, 205, 163, 34, 49, 22, 128, 28, 6, 147, 237, 199, 161, 149, 219, 70, 235, 197, 113, 133, 52, 102], [0, [], 115, 159, 161, 200, 115, 1, 30, 214, 146, 148, 128, 237, 55, 202, 5, 106, 130, 186, 3, 121, 95, 11, 79, 51, 198, 112, 12, 191, 78, 129, 4, 147, 49, 58, 57, 103, 214, 19, 60, 161, 180, 35, 226, 232, 138, 133, 145, 230, 199, 201, 247, 94, 133, 217, 138, 141, 154, 24, 232, 78, 68, 207, 76, 12], [0, [], 186, 104, 21, 123, 194, 133, 234, 131, 135, 233, 83, 14, 77, 147, 225, 107, 246, 102, 20, 214, 184, 229, 114, 95, 7, 194, 53, 127, 116, 7, 250, 59, 9, 93, 15, 68, 255, 174, 103, 99, 24, 228, 1, 48, 32, 25, 36, 42, 145, 170, 41, 149, 204, 188, 125, 210, 163, 83, 241, 51, 228, 204, 165, 83], [0, [], 155, 254, 42, 18, 172, 192, 253, 248, 105, 126, 245, 1, 209, 196, 228, 18, 245, 237, 84, 112, 49, 198, 22, 225, 49, 87, 104, 69, 149, 165, 197, 105, 147, 131, 158, 179, 235, 223, 223, 110, 114, 4, 100, 233, 76, 94, 168, 128, 43, 79, 38, 118, 148, 160, 96, 66, 197, 138, 157, 170, 31, 229, 236, 37], [0, [], 48, 197, 127, 145, 4, 14, 131, 24, 3, 176, 45, 227, 176, 44, 198, 145, 29, 249, 227, 141, 89, 110, 248, 19, 240, 204, 22, 142, 156, 177, 161, 135, 5, 230, 176, 185, 19, 19, 32, 130, 129, 14, 211, 145, 47, 254, 121, 165, 211, 203, 133, 62, 239, 93, 141, 21, 160, 55, 230, 93, 227, 48, 110, 161], [0, [], 3, 102, 198, 143, 229, 37, 226, 121, 94, 23, 19, 25, 9, 33, 244, 88, 76, 118, 53, 129, 116, 201, 90, 69, 57, 21, 66, 5, 29, 27, 175, 133, 152, 228, 45, 185, 77, 147, 249, 224, 6, 29, 153, 18, 155, 196, 156, 9, 164, 56, 67, 121, 170, 162, 95, 226, 43, 37, 57, 16, 135, 55, 118, 205], [0, [], 134, 60, 61, 120, 49, 170, 155, 114, 43, 24, 70, 254, 102, 46, 10, 153, 66, 156, 0, 93, 23, 30, 112, 182, 63, 20, 130, 5, 63, 187, 127, 233, 149, 72, 212, 24, 130, 185, 40, 105, 145, 10, 98, 197, 73, 85, 189, 14, 165, 14, 25, 182, 210, 107, 137, 11, 142, 234, 245, 159, 41, 143, 222, 250]]

    # print(codes)

    # codes = [[1993, ['P', 'H', 'H', 'H', 'H', 'H', 'H'], 181, 104, 108, 246, 83, 137, 44, 101, 103, 233, 162, 43, 253, 131, 181, 1, 109, 218, 212, 179, 23, 159, 140, 148, 136, 0, 136, 231, 149, 74, 135, 45, 126, 130, 4, 195, 113, 186, 52, 6, 225, 96, 113, 44, 46, 227, 160, 100, 56, 92, 130, 93, 115, 38, 130, 6, 172, 62, 108, 218, 184, 51, 22, 212], [0, [], 78, 191, 128, 239, 52, 29, 93, 230, 187, 86, 53, 24, 233, 4, 222, 77, 165, 164, 209, 152, 194, 157, 48, 45, 28, 44, 110, 73, 80, 228, 85, 143, 37, 122, 155, 144, 157, 198, 168, 7, 115, 100, 195, 93, 119, 26, 66, 190, 97, 244, 14, 116, 5, 208, 167, 164, 148, 11, 154, 14, 82, 86, 171, 164], [0, [], 211, 100, 214, 87, 148, 152, 78, 216, 184, 28, 76, 6, 247, 3, 33, 150, 29, 78, 233, 204, 180, 91, 126, 106, 104, 192, 179, 215, 41, 9, 199, 72, 104, 246, 174, 201, 9, 50, 42, 38, 87, 115, 226, 25, 12, 202, 66, 235, 29, 54, 35, 41, 109, 167, 150, 54, 207, 146, 151, 147, 86, 16, 10, 179], [0, [], 254, 109, 68, 58, 219, 241, 10, 49, 114, 206, 170, 220, 207, 252, 92, 84, 149, 130, 181, 77, 113, 183, 21, 92, 106, 173, 63, 13, 179, 9, 204, 56, 127, 8, 197, 156, 83, 175, 83, 101, 62, 32, 181, 63, 58, 172, 236, 95, 93, 119, 222, 157, 23, 162, 198, 172, 52, 90, 136, 69, 155, 33, 102, 233], [0, [], 55, 153, 227, 139, 215, 39, 240, 163, 61, 29, 244, 238, 246, 91, 58, 120, 45, 204, 58, 187, 169, 59, 90, 31, 110, 240, 172, 51, 212, 219, 142, 30, 71, 165, 23, 140, 224, 126, 127, 249, 135, 170, 154, 146, 123, 84, 57, 229, 141, 167, 150, 130, 156, 141, 8, 101, 103, 100, 178, 130, 28, 12, 124, 203], [0, [], 237, 216, 107, 127, 111, 255, 196, 196, 24, 11, 239, 56, 141, 247, 30, 122, 75, 60, 204, 108, 235, 243, 143, 84, 167, 64, 75, 210, 103, 16, 63, 229, 151, 242, 93, 205, 217, 51, 207, 75, 24, 1, 107, 147, 30, 39, 179, 44, 252, 217, 192, 220, 179, 106, 120, 7, 27, 198, 235, 88, 206, 212, 39, 142], [0, [], 38, 31, 31, 81, 147, 63, 8, 40, 235, 50, 2, 106, 175, 37, 208, 209, 70, 26, 101, 239, 251, 4, 158, 171, 178, 226, 166, 220, 172, 222, 75, 153, 18, 6, 17, 205, 178, 10, 221, 236, 66, 149, 34, 59, 50, 82, 114, 13, 224, 133, 12, 173, 60, 50, 32, 109, 27, 76, 219, 83, 228, 158, 173, 67], [0, [], 45, 190, 251, 183, 204, 133, 224, 43, 239, 119, 151, 150, 142, 203, 178, 195, 114, 244, 194, 74, 186, 103, 148, 205, 90, 75, 125, 15, 246, 171, 47, 67, 215, 225, 218, 16, 183, 112, 246, 243, 167, 62, 1, 166, 57, 24, 41, 110, 83, 57, 252, 33, 160, 201, 255, 180, 241, 21, 150, 218, 44, 95, 47, 171], [0, [], 248, 110, 223, 35, 67, 76, 184, 11, 29, 243, 134, 120, 70, 251, 19, 32, 79, 119, 63, 1, 53, 223, 245, 137, 23, 116, 83, 197, 152, 217, 143, 194, 190, 164, 213, 30, 206, 118, 231, 131, 76, 140, 101, 4, 124, 176, 129, 92, 231, 56, 217, 14, 40, 201, 252, 190, 113, 25, 137, 226, 178, 207, 233, 95], [-1, ['P'], 23, 229, 149, 219, 227, 157, 227, 197, 215, 117, 173, 229, 109, 249, 5, 185, 246, 100, 102, 230, 75, 62, 28, 74, 48, 94, 116, 179, 187, 106, 40, 152, 250, 69, 168, 178, 220, 220, 28, 188, 81, 4, 39, 70, 101, 175, 69, 125, 86, 26, 108, 16, 102, 160, 103, 111, 142, 177, 98, 26, 251, 118, 94, 120], [-1, ['P'], 23, 64, 94, 36, 203, 216, 205, 80, 111, 49, 254, 87, 171, 193, 177, 56, 106, 163, 38, 85, 121, 131, 37, 64, 29, 64, 55, 93, 145, 28, 157, 203, 178, 100, 78, 40, 32, 64, 78, 170, 71, 125, 116, 72, 133, 65, 203, 50, 198, 111, 229, 143, 248, 172, 53, 97, 32, 154, 190, 118, 218, 178, 185, 28], [-1, ['P'], 3, 17, 252, 11, 208, 252, 215, 8, 127, 148, 179, 165, 196, 197, 95, 17, 134, 235, 68, 182, 81, 139, 163, 221, 188, 215, 69, 242, 126, 59, 147, 3, 77, 20, 48, 192, 124, 253, 188, 49, 84, 214, 200, 88, 132, 137, 212, 46, 181, 181, 8, 1, 149, 5, 250, 121, 19, 6, 21, 208, 121, 189, 10, 202], [-1, ['P'], 197, 121, 132, 223, 75, 203, 164, 94, 24, 197, 69, 254, 124, 233, 165, 103, 217, 121, 83, 100, 183, 36, 25, 154, 26, 160, 127, 77, 198, 229, 179, 209, 188, 187, 146, 125, 55, 116, 176, 225, 168, 124, 13, 84, 22, 149, 8, 194, 9, 216, 249, 0, 109, 102, 161, 170, 87, 59, 90, 46, 33, 1, 243, 15], [-1, ['P'], 184, 205, 159, 12, 140, 79, 117, 68, 104, 34, 240, 98, 194, 33, 219, 138, 48, 223, 249, 32, 105, 167, 191, 27, 39, 33, 243, 36, 152, 233, 77, 84, 119, 168, 71, 236, 214, 70, 197, 189, 196, 117, 229, 142, 36, 152, 124, 16, 157, 218, 58, 77, 69, 152, 155, 151, 44, 40, 228, 109, 232, 64, 238, 248], [-2, ['H', 'D'], 60, 88, 135, 53, 18, 154, 244, 40, 233, 144, 213, 15, 44, 183, 134, 76, 0, 146, 255, 230, 172, 198, 184, 125, 2, 8, 163, 254, 59, 149, 221, 6, 26, 240, 231, 241, 80, 88, 226, 146, 0, 90, 201, 172, 14, 191, 83, 89, 195, 1, 229, 54, 113, 72, 143, 24, 123, 193, 226, 170, 169, 203, 109, 33], [-2, ['L', 'H'], 109, 121, 89, 12, 255, 222, 59, 188, 109, 33, 44, 211, 175, 110, 27, 6, 73, 71, 133, 197, 250, 103, 81, 96, 58, 165, 42, 98, 50, 213, 10, 164, 56, 190, 122, 92, 21, 103, 82, 107, 126, 98, 133, 184, 77, 162, 189, 34, 13, 198, 136, 197, 8, 233, 8, 35, 113, 185, 27, 109, 211, 154, 104, 247], [-2, ['P', 'P'], 19, 212, 150, 227, 181, 199, 46, 103, 21, 47, 101, 99, 254, 86, 15, 83, 86, 204, 191, 250, 93, 170, 236, 132, 23, 98, 239, 107, 33, 118, 213, 230, 127, 53, 234, 235, 165, 171, 6, 175, 110, 248, 65, 119, 244, 175, 212, 205, 229, 210, 16, 155, 141, 181, 18, 74, 13, 78, 241, 150, 79, 83, 197, 23], [-2, ['L', 'P'], 90, 142, 131, 0, 116, 100, 230, 178, 84, 111, 239, 103, 34, 219, 49, 5, 250, 25, 201, 253, 243, 4, 145, 85, 135, 114, 47, 88, 67, 159, 142, 161, 237, 183, 126, 225, 45, 115, 69, 109, 90, 115, 25, 163, 66, 37, 213, 80, 156, 212, 216, 232, 20, 198, 154, 55, 147, 119, 239, 88, 215, 240, 239, 184], [-3, ['L', 'P', 'P'], 112, 233, 86, 110, 96, 250, 91, 239, 39, 76, 205, 20, 114, 97, 237, 24, 6, 216, 10, 95, 24, 251, 168, 162, 163, 43, 66, 103, 217, 109, 153, 42, 96, 93, 46, 80, 86, 188, 185, 97, 208, 223, 135, 179, 54, 59, 177, 211, 24, 255, 212, 69, 28, 200, 179, 80, 173, 23, 248, 254, 105, 67, 174, 215], [-9, ['H', 'H', 'P', 'P', 'D', 'L', 'P', 'P', 'D'], 107, 152, 196, 31, 171, 184, 23, 69, 38, 56, 46, 55, 222, 22, 254, 147, 86, 211, 53, 136, 83, 250, 195, 60, 4, 242, 216, 221, 177, 17, 230, 78, 111, 123, 251, 247, 10, 232, 38, 200, 120, 139, 196, 44, 163, 117, 199, 109, 238, 119, 210, 213, 41, 247, 78, 207, 226, 30, 96, 239, 195, 197, 134, 232]]


    x_axis = []
    y_axis = []

    print([x[0] for x in codes])
    print([x[1] for x in codes])

    for No in range(500):
        winners = list(filter(lambda child: child[0] > (no_treasures - 1) * score_per_treasure,codes))
        if len(winners) > 0:
            print("solution found:")
            return [win[1] for win in winners]
        print(codes[0][0])
        avg = reduce(lambda a,b:a+b,[x[0] for x in codes]) / generation_size
        print(avg)
        x_axis.append(No)
        y_axis.append(avg)
        # y.append(codes[0][0])
        plt.plot(x_axis, y_axis,color='g')
        # plt.pause(0.0001)
        # plt.show(block=False)
        new_g = codes[:survivers_count].copy()
        for a in range(survivers_count,generation_size):
            child = crossover(codes)
            new_g.append(child)
            # codes.sort(key=lambda x: x[0], reverse=True)
        codes = new_g.copy()
        codes.sort(key=lambda key: key[0], reverse=True)


    print(codes[0])
    print([x[0] for x in codes])
    # x = [2, 4, 6]
    # y = [1, 3, 5]
    # plt.plot(x, y)
    plt.show()

print(evolution())