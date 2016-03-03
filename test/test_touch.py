import os
import time
from shellscript import touch, dev
from util import file_make_unique_name, file_make_text


def valid_input(tmpdir):
    def _():
        f, _ = file_make_text(tmpdir)
        return [], dict(f=f)
    yield _

    def _():
        f = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
        return [], dict(f=f)
    yield _


def invalid_input(tmpdir):
    yield lambda: ([], {})

    def _():
        f = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
        return [], dict(f=os.path.join(f, 'f'))
    yield _


def test_arg_file_simple(tmpdir):
    f = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = touch(f)
    assert os.path.exists(f)


def test_arg_file_wildcard(tmpdir):
    fs = [
            file_make_text(tmpdir, postfix='.txt')[0],
            file_make_text(tmpdir, postfix='.py')[0],
            file_make_text(tmpdir, postfix='.txt')[0] ]
    stats_before = [ os.stat(f) for f in ( fs[0], fs[2] )]
    time.sleep(2)
    cmd = touch(os.path.join(tmpdir.strpath, '*.txt'))
    stats_after = [ os.stat(f) for f in ( fs[0], fs[2] )]
    for before, after in zip(stats_before, stats_after):
        assert before.st_atime != after.st_atime
        assert before.st_mtime != after.st_mtime


def test_arg_no_create(tmpdir):
    f, _ = file_make_text(tmpdir)
    f2 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = touch([f, f2], nocreate=True)
    assert os.path.exists(f)
    assert not os.path.exists(f2)
    cmd = touch([f, f2])
    assert os.path.exists(f)
    assert os.path.exists(f2)


def test_arg_time_access(tmpdir):
    f, _ = file_make_text(tmpdir)
    stat_before = os.stat(f)
    time.sleep(2)
    cmd = touch(f, time='access')
    stat_after = os.stat(f)
    assert stat_before.st_atime != stat_after.st_atime
    assert stat_before.st_mtime == stat_after.st_mtime


def test_arg_time_modify(tmpdir):
    f, _ = file_make_text(tmpdir)
    stat_before = os.stat(f)
    time.sleep(2)
    cmd = touch(f, time='modify')
    stat_after = os.stat(f)
    assert stat_before.st_atime == stat_after.st_atime
    assert stat_before.st_mtime != stat_after.st_mtime
