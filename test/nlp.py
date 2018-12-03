#!/usr/local/bin/python
import unittest
import sys
import pprint
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.nlp.functions import *

class NlpTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(NlpTest, self).__init__(*args, **kwargs)
    
    def test_text2terms(self):
        t = "Live Animals"
        d = ['live[j]', 'animals[n]']
        self.assertEqual(d, text2terms(t))
        
if __name__ == '__main__':
    unittest.main()