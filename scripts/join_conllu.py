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
    file.close()
    # print(j.name)
    for n in reversed(nj.indexes):
        # Various clitics processed
        nj.join_clitics(n)
        # nj.fix_joined_space_after(n)
    # f = FileWriter(nj)
    # f.write_to_file(sepdir=False, overwrite=True)

    # output written to file ()
    f1 = FileWriter(nj)
    f1.write_to_file(sepdir=False, overwrite=True)

    # SENTENCES JOINED, comment out if not wanted
    # TODO: find more efficient way to implement (not write-rewrite output)
    #
    # # former output file used as input
    # file = open(IN_PATH, 'r')
    # sj = SentJoiner(file)
    # file.close()
    #
    # # final output file
    # sj.set_vars()
    # f2 = FileWriter(sj)
    # # in this setting = writes output to seperate directory
    # f2.write_to_file(sepdir=False, overwrite=True)
