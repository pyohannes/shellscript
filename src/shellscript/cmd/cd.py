import os
import sys

from shellscript.proto import OnceReturnCommand, resolve, ErrString


class cd(OnceReturnCommand):
    def __init__(self, path=None, *args, **kwargs):
        super(cd, self).__init__(*args, **kwargs)
        self._path = resolve(path)

    def generator_step(self):
        if isinstance(self._path, list) and self._path:
            self._path = self._path[0]
        if not self._path:
            self._path = os.environ.get("HOME")
        try:
            os.chdir(self._path)
        except:
            self.set_error()
            return ErrString(sys.exc_info()[1])
