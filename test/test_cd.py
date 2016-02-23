import os

from shellscript import cd
from util import original_env


def valid_input(tmpdir):
    yield lambda: ([], dict(path=os.getcwd()))
    yield lambda: ([], dict(path=tmpdir.strpath))


def invalid_input(tmpdir):

    def _():
        p = os.getcwd()
        while os.path.exists(p):
            p += 'x'
        return [], dict(path=p)
    yield _

    home = os.environ['HOME']
    def _():
        try:
            del os.environ['HOME']
        except KeyError: pass
        return [], dict()
    yield _
    os.environ['HOME'] = home


def test_back_relative(original_env):
    curr = os.getcwd()
    cmd = cd("..")
    assert os.getcwd() == os.path.dirname(curr)
    assert cmd.ret == 0


def test_back_absolute(original_env):
    curr = os.getcwd()
    cmd = cd(os.path.dirname(curr))
    assert os.getcwd() == os.path.dirname(curr)
    assert cmd.ret == 0


def test_go_home(original_env):
    cmd = cd()
    assert os.getcwd() == os.environ['HOME']
    assert cmd.ret == 0


def test_go_home_via_env(original_env):
    cmd = cd('$HOME')
    assert os.getcwd() == os.environ['HOME']
    assert cmd.ret == 0


def test_no_alteration_on_error(original_env, tmpdir):
    curr = os.getcwd()
    for setup in invalid_input(tmpdir):
        args, kwargs = setup()
        cd(*args, **kwargs)
        assert os.getcwd() == curr


def test_wildcard(original_env, tmpdir):
    d = tmpdir.mkdir('abcdefghijkl')
    cd(path=os.path.join(tmpdir.strpath, 'abcd*'))
    assert os.getcwd() == d.strpath
