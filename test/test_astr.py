import os
import sys

from shellscript import dev, astr, ls, whoami


def test_astr_whoami(tmpdir):
    assert astr(whoami) == str(whoami(out=dev.itr))


def test_astr_ls(tmpdir):
    d = os.path.dirname(os.path.abspath(__file__))
    out = []
    ls(d, out=out)
    assert astr(ls, d) == ('\n'.join(out))
