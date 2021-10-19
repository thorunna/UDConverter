# Treebank format converter

A Python module for converting bracket parsed [PPCHE-format](https://www.ling.upenn.edu/hist-corpora/) treebanks to the [Universal Dependencies](https://universaldependencies.org/) framework. It is heavily based on existing [NLTK](https://www.nltk.org/) packages.

At the moment the module is specifically configured to convert treebanks in the [IcePaHC](https://linguist.is/icelandic_treebank/Icelandic_Parsed_Historical_Corpus_(IcePaHC)) format, which is based on PPCME.

## Setup

Install all requirements by running: 

`pip install -r requirements.txt`

## Usage

Scripts to run are in the `scripts` folder.

_In all examples below, the_ `--output` _flag is used to write to files in the_ `/CoNNLU/` _output folder. Otherwise prints to standard output._

> *Convert single file or directory of files:*

> `convert.py -N -i path/to/corpus/file.psd --output --post_process`

> `convert.py -N -i path/to/corpus/* --output --post_process`

_For further usage, input files must be placed in a folder within the_ `corpora` _folde:r_

> *Convert single tree in treebank using sentence ID (only prints to standard output):*

> `convert.py -C FOLDER_NAME -id SENTENCE_ID`

> *Convert single file in treebank*

> `convert.py -C FOLDER_NAME -f FILE_NAME --output --post_process`

_Additionally included is a script to only convert the IcePaHC corpus (_ `icepahc-v0.9`_), with pre- and post-processing:_

> `convert_icepahc.py`


## Acknowledgements
This converter is part of the UniTree project for IcePaHC, funded by The Strategic Research and Development Programme for Language Technology, grant no. 180020-5301. Thanks are due to Örvar Kárason, whose previous work was used as a basis for the conversion.
