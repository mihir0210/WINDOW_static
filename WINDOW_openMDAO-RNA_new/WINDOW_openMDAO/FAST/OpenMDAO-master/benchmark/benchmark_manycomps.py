
import unittest

from openmdao.api import Problem, Group
from openmdao.test_suite.build4test import DynComp, create_dyncomps


class BM(unittest.TestCase):
    """Setup of models with lots of components"""

    def benchmark_100(self):
        p = Problem()
        create_dyncomps(p.model, 100, 10, 10, 5)
        p.setup(check=False)
        p.final_setup()

    def benchmark_500(self):
        p = Problem()
        create_dyncomps(p.model, 500, 10, 10, 5)
        p.setup(check=False)
        p.final_setup()

    def benchmark_1K(self):
        p = Problem()
        create_dyncomps(p.model, 1000, 10, 10, 5)
        p.setup(check=False)
        p.final_setup()
