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
        args = args + alias_args
        kwargs.update(alias_kwargs)
        return cmd(*args, **kwargs)
    return _cmd
