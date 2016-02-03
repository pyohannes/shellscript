import os
import sys

from shellscript import dev, alias, ls, run


def test_ls_all(tmpdir):
    d = os.path.dirname(__file__)
    lsall = alias(ls, all=True)
    assert list(ls(all=True, out=dev.itr)) == list(lsall(out=dev.itr))


def test_arg_order(tmpdir):
    p = alias(run, sys.executable, '-c')
    cmd = p('print("ab\\ncd")', out=dev.itr)
    assert list(cmd) == [ 'ab', 'cd' ]
