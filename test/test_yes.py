from shellscript import yes, dev


def valid_input(tmpdir):
    return []


def invalid_input(tmpdir):
    return []


def test_yes(tmpdir):
    cmd = yes(out=dev.itr)
    result = []
    for step, output in enumerate(cmd):
        if step >= 50:
            break
        result.append(output)
    assert result == ([ 'y' ]*50)


def test_yes_custom_string(tmpdir):
    s = 'a b c d e f g h'
    cmd = yes(s, out=dev.itr)
    result = []
    for step, output in enumerate(cmd):
        if step >= 50:
            break
        result.append(output)
    assert result == ([ s ]*50)
