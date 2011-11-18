# python import
import math

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


def parse_amount(amount_str, nb_of_dec):
    """ return a numerical amount from the cfonb amount string

    >>> from cfonb.parser.common import parse_amount
    >>> parse_amount('0001234{', 2)
    123.4
    >>> parse_amount('0000004843H', 2)
    484.38
    >>> parse_amount('000000920}', 2)
    -92.0
    >>> parse_amount('000117O', 3)
    -1.176
    """
    # insert the comma
    nb_of_dec = int(nb_of_dec)
    amount_str = amount_str[:-nb_of_dec] + '.' + amount_str[-nb_of_dec:]
    # translate the last char and set the sign
    credit_trans = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5',
                    'F': '6', 'G': '7', 'H': '8', 'I': '9', '{': '0'}
    debit_trans  = {'J': '1', 'K': '2', 'L': '3', 'M': '4', 'N': '5',
                    'O': '6', 'P': '7', 'Q': '8', 'R': '9', '}': '0'}
    if amount_str[-1] in debit_trans:
        amount_num = -float(amount_str.replace(amount_str[-1], debit_trans[amount_str[-1]]))
    elif amount_str[-1] in credit_trans:
        amount_num = float(amount_str.replace(amount_str[-1], credit_trans[amount_str[-1]]))
    else:
        raise Exception('Bad amount string')
    return amount_num


def write_amount(amount, nb_of_dec):
    """Returns a cfonb string for a numerical amount.

    >>> from cfonb.parser.common import parse_amount
    >>> write_amount(123.4, 2)
    '0000000001234{'
    >>> write_amount(484.38, 2)
    '0000000004843H'
    >>> write_amount(-92.0, 2)
    '0000000000920}'
    >>> write_amount(-1.176, 3)
    '0000000000117O'
    """
    # split amount, ex.: (123.4, 2) -> dec = 40, num = 123
    dec, num = math.modf(amount)
    num = str(abs(num)).split('.')[0]
    dec = '0' * nb_of_dec if dec == 0\
            else str(abs(dec * math.pow(10, nb_of_dec))).split('.')[0]
    # translate the last char and set the sign
    credit_trans = ['{', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    debit_trans  = ['}', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    # prepare amount
    amount_str = '%s%s' % (num, dec[:-1])
    if amount > 0:
        last_str = credit_trans[int(dec[-1])]
    else:
        last_str = debit_trans[int(dec[-1])]
    # str result
    return (amount_str + last_str).zfill(14)

