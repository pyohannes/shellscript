import os
import sys
import time

from shellscript.proto import Command, OutString, ErrString, resolve


class touch(Command):
    """Change file timestamps.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        f: The files or list of files to be modified.
        bool nocreate: Do not create any files.
        str time: Which time to change ('access' or 'atime'). Can be a comma 
        separated list.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """

    def __init__(self, f=None, nocreate=False, time=None, *args, **kwargs):
        self._f = f
        self._nocreate = nocreate
        if time:
            self._time = time.split(',')
        else:
            self._time = [ 'access', 'modify' ]
        super(touch, self).__init__(*args, **kwargs)

    def initialize(self):
        super(touch, self).initialize()
        self._flist = resolve(self._f)
        if not self._flist:
            self.stop_with_error('No files given.', 1)

    def work(self):
        t = int(time.time())
        for f in self._flist:
            try:
                if not os.path.exists(f):
                    if not self._nocreate:
                        with open(f, 'w'):
                            pass
                    else:
                        continue
                times_orig = os.stat(f)
                times = (
                        t if 'access' in self._time else times_orig.st_atime,
                        t if 'modify' in self._time else times_orig.st_mtime
                        )
                os.utime(f, times)
            except:
                self.buffer_return(ErrString(sys.exc_info()[1]))
                self.ret = 1
        self.stop()
