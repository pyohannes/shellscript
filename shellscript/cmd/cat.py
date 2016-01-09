import os
import sys

from shellscript.proto import Command, OutString, ErrString, resolve


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
        self._files = resolve(f or [])
        self._active_file = None
        self._pos = 0
        super(cat, self).__init__(*args, **kwargs)

    def generator_step(self):
        if not self._active_file:
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
        try:
            return OutString(self._active_file.__next__().strip('\n'))
        except StopIteration:
            self._active_file.close()
            self._active_file = None
            return self.generator_step()
