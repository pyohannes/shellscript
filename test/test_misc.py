import os

from shellscript import *


def test_command_as_input(tmpdir):
    files = [ 'a.py', 'b.py', 'c.py', 'd.txt', 'e.py' ]
    for t in files:
        f = tmpdir.join(t)
        f.write(t)
    cmd = cat(ls(os.path.join(tmpdir.strpath, '*.py'), out=dev.itr), out=dev.itr)
    assert list(cmd) == [ t for t in files if t.endswith('.py') ]


