import json
import os
from collections import defaultdict

def ensure_folder(folder_name):
    "Make sure a folder exists. If not, create it."
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def participant_index(items):
    "Build an index: identifier -> descriptions"
    description_index = defaultdict(list)
    image_index = defaultdict(list)
    for item in items:
        participant = item['participant']
        image = item['image']
        # Skip empty descriptions.
        if len(item['normalized_description']) == 0:
            continue
        description = item['normalized_description'] + '\n'
        description_index[participant].append(description)
        image_index[participant].append(image)
    return description_index, image_index


def create_participant_files(folder='Participants/'):
    "Create files with descriptions per participant."
    description_index, image_index = participant_index(data)
    ensure_folder(folder)
    for participant, lines in description_index.items():
        with open(folder + str(participant) + '.txt', 'w') as f:
            f.writelines(lines)
    with open(folder + 'participant_lines_image_mapping.json', 'w')  as f:
        json.dump(image_index, f, indent=2)


# Open the original annotations, and select the normalized descriptions.
with open('./annotations_final.json') as f:
    data = json.load(f)

# Write out as plain text.
with open('spoken_plain.txt', 'w') as f:
    lines = [entry['normalized_description'] + '\n' for entry in data]
    f.writelines(lines)

create_participant_files('Participants/Plain/')
