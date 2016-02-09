import os
import time
from shellscript import sleep


def valid_input(tmpdir):
    yield [], dict(secs=0.1)


def invalid_input(tmpdir):
    yield [], dict(secs=-2)


def test_sleep(tmpdir):
    cmd = sleep(2)
    start = time.time()
    list(cmd)
    end = time.time()
    assert (end - start) >= 2
