# cfonb import
from .common import Row, ParsingError


class StatementReader(object):
    """Statement file parser. Parse file object to corresponding
    row objects for further use. Offers useful method for reading, writing and
    comparing issues.
    """

    def parse(self, file_obj):
        """ Parser a file object and return the list of bank statement
        extracted from the file"""

        file_lines  = file_obj.readlines()
        # content
        result = {}
        for index, line in enumerate(file_lines):

            if line[0:2] == '01':
                row = Row(line)
                
                #If a statement already exist for the same account
                #we updated it else we create a new own
                if result.get(row.account_nb):
                    statement = result[row.account_nb]
                else:
                    statement = Statement()
                    result[row.account_nb] = statement
                    statement.header = row
                    statement.account_nb = row.account_nb

            elif line[0:2] == '04':
                row = Row(line)
                statement.lines.append(row)
            
            elif line[0:2] == '05':
                new_row = Row(line)
                if new_row.get('label') and row.get('label'):
                    index = 0
                    while True:
                        index += 1
                        if not row.get('label_%s'%index):
                            row['label_%s'%index] = new_row.label
                            break
                else:
                    row.update(new_row)

            elif line[0:2] == '07':
                statement.footer = Row(line)
            else:
                raise ParsingError('line %s is invalid: "%s"' % (index, line))

        return [result[key] for key in result]

class Statement(object):

    def __init__(self):
        self.header = None
        self.footer   = None
        self.lines  = list()
        self.account_nb = None


