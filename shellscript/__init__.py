from .proto import dev

from .cmd.alias import alias
from .cmd.cat import cat
from .cmd.cd import cd
from .cmd.grep import grep
from .cmd.ls import ls
from .cmd.pwd import pwd


def get_all_commands():
    """
    Returns a list of all shellscript command classes.

    """
    return [
            alias, cat, cd, grep, ls, pwd
           ]
