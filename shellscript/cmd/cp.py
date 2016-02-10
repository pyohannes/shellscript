import os
import shutil
import sys

from shellscript.proto import Command, OutString


class cp(Command):
    """Copy *src* to *dst*.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        src: The source file or source directory.
        dst: The destination file or directory name.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """

    def __init__(self, src=None, dst=None, *args, **kwargs):
        self._src = src
        self._dst = dst
        super(cp, self).__init__(*args, **kwargs)

    def initialize(self):
        super(cp, self).initialize()
        if not self._src:
            self.stop_with_error('No source given.', 1)
        if not self._dst:
            self.stop_with_error('No destination given.', 1)

    def work(self):
        try:
            if os.path.isdir(self._src):
                pass
            elif os.path.isfile(self._src):
                dstfile = self._dst
                if os.path.isdir(self._dst):
                    dstfile = os.path.join(self._dst, os.path.basename(self._src))
                shutil.copyfile(self._src, dstfile)
            else:
                self.stop_with_error('No such file or directory: %s' %
                        self._src, 1)
        except StopIteration:
            raise
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
        self.stop()
