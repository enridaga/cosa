#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

def _dataset(outputFile):
    from cosa.data.functions import dataset
    dataset(outputFile)

        
def _help():
    print 'Usage: '
    print ' ./devel.py dataset <saveToFile>'

def main():
    _dataset(sys.argv[1]);

if __name__ == "__main__":
    main()