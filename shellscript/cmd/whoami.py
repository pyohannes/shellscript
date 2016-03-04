import getpass

from shellscript.proto import Command, OutString


class whoami(Command):
    """Print the user name associated with the current effective user ID.

    ret is set to 0 on success and to 1 on failure.

    Yields:
        shellscript.proto.OutString: The name of the current user.
    """

    def work(self):
        self.buffer_return(OutString(getpass.getuser()))
        self.stop()
