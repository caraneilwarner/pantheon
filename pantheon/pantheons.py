"""Defines a class Pantheon."""
import random
from pantheon.gods import *
from math import ceil

class Pantheon:
    def __init__(self, mother_of_creation, father_of_creation):
        if not mother_of_creation.chromosomes == "XX":
            print('Invalid mother of creation. Must have XX chromosomes.')
        if not father_of_creation.chromosomes == "XY":
            print('Invalid father of creation. Must have XY chromosomes.')
        self.gods = {}
        self.add_god(mother_of_creation)
        self.add_god(father_of_creation)


    def add_god(self, god):
        """Add a god to this Pantheon's gods dictionary."""
        self.gods[god.name] = god


    def get_god(self, name_of_god):
        """Retrieve a god from this Pantheon's gods dictionary."""
        try:
            return self.gods[name_of_god]
        except:
            print('No deity named %s in this pantheon.' % name_of_god)


    def spawn(self, generations):
        """Grow this Pantheon by multiplying Gods."""
        egg_donors = [god for god in self.gods.values() if god.chromosomes == 'XX']
        sperm_donors = [god for god in self.gods.values() if god.chromosomes == 'XY']

        for i in range(generations):
            print("\nGENERATION %d\n" % (i+1))
            gen_xx = []
            gen_xy = []

            for egg_donor in egg_donors:
                sperm_donor = random.choice(sperm_donors)
                brood = self.breed(egg_donor, sperm_donor)

                for child in brood:
                    if child.divinity > human:
                        # divine offspring join the Pantheon
                        self.add_god(child)
                    if child.chromosomes == 'XX':
                        gen_xx.append(child)
                    else:
                        gen_xy.append(child)

            # elder gods leave the breeding pool
            egg_donors = [ed for ed in egg_donors if ed.generation > (i-2)]
            sperm_donors = [sd for sd in sperm_donors if sd.generation > (i-3)]

            # mature offspring join the breeding pool
            egg_donors += gen_xx
            sperm_donors += gen_xy


    def breed(self, egg_donor, sperm_donor):
        """Get it on."""
        offspring = []
        try:
            num_children = npchoice([1,2], 1, p=[0.8, 0.2])[0] # 20% chance of twins
            for _ in range(num_children):
                child = God(egg_donor, sperm_donor)
                offspring.append(child)
                send_birth_announcement(egg_donor, sperm_donor, child)
        except ValueError:
            print("Breeding error occurred. Likely the generator ran out of names.")

        return offspring


def send_birth_announcement(parent_a, parent_b, child):
    """Convenience method for presentations."""
    print("%s - %s" % (child.name, child.epithet))
