import random
from make_deity import *

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

            for egg_donor in egg_donors:
                sperm_donor = random.choice(sperm_donors)
                offspring = God(egg_donor, sperm_donor)
                send_birth_announcement(egg_donor, sperm_donor, offspring)
                offspring.parents = [egg_donor, sperm_donor]

                # divine offspring joins pantheon
                if offspring.divinity > 1:
                    self.gods.append(offspring)
                    if offspring.chromosomes == 'XX':
                        egg_donors.append(offspring)
                    else:
                        sperm_donors.append(offspring)

def send_birth_announcement(parent_a, parent_b, offspring=None):
    print("%s - %s" % (offspring.name, offspring.epithet))
