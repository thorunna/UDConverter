import os
import csv
import time

DMII_path = os.path.join('DMII_data', 'SHsnid.csv')
spurnarmyndir_path = os.path.join('DMII_data', 'spurnarmyndir.txt')
plastur_path = os.path.join('DMII_data', 'plastur.feb2013.txt')

DMII = csv.reader(open(DMII_path, encoding = 'UTF-8'), delimiter=';')
SpMy = csv.reader(open(spurnarmyndir_path, encoding = 'UTF-8'), delimiter=';')
Plst = csv.reader(open(plastur_path, encoding = 'UTF-8'), delimiter=';')

#for row in Plst:
#    print(row)

#f = open('plastur_copy', 'w+')
#f.write(Plst)
#f.close()

#with open('plastur_copy', 'w+', encoding='utf-8') as file:
#    for row in Plst:
#        file.write(row)

namelist = ['no', 'lo', 'so', 'ao', 'pfn', 'afturbfn', 'fn', 'to', 'gr']

no = []
lo = []
so = []
ao = []
pfn = []
afturbfn = []
fn = []
to = []
gr = []


# with open('BKL_utts.03.tsv', 'w') as tsvfile:
#     writer = csv.writer(tsvfile, delimiter='\t')
#     for line in all_lines:
#         writer.writerow(line)

def makefiles(list, dir):
    for name in list:
        start = time.time()
        filename = os.path.join(dir, name+'.csv')
        print('Writing to file:', filename)
        list_var = globals()[name]
        with open(filename, 'w') as file:
            writer = csv.writer(file, delimiter=';')
            for line in list_var:
                writer.writerow(line)
        end = time.time()
        print('Done. Time elapsed:', end-start, 'seconds')

def split(dmii, string):
    print('Processing {0}...'.format(string))
    start = time.time()
    for line in dmii:
        # if line[2] not in {'kk', 'kvk', 'hk', 'so', 'lo'}:
        #     print(line[2], end=' ')
        if line [2] in {'kk', 'kvk', 'hk'}:
            no.append(line)
        elif line [2] == 'lo':
            lo.append(line)
        elif line [2] == 'so':
            so.append(line)
        elif line [2] == 'ao':
            ao.append(line)
        elif line [2] == 'pfn':
            pfn.append(line)
        elif line [2] == 'abfn':
            afturbfn.append(line)
        elif line [2] == 'fn':
            fn.append(line)
        elif line [2] == 'to':
            to.append(line)
        elif line [2] == 'gr':
            gr.append(line)
        else:
            continue
            # print(line)

    end = time.time()
    print('Time elapsed:', end-start, 'seconds.')

split(DMII, 'DMII database')
split(Plst, 'Plástur')
split(SpMy, 'Spurnarmyndir')

parent_dir = os.path.join('DMII_data', 'split2')
os.mkdir(parent_dir)

makefiles(namelist, parent_dir)

print('Nafnorð:', len(no))
print('lýsingarorð:', len(lo))
print('Sagnorð:', len(so))
print('Atviksorð:', len(ao))
print('Persónufornöfn:', len(pfn))
print('Afturb. fornöfn:', len(afturbfn))
print('Önnur fornöfn:', len(fn))
print('Töluorð:',len(to))
print('Greinir:', len(gr))
