import re
import sys
import os

from lib.features import Features, getTagDict

'''
# TODO: Eventually move feature insertion into depender module

Hinrik Hafsteinsson 2019
Þórunn Arnardóttir
Part of UniTree project for IcePaHC

Text preperation script for CoNLL-U output file (.conllu). Not to be run by itself,
part of postprocessing pipeline.
 - Renames various string nodes in CoNLL-U lines
 - input: .conllu file on command line (edits files in situ by renaming/removing)
'''

WORD_INDEX = 1

def rename_abbrevations(line):
    '''
    Replaces (standard) abbrevations in CoNLLU with corresponding word
    '''
    ABBR = r'^\$?([A-Za-zþðöÞÐÖ]|frv|fl)\.?\$?$'
    abbr_map = {
        #abbr : token, lemma, lemma(true)
        'o.' : ('og', 'og', 'og'),
        's.' : ('svo', 'svo', ''),
        'frv.' : ('framvegis', 'framvegis', ''),
        't.' : ('til', 'til', ''),
        't.' : ('til', 't', ''),
        'd.' : ('dæmis', 'dæmi', ''),
        'fl.' : ('fleira', 'margur', ''),
        't.$' : ('til', 't', 'til'),
        '$d.' : ('dæmis', 'd', 'dæmi'),
        'þ.$' : ('það', 'þú', 'þú'),
        '$e.' : ('er', 'vera', ''),
        '$e.$' : ('er', 'vera', ''),
        '$a.$' : ('að', 'a.', 'að'),
        '$s.' : ('segja', 's', 'segja'),
        'a$' : ('að', 'að', 'að'),
        '$m$' : ('minnsta', 'lítill', ''),
        '$k' : ('kosti', 'kostur', ''),
        'm.$' : ('meðal', 'm', 'meðal'),
        '$a.' : ('annars', 'annar', ''),
        'm.$' : ('meira', 'm', 'meira'),
        '$a.$' : ('að', 'a.', 'að'),
        '$s.' : ('segja', 's', 'segja'),
        't.$' : ('til', 'til', ''),
        '$d.' : ('dæmis', 'dæmis', '')
    }

    # line = line.split('\t')
    if len(line) < 10: return line # '\t'.join(line)
    for k,v in abbr_map.items():
        if line[1] == k and line[2] == v[1]:
            line[1] = v[0]
            if len(line[2]) <= 2:
                line[2] = v[2]
            # print(line)
    # line = '\t'.join(line)
    return line

def fix_dash(line):
    '''
    Fixes various punctuations (-, /, ') that are escaped in corpus data
    '''
    # line = line.split('\t')
    if len(line) < 10: return line # '\t'.join(line)
    if re.search(r'[<>]', line[1]):
        ''' Tokens processed '''
        # print('\t', line[1], line[2])
        if re.search(r'</?dash/?>', line[1]):
            line[1] = re.sub(r'</?dash/?>', '-', line[1])
        elif re.search(r'</?slash/?>', line[1]):
            line[1] = re.sub(r'</?slash/?>', '/', line[1])
        elif re.search(r'</?apostrophe/?>', line[1]):
            line[1] = re.sub(r'</?apostrophe/?>', "'", line[1])
        else:
            # print('\t', line[1], line[2])
            pass
    if re.search(r'[<>]', line[2]):
        ''' Lemmas processed '''
        if re.search(r'</?dash/?>', line[2]):
            ''' Note: dash (-) must either removed or kept in lemma'''
            line[2] = re.sub(r'</?dash/?>', '', line[2]) # dash removed
            # line[2] = re.sub(r'</?dash/?>', '-', line[2]) # dash kept
        elif re.search(r'</?slash/?>', line[2]):
            line[2] = re.sub(r'</?slash/?>', '/', line[2])
        elif re.search(r'</?apostrophe/?>', line[2]):
            line[2] = re.sub(r'</?apostrophe/?>', "'", line[2])
        else:
            # print('\t', line[1], line[2])
            pass
    # line = '\t'.join(line)
    return line

def insert_features(lines, OTB_tagDict, line_index):
    '''
    '''
    global WORD_INDEX

    if len(lines[line_index]) < 10: return lines[line_index]
    try:
        f = Features(lines, OTB_tagDict, line_index, WORD_INDEX)
        # print(f.curr_line)
        f.get_UD_tag()
        f.get_OTB_tag()
        # if f.OTB_tag:
        if f.OTB_tag:
            WORD_INDEX += 1
            # print(f.word_index, f.token, f.OTB_token, f.OTB_tag, f.IcePaHC_tag, f.UD_tag)
            # print('start')
            # print(f.curr_line)
            # print(f.token, f.OTB_tag, f.features.featString())
            lines[line_index][3] = re.sub(lines[line_index][3], f.UD_tag, lines[line_index][3])
            if not f.features.featString() == '':
                lines[line_index][5] = re.sub(lines[line_index][3], f.features.featString(), lines[line_index][3])
            lines[line_index][9] = re.sub('_', f.OTB_tag, lines[line_index][9])
            # print(lines[line_index], f.token)
            # return WORD_INDEX
            return lines[line_index]
    except RecursionError:
        print('Recursion error!!!!')
        # print(f.curr_line)
        print(f.token, f.IcePaHC_tag)
        return

def remove_split(line):
    '''
    '''
    line = '\t'.join(line)
    line = re.sub(r'\$', '', line)
    return line.split('\t')

def check_None(line):
    line = line.split('\t')
    if len(line) < 10: return '\t'.join(line)
    elif 'None' in line:
        return None
    else:
        return '\t'.join(line)


def debug_iterate_lines():
    '''
    Function for testing script and safe debugging
    '''
    for filename in os.listdir('testing/CoNLLU_output'):
        print(filename)
        in_path = os.path.join('testing/CoNLLU_output', filename)
        # OTB_path = os.path.join('taggers','tagged', re.sub('conllu', 'txt.tagged', filename))

        OTB_tagDict = getTagDict(filename)

        in_file = open(in_path)
        lines = in_file.readlines()
        lines = [line.split('\t') for line in lines]
        in_file.close()

        # indexes = range(len(lines))
        line_indexes = [i for i in range(len(lines))]

        for index in line_indexes:
            lines[index] = fix_dash(lines[index])
            lines[index] = rename_abbrevations(lines[index])
            lines[index] = remove_split(lines[index])
            lines[index] = insert_features(lines[index])


def main():
    in_path = sys.argv[1]
    # in_path = 'testing/CoNLLU_output/1350.bandamennM.nar-sag.conllu'

    out_path = in_path + '.tmp'
    in_file = open(in_path, 'r')
    out_file = open(out_path, 'w')

    filename = os.path.basename(in_path)
    OTB_tagDict = getTagDict(filename)

    lines = in_file.readlines()
    lines = [line.split('\t') for line in lines]
    in_file.close()
    line_indexes = [i for i in range(len(lines))]

    for index in line_indexes:
        lines[index] = fix_dash(lines[index])
        lines[index] = rename_abbrevations(lines[index])
        lines[index] = remove_split(lines[index])
        lines[index] = insert_features(lines, OTB_tagDict, index)
        # if lines[index] == None:
        #     print(lines[index])

    for line in lines:
        try:
            line = '\t'.join(line)
            out_file.write(line)
        except TypeError:
            continue
        # except TypeError:
        # print(line)


    out_file.close()
    os.remove(in_path)
    os.rename(out_path, in_path)

if __name__ == '__main__':
    # debug_iterate_lines()
    main()
