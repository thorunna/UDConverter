from lib import DMII_data
from ast import literal_eval as make_tuple
import os
import json
from pprint import pprint

# DMII_no = DMII_data.DMII_data('no')
# DMII_lo = DMII_data.DMII_data('lo')
# DMII_fn = DMII_data.DMII_data('fn')
# DMII_to = DMII_data.DMII_data('to')
# DMII_ao = DMII_data.DMII_data('ao')
# DMII_so = DMII_data.DMII_data('so')



# os.chdir('/Users/hinrik/Documents/trjabankar')
cwd = os.getcwd()
# print(cwd)


DMII_dir = os.path.join(cwd, 'DMII_data')
json_dir = os.path.join(DMII_dir, 'json')

def make_out_dir():
    if not os.path.isdir(json_dir):
        os.mkdir(json_dir)
    else:
        print('JSON directory already exists')

def remap_keys(mapping):
    return [{'key':k, 'value': v} for k, v in mapping.items()]

def write_json(dict, file):
    with open(file, 'w') as file:
        data = {str(k):v for k,v in dict.items()}
        json.dump(data, file)

def process_DMII():
    flags = ['no', 'lo', 'fn', 'to', 'ao', 'so', 'combined']
    for flag in flags:
        # print('Processing DMII data for {0}.csv...'.format(flag))
        data = DMII_data.DMII_data(flag)
        json_filename = 'DMII_{0}.json'.format(flag)
        json_filepath = os.path.join(json_dir, json_filename)
        print('Writing data to ' + json_filename)
        write_json(data, json_filepath)
        print('Finished!')




process_DMII()

# print(DMII_fn.keys())

# d = load_json(json_filepath)

# pprint(d)

# if __name__ == '__main__':
#     pass
