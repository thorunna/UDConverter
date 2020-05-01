#!/bin/bash

# 12.06.19
# Hinrik Hafsteinsson
# Þórunn Arnardóttir
#
# Script for cleaning IcePaHC corpus files (.psd)
#  - Removes sentence ID tags
#  - Removes nonstructural label nodes
#  - Removes last parantheses from each file (main imbalance issue)
#  - Adds token/lemma for missing punctuations (, and .)
#  - Replaces (, <dash/>) with (, ,-,)
#  - Joins nouns with corresponding determiners (stýrimanns$ $ins -> stýrimannsins)
# Machine-specific paths must be specified before use

# paths

# in_dir="./testing/corpora/icepahc-v0.9/psd_orig"
# out_dir="./testing/corpora/icepahc-v0.9/psd"
# in_dir="../testing/corpora/icecorpus/psd_orig"
# out_dir="../testing/corpora/icecorpus/psd"

in_path=$1
file=$2


# cp $in_path $file

# Corpus errors fixed before processing
# ./fix_corpus_errors.sh

echo "Pre-processing ${file##*/}"

# Include token and lemma for ',' and '.'
sed -i "" 's/(, -)/(, ,-,)/g' $file
sed -i "" 's/(\. -)/(\. \.-\.)/g' $file
# Delete extra (, ---)
sed -i "" 's/(, ---)//g' $file
# Delete extra (, ---)
sed -i "" 's/(, -----)//g' $file
# Correct (. ---)
sed -i "" 's/(\. ---)/(\. \.-\.)/g' $file
# Delete extra (- -)
sed -i "" 's/(- -)//g' $file
# Delete extra (- ---)
sed -i "" 's/^(IP-MAT (- ---)/(IP-MAT/g' $file
# Delete extra (NUM-N -)
sed -i "" 's/(NUM-N -)//g' $file    # ath. --- í frumtextanum
# Remove -TTT (possibly temporary)
sed -i "" 's/-TTT//g' $file
# Correct one instance of uneven parentheses
sed -i "" 's/^(VAG sofandi\.-sofa))/(VAG sofandi\.-sofa)/g' $file
# Join various split words in psd files
python3 ./join_psd.py $file


echo "Done."
