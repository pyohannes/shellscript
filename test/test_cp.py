import os
from shellscript import cp, dev


def valid_input(tmpdir):
    yield [], dict(src=__file__, dst=tmpdir.strpath)

    yield [], dict(src=__file__, dst=os.path.join(tmpdir.strpath,
        os.path.basename(__file__)))


def invalid_input(tmpdir):
    f = os.path.join(tmpdir.strpath, 'x')
    while os.path.exists(f):
        f += 'x'
    yield [], dict(src=f, dst=tmpdir.strpath)

    f_existing = tmpdir.join('existing')
    f_existing.write('xy')
    yield [], dict(src=f_existing)

    yield [], dict(dst=f_existing)


def _make_unique_filename(tmpdir):
    fname = 'testfile'
    while os.path.exists(os.path.join(tmpdir.strpath, fname)):
        fname += 'f'
    return fname


def _make_unique_dirname(tmpdir):
    dname = 'testdir'
    while os.path.exists(os.path.join(tmpdir.strpath, dname)):
        dname += 'd'
    return dname


def _make_test_textfile(tmpdir):
    txt = None
    with open(__file__, 'r') as f:
        txt = f.read()
    src = tmpdir.join('testfile')
    f = tmpdir.join(_make_unique_filename(tmpdir))
    f.write(txt)
    return f.strpath, txt


def test_simple(tmpdir):
    src, txt = _make_test_textfile(tmpdir)
    tgt = tmpdir.join(_make_unique_filename(tmpdir))
    cmd = cp(src, tgt.strpath)
    assert os.path.exists(tgt.strpath)
    with open(tgt.strpath, 'r') as f:
        assert f.read() == txt


def test_simple_dirtarget(tmpdir):
    src, txt = _make_test_textfile(tmpdir)
    tgtdir = tmpdir.mkdir(_make_unique_dirname(tmpdir))
    cmd = cp(src, tgtdir.strpath)
    tgt = os.path.join(tgtdir.strpath, os.path.basename(src))
    assert os.path.exists(tgt)
    with open(tgt, 'r') as f:
        assert f.read() == txt
