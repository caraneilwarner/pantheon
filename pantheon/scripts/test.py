"""Run many searches to compare outcomes for different strategies."""

import process
from process import *
import random
"""
# TRY SPACY

docs = get_docs()
noun_tokens_spacy = get_tokens_of_type(docs, 'NOUN')
verb_tokens_spacy = get_tokens_of_type(docs, 'VERB')

# TRY NLTK

texts = get_texts()
noun_tokens_nltk = get_tokens_by_pos(texts, ['NN','NNS'])
verb_tokens_nltk = get_tokens_by_pos(texts, ['VBG'])
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

    for offset in [0,10,25,50,75,100]:
        print("\n%s Run %d: offset=%d\n" % (word.upper(), run, offset))
        for title in get_titles():
            matches = get_matches(word, tokens[title], 10, offset)
            print(title + ": " + ', '.join(matches))
        run += 1

    return


def test_vary_popularity(word, tokens):
    print("\nEFFECT OF FILTERING BY COUNT: " + word + "\n")
    
    counter = get_overlapping_matches(word, tokens, 1000)

    for popularity in [12,10,8,6,4,2,1]:
        popular_matches = get_popular_matches(word, counter, popularity)
        print(str(popularity) + ': ' + ', '.join(popular_matches))             


def test_vary_library(word, limit, libraries):
    print("\n" + word + ": ")
    for lib_name, lib in libraries.items(): 
        print(lib_name + ": "  + ", ".join([w for w,c in get_overlapping_matches(word, lib, limit)]))


def test_vary_input_pos(limit):
    """This test is unique in that it uses a hard-coded list of words. It doesn't accept words."""
    agri_words = ['farmer','farmers','farming','farms']
    print("\nWORDS DEALING WITH AGRICULTURE")
    for word in agri_words:
        test_vary_library(word, limit)

    war_words = ['soldier','soldiers','warring','war']
    print("\nWORDS DEALING WITH WAR")
    for word in war_words:
        test_vary_library(word, limit)

    elem_words = ['flame','flames','burning','fire']
    print("\nWORDS DEALING WITH ELEMENTAL FIRE")
    for word in elem_words:
        test_vary_library(word, limit)

    color_words = ['red','redish','crimson']
    print("\nWORDS MEANING RED")
    for word in color_words:
        test_vary_library(word, limit)



def test_vary_num_seeds(word, tokens, runs):
    print("**********************************************************************************")
    print("\nEFFECT OF VARYING NUMBER OF SEED TEXTS: " + word + "\n")

    for sample_size in [12, 3]:
        print("\nTESTING SAMPLE SIZE %d: %s\n" % (sample_size, word))
        
        for i in range(runs):

            # Randomly select a sample of seed texts
            titles = random.sample(tokens.keys(), sample_size)
            titles_str = ", ".join(titles[:3]) 
            titles_str = titles_str + "..." if len(titles) > 3 else titles_str         

            print("-------------------------------------------------------------------------")
            print("RUN %d SS %d: %s" % (i+1, sample_size, titles_str))
            print("-------------------------------------------------------------------------")
       
            sample = {title:tokens[title] for title in titles}
            overlapping_matches = [ word for word,count in get_overlapping_matches(word, sample, 50)]
            print(", ".join(overlapping_matches) + "\n")

