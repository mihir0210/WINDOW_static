from __future__ import print_function

import unittest

from six import assertRaisesRegex
from six.moves import range

import itertools

import numpy as np

try:
    from parameterized import parameterized
except ImportError:
    from openmdao.utils.assert_utils import SkipParameterized as parameterized

from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ExplicitComponent, \
    NonlinearRunOnce, NonLinearRunOnce
from openmdao.utils.assert_utils import assert_rel_error, assert_warning
from openmdao.test_suite.components.sellar import SellarDis2


class SimpleGroup(Group):

    def __init__(self):
        super(SimpleGroup, self).__init__()

        self.add_subsystem('comp1', IndepVarComp('x', 5.0))
        self.add_subsystem('comp2', ExecComp('b=2*a'))
        self.connect('comp1.x', 'comp2.a')


class BranchGroup(Group):

    def __init__(self):
        super(BranchGroup, self).__init__()

        b1 = self.add_subsystem('Branch1', Group())
        g1 = b1.add_subsystem('G1', Group())
        g2 = g1.add_subsystem('G2', Group())
        g2.add_subsystem('comp1', ExecComp('b=2.0*a', a=3.0, b=6.0))

        b2 = self.add_subsystem('Branch2', Group())
        g3 = b2.add_subsystem('G3', Group())
        g3.add_subsystem('comp2', ExecComp('b=3.0*a', a=4.0, b=12.0))


class SetOrderGroup(Group):
    def setup(self):
        self.add_subsystem('C1', ExecComp('y=2.0*x'))
        self.add_subsystem('C2', ExecComp('y=2.0*x'))
        self.add_subsystem('C3', ExecComp('y=2.0*x'))

        self.set_order(['C1', 'C3', 'C2'])

        self.connect('C1.y', 'C3.x')
        self.connect('C3.y', 'C2.x')


class ReportOrderComp(ExplicitComponent):
    def __init__(self, order_list):
        super(ReportOrderComp, self).__init__()
        self._order_list = order_list

    def setup(self):
        self.add_input('x', 0.0)
        self.add_output('y', 0.0)

    def compute(self, inputs, outputs):
        self._order_list.append(self.pathname)


