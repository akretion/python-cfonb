# cfonb import
from cfonb.parser import Row, ParsingError


class Statement(object):
    """Satement file parser and container. Parse file object to corresponding
    row objects for further use. Offers useful method for reading, writing and
    comparing issues.
    """

    def __init__(self):
        self.header = None
        self.footer   = None
        self.lines  = list()

    def parse(self, file_obj):
        file_lines  = file_obj.readlines()
        # header and footer
        self.header = Row(file_lines.pop(0))
        self.footer = Row(file_lines.pop())

        if file_lines[0][0:2] != '04':
            raise ParserError('the first line after the header must be a'
                    '04 line. This line is invalid %s'%file_lines[0])
        # content
        for index, line in enumerate(file_lines):
            # parse line
            if line[0:2] == '04':
                row = Row(line)
                self.lines.append(row)
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
            else:
                if line[0:2] in ['01', '07']:#we don't take care of subtotal
                    continue
                else:
                    raise ParsingError('line %s is invalid: "%s"' % (index, line))
