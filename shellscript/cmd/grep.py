import os
import sys
import re

from shellscript.proto import Command, OutString, ErrString, resolve


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
        self._args=dict(
                regex=regex,
                f=f)
        super(grep, self).__init__(*args, **kwargs)

    def initialize(self):
        try:
            self._regex = re.compile(self._args['regex'])
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
        self._files = resolve(self._args['f'] or [])
        self._active_file = None
        self._pos = 0
        self._print_names = len(self._files) > 1

    @property
    def is_ready(self):
        try:
            return self._files or self.is_input_piped
        except AttributeError: 
            return False

    def generator_step(self):
        if not self.is_input_piped and not self._active_file:
            if self._pos >= len(self._files):
                self.stop()
            else:
                pos = self._pos
                self._pos += 1
                try:
                    self._active_file = open(self._files[pos])
                except:
                    self.ret = 1
                    return ErrString(sys.exc_info()[1])
        while True:
            try:
                if self.is_input_piped:
                    line = self._inp.__next__(from_out=True).strip('\n')
                else:
                    line = self._active_file.__next__().strip('\n')
                if self._regex.search(line):
                    if self._print_names:
                        return OutString('%s: %s' % (self._files[self._pos-1], line))
                    else:
                        return OutString(line)
            except StopIteration:
                if self._active_file:
                    self._active_file.close()
                    self._active_file = None
                    return self.generator_step()
                else:
                    self.stop()
