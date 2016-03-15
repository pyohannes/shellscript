import os
import pytest

from shellscript import *
from shellscript.proto import ProtocolError

from util import file_make_unique_name


def test_cat_grep(tmpdir):
    text = ['def xy():', ' return False']
    f = tmpdir.join('input')
    f.write('\n'.join(text))
    cmd = cat(f.strpath, out=pipe(grep, '^def', out=dev.itr))
    assert list(cmd) == [ text[0] ]


def test_cat_grep_multiple_invocation(tmpdir):
    text = ['def xy():', ' return False']
    f = tmpdir.join('input')
    f.write('\n'.join(text))
    cmd = cat(f.strpath, out=pipe(grep, '^def', out=dev.itr))
    assert list(cmd) == list(cmd) == list(cmd) == [ text[0] ]


def test_cat_grep_out_err(tmpdir):
    err = []
    cmd = cat(tmpdir.strpath, err=err, out=(grep, '^def'))
    assert len(err) != 0


def test_invalid_out_redir():
    with pytest.raises(ProtocolError):
        cat(__file__, out=3.14)


def test_invalid_err_redir():
    with pytest.raises(ProtocolError):
        cat(__file__, err=3.14)


def test_invalid_err_pipe():
    with pytest.raises(ProtocolError):
        cat(__file__, out=(grep, 'ab'), err=(grep, 'cd'))


def test_astr_cat_wc(tmpdir):
    text = [ '1', '2', '3', '4' ]
    f = tmpdir.join(file_make_unique_name(tmpdir))
    f.write('\n'.join(text))
    out = astr(cat, f.strpath, out=(wc,))
    assert out.split() == [ '4', '4', '7' ]
