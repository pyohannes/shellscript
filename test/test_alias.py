from shellscript import alias, cd


def valid_input(tmpdir):

    yield dict(cmd=cd, all=True)


def invalid_input(tmpdir):

    yield dict()


def test_ls_all(tmpdir):
    d = os.path.dirname(__file__)
    lsall = alias(ls, all=True)
    assert list(ls(out=dev.itr)) == list(lsall())
