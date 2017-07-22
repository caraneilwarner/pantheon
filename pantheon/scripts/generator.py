import process
from process import *
import random
from numpy.random import choice as npchoice

"""
texts = get_texts()
noun_tokens = get_tokens_by_pos(texts, ['NNS'])
verb_tokens = get_tokens_by_pos(texts, ['VBG'])
"""

MALE = 'M'
FEMALE = 'F'
NON_BINARY = 'NB'

"""
IDEAS

# Good starters: mother flowers and honey, father hunt and fire

#TODO: wire up name generator
#TODO: add stopwords
#TODO: explore making some genes dominant, some recessive
#TODO: introduce probability for trans/non-gender
#TODO: introduce chance of twins, tripplets, infertility, refusal to mate
#TODO: introduce more titles. Ex Lord, Lady...
#TODO: introduce more epithet templates, allow 2-4 words instead of just 3
#TODO: introduce generations to spawn()

"""

class Pantheon:
    def __init__(self, mother_of_creation, father_of_creation):
        self.mother_of_creation = mother_of_creation
        self.father_of_creation = father_of_creation
        self.gods = [self.mother_of_creation, self.father_of_creation]


    def spawn(self, generations):
        egg_donors = [god for god in self.gods if god.chromosomes == 'XX']
        sperm_donors = [god for god in self.gods if god.chromosomes == 'XY']

        for _ in range(generations):
            egg_donor = random.choice(egg_donors)
            sperm_donor = random.choice(sperm_donors)
            offspring = self.fertilize(egg_donor, sperm_donor)
            send_birth_announcement(egg_donor, sperm_donor, offspring)

            # Baby is all grown up...
            if offspring.chromosomes == 'XX':
                egg_donors.append(offspring)
            else:
                sperm_donors.append(offspring)


    def fertilize(self, egg_donor, sperm_donor):
        egg_word = egg_donor.get_gamete()
        sperm_word = sperm_donor.get_gamete()
        offspring = God(egg_word, sperm_word)
        return offspring


class God:
    def __init__(self, egg_word, sperm_word):
        self.chromosomes = random.choice(['XX','XY'])
        self.gender = get_gender(self.chromosomes)

        # 'mother' and 'father' in the sense of egg/sperm donor, not the roles 'mommy' and 'daddy'
        self.genes_from_mother = self.get_egg(egg_word)
        self.genes_from_father = self.get_sperm(sperm_word)
        self.genome = self.genes_from_mother + self.genes_from_father

        self.name = self.get_name()
        self.epithet = self.get_epithet()


    def get_egg(self, egg_word):
        phenotype = get_overlapping_matches(egg_word, noun_tokens, 23)
        genotype = [gene for gene,expression in phenotype]
        return genotype


    def get_sperm(self, sperm_word):
        if self.chromosomes == "XX":
            phenotype = get_overlapping_matches(sperm_word, noun_tokens, 23)
        elif self.chromosomes == "XY":
            phenotype = get_overlapping_matches(sperm_word, verb_tokens, 23)
        genotype = [gene for gene, expression in phenotype]
        return genotype


    def get_name(self):
        if self.gender == FEMALE:
            return 'Lorem'
        elif self.gender == MALE:
            return 'Ipsum'
        else:
            return 'Dolor'       


    def get_epithet(self):
        if self.gender == FEMALE:
            title = 'Godess'
        elif self.gender == MALE:
            title = 'God'
        else:
            title = 'God'

        domains = random.sample(self.genome, 3)
        return '%s of %s, %s, and %s' % (title, *domains)


    def change_epithet(self):
        self.epithet = self.get_epithet()
        print(self.epithet)

    def get_gamete(self):
        return random.choice(self.genome)


"""Miscellaneous helpers"""

def send_birth_announcement(parent_a, parent_b, offspring=None):
    print("The union of the %s and the %s produced the %s." % (parent_a.epithet, parent_b.epithet, offspring.epithet))


def get_gender(chromosomes):
    genders = [MALE, FEMALE, NON_BINARY]
    probabilities = [0.8, 0.1, 0.1] if chromosomes == 'XY' else [0.1, 0.8, 0.1]
    return npchoice(genders, 1, p=probabilities)[0]

