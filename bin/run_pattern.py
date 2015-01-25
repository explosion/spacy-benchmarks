#!/usr/bin/env python
import plac

from lib.corpus import Gigaword


@plac.annotations(
    giga_db_loc=("Path to the sqlite3 docs DB.", "positional"),
    n_docs=("Number of docs to process", "option", "n", int),
    pos_tag=("Do POS tagging?", "flag", "t", bool),
    parse=("Do parsing?", "flag", "p", bool),
)
def main(giga_db_loc, n_docs, pos_tag=False, parse=False):
    docs = Gigaword(giga_db_loc, limit=n_docs)
    from pattern.en import parsetree
    n_sents = 0
    for doc in docs:

        tokens = parsetree(doc,
            tokenize = True,     
            tags = pos_tag,     
            chunks = parse,    
            relations = parse,
            lemmata = pos_tag, 
            encoding = 'utf-8',
            tagset = None)    
        n_sents += len(tokens)

    print n_sents


if __name__ == '__main__':
    plac.call(main)
