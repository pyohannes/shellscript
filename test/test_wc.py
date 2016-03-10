import unittest
import os

from shellscript import wc, cat, dev, astr
from util import file_make_unique_name, file_make_text, original_env


def valid_input(tmpdir):
    yield lambda: ([], dict(f=__file__))


def invalid_input(tmpdir):
    yield lambda: ([], dict(f=tmpdir.strpath))


def test_simple(tmpdir):
    text = [ 'ab', 'cd', 'ef', 'gh' ]
    f = tmpdir.join(file_make_unique_name(tmpdir))
    f.write('\n'.join(text))
    out1 = astr(wc, f=f.strpath)
    #out2 = astr(cat, f=f.strpath, out=wc())
    out2 = list(cat(f=f.strpath, out=wc()))
    assert out1.split() == [ '4', '4', '11', f.strpath ]
    assert out2[0].split() == [ '4', '4', '11' ]


def test_glob(tmpdir,  original_env):
    text = [ 'ab', 'c de', 'fg hi', 'j klm n' ]
    for p in text:
        tmpdir.join(p).write(p)
    os.chdir(tmpdir.strpath) 
    out = astr(wc, f='*')
    assert sorted([ o.split() for o in out.split('\n') ]) == \
            sorted([ [ '1', '1', '2', 'ab' ], 
              [ '1', '2', '4', 'c', 'de' ], 
              [ '1', '2', '5', 'fg', 'hi' ], 
              [ '1', '3', '7', 'j', 'klm', 'n' ],
              [ '4', '8', '18', 'total'] ])


def test_args(tmpdir, original_env):
    text = [ 'ab', 'c de', 'fg hi', 'j klm n' ]
    for p in text:
        tmpdir.join(p).write(p)
    os.chdir(tmpdir.strpath)
    out = astr(wc, f='*', chars=True)
    assert sorted([ o.split() for o in out.split('\n') ]) == \
            sorted([ [ '2', 'ab' ], 
              [ '4', 'c', 'de' ], 
              [ '5', 'fg', 'hi' ], 
              [ '7', 'j', 'klm', 'n' ],
              [ '18', 'total' ] ])
    out = astr(wc, f='*', lines=True)
    assert sorted([ o.split() for o in out.split('\n') ]) == \
            sorted([ [ '1', 'ab' ], 
              [ '1', 'c', 'de' ], 
              [ '1', 'fg', 'hi' ], 
              [ '1', 'j', 'klm', 'n' ],
              [ '4', 'total' ] ])
    out = astr(wc, f='*', words=True)
    assert sorted([ o.split() for o in out.split('\n') ]) == \
            sorted([ [ '1', 'ab' ], 
              [ '2', 'c', 'de' ], 
              [ '2', 'fg', 'hi' ], 
              [ '3', 'j', 'klm', 'n' ],
              [ '8', 'total', ]])
    out = astr(wc, f='*', words=True, chars=True)
    assert sorted([ o.split() for o in out.split('\n') ]) == \
            sorted([ [ '1', '2', 'ab' ], 
              [ '2', '4', 'c', 'de' ], 
              [ '2', '5', 'fg', 'hi' ], 
              [ '3', '7', 'j', 'klm', 'n' ],
              [ '8', '18', 'total' ] ])


def test_max_line_length(tmpdir):
    f1 = tmpdir.join(file_make_unique_name(tmpdir))
    f1.write('a\nbc\ndefgh\nijklmno\np')
    f2 = tmpdir.join(file_make_unique_name(tmpdir))
    f2.write('abcdefgh\nijklmno\np\nqrstuv')
    out = astr(wc, f=[f1.strpath, f2.strpath], max_line_length=True)
    assert sorted([ o.split() for o in out.split('\n') ]) == \
            sorted([ [ '7', f1.strpath ], 
              [ '8', f2.strpath ],
              [ '8', 'total' ] ])
