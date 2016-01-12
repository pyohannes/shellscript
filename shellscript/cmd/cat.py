import os
import sys

from shellscript.proto import Command, OutString, ErrString, resolve
from shellscript.util import InputReader


class cat(Command):
    """Concatenate and print files.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        f: A *str* or a list of *str*. An element is supposed to be a file name
        and can contain wild cards.

    Yields:
        shellscript.proto.OutString: The content of the files.
    """
    def __init__(self, f=None, *args, **kwargs):
        self._args = dict(
                f=f)
        super(cat, self).__init__(*args, **kwargs)

    def initialize(self):
        self._iread = InputReader(self, resolve(self._args['f'] or []))

    def generator_step(self):
        try:
            return OutString(self._iread.get_next_line())
        except StopIteration:
            self.stop()
        except:
            self.ret = 1
            return ErrString(sys.exc_info()[1])
