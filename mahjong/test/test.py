
# -*- coding: utf-8 -*-
import unittest


test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern="tests_*.py")

runner = unittest.TextTestRunner()

runner.run(discover)



