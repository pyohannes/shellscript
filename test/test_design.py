import shellscript
from shellscript.proto import OutString, ErrString, dev
from shellscript.util import to_py_str_list


# Tests that assure that all shellscript commands correctly implement the
# shellscript protocol.


def _get_test_module_for_command(command):
    return __import__('test_%s' % command.__name__)


def _get_all_commands_and_input(tmpdir, inputfunc='valid_input'):
    for command in shellscript.get_all_commands():
        testmod = _get_test_module_for_command(command)
        for setup in getattr(testmod, inputfunc)(tmpdir):
            yield command, setup


def assert_proper_out(out):
    for l in list(out): 
        assert isinstance(l, str)
        assert isinstance(l, OutString) or isinstance(l, ErrString)


def test_call(tmpdir):
    # 1. Every command is a Python class.
    for command, setup in _get_all_commands_and_input(tmpdir):
        command()

    
def test_valid(tmpdir):
    # 2. Every command constructor excepts the arguments *out*, *err* and 
    #    *outerr*.
    # 7. Every command instance has a ret attribute.
    fname = tmpdir.mkdir('test').join('out.txt').strpath
    for command, setup in _get_all_commands_and_input(tmpdir):
        l = []
        with open(fname, 'w') as f:
            for out in (dev.out, dev.err, dev.itr, dev.nul, f, l):
                args, kwargs = setup()
                c = command(*args, out=out, **kwargs) 
                if c.ret is None:
                    list(c)
                assert c.ret == 0 
                args, kwargs = setup()
                c = command(*args, err=out, **kwargs) 
                if c.ret is None:
                    list(c)
                assert c.ret == 0 
                args, kwargs = setup()
                c = command(*args, outerr=out, **kwargs) 
                if c.ret is None:
                    list(c)
                assert c.ret == 0 


def test_invalid(tmpdir):
    # 6. A command must not raise an exception
    # 7. Every command instance has a ret attribute.
    # 8. On error every command generator must yield an ErrString.
    for command, setup in _get_all_commands_and_input(tmpdir, 'invalid_input'):
        args, kwargs = setup()
        c = command(*args, err=dev.itr, **kwargs)
        out = list(c)
        assert c.ret != 0
        assert [ l for l in out if isinstance(l, ErrString) ]


def test_output(tmpdir):
    # 4. Every command instance is a generator that yields strings.
    # 5. Every string yielded by a command is an instance of OutString or
    #    ErrString.
    for command, setup in _get_all_commands_and_input(tmpdir):
        args, kwargs = setup()
        c = command(*args, **kwargs)
        assert_proper_out(c)


def test_generator(tmpdir):
    # 4. Every command instance is a generator that yields strings.
    for command, setup in _get_all_commands_and_input(tmpdir, 'invalid_input'):
        args, kwargs = setup()
        c = command(*args, **kwargs)
        out1 = list(c)
        assert_proper_out(out1)
        args, kwargs = setup()
        out2 = list(c)
        assert_proper_out(out2)
        assert out1 == out2


def test_redirection(tmpdir):
    # 2. Every command constructor excepts the arguments *out*, *err* and 
    #    *outerr*.
    for num, (command, setup) in enumerate(_get_all_commands_and_input(tmpdir)):
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
            args, kwargs = setup()
            c = command(*args, out=f, **kwargs) 
        fobj_content = _read_file(fname)
        # iter
        args, kwargs = setup()
        c = command(*args, out=dev.itr, **kwargs) 
        l = list(c)
        iter_content = to_py_str_list(l)
        # list
        list_content = []
        args, kwargs = setup()
        c = command(*args, out=list_content, **kwargs) 
        list_content = to_py_str_list(list_content)
        # file as string
        fname = tmpdir.join('test_%d_out_fname.txt' % num).strpath
        args, kwargs = setup()
        c = command(*args, out=fname, **kwargs)
        fname_content = _read_file(fname)
        # default redirection
        fname_def = tmpdir.join('test_%d_out_fname_def.txt' % num).strpath
        shellscript.settings.default_out = fname_def
        args, kwargs = setup()
        c = command(*args, **kwargs)
        fname_def_content = _read_file(fname_def)
        assert fobj_content == iter_content == list_content == fname_content \
                == fname_def_content


def test_invalid_output(tmpdir):
    # 2. Every command constructor excepts the arguments *out*, *err* and 
    #    *outerr*.
    for command, setup in _get_all_commands_and_input(tmpdir):
        for arg in ('out', 'err', 'outerr'):
            args, kwargs = setup()
            kwargs = kwargs.copy()
            kwargs[arg] = 3
            try:
                c = command(*args, **kwargs) 
                assert False
            except:
                pass
