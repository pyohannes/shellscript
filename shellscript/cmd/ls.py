import os
import sys

from shellscript.proto import Command, OutString, ErrString, resolve


class ls(Command):
    """List directory contents.

    List information about the files (the current directory by default). Sort
    entries alphabetically.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        f: A *str* or a list of *str*. An element is supposed to be a directory
        name and can contain wild cards.
        bool all: Show hidden files.

    Yields:
        shellscript.proto.OutString: A file name.
    """
    def __init__(self, f='.', all=False, *args, **kwargs):
        self._args = dict(
                f=f)
        self._all = all
        super(ls, self).__init__(*args, **kwargs)

    def initialize(self):
        super(ls, self).initialize()
        self._path = [ p for p in resolve(self._args['f']) \
                       if os.path.exists(p) ]
        if not self._path:
            self.stop_with_error('Cannot access %s: No such file or directory'\
                    % self._args['f'], 1)
        if len(self._path) == 1 and os.path.isdir(self._path[0]):
            self._path = os.listdir(self._path[0])
        if self._all:
            self._path.extend([ '.', '..' ])
        self._path.sort()
        self._path.reverse()

    def work(self):
        while True:
            try:
                ret = self._path.pop()
            except IndexError:
                self.stop()
            if not self._all:
                if os.name == 'nt':
                    attrs = ctypes.windll.kernel32.GetFileAttributes(ret)
                    if attrs & (2 | 4):
                        continue
                else:
                    if ret.startswith('.'):
                        continue
            return OutString(ret)
