
'''
convert.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2020
Part of UniTree project for IcePaHC
'''

import time
import re
import os
import json
import requests
import subprocess
from sys import stdin, stdout

from nltk.corpus.util import LazyCorpusLoader
from nltk.data import path

from lib.depender import Converter
from lib.reader import IcePaHCFormatReader, IndexedCorpusTree
from lib.tools import decode_escaped, fix_IcePaHC_tree_errors, tagged_corpus

def run_pre(corpus_path):
    '''Run preprocessing shell script for the given corpus.'''
    subprocess.check_call(
        ['./preProcess.sh', corpus_path])
#
# def run_post():
#     '''Run postprocessing shell script for the given corpus.'''
#     subprocess.check_call(['./postProcess.sh', '../testing/CoNLLU_output'])

def fix_annotation_errors(corpus_path, new_corpus_path):
    '''Run error fix shell script for given .psd file'''
    subprocess.check_call(['./fix_corpus_errors.sh', corpus_path, new_corpus_path])

# def run_pre_file(file_path):
#     '''Run preprocessing shell script for given .psd file'''
#     subprocess.check_call(['./preProcessSingleFile.sh', file_path])

def run_post_file(file_path):
    '''Run postprocessing shell script for given .conllu file'''
    subprocess.check_call(['./postProcessSingleFile.sh', file_path])

def main():

    IcePaHC_DIR = '../psd/corpora/icepahc-v0.9/psd'
    FIXED_IcePaHC_DIR = '../psd/corpora/icepahc-v0.9/psd_fix'

    fix_annotation_errors(IcePaHC_DIR, FIXED_IcePaHC_DIR)

    run_pre(FIXED_IcePaHC_DIR)

    path.extend(['../psd/'])

    ICEPAHC = LazyCorpusLoader(
        'icepahc-v0.9/psd_fix/', IcePaHCFormatReader,
        r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
        )

    fileids = ICEPAHC.fileids()  # leave uncommented for whole corpus use
    # fileids = ['1150.homiliubok.rel-ser.psd'] # For debug use only
    # fileids = ['2008.mamma.nar-fic.psd', '2008.ofsi.nar-sag.psd'] # For debug use only

    # Instance of Converter class
    c = Converter(auto_tags='corpus')
    # c = Converter()
    total_sents = 0
    file_num = 1

    # OUTPUT_DIR = '../testing/CoNLLU_output/'
    OUTPUT_DIR = '../IcePaHC-CoNLLU/'
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # f = open('ofsi_conllu.conllu', 'w+')

    ''' Prints the dependency graph data in conllU format '''
    for fileid in fileids:

        OUT_FILE_NAME = re.sub(r'\.psd', '.conllu', fileid)
        OUT_FILE_PATH = OUTPUT_DIR + OUT_FILE_NAME
        OUT_FILE = open(OUT_FILE_PATH, 'w+')

        # file_length = len(ICEPAHC.parsed_sents(fileid))

        error_num = 0
        start = time.time()
        file_sents = 0

        # print('\nProcessing file: {0}...'.format(fileid))
        tree_counter = 0

        tag_dict = tagged_corpus(ICEPAHC.parsed_sents(fileid))
        c.set_tag_dict(tag_dict)

        to_join = []
        try:
            for tree in ICEPAHC.parsed_sents(fileid):

                # Catch error in corpus where punctuation tokens are missing
                tree = fix_IcePaHC_tree_errors(tree)

                # UniversalDependencyGraph object created from tree
                dep = c.create_dependency_graph(tree)

                # Sentences split between clauses joined together and output written
                # to file
                if dep.get_by_address(len(dep.nodes)-1)['word'] not in {'.', ':', '?', '!', 'kafli', 'kapítuli'} \
                and len(dep.nodes) != 1:
                    to_join.append(dep)
                else:
                    if len(to_join) == 0:
                        # write out dep. graphs that don't need to be joined
                        dep_c = c.add_space_after(dep).to_conllU()

                        sent_id = re.sub(r'\.psd', '', fileid).upper() + ',' + str(file_sents+1) + '.' + str(total_sents+1)
                        sent_id_line = '# sent_id = ' + sent_id + '\n'

                        text_line = dep.plain_text()+'\n'
                        # icepahc_id_line = str(dep.original_ID_plain_text(corpus_name='IcePaHC')) + '\n'
                        icepahc_id_line = str(dep.original_ID_plain_text()) + '\n'
                        OUT_FILE.write(sent_id_line)
                        OUT_FILE.write(icepahc_id_line)
                        OUT_FILE.write(text_line)
                        OUT_FILE.write(dep_c)
                        file_sents += 1
                        total_sents += 1
                    else:
                        # write out joined dependency graphs
                        to_join.append(dep)
                        dep = c.add_space_after(c.join_graphs(to_join))
                        dep_c = dep.to_conllU()

                        sent_id = re.sub(r'\.psd', '', fileid).upper() + ',' + str(file_sents+1) + '.' + str(total_sents+1)
                        sent_id_line = '# sent_id = ' + sent_id + '\n'

                        text_line = dep.plain_text()+'\n'
                        # icepahc_id_line = str(dep.original_ID_plain_text(corpus_name='IcePaHC')) + '\n'
                        icepahc_id_line = str(dep.original_ID_plain_text()) + '\n'
                        OUT_FILE.write(sent_id_line)
                        OUT_FILE.write(icepahc_id_line)
                        OUT_FILE.write(text_line)
                        OUT_FILE.write(dep_c)
                        file_sents += 1
                        total_sents += 1
                    to_join = []

                tree_counter += 1
        except Exception as ex:
            print('ERROR', '# sent_id =', sent_id)
            print(tree.corpus_id)
            print(tree)
            print('Failure - {0}. Arguments:\n{1!r}'.format(type(ex).__name__, ex.args))
            raise
            error_num += 1

        run_post_file(OUT_FILE_PATH)

        end = time.time()
        duration = '%.2f' % float(end - start)
        # if error_num > 0:
        print('\t'.join([str(i) for i in [file_num, fileid, tree_counter, file_sents, error_num, str(duration)+' sec']]))
        file_num += 1

    # run_post()


if __name__ == '__main__':
    main()
