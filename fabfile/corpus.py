from fabric.api import *

from lib.corpus import Gigaword

from ._cfg import GIGA_LOC


@task(alias='giga')
def create_gigaword_db(giga_dir, db_loc=GIGA_LOC):
    Gigaword.create(giga_dir, db_loc)
