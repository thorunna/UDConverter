import pyconll
import pyconll.util
import sys
import os

# script that reads conllu file as first argument (path) and prints sentences
# that have != 1 root (most likely 0 or 2 roots)

def get_root_errors(in_file, no_roots_file, many_roots_file):
    count_roots = 0
    no_roots = 0
    many_roots = 0

    for sentence in in_file:

        count_roots = 0
        for token in sentence:
            if token.deprel == 'root' or token.head == '0':
                # print(token.deprel)
                count_roots = count_roots + 1
                # print(count_roots)
        if count_roots == 0:
            no_roots += 1
            no_roots_file.write(sentence.conll())
            no_roots_file.write('\n')
            no_roots_file.write('\n')
            # print('Sentences with != 1 root: ',sentence.conll())
        if count_roots > 1:
            no_roots += 1
            many_roots_file.write(sentence.conll())
            many_roots_file.write('\n')
            many_roots_file.write('\n')

    print('Sents. with no roots: ', no_roots)
    print('Sents. with many roots: ', many_roots)

def main():
    f = open('root_check/no_root_allt.txt', 'w+')
    f2 = open('root_check/too_many_roots_allt.txt', 'w+')
    conllu_path = sys.argv[1]
    for conllu_file in os.listdir(conllu_path):
        print('Current file:', conllu_file)
        train = pyconll.load_from_file(os.path.join(conllu_path, conllu_file))
        get_root_errors(train, f, f2)
    f.close()
    f2.close()


if __name__ == '__main__':
    main()
