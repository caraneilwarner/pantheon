"""Exposes the json data files in the /data/tokens directory. These files contain
raw tokens lists pulled from texts in the /data/corpora directory.
"""
import json
import nltk
import os
import random

primary_tokens = [] # tokens that represent "normal" genes
secondary_tokens = [] # tokens that represent "mutant" genes


abs_path = os.path.abspath(os.path.dirname(__file__))
corpora_dir = os.path.join(abs_path, 'data/corpora/')
tokens_dir = os.path.join(abs_path, 'data/tokens/')

def sequence_genes():
    """An alias."""
    tokenize_corpora()


def filter_genes(pool, filters):
    """An alias."""
    save_tokens_to_dir(pool, filters)


def define_gene_pool(pool, individuals):
    """An alias."""
    make_tokens_dir(pool, individuals)


def select_gene_pool(dir_):
    """An alias."""
    set_token_lists(dir_)

def list_gene_pools():
    """An alias."""
    get_tokens_dirs()

def tokenize_texts():
    """Generate a json file for each txt file in the /data/corpora directory."""
    text_files = [fname for fname in os.listdir(corpora_dir) \
        if fname.split('.')[1] == 'txt']

    for text_fname in text_files:
        json_fname = text_fname.split('.')[0] + '.json'
        if os.path.isfile(corpora_dir + json_fname):
            continue # already tokenized

        print("Tokenizing " + text_fname)
        text = open(corpora_dir + text_fname).read()
        words = nltk.word_tokenize(text)
        with open(corpora_dir + json_fname, 'w') as outjson:
            json.dump(words, outjson)


def list_tokenized_texts():
    """Retrieve the filenames of all tokenized text files in /data/corpora.
    Useful when you want to hand-pick <sources> for make_tokens_dir().
    """
    return [f for f in os.listdir(corpora_dir) if f.split('.')[1] == 'json']


def make_tokens_dir(dir_, sources):
    """Create a new directory named <dir_>. Create a new file within it called
    sources.json. The input <sources> is a list of names of tokenized texts.
    Write <sources> into sources.json.
    """
    os.mkdir(tokens_dir + dir_)
    for source in sources:
        if not os.path.isfile(corpora_dir + source):
            print('Invalid source: ' + source)
            return

    with open(tokens_dir + dir_ + '/sources.json', 'w') as outjson:
        json.dump(sources, outjson)


def make_tokens_list(dir_, filters):
    """Find sources.json in <dir_>. It contains a list of tokenized texts. For
    each tokenized text listed in sources.json, read its tokens, filter them,
    and add them to an aggregated list. Write the aggregated list to disk using
    a filename based on the <filters> given.
    """
    with open(tokens_dir + dir_ + '/sources.json', 'r') as injson:
        data = json.load(injson)
        sources = [corpora_dir + fname for fname in data]

    with open('data/skipwords.txt', 'r') as f:
        skipwords = [line.rstrip() for line in f]

    tokens_list = []
    for fname in sources:
        print("Incorporating tokens from " + fname)
        with open(fname, 'r') as injson:
            data = json.load(injson)
            words = [w.lower() for w in data if not w == '']
            filtered = [w for w,p in nltk.pos_tag(words) if p in filters]
            sanitized = [w for w in filtered if not w in skipwords]
            tokens_list += sanitized

    tokens_list = list(set(tokens_list)) # unique
    target = tokens_dir + dir_ + '/' + '-'.join(filters) + '.json'
    with open(target, 'w') as outjson:
        json.dump(tokens_list, outjson)


def set_tokens_lists(dir_=None):
    if not dir_: dir_ = random.choice(os.listdir(tokens_dir))
    print("Loading tokens from: " + dir_)

    p_fname = tokens_dir + dir_ + '/NNS.json'
    s_fname = tokens_dir + dir_ + '/VBG.json'

    global primary_tokens
    primary_tokens = json.load(open(p_fname, 'r'))

    global secondary_tokens
    secondary_tokens = json.load(open(s_fname, 'r'))

def get_tokens_dirs():
    tokens_dirs = [ dirname for dirname in os.listdir(tokens_dir) ]

    return tokens_dirs
