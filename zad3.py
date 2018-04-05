from functools import reduce
import json
from pprint import pprint


class VirtualMachine:

    def __init__(self,config):
        with open(config) as data_file:
            data = json.load(data_file)
            row = data["map"]["rows"]
            col = data["map"]["columns"]
            start = data["map"]["start"]
            no_treasures = data["map"]["number_of_treasures"]
            treasures = data["map"]["treasures"]

    def decoder(self, code):
        counter = 0
        pc = 0

        def inc(address):
            if(code[address] < 255):
                code[address] += 1
            else:
                code[address] = 0

        def dec(address):
            if(code[address] == 0):
                code[address] = 255
            else:
                code[address] -= 1

        def print_result(address):
            step = str(bin(code[address]))[2:].count('1')
            if step < 3:
                print('H')
            elif step < 5:
                print('D')
            elif step < 7:
                print('P')
            else:
                print('L')

        while counter < 501 and pc < 4:
            instruction = code[pc] >> 6
            address = code[pc] & int("00111111", 2)
            pc += 1
            if instruction == 0:
                inc(address)
            elif instruction == 1:
                print("dec")
            elif instruction == 2:
                pc = address
            elif instruction == 3:
                print_result(address)
            counter += 1

a = VirtualMachine('config.json')
a.decoder([int("00000000",2), int("11000001",2), int("00000001",2), int("11000001",2)])