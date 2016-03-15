from .proto import dev, Command, pipe


def alias(cmd, *alias_args, **alias_kwargs):
    """Define default arguments for *Command*s.

    Parameters:
        *shellscript.Command* cmd: A command class.
        \*alias_args: Default arguments.
        \*\*alias_args: Default keyword arguments.

    Returns:
        *shellscript.Command*: A function that initializes a command.
    """
    def _cmd(*args, **kwargs):
        args = alias_args + args
        kwargs.update(alias_kwargs)
        return cmd(*args, **kwargs)
    return _cmd


def astr(cmd, *args, **kwargs):
    """Return the *stdout* output of *cmd* as string.

    Parameters:
        *shellscript.Command* cmd: A command class.
        \*args: Arguments.
        \*\*args: Keyword arguments.

    Returns:
        *str*: *stdout* of *cmd* as string.
    """
    if 'out' in kwargs:
        out = kwargs['out']
        if isinstance(out, tuple):
            out = pipe(*out)
        if isinstance(kwargs['out'], Command):
            while out.is_opipe:
                out = out._out
            out._out = dev.itr
    else:
        kwargs['out'] = dev.itr
    return str(cmd(*args, **kwargs))


def to_py_str_list(l):
    """Convert a list of *shellscript.proto._BaseString* objects into pure
    Python *str*s.

    The number of elements in both lists may differ, due to the different
    treatment of newlines.

    Parameters:
        [ *shellscript.proto._BaseString* ]: A list of shellscript strings.

    returns:
        [ *str* ]: A list of Python strings.
    """
    ret = [ str(s) for s in l if (s or s.linebreak) ]
    try:
        if l and l[-1].linebreak:
            ret.append('')
    except AttributeError:
        pass
    return ret
