import shellscript
from shellscript.proto import OutString, ErrString


# Tests that assure that all shellscript commands correctly implement the
# shellscript protocol.


def _get_test_module_for_command(command):
    return __import__('test_%s' % command.__name__)


def _get_all_commands_and_valid_input():
    for command in shellscript.get_all_commands():
        testmod = _get_test_module_for_command(command)
        for kwargs, inp in testmod.valid_input():
            yield command, kwargs, inp


def assert_proper_out(out):
    for l in list(out): 
        assert isinstance(l, str)
        assert isinstance(l, OutString) or isinstance(l, ErrString)


def test_call():
    # 1. Every command is a Python class.
    for command, _, _ in _get_all_commands_and_valid_input():
        command()

    
def test_valid():
    # 2. Every command constructor accepts an argument called inp.
    # 8. Every command instance has a ret attribute.
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        c = command(inp=inp, **kwargs) 
        assert c.ret == 0 
        assert shellscript.ret() == 0


def test_invalid():
    # 7. A command must not raise an exception
    # 8. Every command instance has a ret attribute.
    for command in shellscript.get_all_commands():
        testmod = _get_test_module_for_command(command)
        for kwargs, inp in testmod.invalid_input():
            c = command(inp=inp, **kwargs)
            assert c.ret != 0
            assert shellscript.ret() != 0 


def test_output():
    # 5. Every command instance is a generator that yields strings.
    # 6. Every string yielded by a command is an instance of OutString or
    #    ErrString.
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        c = command(inp=inp, **kwargs)
        assert_proper_out(c)


def test_endless_input():
    # 3. A command must never try to exhaust the input iterator.
    def endless():
        while True:
            yield 'y'
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        c = command(inp=endless(), **kwargs)
        pass 


def test_invalid_input_iter():
    # 2. The input iterator must be an iterable that yields strings.
    for command, kwargs, inp in _get_all_commands_and_valid_input():
        try:
            c = command(inp=3, **kwargs) 
            assert False
        except:
            pass
