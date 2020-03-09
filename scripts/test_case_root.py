# -*- coding: utf-8 -*-

'''06.03.20

Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
Debugging script for use with depender.py module
Part of UniTree project for IcePaHC
'''

import sys
from lib.rules import head_rules
from lib import relations, depender



def main(infile):
    '''05.03.20
    Test case for debugging head choice algorithm
    Prints output to command line

    Args:
        infile (string): Path to input file.

    '''
    c = depender.Converter()
    psd = ''
    with open(infile) as file:
        for line in file:
            psd += line
            if len(line.strip()) == 0 and len(psd.strip()) > 0:
                dep = c.create_dependency_graph(psd)
                print(dep.plain_text())
                print(dep.to_conllU())
                input()

if __name__ == '__main__':
    main(sys.argv[1])
