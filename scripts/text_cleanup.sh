#!/bin/bash

'''
12.06.19
Hinrik Hafsteinsson
Þórunn Arnardóttir

Script for cleaning IcePaHC corpus files (.psd)
 - Removes sentence ID tags
 - Removes nonstructural label nodes
 - Removes last parantheses from each file (main imbalance issue)
 - Adds token/lemma for missing punctuations (, and .)
 - Replaces (, <dash/>) with (, ,-,)
 - Joins nouns with corresponding determiners (stýrimanns$ $ins -> stýrimannsins)
Machine-specific paths must be specified before use
'''

# paths

in_dir="./testing/corpora/icepahc-v0.9/psd_orig"
out_dir="./testing/corpora/icepahc-v0.9/psd"
# in_dir="./testing/corpora/icecorpus/psd_orig"
# out_dir="./testing/corpora/icecorpus/psd"

# Create output directory if needed

if [ ! -d $out_dir ];
  then
    echo "Creating '$out_dir' directory..."
    mkdir $out_dir
  else
    echo "Directory '$out_dir' already exists. Using that."
fi

# Copy files to new directory

for file in $in_dir/*; do
  echo "Copying file: ${file##*/}"
  cp $file ${file//_orig}
done

# Corpus errors fixed before processing
./scripts/fix_corpus_errors.sh

# Each file run through commands

for file in $out_dir/*; do
  echo "Working on file: ${file##*/}"
  # Delete (CODE...)
  sed -i "" 's/(CODE[ {}*<>a-zA-Z0-9a-zA-ZþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\.$_:-?/]*)//g' $file
  # Delete (ID...))
  sed -i "" 's/(ID [0-9]*\.[A-Z]*[0-9]*\.[A-Z]*-[A-Z]*[,\.][0-9]*[,\.][0-9]*))//g' $file
  # Delete lines which include (ID
  # sed -i '/(ID/d' $file

  # Delete every instance of '( '
  sed -i "" 's/^( //g' $file
  # Delete lines which only include (. ?-?)), (. .-.)) or (" "-")) at the beginning of line
  sed -i "" 's/^([\."] [\.?"]-[\.?"]))$//g' $file
  # TODO: insert command that joins punctuation to sentence instead
  #       of deleting line
    # python3 scripts/join_puncts.py $file
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
  # Replace <dash/> with proper notation
  # sed -i "" 's/(, <dash\/>)/(, ,-,)/g' $file # NOTE maybe obsolete, check
  # Remove -TTT (possibly temporary)
  sed -i "" 's/-TTT//g' $file
  # Delete empty spaces before (QTP
  sed -i "" 's/^  (QTP/(QTP/g' $file
  # Delete empty spaces before (IP-MAT
  sed -i "" 's/^  (IP-MAT/(IP-MAT/g' $file
  # Delete empty spaces before (FRAG
  sed -i "" 's/^  (FRAG/(FRAG/g' $file
  # Delete empty spaces before (CP-QUE
  sed -i "" 's/^  (CP-QUE/(CP-QUE/g' $file
  # Delete empty spaces before (IP-IMP-SPE
  sed -i "" 's/^  (IP-IMP-SPE/(IP-IMP-SPE/g' $file
  # Delete empty spaces before (LATIN
  sed -i "" 's/^  (LATIN/(LATIN/g' $file
  # Delete empty spaces before (CP-EXL-SPE
  sed -i "" 's/^  (CP-EXL-SPE/(CP-EXL-SPE/g' $file
  # Correct one instance of uneven parentheses
  sed -i "" 's/^(VAG sofandi\.-sofa))/(VAG sofandi\.-sofa)/g' $file
  # Join nouns and corresponding determiners
  python3 scripts/join_NPs.py $file
  # Delete empty lines
  sed -i "" '/^$/d' $file
  sed -i "" '/^  $/d' $file
  # TEMP ---------
  # python3 scripts/join_sents.py $file
  # Delete last character in file (uneven parentheses) NOTE only needed on some machines!!!
  sed -i "" '$ s/.$//' $file
done

  # sed -i "" 's/) //g' #./testing/corpora/icepahc-v0.9/psd_orig/*.psd
