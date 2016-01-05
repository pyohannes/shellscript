"""Global settings.

Attributes:
    prompt_1: A callable that returns the root shell prompt.
    prompt_2: A callable that returns the nested shell prompt.
"""
import os
import socket
import getpass


def _default_prompt(postfix):
    def _wrapper():
        username = getpass.getuser()
        hostname = socket.gethostname().split('.')[0]
        cwd = os.getcwd()
        return '[%s@%s]%s %s' % (username, hostname, cwd, postfix)
    return _wrapper


prompt_1 = _default_prompt('>>> ')
prompt_2 = _default_prompt('... ')
