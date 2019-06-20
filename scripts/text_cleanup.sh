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
Machine-specific paths must be un-commented before use
'''

# HH Path:
in_dir="./testing/corpora/icepahc-v0.9/psd_orig"
out_dir="./testing/corpora/icepahc-v0.9/psd"


# Create output directory

if [ ! -d $out_dir ];
  then
    echo "Creating '$out_dir' directory..."
    mkdir $out_dir
  else
    echo "Directory '$out_dir' already exists. Using that."
fi

for file in $in_dir/*; do
  echo "Copying file: ${file##*/}"
  cp $file ${file//_orig}
done

for file in $out_dir/*; do
  echo "Working on file: ${file##*/}"
  perl ./rm-nonstruct.prl -i $file
  #Delete (CODE...)
  sed -i "" 's/(CODE[ {}*<>a-zA-Z0-9a-zA-ZþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\.$_:-?/]*)//g' $file
  #Delete (ID...))
  sed -i "" 's/(ID [0-9]*\.[A-Z]*[0-9]*\.[A-Z]*-[A-Z]*[,\.][0-9]*[,\.][0-9]*))//g' $file
  #Delete lines which include (ID
  #sed -i '/(ID/d' $file
  #Delete every instance of '( '
  sed -i "" 's/( //g' $file
  #Delete lines which only include (. ?-?)), (. .-.)) or (" "-")) at the beginning of line
  sed -i "" 's/^([\."] [\.?"]-[\.?"]))$//g' $file
  #Delete empty lines
  sed -i "" '/^$/d' $file
  sed -i "" '/^  $/d' $file
  #Include token and lemma for ',' and '.'
  sed -i "" 's/(, -)/(, ,-,)/g' $file
  sed -i "" 's/(\. -)/(\. \.-\.)/g' $file
  #Delete extra (, ---)
  sed -i "" '/(, ---)/d' $file
  #Correct (. ---)
  sed -i "" 's/(\. ---)/(\. \.-\.)/g' $file
  #Replace <dash/> with proper notation
  sed -i "" 's/(, <dash\/>)/(, ,-,)/g' $file
  #Delete empty spaces before (QTP
  sed -i "" 's/^  (QTP/(QTP/g' $file
  #Delete empty spaces before (IP-MAT
  sed -i "" 's/^  (IP-MAT/(IP-MAT/g' $file
  #Delete empty spaces before (FRAG
  sed -i "" 's/^  (FRAG/(FRAG/g' $file
  #Delete last character in file (uneven parentheses) NOTE only needed on some machines!!!
  # sed -i "" '$ s/.$//' $file
done

  # sed -i "" 's/) //g' #./testing/corpora/icepahc-v0.9/psd_orig/*.psd
