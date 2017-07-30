"""Defines a class God."""
import names
import tokens
import random
from numpy.random import choice as npchoice
from process import *

# Initialize
if not len(tokens.primary_tokens) > 0 : tokens.set_tokens_lists()
if not len(names.female_names) > 0 : names.set_name_lists()

# Divinity constants
god = 3
demi_god = 2
human = 1
divinities = [god, demi_god, human]
p_divinity = {
    # sum : god | demi_god | human
    6: [0.7, 0.3, 0.0],
    5: [0.5, 0.5, 0.0],
    4: [0.0, 0.8, 0.2],
    3: [0.0, 0.3, 0.7],
    2: [0.0, 0.0, 1.0]
}

# Gender constants
male = 'M'
female = 'F'
non_binary = 'NB'
genders = [male, female, non_binary]
p_gender = {
     # chromosomes : male | female | non_binary
    'XX': [0.07, 0.90, 0.03],
    'XY': [0.90, 0.07, 0.03]
}


class God:

    def __init__(self, egg_donor, sperm_donor):
        self.set_chromosomes()
        self.set_gender()
        self.set_inherited_traits(egg_donor, sperm_donor)
        self.set_name()
        self.set_epithet()


    def set_inherited_traits(self, egg_donor, sperm_donor):
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

        self.genome = list(set(egg + sperm)) # Eliminate duplicates
        self.generation = 1
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
        self.parents = [egg_donor, sperm_donor]
        self.generation = max(egg_donor.generation, sperm_donor.generation) + 1
        sum_ = egg_donor.divinity + sperm_donor.divinity
        self.divinity = npchoice(divinities, 1, p=p_divinity[sum_])[0]


    def set_chromosomes(self):
        """This model uses the XY sex-determination system. Sex != gender.
        Assign either XX or XY randomly with a 50/50 chance of each.
        """
        self.chromosomes = random.choice(['XX','XY'])


    def set_gender(self):
        """This model recognizes that sex chromosomes don't always line up with
        gender. Assign M, F, or NB according to the probabilities in p_gender.
        """
        if not self.chromosomes: self.set_chromosomes
        self.gender = npchoice(genders, 1, p=p_gender[self.chromosomes])[0]


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
                name = male_names.pop()

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

        domains = random.sample(self.genome, num_domains)

        # Put it all together
        self.epithet = template % (title, *domains)


    def generate_gamete(self, egg_or_sperm_word):
        """Extract 23 chromosomes (words) from a gene pool by searching one of
        the gene pools (tokens lists) for words closely related to a "seed".
        The seed is egg_or_sperm_word 80 percent of the time so that offspring
        will feel "related" to their parents. 20 percent of the time the seed is
        a random word. This is intended to simulate genetic mutation.
        """
        p_mutation = [0.8, 0.2]
        mutant_word = random.choice(random_list())
        seed = str(npchoice([egg_or_sperm_word, mutant_word], 1, p=p_mutation)[0])

        p_gene_pool = [0.8, 0.2]
        # Can't apply npchoice directly to tokens lists b/c they're multi-dimensional
        use_secondary_pool = (npchoice([0,1], 1, p=p_gene_pool)[0] == 1)
        pool = tokens.secondary_tokens if use_secondary_pool else tokens.primary_tokens

        return get_overlapping_matches(seed, tokens.primary_tokens, 23)

        return get_overlapping_matches(seed, pool, 23)


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


def random_list():
    """Tokens lists are multi-dimensional; they're lists of lists. Return one of
    the lists from the primary_tokens list.
    """
    i = random.choice(range(len(tokens.primary_tokens)))
    return tokens.primary_tokens[i]
