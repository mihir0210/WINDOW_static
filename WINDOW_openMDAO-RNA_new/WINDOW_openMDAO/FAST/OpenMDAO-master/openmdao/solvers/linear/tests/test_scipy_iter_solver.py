"""Test the ScipyKrylov linear solver class."""

from __future__ import division, print_function

from six import iteritems
import unittest

import numpy as np

from openmdao.api import Group, IndepVarComp, Problem, ExecComp, NonlinearBlockGS, BoundsEnforceLS
from openmdao.solvers.linear.linear_block_gs import LinearBlockGS
from openmdao.solvers.linear.scipy_iter_solver import ScipyKrylov, ScipyIterativeSolver
from openmdao.solvers.nonlinear.newton import NewtonSolver
from openmdao.solvers.linear.tests.linear_test_base import LinearSolverTests
from openmdao.test_suite.components.expl_comp_simple import TestExplCompSimpleDense
from openmdao.test_suite.components.misc_components import Comp4LinearCacheTest
from openmdao.test_suite.components.sellar import SellarDis1withDerivatives, SellarDis2withDerivatives
from openmdao.test_suite.groups.implicit_group import TestImplicitGroup
from openmdao.utils.assert_utils import assert_rel_error, assert_warning


# use this to fake out the TestImplicitGroup so it'll use the solver we want.
def krylov_factory(solver):
    def f(junk=None):
        return ScipyKrylov(solver=solver)
    return f


class TestScipyKrylov(LinearSolverTests.LinearSolverTestCase):

    linear_solver_name = 'gmres'
    linear_solver_class = krylov_factory('gmres')

    def test_options(self):
        """Verify that the SciPy solver specific options are declared."""

        group = Group()
        group.linear_solver = self.linear_solver_class()

        self.assertEqual(group.linear_solver.options['solver'], self.linear_solver_name)

    def test_solve_linear_scipy(self):
        """Solve implicit system with ScipyKrylov."""

        # use ScipyIterativeSolver here to check for deprecation warning and verify that the deprecated
        # class still gets the right answer without duplicating this test.
        msg = "ScipyIterativeSolver is deprecated.  Use ScipyKrylov instead."

        with assert_warning(DeprecationWarning, msg):
            group = TestImplicitGroup(lnSolverClass=lambda : ScipyIterativeSolver(solver=self.linear_solver_name))

        p = Problem(group)
        p.setup(check=False)
        p.set_solver_print(level=0)

        # Conclude setup but don't run model.
        p.final_setup()

        d_inputs, d_outputs, d_residuals = group.get_linear_vectors()

        # forward
        d_residuals.set_const(1.0)
        d_outputs.set_const(0.0)
        group.run_solve_linear(['linear'], 'fwd')
        output = d_outputs._data
        assert_rel_error(self, output, group.expected_solution, 1e-15)

        # reverse
        d_outputs.set_const(1.0)
        d_residuals.set_const(0.0)
        group.run_solve_linear(['linear'], 'rev')
        output = d_residuals._data
        assert_rel_error(self, output, group.expected_solution, 1e-15)

    def test_solve_linear_scipy_maxiter(self):
        """Verify that ScipyKrylov abides by the 'maxiter' option."""

        group = TestImplicitGroup(lnSolverClass=self.linear_solver_class)
        group.linear_solver.options['maxiter'] = 2

        p = Problem(group)
        p.setup(check=False)
        p.set_solver_print(level=0)

        # Conclude setup but don't run model.
        p.final_setup()

        d_inputs, d_outputs, d_residuals = group.get_linear_vectors()

        # forward
        d_residuals.set_const(1.0)
        d_outputs.set_const(0.0)
        group.run_solve_linear(['linear'], 'fwd')

        self.assertTrue(group.linear_solver._iter_count == 2)

        # reverse
        d_outputs.set_const(1.0)
        d_residuals.set_const(0.0)
        group.run_solve_linear(['linear'], 'rev')

        self.assertTrue(group.linear_solver._iter_count == 2)

    def test_solve_on_subsystem(self):
        """solve an implicit system with GMRES attached to a subsystem"""

        p = Problem()
        model = p.model = Group()
        dv = model.add_subsystem('des_vars', IndepVarComp())
        # just need a dummy variable so the sizes don't match between root and g1
        dv.add_output('dummy', val=1.0, shape=10)

        grp = TestImplicitGroup(lnSolverClass=self.linear_solver_class)
        g1 = model.add_subsystem('g1', grp)

        p.setup(check=False)

        p.set_solver_print(level=0)

        # Conclude setup but don't run model.
        p.final_setup()

        # forward
        d_inputs, d_outputs, d_residuals = g1.get_linear_vectors()

        d_residuals.set_const(1.0)
        d_outputs.set_const(0.0)
        g1.run_solve_linear(['linear'], 'fwd')

        output = d_outputs._data
        assert_rel_error(self, output, g1.expected_solution, 1e-15)

        # reverse
        d_inputs, d_outputs, d_residuals = g1.get_linear_vectors()

        d_outputs.set_const(1.0)
        d_residuals.set_const(0.0)
        g1.linear_solver._linearize()
        g1.run_solve_linear(['linear'], 'rev')

        output = d_residuals._data
        assert_rel_error(self, output, g1.expected_solution, 3e-15)

    def test_preconditioner_deprecation(self):

        group = TestImplicitGroup(lnSolverClass=self.linear_solver_class)

        msg = "The 'preconditioner' property provides backwards compatibility " \
            + "with OpenMDAO <= 1.x ; use 'precon' instead."

        # check deprecation on setter & getter
        with assert_warning(DeprecationWarning, msg):
            group.linear_solver.preconditioner = LinearBlockGS()

        with assert_warning(DeprecationWarning, msg):
            group.linear_solver.preconditioner

    def test_linear_solution_cache(self):
        # Test derivatives across a converged Sellar model. When caching
        # is performed, the second solve takes less iterations than the
        # first one.

        # Forward mode

        prob = Problem()
        model = prob.model

        model.add_subsystem('px', IndepVarComp('x', 1.0), promotes=['x'])
        model.add_subsystem('d1', Comp4LinearCacheTest(), promotes=['x', 'y'])

        model.nonlinear_solver = NonlinearBlockGS()
        model.linear_solver = ScipyKrylov()

        model.add_design_var('x', cache_linear_solution=True)
        model.add_objective('y', cache_linear_solution=True)

        prob.setup(mode='fwd')
        prob.set_solver_print(level=0)
        prob.run_model()

        J = prob.driver._compute_totals(of=['y'], wrt=['x'], global_names=False, return_format='flat_dict')
        icount1 = prob.model.linear_solver._iter_count
        J = prob.driver._compute_totals(of=['y'], wrt=['x'], global_names=False, return_format='flat_dict')
        icount2 = prob.model.linear_solver._iter_count

        # Should take less iterations when starting from previous solution.
        self.assertTrue(icount2 < icount1)

        # Reverse mode

        prob = Problem()
        model = prob.model

        model.add_subsystem('px', IndepVarComp('x', 1.0), promotes=['x'])
        model.add_subsystem('d1', Comp4LinearCacheTest(), promotes=['x', 'y'])

        model.nonlinear_solver = NonlinearBlockGS()
        model.linear_solver = ScipyKrylov()

        model.add_design_var('x', cache_linear_solution=True)
        model.add_objective('y', cache_linear_solution=True)

        prob.setup(mode='rev')
        prob.set_solver_print(level=0)
        prob.run_model()

        J = prob.driver._compute_totals(of=['y'], wrt=['x'], global_names=False, return_format='flat_dict')
        icount1 = prob.model.linear_solver._iter_count
        J = prob.driver._compute_totals(of=['y'], wrt=['x'], global_names=False, return_format='flat_dict')
        icount2 = prob.model.linear_solver._iter_count

        # Should take less iterations when starting from previous solution.
        self.assertTrue(icount2 < icount1)


