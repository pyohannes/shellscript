from .proto import dev


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
    kwargs['out'] = dev.itr
    return str(cmd(*args, **kwargs))
