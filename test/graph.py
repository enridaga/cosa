import unittest

class GraphTest(unittest.TestCase):
    def __init__(self):
        import sys
        from os.path import dirname, join, abspath
        sys.path.insert(0, abspath(join(dirname(__file__), '..')))
        import cosa
        
    def saveAndLoadTest(self):
        dict = {"a": 1,"b": 2, "c": 3,"e": {"h":0, "j":1, "k": 2, "l": ["m", 10, 11, 12]} }
        arr = {0,1,2,3,4,5,6,7,8}
        print arr
        
if __name__ == '__main__':
    unittest.main()