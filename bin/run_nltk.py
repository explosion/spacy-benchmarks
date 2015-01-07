#!/usr/bin/env python
import plac

import nltk
from lib.corpus import Gigaword


@plac.annotations(
    giga_db_loc=("Path to the sqlite3 docs DB.", "positional"),
    n_docs=("Number of docs to process", "option", "n", int),
    pos_tag=("Do POS tagging?", "flag", "t", bool),
    parse=("Do parsing?", "flag", "p", bool),
)
def main(giga_db_loc, n_docs, pos_tag=False, parse=False):
    docs = Gigaword(giga_db_loc, limit=n_docs)
    sbd = nltk.data.load('tokenizers/punkt/english.pickle')
    n_sents = 0
    for doc in docs:
        sentences = sbd.tokenize(doc)
        for sent in sentences:
            tokens = nltk.word_tokenize(sent)
            if pos_tag:
                tags = nltk.pos_tag(tokens)
            n_sents += 1
    print n_sents


if __name__ == '__main__':
    plac.call(main)
