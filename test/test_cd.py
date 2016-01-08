import os

from shellscript import com, cd
from util import original_env


def valid_input():
    yield dict(path=os.getcwd())


def invalid_input():

    p = os.getcwd()
    while os.path.exists(p):
        p += 'x'
    yield dict(path=p)

    home = os.environ['HOME']
    del os.environ['HOME']
    yield dict()
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


def test_no_alteration_on_error(original_env):
    curr = os.getcwd()
    for kwargs in invalid_input():
        cd(**kwargs)
        assert os.getcwd() == curr


def test_wildcard(original_env, tmpdir):
    d = tmpdir.mkdir('abcdefghijkl')
    cd(path=os.path.join(tmpdir.strpath, 'abcd*'))
    assert os.getcwd() == d.strpath
