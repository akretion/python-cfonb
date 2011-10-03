
G__ = r'( {%d})'

G_N = r'(\d{%d})'
G_N_ = r'([0-9 ]{%d})'

G_A = r'(\w{%d})'
G_A_ = r'([a-zA-Z ]{%d})'

G_AN = r'([a-zA-Z0-9]{%d})'
G_AN_ = r'([a-zA-Z0-9 ]{%d})'

G_AMT = r'(\d{13}[{}A-R]{1})'


class ParsingError(Exception):
    """
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Obj():
    """
    """

    def __init__(self, **entries):
        """
        """
        self.__dict__.update(entries)


class Row(object):
    """
    """

    def __init__(self):
        """
        """
        self.__dict = dict()
        self.__obj = None
        self.__db_id = None

    def parse(self, re, keys, line):
        """
        """
        # do re match
        match = re.match(line)
        # re check
        if match is None:
            raise ParsingError('line is invalid: "%s"' % line)
        else:
            self.__list = list(match.groups())
            self.__dict = dict(zip(keys, self.__list))
            self.__obj = Obj(**self.__dict)
            # TODO add in memory entry and keep id
            self.__db_id = None

    def as_list(self):
        return self.__list

    def as_dict(self):
        return self.__dict

    def as_obj(self):
        return self.__obj
