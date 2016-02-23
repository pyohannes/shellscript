import os
import shutil
import sys

from shellscript.proto import Command, OutString, ErrString, resolve


class mv(Command):
    """Move (rename) files.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        src: The source file or source directory, or a list of those.
        dst: The destination file or directory name.
        bool verbose: Print verbose output.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """

    def __init__(self, src=None, dst=None, verbose=False, *args, **kwargs):
        self._src = src
        self._dst = dst
        self._verbose = verbose
        super(mv, self).__init__(*args, **kwargs)

    def initialize(self):
        super(mv, self).initialize()
        self._srclist = resolve(self._src)
        self._dstlist = resolve(self._dst)
        if not self._srclist:
            self.stop_with_error('No source given.', 1)
        if not self._dstlist:
            self.stop_with_error('No destination given.', 1)
        if len(self._dstlist) > 1:
            self.stop_with_error('Multiple destinations given.', 1)
        if len(self._srclist) > 1 and not os.path.isdir(self._dstlist[0]):
            self.stop_with_error("Target '%s' is not a directory" %
                    self._dstlist[0] , 1)

    def _verbose_output(self, src, dst):
        self.buffer_return(OutString("`%s' -> `%s'" % (src, dst)))

    def work(self):
        for src in self._srclist:
            dst = self._dstlist[0]
            if os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))
            try:
                shutil.move(src, dst)
                if self._verbose:
                    self._verbose_output(src, dst)
            except:
                self.buffer_return(ErrString(sys.exc_info()[1]))
                self.ret = 1
        self.stop()
