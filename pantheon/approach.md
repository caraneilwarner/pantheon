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

**sexual reproduction**: _the process that occurs when a new `God` is initialized with two parent `Gods`._

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

### Spawning Gods

Given two `Gods`, one `XX` **egg donor** and one `XY` **sperm donor**...

1. Select a random word from the `God.genome` of the **egg donor**.
1. Use spaCy to pull 23 related words from the **gene pool**. This is the **egg**.
1. Select a random word from the `God.genome` of the **sperm donor**.
1. Use spaCy to pull 23 related words from the **gene pool**. This is the **sperm**.
1. Add the **egg** and **sperm** together. This list of 46 words is the *genome* for the new `God`.

_Note: because a `God's` genome is populated with words **related** to seeds from its parents' genomes, a `God` feels **genetically related** to its parents. But, because the seeds are selected at **random** from the parents' genomes, there's room for **genetic drift**._

### Spawning Pantheons

Given two `Gods`, one `XX` **egg donor** and one `XY` **sperm donor**, and a number of generations **N**...

1. Declare a list of **egg donors** and a list of **sperm donors**.
1. Iterate **N** times, once for each generation...
1. At the start of each generation breed the **egg donors**.
1. At the end of each generation, add mature offspring to the breeding pool.
1. At the end of each generation, remove elder `Gods` from the breeding pool.
