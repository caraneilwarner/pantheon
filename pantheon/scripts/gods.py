"""Defines a class God."""
import names
import sources
import random
from numpy.random import choice as npchoice
from process import *

# Initialize
if not len(tokens.noun_tokens) > 0 : sources.set_token_lists()
if not len(names.female_names) > 0 : names.set_name_lists()

# Divinity constants
god = 3
demi_god = 2
human = 1
divinities = [god, demi_god, human]
p_divinity = {
    # sum : god | demi_god | human
    6: [0.75, 0.25, 0.0],
    5: [0.5, 0.5, 0.0],
    4: [0.0, 0.75, 0.25],
    3: [0.0, 0.25, 0.75],
    2: [0.0, 0.0, 1.0]
}

# Gender constants
male = 'M'
female = 'F'
non_binary = 'NB'
genders = [male, female, non_binary]
p_gender = {
     # chromosomes : male | female | non_binary
    'XX': [0.05, 0.94, 0.01],
    'XY': [0.94, 0.05, 0.01]
}


class God:

    def __init__(self, egg_donor, sperm_donor):
        self.set_chromosomes()
        self.set_gender()
        self.set_genome_and_divinity(egg_donor, sperm_donor)
        self.set_name()
        self.set_epithet()


    def set_genome_and_divinity(self, egg_donor, sperm_donor):
        """Accepts either strings or Gods as inputs."""
        if type(egg_donor) == str:
            self.reproduce_asexually(egg_donor, sperm_donor)
        else:
            self.reproduce_sexually(egg_donor, sperm_donor)


    def reproduce_asexually(self, egg_word, sperm_word):
        """Produce two gametes, an egg and a sperm, from the input strings.
        Combine them to produce a genome a la sexual reproduction.
        """
        egg = self.generate_gamete(egg_word)
        sperm = self.generate_gamete(sperm_word)

        self.genome = egg + sperm
        self.divinity = god


    def reproduce_sexually(self, egg_donor, sperm_donor):
        """Produce two gametes, an egg and a sperm, from input Gods. Combine
        them to produce a genome a la sexual reproduction. Select offspring's
        divinity based on parents' combined divinity.
        """
        egg_word = random.choice(egg_donor.genome)
        egg = self.generate_gamete(egg_word)
        sperm_word = random.choice(sperm_donor.genome)
        sperm = self.generate_gamete(sperm_word)

        self.genome = egg + sperm
        sum_ = egg_donor.divinity + sperm_donor.divinity
        self.divinity = npchoice(divinities, 1, p=p_divinity[sum_])[0]


    def set_chromosomes(self):
        """This model uses the XY sex-determination system. Sex != gender.
        Assign either XX or XY randomly with a 50/50 chance of each.
        """
        self.chromosomes = random.choice(['XX','XY'])


    def set_gender(self):
        """This model treats gender as independent from sex chromosomes.
        Assign M, F, or NB according to the probabilities in p_gender.
        """
        if not self.chromosomes: self.set_chromosomes
        self.gender = npchoice(genders, 1, p=p_gender[self.chromosomes])[0]


    def set_name(self):
        """Pick a random name from the lists loaded with the model. For Gods that
        identify as neither M nor F, the model attempts to retrieve an androgynous
        name. Not all of the lists contain androgynous names.
        """
        if not self.gender: self.set_gender()

        name = ''
        if self.gender == female:
            name = names.female_names.pop()
        elif self.gender == male:
            name = names.male_names.pop()
        else:
            try:
                name = names.nb_names.pop()
            except:
                # No androgynous names available
                name = male_names.pop()

        self.name = name


    def set_epithet(self):
        """Divine an appropriate epithet for this God. (See what I did there?)"""
        if self.divinity == human:
            if self.gender == female:
                self.epithet = 'an ordinary woman'
            elif self.gender == male:
                self.epithet = 'an ordinary man'
            else:
                self.epithet = 'an ordinary human being'
            return # Return early

        if self.gender == female:
            title = 'Godess'
        elif self.gender == male:
            title = 'God'
        else:
            title = 'Divine Being'
        if self.divinity == demi_god:
            title = 'Semi-' + title if self.gender == non_binary else 'Demi-' + title

        num_domains = npchoice([2,3,4], 1, p=[0.32, 0.64, 0.04])[0]

        if num_domains == 2:
            template = '%s of %s and %s'
        elif num_domains == 3:
            template = '%s of %s, %s, and %s' # Oxford comma, the most divine punctuation.
        elif num_domains == 4:
            template = '%s of %s, %s, %s, and %s'

        domains = random.sample(self.genome, num_domains)

        # Put it all together
        self.epithet = template % (title, *domains)


    def generate_gamete(self, egg_or_sperm_word):
        """Extract 23 chromosomes (words) from the gene pool by searching for
        words that closely match the <egg_or_sperm_word>. This model uses noun
        tokens for its gene pool 95 percent of the time and verb tokens 5 percent
        of the time. Verb tokens produce stranger results. We include them on
        rare occasions to simulate genetic mutation.
        """
        probabilities = [0.95,0.05]
        gene_pool = npchoice([noun_tokens, verb_tokens], 1, p=probabilities)[0]

        return get_common_matches(egg_or_sperm_word, gene_pool, 23)
