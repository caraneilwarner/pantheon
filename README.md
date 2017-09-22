# The Challenge

From [/r/proceduralgeneration](https://www.reddit.com/r/proceduralgeneration/comments/6lt82x/monthly_challenge_20_july_2017_procedural/):

**Procedural Pantheon/Mythology**

_Monthly Challenge 20 - July, 2017_

> Inspired by several submissions on the suggestion thread relating to genealogy, culture, history etc. Your task for the month is to create a program that generates a procedural pantheon, or similar. This could be on the same lines as the greeks, where certain gods have domain over certain aspects of the physical or astral world. It could be like the christian religion, where you have 12 disciples who are known for certain things, or it could be like the Australian dreamtime, where spirits of the natural world shape the landscape in certain ways, or trick people in certain ways. Or it could be like Japanese mythology.

> You are free to generate graphical representations (think of the many forms of Hindu mythology!), or textual ones. For example, your submission could make.[Boris] God of Fire, Walnuts and Cleaning the Letterbox. Boris is the father of [Tracey], Goddess of grass clippings.


# Strategy

Construct two models called `God` and `Pantheon` whose functions are metaphors for sexual reproduction. The goal: generate `Gods` with internally-coherent domains and `Pantheons` with diverse but related deities. 

**Metaphors**

* **chromosomes**: _words._
* **genome**: _a list of 46 words._
* **gamete**: _a list of 23 words._
* **gene pool**: _a multi-dimensional list of tokens drawn from different texts._
* **sexual reproduction**: _the process that occurs when a new `God` is initialized with two parent `Gods`._
* **asexual reproduction**: _the process that occurs when a new `God` is initialized using just strings._


# Models

**Attributes of a `God`**

* **chromosomes**: Either `XX` or `XY`.
* **gender**: Either `male`, `female`, or `non_binary`.
* **genome**: A list of up to 46 words.
* **generation**: An integer set during a `pantheon.spawn()`.
* **divinity**: Either `god`, `demi_god`, or `human`.
* **name**: A string pulled at random from a list of `female_names`, `male_names`, or `nb_names`.
* **epithet**: A string that combines a title (God, Goddess, Divine Being, ...) with between 1 and 4 domains. A domain is a word randomly selected from the `God's` genome. Example: Goddess of hunting and war.
* **parents**: The `Gods` whose egg and sperm combined to create this `God`.

**Attributes of a `Pantheon`**

* **gods**: A dictionary mapping names to `Gods`.

# Reproduction

### Spawning [Gods](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py)

Given two `Gods`, one `XX` **egg donor** and one `XY` **sperm donor**...

1. Select a random word from the `God.genome` of the **egg donor**.
1. Use spaCy to pull 23 related words from the **gene pool**. This is the **egg**.
1. Select a random word from the `God.genome` of the **sperm donor**.
1. Use spaCy to pull 23 related words from the **gene pool**. This is the **sperm**.
1. Add the **egg** and **sperm** together. This list of 46 words is the *genome* for the new `God`.

_Note: because a `God's` genome is populated with words **related** to seeds from its parents' genomes, a `God` feels **genetically related** to its parents. But, because the seeds are selected at **random** from the parents' genomes, there's room for **genetic drift**._

### Spawning [Pantheons](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/pantheons.py)

Given two `Gods`, one `XX` **egg donor** and one `XY` **sperm donor**, and a number of generations **N**...

1. Declare a list of **egg donors** and a list of **sperm donors**.
1. Iterate **N** times, once for each generation...
1. At the start of each generation breed the **egg donors**.
1. At the end of each generation, add mature offspring to the breeding pool.
1. At the end of each generation, remove elder `Gods` from the breeding pool.


# Code Imitating Nature

The model blends randomness and probability to echo the beauty of natural reproduction.

**[Gender](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L26-L35)**: There's a 7% chance a `God` will be transgendered and a 3% chance a `God` will be non-gendered or gender-queer. For this reason the model refers to 'egg donors' and 'sperm donors' not 'mothers' and 'fathers'. Two male `Gods` can procreate, as can two female `Gods`, or a gender-queer `God` and another `God`, as long as one parent is `XX` and one is `XY`.

**[Sex](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L85)**: When a new `God` spawns its sex chromosomes are chosen at random. It's possible for several `Gods` in a row to be `XX` or `XY`. An unexpected consequence of this: some Pantheons grow much faster than others. The rate of growth is determined by the number of `XX` gods born in each generation.

**[Mutation](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L170-L172)**: The related words that spaCy finds in a list of plural nouns often feel "more related" than the ones it finds in a list of gerunds. This is just something I observed. 80% of the time this model pulls gametes from `primary_tokens`, which is a list of NNS; the other 20% of the time it pulls gametes from `secondary_tokens`, which is a list of VBG. The result is some children look a lot like their parents and some look very different; there's variety in how far the apple falls from the tree.

**[Power Level](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L26-L35)**: Many traditions describe old gods as more powerful than young gods. When two `Gods` procreate there's a 30% chance their offspring will be a 'demi-god' rather than a full blown god. That chance jumps to 50% when a 'god' and 'demi-god' procreate, and when two 'demi-gods' procreate there's a 25% chance their offspring will be a lowly human.

**[Twinning](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/pantheons.py#L48)**: 20% of the time coupling produces twins; the other 80% of the time it produces a single child. 

**[Epithets](https://github.com/carawarner/procgen/blob/master/pantheon/scripts/gods.py#L143)**: Most gods (55%) represent 3 domains: God of X, Y, and Z. Slightly fewer gods (35%) represent two domains: God of X and Y. The remaining gods represent 1  or 4 domains.




# Future Enhancements

- [ ] Tweak gene logic to differentiate between **identical** and **fraternal** twins and tripplets.
- [ ] Add logic to de-duplicate domains represented within a `Panetheon`.
- [ ] Find a visualization library to chart the relationships between `Gods` in a `Pantheon`. A family tree.
- [ ] Add chance of tripplets.
- [ ] Add chance of infertility.
- [ ] Add a `God.siblings` attribute.
