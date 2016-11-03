#!/usr/bin/python

import gather_funcs
#from gather_funcs import FakeEntropyGatherer

def main():
    # Get a list of entropy gatherers
    gather_funcs = filter(lambda x: callable(x), gather_funcs.__dict__.values())
    print("Loaded %s entropy functions.")

if __name__ == '__main__':
    main()
