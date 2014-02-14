# python import
from datetime import datetime
import math
import re

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

# all
G_ALL = r'(.{%d})'


class ParsingError(Exception):
    """Simple parsing Exception for the module.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Row(dict):
    """Generic row object to manage bank file parsing, compare and reading.
    """

    def __init__(self, line):
        """Parses flat line according re rules, line and additional info.

        :param re: regular expression to match with
        :param keys: keys values to build dict and object variables for the row
        :param line: the flat line to be parsed
        """
        # do re match
        parser = Parser.get_parser(line[0:2])
        self.update(parser().parse(line))
        
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value 


class Parser(object):
    """ Parser method for reading bank statement line """
    @classmethod
    def get_parser(cls, key):
        for sub_cls in cls.__subclasses__():
            if sub_cls._code == key:
               return sub_cls
        raise Exception('No class found for key %s'%key)

    def __init__(self):
        self._regex 
        regex = r''
        keys = []
        self.size = 0
        for key, value, size in self._regex:
            self.size += size
            if '%d' in value:
                regex += value % size
            else:
                regex += value
            keys += [key]
        self.re = re.compile(regex + r'$')
        self.keys = keys

    def _post(self, res):
        for key in res:
            if key not in ['qualifier', 'additional_info']:
                res[key] = res[key].strip()
        return res



    def parse(self, line):
        if line[-1] == "\n":
            line = line[:-1]
        if len(line) != self.size:
            raise ParsingError("Invalid line: %s. the len should be %s"
                               "instead of %s"%self.size, len(line))
        match = self.re.match(line)
        # re check
        if match is None:
            message= ''
            index = 0
            for key, value, size in self._regex:
                pattern = '%d' in value and value % size or value
                if not re.match(pattern, line[:size]):
                    message += ("The key %s in position %s with the pattern %s"
                                "do not match with %s\n"
                                %(key, index, pattern, line[:size]))
                index += size
                line = line[size:]
            raise ParsingError("Invalid line: %s. Please read detail"
                               "message\n %s" %(line, message))
        else:
            res = dict(zip(self.keys, list(match.groups())))
            return self._post(res)

# http://www.cfonb.org/Web/cfonb/cfonbmain.nsf/DocumentsByIDWeb/7JSHS5/$File/7-8%20Evolution%20Releve%20Comptes%20120%20caracteres%20operations%20virement%20et%20prelevement%20sepa%20V2_0_2010_03.pdf

class ParserContent01(Parser):
    _code = '01'
    _regex = [
        ('record_code',     '(01)',  2),
        ('bank_code',       G_N,     5),
        ('_1',              G__,     4),
        ('desk_code',       G_N,     5),
        ('currency_code',   G_A_,    3),
        ('nb_of_dec',       G_N_,    1),
        ('_2',              G__,     1),
        ('account_nb',      G_AN,   11),
        ('_3',              G__,     2),
        ('prev_date',       G_N,     6),
        ('_4',              G__,    50),
        ('prev_amount',     G_AMT,  14),
        ('_5',              G_ALL,  16),
     ]

    def _post(self, res):
        res = super(ParserContent01, self)._post(res)
        res.update({
            'prev_amount': parse_amount(res['prev_amount'], res['nb_of_dec']),
            'prev_date': parse_date(res['prev_date']),
        })
        return res

class ParserContent04(Parser):
    _code = '04'
    _regex = [
        ('record_code',     '(04)',  2),
        ('bank_code',       G_N,     5),
        ('internal_code',   G_AN,    4),
        ('desk_code',       G_N,     5),
        ('currency_code',   G_A_,    3),
        ('nb_of_dec',       G_N_,    1),
        ('_1',              G_ALL,   1),
        ('account_nb',      G_AN,   11),
        ('operation_code',  G_AN,    2),
        ('operation_date',  G_N,     6),
        ('reject_code',     G_N_,    2), 
        ('value_date',      G_N,     6),
        ('label',           G_ALL,  31),
        ('_2',              G_ALL,   2),
        ('reference',       G_ALL,   7),
        ('exempt_code',     G_ALL,   1),
        ('_3',              G_ALL,   1),
        ('amount',          G_AMT,  14), 
        ('_4:',             G_ALL,  16),
    ]

    def _post(self, res):
        res = super(ParserContent04, self)._post(res)
        res.update({
            'amount': parse_amount(res['amount'], res['nb_of_dec']),
            'value_date': parse_date(res['value_date']),
            'operation_date': parse_date(res['operation_date']),
        })
        return res



class ParserContent05(Parser):
    _code = '05'
    _regex = [
        ('record_code',     '(05)',  2),
        ('bank_code',       G_N,     5),
        ('internal_code',   G_AN,    4),
        ('desk_code',       G_N,     5),
        ('currency_code',   G_A_,    3),
        ('nb_of_dec',       G_N_,    1),
        ('_1',              G_AN_,   1),
        ('account_nb',      G_AN,   11),
        ('operation_code',  G_AN,    2),
        ('operation_date',  G_N,     6),
        ('_2',              G__,     5),
        ('qualifier',       G_AN,    3),
        ('additional_info', G_ALL,  70),
        ('_3',              G__,     2),
    ] 

    def parse(self, line):
        result = super(ParserContent05, self).parse(line)
        parser = Parser.get_parser(result['qualifier'])
        new_result = parser().parse(result['additional_info'])
        return new_result

    
class ParserContent07(Parser):
    _code = '07'
    _regex = [
        ('record_code',     '(07)',  2),
        ('bank_code',       G_N,     5),
        ('_1',              G__,     4),
        ('desk_code',       G_N,     5),
        ('currency_code',   G_A_,    3),
        ('nb_of_dec',       G_N_,    1),
        ('_2',              G__,     1),
        ('account_nb',      G_AN,   11),
        ('_3',              G__,     2),
        ('next_date',       G_N,     6),
        ('_4',              G__,    50),
        ('next_amount',     G_AMT,  14),
        ('_5',              G__,    16),
    ]
    
    def _post(self, res):
        res = super(ParserContent07, self)._post(res)
        res.update({
            'next_amount': parse_amount(res['next_amount'], res['nb_of_dec']),
            'next_date': parse_date(res['next_date']),
        })
        return res


class ParserLIB(Parser):
    _code = "LIB"
    _regex = [
        ('label', G_ALL, 70),
    ]


class ParserNPY(Parser):
    _code = "NPY"
    _regex = [
        ('debtor_name', G_ALL, 70),
    ]


class ParserIPY(Parser):
    _code = 'IPY'
    _regex = [
        ('debtor_id',       G_ALL, 35),
        ('debtor_id_type',  G_ALL, 35),
    ]


class ParserNBE(Parser):
    _code = 'NBE'
    _regex = [
        ('creditor_name',   G_ALL, 70),
    ]


class ParserIBE(Parser):
    _code = 'IBE'
    _regex = [
        ('creditor_id',         G_ALL, 35),
        ('creditor_id_type',    G_ALL, 35),
    ]


class ParserNPO(Parser):
    _code = 'NPO'
    _regex = [
        ('ultimate_debtor_name',    G_ALL, 70),
    ]


class ParserIPO(Parser):
    _code = 'IPO'
    _regex = [
        ('ultimate_debtor_id',      G_ALL, 35),
        ('ultimate_debtor_type',    G_ALL, 35),
    ]


class ParserNBU(Parser):
    _code = 'NBU'
    _regex = [
        ('ultimate_creditor_name',  G_ALL, 70),
    ]


class ParserIBU(Parser):
    _code = 'IBU'
    _regex = [
        ('ultimate_creditor_id',    G_ALL, 35),
        ('ultimate_creditor_type',  G_ALL, 35),
    ]


class ParserLCC(Parser):
    _code = 'LCC'
    _regex = [
        ('remittance_information_1',    G_ALL, 70),
    ]


class ParserLC2(Parser):
    _code = 'LC2'
    _regex = [
        ('remittance_information_2',    G_ALL, 70),
    ]


class ParserLCS(Parser):
    _code = 'LCS'
    _regex = [
        ('creditor_ref_information',    G_ALL, 70),
    ]


class ParserRCN(Parser):
    _code = 'RCN'
    _regex = [
        ('end2end_identification',  G_ALL, 35),
        ('purpose',                 G_ALL, 35),
    ]


class ParserRCN(Parser):
    _code = 'RCN'
    _regex = [
        ('payment_infor_id',    G_ALL, 35),
        ('instruction_id',      G_ALL, 35),
    ]
 

#Specific to bank transfers
class ParserMMO(Parser):
    _code = 'MMO'
    _regex = [
        ('currency_code',               G_AN,   3),
        ('nb_of_dec_amount',            G_N,    1),
        ('equivalent_amount',           G_N_,  14),
        ('nb_of_dec_exchange_rate',     G_N_,   2),
        ('exchange_rate',               G_N_,  11),
        ('_',                           G_AN_, 39)
    ]

    def _post(self, res):
        res = super(ParserMMO, self)._post(res)
        res['equivalent_amount'] = float(res['equivalent_amount'])\
                                        /float(res['nb_of_dec_amount'])
        if res['exchange_rate']:
            res['exchange_rate']=  float(res['exchange_rate'])\
                                        /float(res['nb_of_dec_exchange_rate'])
        return res



class ParserCBE(Parser):
    _code = 'CBE'
    _regex = [
        ('creditor_account',    G_ALL, 70),
    ]


##### TODO FIXME this 3 new parser are introduced by the new sepa norme but
# you know administration is an administration and so the spec for the norme
# are somewhere but I still not suceed to get it, I send an email to the CFONB
# and I wait for the norme. For now I just process the line like that.

#Still no news of the administration
#It seem that the norm allow bank to add what they want very usefull norm ;)
#By chance the next norme will may be fix the format.
#Indeed next norme is "format camt.05". I ask the Cfonb organisation to know when the bank will start to use
#this new format but ... they don't know ;)

class ParserREF(Parser):
    _code = 'REF'
    _regex = [
        ('ref', G_ALL, 70),
    ]

class ParserBDB(Parser):
    _code = 'BDB'
    _regex = [
        ('bdb', G_ALL, 70),
    ]

class ParserLEM(Parser):
    _code = 'LEM'
    _regex = [
        ('lem', G_ALL, 70),
    ]

class ParserPDO(Parser):
    _code = 'PDO'
    _regex = [
        ('pdo', G_ALL, 70),
    ]



#specific to withdrawal
# TODO FIXME it's look like there is something wrong in 
# confb norme indeed 35+4 != 70 and 35 != 70 :S outch!
#class ParserRUM(Parser):
#    _code = 'RUM'
#    _regex = [
#        ('mandate_identification',  G_ALL %35),
#        ('sequence_type',           G_ALL %4),
#    ]
#
#class ParserCPY(Parser):
#    _code = 'CPY'
#    _regex = [
#        ('debtor_account',  G_ALL %35),
#    ]
#

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

def parse_date(date):
    return datetime.strptime(date, '%d%m%y').strftime('%Y-%m-%d')

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

