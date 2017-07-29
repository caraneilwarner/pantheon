"""Defines a class Pantheon."""
import random
from gods import *

class Pantheon:
    def __init__(self, mother_of_creation, father_of_creation):
        self.mother_of_creation = mother_of_creation
        self.father_of_creation = father_of_creation
        self.gods = [mother_of_creation, father_of_creation]


    def spawn(self, generations):
        egg_donors = [god for god in self.gods if god.chromosomes == 'XX']
        sperm_donors = [god for god in self.gods if god.chromosomes == 'XY']

        for i in range(generations):
            print("\nGENERATION %d\n" % (i+1))
            gen_xx = []
            gen_xy = []

            for egg_donor in egg_donors:
                sperm_donor = random.choice(sperm_donors)
                offspring = God(egg_donor, sperm_donor)
                send_birth_announcement(egg_donor, sperm_donor, offspring)
                offspring.parents = [egg_donor, sperm_donor]

                # divine offspring joins pantheon
                if offspring.divinity > 1:
                    self.gods.append(offspring)
                    if offspring.chromosomes == 'XX':
                        gen_xx.append(offspring)
                    else:
                        gen_xy.append(offspring)

            # mature offspring join the breeding pool
            egg_donors += gen_xx
            sperm_donors += gen_xy

            # elder gods leave the breeding pool
            egg_donors = [ed for ed in egg_donors if ed.generation > (i-3)]
            sperm_donors = [sd for sd in sperm_donors if sd.generation > (i-4)]

def send_birth_announcement(parent_a, parent_b, offspring=None):
    #print("%s (gen %d) - %s" % (offspring.name, offspring.generation, offspring.epithet))
    print("%s - %s" % (offspring.name, offspring.epithet))
