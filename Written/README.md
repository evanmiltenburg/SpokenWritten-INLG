# Written descriptions

This folder contains written Dutch image descriptions, provided by 48 native speakers of Dutch.
The images used for this experiment are the same as those in the Dutch Image Description and Eye-tracking Corpus (DIDEC).
This means that we can use this data to compare spoken and written modalities.

## Data collection

This data was collected at XXXXX University on Tuesday 27 November, 2018.
Participants 48 students of XXXXX University (X female), with a mean age of Y.

## Files

This folder contains the following files:

* Conversion script:
    - `./convert_data.py` takes the original files and generates more easily digestible files.

* Original files:
    - `./list_mapping.csv` contains a mapping from questions to image identifiers.
    - `./writtendescriptions.csv` contains the raw Qualtrics output.

* Reorganized data:
    - `./duration_stats.json` contains the duration of each experiment, with some summary statistics.
    - `./written_annotations.json` contains the written descriptions, with the image IDs and automatically generated participant IDs.
    - `./written_plain.txt` contains all the descriptions as plain text.
    - `./Participants/*.txt` contains the descriptions, with one file per participant.

In generating readable participant IDs, I made sure to start at the number 1000,
so that they are clearly distinguishable from the participant IDs from the Spoken
experiment.

## Requirements

To execute the Python file, we used the following versions:

* Python 3.6.6
* NumPy 1.15.1

Other versions may work, but remain untested.
