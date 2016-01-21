import os
from shellscript import ls, dev


def valid_input(tmpdir):

    d = tmpdir.mkdir('test_ls')
    yield dict(f=d.strpath)

    f = d.join('test_ls_1')
    f.write('')
    yield dict(f=f.strpath)

    yield dict(f=os.path.join(d.strpath, '*'))


def invalid_input(tmpdir):

    yield dict(f=os.path.join(tmpdir.strpath, 'invalid'))


def test_empty(tmpdir):
    cmd = ls(f=tmpdir.strpath, out=dev.itr)
    assert len(list(cmd)) == 0


def test_simple_files(tmpdir):
    files = [ 'ab', 'cd', 'ef', 'gh' ]
    for t in files:
        f = tmpdir.join(t)
        f.write(t)
    cmd = ls(f=tmpdir.strpath, out=dev.itr)
    assert list(cmd) == files


def test_simple_glob(tmpdir):
    files = [ 'ab', 'abcd', 'abcdef', 'abcdefgh' ]
    for t in files:
        f = tmpdir.join(t)
        f.write(t)
    cmd = ls(os.path.join(tmpdir.strpath, '*ef*'), out=dev.itr)
    assert list(cmd) == [ os.path.join(tmpdir.strpath, f) for f in  files[2:] ]


def test_hidden_files(tmpdir):
    files = [ '.ab', '.abc', 'abcd', 'abcde' ]
    for t in files:
        f = tmpdir.join(t)
        f.write(t)
    if os.name == 'nt':
        import ctypes
        for f in files[:2]:
            ctypes.windll.kernel32.SetFileAttributesW(f, 2)
    cmd = ls(f=tmpdir.strpath, out=dev.itr)
    assert list(cmd) == files[2:]
    cmd = ls(f=tmpdir.strpath, all=True, out=dev.itr)
    assert list(cmd) == (['.', '..', ] + files)


def test_point(tmpdir):
    assert list(ls(out=dev.itr)) == list(ls(f='.', out=dev.itr))


def test_pointpoint(tmpdir):
    parent = os.path.dirname(os.getcwd())
    assert list(ls(parent, out=dev.itr)) == list(ls(f='..', out=dev.itr))
