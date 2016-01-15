from .proto import OutString, ErrString, ProtocolError


class InputReaderMixin(object):
    """
    """

    def initialize_input(self, files):
        self._input_files = files
        self._active_input_file = None
        self._input_files_pos = -1

    @property
    def curr_input_file_name(self):
        if self.is_ipipe:
            return '<input>'
        else:
            return self._input_files[self._input_files_pos]

    @property
    def len_input_files(self):
        return len(self._input_files)

    @property
    def is_ready(self):
        mixinready = len(self._input_files) or self.is_ipipe
        return mixinready and super(self, InputReaderMixin).is_ready

    def get_input_line(self):
        if self.is_ipipe:
            return self._inp.get_line().strip('\n')

        if not self._active_input_file:
            self._input_files_pos += 1
            if self._input_files_pos >= len(self._input_files):
                raise StopIteration
            else:
                self._active_input_file = open(self._input_files[self._input_files_pos])
        try:
            return self._active_input_file.__next__().strip('\n')
        except StopIteration:
            self._active_input_file.close()
            self._active_input_file = None
            return self.get_input_line()

