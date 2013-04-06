# python import
import re

# cfonb import
from cfonb import parser


HEAD_RE = re.compile(
        r'^%(a)s%(b)s%(c)s%(d)s%(e)s%(f)s%(g)s%(h)s%(i)s%(j)s%(k)s%(l)s%(m)s\n$'
        % {
            'a': '(01)',               # record code
            'b': parser.G_N   % 5,     # bank code
            'c': parser.G__   % 4,     # _
            'd': parser.G_N   % 5,     # desk code
            'e': parser.G_A_  % 3,     # currency code
            'f': parser.G_N_  % 1,     # nb of decimal
            'g': parser.G__   % 1,     # _
            'h': parser.G_AN  % 11,    # account nb
            'i': parser.G__   % 2,     # _
            'j': parser.G_N   % 6,     # previous amount date
            'k': parser.G__   % 50,    # _
            'l': parser.G_AMT,         # previous amount value
            'm': parser.G__   % 16,    # _
            }
        )


[
    H_RECORD_CODE,
    H_BANK_CODE,
    H__1,
    H_DESK_CODE,
    H_CURRENCY_CODE,
    H_NB_OF_DEC,
    H__2,
    H_ACCOUNT_NB,
    H__3,
    H_PREV_DATE,
    H__4,
    H_PREV_AMOUNT,
    H__5,
] = range(13)


HEAD_KEYS = [
    'record_code',
    'bank_code',
    '_1',
    'desk_code',
    'currency_code',
    'nb_of_dec',
    '_2',
    'account_nb',
    '_3',
    'prev_date',
    '_4',
    'prev_amount',
    '_5',
    ]


CONTENT_4_RE = re.compile(
        r'^%(a)s%(b)s%(c)s%(d)s%(e)s%(f)s%(g)s%(h)s%(i)s%(j)s%(k)s%(l)s%(m)s%(n)s%(o)s%(p)s%(q)s%(r)s%(s)s\n$'
        % {
            'a': '(04)',               # record code
            'b': parser.G_N   % 5,     # bank code
            'c': parser.G_AN  % 4,     # internal code
            'd': parser.G_N   % 5,     # desk code
            'e': parser.G_A_  % 3,     # currency code
            'f': parser.G_N_  % 1,     # nb of decimal
            'g': parser.G_AN_ % 1,     # _
            'h': parser.G_AN  % 11,    # account nb
            'i': parser.G_AN  % 2,     # operation code
            'j': parser.G_N   % 6,     # operation date
            'k': parser.G_N_  % 2,     # reject code
            'l': parser.G_N   % 6,     # value date
            'm': parser.G_ALL % 31,    # label
            'n': parser.G_AN_ % 2,     # _
            'o': parser.G_AN   % 7,    # reference in CFONB norme it's G_N
                                       # but in the real world it's an G_AN 
            'p': parser.G_AN_ % 1,     # exempt code
            'q': parser.G_AN_ % 1,     # _
            'r': parser.G_AMT,         # amount
            's': parser.G_AN_ % 16,    # _
            }
        )


[
    _4_RECORD_CODE,
    _4_BANK_CODE,
    _4_INTERNAL_CODE,
    _4_DESK_CODE,
    _4_CURRENCY_CODE,
    _4_NB_OF_DEC,
    _4__1,
    _4_ACCOUNT_NB,
    _4_OPERATION_CODE,
    _4_OPERATION_DATE,
    _4_REJECT_CODE,
    _4_VALUE_DATE,
    _4_LABEL,
    _4__2,
    _4_REFERENCE,
    _4_EXEMPT_CODE,
    _4__3,
    _4_AMOUNT,
    _4__4,
] = range(19)


CONTENT_4_KEYS = [
    'record_code',
    'bank_code',
    'inernal_code',
    'desk_code',
    'currency_code',
    'nb_of_dec',
    '_1',
    'account_nb',
    'operation_code',
    'operation_date',
    'reject_code',
    'value_date',
    'label',
    '_2',
    'reference',
    'exempt_code',
    '_3',
    'amount',
    '_4:',
    ]



