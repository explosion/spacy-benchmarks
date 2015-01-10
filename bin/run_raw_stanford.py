#!/usr/bin/env python
import plac
import os
from os import path
import subprocess

from lib.corpus import Gigaword


STANFORD_PATH = path.join(path.dirname(__file__), '..', 'ext', 'stanford',
                          'stanford-corenlp-full-2014-10-31')


@plac.annotations(
    giga_db_loc=("Path to the sqlite3 docs DB.", "positional"),
    n_docs=("Number of docs to process", "option", "n", int),
    pos_tag=("Do POS tagging?", "flag", "t", bool),
    parse=("Do parsing?", "flag", "p", bool),
)
def main(giga_db_loc, n_docs, pos_tag=False, parse=False):
    docs = Gigaword(giga_db_loc, limit=n_docs)
    docs_dir = '/tmp/docs_queue'
    if not path.exists(docs_dir):
        os.mkdir(docs_dir)
    filelist = []
    for i, doc in enumerate(docs):
        with open(path.join(docs_dir, '%d.txt' % i), 'w') as file_:
            file_.write(doc)
        filelist.append(path.join(docs_dir, '%d.txt' % i))
    queue_loc = '/tmp/stanford_queue.txt'
    with open(queue_loc, 'w') as file_:
        file_.write('\n'.join(filelist))
    if pos_tag:
        annotators = 'tokenize,ssplit,pos,lemma'
    elif parse:
        annotators = 'tokenize,ssplit,pos,lemma,depparse'
    else:
        annotators = 'tokenize,ssplit'
    cmd = 'cd {corenlp} && ./batch.sh {annotators} {filenames}'
    subprocess.call([cmd.format(corenlp=STANFORD_PATH, annotators=annotators,
                    filenames=queue_loc)], shell=True)
    

if __name__ == '__main__':
    plac.call(main)
