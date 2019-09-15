"""
Script to convert Qualtrics results to more manageable format.

Author: XXXXX
Usage: python convert_data.py

Required files:
- writtendescriptions.csv
- list_mapping.csv

Generates:
- written_annotations.json
- written_plain.txt
- duration_stats.json
"""

# Stdlib
import csv
import json
import os
from collections import defaultdict

# Installe:
from numpy import std, median, mean

def get_entries(filename):
    "Load the entries from the file, representing each participant as a dictionary."
    with open(filename, encoding='cp1252') as f:
        reader = csv.reader(f)
        keys = next(reader)
        # Skip next two lines.
        for i in range(2):
            next(reader)
        entries = [dict(zip(keys,row)) for row in reader]
    return entries


def duration_statistics(entries):
    "Generate duration statistics."
    durations = [int(entry['Duration (in seconds)']) for entry in entries]
    return dict(mean_seconds=mean(durations),
                median_seconds=median(durations),
                std_seconds=std(durations),
                min_seconds=min(durations),
                max_seconds=max(durations),
                mean_minutes=mean(durations)/60,
                median_minutes=median(durations)/60,
                std_minutes=std(durations)/60,
                min_minutes=min(durations)/60,
                max_minutes=max(durations)/60,
                durations=durations)


def load_mappings(filename):
    "Load mappings from file."
    with open(filename) as f:
        reader = csv.reader(f,delimiter=';')
        header = next(reader)
        question_to_image = dict()
        image_to_partition = dict()
        for image, question, partition in reader:
            question_to_image[question] = image
            image_to_partition[image] = partition
    return question_to_image, image_to_partition


def write_json(object,filename):
    "Write JSON to a file."
    with open(filename,'w') as f:
        json.dump(object, f, indent=4)


def get_items(entries):
    "Get basic items (to be enriched later)."
    items = []
    for i, entry in enumerate(entries, start=1000):
        response_id = entry['ResponseId']
        for key, value in entry.items():
            if key == 'Q319':
                # Practice question: Ignore.
                continue
            elif key.startswith('Q') and value:
                item = dict(participant=i,
                            description=value.strip(),
                            question=key,
                            response_id=response_id)
                items.append(item)
    return items


def enrich_items(items, question2img, img2part):
    "Enrich items with information about their partition and the image."
    for item in items:
        question = item['question']
        image = question2img[question]
        partition = img2part[image]
        item['image'] = image
        item['partition'] = partition
    # This function modifies the list in place, so it returns nothing.
    return None


def participant_index(items):
    "Build an index: identifier -> descriptions"
    description_index = defaultdict(list)
    image_index = defaultdict(list)
    for item in items:
        participant = item['participant']
        description = item['description'] + '\n'
        image = item['image']
        description_index[participant].append(description)
        image_index[participant].append(image)
    return description_index, image_index


def extract_lines(items):
    "Extract lines to create a plaintext corpus."
    lines = [item['description'] + '\n' for item in items]
    return lines


def ensure_folder(folder_name):
    "Make sure a folder exists. If not, create it."
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def create_participant_files(items, folder='Participants/Plain/'):
    "Create files with descriptions per participant."
    description_index, image_index = participant_index(items)
    ensure_folder(folder)
    for participant, lines in description_index.items():
        with open(folder + str(participant) + '.txt', 'w') as f:
            f.writelines(lines)
    with open(folder + 'participant_lines_image_mapping.json', 'w')  as f:
        json.dump(image_index, f, indent=2)


if __name__ == "__main__":
    entries = get_entries('./writtendescriptions.csv')
    items = get_items(entries)

    question_to_image, image_to_partition = load_mappings('./list_mapping.csv')
    enrich_items(items, question_to_image, image_to_partition)
    write_json(items, 'written_annotations.json')
    
    lines = extract_lines(items)
    with open('written_plain.txt','w') as f:
        f.writelines(lines)
    
    create_participant_files(items)
    
    duration_stats = duration_statistics(entries)
    write_json(duration_stats,"duration_stats.json")
