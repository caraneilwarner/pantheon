"""Run many searches to compare outcomes for different strategies."""

import process
from process import *

"""
docs = get_docs()
tokens = get_tokens(docs)
noun_tokens = get_tokens_of_type(docs, 'NOUN')
verb_tokens = get_tokens_of_type(docs, 'VERB')
"""

def print_titles():
    """Print titles of all available source texts."""
    titles = get_titles()
    print("\n%d SOURCE TEXTS AVAILABLE:\n" % (len(titles)))
    for title in titles:
        print(title)
    print("")


def test_large_limit(word, tokens, limit):
    print("\nEFFECT OF LARGE LIMIT: " + word)
    for title in get_titles():
        matches = get_matches(word, tokens[title], limit)
        print('\n' + title + ': ' + ', '.join(matches))


def test_vary_offset(word, tokens):
    print("\nEFFECT OF VARYING OFFSET: " + word)

    titles = get_titles()
    run = 1

    #for offset in [0,10,25,50,75,100,150,200,400,1000]:
    for offset in [0,10,25,50,75,100]:
        print("\n%s Run %d: offset=%d\n" % (word.upper(), run, offset))
        for title in get_titles():
            matches = get_matches(word, tokens[title], 10, offset)
            print(title + ": " + ', '.join(matches))
        run += 1

    return


def test_vary_sources():
    return


def test_vary_token_type():
    return
