#!/usr/bin/env python
import plac

import nltk
from lib.corpus import Gigaword
from zpar import ZPar


@plac.annotations(
    giga_db_loc=("Path to the sqlite3 docs DB.", "positional"),
    n_docs=("Number of docs to process", "option", "n", int),
    pos_tag=("Do POS tagging?", "flag", "t", bool),
    parse=("Do parsing?", "flag", "p", bool),
)
def main(giga_db_loc, n_docs, pos_tag=False, parse=False):
    docs = Gigaword(giga_db_loc, limit=n_docs)
    sbd = nltk.data.load('tokenizers/punkt/english.pickle')
    from zpar import ZPar
    n = 0
    with ZPar('models/zpar') as z:
        tagger = z.get_tagger()
        if parse:
            parser = z.get_depparser()
        for doc in docs:
            sentences = sbd.tokenize(doc)
            for sent in sentences:
                if parse:
                    dep_parsed_sent = parser.dep_parse_sentence(sent)
                elif pos_tag:
                    tags = parser.tag_sentence(sent)
                n += len(sent)
    print n


if __name__ == '__main__':
    plac.call(main)
