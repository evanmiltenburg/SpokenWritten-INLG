# Spoken descriptions

This folder contains spoken descriptions from the Dutch Image Description and Eye-tracking Corpus (DIDEC).
We used this file to create a plaintext corpus of all the normalized descriptions.

## Requirements

We used Python 3.6.6 to load the JSON file and generate the plaintext version of the corpus.
Other versions remain untested, but will probably also work.

## Files

* `./annotations_final.json` are the original descriptions.
* `./make_plain.py` is the conversion script.
* `./spoken_plain.txt` is the plaintext corpus.
