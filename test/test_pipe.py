import os
import pytest

from shellscript import *
from shellscript.proto import ProtocolError


def test_cat_grep(tmpdir):
    text = ['def xy():', ' return False']
    f = tmpdir.join('input')
    f.write('\n'.join(text))
    cmd = cat(f.strpath, out=grep('^def', out=dev.itr))
    assert list(cmd) == [ text[0] ]


def test_cat_grep_multiple_invocation(tmpdir):
    text = ['def xy():', ' return False']
    f = tmpdir.join('input')
    f.write('\n'.join(text))
    cmd = cat(f.strpath, out=grep('^def', out=dev.itr))
    assert list(cmd) == list(cmd) == list(cmd) == [ text[0] ]


def test_cat_grep_out_err(tmpdir):
    err = []
    cmd = cat(tmpdir.strpath, err=err, out=grep('^def'))
    assert len(err) != 0


def test_invalid_out_redir():
    with pytest.raises(ProtocolError):
        cat(__file__, out=3.14)


def test_invalid_err_redir():
    with pytest.raises(ProtocolError):
        cat(__file__, err=3.14)


def test_invalid_err_pipe():
    with pytest.raises(ProtocolError):
        cat(__file__, out=grep('ab'), err=grep('cd'))