class TestGroup(unittest.TestCase):

    def test_add_subsystem_class(self):
        p = Problem()
        try:
            p.model.add_subsystem('comp', IndepVarComp)
        except TypeError as err:
            self.assertEqual(str(err), "Subsystem 'comp' should be an instance, "
                                       "but a class object was found.")
        else:
            self.fail('Exception expected.')

    def test_same_sys_name(self):
        """Test error checking for the case where we add two subsystems with the same name."""
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp('x', 5.0))
        p.model.add_subsystem('comp2', ExecComp('b=2*a'))

        try:
            p.model.add_subsystem('comp2', ExecComp('b=2*a'))
        except Exception as err:
            self.assertEqual(str(err), "Subsystem name 'comp2' is already used.")
        else:
            self.fail('Exception expected.')

    def test_deprecated_runonce(self):
        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', 5.0))
        p.model.add_subsystem('comp', ExecComp('b=2*a'))

        msg = "NonLinearRunOnce is deprecated.  Use NonlinearRunOnce instead."

        with assert_warning(DeprecationWarning, msg):
            p.model.nonlinear_solver = NonLinearRunOnce()

    def test_group_simple(self):
        from openmdao.api import ExecComp, Problem

        p = Problem()
        p.model.add_subsystem('comp1', ExecComp('b=2.0*a', a=3.0, b=6.0))

        p.setup()

        self.assertEqual(p['comp1.a'], 3.0)
        self.assertEqual(p['comp1.b'], 6.0)

    def test_group_add(self):
        model = Group()
        ecomp = ExecComp('b=2.0*a', a=3.0, b=6.0)

        msg = "The 'add' method provides backwards compatibility with OpenMDAO <= 1.x ; " \
              "use 'add_subsystem' instead."

        with assert_warning(DeprecationWarning, msg):
            comp1 = model.add('comp1', ecomp)

        self.assertTrue(ecomp is comp1)

    def test_group_simple_promoted(self):
        from openmdao.api import ExecComp, Problem, IndepVarComp

        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('a', 3.0),
                              promotes_outputs=['a'])
        p.model.add_subsystem('comp1', ExecComp('b=2.0*a'),
                              promotes_inputs=['a'])

        p.setup()
        p.run_model()

        self.assertEqual(p['a'], 3.0)
        self.assertEqual(p['comp1.b'], 6.0)

    def test_group_rename_connect(self):
        from openmdao.api import Problem, IndepVarComp, ExecComp

        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('aa', 3.0),
                              promotes=['aa'])
        p.model.add_subsystem('comp1', ExecComp('b=2.0*aa'),
                              promotes_inputs=['aa'])

        # here we alias 'a' to 'aa' so that it will be automatically
        # connected to the independent variable 'aa'.
        p.model.add_subsystem('comp2', ExecComp('b=3.0*a'),
                              promotes_inputs=[('a', 'aa')])

        p.setup()
        p.run_model()

        self.assertEqual(p['comp1.b'], 6.0)
        self.assertEqual(p['comp2.b'], 9.0)

    def test_subsys_attributes(self):
        p = Problem()

        class MyGroup(Group):
            def setup(self):
                # two subsystems added during setup
                self.add_subsystem('comp1', ExecComp('b=2.0*a', a=3.0, b=6.0))
                self.add_subsystem('comp2', ExecComp('b=3.0*a', a=4.0, b=12.0))

        # subsystems become attributes
        my_group = p.model.add_subsystem('gg', MyGroup())
        self.assertTrue(p.model.gg is my_group)

        # after calling setup(), MyGroup's subsystems are also attributes
        p.setup()
        self.assertTrue(hasattr(p.model.gg, 'comp1'))
        self.assertTrue(hasattr(p.model.gg, 'comp2'))

        # calling setup() again doesn't break anything
        p.setup()
        self.assertTrue(p.model.gg is my_group)
        self.assertTrue(hasattr(p.model.gg, 'comp1'))
        self.assertTrue(hasattr(p.model.gg, 'comp2'))

        # name cannot start with an underscore
        with self.assertRaises(Exception) as err:
            p.model.add_subsystem('_bad_name', Group())
        self.assertEqual(str(err.exception),
                         "'_bad_name' is not a valid system name.")

        # 'name', 'pathname', 'comm' and 'options' are reserved names
        for reserved in ['name', 'pathname', 'comm', 'options']:
            with self.assertRaises(Exception) as err:
                p.model.add_subsystem(reserved, Group())
            self.assertEqual(str(err.exception),
                             "Group '' already has an attribute '%s'." %
                             reserved)

    def test_group_nested(self):
        from openmdao.api import ExecComp, Problem, Group

        p = Problem()
        p.model.add_subsystem('G1', Group())
        p.model.G1.add_subsystem('comp1', ExecComp('b=2.0*a', a=3.0, b=6.0))
        p.model.G1.add_subsystem('comp2', ExecComp('b=3.0*a', a=4.0, b=12.0))

        p.setup()

        self.assertEqual(p['G1.comp1.a'], 3.0)
        self.assertEqual(p['G1.comp1.b'], 6.0)
        self.assertEqual(p['G1.comp2.a'], 4.0)
        self.assertEqual(p['G1.comp2.b'], 12.0)

    def test_group_getsystem_top(self):
        from openmdao.api import Problem
        from openmdao.core.tests.test_group import BranchGroup

        p = Problem(model=BranchGroup())
        p.setup()

        c1 = p.model.Branch1.G1.G2.comp1
        self.assertEqual(c1.pathname, 'Branch1.G1.G2.comp1')

        c2 = p.model.Branch2.G3.comp2
        self.assertEqual(c2.pathname, 'Branch2.G3.comp2')

    def test_group_nested_promoted1(self):
        from openmdao.api import Problem, Group, ExecComp

        # promotes from bottom level up 1
        p = Problem()
        g1 = p.model.add_subsystem('G1', Group())
        g1.add_subsystem('comp1', ExecComp('b=2.0*a', a=3.0, b=6.0),
                         promotes_inputs=['a'], promotes_outputs=['b'])
        g1.add_subsystem('comp2', ExecComp('b=3.0*a', a=4.0, b=12.0),
                         promotes_inputs=['a'])
        p.setup()

        # output G1.comp1.b is promoted
        self.assertEqual(p['G1.b'], 6.0)
        # output G1.comp2.b is not promoted
        self.assertEqual(p['G1.comp2.b'], 12.0)

        # use unpromoted names for the following 2 promoted inputs
        self.assertEqual(p['G1.comp1.a'], 3.0)
        self.assertEqual(p['G1.comp2.a'], 4.0)

    def test_group_nested_promoted2(self):
        from openmdao.api import Problem, Group, ExecComp

        # promotes up from G1 level
        p = Problem()
        g1 = Group()
        g1.add_subsystem('comp1', ExecComp('b=2.0*a', a=3.0, b=6.0))
        g1.add_subsystem('comp2', ExecComp('b=3.0*a', a=4.0, b=12.0))

        # use glob pattern 'comp?.a' to promote both comp1.a and comp2.a
        # use glob pattern 'comp?.b' to promote both comp1.b and comp2.b
        p.model.add_subsystem('G1', g1,
                              promotes_inputs=['comp?.a'],
                              promotes_outputs=['comp?.b'])
        p.setup()

        # output G1.comp1.b is promoted
        self.assertEqual(p['comp1.b'], 6.0)
        # output G1.comp2.b is promoted
        self.assertEqual(p['comp2.b'], 12.0)

        # access both promoted inputs using unpromoted names.
        self.assertEqual(p['G1.comp1.a'], 3.0)
        self.assertEqual(p['G1.comp2.a'], 4.0)

    def test_group_promotes(self):
        """Promoting a single variable."""
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp([('a', 2.0), ('x', 5.0)]),
                              promotes_outputs=['x'])
        p.model.add_subsystem('comp2', ExecComp('y=2*x'), promotes_inputs=['x'])
        p.setup()

        p.set_solver_print(level=0)
        p.run_model()

        self.assertEqual(p['comp1.a'], 2)
        self.assertEqual(p['x'], 5)
        self.assertEqual(p['comp2.y'], 10)

    def test_group_renames(self):
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp('x', 5.0),
                              promotes_outputs=[('x', 'foo')])
        p.model.add_subsystem('comp2', ExecComp('y=2*foo'), promotes_inputs=['foo'])
        p.setup()

        p.set_solver_print(level=0)
        p.run_model()

        self.assertEqual(p['foo'], 5)
        self.assertEqual(p['comp2.y'], 10)

    def test_group_renames_errors_single_string(self):
        p = Problem()
        with self.assertRaises(Exception) as err:
            p.model.add_subsystem('comp1', IndepVarComp('x', 5.0),
                                  promotes_outputs='x')
        self.assertEqual(str(err.exception),
                         ": promotes must be an iterator of strings and/or tuples.")

    def test_group_renames_errors_not_found(self):
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp('x', 5.0),
                              promotes_outputs=[('xx', 'foo')])
        p.model.add_subsystem('comp2', ExecComp('y=2*foo'), promotes_inputs=['foo'])

        with self.assertRaises(Exception) as err:
            p.setup(check=False)
        self.assertEqual(str(err.exception),
                         "comp1: 'promotes_outputs' failed to find any matches for "
                         "the following names or patterns: ['xx'].")

    def test_group_renames_errors_bad_tuple(self):
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp('x', 5.0),
                              promotes_outputs=[('x', 'foo', 'bar')])
        p.model.add_subsystem('comp2', ExecComp('y=2*foo'), promotes_inputs=['foo'])

        with self.assertRaises(Exception) as err:
            p.setup(check=False)
        self.assertEqual(str(err.exception),
                         "when adding subsystem 'comp1', entry '('x', 'foo', 'bar')' "
                         "is not a string or tuple of size 2")

    def test_group_promotes_multiple(self):
        """Promoting multiple variables."""
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp([('a', 2.0), ('x', 5.0)]),
                              promotes_outputs=['a', 'x'])
        p.model.add_subsystem('comp2', ExecComp('y=2*x'),
                              promotes_inputs=['x'])
        p.setup()

        p.set_solver_print(level=0)
        p.run_model()

        self.assertEqual(p['a'], 2)
        self.assertEqual(p['x'], 5)
        self.assertEqual(p['comp2.y'], 10)

    def test_group_promotes_all(self):
        """Promoting all variables with asterisk."""
        p = Problem()
        p.model.add_subsystem('comp1', IndepVarComp([('a', 2.0), ('x', 5.0)]),
                              promotes_outputs=['*'])
        p.model.add_subsystem('comp2', ExecComp('y=2*x'),
                              promotes_inputs=['x'])
        p.setup()

        p.set_solver_print(level=0)
        p.run_model()

        self.assertEqual(p['a'], 2)
        self.assertEqual(p['x'], 5)
        self.assertEqual(p['comp2.y'], 10)

    def test_group_promotes2(self):

        class Sellar(Group):
            def setup(self):
                dv = self.add_subsystem('des_vars', IndepVarComp(), promotes=['*'])
                dv.add_output('x', 1.0)
                dv.add_output('z', np.array([5.0, 2.0]))

                self.add_subsystem('d1', SellarDis2(),
                                   promotes_inputs=['y1'], promotes_outputs=['foo'])
                self.add_subsystem('d2', SellarDis2())

        p = Problem()
        p.model = Sellar()

        with self.assertRaises(Exception) as err:
            p.setup(check=False)
        self.assertEqual(str(err.exception),
                         "d1: 'promotes_outputs' failed to find any matches for "
                         "the following names or patterns: ['foo'].")

    def test_group_nested_conn(self):
        """Example of adding subsystems and issuing connections with nested groups."""
        g1 = Group()
        c1_1 = g1.add_subsystem('comp1', IndepVarComp('x', 5.0))
        c1_2 = g1.add_subsystem('comp2', ExecComp('b=2*a'))
        g1.connect('comp1.x', 'comp2.a')
        g2 = Group()
        c2_1 = g2.add_subsystem('comp1', ExecComp('b=2*a'))
        c2_2 = g2.add_subsystem('comp2', ExecComp('b=2*a'))
        g2.connect('comp1.b', 'comp2.a')

        model = Group()
        model.add_subsystem('group1', g1)
        model.add_subsystem('group2', g2)
        model.connect('group1.comp2.b', 'group2.comp1.a')

        p = Problem(model=model)
        p.setup()

        c1_1 = p.model.group1.comp1
        c1_2 = p.model.group1.comp2
        c2_1 = p.model.group2.comp1
        c2_2 = p.model.group2.comp2
        self.assertEqual(c1_1.name, 'comp1')
        self.assertEqual(c1_2.name, 'comp2')
        self.assertEqual(c2_1.name, 'comp1')
        self.assertEqual(c2_2.name, 'comp2')

        c1_1 = p.model.group1.comp1
        c1_2 = p.model.group1.comp2
        c2_1 = p.model.group2.comp1
        c2_2 = p.model.group2.comp2
        self.assertEqual(c1_1.name, 'comp1')
        self.assertEqual(c1_2.name, 'comp2')
        self.assertEqual(c2_1.name, 'comp1')
        self.assertEqual(c2_2.name, 'comp2')

        s = p.model._get_subsystem('')
        self.assertEqual(s, None)

        p.set_solver_print(level=0)
        p.run_model()

        self.assertEqual(p['group1.comp1.x'], 5.0)
        self.assertEqual(p['group1.comp2.b'], 10.0)
        self.assertEqual(p['group2.comp1.b'], 20.0)
        self.assertEqual(p['group2.comp2.b'], 40.0)

    def test_reused_output_promoted_names(self):
        prob = Problem()
        prob.model.add_subsystem('px1', IndepVarComp('x1', 100.0))
        G1 = prob.model.add_subsystem('G1', Group())
        G1.add_subsystem("C1", ExecComp("y=2.0*x"), promotes=['y'])
        G1.add_subsystem("C2", ExecComp("y=2.0*x"), promotes=['y'])
        msg = r"Output name 'y' refers to multiple outputs: \['G1.C1.y', 'G1.C2.y'\]."
        with assertRaisesRegex(self, Exception, msg):
            prob.setup(check=False)

    def test_basic_connect_units(self):
        import numpy as np

        from openmdao.api import Problem, IndepVarComp, ExecComp

        p = Problem()
        indep = p.model.add_subsystem('indep', IndepVarComp())
        indep.add_output('x', np.ones(5), units='ft')
        p.model.add_subsystem('C1', ExecComp('y=sum(x)', x={'value': np.zeros(5), 'units': 'inch'},
                                             y={'units': 'inch'}))
        p.model.connect('indep.x', 'C1.x')
        p.set_solver_print(level=0)
        p.setup()
        p.run_model()
        assert_rel_error(self, p['indep.x'], np.ones(5))
        assert_rel_error(self, p['C1.x'], np.ones(5)*12.)
        assert_rel_error(self, p['C1.y'], 60.)

    def test_connect_1_to_many(self):
        import numpy as np

        from openmdao.api import Problem, IndepVarComp, ExecComp

        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)))
        p.model.add_subsystem('C1', ExecComp('y=sum(x)*2.0', x=np.zeros(5)))
        p.model.add_subsystem('C2', ExecComp('y=sum(x)*4.0', x=np.zeros(5)))
        p.model.add_subsystem('C3', ExecComp('y=sum(x)*6.0', x=np.zeros(5)))
        p.model.connect('indep.x', ['C1.x', 'C2.x', 'C3.x'])
        p.set_solver_print(level=0)
        p.setup()
        p.run_model()
        assert_rel_error(self, p['C1.y'], 10.)
        assert_rel_error(self, p['C2.y'], 20.)
        assert_rel_error(self, p['C3.y'], 30.)

    def test_double_src_indices(self):
        class MyComp1(ExplicitComponent):
            def setup(self):
                self.add_input('x', np.ones(3), src_indices=[0, 1, 2])
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = np.sum(inputs['x'])*2.0

        p = Problem()

        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)))
        p.model.add_subsystem('C1', MyComp1())
        p.model.connect('indep.x', 'C1.x', src_indices=[1, 0, 2])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         ": src_indices has been defined in both "
                         "connect('indep.x', 'C1.x') and add_input('C1.x', ...).")

    def test_connect_src_indices(self):
        import numpy as np

        from openmdao.api import Problem, IndepVarComp, ExecComp

        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)))
        p.model.add_subsystem('C1', ExecComp('y=sum(x)*2.0', x=np.zeros(3)))
        p.model.add_subsystem('C2', ExecComp('y=sum(x)*4.0', x=np.zeros(2)))

        # connect C1.x to the first 3 entries of indep.x
        p.model.connect('indep.x', 'C1.x', src_indices=[0, 1, 2])

        # connect C2.x to the last 2 entries of indep.x
        # use -2 (same as 3 in this case) to show that negative indices work.
        p.model.connect('indep.x', 'C2.x', src_indices=[-2, 4])

        p.set_solver_print(level=0)
        p.setup()
        p.run_model()

        assert_rel_error(self, p['C1.x'], np.ones(3))
        assert_rel_error(self, p['C1.y'], 6.)
        assert_rel_error(self, p['C2.x'], np.ones(2))
        assert_rel_error(self, p['C2.y'], 8.)

    def test_connect_src_indices_noflat(self):
        import numpy as np

        from openmdao.api import Problem, IndepVarComp, ExecComp

        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', np.arange(12).reshape((4, 3))))
        p.model.add_subsystem('C1', ExecComp('y=sum(x)*2.0', x=np.zeros((2, 2))))

        # connect C1.x to entries (0,0), (-1,1), (2,1), (1,1) of indep.x
        p.model.connect('indep.x', 'C1.x',
                        src_indices=[[(0, 0), (-1, 1)],
                                     [(2, 1), (1, 1)]], flat_src_indices=False)

        p.set_solver_print(level=0)
        p.setup()
        p.run_model()
        assert_rel_error(self, p['C1.x'], np.array([[0., 10.],
                                                    [7., 4.]]))
        assert_rel_error(self, p['C1.y'], 42.)

    def test_promote_not_found1(self):
        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', ExecComp('y=x'), promotes_inputs=['x'])
        p.model.add_subsystem('C2', ExecComp('y=x'), promotes_outputs=['x*'])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         "C2: 'promotes_outputs' failed to find any matches for "
                         "the following names or patterns: ['x*'].")

    def test_promote_not_found2(self):
        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', ExecComp('y=x'), promotes_inputs=['x'])
        p.model.add_subsystem('C2', ExecComp('y=x'), promotes_inputs=['xx'])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         "C2: 'promotes_inputs' failed to find any matches for "
                         "the following names or patterns: ['xx'].")

    def test_promote_not_found3(self):
        p = Problem()
        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', ExecComp('y=x'), promotes=['x'])
        p.model.add_subsystem('C2', ExecComp('y=x'), promotes=['xx'])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         "C2: 'promotes' failed to find any matches for "
                         "the following names or patterns: ['xx'].")

    def test_missing_promote_var(self):
        p = Problem()

        indep_var_comp = IndepVarComp('z', val=2.)
        p.model.add_subsystem('indep_vars', indep_var_comp, promotes=['*'])

        p.model.add_subsystem('d1', ExecComp("y1=z+bar"),
                              promotes_inputs=['z', 'foo'])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         "d1: 'promotes_inputs' failed to find any matches for "
                         "the following names or patterns: ['foo'].")

    def test_missing_promote_var2(self):
        p = Problem()

        indep_var_comp = IndepVarComp('z', val=2.)
        p.model.add_subsystem('indep_vars', indep_var_comp, promotes=['*'])

        p.model.add_subsystem('d1', ExecComp("y1=z+bar"),
                              promotes_outputs=['y1', 'blammo', ('bar', 'blah')])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         "d1: 'promotes_outputs' failed to find any matches for "
                         "the following names or patterns: ['bar', 'blammo'].")

    def test_promote_src_indices(self):
        import numpy as np

        from openmdao.api import ExplicitComponent, Problem, IndepVarComp

        class MyComp1(ExplicitComponent):
            def setup(self):
                # this input will connect to entries 0, 1, and 2 of its source
                self.add_input('x', np.ones(3), src_indices=[0, 1, 2])
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = np.sum(inputs['x'])*2.0

        class MyComp2(ExplicitComponent):
            def setup(self):
                # this input will connect to entries 3 and 4 of its source
                self.add_input('x', np.ones(2), src_indices=[3, 4])
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = np.sum(inputs['x'])*4.0

        p = Problem()

        # by promoting the following output and inputs to 'x', they will
        # be automatically connected
        p.model.add_subsystem('indep', IndepVarComp('x', np.ones(5)),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', MyComp1(), promotes_inputs=['x'])
        p.model.add_subsystem('C2', MyComp2(), promotes_inputs=['x'])

        p.set_solver_print(level=0)
        p.setup()
        p.run_model()

        assert_rel_error(self, p['C1.x'], np.ones(3))
        assert_rel_error(self, p['C1.y'], 6.)
        assert_rel_error(self, p['C2.x'], np.ones(2))
        assert_rel_error(self, p['C2.y'], 8.)

    def test_promote_src_indices_nonflat(self):
        import numpy as np

        from openmdao.api import ExplicitComponent, Problem, IndepVarComp

        class MyComp(ExplicitComponent):
            def setup(self):
                # We want to pull the following 4 values out of the source:
                # [(0,0), (3,1), (2,1), (1,1)].
                # Because our input is also non-flat we arrange the
                # source index tuples into an array having the same shape
                # as our input.  If we didn't set flat_src_indices to False,
                # we could specify src_indices as a 1D array of indices into
                # the flattened source.
                self.add_input('x', np.ones((2, 2)),
                               src_indices=[[(0, 0), (3, 1)],
                                            [(2, 1), (1, 1)]],
                               flat_src_indices=False)
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = np.sum(inputs['x'])

        p = Problem()

        # by promoting the following output and inputs to 'x', they will
        # be automatically connected
        p.model.add_subsystem('indep',
                              IndepVarComp('x', np.arange(12).reshape((4, 3))),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', MyComp(),
                              promotes_inputs=['x'])

        p.set_solver_print(level=0)
        p.setup()
        p.run_model()

        assert_rel_error(self, p['C1.x'],
                         np.array([[0., 10.],
                                   [7., 4.]]))
        assert_rel_error(self, p['C1.y'], 21.)

    def test_promote_src_indices_nonflat_to_scalars(self):
        class MyComp(ExplicitComponent):
            def setup(self):
                self.add_input('x', 1.0, src_indices=[(3, 1)], shape=(1,))
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = inputs['x']*2.0

        p = Problem()

        p.model.add_subsystem('indep',
                              IndepVarComp('x', np.arange(12).reshape((4, 3))),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', MyComp(), promotes_inputs=['x'])

        p.set_solver_print(level=0)
        p.setup()
        p.run_model()
        assert_rel_error(self, p['C1.x'], 10.)
        assert_rel_error(self, p['C1.y'], 20.)

    def test_promote_src_indices_nonflat_error(self):
        class MyComp(ExplicitComponent):
            def setup(self):
                self.add_input('x', 1.0, src_indices=[(3, 1)])
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = np.sum(inputs['x'])

        p = Problem()

        p.model.add_subsystem('indep',
                              IndepVarComp('x', np.arange(12).reshape((4, 3))),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', MyComp(), promotes_inputs=['x'])

        with self.assertRaises(Exception) as context:
            p.setup(check=False)
        self.assertEqual(str(context.exception),
                         "src_indices for 'x' is not flat, so its input shape "
                         "must be provided. src_indices may contain an extra "
                         "dimension if the connected source is not flat, making "
                         "the input shape ambiguous.")

    @parameterized.expand(itertools.product(
        [((4, 3),  [(0, 0), (3, 1), (2, 1), (1, 1)]),
         ((1, 12), [(0, 0), (0, 10), (0, 7), (0, 4)]),
         ((12,),   [0, 10, 7, 4]),
         ((12, 1), [(0, 0), (10, 0), (7, 0), (4, 0)])],
        [(2, 2), (4,), (4, 1), (1, 4)],
    ), name_func=lambda f, n, p: 'test_promote_src_indices_'+'_'.join(str(a) for a in p.args))
    def test_promote_src_indices_param(self, src_info, tgt_shape):
        src_shape, idxvals = src_info

        class MyComp(ExplicitComponent):
            def setup(self):
                if len(tgt_shape) == 1:
                    tshape = None  # don't need to set shape if input is flat
                    sidxs = idxvals
                else:
                    tshape = tgt_shape
                    sidxs = []
                    i = 0
                    for r in range(tgt_shape[0]):
                        sidxs.append([])
                        for c in range(tgt_shape[1]):
                            sidxs[-1].append(idxvals[i])
                            i += 1

                self.add_input('x', np.ones(4).reshape(tgt_shape),
                               src_indices=sidxs, shape=tshape)
                self.add_output('y', 1.0)

            def compute(self, inputs, outputs):
                outputs['y'] = np.sum(inputs['x'])

        p = Problem()

        p.model.add_subsystem('indep',
                              IndepVarComp('x', np.arange(12).reshape(src_shape)),
                              promotes_outputs=['x'])
        p.model.add_subsystem('C1', MyComp(), promotes_inputs=['x'])

        p.set_solver_print(level=0)
        p.setup(check=False)
        p.run_model()
        assert_rel_error(self, p['C1.x'],
                         np.array([0., 10., 7., 4.]).reshape(tgt_shape))
        assert_rel_error(self, p['C1.y'], 21.)

    def test_set_order_feature(self):
        from openmdao.api import Problem, IndepVarComp

        class ReportOrderComp(ExplicitComponent):
            """Adds name to list."""

            def __init__(self, order_list):
                super(ReportOrderComp, self).__init__()
                self._order_list = order_list

            def compute(self, inputs, outputs):
                self._order_list.append(self.pathname)

        # this list will record the execution order of our C1, C2, and C3 components
        order_list = []

        prob = Problem()
        model = prob.model

        model.add_subsystem('indeps', IndepVarComp('x', 1.))
        model.add_subsystem('C1', ReportOrderComp(order_list))
        model.add_subsystem('C2', ReportOrderComp(order_list))
        model.add_subsystem('C3', ReportOrderComp(order_list))

        prob.set_solver_print(level=0)

        prob.setup(check=False)
        prob.run_model()

        self.assertEqual(order_list, ['C1', 'C2', 'C3'])

        # reset the shared order list
        order_list[:] = []

        # now swap C2 and C1 in the order
        model.set_order(['indeps', 'C2', 'C1', 'C3'])

        # after changing the order, we must call setup again
        prob.setup(check=False)
        prob.run_model()
        self.assertEqual(order_list, ['C2', 'C1', 'C3'])

    def test_set_order(self):

        order_list = []
        prob = Problem()
        model = prob.model
        model.nonlinear_solver = NonlinearRunOnce()
        model.add_subsystem('indeps', IndepVarComp('x', 1.))
        model.add_subsystem('C1', ReportOrderComp(order_list))
        model.add_subsystem('C2', ReportOrderComp(order_list))
        model.add_subsystem('C3', ReportOrderComp(order_list))
        model.connect('indeps.x', 'C1.x')
        model.connect('C1.y', 'C2.x')
        model.connect('C2.y', 'C3.x')
        prob.set_solver_print(level=0)

        self.assertEqual(['indeps', 'C1', 'C2', 'C3'],
                         [s.name for s in model._static_subsystems_allprocs])

        prob.setup(check=False)
        prob.run_model()

        self.assertEqual(['C1', 'C2', 'C3'], order_list)

        order_list[:] = []

        # Big boy rules
        model.set_order(['indeps', 'C2', 'C1', 'C3'])

        prob.setup(check=False)
        prob.run_model()
        self.assertEqual(['C2', 'C1', 'C3'], order_list)

        # Extra
        with self.assertRaises(ValueError) as cm:
            model.set_order(['indeps', 'C2', 'junk', 'C1', 'C3'])

        self.assertEqual(str(cm.exception),
                         ": subsystem(s) ['junk'] found in subsystem order but don't exist.")

        # Missing
        with self.assertRaises(ValueError) as cm:
            model.set_order(['indeps', 'C2', 'C3'])

        self.assertEqual(str(cm.exception),
                         ": ['C1'] expected in subsystem order and not found.")

        # Extra and Missing
        with self.assertRaises(ValueError) as cm:
            model.set_order(['indeps', 'C2', 'junk', 'C1', 'junk2'])

        self.assertEqual(str(cm.exception),
                         ": ['C3'] expected in subsystem order and not found.\n"
                         ": subsystem(s) ['junk', 'junk2'] found in subsystem order "
                         "but don't exist.")

        # Dupes
        with self.assertRaises(ValueError) as cm:
            model.set_order(['indeps', 'C2', 'C1', 'C3', 'C1'])

        self.assertEqual(str(cm.exception),
                         ": Duplicate name(s) found in subsystem order list: ['C1']")

    def test_set_order_init_subsystems(self):
        prob = Problem()
        model = prob.model
        model.add_subsystem('indeps', IndepVarComp('x', 1.))
        model.add_subsystem('G1', SetOrderGroup())
        prob.setup(check=False)
        prob.run_model()

        # this test passes if it doesn't raise an exception


class MyComp(ExplicitComponent):
    def __init__(self, input_shape, src_indices=None, flat_src_indices=False):
        super(MyComp, self).__init__()
        self._input_shape = input_shape
        self._src_indices = src_indices
        self._flat_src_indices = flat_src_indices

    def setup(self):
        self.add_input('x', val=np.zeros(self._input_shape),
                       src_indices=self._src_indices, flat_src_indices=self._flat_src_indices)
        self.add_output('y', val=np.zeros(self._input_shape))

    def compute(self, inputs, outputs):
        outputs['y'] = 2.0 * inputs['x']


def src_indices_model(src_shape, tgt_shape, src_indices=None, flat_src_indices=False,
                      promotes=None):
    prob = Problem()
    prob.model.add_subsystem('indeps', IndepVarComp('x', shape=src_shape),
                             promotes=promotes)
    prob.model.add_subsystem('C1', MyComp(tgt_shape,
                                          src_indices=src_indices if promotes else None,
                                          flat_src_indices=flat_src_indices),
                             promotes=promotes)
    if promotes is None:
        prob.model.connect('indeps.x', 'C1.x', src_indices=src_indices,
                           flat_src_indices=flat_src_indices)
    prob.setup(check=False)
    return prob


class TestConnect(unittest.TestCase):

    def setUp(self):
        prob = Problem(Group())

        sub = prob.model.add_subsystem('sub', Group())

        idv = sub.add_subsystem('src', IndepVarComp())
        idv.add_output('x', np.arange(15).reshape((5, 3)))  # array
        idv.add_output('s', 3.)                             # scalar

        sub.add_subsystem('tgt', ExecComp('y = x'))
        sub.add_subsystem('cmp', ExecComp('z = x'))
        sub.add_subsystem('arr', ExecComp('a = x', x=np.zeros(2)))

        self.sub = sub
        self.prob = prob

    def test_src_indices_as_int_list(self):
        self.sub.connect('src.x', 'tgt.x', src_indices=[1])

    def test_src_indices_as_int_array(self):
        self.sub.connect('src.x', 'tgt.x', src_indices=np.zeros(1, dtype=int))

    def test_src_indices_as_float_list(self):
        msg = "src_indices must contain integers, but src_indices for " + \
              "connection from 'src.x' to 'tgt.x' is <.* 'numpy.float64'>."

        with assertRaisesRegex(self, TypeError, msg):
            self.sub.connect('src.x', 'tgt.x', src_indices=[1.0])

    def test_src_indices_as_float_array(self):
        msg = "src_indices must contain integers, but src_indices for " + \
              "connection from 'src.x' to 'tgt.x' is <.* 'numpy.float64'>."

        with assertRaisesRegex(self, TypeError, msg):
            self.sub.connect('src.x', 'tgt.x', src_indices=np.zeros(1))

    def test_src_indices_as_str(self):
        msg = "src_indices must be an index array, " + \
              "did you mean connect('src.x', [tgt.x, cmp.x])?"

        with assertRaisesRegex(self, TypeError, msg):
            self.sub.connect('src.x', 'tgt.x', 'cmp.x')

    def test_already_connected(self):
        msg = "Input 'tgt.x' is already connected to 'src.x'."

        self.sub.connect('src.x', 'tgt.x', src_indices=[1])
        with assertRaisesRegex(self, RuntimeError, msg):
            self.sub.connect('cmp.x', 'tgt.x', src_indices=[1])

    def test_invalid_source(self):
        msg = "Output 'src.z' does not exist for connection " + \
              "in 'sub' from 'src.z' to 'tgt.x'."

        # source and target names can't be checked until setup
        # because setup is not called until then
        self.sub.connect('src.z', 'tgt.x', src_indices=[1])
        with assertRaisesRegex(self, NameError, msg):
            self.prob.setup(check=False)

    def test_invalid_target(self):
        msg = "Input 'tgt.z' does not exist for connection " + \
              "in 'sub' from 'src.x' to 'tgt.z'."

        # source and target names can't be checked until setup
        # because setup is not called until then
        self.sub.connect('src.x', 'tgt.z', src_indices=[1])
        with assertRaisesRegex(self, NameError, msg):
            self.prob.setup(check=False)

    def test_connect_within_system(self):
        msg = "Output and input are in the same System for connection " + \
              "from 'tgt.y' to 'tgt.x'."

        with assertRaisesRegex(self, RuntimeError, msg):
            self.sub.connect('tgt.y', 'tgt.x', src_indices=[1])

    def test_connect_within_system_with_promotes(self):
        prob = Problem(Group())

        sub = prob.model.add_subsystem('sub', Group())
        sub.add_subsystem('tgt', ExecComp('y = x'), promotes_outputs=['y'])
        sub.connect('y', 'tgt.x', src_indices=[1])

        msg = "Output and input are in the same System for connection " + \
              "in 'sub' from 'y' to 'tgt.x'."

        with assertRaisesRegex(self, RuntimeError, msg):
            prob.setup(check=False)

    def test_connect_units_with_unitless(self):
        prob = Problem(Group())
        prob.model.add_subsystem('px1', IndepVarComp('x1', 100.0))
        prob.model.add_subsystem('src', ExecComp('x2 = 2 * x1', x2={'units': 'degC'}))
        prob.model.add_subsystem('tgt', ExecComp('y = 3 * x', x={'units': 'unitless'}))

        prob.model.connect('px1.x1', 'src.x1')
        prob.model.connect('src.x2', 'tgt.x')

        msg = "Output 'src.x2' with units of 'degC' is connected " \
              "to input 'tgt.x' which has no units."

        with assert_warning(UserWarning, msg):
            prob.setup(check=False)

    def test_connect_incompatible_units(self):
        msg = "Output units of 'degC' for 'src.x2' are incompatible " \
              "with input units of 'm' for 'tgt.x'."

        prob = Problem(Group())
        prob.model.add_subsystem('px1', IndepVarComp('x1', 100.0))
        prob.model.add_subsystem('src', ExecComp('x2 = 2 * x1', x2={'units': 'degC'}))
        prob.model.add_subsystem('tgt', ExecComp('y = 3 * x', x={'units': 'm'}))

        prob.model.connect('px1.x1', 'src.x1')
        prob.model.connect('src.x2', 'tgt.x')

        with assertRaisesRegex(self, RuntimeError, msg):
            prob.setup(check=False)

    def test_connect_units_with_nounits(self):
        prob = Problem(Group())
        prob.model.add_subsystem('px1', IndepVarComp('x1', 100.0))
        prob.model.add_subsystem('src', ExecComp('x2 = 2 * x1'))
        prob.model.add_subsystem('tgt', ExecComp('y = 3 * x', x={'units': 'degC'}))

        prob.model.connect('px1.x1', 'src.x1')
        prob.model.connect('src.x2', 'tgt.x')

        prob.set_solver_print(level=0)

        msg = "Input 'tgt.x' with units of 'degC' is " \
              "connected to output 'src.x2' which has no units."

        with assert_warning(UserWarning, msg):
            prob.setup(check=False)

        prob.run_model()

        assert_rel_error(self, prob['tgt.y'], 600.)

    def test_connect_units_with_nounits_prom(self):
        prob = Problem(Group())
        prob.model.add_subsystem('px1', IndepVarComp('x', 100.0), promotes_outputs=['x'])
        prob.model.add_subsystem('src', ExecComp('y = 2 * x'), promotes=['x', 'y'])
        prob.model.add_subsystem('tgt', ExecComp('z = 3 * y', y={'units': 'degC'}), promotes=['y'])

        prob.set_solver_print(level=0)

        msg = "Input 'tgt.y' with units of 'degC' is " \
              "connected to output 'src.y' which has no units."

        with assert_warning(UserWarning, msg):
            prob.setup(check=False)

        prob.run_model()

        assert_rel_error(self, prob['tgt.z'], 600.)

    def test_mix_promotes_types(self):
        prob = Problem()
        prob.model.add_subsystem('src', ExecComp(['y = 2 * x', 'y2 = 3 * x']),
                                 promotes=['x', 'y'], promotes_outputs=['y2'])

        with self.assertRaises(RuntimeError) as context:
            prob.setup(check=False)

        self.assertEqual(str(context.exception),
                         "src: 'promotes' cannot be used at the same time as "
                         "'promotes_inputs' or 'promotes_outputs'.")

    def test_mix_promotes_types2(self):
        prob = Problem()
        prob.model.add_subsystem('src', ExecComp(['y = 2 * x', 'y2 = 3 * x2']),
                                 promotes=['x', 'y'], promotes_inputs=['x2'])
        with self.assertRaises(RuntimeError) as context:
            prob.setup(check=False)

        self.assertEqual(str(context.exception),
                         "src: 'promotes' cannot be used at the same time as "
                         "'promotes_inputs' or 'promotes_outputs'.")

    def test_nested_nested_conn(self):
        prob = Problem()
        root = prob.model

        root.add_subsystem('p', IndepVarComp('x', 1.0))

        G1 = root.add_subsystem('G1', Group())
        par1 = G1.add_subsystem('par1', Group())

        par1.add_subsystem('c2', ExecComp('y = x * 2.0'))
        par1.add_subsystem('c4', ExecComp('y = x * 4.0'))

        prob.model.add_design_var('p.x')
        prob.model.add_constraint('G1.par1.c4.y', upper=0.0)

        root.connect('p.x', 'G1.par1.c2.x')
        root.connect('G1.par1.c2.y', 'G1.par1.c4.x')

        prob.setup(check=False)
        prob.run_driver()

        assert_rel_error(self, prob['G1.par1.c4.y'], 8.0)

    def test_bad_shapes(self):
        self.sub.connect('src.s', 'arr.x')

        msg = ("The source and target shapes do not match or are ambiguous for the connection "
               "'sub.src.s' to 'sub.arr.x'.")

        with assertRaisesRegex(self, ValueError, msg):
            self.prob.setup(check=False)

    def test_bad_indices_shape(self):
        p = Problem()
        p.model.add_subsystem('IV', IndepVarComp('x', np.arange(12).reshape((4, 3))))
        p.model.add_subsystem('C1', ExecComp('y=sum(x)*2.0', x=np.zeros((2, 2))))

        p.model.connect('IV.x', 'C1.x', src_indices=[(1, 1)])

        msg = (r"The source indices \[\[1 1\]\] do not specify a valid shape for "
               r"the connection 'IV.x' to 'C1.x'. The target "
               r"shape is \(2.*, 2.*\) but indices are \(1.*, 2.*\).")

        with assertRaisesRegex(self, ValueError, msg):
            p.setup(check=False)

    def test_bad_indices_dimensions(self):
        self.sub.connect('src.x', 'arr.x', src_indices=[(2, -1, 2), (2, 2, 2)],
                         flat_src_indices=False)

        msg = ("The source indices [[ 2 -1  2] [ 2  2  2]] do not specify a "
               "valid shape for the connection 'sub.src.x' to 'sub.arr.x'. "
               "The source has 2 dimensions but the indices expect 3.")

        try:
            self.prob.setup(check=False)
        except ValueError as err:
            self.assertEqual(str(err), msg)
        else:
            self.fail('Exception expected.')

    def test_bad_indices_index(self):
        # the index value within src_indices is outside the valid range for the source
        self.sub.connect('src.x', 'arr.x', src_indices=[(2, -1), (4, 4)],
                         flat_src_indices=False)

        msg = ("The source indices do not specify a valid index for the "
               "connection 'sub.src.x' to 'sub.arr.x'. Index '4' "
               "is out of range for source dimension of size 3.")

        try:
            self.prob.setup(check=False)
        except ValueError as err:
            self.assertEqual(str(err), msg)
        else:
            self.fail('Exception expected.')

    def test_src_indices_shape(self):
        src_indices_model(src_shape=(3, 3), tgt_shape=(2, 2),
                          src_indices=[[4, 5], [7, 8]],
                          flat_src_indices=True)

    def test_src_indices_shape_bad_idx_flat(self):
        try:
            src_indices_model(src_shape=(3, 3), tgt_shape=(2, 2),
                              src_indices=[[4, 5], [7, 9]],
                              flat_src_indices=True)
        except Exception as err:
            self.assertEqual(str(err), "The source indices do not specify a valid index "
                                       "for the connection 'indeps.x' to 'C1.x'. "
                                       "Index '9' is out of range for a flat source of size 9.")
        else:
            self.fail("Exception expected.")

    def test_src_indices_shape_bad_idx_flat_promotes(self):
        try:
            src_indices_model(src_shape=(3, 3), tgt_shape=(2, 2),
                              src_indices=[[4, 5], [7, 9]],
                              flat_src_indices=True, promotes=['x'])
        except Exception as err:
            self.assertEqual(str(err), "The source indices do not specify a valid index "
                                       "for the connection 'indeps.x' to 'C1.x'. "
                                       "Index '9' is out of range for a flat source of size 9.")
        else:
            self.fail("Exception expected.")

    def test_src_indices_shape_bad_idx_flat_neg(self):
        try:
            src_indices_model(src_shape=(3, 3), tgt_shape=(2, 2),
                              src_indices=[[-10, 5], [7, 8]],
                              flat_src_indices=True)
        except Exception as err:
            self.assertEqual(str(err), "The source indices do not specify a valid index "
                                       "for the connection 'indeps.x' to 'C1.x'. "
                                       "Index '-10' is out of range for a flat source of size 9.")
        else:
            self.fail("Exception expected.")


if __name__ == "__main__":
    unittest.main()
