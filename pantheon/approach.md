# The Challenge

From [/r/proceduralgeneration](https://www.reddit.com/r/proceduralgeneration/comments/6lt82x/monthly_challenge_20_july_2017_procedural/):

**Procedural Pantheon/Mythology**

_Monthly Challenge 20 - July, 2017_

> Inspired by several submissions on the suggestion thread relating to genealogy, culture, history etc. Your task for the month is to create a program that generates a procedural pantheon, or similar. This could be on the same lines as the greeks, where certain gods have domain over certain aspects of the physical or astral world. It could be like the christian religion, where you have 12 disciples who are known for certain things, or it could be like the Australian dreamtime, where spirits of the natural world shape the landscape in certain ways, or trick people in certain ways. Or it could be like Japanese mythology.

> You are free to generate graphical representations (think of the many forms of Hindu mythology!), or textual ones. For example, your submission could make.[Boris] God of Fire, Walnuts and Cleaning the Letterbox. Boris is the father of [Tracey], Goddess of grass clippings.


# Strategy

Write two python classes, `God` and `Pantheon`, whose functions are metaphors for sexual reproduction. The goal is to generate `Gods` with internally-coherent domains and `Pantheons` with diverse but related deities.


**chromosomes**: _words._

**genome**: _a list of 46 words._

**gamete**: _a list of 23 words._

**gene pool**: _a multi-dimensional list of tokens drawn from different texts._

**sexual reproduction**: _the process that occurs when a new `God` is initialized with two parent `God`s._

**asexual reproduction**: _the process that occurs when a new `God` is initialized using just strings._

# Models

**Attributes of a `God`:**

```
chromosomes: Either `XX` or `XY`.

gender: Either `male`, `female`, or `non_binary`.

genome: A list of up to 46 words.

generation: An integer set during a `pantheon.spawn()`.

divinity: Either `god`, `demi_god`, or `human`.

name: A string pulled at random from a list of `female_names`, `male_names`, or `nb_names`.

epithet: A string that combines a title (God, Goddess, Divine Being, ...) with between 1 and 4 domains. A domain is a word 

randomly selected from the `God's` genome. Example: Goddess of hunting and war.

parents: The `Gods` whose egg and sperm combined to create this `God`.
```

**Attributes of a `Pantheon`:**

```
gods: A dictionary mapping names to `Gods`.
```

# Reproduction

**Producing a `God`**

Call `God(egg_donor, sperm_donor)` with arguments that are either both strings or both `Gods`. If the arguments are strings [asexual reproduction](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L56) will occur; if the arguments are `Gods` [sexual reproduction](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L68) will occur. The processes are similar. Here's sexual reproduction.

```
1. Grab a **random** word from the `God.genome` of the `egg_donor` and `sperm_donor`. 

2. Use those random words to [generate two gametes](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L159). Each gamete is a list of 23 **related** words. The model uses spaCy to find related words in a gene pool.

3. Combine the gametes. This is the new `God's` genome.
```

Because a `God's` genome is populated with words **related** to its parents' genomes, a `God` feels **genetically related** to its parents. But, because the seed is selected at **random** from the parents' genomes, there's room for **genetic drift**.


**Producing a `Pantheon`**

Call `Pantheon(mother_of_creation, father_of_creation)` with arguments that are `Gods`. One `God` must have `XX` chromosomes and one must have `XY` chromosomes, but their genders do not matter; the model just needs an egg donor and a sperm donor.

With an initial egg donor and sperm donor, you can [spawn more `Gods`](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/pantheons.py#L15) by calling `Pantheon.spawn(num_generations)`. At the beginning of each generation most of the fertile `egg_donors` will breed; at the end their offspring will be added to the breeding pool and older `Gods` will be removed from the breeding pool (see [here](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/pantheons.py#L37-L43)).
