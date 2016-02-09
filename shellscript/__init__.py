from .proto import dev
from .util import alias

from .cmd.cat import cat
from .cmd.cd import cd
from .cmd.grep import grep
from .cmd.ls import ls
from .cmd.pwd import pwd
from .cmd.run import run
from .cmd.sleep import sleep


def get_all_commands():
    """
    Returns a list of all shellscript command classes.

    """
    return [
            cat, cd, grep, ls, pwd, run, sleep
           ]
