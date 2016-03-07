import os
import time
from shellscript import date, dev


def valid_input(tmpdir):
    yield lambda: ([], dict())

    yield lambda: ([], dict(fmt='%m'))


def invalid_input(tmpdir):
    yield lambda: ([], dict(fmt=9))


def test_arg_fmt_default(tmpdir):
    cmd = date(out=dev.itr)
    assert list(cmd) == [ time.strftime('%c') ]


def test_arg_fmt_custom(tmpdir):
    cmd = date('%m', out=dev.itr)
    assert list(cmd) == [ time.strftime('%m') ]
