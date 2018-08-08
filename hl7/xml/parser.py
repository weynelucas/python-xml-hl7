from .containers import Message


def parse(line):
    """
    Returns a instance of the `hl7.Message` that allows
    indexed access to the data elements.
    """
    return Message(line)