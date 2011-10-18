import unittest

from cfonb.tests import test_statement
from cfonb.tests import test_transfert

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_statement.suite())
    suite.addTest(test_transfert.suite())
    return suite
