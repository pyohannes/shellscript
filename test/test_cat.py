import os
from shellscript import cat, dev


def valid_input(tmpdir):

    f = tmpdir.join('test_cat1')
    f.write('ab\ncd\n')
    yield dict(f=f.strpath)

    yield dict(f=__file__)


def invalid_input(tmpdir):
    yield dict(f=tmpdir.strpath)


def test_simple_from_file(tmpdir):
    text = [ 'ab', 'cd', 'ef', 'gh' ]
    f = tmpdir.join('testfile')
    f.write('\n'.join(text))
    cmd = cat(f.strpath, out=dev.itr)
    assert list(cmd) == text


def test_glob_from_file(tmpdir):
    text = set([ 'ab', 'cd', 'ef', 'gh' ])
    for t in text:
        f = tmpdir.join(t)
        f.write(t)
    cmd = cat(f=os.path.join(tmpdir.strpath, '*'), out=dev.itr)
    assert set(list(cmd)) == text


def test_simple_from_list(tmpdir):
    text = [ 'ab', 'cd', 'ef', 'gh' ]
    fs = []
    for t in text:
        f = tmpdir.join(t)
        f.write(t)
        fs.append(f.strpath)
    cmd = cat(f=fs, out=dev.itr)
    assert list(cmd) == text