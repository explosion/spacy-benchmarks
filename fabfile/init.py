from fabric.api import *
import sys

from pathlib import Path

from fabtools.python import virtualenv
import os
from ._cfg import VENV_DIR, DATA_DIR, CACHE_DIR


URLS = {
    'zpar': ('http://downloads.sourceforge.net/project/zpar/0.7/english.zip?r='
            'http%3A%2F%2Fsourceforge.net%2Fprojects%2Fzpar%2Ffiles%2F0.7%2F&ts'
            '=1420629795&use_mirror=softlayer-sng'),
    'corenlp': 'http://nlp.stanford.edu/software/stanford-corenlp-full-2014-10-31.zip',
    'corenlp-sr': 'http://nlp.stanford.edu/software/stanford-srparser-2014-10-23-models.jar'
}


FILENAMES = {'zpar': 'english.tgz',
             'corenlp': 'stanford-corenlp-full-2014-10-31.zip',
             'corenlp-sr': 'stanford-srparser-2014-10-23-models.jar'
            }


def download(filename, url):
    cache_path = CACHE_DIR / filename
    if not cache_path.exists():
        with lcd(str(CACHE_DIR)):
            local('wget %s' % url)
    return cache_path


def unzip_into(archive, dest_dir):
    dest = dest_dir / archive.name
    local('cp %s %s' % (archive, dest))
    with lcd(str(dest_dir)):
        local('unzip -f %s' % dest.name)
        dest.unlink()


@task(default=True)
def init(lang="python2.7"):
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir()
    env()
    spacy()
    nltk()
    zpar()
    stanford()
    turbo()
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()


@task
def env(lang="python2.7"):
    if VENV_DIR.exists():
        local('rm -rf %s' % VENV_DIR)
    local('python -m virtualenv -p %s %s' % (lang, VENV_DIR))
    with virtualenv(str(VENV_DIR)):
        local('pip install setuptools==9.0')
        local('pip install plac')


@task
def spacy():
    with virtualenv(str(VENV_DIR)):
        local('pip install spacy')


@task
def nltk():
    with virtualenv(str(VENV_DIR)):
        local('pip install numpy')
        local('pip install nltk')


@task
def zpar():
    with virtualenv(str(VENV_DIR)):
        local('pip install python-zpar')
    download(Path(FILENAMES['zpar']), URLS['zpar'])
    with lcd('models'):
        local('unzip english.zip')
        local('mv english/ zpar/')


@task
def stanford():
    stanford_dir = Path('ext/stanford')
    if not stanford_dir.exists():
        stanford_dir.mkdirs()
    url = URLS['corenlp']
    filename = Path(FILENAMES['corenlp'])
    path = download(filename, url)
    unzip_into(path, stanford_dir)
    download(Path(FILENAMES['corenlp-sr']), URLS['corenlp-sr'])
    with virtualenv(str(VENV_DIR)):
        local('pip install https://github.com/honnibal/stanford_corenlp_pywrapper/archive/master/zip')
