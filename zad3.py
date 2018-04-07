from functools import reduce
import json
from pprint import pprint
from random import randint


class VirtualMachine:

    def __init__(self,config):
        with open(config) as data_file:
            data = json.load(data_file)
            self.row = data["map"]["rows"]
            self.col = data["map"]["columns"]
            self.start = data["map"]["start"]
            self.no_treasures = data["map"]["number_of_treasures"]
            self.treasures = data["map"]["treasures"]
            self.instruction_count = data["inst_count"]
            self.score_per_treasure = data["score_per_treasure"]
            self.score_per_step = data["score_per_step"]

    def decoder(self, code):
        counter = 0
        pc = 0
        position = self.start
        steps = [0]
        place_of_treasures = self.treasures

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

        def move(direction):
            if direction == 'H':
                position[1] += 1
                if position[1] <= 0:
                    return False

        def check_treasures(place):
            if len(list(filter(lambda x: x != place, place_of_treasures))) < len(place_of_treasures):
                place_of_treasures.remove(next(filter(lambda x: x == place, place_of_treasures)))
                return self.score_per_treasure
            else:
                return 0

        def print_result():
            step = str(bin(code[address]))[2:].count('1')
            if step < 3:
                position[1] -= 1
                if position[1] < 0:
                    return False
                else:
                    steps.append('H')
            elif step < 5:
                position[1] += 1
                if position[1] >= self.row:
                    return False
                else:
                    steps.append('D')
            elif step < 7:
                position[0] += 1
                if position[0] >= self.col:
                    return False
                else:
                    steps.append('P')
            else:
                position[0] -= 1
                if position[0] < 0:
                    return False
                else:
                    steps.append('L')
            steps[0] += self.score_per_step + check_treasures(position)
            if len(place_of_treasures) == 0:
                return False

        while counter < 501 and pc < self.instruction_count:
            instruction = code[pc] >> 6
            address = code[pc] & int("00111111", 2)
            pc += 1
            if instruction == 0:
                inc()
            elif instruction == 1:
                dec()
            elif instruction == 2:
                pc = address
            elif instruction == 3:
                if print_result() == False:
                    steps[0] -= self.score_per_treasure * len(place_of_treasures)
                    return steps
            counter += 1
        steps[0] -= self.score_per_treasure * len(place_of_treasures)
        return steps


a = VirtualMachine('config.json')
code2 = [randint(0,255) for x in range(0,64)]
print(code2)
#code = [198, 70, 10, 247, 57, 235, 12, 36, 235, 63, 88, 240, 247, 93, 201, 191, 135, 126, 238, 2, 42, 23, 20, 144, 64, 184, 230, 181, 238, 168, 201, 216, 130, 55, 26, 203, 174, 61, 168, 56, 146, 83, 244, 251, 16, 109, 153, 15, 61, 9, 250, 16, 22, 26, 17, 12, 233, 193, 31, 30, 244, 162, 248, 170]
#code = [142, 138, 169, 93, 191, 104, 188, 98, 39, 159, 166, 52, 246, 189, 80, 72, 132, 16, 123, 151, 73, 170, 4, 125, 193, 127, 196, 131, 111, 138, 241, 191, 30, 107, 93, 143, 177, 85, 96, 49, 33, 221, 73, 97, 213, 80, 40, 178, 89, 239, 101, 83, 183, 69, 169, 44, 25, 127, 56, 202, 80, 249, 38, 108]


print(a.decoder(code2))