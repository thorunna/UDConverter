from lib.joiners import SentJoiner, NodeJoiner, FileWriter
import sys

'''
Hinrik Hafsteinsson
Þórunn Arnardóttir
2019

Text preperation script for IcePaHC CoNLLU output file (.conllu). Not to be run
by itself, part of postrocessing pipeline.
 - Joins various nodes in IcePaHC files that have been split with '$' character
 - Joins sentences that have been split into main clauses, based on punctuation
 - Fixes UD token IDs and dependency heads after joining
 - See module code for further documentation
'''

if __name__ == '__main__':

    # for file in os.listdir('testing/corpora/icecorpus/psd_orig'):
    IN_PATH = sys.argv[1]

    file = open(IN_PATH, 'r')

    # NODES JOINED
    nj = NodeJoiner(file)
    close(file)
    # print(j.name)
    for n in reversed(nj.indexes):
        # Various clitics processed
        nj.join_clitics(n)
    f = FileWriter(nj)
    f.write_to_file(sepdir=False, overwrite=True)
    for s in

    # output written to file ()
    f1 = FileWriter(nj)
    f1.write_to_file(sepdir=False, overwrite=True)

    # SENTENCES JOINED, comment out if not wanted
    # TODO: finish

    # # former output file used as input
    # file = open(IN_PATH, 'r')
    # sj = SentJoiner(file)
    # close(file)
    #
    # final output file
    # sj.set_vars()
    # f2 = FileWriter(file)
    # f2.write_to_file(sepdir=False, overwrite=True)
