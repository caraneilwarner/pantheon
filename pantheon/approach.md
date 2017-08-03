# The Challenge

From [/r/proceduralgeneration](https://www.reddit.com/r/proceduralgeneration/comments/6lt82x/monthly_challenge_20_july_2017_procedural/):

**Procedural Pantheon/Mythology**

_Monthly Challenge 20 - July, 2017_

> Inspired by several submissions on the suggestion thread relating to genealogy, culture, history etc. Your task for the month is to create a program that generates a procedural pantheon, or similar. This could be on the same lines as the greeks, where certain gods have domain over certain aspects of the physical or astral world. It could be like the christian religion, where you have 12 disciples who are known for certain things, or it could be like the Australian dreamtime, where spirits of the natural world shape the landscape in certain ways, or trick people in certain ways. Or it could be like Japanese mythology.

> You are free to generate graphical representations (think of the many forms of Hindu mythology!), or textual ones. For example, your submission could make.[Boris] God of Fire, Walnuts and Cleaning the Letterbox. Boris is the father of [Tracey], Goddess of grass clippings.


# Strategy

Write two python classes, `God` and `Pantheon`, whose functions are metaphors for **sexual reproduction** in order to generate gods with internally-coherent domains and Pantheons with diverse but related deities. 

### The Metaphor

Words are **chromosomes**.
A list of 46 words is a **genome** and a list of 23 words is a **gamete** (aka egg or sperm).
A multi-dimensional list of tokens (words) is a **gene pool**.

### The Models

A `God` has:

`chromosomes`: Either `XX` or `XY`.
`gender`: Either `male`, `female`, or `non_binary`.
`genome`: A list of up to 46 words.
`generation`: An integer set during a `pantheon.spawn()`.
`divinity`: Either `god`, `demi_god`, or `human`. 
`name`: A string pulled at random from a list of `female_names`, `male_names`, or `nb_names`.
`epithet`: A string that combines a title (God, Godess, Divine Being, ...) with between 1 and 4 domains. 

A `Pantheon` has:

`gods`: A dictionary mapping names to `God`s. 

### Reproduction

To generate a `God` call `God(egg_donor, sperm_donor)` with arguments that are either both strings or both `God`s. If the arguments are strings, **asexual reproduction** will occur; if the arguments are `God`s, **sexual reproduction** will occur.
