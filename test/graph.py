import unittest
import sys
import pprint
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.graph.functions import *

class GraphTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GraphTest, self).__init__(*args, **kwargs)
        
    def test_showGraph(self):
        node = {}
        node['label'] = 'ROOT'
        node['root'] = True
        node['sub'] = []
        subItem = {}
        subItem['label'] = 'Live Animals'
        subItem['terms'] = {
            'live': {
                'live': 1.0,
                'alive': 0.9
            },
            'animals': {
                'live': 1.0,
                'alive': 0.9
            }
        }
        subItem['entities'] = {
            'http://uk.dbpedia.org/ontology/Animal': {
                'score': 0.8,
                'types': [],
                'subjects': []
            }
        }
        node['sub'].append(subItem)

        pprint.pprint(node)


    def test_saveAndLoad(self):
        dict = {"a": 1,"b": 2, "c": 3,"e": {"h":0, "j":1, "k": 2, "l": ["m", 10, 11, 12]} }
        #arr = {0,1,2,3,4,5,6,7,8}
        saveGraph(dict, 'test_dict.dict')
        dict2 = loadGraph('test_dict.dict')
        self.assertDictEqual(dict, dict2)
        
if __name__ == '__main__':
    unittest.main()