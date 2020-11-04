"""Test the LinearRunOnce linear solver class."""

import unittest

from openmdao.api import Problem, Group, IndepVarComp
from openmdao.utils.assert_utils import assert_rel_error
from openmdao.solvers.linear.linear_runonce import LinearRunOnce
from openmdao.test_suite.components.paraboloid import Paraboloid
from openmdao.test_suite.groups.parallel_groups import ConvergeDivergeGroups


class TestLinearRunOnceSolver(unittest.TestCase):

    def test_converge_diverge_groups(self):
        # Test derivatives for converge-diverge-groups topology.
        prob = Problem()
        model = prob.model = ConvergeDivergeGroups()

        model.linear_solver = LinearRunOnce()
        model.g1.linear_solver = LinearRunOnce()
        model.g1.g2.linear_solver = LinearRunOnce()
        model.g3.linear_solver = LinearRunOnce()

        prob.set_solver_print(level=0)
        prob.setup(check=False, mode='fwd')
        prob.run_model()

        wrt = ['iv.x']
        of = ['c7.y1']

        # Make sure value is fine.
        assert_rel_error(self, prob['c7.y1'], -102.7, 1e-6)

        J = prob.compute_totals(of=of, wrt=wrt, return_format='flat_dict')
        assert_rel_error(self, J['c7.y1', 'iv.x'][0][0], -40.75, 1e-6)

        prob.setup(check=False, mode='rev')
        prob.run_model()

        J = prob.compute_totals(of=of, wrt=wrt, return_format='flat_dict')
        assert_rel_error(self, J['c7.y1', 'iv.x'][0][0], -40.75, 1e-6)

    def test_undeclared_options(self):
        # Test that using options that should not exist in class cause an error
        solver = LinearRunOnce()

        msg = "\"Option '%s' cannot be set because it has not been declared.\""

        for option in ['atol', 'rtol', 'maxiter', 'err_on_maxiter']:
            with self.assertRaises(KeyError) as context:
                solver.options[option] = 1

            self.assertEqual(str(context.exception), msg % option)


    def test_feature_solver(self):
        from openmdao.api import Problem, Group, IndepVarComp, LinearRunOnce
        from openmdao.test_suite.components.paraboloid import Paraboloid

        prob = Problem()
        model = prob.model

        model.add_subsystem('p1', IndepVarComp('x', 0.0), promotes=['x'])
        model.add_subsystem('p2', IndepVarComp('y', 0.0), promotes=['y'])
        model.add_subsystem('comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])

        model.linear_solver = LinearRunOnce()

        prob.setup(check=False, mode='fwd')

        prob.run_model()

        of = ['f_xy']
        wrt = ['x', 'y']
        derivs = prob.compute_totals(of=of, wrt=wrt, return_format='dict')

        assert_rel_error(self, derivs['f_xy']['x'], [[-6.0]], 1e-6)
        assert_rel_error(self, derivs['f_xy']['y'], [[8.0]], 1e-6)


if __name__ == "__main__":
    unittest.main()
