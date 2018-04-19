==================
Pantheon Generator
==================

This library procedurally generates `Gods` with internally-coherent domains,
and `Pantheons` comprising generations of `Gods` that feel related to one
another. To achieve a good mix of cohesiveness and novelty, it employs the
metaphor of sexual reproduction:

* Words are **chromosomes**.
* A **genome** is a list of 46 words.
* A **gamete** (an egg or sperm) is a list of 23 words.
* A **gene pool** is a list of tokens drawn from different texts.
* **Asexual reproduction** occurs when a user generates a `God` from two strings.
* **Sexual reproduction** occurs when a user generates a `Pantheon` from two `Gods`.

==========
How To Use
==========

**Installation**

python3 -m venv env

pip install pantheon-generator

python -m spacy download en_core_web_md


**Interaction**

Generate individual `Gods` with seeder words:

`God("milk","honey")`

Generate `Pantheons` with two `God` objects:

`Pantheon(God, God)`

*Note*: `Gods` have chromosomes and you must have an XX and an XY to spawn a Pantheon.
That said, gender != chromosomes so it is possible to have two fathers of creation, or
two mothers of creation, or non-binary divine beings as the parents of your pantheon.


===============================================================================================
How `Gods <https://github.com/carawarner/pantheon/blob/master/pantheon/gods.py>`_ Spawn
===============================================================================================

Given two `Gods`, one `XX` **egg donor** and one `XY` **sperm donor**...

#. Select a random word from the `God.genome` of the **egg donor**.
#. Use spaCy to pull 23 related words from the **gene pool**. This is the **egg**.
#. Select a random word from the `God.genome` of the **sperm donor**.
#. Use spaCy to pull 23 related words from the **gene pool**. This is the **sperm**.
#. Add the **egg** and **sperm** together. This list of 46 words is the *genome* for the new `God`.

*Note:* because a `God's` genome is populated with words related to seeds from its
parents' genomes, a `God` feels genetically related to its parents. But, because the
seeds are selected at random from the parents' genomes, there's room for genetic drift.


=========================================================================================================
How `Pantheons <https://github.com/carawarner/pantheon/blob/master/pantheon/pantheons.py>`_ Spawn
=========================================================================================================

Given two `Gods`, one `XX` **egg donor** and one `XY` **sperm donor**, and a number
of generations **N**...

#. Declare a list of **egg donors** and a list of **sperm donors**.
#. Iterate **N** times, once for each generation...
#. At the start of each generation breed the **egg donors**.
#. At the end of each generation, add mature offspring to the breeding pool.
#. At the end of each generation, remove elder `Gods` from the breeding pool.


=============
More Features
=============

The model blends randomness and probability to echo the beauty of nature.

`Gender <https://github.com/carawarner/pantheon/blob/master/pantheon/gods.py#L26-L35>`_
***********************************************************************************************
There's a 7% chance a `God` will be transgendered and a 3% chance a `God` will be non-
gendered or gender-queer. For this reason the model refers to 'egg donors' and 'sperm
donors' not 'mothers' and 'fathers'. Two male `Gods` can procreate, as can two female
`Gods`, or a gender-queer `God` and another `God`, as long as one parent is `XX` and
one is `XY`.

`Sex <https://github.com/carawarner/pantheon/blob/master/pantheon/gods.py#L57>`_
****************************************************************************************
When a new `God` spawns, its sex chromosomes are chosen at random. It's possible for
several `Gods` in a row to be `XX` or `XY`. An unexpected consequence of this: some
Pantheons grow much faster than others. The rate of growth is determined by the number
of `XX` gods born in each generation.

`Mutation <https://github.com/carawarner/pantheon/blob/master/pantheon/gods.py#L170-L172>`_
***************************************************************************************************
The related words that spaCy finds in a list of plural nouns often feel "more related"
than the ones it finds in a list of gerunds. This is just something I observed. 80% of
the time this model pulls gametes from `primary_tokens`, which is a list of NNS; the
other 20% of the time it pulls gametes from `secondary_tokens`, which is a list of VBG.
The result is some children look a lot like their parents and some look very different;
there's variety in how far the apple falls from the tree.

`Power Level <https://github.com/carawarner/pantheon/blob/master/pantheon/gods.py#L12-L25>`_
****************************************************************************************************
Many traditions describe old gods as more powerful than young gods. When two `Gods` procreate
there's a 30% chance their offspring will be a 'demi-god' rather than a full blown god. That
chance jumps to 50% when a 'god' and 'demi-god' procreate, and when two 'demi-gods' procreate
there's a 25% chance their offspring will be a lowly human.

`Twinning <https://github.com/carawarner/pantheon/blob/master/pantheon/pantheons.py#L65>`_
**************************************************************************************************
20% of the time coupling produces twins; the other 80% of the time it produces a single child.

`Epithets <https://github.com/carawarner/pantheon/blob/master/pantheon/gods.py#L149>`_
*******************************************************************************************************
Most gods (55%) represent 3 domains: God of X, Y, and Z. Slightly fewer gods (35%) represent
two domains: God of X and Y. The remaining gods represent 1  or 4 domains.
