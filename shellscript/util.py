from .proto import OutString, ErrString, ProtocolError


class InputReader(object):
    """
    """

    def __init__(self, obj, files):
        self._obj = obj
        self.files = files
        self._active_file = None
        self._pos = -1

    @property
    def curr_file_name(self):
        if self.is_ipipe:
            return '<input>'
        else:
            return self.files[self._pos]

    @property
    def is_ready(self):
        return len(self.files) or self.is_ipipe

    @property
    def is_ipipe(self):
        return self._obj.is_input_piped

    def get_next_line(self):
        if self.is_ipipe:
            return self._obj._inp.__next__(from_out=True).strip('\n')

        if not self._active_file:
            self._pos += 1
            if self._pos >= len(self.files):
                raise StopIteration
            else:
                self._active_file = open(self.files[self._pos])
        try:
            return self._active_file.__next__().strip('\n')
        except StopIteration:
            self._active_file.close()
            self._active_file = None
            return self.get_next_line()

