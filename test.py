import zad3 as z
# from itertools import islice
import unittest
import random as rand


class GeneratorTests(unittest.TestCase):

    def test_virtual_do_not_change_the_code(self):
        codes = [[198, 70, 10, 247, 57, 235, 12, 36, 235, 63, 88, 240, 247, 93, 201, 191, 135, 126, 238, 2, 42, 23, 20, 144, 64, 184, 230, 181, 238, 168, 201, 216, 130, 55, 26, 203, 174, 61, 168, 56, 146, 83, 244, 251, 16, 109, 153, 15, 61, 9, 250, 16, 22, 26, 17, 12, 233, 193, 31, 30, 244, 162, 248, 170],
                [142, 138, 169, 93, 191, 104, 188, 98, 39, 159, 166, 52, 246, 189, 80, 72, 132, 16, 123, 151, 73, 170, 4, 125, 193, 127, 196, 131, 111, 138, 241, 191, 30, 107, 93, 143, 177, 85, 96, 49, 33, 221, 73, 97, 213, 80, 40, 178, 89, 239, 101, 83, 183, 69, 169, 44, 25, 127, 56, 202, 80, 249, 38, 108],
                [212, 75, 78, 55, 237, 44, 113, 205, 180, 77, 65, 240, 89, 18, 198, 67, 126, 228, 101, 195, 2, 95, 3, 57, 167, 122, 115, 228, 249, 19, 198, 109, 39, 105, 222, 21, 46, 124, 196, 240, 15, 8, 195, 202, 7, 221, 118, 150, 133, 13, 83, 196, 225, 29, 221, 167, 174, 58, 110, 30, 13, 5, 80, 236],
                [225, 143, 0, 245, 61, 255, 168, 68, 56, 55, 168, 21, 123, 37, 193, 255, 239, 108, 155, 168, 221, 167, 208, 137, 152, 205, 80, 89, 236, 184, 144, 132, 170, 201, 110, 4, 255, 156, 48, 68, 93, 232, 254, 227, 34, 75, 52, 74, 102, 174, 42, 247, 116, 204, 206, 146, 141, 34, 246, 0, 76, 55, 209, 194],
                [172, 177, 92, 167, 6, 155, 2, 13, 132, 66, 46, 172, 8, 161, 103, 189, 20, 163, 180, 17, 205, 112, 236, 212, 167, 254, 185, 35, 176, 70, 194, 107, 198, 61, 60, 223, 86, 180, 214, 70, 136, 214, 122, 247, 115, 166, 227, 33, 238, 202, 102, 225, 162, 180, 12, 113, 55, 85, 248, 200, 62, 142, 96, 224],
                [39, 146, 106, 144, 12, 236, 84, 22, 54, 108, 158, 207, 99, 225, 69, 198, 87, 1, 240, 117, 121, 226, 97, 128, 83, 220, 255, 184, 29, 245, 172, 82, 185, 181, 40, 193, 36, 191, 76, 137, 188, 206, 37, 188, 199, 1, 243, 131, 167, 70, 26, 127, 216, 252, 149, 51, 107, 188, 52, 96, 95, 49, 45, 141],
                [201, 160, 236, 160, 201, 210, 94, 198, 63, 164, 224, 94, 91, 182, 160, 54, 27, 78, 44, 214, 50, 11, 205, 153, 76, 52, 118, 191, 242, 16, 252, 12, 212, 135, 248, 212, 43, 124, 107, 238, 98, 92, 47, 174, 254, 177, 141, 175, 20, 172, 108, 126, 48, 230, 10, 144, 149, 103, 107, 242, 187, 165, 87, 137],
                [179, 236, 7, 58, 81, 151, 77, 70, 130, 44, 122, 90, 95, 168, 78, 162, 255, 187, 248, 70, 225, 17, 2, 205, 236, 221, 236, 48, 1, 18, 33, 240, 238, 168, 82, 20, 44, 44, 108, 54, 157, 86, 13, 158, 233, 186, 96, 6, 185, 60, 7, 223, 54, 14, 111, 80, 186, 61, 123, 101, 84, 103, 163, 246],
                [0,[],94, 63, 104, 143, 202, 111, 115, 112, 246, 161, 50, 64, 20, 176, 231, 135, 103, 52, 8, 247, 249, 36, 100, 144, 221, 241, 243, 179, 231, 195, 231, 146, 72, 93, 66, 137, 15, 35, 149, 198, 52, 124, 91, 238, 116, 87, 192, 11, 39, 213, 10, 9, 30, 87, 195, 32, 108, 251, 44, 166, 25, 170, 24, 169],
                [0,[],193, 48, 10, 221, 239, 80, 48, 74, 239, 244, 32, 153, 124, 121, 89, 9, 107, 107, 154, 125, 84, 89, 156, 166, 120, 79, 241, 174, 44, 28, 111, 35, 121, 20, 161, 165, 95, 171, 173, 194, 136, 78, 149, 104, 180, 227, 157, 2, 31, 123, 40, 93, 219, 136, 99, 48, 113, 92, 39, 198, 140, 72, 209, 20]]
        # self.assertEqual(code[2:],z.fitness(code)[2:]) for code in codes
        for code in codes:
            self.assertEqual(code[2:], z.fitness(code)[2:])

    def test_solution(self):
        codes = [list((rand.randint(0, 255) for x in range(z.instruction_count))) for y in range(z.generation_size)]
        print("#########")
        print(codes)
        print("#########")
        steps = 250
        winners = z.evolution(codes.copy(),steps)
        treasures = z.treasures

        def helper_control():
            if position[0] < 0 or position[0] > z.col or position[1] < 0 or position[1] >= z.row:
                return False
            else:
                return True

        def check_treasures(place):
            if len(list(filter(lambda pl: pl != place, treasures))) < len(treasures):
                treasures.remove(next(filter(lambda pl: pl == place, treasures)))
            return treasures

        while not winners and steps < 500:
            winners = z.evolution(codes.copy(),steps)
            steps += 50
        position = [z.startx,z.starty]
        directions = {'H':[1,-1],
                      'D':[1,1],
                      'L':[0,-1],
                      'P':[0,1]}

        if steps >= 500 :
            return False
        # m = map(lambda move: directions[move],winnners) for win in winners
        for win in winners:
            m = list(map(lambda move: directions[move], win))
            for step in m:
                position[step[0]] += step[1]
                self.assertEqual(True,helper_control())
                check_treasures(position)
        self.assertEqual(0,len(treasures))

    # def test_10_solutions(self):
    #     for t in range(10):
    #         self.assertNotEqual(False,self.test_solution())

if __name__ == '__main__':
    unittest.main()