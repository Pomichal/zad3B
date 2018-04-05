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

    def decoder(self, code):
        counter = 0
        pc = 0
        position = self.start
        steps = []

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

        def print_result():
            step = str(bin(code[address]))[2:].count('1')
            if step < 3:
                position[1] -= 1
                if position[1] < 0:
                    return False
                ##else kontroluj poklady
                else:
                    steps.append('H')
            elif step < 5:
                position[1] += 1
                if position[1] >= self.row:
                    return False
                ##else zvys kroky a poklady
                else:
                    steps.append('D')
            elif step < 7:
                position[0] += 1
                if position[0] >= self.col:
                    return False
                ##else zvys kroky a kontroluj poklady
                else:
                    steps.append('P')
            else:
                position[0] -= 1
                if position[0] < 0:
                    return False
                ##else zvys kroky a kontroluj poklady
                else:
                    steps.append('L')

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
                if not print_result():
                    return steps
            counter += 1
        return steps

a = VirtualMachine('config.json')
code = [randint(0,255) for x in range(0,64)]
print(code)
print(a.decoder(code))