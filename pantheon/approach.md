# The Challenge

From [/r/proceduralgeneration](https://www.reddit.com/r/proceduralgeneration/comments/6lt82x/monthly_challenge_20_july_2017_procedural/):

**Procedural Pantheon/Mythology**

_Monthly Challenge 20 - July, 2017_

> Inspired by several submissions on the suggestion thread relating to genealogy, culture, history etc. Your task for the month is to create a program that generates a procedural pantheon, or similar. This could be on the same lines as the greeks, where certain gods have domain over certain aspects of the physical or astral world. It could be like the christian religion, where you have 12 disciples who are known for certain things, or it could be like the Australian dreamtime, where spirits of the natural world shape the landscape in certain ways, or trick people in certain ways. Or it could be like Japanese mythology.

> You are free to generate graphical representations (think of the many forms of Hindu mythology!), or textual ones. For example, your submission could make.[Boris] God of Fire, Walnuts and Cleaning the Letterbox. Boris is the father of [Tracey], Goddess of grass clippings.


# Strategy

Let's call words **chromosomes**. That makes a list of 46 words a **genome** and a list of 23 words a **gamete** (egg or sperm). A tokenized text is a **genetic individual** and a list of tokenized texts is a **gene pool**. 

The generator in `gods.py` takes an `egg_word` and uses spaCy's word relatedness vectors to pull 23 related words from a series of tokenized texts (the gene pool). It then does the same with a `sperm_word`. It combines the two 23-word lists to produce the unique genome for a new god.

### Sex and Gender

Because this model is based on sexual reproduction each god is assigned XX or XY *chromosomes*. This is done at random. The god's gender is then chosen according to the following probabilities: 90% of the time the god will be cisgendered, 5% of the time the god will be transgendered, and 5% of the time the god will identify as neither male nor female. The model prefers labels like `egg_donor` and `sperm_donor` over `mother` and `father` because it does not assume reproducing pairs will be cis-gendered. An egg could come from a father, and a sperm from a mother.

Gender manifests in things like the god's epithet. A female god (whether XX or XY) will be called Godess or Demi-Godess; a male god (XX or XY) will be called God or Demi-God; and a non-binary god will be called Divine Being or Semi-Divine Being.

### Mutation

Concrete nouns produce the best results when searching for related words. Here "best" means "most obviously related to the intended meaning of the input." Gerunds (verbs made nouns) produce some funky results. 80% of the time this model pulls related words from a list of nouns; the remaining 20% of the time it pulls related words from a list of gerunds. You might call these the *regular gene pool* and the *mutant gene pool*.

### Dilution

Over time deity is diluted. When a pantheon spawns, its early generations will mostly be Gods, Godesses, and Divine Beings. Subsequent generations skew toward Demi-Gods, Demi-Godesses, and Semi-Divine Beings. 7+ generations in you will start seeing a few humans pop up.

None of this is random. Probabilities are defined in `gods.py`. The union of two gods will likely produce a god but might produce a demi-god. The union of god and demi-god will likely produce a demi-god but might produce a god. The union of demi-god and demi-god will likely produce a demi-god but might produce a human. And so on.
