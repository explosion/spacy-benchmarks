#!/usr/bin/env python
import plac
from os import path

from lib.corpus import Gigaword
from stanford_corenlp_pywrapper import sockwrap


sockwrap.XMX_AMOUNT = "2g"

STANFORD_PATH = path.join(path.dirname(__file__), '..', 'ext', 'stanford',
                          'stanford-corenlp-full-2014-10-31')

CONFIG_PATH = path.join(path.dirname(__file__), '..', 'stanford.ini')


@plac.annotations(
    giga_db_loc=("Path to the sqlite3 docs DB.", "positional"),
    n_docs=("Number of docs to process", "option", "n", int),
    pos_tag=("Do POS tagging?", "flag", "t", bool),
    parse=("Do parsing?", "flag", "p", bool),
)
def main(giga_db_loc, n_docs, pos_tag=False, parse=False):
    docs = Gigaword(giga_db_loc, limit=n_docs)
    if parse:
        mode = "justparse"
    elif pos_tag:
        mode = "pos"
    else:
        mode = "tokenize"
    nlp = sockwrap.SockWrap(mode=mode, corenlp_libdir=STANFORD_PATH, configfile=CONFIG_PATH,
                            server_port=12342)
    for doc in docs:
        parse = nlp.parse_doc(doc)


if __name__ == '__main__':
    plac.call(main)
