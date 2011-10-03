
# blank only rule
G__ = r'( {%d})'

# numeric or numeric|blank only rule
G_N = r'(\d{%d})'
G_N_ = r'([0-9 ]{%d})'

# alpha or alpha|blank only rule
G_A = r'(\w{%d})'
G_A_ = r'([a-zA-Z ]{%d})'

# alphanum or alphanum|blank only rule
G_AN = r'([a-zA-Z0-9]{%d})'
G_AN_ = r'([a-zA-Z0-9 ]{%d})'

# cfonb amount rule
G_AMT = r'(\d{13}[{}A-R]{1})'


class ParsingError(Exception):
    """Simple parsing Exception for the module.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Obj():
    """Generic object build from a given dict.
    """

    def __init__(self, **entries):
        """Create real object based on passed dict.
        """
        self.__dict__.update(entries)


class Row(object):
    """Generic row object to manage bank file parsing, compare and reading.
    """

    def __init__(self):
        """Empty all at start.
        """
        self.empty()

    def empty(self):
        """Initializes values to their default values.
        """
        self.line_nb = None
        self.__list  = dict()
        self.__dict  = dict()
        self.__obj   = None
        self.__db_id = None

    def parse(self, re, keys, line, line_nb=None):
        """Parses flat line according re rules, line and additional info.

        :param re: regular expression to match with
        :param keys: keys values to build dict and object variables for the row
        :param line: the flat line to be parsed
        :param line_nb: optional info to keep index in the original file
        """
        # do re match
        match = re.match(line)
        # re check
        if match is None:
            self.empty()
            raise ParsingError('line is invalid: "%s"' % line)
        else:
            self.line_nb = line_nb
            self.__list = list(match.groups())
            self.__dict = dict(zip(keys, self.__list))
            self.__obj = Obj(**self.__dict)

    def as_list(self):
        return self.__list

    def as_dict(self):
        return self.__dict

    def as_obj(self):
        return self.__obj

    def __str__(self) :
        return str(self.__dict)

    def __eq__(self, other) :
        return self.__dict == other.__dict
