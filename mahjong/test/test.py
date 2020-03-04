
# -*- coding: utf-8 -*-
import sys

import unittest
sys.path.append("..")
sys.path.append("../../")

test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern="tests_*.py")

runner = unittest.TextTestRunner()

runner.run(discover)



