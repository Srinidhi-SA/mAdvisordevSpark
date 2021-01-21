from __future__ import absolute_import

from unittest import TestLoader
from unittest import TestSuite

from . import test_column

def suite():
    return TestSuite((TestLoader().loadTestsFromTestCase(test_column.TestColumnType),))

