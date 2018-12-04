#!/usr/local/bin/python
import unittest
import sys
import pprint
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cosa.search.match import *
from cosa.nlp.functions import *
from cosa.graph.functions import *

class MatchTest(unittest.TestCase):
    CEREALS = {'code': '1000000000-80', 'terms': {'cereals[n]': {u'stewed[n]': 0.7764776349067688, u'compote[n]': 0.755449116230011, u'puddings[n]': 0.7699476480484009, u'rissoles[n]': 0.7585991621017456, u'hard-cooked[j]': 0.7554789781570435, u'strawberries[n]': 0.7493680119514465, u'stuffed[n]': 0.7855944633483887, u'sliced[n]': 0.7470594048500061, u'beets[n]': 0.7468308806419373, u'vegetables[n]': 0.7578145861625671, u'braised[n]': 0.7556328773498535, u'horse-radish[j]': 0.7597455382347107, u'butterine[n]': 0.753279983997345, u'diced[j]': 0.7449774146080017, u'meats[n]': 0.7527689337730408, u'raspberries[n]': 0.7478814721107483, u'popovers[n]': 0.8091792464256287, u'cooked[n]': 0.7515818476676941, u'succotash[n]': 0.7594679594039917, u'radishes[n]': 0.746717095375061, u'cutlets[n]': 0.7511512041091919, u'cucumbers[n]': 0.7651965618133545, u'tarragon[n]': 0.757579505443573, u'reduced[n]': 0.7441823482513428, u'mushrooms[n]': 0.7890390157699585, u'prunes[n]': 0.7568647861480713, u'lemons[n]': 0.7575535178184509, u'poached[n]': 0.7699248194694519, u'unroasted[j]': 0.7560224533081055, u'corned[n]': 0.792959988117218, u'cookies[n]': 0.749269425868988, u'celeriac[n]': 0.7549691200256348, u'chive[n]': 0.7475379109382629, u'preserves[n]': 0.7537457942962646, u'scallops[n]': 0.746527373790741, u'planked[n]': 0.7591778635978699, u'creamed[n]': 0.7523108124732971, u'grilled[n]': 0.7670201063156128, u'okra[n]': 0.7945480346679688, u'soups[n]': 0.7799786329269409, u'chilli[n]': 0.770285427570343, u'dumplings[n]': 0.7757858633995056, u'hashed[n]': 0.7506567239761353, u'brocoli[n]': 0.7520615458488464, u'dried[n]': 0.8089413046836853, u'croquettes[n]': 0.7475957870483398, u'finely-minced[j]': 0.7531716823577881, u'jellied[n]': 0.7826042175292969, u'parsnips[n]': 0.761404275894165, u'cherries[n]': 0.7753180265426636, u'wines[n]': 0.7490634918212891, u'pickling[n]': 0.7451664805412292, u'mince[n]': 0.7616487741470337, u'salads[n]': 0.7466615438461304, u'salsify[n]': 0.7504962682723999, u'apricots[n]': 0.7620011568069458, u'curried[n]': 0.7748796343803406, u'malted[n]': 0.7446199059486389, u'almonds[n]': 0.7666484117507935, u'sauces[n]': 0.7901585102081299, u'scalloped[n]': 0.7710123062133789, u'tomatoes[n]': 0.7844180464744568, u'roasted[n]': 0.7706313133239746, u'truffles[n]': 0.74699866771698, u'steamed[n]': 0.7711057662963867, u'turnips[n]': 0.7592406272888184, u'lentils[n]': 0.7919096946716309, u'cooked[j]': 0.7885929942131042, u'dressings[n]': 0.7512006759643555, u'escalloped[n]': 0.7746775150299072, u'cantaloup[n]': 0.7442024350166321, u'canned[n]': 0.8098195791244507, u'minced[n]': 0.7766795754432678, u'cauliflowers[n]': 0.7439226508140564, u'desserts[n]': 0.757439911365509, u'sprouts[n]': 0.7770397067070007, u'raisins[n]': 0.7805812358856201, u'pineapples[n]': 0.7846521139144897, u'kohlrabi[n]': 0.7606574892997742, u'protose[n]': 0.7465308308601379, u'haricot[n]': 0.7529014945030212, u'wafers[n]': 0.774757981300354, u'balls[n]': 0.7494478225708008, u'puree[n]': 0.7643208503723145, u'candies[n]': 0.7488436102867126, u'currants[n]': 0.7679557204246521, u'catchup[n]': 0.7539600133895874, u'artichokes[n]': 0.7760335206985474, u'fritters[n]': 0.7545848488807678, u'rice[v]': 0.755017101764679, u'chervil[n]': 0.7520471811294556, u'salted[n]': 0.7482898831367493, u'clove[v]': 0.7437666058540344, u'catsup[n]': 0.7708659768104553, u'eggplant[n]': 0.7650061249732971, u'saut\xe9d[n]': 0.7843319177627563, u'horseradish[n]': 0.7598838806152344, u'comp\xf4te[n]': 0.7541021108627319, u'breads[n]': 0.7494605779647827, u'tartare[n]': 0.7760413885116577}}, 'parent': False, 'label': 'CEREALS', 'other': False, 'row': {'End date': '', 'Indent': '', 'Description': 'CEREALS', 'Language': 'EN', 'Hier.Pos.': '2', 'Goods code': '1000000000 80', 'Start date': '31/12/1971 '}}
    
    def __init__(self, *args, **kwargs):
        super(MatchTest, self).__init__(*args, **kwargs)
    
    def test_terms(self):
        q = {}
        q['label'] = 'Emerald Tree Boa'
        terms = text2terms(q['label'])
        asDict = {}
        for n in terms:
            asDict[n] = {n: 1.0}
        q['terms'] = asDict
        
        n1 = self.CEREALS
        n2 = self.ANIMALS
        
        print match
        
if __name__ == '__main__':
    unittest.main()