#!/usr/bin/env python
import plac

from spacy.en import English
from lib.corpus import Gigaword


def main(giga_db_loc, n):
    n = int(n)
    docs = Gigaword(giga_db_loc, limit=n)
    i = 0
    for doc in docs:
        i += len(doc)
    print i




if __name__ == '__main__':
    plac.call(main)
