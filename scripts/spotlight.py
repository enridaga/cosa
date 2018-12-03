#!/usr/local/bin/python

def main():
    import sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from cosa.dbpedia.spotlight import spotlight


    print spotlight('snake',0.1)


if __name__ == "__main__":
    main()