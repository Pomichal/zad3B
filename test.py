import zad3 as z
from itertools import islice
import unittest

class GeneratorTests(unittest.TestCase):

    def test_cut(self):
        v = z.virtual_machine()
        code = ["00000000","01000001","10000001","11000001"]
        self.assertEqual(list(v.cut(code)),[[0,0],[1,1],[2,1],[3,1]])


if __name__ == '__main__':
    unittest.main()