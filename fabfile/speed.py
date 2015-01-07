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


# The code here is quite repetitive, by choice.
# Because these scripts all just dispatch a bunch of jobs, I find it easier to
# read the list of commands in sequence, instead of following wrappers upon
# wrappers.
# This also makes it easier to understand any one function independently, and to
# update them independently in ad hoc ways.


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
def tag(n=1000, to_run='snz'):
    do_spacy = 's' in to_run
    do_zpar = 'z' in to_run
    do_nltk = 'n' in to_run
    n = int(n)
    with virtualenv(VENV_DIR):
        with Timer('spacy', n) as spacy_time:
            if do_spacy:
                local('time bin/run_spacy.py -t -n %d %s' % (n, GIGA_LOC))
        with Timer('nltk', n) as nltk_time:
            if do_nltk:
                local('time bin/run_nltk.py -t -n %d %s' % (n, GIGA_LOC))
        with Timer('zpar', n) as zpar_time:
            if do_zpar:
                local('time bin/run_zpar.py -t -n %d %s' % (n, GIGA_LOC))
        print("Milliseconds per document of the taggers:")
        print(spacy_time)
        print(zpar_time)
        print(nltk_time)


@task
def parse(n=1000):
    n = int(n)
    with virtualenv(VENV_DIR):
        with Timer('spacy', n) as spacy_time:
            local('time bin/run_spacy.py -t -p -n %d %s' % (n, GIGA_LOC))

    print("Milliseconds per document of the parsers:")
    print(spacy_time)
