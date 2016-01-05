from .cmd.cd import cd
from .util import com


def get_all_commands():
    """
    Returns a list of all shellscript command classes.

    """
    return [
            cd
           ]
