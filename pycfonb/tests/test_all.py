import unittest

from pycfonb.tests import test_statement

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_statement.suite())
    return suite
