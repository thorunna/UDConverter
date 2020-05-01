import os
import re
import json
import string
import requests

from collections import defaultdict

from lib.rules import UD_map, OTB_map
from lib.tools import decode_escaped

# in_path = str(sys.argv[1])
# in_path = 'taggers/test_conllu/2008.mamma.nar-fic.conllu'

# def getTagDict(filename):
#     OTB_path = os.path.join('../taggers','tagged', re.sub('conllu', 'txt.tagged', filename))
#     OTB_file = open(OTB_path, 'r')
#     index = 0
#     # empty tuple returned to trip token correction if end of dict found
#     indexedWords = defaultdict(lambda: ('',''))
#     for line in OTB_file.readlines():
#         # print(line)
#         if not '\t' in line: continue
#         word,tag = line.strip('\n').split('\t')
#         if word == '$': continue
#         if '``' in word:
#             # print(line.strip('\n'))
#             word = re.sub('``', '"', word)
#             # print(word)
#         index += 1
#         indexedWords[index] = word, tag
#     OTB_file.close()
#     return indexedWords

    # def featString(self):
    #     '''
    #     returns feature dict in string format that matches ConllU output
    #     returns '_' if feature dict empty
    #
    #     ex: Number=Plur|Mood=Sub|Tense=Pres|Voice=Act|Person=1
    #     ex: _
    #
    #     '''
    #     NoneType = type(None)
    #     if not isinstance(self.all_features, (str, NoneType)):
    #         return '|'.join(['='.join([k,v]) for k,v in sorted(self.all_features.items(), key=lambda x: x[0].lower())])
    #     else:
    #         return self.all_features



class Features():
    '''
    '''
    def __init__(self, tag):
        # print(tag)
        self.features = defaultdict(list)
        self.methods = {
            'n' : self._noun_features,
            'l' : self._adjective_features,
            'f' : self._pronoun_features,
            'g' : self._determiner_features,
            't' : self._numeral_features,
            's' : self._verb_features,
            'a' : self._adverb_features,
            'e' : self._other_features,
            'x' : self._other_features
        }
        self.methods.get(tag[0], lambda x: 'x')(tag)

    def _noun_features(self, tag):
        if '-' in tag:
            tag, tag_extra = tag.split('-')
        self.features['Gender'] = OTB_map['Gender'][tag[1]]
        self.features['Number'] = OTB_map['Number'][tag[2]]
        self.features['Case'] = OTB_map['Case'][tag[3]]
        if len(tag) > 4:
            self.features['Definite'] = OTB_map['Definite'][tag[4]]
        else:
            self.features['Definite'] = OTB_map['Definite'][None]
        return self

    def _adjective_features(self, tag):
        self.features['Gender'] = OTB_map['Gender'][tag[1]]
        self.features['Number'] = OTB_map['Number'][tag[2]]
        self.features['Case'] = OTB_map['Case'][tag[3]]
        self.features['Definite'] = OTB_map['Definite'][tag[4]]
        self.features['Degree'] = OTB_map['Degree'][tag[5]]
        return self

    def _pronoun_features(self, tag):
        self.features['PronType'] = OTB_map['PronType'][tag[1]]
        if tag[2] in {'1', '2'}:
            self.features['Person'] = OTB_map['Person'][tag[2]]
        else:
            self.features['Gender'] = OTB_map['Gender'][tag[2]]
        self.features['Number'] = OTB_map['Number'][tag[3]]
        self.features['Case'] = OTB_map['Case'][tag[4]]
        return self

    def _determiner_features(self, tag):
        self.features['Gender'] = OTB_map['Gender'][tag[1]]
        self.features['Number'] = OTB_map['Number'][tag[2]]
        self.features['Case'] = OTB_map['Case'][tag[3]]
        return self

    def _numeral_features(self, tag):
        self.features['NumType'] = OTB_map['NumType'][tag[1]]
        if len(tag) > 2:
            self.features['Gender'] = OTB_map['Gender'][tag[2]]
            self.features['Number'] = OTB_map['Number'][tag[3]]
            self.features['Case'] = OTB_map['Case'][tag[4]]
        return self

    def _verb_features(self, tag):
        if tag[1] not in {'s', 'þ', 'l', 'n'}:
            self.features['Mood'] = OTB_map['Mood'][tag[1]]
            self.features['Voice'] = OTB_map['Voice'][tag[2]]
            self.features['Person'] = OTB_map['Person'][tag[3]]
            self.features['Number'] = OTB_map['Number'][tag[4]]
            self.features['Tense'] = OTB_map['Tense'][tag[5]]
            self.features['VerbForm'] = OTB_map['VerbForm']['']
        elif tag[1] in {'þ', 'l'}:
            self.features['VerbForm'] = OTB_map['VerbForm'][tag[1]]
            self.features['Voice'] = OTB_map['Voice'][tag[2]]
            if tag[1] == 'þ':
                self.features['Gender'] = OTB_map['Gender'][tag[3]]
                self.features['Number'] = OTB_map['Number'][tag[4]]
                self.features['Case'] = OTB_map['Case'][tag[5]]
        else:
            self.features['VerbForm'] = OTB_map['VerbForm'][tag[1]]
            self.features['Voice'] = OTB_map['Voice'][tag[2]]
        return self

    def _adverb_features(self, tag):
        if tag[-1] in {'m', 'e'}:
            if len(tag) == 2:
                return self
            else:
                self.features['Degree'] = OTB_map['Degree'][tag[-1]]
        # else:
        #     self.features['Degree'] = None#OTB_map['Degree']['f']
        return self

    def _other_features(self, tag):
        if tag[0] == 'e':
            self.features['Foreign'] = 'Yes'

    def _get_features(self, tag):
        self.methods.get(tag[0], lambda x: 'x')(tag)
        self.features.setAll_features()
        return self

    # Here follow methods for finding a word's UD-tag from its IcePaHC tag

    @staticmethod
    def get_UD_tag(tag):
        '''

        '''
        if '-' in tag:
            tag = tag.split('-')[0]
        try:
            tag = UD_map[tag]
            return tag
        except:
            # raise
            if re.search(r'(DO|DA|RD|RA)', tag[0:2]):
                tag = 'VERB'       #ATH. merkt sem sögn í bili
                return tag
            elif re.search(r'(BE|BA|HV|HA|MD|MA)', tag[0:2]):
                tag = 'AUX'
                return tag
            elif tag == 'CONJ':
                tag = 'CCONJ'
                return tag
            elif tag in string.punctuation:
                tag = 'PUNCT'
                return tag
            else:
                tag = UD_map.get(tag[0], 'X')
                return tag

    @staticmethod
    def tagged_sent(sent):
        """
        Calls tagging API from http://malvinnsla.arnastofnun.is/about_en

        Arguments:
            dgraph: UniversalDependencyGraph
        Returns:
            type: .

        """
        try:
            url = 'http://malvinnsla.arnastofnun.is'
            payload = {'text':decode_escaped(sent), 'lemma':'on'}
            headers = {}
            res = requests.post(url, data=payload, headers=headers)
            tagged = json.loads(res.text)
            return {pair['word']:(pair['tag'],pair['lemma']) for pair in tagged['paragraphs'][0]['sentences'][0]}
        except:
            raise FeatureExtractionError('Tags could not be retrieved. Possibly no internet connection')

    # @staticmethod
    # def tagged_corpus(sent_list):
    #     try:
    #         url = 'http://malvinnsla.arnastofnun.is'
    #         payload = {'text':sent, 'lemma':'on'}
    #         headers = {}
    #         res = requests.post(url, data=payload, headers=headers)
    #         tagged = json.loads(res.text)
    #         return {pair['word']:(pair['tag'],pair['lemma']) for pair in tagged['paragraphs'][0]['sentences'][0]}
    #     except:
    #         raise FeatureExtractionError('Tags could not be retrieved. Possibly no internet connection')

