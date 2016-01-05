import os
import pytest


@pytest.yield_fixture
def original_env():
    backup = os.environ.copy()
    cwd = os.getcwd()
    yield os.environ
    os.chdir(cwd)
    os.environ.clear()
    os.environ.update(backup)
