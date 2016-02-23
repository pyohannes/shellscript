import os
from shellscript import mv, dev
from util import file_make_unique_name, file_make_text, file_equals, \
                  dir_equals
 

def valid_input(tmpdir):
    def _():
        f1, _ = file_make_text(tmpdir)
        return [], dict(src=f1, dst=tmpdir.strpath)
    yield _

    def _():
        f2, _ = file_make_text(tmpdir)
        return [], dict(src=f2, dst=os.path.join(tmpdir.strpath,
            os.path.basename(__file__)))
    yield _


def invalid_input(tmpdir):
    def _():
        f = os.path.join(tmpdir.strpath, 'x')
        while os.path.exists(f):
            f += 'x'
        return [], dict(src=f, dst=tmpdir.strpath)
    yield _

    def _():
        f1, _ = file_make_text(tmpdir)
        f2, _ = file_make_text(tmpdir)
        f3name = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
        return [], dict(src=[f1, f2], dst=f3name)
    yield _
   
    def _():
        f1, _ = file_make_text(tmpdir)
        d1 = tmpdir.mkdir(file_make_unique_name(tmpdir))
        d2 = tmpdir.mkdir(file_make_unique_name(tmpdir))
        return [], dict(src=f1, dst=[d1.strpath, d2.strpath])
    yield _


def test_arg_verbose(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    file_make_text(srcdir)
    file_make_text(srcdir)
    file_make_text(srcdir)
    tgtdir1 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir2 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    out = []
    cmd = mv(os.path.join(srcdir.strpath, '*'), tgtdir1.strpath, out=out)
    assert len(out) == 0
    cmd = mv(os.path.join(tgtdir1.strpath, '*'), tgtdir2.strpath, verbose=True,
            out=out)
    assert len(out) == 3


def test_arg_srcdst_simple(tmpdir):
    src, txt = file_make_text(tmpdir)
    tgt = tmpdir.join(file_make_unique_name(tmpdir))
    cmd = mv(src, tgt.strpath)
    assert os.path.isfile(tgt.strpath)
    with open(tgt.strpath, 'r') as f:
        assert f.read() == txt


def test_arg_src_dir(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    srcdir_sub = srcdir.mkdir(file_make_unique_name(srcdir))
    file_make_text(srcdir_sub),
    file_make_text(srcdir_sub),
    file_make_text(srcdir)
    tgtdir = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = mv(srcdir.strpath, tgtdir)
    assert len(os.listdir(tgtdir)) == 2
    assert not os.path.exists(srcdir.strpath)


def test_arg_src_list(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src = [
            file_make_text(srcdir)[0],
            file_make_text(srcdir)[0] ]
    cmd = mv(src, tgtdir.strpath)
    assert set(os.listdir(tgtdir.strpath)) == set(
            [ os.path.basename(e) for e in src ])
    assert len(os.listdir(srcdir.strpath)) == 0


def test_arg_src_wildcard(tmpdir):
    f_txt = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.txt'))
    f_rtf = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.rtf'))
    for f in (f_txt, f_rtf):
        with open(f, 'w') as fobj:
            fobj.write('ab')
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    cmd = mv(os.path.join(tmpdir.strpath, '*.txt'), tgtdir.strpath)
    assert os.listdir(tgtdir.strpath) == [ os.path.basename(f_txt) ]


def test_arg_src_wildcardlist(tmpdir):
    f_txt = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.txt'))
    f_rtf = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.rtf'))
    f_py = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.py'))
    for f in (f_txt, f_rtf, f_py):
        with open(f, 'w') as fobj:
            fobj.write('ab')
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src = [ os.path.join(tmpdir.strpath, '*.%s' % ext) \
            for ext in ('py', 'txt') ]
    cmd = mv(src, tgtdir.strpath)
    assert sorted(os.listdir(tgtdir.strpath)) == sorted(
            [ os.path.basename(f_txt), os.path.basename(f_py) ])


def test_arg_dst_dir(tmpdir):
    src, txt = file_make_text(tmpdir)
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    cmd = mv(src, tgtdir.strpath)
    tgt = os.path.join(tgtdir.strpath, os.path.basename(src))
    assert os.path.exists(tgt)
    with open(tgt, 'r') as f:
        assert f.read() == txt


def test_arg_dst_wildcard(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src, txt = file_make_text(srcdir)
    tgtdir_parent = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir = tgtdir_parent.mkdir(file_make_unique_name(tgtdir_parent))
    cmd = mv(src, os.path.join(tgtdir_parent.strpath, '*'))
    assert os.path.exists(
            os.path.join(tgtdir.strpath, os.path.basename(srcdir.strpath)))
