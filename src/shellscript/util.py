from .proto import OutString, ErrString, ProtocolError

def com(cmd):
    """Run the given command and return its output.
    """
    out, err = [], []
    for l in cmd:
        if isinstance(l, OutString):
            out.append(l)
        elif isinstance(l, ErrString):
            err.append(l)
        else:
            raise ProtocolError(
                    "Not a valid output or error string: '%s'." % l)
    return out, err
