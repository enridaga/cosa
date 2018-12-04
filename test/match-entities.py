#!/usr/local/bin/python
import unittest
import sys
import pprint
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.search.match import *
from cosa.search.functions import *
from cosa.graph.functions import *

class MatchEntitiesTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MatchEntitiesTest, self).__init__(*args, **kwargs)
        
    def test_entities(self):
        q = {
            "e1" :{
                'score': u'1.0',
                'types': [u'A',u'B',u'C', u'D', u'E'],
                'subjects': [u'a', u'b', u'c', u'd', u'e']
            },
            "e2": {
                'score': u'0.3',
                'types': [u'F',u'G'],
                'subjects': [u'f', u'g', u'h', u'i', u'l']
            }
        }
        
        # Full Match
        n0 = {
            "e1" :{
                'score': u'1.0',
                'types': [u'A',u'B',u'C', u'D', u'E'],
                'subjects': [u'a', u'b', u'c', u'd', u'e']
            },
            "e2": {
                'score': u'0.3',
                'types': [u'F',u'G'],
                'subjects': [u'f', u'g', u'h', u'i', u'l']
            }
        }
        
        # Partial Match
        n1 = {
            "e3" :{
                'score': u'1.0',
                'types': [u'A', u'X1', u'X2', u'X3', u'X4'],
                'subjects': [u'a', u'xb', u'xc', u'xd', u'xe']
            },
            "e2": {
                'score': u'0.3',
                'types': [u'F',u'XG'],
                'subjects': [u'f', u'g', u'xh', u'xi', u'xl']
            }
        }
        
        # No Match
        n2 = {
            "e4" :{
                'score': u'1.0',
                'types': [u'WA',u'WB',u'WC', u'WD', u'WE'],
                'subjects': [u'wa', u'wb', u'wc', u'wd', u'we']
            },
            "e5": {
                'score': u'0.3',
                'types': [u'WF',u'WG'],
                'subjects': [u'wf', u'wg', u'wh', u'wi', u'wl']
            }
        }
        
        print "Match types"
        print "Full Match"
        print matchTypes(q, n0)
        print "Partial Match"
        print matchTypes(q, n1)
        print "No Match"
        print matchTypes(q, n2)
        
        print "Match subjects"
        print "Full Match"
        print matchSubjects(q, n0)
        print "Partial Match"
        print matchSubjects(q, n1)
        print "No Match"
        print matchSubjects(q, n2)
        
        print "Match both"
        print "Full Match"
        print matchSubjects(q, n0)
        print "Partial Match"
        print matchSubjects(q, n1)
        print "No Match"
        print matchSubjects(q, n2)
        
if __name__ == '__main__':
    unittest.main()