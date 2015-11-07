# print types
class PrintType:
    def __init__(self, prefix, suffix, color):
        self.prefix = prefix
        self.suffix = suffix
        self.color = color

HEADER = PrintType('', '\n===', '\033[95m')
WHOOPS = PrintType('WHOOPS: ', '', '\033[93m')
FAIL = PrintType('FAIL: ', '', '\033[91m')
NORMAL = PrintType('', '', '\033[0m')
BOLD = PrintType('', '', '\033[1m')


def string(print_string, print_type):
    print print_type.color + print_type.prefix + print_string + print_type.suffix + NORMAL.color


