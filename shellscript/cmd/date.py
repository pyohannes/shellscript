import sys
import time

from shellscript.proto import Command, OutString, ErrString


class date(Command):
    """Print the system date and time.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        *str* fmt: A time.strftime format string.

    Yields:
        shellscript.proto.OutString: The current date time.
    """
    def __init__(self, fmt=None, *args, **kwargs):
        self._fmt = fmt if fmt is not None else '%c'
        super(date, self).__init__(*args, **kwargs)

    def work(self):
        try:
            self.buffer_return(OutString(time.strftime(self._fmt)))
        except:
            self.buffer_return(ErrString(sys.exc_info()[1]))
            self.ret = 1
        self.stop()
