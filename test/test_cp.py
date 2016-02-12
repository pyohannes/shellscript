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
    yield [], dict(src=f_existing.strpath)

    yield [], dict(dst=f_existing.strpath)

    # dir as src without recurse
    d_src = tmpdir.mkdir(_make_unique_name(tmpdir))
    d_tgt = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir))
    yield [], dict(src=d_src.strpath, dst=d_tgt)


def _make_unique_name(tmpdir, prefix='', postfix=''):
    make_full_name = lambda s: '%s%s%s' % (prefix, s, postfix)
    fname = 'testfile'
    while os.path.exists(os.path.join(tmpdir.strpath, make_full_name(fname))):
        fname += 'f'
    return make_full_name(fname)


def _make_test_textfile(tmpdir):
    txt = None
    with open(__file__, 'r') as f:
        txt = f.read()
    src = tmpdir.join('testfile')
    f = tmpdir.join(_make_unique_name(tmpdir))
    f.write(txt)
    return f.strpath, txt


def _file_equals(f1, f2):
    if not os.path.isfile(f1) or not os.path.isfile(f2):
        return False
    with open(f1, 'r') as f1_obj:
        with open(f2, 'r') as f2_obj:
            return f1_obj.read() == f2_obj.read()


def _dir_equals(d1, d2):
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
            if not _file_equals(e1_name, e2_name):
                return False
        elif os.path.isdir(e1_name) and os.path.isdir(e2_name):
            # directory compare
            if not _dir_equals(e1_name, e2_name):
                return False
        else:
            # type differs
            return False
    return True


def test_arg_srcdst_simple(tmpdir):
    src, txt = _make_test_textfile(tmpdir)
    tgt = tmpdir.join(_make_unique_name(tmpdir))
    cmd = cp(src, tgt.strpath)
    assert _file_equals(src, tgt.strpath)


def test_arg_src_dir(tmpdir):
    srcdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    srcdir_sub = srcdir.mkdir(_make_unique_name(srcdir))
    _make_test_textfile(srcdir_sub),
    _make_test_textfile(srcdir_sub),
    _make_test_textfile(srcdir)
    tgtdir = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir))
    cmd = cp(srcdir.strpath, tgtdir, recurse=True)
    assert _dir_equals(srcdir.strpath, tgtdir)


def test_arg_src_list(tmpdir):
    srcdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    tgtdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    src = [
            _make_test_textfile(srcdir)[0],
            _make_test_textfile(srcdir)[0] ]
    cmd = cp(src, tgtdir.strpath)
    assert _dir_equals(srcdir.strpath, tgtdir.strpath)


def test_arg_src_wildcard(tmpdir):
    f_txt = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir,
        postfix='.txt'))
    f_rtf = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir,
        postfix='.rtf'))
    for f in (f_txt, f_rtf):
        with open(f, 'w') as fobj:
            fobj.write('ab')
    tgtdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    cmd = cp(os.path.join(tmpdir.strpath, '*.txt'), tgtdir.strpath)
    assert os.listdir(tgtdir.strpath) == [ os.path.basename(f_txt) ]


def test_arg_src_wildcardlist(tmpdir):
    f_txt = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir,
        postfix='.txt'))
    f_rtf = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir,
        postfix='.rtf'))
    f_py = os.path.join(tmpdir.strpath, _make_unique_name(tmpdir,
        postfix='.py'))
    for f in (f_txt, f_rtf, f_py):
        with open(f, 'w') as fobj:
            fobj.write('ab')
    tgtdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    src = [ os.path.join(tmpdir.strpath, '*.%s' % ext) \
            for ext in ('py', 'txt') ]
    cmd = cp(src, tgtdir.strpath)
    assert sorted(os.listdir(tgtdir.strpath)) == sorted(
            [ os.path.basename(f_txt), os.path.basename(f_py) ])


def test_arg_dst_dir(tmpdir):
    src, txt = _make_test_textfile(tmpdir)
    tgtdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    cmd = cp(src, tgtdir.strpath)
    tgt = os.path.join(tgtdir.strpath, os.path.basename(src))
    assert os.path.exists(tgt)
    with open(tgt, 'r') as f:
        assert f.read() == txt


def test_arg_dst_list(tmpdir):
    srcdir1 = tmpdir.mkdir(_make_unique_name(tmpdir))
    src, txt = _make_test_textfile(srcdir1)
    tgtdir1 = tmpdir.mkdir(_make_unique_name(tmpdir))
    tgtdir2 = tmpdir.mkdir(_make_unique_name(tmpdir))
    cmd = cp(src, [tgtdir1.strpath, tgtdir2.strpath])
    assert _dir_equals(tgtdir1.strpath, srcdir1.strpath)
    assert _dir_equals(tgtdir2.strpath, srcdir1.strpath)


def test_arg_dst_wildcard(tmpdir):
    srcdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    src, txt = _make_test_textfile(srcdir)
    tgtdir_parent = tmpdir.mkdir(_make_unique_name(tmpdir))
    tgtdir = tgtdir_parent.mkdir(_make_unique_name(tgtdir_parent))
    cmd = cp(src, os.path.join(tgtdir_parent.strpath, '*'))
    assert _dir_equals(srcdir.strpath, tgtdir.strpath)


def test_arg_dst_wildcardlist(tmpdir):
    srcdir = tmpdir.mkdir(_make_unique_name(tmpdir))
    src, txt = _make_test_textfile(srcdir)
    tgtdir_parent1 = tmpdir.mkdir(_make_unique_name(tmpdir))
    tgtdir1 = tgtdir_parent1.mkdir(_make_unique_name(tgtdir_parent1))
    tgtdir_parent2 = tmpdir.mkdir(_make_unique_name(tmpdir))
    tgtdir2 = tgtdir_parent2.mkdir(_make_unique_name(tgtdir_parent2))
    cmd = cp(
            src, 
            [ os.path.join(tgtdir_parent1.strpath, '*'),
              os.path.join(tgtdir_parent2.strpath, '*') ])
    assert _dir_equals(srcdir.strpath, tgtdir1.strpath)
    assert _dir_equals(srcdir.strpath, tgtdir2.strpath)
