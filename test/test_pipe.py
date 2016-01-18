import os
from shellscript import *


def test_cat_grep(tmpdir):
    text = ['def xy():', ' return False']
    f = tmpdir.join('input')
    f.write('\n'.join(text))
    cmd = cat(f.strpath, out=grep('^def', out=dev.itr))
    assert list(cmd) == [ text[0] ]


def test_cat_grep_out_err(tmpdir):
    err = []
    cmd = cat(tmpdir.strpath, err=err, out=grep('^def'))
    assert len(err) != 0
