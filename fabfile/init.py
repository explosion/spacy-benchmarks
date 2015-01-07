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
    with virtualenv(VENV_DIR):
        local('pip install python-zpar')
    local('wget http://downloads.sourceforge.net/project/zpar/0.7/english.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fzpar%2Ffiles%2F0.7%2F&ts=1420629795&use_mirror=softlayer-sng')
    local('mv english.zip models/')
    with lcd('models'):
        local('unzip english.zip')
        local('mv english/ zpar/')


@task
def install_stanford():
    pass


@task
def install_turbo():
    pass
