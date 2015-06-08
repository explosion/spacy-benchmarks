#!/usr/bin/env python
import plac
import codecs

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
    out_dir = '/tmp/spacy_out'
    if path.exists(out_dir):
        shutil.rmtree(out_dir)
    for i, doc in enumerate(docs):
        tokens = nlp(doc, tag=pos_tag, parse=parse)
        with codecs.open(path.join(out_dir, '%d.txt' % i), 'w', 'utf8') as file_:
            for sent in tokens.sents:
                for word in sent:
                    file_.write('%d\t%s\t%s\t%s\t%d' % (word.orth_, word.tag_, word.head.i, word.dep_))


if __name__ == '__main__':
    plac.call(main)
