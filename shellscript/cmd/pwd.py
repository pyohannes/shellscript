import os

from shellscript.proto import Command, OutString


class pwd(Command):
    """Print the full filename of the current working directory.

    ret is set to 0 on success and to 1 on failure.

    Yields:
        shellscript.proto.OutString: The current working directory.
    """

    def generator_step(self):
        self.buffer_return(OutString(os.getcwd()))
        self.stop()
