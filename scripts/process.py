import nltk
import os
import spacy

from collections import Counter
from numpy import dot
from numpy.linalg import norm

nlp = spacy.load('en_core_web_md')


def get_matches(word, tokens, limit, offset=0):
    """Return words from <tokens> that are most closely related to <word>."""
    return closest(tokens, word_vec(word), limit, offset)


def word_vec(word):
    """Return spaCy's vector for <word>."""
    return nlp.vocab[word].vector


def cosine(vec1, vec2):
    """Compare vectors. Borrowed from A. Parish."""
    if norm(vec1) > 0 and norm(vec2) > 0:
        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    else:
        return 0.0


def closest(tokens, search_vec, limit, offset=0):
    """Return the <limit> words from <tokens> whose vectors most closely
    resemble the search_vec. Skip the first <offset> results.
    """
    return sorted(tokens,
                  key=lambda x: cosine(search_vec, word_vec(x)),
                  reverse=True)[offset:offset+limit]
