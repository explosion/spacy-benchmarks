# Setup the corpus DB

The speed test expects to read documents from a simple SQLite table. More corpus
injestors need to be written. So far there's one to create the table from the Gigaword
corpus.

    fab corpus.giga:path_to_gigaword/

# Setup the tools

    fab init

This should download and install spaCy and other NLP libraries.

# Running a benchmark

    fab speed:parse,spacy,n=1000
    fab speed:tag,spacy
    fab speed:tag,spacy,nltk,n=10000
    fab speed:tokenize,spacy,clearnlp
