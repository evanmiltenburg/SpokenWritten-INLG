from collections import namedtuple

Entry = namedtuple('Entry', ['number', 'token', 'lemma', 'segmentation', 'pos',
                             'confidence', 'named_entity_type', 'base_phrase_chunk',
                             'head', 'dep_relation'])


def process_line(line):
    "Turn each line into a named tuple with all the token properties."
    row = line.strip().split('\t')
    return Entry(*row)
    

def sentence_generator(filename):
    "Generate sentences for a particular file."
    with open(filename) as f:
        sentence = []
        for line in f:
            if line == '\n':
                yield sentence
                sentence = []
            else:
                entry = process_line(line)
                sentence.append(entry)


def prepare_data(filename):
    return [[(token.token, token.pos, token.lemma) for token in sentence]
            for sentence in sentence_generator(filename)]