class TestScipyKrylovFeature(unittest.TestCase):

    def test_feature_simple(self):
        """Tests feature for adding a Scipy GMRES solver and calculating the
        derivatives."""
        from openmdao.api import Problem, Group, IndepVarComp, ScipyKrylov
        from openmdao.test_suite.components.expl_comp_simple import TestExplCompSimpleDense

        # Tests derivatives on a simple comp that defines compute_jacvec.
        prob = Problem()
        model = prob.model
        model.add_subsystem('x_param', IndepVarComp('length', 3.0),
                            promotes=['length'])
        model.add_subsystem('mycomp', TestExplCompSimpleDense(),
                            promotes=['length', 'width', 'area'])

        model.linear_solver = ScipyKrylov()
        prob.set_solver_print(level=0)

        prob.setup(check=False, mode='fwd')
        prob['width'] = 2.0
        prob.run_model()

        of = ['area']
        wrt = ['length']

        J = prob.compute_totals(of=of, wrt=wrt, return_format='flat_dict')
        assert_rel_error(self, J['area', 'length'][0][0], 2.0, 1e-6)

    def test_specify_solver(self):
        import numpy as np

        from openmdao.api import Problem, Group, IndepVarComp, ScipyKrylov, \
             NonlinearBlockGS, ExecComp
        from openmdao.test_suite.components.sellar import SellarDis1withDerivatives, \
             SellarDis2withDerivatives

        prob = Problem()
        model = prob.model

        model.add_subsystem('px', IndepVarComp('x', 1.0), promotes=['x'])
        model.add_subsystem('pz', IndepVarComp('z', np.array([5.0, 2.0])), promotes=['z'])

        model.add_subsystem('d1', SellarDis1withDerivatives(), promotes=['x', 'z', 'y1', 'y2'])
        model.add_subsystem('d2', SellarDis2withDerivatives(), promotes=['z', 'y1', 'y2'])

        model.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                z=np.array([0.0, 0.0]), x=0.0),
                            promotes=['obj', 'x', 'z', 'y1', 'y2'])

        model.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'), promotes=['con1', 'y1'])
        model.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'), promotes=['con2', 'y2'])

        model.nonlinear_solver = NonlinearBlockGS()

        model.linear_solver = ScipyKrylov()

        prob.setup()
        prob.run_model()

        wrt = ['z']
        of = ['obj']

        J = prob.compute_totals(of=of, wrt=wrt, return_format='flat_dict')
        assert_rel_error(self, J['obj', 'z'][0][0], 9.61001056, .00001)
        assert_rel_error(self, J['obj', 'z'][0][1], 1.78448534, .00001)

    def test_feature_maxiter(self):
        import numpy as np

        from openmdao.api import Problem, Group, IndepVarComp, ScipyKrylov, NonlinearBlockGS, ExecComp
        from openmdao.test_suite.components.sellar import SellarDis1withDerivatives, SellarDis2withDerivatives

        prob = Problem()
        model = prob.model

        model.add_subsystem('px', IndepVarComp('x', 1.0), promotes=['x'])
        model.add_subsystem('pz', IndepVarComp('z', np.array([5.0, 2.0])), promotes=['z'])

        model.add_subsystem('d1', SellarDis1withDerivatives(), promotes=['x', 'z', 'y1', 'y2'])
        model.add_subsystem('d2', SellarDis2withDerivatives(), promotes=['z', 'y1', 'y2'])

        model.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                z=np.array([0.0, 0.0]), x=0.0),
                            promotes=['obj', 'x', 'z', 'y1', 'y2'])

        model.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'), promotes=['con1', 'y1'])
        model.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'), promotes=['con2', 'y2'])

        model.nonlinear_solver = NonlinearBlockGS()

        model.linear_solver = ScipyKrylov()
        model.linear_solver.options['maxiter'] = 3

        prob.setup()
        prob.run_model()

        wrt = ['z']
        of = ['obj']

        J = prob.compute_totals(of=of, wrt=wrt, return_format='flat_dict')
        assert_rel_error(self, J['obj', 'z'][0][0], 0.0, .00001)
        assert_rel_error(self, J['obj', 'z'][0][1], 0.0, .00001)

    def test_feature_atol(self):
        import numpy as np

        from openmdao.api import Problem, Group, IndepVarComp, ScipyKrylov, NonlinearBlockGS, ExecComp
        from openmdao.test_suite.components.sellar import SellarDis1withDerivatives, SellarDis2withDerivatives

        prob = Problem()
        model = prob.model

        model.add_subsystem('px', IndepVarComp('x', 1.0), promotes=['x'])
        model.add_subsystem('pz', IndepVarComp('z', np.array([5.0, 2.0])), promotes=['z'])

        model.add_subsystem('d1', SellarDis1withDerivatives(), promotes=['x', 'z', 'y1', 'y2'])
        model.add_subsystem('d2', SellarDis2withDerivatives(), promotes=['z', 'y1', 'y2'])

        model.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                z=np.array([0.0, 0.0]), x=0.0),
                            promotes=['obj', 'x', 'z', 'y1', 'y2'])

        model.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'), promotes=['con1', 'y1'])
        model.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'), promotes=['con2', 'y2'])

        model.nonlinear_solver = NonlinearBlockGS()

        model.linear_solver = ScipyKrylov()
        model.linear_solver.options['atol'] = 1.0e-20

        prob.setup()
        prob.run_model()

        wrt = ['z']
        of = ['obj']

        J = prob.compute_totals(of=of, wrt=wrt, return_format='flat_dict')
        assert_rel_error(self, J['obj', 'z'][0][0], 9.61001055699, .00001)
        assert_rel_error(self, J['obj', 'z'][0][1], 1.78448533563, .00001)

    def test_specify_precon(self):
        import numpy as np

        from openmdao.api import Problem, ScipyKrylov, NewtonSolver, LinearBlockGS, \
             DirectSolver

        from openmdao.test_suite.components.double_sellar import DoubleSellar

        prob = Problem(model=DoubleSellar())
        model = prob.model

        model.nonlinear_solver = NewtonSolver()
        model.nonlinear_solver.linesearch = BoundsEnforceLS()
        model.linear_solver = ScipyKrylov()
        model.g1.linear_solver = DirectSolver()
        model.g2.linear_solver = DirectSolver()

        model.linear_solver.precon = LinearBlockGS()
        # TODO: This should work with 1 iteration.
        #model.linear_solver.precon.options['maxiter'] = 1

        prob.setup()
        prob.set_solver_print(level=2)
        prob.run_model()

        assert_rel_error(self, prob['g1.y1'], 0.64, .00001)
        assert_rel_error(self, prob['g1.y2'], 0.80, .00001)
        assert_rel_error(self, prob['g2.y1'], 0.64, .00001)
        assert_rel_error(self, prob['g2.y2'], 0.80, .00001)


if __name__ == "__main__":
    unittest.main()
