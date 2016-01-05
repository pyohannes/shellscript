import os
import sys

from shellscript.proto import Command, resolve


class cd(Command):
    """Change the current working directory to path. The variable HOME is the 
    default path.

    ret is set 0 on success and 1 on failure.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """

    def __init__(self, path=None, *args, **kwargs):
        super(cd, self).__init__(*args, **kwargs)
        self._path = resolve(path)

    def generator_step(self):
        if isinstance(self._path, list) and self._path:
            self._path = self._path[0]
        if not self._path:
            if not 'HOME' in os.environ:
                self.stop_with_error('$HOME cannot be determined.', 1)
            else:
                self._path = os.environ["HOME"]
        try:
            os.chdir(self._path)
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
        self.stop()
