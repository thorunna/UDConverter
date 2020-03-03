from lib.depender import Converter

from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
import time
import re
import os

path.extend(['../testing/'])

icepahc = LazyCorpusLoader(
    'icecorpus/psd/', CategorizedBracketParseCorpusReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
)

if __name__ == '__main__':
    fileids = icepahc.fileids() # leave uncommented for whole corpus use
    # fileids = ['2008.ofsi.nar-sag.psd'] # For debug use only
    c = Converter() # Creates instance of Converter class
    total_sents = 0
    file_num = 1

    outputDir = '../testing/CoNLLU_output/'
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)

    # f = open('ofsi_conllu.conllu', 'w+')

    ''' Prints the dependency graph data in conllU format '''
    for fileid in fileids:

        outFileName = re.sub(r'\.psd', '.conllu', fileid)
        outFilePath = outputDir + outFileName
        outFile = open(outFilePath, 'w+')

        error_num = 0
        start = time.time()
        file_sents = 0
        # print('\nProcessing file: {0}...'.format(fileid))

        for tree in icepahc.parsed_sents(fileid):
            treeID = fileid + '_' + str(file_sents+1) + '_' + str(total_sents+1)
            try:
                dep = c.create_dependency_graph(str(tree))
                dep_c = dep.to_conllU()
                outFile.write('# sent_id = ')
                outFile.write(treeID)
                outFile.write('\n')
                outFile.write(dep_c)
                # print('# sent_id =', treeID)
                # print(dep_c)
            except Exception as ex:
                print('ERROR', '# sent_id =', treeID)
                print(tree)
                # print('Failure - {0}. Arguments:\n{1!r}'.format(type(ex).__name__, ex.args))
                raise
                error_num += 1
            file_sents += 1
            total_sents += 1
        end = time.time()
        duration = '%.2f' % float(end - start)
        # if error_num > 0:
        print('\t'.join([str(i) for i in [file_num, fileid,file_sents, error_num, str(duration)+' sec']]))
        file_num += 1

    # f.close()
