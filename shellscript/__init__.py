from .proto import dev
from .util import alias

from .cmd.cat import cat
from .cmd.cd import cd
from .cmd.cp import cp
from .cmd.grep import grep
from .cmd.ls import ls
from .cmd.mv import mv
from .cmd.pwd import pwd
from .cmd.rm import rm
from .cmd.run import run
from .cmd.sleep import sleep
from .cmd.touch import touch
from .cmd.yes import yes


def get_all_commands():
    """
    Returns a list of all shellscript command classes.

    """
    return [
            cat, cp, cd, grep, ls, mv, pwd, rm, run, sleep, touch, yes
           ]
