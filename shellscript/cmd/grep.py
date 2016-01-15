import os
import sys
import re

from shellscript.proto import Command, OutString, ErrString, resolve
from shellscript.util import InputReaderMixin


class grep(Command, InputReaderMixin):
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
        self.initialize_input(resolve(self._args['f'] or []))

    def work(self):
        while True:
            try:
                line = self.get_input_line()
                if self._regex.search(line):
                    if not self.is_ipipe and self.len_input_files > 1:
                        return OutString('%s: %s' % 
                                (self.curr_input_file_name, line))
                    else:
                        return OutString(line)
            except StopIteration:
                self.stop()
            except:
                self.ret = 1
                return ErrString(sys.exc_info()[1])
