import os

from shellscript import pwd, cd, dev
from util import original_env


def valid_input():
    yield {}


def invalid_input():
    return []


def test_current():
    cmd = pwd(out=dev.itr)
    assert list(cmd) == [ os.getcwd() ]
    assert cmd.ret == 0
