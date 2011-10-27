# python import - http://docs.python.org/library/unittest.html
import unittest
from StringIO import StringIO

# import cfonb module
from cfonb.parser import Row, ParsingError, statement as p


HEAD_LINE = '0130002    00447     0000888899H  160811                                                  0000000132303H                '


HEAD_VALUES = [
    '01',
    '30002',
    '    ',
    '00447',
    '   ',
    ' ',
    ' ',
    '0000888899H',
    '  ',
    '160811',
    '                                                  ',
    '0000000132303H',
    '                ',
    ]


CONTENT_4_LINE = '0430002013400447EUR2E0000431040H21210811  210811VIREMENT COMBELL                 0000000  0000000020000}                '

CONTENT_4_VALUES = [
    '04',
    '30002',
    '0134',
    '00447',
    'EUR',
    '2',
    'E',
    '0000431040H',
    '21',
    '210811',
    '  ',
    '210811',
    'VIREMENT COMBELL               ',
    '  ',
    '0000000',
    ' ',
    ' ',
    '0000000020000}',
    '                ',
    ]


FOOT_LINE = '0730002    00447     0000888899H  280911                                                  0000000118711D                '


FOOT_VALUES = [
    '07',
    '30002',
    '    ',
    '00447',
    '   ',
    ' ',
    ' ',
    '0000888899H',
    '  ',
    '280911',
    '                                                  ',
    '0000000118711D',
    '                ',
    ]


class TestStatement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_head(self):
        row = p.parse_head(HEAD_LINE)
        # little type check
        self.assertIsInstance(row, Row, 'invalid row type: %s' % type(row))
        # list copy for check
        list_1 = row.as_list()[:]
        list_2 = row.as_dict().values()[:]
        # sort list to be compared
        list_1.sort()
        list_2.sort()
        # list check
        self.assertEqual(list_1, list_2)
        # check dict and obj format
        for i in range(13):
            self.assertEqual(row.as_list()[i], getattr(row.as_obj(), p.HEAD_KEYS[i]))
            self.assertEqual(row.as_list()[i], HEAD_VALUES[i])

    def test_parse_content_4(self):
        row = p.parse_content_4(CONTENT_4_LINE)
        # little type check
        self.assertIsInstance(row, Row, 'invalid row type: %s' % type(row))
        # list copy for check
        list_1 = row.as_list()[:]
        list_2 = row.as_dict().values()[:]
        # sort list to be compared
        list_1.sort()
        list_2.sort()
        # list check
        self.assertEqual(list_1, list_2)
        # check dict and obj format
        for i in range(19):
            self.assertEqual(row.as_list()[i], getattr(row.as_obj(), p.CONTENT_4_KEYS[i]))
            self.assertEqual(row.as_list()[i], CONTENT_4_VALUES[i])

    def test_parse_footer(self):
        row = p.parse_footer(FOOT_LINE)
        # little type check
        self.assertIsInstance(row, Row, 'invalid row type: %s' % type(row))
        # list copy for check
        list_1 = row.as_list()[:]
        list_2 = row.as_dict().values()[:]
        # sort list to be compared
        list_1.sort()
        list_2.sort()
        # list check
        self.assertEqual(list_1, list_2)
        # check dict and obj format
        for i in range(13):
            self.assertEqual(row.as_list()[i], getattr(row.as_obj(), p.FOOT_KEYS[i]))
            self.assertEqual(row.as_list()[i], FOOT_VALUES[i])

    def test_statement(self):
        # prepare file obj
        file_obj = StringIO()
        file_obj.write("%s\n" % HEAD_LINE)
        file_obj.write("%s\n" % CONTENT_4_LINE)
        file_obj.write("%s\n" % FOOT_LINE)
        file_obj.seek(0)
        # init statement
        statement = p.Statement()
        statement.parse(file_obj)
        # prepare values to compare
        header_line = p.parse_head(HEAD_LINE)
        content_line = p.parse_content_4(CONTENT_4_LINE)
        footer_line = p.parse_footer(FOOT_LINE)
        # some tests
        self.assertIsInstance(statement, p.Statement)
        self.assertIsInstance(statement.header, Row)
        self.assertIsInstance(statement.footer, Row)
        self.assertIsInstance(statement.lines, list)
        self.assertEqual(len(statement.lines), 1)
        self.assertIsInstance(statement.lines[0], Row)
        self.assertEqual(statement.header, header_line)
        self.assertEqual(statement.footer, footer_line)
        self.assertEqual(statement.lines[0], content_line)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestStatement('test_parse_head'))
    suite.addTest(TestStatement('test_parse_content_4'))
    suite.addTest(TestStatement('test_parse_footer'))
    suite.addTest(TestStatement('test_statement'))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(suite())
