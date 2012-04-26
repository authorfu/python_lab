#!/usr/bin/python
# coding:utf-8

import unittest

from tests import test_storage 

suite = unittest.TestLoader().loadTestsFromModule(test_storage)

unittest.TextTestRunner(verbosity=2).run(suite)
