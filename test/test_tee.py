import os

from shellscript import tee, cat, dev
from util import file_make_unique_name, file_make_text, file_equals


def valid_input(tmpdir):
    return []


def invalid_input(tmpdir):
    return []


def test_file(tmpdir):
    outf1 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    outf2 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cat(__file__, out=tee(outf1, out=outf2))
    assert file_equals(outf1, __file__)
    assert file_equals(outf2, __file__)


def test_filelist(tmpdir):
    outf1 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    outf2 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    outf3 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    cmd = cat(__file__, out=tee([ outf1, outf2 ], out=outf3))
    assert file_equals(__file__, outf1)
    assert file_equals(__file__, outf2)
    assert file_equals(__file__, outf3)


def test_append(tmpdir):
    outf = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    outl = []
    cmd = cat(__file__, out=tee(outf, out=outl))
    cmd = cat(__file__, out=tee(outf, out=outl))
    with open(outf, 'r') as f:
        assert len(f.readlines()) < len(outl)
    outf2 = os.path.join(tmpdir.strpath, file_make_unique_name(tmpdir))
    outl2 = []
    cmd = cat(__file__, out=tee(outf2, out=outl2))
    cmd = cat(__file__, out=tee(outf2, append=True, out=outl2))
    with open(outf2, 'r') as f2:
        assert f2.read().split('\n') == outl2


def test_stdout(tmpdir):
    outl = []
    cmd = cat(__file__, out=tee(out=outl))
    with open(__file__, 'r') as f:
        assert (len(f.read().split('\n')) * 2) == len(outl)
