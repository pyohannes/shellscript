import sys
import time

from shellscript.proto import Command, InputReaderMixin, OutString, ErrString,\
                              resolve


class tee(Command, InputReaderMixin):
    """Read from standard input and write to standard output and files.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        f: The destination files, or a list of those.
        bool append: Append to given files, do not overwrite.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """
    def __init__(self, f=None, append=False, *args, **kwargs):
        self._f = f
        self._append = append
        super(tee, self).__init__(*args, **kwargs)


    def initialize(self):
        super(tee, self).initialize()
        flags = 'w' if not self._append else 'a'
        fs = resolve(self._f)
        if fs:
            self._fobjs = [ open(f, flags) for f in resolve(self._f) ]
        else:
            self._fobjs = None
        self._first_line = True
        self.initialize_input([])

    def finalize(self):
        if self._fobjs:
            for f in self._fobjs:
                f.close()

    def work(self):
        try:
            l = self.get_input_line()
            if self._fobjs:
                for f in self._fobjs:
                    if not self._first_line:
                        f.write('\n')
                    f.write(l)
                self._first_line = False
            else:
                self.buffer_return(OutString(l))
            return OutString(l)
        except StopIteration:
            raise
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
