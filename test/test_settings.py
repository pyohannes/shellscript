import os

from util import original_env
from shellscript.settings import load


def _reset_paths(tmpdir):
    os.environ['HOME'] = tmpdir
    try:
        del os.environ['SHELLSCRIPTRC']
    except KeyError: pass


def test_load_nonexistent(tmpdir, original_env):
    _reset_paths(tmpdir.strpath) 
    mod = load()
    assert mod is None

def test_load_home(tmpdir, original_env):
    _reset_paths(tmpdir.strpath) 
    tmpdir.join('.shellscriptrc').write('ps = alias(run, "ps")')
    mod = load()
    assert mod and 'ps' in mod.__dict__


def test_load_envvar(tmpdir, original_env):
    _reset_paths(tmpdir.strpath) 
    f = tmpdir.join('shellscript')
    f.write('ps = alias(run, "ps")')
    os.environ['SHELLSCRIPTRC'] = f.strpath
    mod = load()
    assert mod and 'ps' in mod.__dict__
