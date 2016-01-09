from .util import com
from .proto import dev

from .cmd.cat import cat
from .cmd.cd import cd
from .cmd.pwd import pwd


def get_all_commands():
    """
    Returns a list of all shellscript command classes.

    """
    return [
            cat, cd, pwd
           ]
