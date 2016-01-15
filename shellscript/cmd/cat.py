import os
import sys

from shellscript.proto import Command, OutString, ErrString, resolve
from shellscript.util import InputReaderMixin


class cat(Command, InputReaderMixin):
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
        self.initialize_input(resolve(self._args['f'] or []))

    def work(self):
        try:
            return OutString(self.get_input_line())
        except StopIteration:
            self.stop()
        except:
            self.ret = 1
            return ErrString(sys.exc_info()[1])
