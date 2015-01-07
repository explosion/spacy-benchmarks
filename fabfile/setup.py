from fabric.api import *

from os.path import exists as file_exists
from fabtools.python import virtualenv
from os import path
import os
from ._cfg import VENV_DIR


PWD = path.dirname(__file__)


@task(default=True)
def init(lang="python2.7"):
    make_env(lang)
    install_spacy()
    install_nltk()
    install_zpar()
    install_stanford()
    install_turbo()
    if not path.exists('data'):
        os.mkdir(path.join('data'))


@task
def make_env(lang="python2.7"):
    if file_exists(VENV_DIR):
        local('rm -rf %s' % VENV_DIR)
    local('virtualenv -p %s %s' % (lang, VENV_DIR))
    with virtualenv(VENV_DIR):
        local('pip install setuptools==9.0')
        local('pip install plac')


@task
def install_spacy():
    with virtualenv(VENV_DIR):
        local('pip install spacy')


@task
def install_nltk():
    with virtualenv(VENV_DIR):
        local('pip install numpy')
        local('pip install nltk')


@task
def install_zpar():
    local('pip install python-zpar')


@task
def install_stanford():
    pass
