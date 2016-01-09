import os
from shellscript import cat, dev


def valid_input(tmpdir):

    f = os.path.join(tmpdir.strpath, 'test_cat')
    with open(f, 'w') as fobj:
        fobj.write('ab\ncd\n')
    yield dict(f=f)

    yield dict(f=__file__)


def invalid_input(tmpdir):
    yield dict(f=tmpdir.strpath)


def test_simple_from_file(tmpdir):
    text = [ 'ab', 'cd', 'ef', 'gh' ]
    f = os.path.join(tmpdir.strpath, 'testfile')
    with open(f, 'w') as fobj:
        fobj.write('\n'.join(text))
    cmd = cat(f, out=dev.itr)
    assert list(cmd) == text


def test_glob_from_file(tmpdir):
    text = set([ 'ab', 'cd', 'ef', 'gh' ])
    for t in text:
        with open(os.path.join(tmpdir.strpath, t), 'w') as fobj:
            fobj.write(t)
    cmd = cat(f=os.path.join(tmpdir.strpath, '*'), out=dev.itr)
    assert set(list(cmd)) == text


def test_simple_from_list(tmpdir):
    text = [ 'ab', 'cd', 'ef', 'gh' ]
    fs = []
    for t in text:
        fs.append(os.path.join(tmpdir.strpath, t))
        with open(fs[-1], 'w') as f:
            f.write(t)
    cmd = cat(f=fs, out=dev.itr)
    assert list(cmd) == text
