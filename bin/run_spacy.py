#!/usr/bin/env python
import plac

from spacy.en import English
from lib.corpus import Gigaword


@plac.annotations(
    giga_db_loc=("Path to the sqlite3 docs DB.", "positional"),
    n_docs=("Number of docs to process", "option", "n", int),
    pos_tag=("Do POS tagging?", "flag", "t", bool),
    parse=("Do parsing?", "flag", "p", bool),
)
def main(giga_db_loc, n_docs, pos_tag=False, parse=False):
    docs = Gigaword(giga_db_loc, limit=n_docs)
    nlp = English()
    for doc in docs:
        tokens = nlp(doc, tag=pos_tag, parse=parse)


if __name__ == '__main__':
    plac.call(main)
