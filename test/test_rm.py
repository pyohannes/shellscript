import os
from shellscript import rm, dev
from util import file_make_unique_name, file_make_text


def valid_input(tmpdir):
    def _():
        f, _ = file_make_text(tmpdir)
        return [], dict(f=f)
    yield _

    def _():
        d = tmpdir.mkdir(file_make_unique_name(tmpdir))
        f, _ = file_make_text(d)
        return [], dict(f=d.strpath, recurse=True)
    yield _

    def _():
        f = file_make_unique_name(tmpdir)
        return [], dict(f=f, force=True)
    yield _


def invalid_input(tmpdir):
    def _():
        d = tmpdir.mkdir(file_make_unique_name(tmpdir))
        f, _ = file_make_text(d)
        return [], dict(f=d.strpath)
    yield _

    def _():
        f = file_make_unique_name(tmpdir)
        return [], dict(f=os.path.join(tmpdir.strpath, f))
    yield _


def test_arg_file_simple(tmpdir):
    f , _ = file_make_text(tmpdir)
    cmd = rm(f)
    assert not os.path.exists(f)


def test_arg_file_wildcard(tmpdir):
    fs = [
            file_make_text(tmpdir, postfix='.txt')[0],
            file_make_text(tmpdir, postfix='.py')[0],
            file_make_text(tmpdir, postfix='.txt')[0] ]
    cmd = rm(os.path.join(tmpdir.strpath, '*.txt'))
    assert not os.path.exists(fs[0])
    assert os.path.exists(fs[1])
    assert not os.path.exists(fs[2])


def test_arg_file_wildcardlist(tmpdir):
    fs = [
            file_make_text(tmpdir, postfix='.txt')[0],
            file_make_text(tmpdir, postfix='.py')[0],
            file_make_text(tmpdir, postfix='.rtf')[0] ]
    cmd = rm([ 
        os.path.join(tmpdir.strpath, '*.txt'),
        os.path.join(tmpdir.strpath, '*.py')])
    assert not os.path.exists(fs[0])
    assert not os.path.exists(fs[1])
    assert os.path.exists(fs[2])


def test_arg_dir(tmpdir):
    d = tmpdir.mkdir(file_make_unique_name(tmpdir))
    f, _ = file_make_text(d)
    cmd = rm(d.strpath, recurse=True)
    assert not os.path.exists(d.strpath)


def test_arg_verbose(tmpdir):
    d = tmpdir.mkdir(file_make_unique_name(tmpdir))
    file_make_text(d)
    file_make_text(d)
    out = []
    cmd = rm(d.strpath, recurse=True, verbose=True, out=out)
    assert len(out) == 3
