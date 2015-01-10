from __future__ import print_function
from __future__ import division
import platform

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

    def __str__(self):
        return '%s\t%.2f ms / doc' % (self.name, self.msecs / self.n)


@task(default=True)
def run(mode, *systems, **kwargs):
    n = int(kwargs.get('n', 1000))
    flags_str = _parse_mode_string(mode)

    cmd = './bin/run_{name}.py {mode} -n {n} {giga_loc}'
    for name in systems:
        with Timer(name, n) as timer:
            with virtualenv(str(VENV_DIR)):
                local(cmd.format(name=name, mode=flags_str, n=n, giga_loc=GIGA_LOC))
        print(timer)


def _parse_mode_string(mode):
    if mode == 'tok':
        return ''
    if mode == 'tag':
        return '-t'
    elif mode == 'parse':
        return '-p'
    else:
        raise ValueError('Invalid mode: got %s, should be one of [tok, tag, parse]' % mode)
