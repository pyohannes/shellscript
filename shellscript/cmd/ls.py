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
        bool indicator_slash: Prepend directories with a slash.

    Yields:
        shellscript.proto.OutString: A file name.
    """
    def __init__(self, f='.', all=False, indicator_slash=False, *args, **kwargs):
        self._args = dict(
                f=f)
        self._all = all
        self._indicator_slash = indicator_slash
        super(ls, self).__init__(*args, **kwargs)

    def initialize(self):
        super(ls, self).initialize()
        self._path = [ p for p in resolve(self._args['f']) \
                       if os.path.exists(p) ]
        self._path_root = None
        if not self._path:
            self.stop_with_error('Cannot access %s: No such file or directory'\
                    % self._args['f'], 1)
        if len(self._path) == 1 and os.path.isdir(self._path[0]):
            self._path_root = self._path[0]
            self._path = os.listdir(self._path_root)
        if self._all:
            self._path.extend([ '.', '..' ])
        self._path.sort()
        self._path.reverse()

    def _get_absolute_path(self, p):
        if self._path_root:
            return os.path.abspath(os.path.join(self._path_root, p))
        else:
            return os.path.abspath(p)

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
            if self._indicator_slash and \
                    os.path.isdir(self._get_absolute_path(ret)):
                ret += '/'
            return OutString(ret)
