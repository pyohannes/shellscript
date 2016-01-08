from .cmd.cd import cd
from .cmd.pwd import pwd
from .util import com
from .proto import dev


def get_all_commands():
    """
    Returns a list of all shellscript command classes.

    """
    return [
            cd, pwd
           ]
