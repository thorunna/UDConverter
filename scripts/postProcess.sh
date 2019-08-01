#!/usr/bin/env bash

'''
01.08.19
Hinrik Hafsteinsson
Þórunn Arnardóttir

Script for postprocessing IcePaHC Conll-U files
Machine-specific paths must be specified before use
'''


dir="./testing/CoNLLU_output"

for file in $dir/*; do
  echo "Working on file: ${file##*/}"
  python3 scripts/join_verb_clitics.py $file
done
