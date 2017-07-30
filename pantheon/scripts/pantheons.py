"""Defines a class Pantheon."""
import random
from gods import *
from math import ceil

class Pantheon:
    def __init__(self, mother_of_creation, father_of_creation):
        self.mother_of_creation = mother_of_creation
        self.father_of_creation = father_of_creation
        self.gods = {}
        self.gods[mother_of_creation.name] = mother_of_creation
        self.gods[father_of_creation.name] = father_of_creation


    def spawn(self, generations):
        egg_donors = [god for god in self.gods.values() if god.chromosomes == 'XX']
        sperm_donors = [god for god in self.gods.values() if god.chromosomes == 'XY']

        for i in range(generations):
            print("\nGENERATION %d\n" % (i+1))
            gen_xx = []
            gen_xy = []

            for egg_donor in random.sample(egg_donors, ceil((len(egg_donors) / 1.25))):
                sperm_donor = random.choice(sperm_donors)
                offspring = self.breed(egg_donor, sperm_donor)

                # divine offspring join pantheon
                for child in offspring:
                    if child.divinity > 1:
                        self.gods[child.name] = child
                        if child.chromosomes == 'XX':
                            gen_xx.append(child)
                        else:
                            gen_xy.append(child)

            # mature offspring join the breeding pool
            egg_donors += gen_xx
            sperm_donors += gen_xy

            # elder gods leave the breeding pool
            egg_donors = [ed for ed in egg_donors if ed.generation > (i-2)]
            sperm_donors = [sd for sd in sperm_donors if sd.generation > (i-3)]


    def breed(self, egg_donor, sperm_donor):
        offspring = []
        num_children = npchoice([1,2], 1, p=[0.8, 0.2])[0] # 20% chance of twins
        for _ in range(num_children):
            child = God(egg_donor, sperm_donor)
            offspring.append(child)
            send_birth_announcement(egg_donor, sperm_donor, child)

        return offspring


    def get_god(self, name):
        try:
            return self.gods[name]
        except:
            print('No deity named %s in this pantheon.' % name)


def send_birth_announcement(parent_a, parent_b, child):
    print("%s - %s" % (child.name, child.epithet))
