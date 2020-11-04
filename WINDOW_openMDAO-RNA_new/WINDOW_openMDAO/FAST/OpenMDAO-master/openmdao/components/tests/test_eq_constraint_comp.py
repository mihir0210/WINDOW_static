import unittest

import numpy as np

from openmdao.api import Problem, Group, IndepVarComp, ExecComp, \
    EQConstraintComp, ScipyOptimizeDriver

from openmdao.test_suite.components.sellar import \
    SellarDis1withDerivatives, SellarDis2withDerivatives

from openmdao.utils.assert_utils import assert_rel_error, assert_check_partials
from numpy.testing import assert_almost_equal


class SellarIDF(Group):
    """
    Individual Design Feasible (IDF) architecture for the Sellar problem.
    """
    def setup(self):
        # construct the Sellar model with `y1` and `y2` as independent variables
        dv = IndepVarComp()
        dv.add_output('x', 5.)
        dv.add_output('y1', 5.)
        dv.add_output('y2', 5.)
        dv.add_output('z', np.array([2., 0.]))

        self.add_subsystem('dv', dv)
        self.add_subsystem('d1', SellarDis1withDerivatives())
        self.add_subsystem('d2', SellarDis2withDerivatives())

        self.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                           x=0., z=np.array([0., 0.])))

        self.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'))
        self.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'))

        self.connect('dv.x', ['d1.x', 'obj_cmp.x'])
        self.connect('dv.y1', ['d2.y1', 'obj_cmp.y1', 'con_cmp1.y1'])
        self.connect('dv.y2', ['d1.y2', 'obj_cmp.y2', 'con_cmp2.y2'])
        self.connect('dv.z', ['d1.z', 'd2.z', 'obj_cmp.z'])

        # rather than create a cycle by connecting d1.y1 to d2.y1 and d2.y2 to d1.y2
        # we will constrain y1 and y2 to be equal for the two disciplines

        equal = EQConstraintComp()
        self.add_subsystem('equal', equal)

        equal.add_eq_output('y1', add_constraint=True)
        equal.add_eq_output('y2', add_constraint=True)

        self.connect('dv.y1', 'equal.lhs:y1')
        self.connect('d1.y1', 'equal.rhs:y1')

        self.connect('dv.y2', 'equal.lhs:y2')
        self.connect('d2.y2', 'equal.rhs:y2')

        # the driver will effectively solve the cycle
        # by satisfying the equality constraints

        self.add_design_var('dv.x', lower=0., upper=5.)
        self.add_design_var('dv.y1', lower=0., upper=5.)
        self.add_design_var('dv.y2', lower=0., upper=5.)
        self.add_design_var('dv.z', lower=np.array([-5., 0.]), upper=np.array([5., 5.]))
        self.add_objective('obj_cmp.obj')
        self.add_constraint('con_cmp1.con1', upper=0.)
        self.add_constraint('con_cmp2.con2', upper=0.)


