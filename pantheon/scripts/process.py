import spacy
import compute
from compute import nlp, closest, word_vec
from collections import Counter


def get_titles():
    """Produce a list of the titles of the source texts."""
    return [
        'babylonian-legends-of-creation',
        'caves-of-the-ozarks',
        'common-diseases-of-farm-animals',
        'custom-and-myth',
        'deities-of-the-maya',
        'divine-mythology-of-the-north',
        'elements-of-geology',
        'legends-of-the-gods',
        'myth-ritual-religion',
        'myths-legends-of-ancient-greece-rome',
        'myths-legends-of-china',
        'myths-of-babylonia-assyria',
        'poetry-of-architecture',
        'remarkable-criminals'
    ]


def get_docs():
    """Produce a dictionary mapping source text titles to docs.
    Docs are useful for text filtering.
    """
    titles = get_titles()
    docs = {}
    for title in titles:
        path = '../src/' + title + '.txt'
        docs[title] = nlp(open(path).read())
    
    return docs


def get_tokens(docs):
    """Produce a dictionary mapping source text titles to tokens.
    Tokens are useful for doing math on word vectors.
    """
    tokens = {}
    for title, doc in docs.items():
        tokens[title] = list(set([w.text.lower() for w in doc if w.is_alpha]))

    return tokens


def get_tokens_of_type(docs, type):
    """Same as get_tokens() but it allows you to filter on type of word.
    Valid types are NOUN, ADV, ADJ, VERB. Type is a string.
    """
    tokens = {}
    for title, doc in docs.items():
        tokens[title] = list(set([w.text.lower() for w in doc if w.pos_ == type]))

    return tokens


def get_matches(word, tokens, limit=10, offset=0):
    """Search each source in <tokens> for the words most closely relate
    to te given <word>. Return aggregated results.
    """
    if type(tokens) == list:
        return closest(tokens, word_vec(word), limit, offset)

    results = []
    for source, source_tokens in tokens.items():
        results += closest(source_tokens, word_vec(word), limit, offset)

    return results


def get_overlapping_matches(word, tokens, limit=10, offset=0):
    """Select 10 most frequently occurring matches from aggregated search
    results of get_matches().
    """
    results = get_matches(word, tokens, limit, offset)
    counter = Counter(results)
    return counter.most_common(limit)


def get_genetic_matches(words, tokens, limit=100):
    """WIP"""
    genomes = {word:get_overlapping_matches(word, tokens, limit) for word in words}
    genetic_matches = {}
    for word,genome in genomes:
        relations = get_relations(word, genomes)
        genetic_matches[word] = relations

def get_relations(word, genomes):
    """WIP"""
    return 










