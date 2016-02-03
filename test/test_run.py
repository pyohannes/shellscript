import os
import sys

from shellscript import run, dev


def valid_input(tmpdir):

    yield [sys.executable, '-c', 'quit()'], dict()


def invalid_input(tmpdir):

    p = sys.executable
    while os.path.exists(p):
        p += 'a'
    yield [p], dict()


def test_stdout_stderr(tmpdir):
    script = [ 'import sys ; ' + \
               'sys.stdout.write("ab") ; ' + \
               'sys.stderr.write("cd")'
             ]
    out = []
    err = []
    cmd = run(sys.executable, '-c', script, out=out, err=err)
    assert out == [ 'ab' ]
    assert err == [ 'cd' ]


def test_stdout_delay(tmpdir):
    script = [ 'import sys, time ; ' + \
               'sys.stdout.write("ab\\ncd\\nef") ; ' + \
               'time.sleep(5)'
             ]
    cmd = run(sys.executable, '-c', script, out=dev.itr)
    assert list(cmd) == [ 'ab', 'cd', 'ef' ]
