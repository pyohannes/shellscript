import shellscript


def _get_test_module_for_command(command):
    return __import__('test_%s' % command.__name__)


def _get_all_commands_and_valid_input():
    for command in shellscript.get_all_commands():
        testmod = _get_test_module_for_command(command)
        for kwargs, inp in testmod.valid_input():
            yield command, kwargs, inp


def assert_proper_out(out):
    for l in list(out): # P4
        assert isinstance(l, str) # P5


def test_call():
    for command, _, _ in _get_all_commands_and_valid_input():
        command() # P6, P1

    
def test_valid():
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        c = command(inp=inp, **kwargs) # P2
        assert c.ret == 0 # P9
        assert shellscript.ret() == 0 # P10


def test_invalid():
    for command in shellscript.get_all_commands():
        testmod = _get_test_module_for_command(command)
        for kwargs, inp in testmod.invalid_input():
            c = command(inp=inp, **kwargs) # P6
            assert c.ret != 0 # P9
            assert shellscript.ret() != 0 # P10


def test_output():
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        c = command(inp=inp, **kwargs)
        assert_proper_out(c) # P4, P5


def test_endless_input():
    def endless():
        while True:
            yield 'y'
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        c = command(inp=endless(), **kwargs)
        pass # P7


def test_invalid_input_iter():
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        try:
            c = command(inp=3, **kwargs) # P3
            assert False
        except:
            pass


def test_communicate():
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        out, err = shellscript.com(command(inp=inp, **kwargs)) # P8
        assert_proper_out(out)
        assert_proper_out(err)
