import unittest
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.graph.functions import *

class GraphTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GraphTest, self).__init__(*args, **kwargs)
        
    def test_saveAndLoad(self):
        dict = {"a": 1,"b": 2, "c": 3,"e": {"h":0, "j":1, "k": 2, "l": ["m", 10, 11, 12]} }
        #arr = {0,1,2,3,4,5,6,7,8}
        saveGraph(dict, 'test_dict.dict')
        dict2 = loadGraph('test_dict.dict')
        self.assertDictEqual(dict, dict2)
        
if __name__ == '__main__':
    unittest.main()