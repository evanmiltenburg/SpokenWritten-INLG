import json
import csv
import glob
from string import punctuation
from numpy import mean
from nltk import ngrams

# Installed
import spacy
import pyphen


################################################################################
# Global variables.

punctuation_set = set(punctuation)
nlp = spacy.load('nl', disable=['ner'])
dic = pyphen.Pyphen(lang='nl')


################################################################################
# Load data

with open('./Written/written_annotations.json') as f:
    written_data = json.load(f)


with open('./Spoken/annotations_final.json') as f:
    spoken_data = json.load(f)

# Remove empty descriptions.
spoken_data = [entry for entry in spoken_data if len(entry['normalized_description']) > 0 and entry['normalized_description'].strip() != '-']

with open('./Written/Participants/PID.json') as f:
    written_pid = json.load(f)


with open('./Spoken/Participants/PID.json') as f:
    spoken_pid = json.load(f)


# Add relevant fields.
for entry in spoken_data:
    entry['modality'] = 'spoken'
    entry['description'] = entry['normalized_description']
    participant = entry['participant']
    image = entry['image']
    entry['PID'] = spoken_pid[participant]["per_sentence"][image]


for entry in written_data:
    entry['modality'] = 'written'
    participant = str(entry['participant'])
    image = entry['image']
    entry['PID'] = written_pid[participant]["per_sentence"][image]


with open('./semantic_categories.json') as f:
    semantic_categories = json.load(f)


################################################################################
# Preprocess data

def run_pipeline(entries):
    for entry in entries:
        entry['doc'] = nlp(entry['description'])
        entry['tokens'] = [tok.orth_ for tok in entry['doc'] if not tok.orth_ in punctuation_set]
        entry['length'] = len(entry['tokens'])
    return None


################################################################################
# Helper functions

def syllable_count(word):
    "Compute the number of syllables for a word."
    with_hyphens = dic.inserted(word)
    syllables = with_hyphens.split('-')
    return len(syllables)


################################################################################
# Define metrics

def attributive_count(entry):
    "Count attributive adjectives in a document."
    attributive_counter = 0
    for tok in entry['doc']:
        if all([tok.pos_ == 'ADJ',
                tok.dep_ == 'amod',
                tok.head.pos_ in {'NOUN', 'PROPN'}]):
            attributive_counter += 1
    entry['attributives'] = attributive_counter
    return None


def num_adverbs(entry):
    "Count the number of adverbs."
    adverbs = [tok for tok in entry['doc'] if tok.pos_ == 'ADV']
    entry['adverbs'] = len(adverbs)
    return None


def num_prepositions(entry):
    "Count the number of prepositions."
    prepositions = [tok for tok in entry['doc'] if tok.pos_ == 'ADP']
    entry['prepositions'] = len(prepositions)
    return None


def num_syllables(entry):
    "Count the mean number of syllables"
    lengths = [syllable_count(word) for word in entry['tokens']]
    entry['syllables'] = mean(lengths)
    return None


def num_chars(entry):
    "Count the mean number of characters"
    lengths = [len(word) for word in entry['tokens']]
    entry['chars'] = mean(lengths)
    if len(lengths)==0:
        print(entry)
    return None


def count_words(entry, index):
    "Count the words in each category in the index."
    for category in index:
        count = 0
        words = index[category]['words']
        bigrams = index[category]['bigrams']
        # Count individual words
        for word in entry['tokens']:
            if word.lower() in words:
                count += 1
        # Count bigrams (if there are any)
        if bigrams:
            for w1,w2 in ngrams(entry['tokens'], 2):
                if (w1.lower(),w2.lower()) in bigrams:
                    count += 1
        entry[category] = count
    return None


################################################################################
# Process data

for subset in [spoken_data, written_data]:
    run_pipeline(subset)
    for entry in subset:
        attributive_count(entry)
        num_adverbs(entry)
        num_prepositions(entry)
        num_syllables(entry)
        num_chars(entry)
        count_words(entry, semantic_categories)


################################################################################
# Write to file

# Ensure that images and participants are interpreted as categorical.
# By appending 'ppt-' and 'img-', the fields are no longer interpretable as numerical data.
for subset in [spoken_data, written_data]:
    for entry in subset:
        entry['participant'] = 'ppt-' + str(entry['participant'])
        entry['image'] = 'img-' + str(entry['image'])

header = ['participant', 'image', 'modality', 'PID', 'length', 'attributives',
          'adverbs', 'syllables', 'chars', 'consciousness_of_projection',
          'self_reference_words', 'negations', 'pseudo_quantifiers',
          'positive_allness', 'prepositions']

with open('./Prepared/overall_stats.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for subset in [spoken_data, written_data]:
        for entry in subset:
            row = [entry[item] for item in header]
            writer.writerow(row)
