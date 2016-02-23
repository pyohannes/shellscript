import os
import pytest


@pytest.yield_fixture
def original_env():
    backup = os.environ.copy()
    cwd = os.getcwd()
    yield os.environ
    os.chdir(cwd)
    os.environ.clear()
    os.environ.update(backup)


def file_make_unique_name(tmpdir, prefix='', postfix=''):
    make_full_name = lambda s: '%s%s%s' % (prefix, s, postfix)
    fname = 'testfile'
    while os.path.exists(os.path.join(tmpdir.strpath, make_full_name(fname))):
        fname += 'f'
    return make_full_name(fname)


def file_make_text(tmpdir):
    txt = None
    with open(__file__, 'r') as f:
        txt = f.read()
    src = tmpdir.join('testfile')
    f = tmpdir.join(file_make_unique_name(tmpdir))
    f.write(txt)
    return f.strpath, txt


def file_equals(f1, f2):
    if not os.path.isfile(f1) or not os.path.isfile(f2):
        return False
    with open(f1, 'r') as f1_obj:
        with open(f2, 'r') as f2_obj:
            return f1_obj.read() == f2_obj.read()


def dir_equals(d1, d2):
    if not os.path.exists(d1) or not os.path.exists(d2):
        return False
    d1_c = os.listdir(d1)
    d2_c = os.listdir(d2)
    if not sorted(d1_c) == sorted(d2_c):
        return False
    for entry in d1_c:
        e1_name = os.path.join(d1, entry)
        e2_name = os.path.join(d2, entry)
        if os.path.isfile(e1_name) and os.path.isfile(e2_name):
            # file compare
            if not file_equals(e1_name, e2_name):
                return False
        elif os.path.isdir(e1_name) and os.path.isdir(e2_name):
            # directory compare
            if not dir_equals(e1_name, e2_name):
                return False
        else:
            # type differs
            return False
    return True


