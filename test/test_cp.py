import os
import stat
import time
from shellscript import cp, dev
from util import file_make_unique_name, file_make_text, file_equals, \
                  dir_equals


def valid_input(tmpdir):
    yield lambda: ([], dict(src=__file__, dst=tmpdir.strpath))

    yield lambda: ([], dict(src=__file__, dst=os.path.join(tmpdir.strpath,
        os.path.basename(__file__))))


def invalid_input(tmpdir):
    def _():
        f = os.path.join(tmpdir.strpath, 'x')
        while os.path.exists(f):
            f += 'x'
        return [], dict(src=f, dst=tmpdir.strpath)
    yield _
    
    f_existing = tmpdir.join('existing')
    f_existing.write('xy')

    def _():
        return [], dict(src=f_existing.strpath)
    yield _
    
    yield lambda: ([], dict(dst=f_existing.strpath))
    
    def _():
        # dir as src without recurse
        d_src = tmpdir.mkdir(file_make_unique_name(tmpdir))
        d_tgt = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
        return [], dict(src=d_src.strpath, dst=d_tgt)
    yield _


def test_arg_srcdst_simple(tmpdir):
    src, txt = file_make_text(tmpdir)
    tgt = tmpdir.join(file_make_unique_name(tmpdir))
    cmd = cp(src, tgt.strpath)
    assert file_equals(src, tgt.strpath)


def test_arg_src_dir(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    srcdir_sub = srcdir.mkdir(file_make_unique_name(srcdir))
    file_make_text(srcdir_sub),
    file_make_text(srcdir_sub),
    file_make_text(srcdir)
    tgtdir = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(srcdir.strpath, tgtdir, recurse=True)
    assert dir_equals(srcdir.strpath, tgtdir)


def test_arg_src_list(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src = [
            file_make_text(srcdir)[0],
            file_make_text(srcdir)[0] ]
    cmd = cp(src, tgtdir.strpath)
    assert dir_equals(srcdir.strpath, tgtdir.strpath)


def test_arg_src_wildcard(tmpdir):
    f_txt = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.txt'))
    f_rtf = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir,
        postfix='.rtf'))
    for f in (f_txt, f_rtf):
        with open(f, 'w') as fobj:
            fobj.write('ab')
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    cmd = cp(os.path.join(tmpdir.strpath, '*.txt'), tgtdir.strpath)
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
    cmd = cp(src, tgtdir.strpath)
    assert sorted(os.listdir(tgtdir.strpath)) == sorted(
            [ os.path.basename(f_txt), os.path.basename(f_py) ])


def test_arg_dst_dir(tmpdir):
    src, txt = file_make_text(tmpdir)
    tgtdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    cmd = cp(src, tgtdir.strpath)
    tgt = os.path.join(tgtdir.strpath, os.path.basename(src))
    assert os.path.exists(tgt)
    with open(tgt, 'r') as f:
        assert f.read() == txt


def test_arg_dst_list(tmpdir):
    srcdir1 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src, txt = file_make_text(srcdir1)
    tgtdir1 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir2 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    cmd = cp(src, [tgtdir1.strpath, tgtdir2.strpath])
    assert dir_equals(tgtdir1.strpath, srcdir1.strpath)
    assert dir_equals(tgtdir2.strpath, srcdir1.strpath)


def test_arg_dst_wildcard(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src, txt = file_make_text(srcdir)
    tgtdir_parent = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir = tgtdir_parent.mkdir(file_make_unique_name(tgtdir_parent))
    cmd = cp(src, os.path.join(tgtdir_parent.strpath, '*'))
    assert dir_equals(srcdir.strpath, tgtdir.strpath)


def test_arg_dst_wildcardlist(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    src, txt = file_make_text(srcdir)
    tgtdir_parent1 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir1 = tgtdir_parent1.mkdir(file_make_unique_name(tgtdir_parent1))
    tgtdir_parent2 = tmpdir.mkdir(file_make_unique_name(tmpdir))
    tgtdir2 = tgtdir_parent2.mkdir(file_make_unique_name(tgtdir_parent2))
    cmd = cp(
            src, 
            [ os.path.join(tgtdir_parent1.strpath, '*'),
              os.path.join(tgtdir_parent2.strpath, '*') ])
    assert dir_equals(srcdir.strpath, tgtdir1.strpath)
    assert dir_equals(srcdir.strpath, tgtdir2.strpath)


def test_arg_verbose(tmpdir):
    srcdir = tmpdir.mkdir(file_make_unique_name(tmpdir))
    file_make_text(srcdir)
    file_make_text(srcdir)
    file_make_text(srcdir)
    out = []
    tgtdir = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(srcdir.strpath, tgtdir, recurse=True, out=out)
    assert len(out) == 0
    tgtdir = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(srcdir.strpath, tgtdir, recurse=True, 
            verbose=True, out=out)
    assert len(out) == 4


def _arg_preserve_template(tmpdir, src, kwargs):
    # wait before creating next file
    time.sleep(2)
    tgt1 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(src, tgt1, **kwargs)
    tgt1_stat = os.stat(tgt1)
    src_stat = os.stat(src)
    assert src_stat.st_mode != tgt1_stat.st_mode
    assert src_stat.st_mtime != tgt1_stat.st_mtime
    tgt2 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(src, tgt2, preserve="mode", **kwargs)
    tgt2_stat = os.stat(tgt2)
    src_stat = os.stat(src)
    assert src_stat.st_mode == tgt2_stat.st_mode
    assert src_stat.st_mtime != tgt2_stat.st_mtime
    tgt3 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(src, tgt3, preserve="timestamps", **kwargs)
    tgt3_stat = os.stat(tgt3)
    src_stat = os.stat(src)
    assert src_stat.st_mode != tgt3_stat.st_mode
    assert src_stat.st_mtime == tgt3_stat.st_mtime
    tgt4 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(src, tgt4, preserve="timestamps,mode", **kwargs)
    tgt4_stat = os.stat(tgt4)
    src_stat = os.stat(src)
    assert src_stat.st_mode == tgt4_stat.st_mode
    assert src_stat.st_mtime == tgt4_stat.st_mtime
    tgt5 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cp(src, tgt5, p=True, **kwargs)
    tgt5_stat = os.stat(tgt5)
    src_stat = os.stat(src)
    assert src_stat.st_mode == tgt5_stat.st_mode
    assert src_stat.st_mtime == tgt5_stat.st_mtime


def test_arg_preserve_file(tmpdir):
    src, txt = file_make_text(tmpdir)
    os.chmod(src, 0o777)
    _arg_preserve_template(tmpdir, src, kwargs=dict())


def test_arg_preserve_dir(tmpdir):
    d = tmpdir.mkdir(file_make_unique_name(tmpdir))
    os.chmod(d.strpath, 0o777)
    _arg_preserve_template(tmpdir, d.strpath, kwargs=dict(recurse=True))
