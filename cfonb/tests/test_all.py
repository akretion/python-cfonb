import unittest
import doctest

# cfonb import
from cfonb.writer import transfert

# cfonb tests import
from cfonb.tests import test_statement
from cfonb.tests import test_transfert

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_statement.suite())
    suite.addTest(test_transfert.suite())
    # doctests
    suite.addTest(doctest.DocTestSuite(transfert,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    return suite