class TestEQConstraintComp(unittest.TestCase):

    def test_sellar_idf(self):
        prob = Problem(SellarIDF())
        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', disp=False)
        prob.setup()

        # check derivatives
        prob['dv.y1'] = 100
        prob['equal.rhs:y1'] = 1

        prob.run_model()

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

        # check results
        prob.run_driver()

        assert_rel_error(self, prob['dv.x'], 0., 1e-5)
        assert_rel_error(self, prob['dv.z'], [1.977639, 0.], 1e-5)

        assert_rel_error(self, prob['obj_cmp.obj'], 3.18339395045, 1e-5)

        assert_almost_equal(prob['dv.y1'], 3.16)
        assert_almost_equal(prob['d1.y1'], 3.16)

        assert_almost_equal(prob['dv.y2'], 3.7552778)
        assert_almost_equal(prob['d2.y2'], 3.7552778)

        assert_almost_equal(prob['equal.y1'], 0.0)
        assert_almost_equal(prob['equal.y2'], 0.0)

    def test_create_on_init(self):
        prob = Problem()
        model = prob.model

        # find intersection of two non-parallel lines
        model.add_subsystem('indep', IndepVarComp('x', val=0.))
        model.add_subsystem('f', ExecComp('y=3*x-3', x=0.))
        model.add_subsystem('g', ExecComp('y=2.3*x+4', x=0.))
        model.add_subsystem('equal', EQConstraintComp('y', val=11.))

        model.connect('indep.x', 'f.x')
        model.connect('indep.x', 'g.x')

        model.connect('f.y', 'equal.lhs:y')
        model.connect('g.y', 'equal.rhs:y')

        model.add_design_var('indep.x', lower=0., upper=20.)
        model.add_objective('f.y')

        prob.setup(mode='fwd')

        # verify that the output variable has been initialized
        self.assertEqual(prob['equal.y'], 11.)

        # verify that the constraint has not been added
        self.assertFalse('equal.y' in model.get_constraints())

        # manually add the constraint
        model.add_constraint('equal.y', equals=0.)
        prob.setup(mode='fwd')

        prob.driver = ScipyOptimizeDriver(disp=False)

        prob.run_driver()

        assert_almost_equal(prob['equal.y'], 0.)
        assert_almost_equal(prob['indep.x'], 10.)
        assert_almost_equal(prob['f.y'], 27.)
        assert_almost_equal(prob['g.y'], 27.)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_create_on_init_add_constraint(self):
        prob = Problem()
        model = prob.model

        # find intersection of two non-parallel lines
        model.add_subsystem('indep', IndepVarComp('x', val=0.))
        model.add_subsystem('f', ExecComp('y=3*x-3', x=0.))
        model.add_subsystem('g', ExecComp('y=2.3*x+4', x=0.))
        model.add_subsystem('equal', EQConstraintComp('y', add_constraint=True))

        model.connect('indep.x', 'f.x')
        model.connect('indep.x', 'g.x')

        model.connect('f.y', 'equal.lhs:y')
        model.connect('g.y', 'equal.rhs:y')

        model.add_design_var('indep.x', lower=0., upper=20.)
        model.add_objective('f.y')

        prob.setup(mode='fwd')

        # verify that the constraint has been added as requested
        self.assertTrue('equal.y' in model.get_constraints())

        prob.driver = ScipyOptimizeDriver(disp=False)

        prob.run_driver()

        assert_almost_equal(prob['equal.y'], 0.)
        assert_almost_equal(prob['indep.x'], 10.)
        assert_almost_equal(prob['f.y'], 27.)
        assert_almost_equal(prob['g.y'], 27.)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_create_on_init_add_constraint_no_normalization(self):
        prob = Problem()
        model = prob.model

        # find intersection of two non-parallel lines
        model.add_subsystem('indep', IndepVarComp('x', val=-2.0))
        model.add_subsystem('f', ExecComp('y=3*x-3', x=0.))
        model.add_subsystem('g', ExecComp('y=2.3*x+4', x=0.))
        model.add_subsystem('equal', EQConstraintComp('y', add_constraint=True, normalize=False,
                                                      ref0=0, ref=100.0))

        model.connect('indep.x', 'f.x')
        model.connect('indep.x', 'g.x')

        model.connect('f.y', 'equal.lhs:y')
        model.connect('g.y', 'equal.rhs:y')

        model.add_design_var('indep.x', lower=0., upper=20.)
        model.add_objective('f.y')

        prob.setup(mode='fwd')

        # verify that the constraint has been added as requested
        self.assertTrue('equal.y' in model.get_constraints())

        # verify that the output is not being normalized
        prob.run_model()
        lhs = prob['f.y']
        rhs = prob['g.y']
        diff = lhs - rhs
        assert_rel_error(self, prob['equal.y'], diff)

        prob.driver = ScipyOptimizeDriver(disp=False)

        prob.run_driver()

        assert_almost_equal(prob['equal.y'], 0.)
        assert_almost_equal(prob['indep.x'], 10.)
        assert_almost_equal(prob['f.y'], 27.)
        assert_almost_equal(prob['g.y'], 27.)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_vectorized(self):
        prob = Problem()
        model = prob.model

        n = 100

        # find intersection of two non-parallel lines, vectorized
        model.add_subsystem('indep', IndepVarComp('x', val=np.ones(n)))
        model.add_subsystem('f', ExecComp('y=3*x-3', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('g', ExecComp('y=2.3*x+4', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('equal', EQConstraintComp('y', val=np.ones(n), add_constraint=True))
        model.add_subsystem('obj_cmp', ExecComp('obj=sum(y)', y=np.zeros(n)))

        model.connect('indep.x', 'f.x')
        model.connect('indep.x', 'g.x')
        model.connect('f.y', 'equal.lhs:y')
        model.connect('g.y', 'equal.rhs:y')
        model.connect('f.y', 'obj_cmp.y')

        model.add_design_var('indep.x', lower=np.zeros(n), upper=20.*np.ones(n))
        model.add_objective('obj_cmp.obj')

        prob.setup(mode='fwd')

        prob.driver = ScipyOptimizeDriver(disp=False)

        prob.run_driver()

        assert_almost_equal(prob['equal.y'], np.zeros(n))
        assert_almost_equal(prob['indep.x'], np.ones(n)*10.)
        assert_almost_equal(prob['f.y'], np.ones(n)*27.)
        assert_almost_equal(prob['g.y'], np.ones(n)*27.)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_vectorized_no_normalization(self):
        prob = Problem()
        model = prob.model

        n = 100

        # find intersection of two non-parallel lines, vectorized
        model.add_subsystem('indep', IndepVarComp('x', val=-2.0*np.ones(n)))
        model.add_subsystem('f', ExecComp('y=3*x-3', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('g', ExecComp('y=2.3*x+4', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('equal', EQConstraintComp('y', val=np.ones(n), add_constraint=True,
                                                      normalize=False))
        model.add_subsystem('obj_cmp', ExecComp('obj=sum(y)', y=np.zeros(n)))

        model.connect('indep.x', 'f.x')
        model.connect('indep.x', 'g.x')
        model.connect('f.y', 'equal.lhs:y')
        model.connect('g.y', 'equal.rhs:y')
        model.connect('f.y', 'obj_cmp.y')

        model.add_design_var('indep.x', lower=np.zeros(n), upper=20.*np.ones(n))
        model.add_objective('obj_cmp.obj')

        prob.setup(mode='fwd')

        prob.driver = ScipyOptimizeDriver(disp=False)

        # verify that the output is not being normalized
        prob.run_model()
        lhs = prob['f.y']
        rhs = prob['g.y']
        diff = lhs - rhs
        assert_rel_error(self, prob['equal.y'], diff)

        prob.run_driver()

        assert_almost_equal(prob['equal.y'], np.zeros(n))
        assert_almost_equal(prob['indep.x'], np.ones(n)*10.)
        assert_almost_equal(prob['f.y'], np.ones(n)*27.)
        assert_almost_equal(prob['g.y'], np.ones(n)*27.)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_scalar_with_mult(self):
        prob = Problem()
        model = prob.model

        # find where 2*x == x^2
        model.add_subsystem('indep', IndepVarComp('x', val=1.))
        model.add_subsystem('multx', IndepVarComp('m', val=2.))
        model.add_subsystem('f', ExecComp('y=x**2', x=1.))
        model.add_subsystem('equal', EQConstraintComp('y', use_mult=True))

        model.connect('indep.x', 'f.x')

        model.connect('indep.x', 'equal.lhs:y')
        model.connect('multx.m', 'equal.mult:y')
        model.connect('f.y', 'equal.rhs:y')

        model.add_design_var('indep.x', lower=0., upper=10.)
        model.add_constraint('equal.y', equals=0.)
        model.add_objective('f.y')

        prob.setup(mode='fwd')
        prob.driver = ScipyOptimizeDriver(disp=False)
        prob.run_driver()

        assert_rel_error(self, prob['equal.y'], 0., 1e-6)
        assert_rel_error(self, prob['indep.x'], 2., 1e-6)
        assert_rel_error(self, prob['f.y'], 4., 1e-6)

        cpd = prob.check_partials(out_stream=None)
        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_vectorized_with_mult(self):
        prob = Problem()
        model = prob.model

        n = 100

        # find where 2*x == x^2, vectorized
        model.add_subsystem('indep', IndepVarComp('x', val=np.ones(n)))
        model.add_subsystem('multx', IndepVarComp('m', val=np.ones(n)*2.))
        model.add_subsystem('f', ExecComp('y=x**2', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('equal', EQConstraintComp('y', val=np.ones(n),
                            use_mult=True, add_constraint=True))
        model.add_subsystem('obj_cmp', ExecComp('obj=sum(y)', y=np.zeros(n)))

        model.connect('indep.x', 'f.x')

        model.connect('indep.x', 'equal.lhs:y')
        model.connect('multx.m', 'equal.mult:y')
        model.connect('f.y', 'equal.rhs:y')
        model.connect('f.y', 'obj_cmp.y')

        model.add_design_var('indep.x', lower=np.zeros(n), upper=np.ones(n)*10.)
        model.add_objective('obj_cmp.obj')

        prob.setup(mode='fwd')
        prob.driver = ScipyOptimizeDriver(disp=False)
        prob.run_driver()

        assert_rel_error(self, prob['equal.y'], np.zeros(n), 1e-6)
        assert_rel_error(self, prob['indep.x'], np.ones(n)*2., 1e-6)
        assert_rel_error(self, prob['f.y'], np.ones(n)*4., 1e-6)

        cpd = prob.check_partials(out_stream=None)
        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_vectorized_with_default_mult(self):
        prob = Problem()
        model = prob.model

        n = 100

        # find where 2*x == x^2, vectorized
        model.add_subsystem('indep', IndepVarComp('x', val=np.ones(n)))
        model.add_subsystem('f', ExecComp('y=x**2', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('equal', EQConstraintComp('y', val=np.ones(n),
                            use_mult=True, mult_val=2., add_constraint=True))
        model.add_subsystem('obj_cmp', ExecComp('obj=sum(y)', y=np.zeros(n)))

        model.connect('indep.x', 'f.x')

        model.connect('indep.x', 'equal.lhs:y')
        model.connect('f.y', 'equal.rhs:y')
        model.connect('f.y', 'obj_cmp.y')

        model.add_design_var('indep.x', lower=np.zeros(n), upper=np.ones(n)*10.)
        model.add_objective('obj_cmp.obj')

        prob.setup(mode='fwd')
        prob.driver = ScipyOptimizeDriver(disp=False)
        prob.run_driver()

        assert_rel_error(self, prob['equal.y'], np.zeros(n), 1e-6)
        assert_rel_error(self, prob['indep.x'], np.ones(n)*2., 1e-6)
        assert_rel_error(self, prob['f.y'], np.ones(n)*4., 1e-6)

        cpd = prob.check_partials(out_stream=None)
        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_rhs_val(self):
        prob = Problem()
        model = prob.model

        # find where x^2 == 4
        model.add_subsystem('indep', IndepVarComp('x', val=1.))
        model.add_subsystem('f', ExecComp('y=x**2', x=1.))
        model.add_subsystem('equal', EQConstraintComp('y', rhs_val=4.))

        model.connect('indep.x', 'f.x')
        model.connect('f.y', 'equal.lhs:y')

        model.add_design_var('indep.x', lower=0., upper=10.)
        model.add_constraint('equal.y', equals=0.)
        model.add_objective('f.y')

        prob.setup(mode='fwd')
        prob.driver = ScipyOptimizeDriver(disp=False)
        prob.run_driver()

        assert_rel_error(self, prob['equal.y'], 0., 1e-6)
        assert_rel_error(self, prob['indep.x'], 2., 1e-6)
        assert_rel_error(self, prob['f.y'], 4., 1e-6)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)

    def test_vectorized_rhs_val(self):
        prob = Problem()
        model = prob.model

        n = 100

        # find where x^2 == 4, vectorized
        model.add_subsystem('indep', IndepVarComp('x', val=np.ones(n)))
        model.add_subsystem('f', ExecComp('y=x**2', x=np.ones(n), y=np.ones(n)))
        model.add_subsystem('equal', EQConstraintComp('y', val=np.ones(n),
                            rhs_val=np.ones(n)*4., use_mult=True, mult_val=2.))
        model.add_subsystem('obj_cmp', ExecComp('obj=sum(y)', y=np.zeros(n)))

        model.connect('indep.x', 'f.x')

        model.connect('indep.x', 'equal.lhs:y')
        model.connect('f.y', 'obj_cmp.y')

        model.add_design_var('indep.x', lower=np.zeros(n), upper=np.ones(n)*10.)
        model.add_constraint('equal.y', equals=0.)
        model.add_objective('obj_cmp.obj')

        prob.setup(mode='fwd')
        prob.driver = ScipyOptimizeDriver(disp=False)
        prob.run_driver()

        assert_rel_error(self, prob['equal.y'], np.zeros(n), 1e-6)
        assert_rel_error(self, prob['indep.x'], np.ones(n)*2., 1e-6)
        assert_rel_error(self, prob['f.y'], np.ones(n)*4., 1e-6)

        cpd = prob.check_partials(out_stream=None)
        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

    def test_renamed_vars(self):
        prob = Problem()
        model = prob.model

        # find intersection of two non-parallel lines, fx_y and gx_y
        equal = EQConstraintComp('y', lhs_name='fx_y', rhs_name='gx_y',
                                        add_constraint=True)

        model.add_subsystem('indep', IndepVarComp('x', val=0.))
        model.add_subsystem('f', ExecComp('y=3*x-3', x=0.))
        model.add_subsystem('g', ExecComp('y=2.3*x+4', x=0.))
        model.add_subsystem('equal', equal)

        model.connect('indep.x', 'f.x')
        model.connect('indep.x', 'g.x')

        model.connect('f.y', 'equal.fx_y')
        model.connect('g.y', 'equal.gx_y')

        model.add_design_var('indep.x', lower=0., upper=20.)
        model.add_objective('f.y')

        prob.setup(mode='fwd')
        prob.driver = ScipyOptimizeDriver(disp=False)
        prob.run_driver()

        assert_almost_equal(prob['equal.y'], 0.)
        assert_almost_equal(prob['indep.x'], 10.)
        assert_almost_equal(prob['f.y'], 27.)
        assert_almost_equal(prob['g.y'], 27.)

        cpd = prob.check_partials(out_stream=None)

        for (of, wrt) in cpd['equal']:
            assert_almost_equal(cpd['equal'][of, wrt]['abs error'], 0.0, decimal=5)

        assert_check_partials(cpd, atol=1e-5, rtol=1e-5)


class TestFeatureEQConstraintComp(unittest.TestCase):

    def test_feature_sellar_idf(self):
        prob = Problem(model=SellarIDF())
        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', disp=True)
        prob.setup()
        prob.run_driver()

        assert_rel_error(self, prob['dv.x'], 0., 1e-5)

        assert_rel_error(self, [prob['dv.y1'], prob['d1.y1']], [[3.16], [3.16]], 1e-5)
        assert_rel_error(self, [prob['dv.y2'], prob['d2.y2']], [[3.7552778], [3.7552778]], 1e-5)

        assert_rel_error(self, prob['dv.z'], [1.977639, 0.], 1e-5)

        assert_rel_error(self, prob['obj_cmp.obj'], 3.18339395045, 1e-5)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
