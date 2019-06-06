
import os
import csv

def get_BIN():
    bin_tokens = []
    bin_tags = []
    BIN_path = os.path.join('BIN_gogn', 'SHsnid.csv')
    BIN = csv.reader(open(BIN_path, encoding = 'UTF-8'), delimiter=';')
    for line in BIN:
        print(line)
    #     bin_tokens.append(line[4])
    #     bin_tags.append(line[5])
    # bin_both = dict(zip(bin_tokens, bin_tags))
    return bin_both

if __name__ == '__main__':
    get_BIN()
