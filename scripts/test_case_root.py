
from lib.rules import head_rules
from lib import relations, depender
import sys


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
                print(dep.to_conllU())
                input()

if __name__ == '__main__':
    main(sys.argv[1])
