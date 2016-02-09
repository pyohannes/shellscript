import sys
import time

from shellscript.proto import Command, OutString


class sleep(Command):
    """Delay for a specified amount of time.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        secs: Number of seconds to delay.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """
    def __init__(self, secs=None, *args, **kwargs):
        self._secs = secs
        super(sleep, self).__init__(*args, **kwargs)

    def work(self):
        try:
            time.sleep(self._secs)
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
        self.stop()
