from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *

path.extend(['./testing/'])


s = '---'
print(s.split('-'))


icepahc = LazyCorpusLoader(
    'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
)

fileids = icepahc.fileids() # TODO: Get fileid info per tree for tree ids
# sents = icepahc.parsed_sents()

def sent_text(sentence):
    '''
    Takes in a nltk Tree object and returns the sentence text in string form
    '''
    text = []
    leaves = sentence.pos()
    for leaf in leaves:
        # print(leaf)
        if len(leaf[0]) == 1:
            leaf = leaf[1]
        elif leaf[0] == '---':
            leaf = '-'
        elif leaf[0] == '-----':
            leaf = '--'
        else:
            leaf = leaf[0].split('-')
        if leaf[0][0] in {'*', '0', ''}: continue
        text.append(leaf[0])
    return text

with open('sent_ERRORS.out', 'w') as file:
    total_num = 0
    for fileid in fileids:
        sent_num = 0
        for tree in icepahc.parsed_sents(fileid):
            id = fileid + '_' + str(sent_num + 1)
            try:
                text = sent_text(tree)
                sent_num += 1
                total_num += 1
                # print(id, total_num+1)
                # print(' '.join(text))
                # print(tree)
                # file.write(id + '\t' + str(total_num) + ' '.join(text) + '\n')
            except AttributeError:
                sent_num += 1
                total_num += 1
                # print(fileid, sent_num, 'ERROR - flat tree', ' '.join(text))
                print(id, total_num+1, 'ERROR - flat tree')
                file.write('(ERROR - flat tree)' + '\t' + id + '\t' + str(total_num) + '\t' + ' '.join(text) + '\n')
            except IndexError:
                sent_num += 1
                total_num += 1
                print(id, total_num+1, 'ERROR - something INDEX')
                # print(fileid, senþt_num, 'ERROR - something INDEX', ' '.join(text))
                print(tree)
                # raise
                file.write('(ERROR - something INDEX)' + '\t' + id + '\t' + str(total_num) + '\t' + ' '.join(text) + '\n')
            # print(text)