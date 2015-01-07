from fabric.api import *

from os.path import exists as file_exists
from fabtools.python import virtualenv
from os import path
from ._cfg import VENV_DIR


PWD = path.dirname(__file__)


@task(default=True)
def env(lang="python2.7"):
    if file_exists(VENV_DIR):
        local('rm -rf %s' % VENV_DIR)
    local('virtualenv -p %s %s' % (lang, VENV_DIR))
    with virtualenv(VENV_DIR):
        local('pip install setuptools==9.0')
        local('pip install plac')
        local('pip install spacy')
        local('pip install nltk')
