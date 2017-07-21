import process
from process import *
import random

#TODO: add stopwords
#TODO: consider increasing size of genome
#TODO: randomize sources?

"""
texts = get_texts()
noun_tokens = get_tokens_by_pos(texts, ['NNS'])
verb_tokens = get_tokens_by_pos(texts, ['VBG'])
"""

# Good starters: mother flowers and honey, father hunt and fire

class Pantheon:
    def __init__(self, mother_of_creation, father_of_creation):
        self.mother_of_creation = mother_of_creation
        self.father_of_creation = father_of_creation
        self.gods = [self.mother_of_creation, self.father_of_creation]


    def spawn(self):
        she_gods = [god for god in self.gods if god.gender == "F"]
        he_gods = [god for god in self.gods if god.gender == "M"]

        mother = random.choice(she_gods)
        father = random.choice(he_gods)
        offspring = self.copulate(mother, father)
        print("The union of the %s and the %s produced the %s" % (mom.epitaph, dad.epitaph, offspring.epitaph))


    def copulate(self, mother, father):
        egg_word = mother.gamete()
        sperm_word = father.gamete()
        offspring = God(egg_word, sperm_word)
        return offspring


class God:
    def __init__(self, egg_word, sperm_word):
        self.genes_from_mom = self.get_egg(egg_word)
        self.genes_from_dad = self.get_sperm(sperm_word)
        self.genome = self.genes_from_mom + self.genes_from_dad        
        self.name = self.get_name()
        self.epitaph = self.get_epitaph()


    def get_egg(self, egg_word):
        phenotype = get_overlapping_matches(egg_word, noun_tokens)
        genotype = [gene for gene,expression in phenotype]
        return genotype


    def get_sperm(self, sperm_word):
        chromosome = random.choice(['X','Y'])

        if chromosome == 'X':
            phenotype = get_overlapping_matches(sperm_word, noun_tokens)
            self.gender = 'F'
        elif chromosome == 'Y':
            phenotype = get_overlapping_matches(sperm_word, verb_tokens)
            self.gender = 'M'

        genotype = [gene for gene, expression in phenotype]
        return genotype


    def get_name(self):
        #TODO: wire up name generator
        if self.gender == 'F':
            return 'Jane Doe'
        else:
            return 'John Doe'


    def get_epitaph(self):
        #TODO: introduce more templates
        title = 'Godess' if self.gender == 'F' else 'God'
        domains = random.sample(self.genome, 3)
        return '%s of %s, %s, and %s' % (title, *domains)


    def reset_epitaph(self):
        self.epitaph = get_epitaph()


    def gamete(self):
        #TODO: introduce chance of infertility
        return random.choice(self.genome)
