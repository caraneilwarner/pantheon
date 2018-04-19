"""Exposes the json data files in the /data/names directory."""
import json
import os
import random

female_names = []
male_names = []
nb_names = []

abs_path = os.path.abspath(os.path.dirname(__file__))
names_dir = os.path.join(abs_path, 'data/names/')


def set_name_lists(ethnicity=None):
    """Set three globally available lists of names."""
    if not ethnicity: ethnicity = random.choice(get_ethnicities())
    print("Loading names from: " + ethnicity)
    filename = names_dir + ethnicity + '.json'

    try:
        with open(filename, 'r') as injson:
            data = json.load(injson)
    except:
        return 'Unable to read from file: ' + filename
    else:
        names = [ tuple(name.split(',')) for name in data ]
        random.shuffle(names)

        global female_names
        female_names = [name for name,gender,*desc in names if gender == 'girl']

        global male_names
        male_names = [name for name,gender,*desc in names if gender == 'boy']

        global nb_names
        nb_names = [name for name,gender,*desc in names if gender == 'boygirl']


def get_ethnicities():
    """Retrieve a list of the ethnicities for which name data was scraped.
    Exclude the file extension for human friendliness.
    """
    ethnicities = [ fname.split('.')[0] for fname in os.listdir(names_dir) ]

    return ethnicities


def print_ethnicities():
    """Print a list of the ethnicities for which name data was scraped."""
    print('\nETHNICITIES REPRESENTED: \n')
    print('\n'.join(get_ethnicities()))
    print("\n")
