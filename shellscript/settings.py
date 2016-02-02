"""Global settings.

Attributes:
    prompt_1: A callable that returns the root shell prompt.
    prompt_2: A callable that returns the nested shell prompt.
"""
import imp
import getpass
import os
import socket
import sys
import tempfile


def load():
    rc = os.environ.get('SHELLSCRIPTRC')
    if not rc and 'HOME' in os.environ:
        rc = os.path.join(os.environ['HOME'], '.shellscriptrc')
    if rc:
        try:
            tmpf = tempfile.mktemp()
            with open(tmpf, 'w') as f:
                f.write('from shellscript import *\n')
                with open(rc, 'r') as frc:
                    f.write(frc.read())
            return imp.load_source('shellscript.custom_settings', tmpf)
        except:
            sys.stderr.write('%s\n' % sys.exc_info()[1])
        finally:
            if os.path.exists(tmpf):
                os.remove(tmpf)
    return None


def _default_prompt(postfix):
    def _wrapper():
        username = getpass.getuser()
        hostname = socket.gethostname().split('.')[0]
        cwd = os.getcwd()
        return '[%s@%s]%s %s' % (username, hostname, cwd, postfix)
    return _wrapper


prompt_1 = _default_prompt('>>> ')
prompt_2 = _default_prompt('... ')
