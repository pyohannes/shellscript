import os
from shellscript import grep, dev


def valid_input(tmpdir):

    def _():
        f = tmpdir.join('test_grep1')
        f.write('ab\ncd\nef\ngh')
        return [], dict(regex='.*', f=f.strpath)
    yield _

    yield lambda: ([], dict(regex='^def', f=__file__))


def invalid_input(tmpdir):
    yield lambda: ([], dict(regex='x', f=tmpdir.strpath))

    yield lambda: ([], dict(regex=3, f=__file__))

    yield lambda: ([], dict(f=__file__))


def test_from_file(tmpdir):
    text = [ 'abcdefghij', 'bcdefghijk', 'cdefghijkl', 'defghijklm' ]
    f = tmpdir.join('f')
    f.write('\n'.join(text))
    cmd = grep(regex='cd.*jk', f=f.strpath, out=dev.itr)
    assert list(cmd) == text[1:3]


def test_from_multiple_files(tmpdir):
    texts = [ [ 'abj', 'kltm', 'a kt', 'bco' ],
              [ 'jtl', 'zlm ', 'axew', 'abo' ] ]
    files = []
    for num, text in enumerate(texts):
        f = tmpdir.join('f%d' % num)
        f.write('\n'.join(text))
        files.append(f.strpath)
    cmd1 = grep(regex='^a', f=os.path.join(tmpdir.strpath, '*'), out=dev.itr)
    cmd2 = grep(regex='^a', f=files, out=dev.itr)
    assert list(cmd1) == list(cmd2) == [ 
            '%s: abj' % files[0], 
            '%s: a kt' % files[0], 
            '%s: axew' % files[1], 
            '%s: abo' % files[1]
            ] 
