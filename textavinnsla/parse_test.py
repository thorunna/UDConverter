from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *

# path.extend(['/Users/hinrik/Documents/trjabankar'])
# path.extend(['./icepahc_nltk/'])
path.extend(['./testing/'])


# icepahc = LazyCorpusLoader(
#     'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
#     r'2008\.mamma\.nar-fic\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
# )

icepahc = LazyCorpusLoader(
    'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
)

tree = icepahc.parsed_sents()[0]

ptree = ParentedTree.convert(tree)

sentence = []
runner = 0
sentence.append(['nr.', 'token', 'lemma', 'UD_tag', 'ice_tag', 'feats', 'rel', 'rel_type'])
for i in tree.pos():
    token = i[0]
    if token[0] in ['*', '0']: continue
    ice_tag = i[1]
    runner += 1
    lemma = '_'
    UD_tag = '_'
    feats = '_'
    rel = '_'
    rel_type = '_'
    line = [str(runner), token, lemma, UD_tag, ice_tag, feats, rel, rel_type]
    sentence.append(line)
print()
for i in sentence:
    print('\t'.join(i))


# print(tree.pformat_latex_qtree())
