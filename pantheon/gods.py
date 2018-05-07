"""Defines a class God."""
import pantheon.names as names
import pantheon.tokens as tokens
import random
from numpy.random import choice as npchoice
from pantheon.process import *

# Divinity constants
god = 3
demi_god = 2
human = 1
divinities = [god, demi_god, human]
p_divinity = {
    # sum : [p_god, p_demi, p_human]
    6: [0.7, 0.3, 0.0], # god+god     = usually god, sometimes demi
    5: [0.5, 0.5, 0.0], # god+demi    = either god or demi
    4: [0.0, 0.8, 0.2], # d+d OR g+h  = usually demi, sometimes human
    3: [0.0, 0.3, 0.7], # demi+human  = usually human, sometimes demi
    2: [0.0, 0.0, 1.0]  # human+human = always human
}

# Gender constants
male = 'M'
female = 'F'
non_binary = 'NB'
genders = [male, female, non_binary]
valid_chromosomes = ['XX','XY']
p_gender = {
     # chromosomes : [p_male, p_female, p_nb]
    'XX': [0.09, 0.85, 0.06], # usually female, sometimes trans, occasionally NB
    'XY': [0.85, 0.09, 0.06]  # usually male, sometimes trans, occasionally NB
}


class God:

    def __init__(self, egg_donor, sperm_donor, chromosomes=None, gender=None):
        self.set_chromosomes(chromosomes)
        self.set_gender(gender)
        self.set_inherited_traits(egg_donor, sperm_donor)
        self.set_name()
        self.set_epithet()


    def set_chromosomes(self, chromosomes=None):
        """This model uses the XY sex-determination system. Sex != gender.
        Assign either XX or XY randomly with a 50/50 chance of each, unless
        <chromosomes> are passed as an argument.
        """
        if chromosomes and chromosomes in valid_chromosomes:
            self.chromosomes = chromosomes
        else:
            self.chromosomes = random.choice(['XX','XY'])


    def set_gender(self, gender=None):
        """This model recognizes that sex chromosomes don't always line up with
        gender. Assign M, F, or NB according to the probabilities in p_gender.
        """
        if gender and gender in genders:
            self.gender = gender
        else:
            if not self.chromosomes: self.set_chromosomes()
            self.gender = npchoice(genders, 1, p=p_gender[self.chromosomes])[0]


    def set_inherited_traits(self, egg_donor, sperm_donor):
        """Accept either strings or Gods as inputs."""
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

        self.genome = list(set(egg + sperm)) # Eliminate duplicates
        self.generation = 1
        self.divinity = god # If it springs out of the ether, it's a god


    def reproduce_sexually(self, egg_donor, sperm_donor):
        """Produce two gametes, an egg and a sperm, from input Gods. Combine
        them to produce a genome a la sexual reproduction. Assign divinity
        according to probabilities in p_divinity. The more divine the parents,
        the more divine their offspring.
        """
        egg_word = random.choice(egg_donor.genome)
        egg = self.generate_gamete(egg_word)
        sperm_word = random.choice(sperm_donor.genome)
        sperm = self.generate_gamete(sperm_word)

        self.genome = list(set(egg + sperm)) # Eliminate duplicates
        self.parents = [egg_donor.name, sperm_donor.name]
        self.generation = max(egg_donor.generation, sperm_donor.generation) + 1
        sum_ = egg_donor.divinity + sperm_donor.divinity
        self.divinity = int(npchoice(divinities, 1, p=p_divinity[sum_])[0])


    def set_name(self):
        """Pick a random name from the lists loaded with the model. For Gods that
        identify as neither M nor F, the model attempts to retrieve an androgynous
        name. Note: not all of the scraped name lists contain androgynous names.
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
                name = names.male_names.pop()

        self.name = name


    def set_epithet(self):
        """Divine an appropriate epithet for this God. (See what I did there?)"""
        if self.divinity == human:
            obsession = random.choice(self.genome)
            if self.gender == female:
                self.epithet = 'an ordinary woman'
            elif self.gender == male:
                self.epithet = 'an ordinary man'
            else:
                self.epithet = 'an ordinary human being who loves ' + obsession
            return # Return early. The rest of the function deals with gods.

        if self.gender == female:
            title = 'Goddess'
        elif self.gender == male:
            title = 'God'
        else:
            title = 'Divine Being'
        if self.divinity == demi_god:
            title = 'Semi-' + title if self.gender == non_binary else 'Demi-' + title

        num_domains = npchoice([1,2,3,4], 1, p=[0.05, 0.35, 0.55, 0.05])[0]

        if num_domains == 1:
            template = '%s of %s'
        if num_domains == 2:
            template = '%s of %s and %s'
        elif num_domains == 3:
            template = '%s of %s, %s, and %s' # Oxford comma, the most divine punctuation.
        elif num_domains == 4:
            template = '%s of %s, %s, %s, and %s'

        self.domains = random.sample(self.genome, num_domains)

        # Put it all together
        self.epithet = template % (title, *self.domains)


    def generate_gamete(self, egg_or_sperm_word):
        """Extract 23 'chromosomes' aka words from 'gene pool' aka list of tokens
        by searching the list of tokens for words that are related to the given
        egg_or_sperm_word.
        """
        p_rate_of_mutation = [0.9, 0.1]
        should_use_mutant_pool = (npchoice([0,1], 1, p=p_rate_of_mutation)[0] == 1)
        if should_use_mutant_pool:
            pool = tokens.secondary_tokens
        else:
            pool = tokens.primary_tokens

        return get_matches(egg_or_sperm_word, pool, 23)


    def print_parents(self):
        """Print parents' names and epithets."""
        if self.gender == female:
            title = 'Daughter'
        elif self.gender == male:
            title = 'Son'
        else:
            title = 'Child'

        p1 = self.parents[0]
        p2 = self.parents[1]

        template = '%s of %s, the %s, and %s, the %s.'

        print(template % (title, p1.name, p1.epithet, p2.name, p2.epithet))

if __name__ == "__main__":
    if not len(tokens.primary_tokens) > 0 : tokens.set_tokens_lists()
    if not len(names.female_names) > 0 : names.set_name_lists()
