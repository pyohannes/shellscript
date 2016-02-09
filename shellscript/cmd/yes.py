import sys
import time

from shellscript.proto import Command, OutString


class yes(Command):
    """Output a string repeatedly until killed.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        s: The string to output, default 'y'.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """
    def __init__(self, s='y', *args, **kwargs):
        self._s = s
        super(yes, self).__init__(*args, **kwargs)

    def work(self):
        return OutString(self._s)
