# python import
import re
from collections import OrderedDict
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

# http://www.cfonb.org/Web/cfonb/cfonbmain.nsf/DocumentsByIDWeb/7JSHS5/$File/7-8%20Evolution%20Releve%20Comptes%20120%20caracteres%20operations%20virement%20et%20prelevement%20sepa%20V2_0_2010_03.pdf
ADDITIONAL_INFO = {
   "NPY": OrderedDict([
        ('debtor_name',                 parser.G_ALL %70),
    ]),
    "IPY": OrderedDict([
        ('debtor_id',                   parser.G_ALL %35),
        ('debtor_id_type',              parser.G_ALL %35),
    ]),
    "NBE": OrderedDict([
        ('creditor_name',               parser.G_ALL %70),
    ]),
    "IBE": OrderedDict([
        ('creditor_id',                 parser.G_ALL %35),
        ('creditor_id_type',            parser.G_ALL %35),
    ]),
    "NPO": OrderedDict([
        ('ultimate_debtor_name',        parser.G_ALL %70),
    ]),
    "IPO": OrderedDict([
        ('ultimate_debtor_id',          parser.G_ALL %35),
        ('ultimate_debtor_type',        parser.G_ALL %35),
    ]),
    "NBU": OrderedDict([
        ('ultimate_creditor_name',      parser.G_ALL %70),
    ]),
    "IBU": OrderedDict([
        ('ultimate_creditor_id',        parser.G_ALL %35),
        ('ultimate_creditor_type',      parser.G_ALL %35),
    ]),
    "LCC": OrderedDict([
        ('remittance_information_1',    parser.G_ALL %70),
    ]),
    "LC2": OrderedDict([
        ('remittance_information_2',    parser.G_ALL %70),
    ]),
    "LCS": OrderedDict([
        ('creditor_ref_information',    parser.G_ALL %70),
    ]),
    "RCN": OrderedDict([
        ('end2end_identification',      parser.G_ALL %35),
        ('purpose',                     parser.G_ALL %35),
    ]),
    "RCN": OrderedDict([
        ('payment_infor_id',            parser.G_ALL %35),
        ('instruction_id',              parser.G_ALL %35),
    ]),
 
#Specific to bank transfers
    "MMO": OrderedDict([
        ('currency_code',               parser.G_AN  %3),
        ('nb_of_dec_amount',            parser.G_N   %1),
        ('equivalent_amount',           parser.G_N_  %14),
        ('nb_of_dec_exchange_rate',     parser.G_N_  %2),
        ('exchange_rate',               parser.G_N_  %11),
        ('_',                           parser.G_AN_ %39)
    ]),
    "CBE": OrderedDict([
        ('creditor_account',            parser.G_ALL %70),
    ]),   


#specific to withdrawal
# TODO FIXME it's look like there is something wrong in 
# confb norme indeed 35+4 != 70 and 35 != 70 :S outch!
#    "RUM": OrderedDict([
#        ('mandate_identification',      parser.G_ALL %35),
#        ('sequence_type',               parser.G_ALL %4),
#    ]),
#    "CPY": OrderedDict([
#        ('debtor_account',              parser.G_ALL %35),
#    ]),
#    
}  
   
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

    def parser_sub_content_5(self, row):
        regex = r''
        keys = []
        for key, value in ADDITIONAL_INFO[row.qualifier].iteritems():
            regex += value
            keys += [key]
        reg = re.compile(regex + r'$')
        match = reg.match(row.additional_info)
        # re check
        if match is None:
            import pdb; pdb.set_trace()
            raise parser.ParsingError('line is invalid: "%s"' % row.additional_info)
        else:
            res = dict(zip(keys, list(match.groups())))
            import pdb; pdb.set_trace()
            return res

    def parse_content_5(self, previous_row, line):
        """NOT TESTED
        """
        # init row
        row = parser.Row(CONTENT_5_RE, CONTENT_5_KEYS, line)
        # return initialized row
        if row.qualifier == 'LIB':
            index = 0
            while True:
                index += 1
                if not previous_row.get('LIB_%s'%index):
                    previous_row['LIB_%s'%index] = row.additional_info.strip()
                    break
        else:
            previous_row.update(self.parser_sub_content_5(row))
        #return sub_content

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
                self.lines.append(row)
            elif CONTENT_5_RE.match(line):
                self.parse_content_5(row, line)
            else:
                if line[0:2] in ['01', '07']:#we don't take care of subtotal
                    continue
                else:
                    raise parser.ParsingError('line %s is invalid: "%s"' % (index, line))
            # update content
