import os
import sys
import re

from shellscript.proto import Command, OutString, ErrString, resolve
from shellscript.util import InputReader


class grep(Command):
    """Print lines matching a pattern.

    *grep* searches given input files for lines matching the given regular 
    expression.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        regex: A Python regular expression.
        f: A *str* or a list of *str*. An element is supposed to be a file name
        and can contain wild cards.

    Yields:
        shellscript.proto.OutString: Lines matching *regex*.
    """
    def __init__(self, regex=None, f=None, *args, **kwargs):
        self._args = dict(
                regex=regex,
                f=f)
        super(grep, self).__init__(*args, **kwargs)

    def initialize(self):
        try:
            self._regex = re.compile(self._args['regex'])
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
        self._iread = InputReader(self, resolve(self._args['f'] or []))

    @property
    def is_ready(self):
        try:
            return self._iread.is_ready
        except AttributeError:
            return False

    def generator_step(self):
        while True:
            try:
                line = self._iread.get_next_line()
                if self._regex.search(line):
                    if not self._iread.is_ipipe and len(self._iread.files) > 1:
                        return OutString('%s: %s' % 
                                (self._iread.curr_file_name, line))
                    else:
                        return OutString(line)
            except StopIteration:
                self.stop()
            except:
                self.ret = 1
                return ErrString(sys.exc_info()[1])
