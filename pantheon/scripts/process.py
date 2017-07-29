import nltk
import os
import spacy

from collections import Counter
from numpy import dot
from numpy.linalg import norm

nlp = spacy.load('en_core_web_md')


def get_matches(word, tokens_lists, limit=10, offset=0):
    """Input <tokens> is a dictionary mapping filenames to tokens. Search each
    file's tokens for the words that are most closely related to <word>. Take
    all those matches, aggregate them, and return them in one big list.
    """
    results = []
    for tokens in tokens_lists:
        results += closest(tokens, word_vec(word), limit, offset)

    return results


def get_overlapping_matches(word, tokens, limit=10, offset=0):
    """Input <tokens> is a dictionary mapping filenames to tokens. Use method
    get_matches() to grab all the matching words from all the files. Produce a
    Counter and use it to sort words by the number of texts that share them.
    Return the most widely shared words. (Not same as most frequently used.)
    """
    results = get_matches(word, tokens, limit, offset)
    counter = Counter(results)

    return [word for word,count in counter.most_common(limit)]


def word_vec(word):
    """Return spaCy's vector for <word>."""
    return nlp.vocab[word].vector


def cosine(vec1, vec2):
    """Compare vectors. Borrowed from A. Parish."""
    if norm(vec1) > 0 and norm(vec2) > 0:
        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    else:
        return 0.0


def closest(tokens, search_vec, limit=10, offset=0):
    """Return the <limit> words from <tokens> whose vectors most closely
    resemble the search_vec. Skip the first <offset> results.
    """
    return sorted(tokens,
                  key=lambda x: cosine(search_vec, word_vec(x)),
                  reverse=True)[offset:offset+limit]
