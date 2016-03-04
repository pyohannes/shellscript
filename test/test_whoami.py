import getpass
import os

from shellscript import whoami, dev


def valid_input(tmpdir):
    yield lambda: ([], {})


def invalid_input(tmpdir):
    return []


def test_current():
    cmd = whoami(out=dev.itr)
    assert list(cmd) == [ getpass.getuser() ]
    assert cmd.ret == 0
