#!/usr/bin/env python
import plac

from spacy.en import English
from lib.corpus import Gigaword


def tokenize(giga_db_loc, n):
    n = int(n)

def main(giga_db_loc, n):
    docs = Gigaword(giga_db_loc, limit=n)
    i = 0
    for doc in docs:
        tokens = doc.split()
        i += len(tokens)
    print i


if __name__ == '__main__':
    plac.call(main)
