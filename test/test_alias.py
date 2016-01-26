import os

from shellscript import dev, alias, ls


def test_ls_all(tmpdir):
    d = os.path.dirname(__file__)
    lsall = alias(ls, all=True)
    assert list(ls(all=True, out=dev.itr)) == list(lsall(out=dev.itr))
