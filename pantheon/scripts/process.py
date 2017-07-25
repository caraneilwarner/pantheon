import nltk
import os
import spacy

from collections import Counter
from numpy import dot
from numpy.linalg import norm

nlp = spacy.load('en_core_web_md')


def get_texts():
    """Read in source texts from corpora directory."""
    corpora = [filename for filename in os.listdir('../src/corpora/')]
    texts = {}
    for filename in corpora:
        texts[filename] = open('../src/corpora/' + filename).read()

    return texts


def get_tokens(texts, filters):
    """Retrieve tokens that match the given part of speech (pos) filters. See:
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    """
    tokens = {}
    for title,text in texts.items():
        words = nltk.word_tokenize(text)
        unique_words = list(set([w.lower() for w in words]))
        tokens[title] = [w for w,p in nltk.pos_tag(unique_words) if p in filters]

    return tokens


def get_matches(word, tokens, limit=10, offset=0):
    """Input <tokens> is a dictionary mapping filenames to tokens. Search each
    file's tokens for the words that are most closely related to <word>. Take
    all those matches, aggregate them, and return them in one big list.
    """
    results = []
    for source, source_tokens in tokens.items():
        results += closest(source_tokens, word_vec(word), limit, offset)

    return results


def get_common_matches(word, tokens, limit=10, offset=0):
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
