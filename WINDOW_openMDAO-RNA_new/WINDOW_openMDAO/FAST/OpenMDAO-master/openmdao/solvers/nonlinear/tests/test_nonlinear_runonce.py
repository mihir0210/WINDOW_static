"""Test the NonlinearRunOnce linear solver class."""

import unittest

from openmdao.api import Problem, ScipyKrylov, IndepVarComp, Group, ExplicitComponent, \
     AnalysisError, ParallelGroup, ExecComp
from openmdao.solvers.nonlinear.nonlinear_runonce import NonlinearRunOnce
from openmdao.test_suite.components.ae_tests import AEComp, AEDriver
from openmdao.test_suite.components.paraboloid import Paraboloid
from openmdao.test_suite.groups.parallel_groups import ConvergeDivergeGroups
from openmdao.utils.assert_utils import assert_rel_error
from openmdao.utils.mpi import MPI

try:
    from openmdao.vectors.petsc_vector import PETScVector
except ImportError:
    PETScVector = None


class TestNonlinearRunOnceSolver(unittest.TestCase):

    def test_converge_diverge_groups(self):
        # Test derivatives for converge-diverge-groups topology.
        prob = Problem()
        model = prob.model = ConvergeDivergeGroups()

        model.linear_solver = ScipyKrylov()
        model.nonlinear_solver = NonlinearRunOnce()

        model.g1.nonlinear_solver = NonlinearRunOnce()
        model.g1.g2.nonlinear_solver = NonlinearRunOnce()
        model.g3.nonlinear_solver = NonlinearRunOnce()

        prob.set_solver_print(level=0)
        prob.setup(check=False, mode='fwd')
        prob.run_model()

        # Make sure value is fine.
        assert_rel_error(self, prob['c7.y1'], -102.7, 1e-6)

    def test_undeclared_options(self):
        # Test that using options that should not exist in class cause an error
        solver = NonlinearRunOnce()

        msg = "\"Option '%s' cannot be set because it has not been declared.\""

        for option in ['atol', 'rtol', 'maxiter', 'err_on_maxiter']:
            with self.assertRaises(KeyError) as context:
                solver.options[option] = 1

            self.assertEqual(str(context.exception), msg % option)

    def test_feature_solver(self):
        from openmdao.api import Problem, Group, NonlinearRunOnce, IndepVarComp
        from openmdao.test_suite.components.paraboloid import Paraboloid

        prob = Problem()
        model = prob.model

        model.add_subsystem('p1', IndepVarComp('x', 0.0), promotes=['x'])
        model.add_subsystem('p2', IndepVarComp('y', 0.0), promotes=['y'])
        model.add_subsystem('comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])

        model.nonlinear_solver = NonlinearRunOnce()

        prob.setup(check=False, mode='fwd')

        prob['x'] = 4.0
        prob['y'] = 6.0

        prob.run_model()

        assert_rel_error(self, prob['f_xy'], 122.0)


@unittest.skipUnless(PETScVector, "PETSc is required.")
class TestNonlinearRunOnceSolverMPI(unittest.TestCase):

    N_PROCS = 2

    @unittest.skipUnless(MPI, "MPI is not active.")
    def test_reraise_analylsis_error(self):
        prob = Problem()
        model = prob.model

        model.add_subsystem('p1', IndepVarComp('x', 0.5))
        model.add_subsystem('p2', IndepVarComp('x', 3.0))
        sub = model.add_subsystem('sub', ParallelGroup())

        sub.add_subsystem('c1', AEComp())
        sub.add_subsystem('c2', AEComp())

        model.add_subsystem('obj', ExecComp(['val = x1 + x2']))

        model.connect('p1.x', 'sub.c1.x')
        model.connect('p2.x', 'sub.c2.x')
        model.connect('sub.c1.y', 'obj.x1')
        model.connect('sub.c2.y', 'obj.x2')

        prob.driver = AEDriver()

        prob.setup(check=False)

        handled = prob.run_driver()
        self.assertTrue(handled)


if __name__ == "__main__":
    unittest.main()
