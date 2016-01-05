from shellscript import com
from shellscript.proto import OutString, ErrString


def test_com():
    def _cmd():
        yield OutString('out')
        yield ErrString('err')
        yield OutString('out2')
    cmd = _cmd()
    out, err = com(cmd)
    assert out == [ 'out', 'out2' ]
    assert err == [ 'err' ]
