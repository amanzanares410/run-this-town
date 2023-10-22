# test_file.py

import unittest

def add(a, b):
    return a + b
class TestYourFunction(unittest.TestCase):
    
    def test_case_1(self):
        result = add(1, 2)
        self.assertEqual(result, 3)
        
    def test_case_2(self):
        result = add(0, 0)
        self.assertEqual(result, 0)
        
    def test_case_3(self):
        result = add(-1, 1)
        self.assertEqual(result, 0)
        
if __name__ == '__main__':
    unittest.main()