CONTENT_5_RE = re.compile(
        r'^%(a)s%(b)s%(c)s%(d)s%(e)s%(f)s%(g)s%(h)s%(i)s%(j)s%(k)s%(l)s%(m)s%(n)s\n$'
        % {
            'a': '(05)',               # record code
            'b': parser.G_N   % 5,     # bank code
            'c': parser.G_AN  % 4,     # internal code
            'd': parser.G_N   % 5,     # desk code
            'e': parser.G_A_  % 3,     # currency code
            'f': parser.G_N_  % 1,     # nb of decimal
            'g': parser.G_AN_ % 1,     # _
            'h': parser.G_AN  % 11,    # account nb
            'i': parser.G_AN  % 2,     # operation code
            'j': parser.G_N   % 6,     # operation date
            'k': parser.G__   % 5,     # _
            'l': parser.G_AN  % 3,     # qualifier
            'm': parser.G_ALL % 70,    # additional info
            'n': parser.G__   % 2,     # _
            }
        )


[
    _5_RECORD_CODE,
    _5_BANK_CODE,
    _5_INTERNAL_CODE,
    _5_DESK_CODE,
    _5_CURRENCY_CODE,
    _5_NB_OF_DEC,
    _5__1,
    _5_ACCOUNT_NB,
    _5_OPERATION_CODE,
    _5_OPERATION_DATE,
    _5__2,
    _5_QUALIFIER,
    _5_ADDITIONAL_INFO,
    _5__3,
] = range(14)


CONTENT_5_KEYS = [
    'record_code',
    'bank_code',
    'inernal_code',
    'desk_code',
    'currency_code',
    'nb_of_dec',
    '_1',
    'account_nb',
    'operation_code',
    'operation_date',
    '_2',
    'qualifier',
    'additional_info',
    '_3',
    ]




FOOT_RE = re.compile(
        r'^%(a)s%(b)s%(c)s%(d)s%(e)s%(f)s%(g)s%(h)s%(i)s%(j)s%(k)s%(l)s%(m)s\n$'
        % {
            'a': '(07)',               # record code
            'b': parser.G_N   % 5,     # bank code
            'c': parser.G__   % 4,     # _
            'd': parser.G_N   % 5,     # desk code
            'e': parser.G_A_  % 3,     # currency code
            'f': parser.G_N_  % 1,     # nb of decimal
            'g': parser.G__   % 1,     # _
            'h': parser.G_AN  % 11,    # account nb
            'i': parser.G__   % 2,     # _
            'j': parser.G_N   % 6,     # next amount date
            'k': parser.G__   % 50,    # _
            'l': parser.G_AMT,         # next amount value
            'm': parser.G__   % 16,    # _
            }
        )


[
    F_RECORD_CODE,
    F_BANK_CODE,
    F__1,
    F_DESK_CODE,
    F_CURRENCY_CODE,
    F_NB_OF_DEC,
    F__2,
    F_ACCOUNT_NB,
    F__3,
    F_NEXT_DATE,
    F__4,
    F_NEXT_AMOUNT,
    F__5,
] = range(13)


FOOT_KEYS = [
    'record_code',
    'bank_code',
    '_1',
    'desk_code',
    'currency_code',
    'nb_of_dec',
    '_2',
    'account_nb',
    '_3',
    'next_date',
    '_4',
    'next_amount',
    '_5',
    ]



class Statement(object):
    """Satement file parser and container. Parse file object to corresponding
    row objects for further use. Offers useful method for reading, writing and
    comparing issues.
    """

    def __init__(self):
        self.header = None
        self.footer   = None
        self.lines  = list()

    def parse_header(self, line):
        self.header = parser.Row(HEAD_RE, HEAD_KEYS, line)

    def parse_footer(self, line):
        self.footer = parser.Row(FOOT_RE, FOOT_KEYS, line)

    def parse_content_4(self, line):
        # init row
        row = parser.Row(CONTENT_4_RE, CONTENT_4_KEYS, line)
        # return initialized row
        return row

    def parse_content_5(self, line):
        """NOT TESTED
        """
        # init row
        row = parser.Row(CONTENT_5_RE, CONTENT_5_KEYS, line)
        # return initialized row
        return row


    def parse(self, file_obj):
        file_lines  = file_obj.readlines()
        # header and footer
        self.parse_header(file_lines.pop(0))
        self.parse_footer(file_lines.pop())

        # content
        for index, line in enumerate(file_lines):
            # parse line
            if CONTENT_4_RE.match(line):
                row = self.parse_content_4(line)
            elif CONTENT_5_RE.match(line):
                row = self.parse_content_5(line)
            else:
                if line[0:2] in ['01', '07']:#we don't take care of subtotal
                    continue
                else:
                    raise parser.ParsingError('line %s is invalid: "%s"' % (index, line))
            # update content
            self.lines.append(row)
