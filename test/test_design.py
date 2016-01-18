import shellscript
from shellscript.proto import OutString, ErrString, dev


# Tests that assure that all shellscript commands correctly implement the
# shellscript protocol.


def _get_test_module_for_command(command):
    return __import__('test_%s' % command.__name__)


def _get_all_commands_and_input(tmpdir, inputfunc='valid_input'):
    for command in shellscript.get_all_commands():
        testmod = _get_test_module_for_command(command)
        for kwargs in getattr(testmod, inputfunc)(tmpdir):
            yield command, kwargs


def assert_proper_out(out):
    for l in list(out): 
        assert isinstance(l, str)
        assert isinstance(l, OutString) or isinstance(l, ErrString)


def test_call(tmpdir):
    # 1. Every command is a Python class.
    for command, _ in _get_all_commands_and_input(tmpdir):
        command()

    
def test_valid(tmpdir):
    # 2. Every command constructor excepts the arguments *out*, *err* and 
    #    *outerr*.
    # 7. Every command instance has a ret attribute.
    fname = tmpdir.mkdir('test').join('out.txt').strpath
    for command, kwargs in _get_all_commands_and_input(tmpdir):
        l = []
        with open(fname, 'w') as f:
            for out in (dev.out, dev.err, dev.itr, dev.nul, f, l):
                c = command(out=out, **kwargs) 
                list(c)
                assert c.ret == 0 
                c = command(err=out, **kwargs) 
                list(c)
                assert c.ret == 0 
                c = command(outerr=out, **kwargs) 
                list(c)
                assert c.ret == 0 


def test_invalid(tmpdir):
    # 6. A command must not raise an exception
    # 7. Every command instance has a ret attribute.
    # 8. On error every command generator must yield an ErrString.
    for command, kwargs in _get_all_commands_and_input(tmpdir, 'invalid_input'):
        c = command(err=dev.itr, **kwargs)
        out = list(c)
        assert c.ret != 0
        assert [ l for l in out if isinstance(l, ErrString) ]


def test_output(tmpdir):
    # 4. Every command instance is a generator that yields strings.
    # 5. Every string yielded by a command is an instance of OutString or
    #    ErrString.
    for command, kwargs in _get_all_commands_and_input(tmpdir):
        c = command(**kwargs)
        assert_proper_out(c)


def test_generator(tmpdir):
    # 4. Every command instance is a generator that yields strings.
    for command, kwargs in _get_all_commands_and_input(tmpdir, 'invalid_input'):
        c = command(**kwargs)
        out1 = list(c)
        assert_proper_out(out1)
        out2 = list(c)
        assert_proper_out(out2)
        assert out1 == out2


def test_redirection(tmpdir):
    # 2. Every command constructor excepts the arguments *out*, *err* and 
    #    *outerr*.
    for num, (command, kwargs) in enumerate(_get_all_commands_and_input(tmpdir)):
        def _read_file(fname):
            with open(fname, 'r') as f:
                file_content = f.read()
                if file_content:
                    return file_content.split('\n')
                else:
                    return []
        # file
        fname = tmpdir.join('test_%d_out_fobj.txt' % num).strpath
        with open(fname, 'w') as f:
            c = command(out=f, **kwargs) 
        fobj_content = _read_file(fname)
        # iter
        c = command(out=dev.itr, **kwargs) 
        iter_content = list(c)
        # list
        list_content = []
        c = command(out=list_content, **kwargs) 
        # file as string
        fname = tmpdir.join('test_%d_out_fname.txt' % num).strpath
        c = command(out=fname, **kwargs)
        fname_content = _read_file(fname)
        assert fobj_content == iter_content == list_content == fname_content


def test_invalid_output(tmpdir):
    # 2. Every command constructor excepts the arguments *out*, *err* and 
    #    *outerr*.
    for command, kwargs in _get_all_commands_and_input(tmpdir):
        for arg in ('out', 'err', 'outerr'):
            args = kwargs.copy()
            args[arg] = 3
            try:
                c = command(**kwargs) 
                assert False
            except:
                pass
