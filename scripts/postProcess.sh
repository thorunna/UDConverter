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
  # All lines with 'None' as token/lemma removed (errors from sentence parsing step)
  # Will need to be addressed at source
  sed -i "" '/None\tNone\tNone\tNone\t/d' $file
  # TODO:
  #   - Possibly remove $ from CoNLLU files in 'því$ $að' and 'þó$ $að'
  #     in e.g. 1260.jomsvikingar.nar-sag.conllu
  #   - ONE+Q-G changed to ADV (and possibly others) if joined ('einhversstaðar')
  # python3 taggers/test_conllu/otb_feats.py $file
  python3 scripts/join_conllu.py $file
  python3 scripts/rename_conllu.py $file
done

# Former todo, now done:
#   - ADD SCRIPT FOR renaming abbrevations to correct tokens/lemmas in:
#       1725.biskupasogur.nar-rel.psd ('Þ.b.') (skipped)
#       1985.sagan.nar-fic.conllu ('m.a.s.')
#       1985.margsaga.nar-fic.conllu ('amk')
#       1920.arin.rel-ser.conllu ('þ.e.a.s.')
#   - Join ON clitics (e.g. þar$ $s = þar sem) in same manner as verb clitics
#       Along with this:
#        - Þann$ $veg in 1525.erasmus.nar-sag.conllu
#   - ADD SCRIPT for temporarily removing all remaining '$' in CoNLLU (implemented but not as )
