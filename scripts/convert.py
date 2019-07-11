from lib import DMII_data
from lib import depender

from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
import time
import re

path.extend(['./testing/'])

DMII_combined = DMII_data.load_json('combined') # TODO: Move to features script

icepahc = LazyCorpusLoader(
    'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
)

#if __name__ == '__main__':
#fileids = icepahc.fileids() # leave uncommented for whole corpus use
fileids = ['1985.sagan.nar-fic.psd'] # For debug use only
c = depender.Converter() # Creates instance of Converter class
total_sents = 0

    #f = open('voggur_conllu.conllu', 'w+')

''' Prints the dependency graph data in conllU format '''
for fileid in fileids:
    error_num = 0
    start = time.time()
    file_sents = 0
    print('\nProcessing file: {0}...'.format(fileid))
    for tree in icepahc.parsed_sents(fileid):
        treeID = fileid + '_' + str(file_sents+1) + '_' + str(total_sents+1)
        try:
            dep = c.create_dependency_graph(str(tree))
            dep_c = dep.to_conllU()
                #print(dep_c)
                #f.write('# sent_id =', treeID)
            print('# sent_id =', treeID)
                #f.write(dep.to_conllU())
            print(dep.to_conllU())
        except:
            error_num += 1
        file_sents += 1
        total_sents += 1
    end = time.time()
    duration = '%.2f' % float(end - start)
    print('Finished! Time elapsed: {0} seconds'.format(duration))
    print('Number of sentences in file: {0}'.format(file_sents))
    print('Number of failed sentences: {0}'.format(error_num))

    #f.close()
