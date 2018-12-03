#!/usr/local/bin/python
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

def _csv2graph(csv, out):
    from cosa.graph.functions import csv2graph
    csv2graph(csv, out)
    
    
def main():
    func = sys.argv[1]
    if(func == 'csv2graph'):
        _csv2graph(sys.argv[2], sys.argv[3])
    else:
        print 'Dunno'

if __name__ == "__main__":
    main()