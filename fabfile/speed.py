from __future__ import print_function
from __future__ import division

from fabric.api import *
from fabtools.python import virtualenv

from _cfg import VENV_DIR, GIGA_LOC

import time


class Timer(object):
    # From http://www.huyng.com/posts/python-performance-analysis/
    def __init__(self, name, n):
        self.name = name
        self.n = n

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        print(self.name, 'finished in', '%.2fs' % self.secs)

    def __str__(self):
        return '%s\t%.2f ms / doc' % (self.name, self.msecs / self.n)


@task
def tok(n=1000):
    n = int(n)
    with virtualenv(VENV_DIR):
        with Timer('noop', n) as noop_time:
            local('time bin/run_noop.py %s %d' % (GIGA_LOC, n))
        with Timer('split', n) as split_time:
            local('time bin/run_split.py %s %d' % (GIGA_LOC, n))
        with Timer('spacy', n) as spacy_time:
            local('time bin/run_spacy.py -n %d %s' % (n, GIGA_LOC))
        with Timer('nltk', n) as nltk_time:
            local('time bin/run_nltk.py -n %d %s' % (n, GIGA_LOC))


    print("Milliseconds per document of the tokenizers:")
    print(noop_time)
    print(split_time)
    print(spacy_time)
    print(nltk_time)


@task
def tag(n=1000):
    n = int(n)
    with virtualenv(VENV_DIR):
        print("Milliseconds per document of the tokenizers:")
        with Timer('spacy', n) as spacy_time:
            local('time bin/run_spacy.py -t -n %d %s' % (n, GIGA_LOC))
        with Timer('nltk', n) as nltk_time:
            local('time bin/run_nltk.py -t -n %d %s' % (n, GIGA_LOC))
        print(spacy_time)
        print(nltk_time)


@task
def parse(n=1000):
    n = int(n)
    with virtualenv(VENV_DIR):
        with Timer('spacy', n) as spacy_time:
            local('time bin/run_spacy.py -t -p -n %d %s' % (n, GIGA_LOC))

    print("Milliseconds per document of the tokenizers:")
    print(spacy_time)