class FeatureExtractionError(Exception):
    """docstring for ."""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FeatureExtractionError: {0}'.format(self.message)
        else:
            return 'FeatureExtractionError has been raised'


if __name__ == '__main__':

    in_dir = 'testing/CoNLLU_output/'
    # in_path = 'testing/CoNLLU_output/1985.sagan.nar-fic.conllu'


    for filename in os.listdir(in_dir)[1:]:
        # filename = os.path.basename(in_path)
        in_path = os.path.join(in_dir, filename)
        # OTB_path = os.path.join('taggers','tagged', re.sub('conllu', 'txt.tagged', filename))
        # OTB_path = 'taggers/tagged/2008.mamma.nar-fic.txt.tagged'
        out_path = in_path + '.tmp'

        CoNLLU_file = open(in_path, 'r')
        # OTB_file = open(OTB_path, 'r')

        CoNLLU_lines = [line.split('\t') for line in list(CoNLLU_file.readlines())]
        line_indexes = [i for i in range(len(CoNLLU_lines))]
        self.OTB_tagDict = getTagDict(filename)

        word_index = 1
        try:
            for i in line_indexes:
                f = Features(CoNLLU_lines, self.OTB_tagDict, i, word_index)
                f.get_UD_tag()
                f.get_OTB_tag()
                # print(f.index, f.IcePaHC_tag, f.UD_tag)
                # if f.OTB_token == 'Placeholder':
                #     print(f.word_index, f.token, f.OTB_token, f.OTB_tag, f.IcePaHC_tag, f.UD_tag)
                if f.OTB_tag:
                    word_index += 1
                    # print(f.word_index, f.token, f.OTB_token, f.OTB_tag, f.IcePaHC_tag, f.UD_tag)
                    # print(f.curr_line)
        except RecursionError:
            print('Recursion error!!!!')
            # print(f.curr_line)
            print(f.token, f.IcePaHC_tag)
            break
        print('You have just finished', filename)
        # input()

        CoNLLU_file.close()
        # OTB_file.close()
