from __future__ import print_function, division
import unittest
import numpy as np

from openmdao.api import Group, IndepVarComp, ExecComp, NonlinearBlockGS
from openmdao.test_suite.components.sellar import SellarDis1, SellarDis2

from openmdao.utils.assert_utils import assert_rel_error



class TestSellarMDAPromoteConnect(unittest.TestCase):

    def test_sellar_mda_promote(self):
        import numpy as np
        from openmdao.api import Problem, Group, IndepVarComp, ExecComp, NonlinearBlockGS
        from openmdao.test_suite.components.sellar import SellarDis1, SellarDis2

        class SellarMDA(Group):
            """
            Group containing the Sellar MDA.
            """

            def setup(self):
                indeps = self.add_subsystem('indeps', IndepVarComp(), promotes=['*'])
                indeps.add_output('x', 1.0)
                indeps.add_output('z', np.array([5.0, 2.0]))

                cycle = self.add_subsystem('cycle', Group(), promotes=['*'])
                cycle.add_subsystem('d1', SellarDis1(), promotes_inputs=['x', 'z', 'y2'], promotes_outputs=['y1'])
                cycle.add_subsystem('d2', SellarDis2(), promotes_inputs=['z', 'y1'], promotes_outputs=['y2'])

                # Nonlinear Block Gauss Seidel is a gradient free solver
                cycle.nonlinear_solver = NonlinearBlockGS()

                self.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                   z=np.array([0.0, 0.0]), x=0.0),
                                   promotes=['x', 'z', 'y1', 'y2', 'obj'])

                self.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'), promotes=['con1', 'y1'])
                self.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'), promotes=['con2', 'y2'])


        prob = Problem()

        prob.model = SellarMDA()

        prob.setup()

        prob['x'] = 2.
        prob['z'] = [-1., -1.]

        prob.run_model()

        assert_rel_error(self, (prob['y1'][0], prob['y2'][0], prob['obj'][0], prob['con1'][0], prob['con2'][0]),
                         (2.10951651, -0.54758253,  6.8385845,  1.05048349, -24.54758253), 1e-5)


    def test_sellar_mda_connect(self):
        import numpy as np
        from openmdao.api import Problem, Group, IndepVarComp, ExecComp, NonlinearBlockGS
        from openmdao.test_suite.components.sellar import SellarDis1, SellarDis2

        class SellarMDAConnect(Group):
            """
            Group containing the Sellar MDA. This version uses the disciplines without derivatives.
            """

            def setup(self):
                indeps = self.add_subsystem('indeps', IndepVarComp())
                indeps.add_output('x', 1.0)
                indeps.add_output('z', np.array([5.0, 2.0]))

                cycle = self.add_subsystem('cycle', Group())
                cycle.add_subsystem('d1', SellarDis1())
                cycle.add_subsystem('d2', SellarDis2())
                cycle.connect('d1.y1', 'd2.y1')
                cycle.connect('d2.y2', 'd1.y2')

                # Nonlinear Block Gauss Seidel is a gradient free solver
                cycle.nonlinear_solver = NonlinearBlockGS()

                self.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                       z=np.array([0.0, 0.0]), x=0.0))

                self.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'))
                self.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'))

                self.connect('indeps.x', ['cycle.d1.x', 'obj_cmp.x'])
                self.connect('indeps.z', ['cycle.d1.z', 'cycle.d2.z', 'obj_cmp.z'])
                self.connect('cycle.d1.y1', ['obj_cmp.y1', 'con_cmp1.y1'])
                self.connect('cycle.d2.y2', ['obj_cmp.y2', 'con_cmp2.y2'])

        prob = Problem()

        prob.model = SellarMDAConnect()

        prob.setup()

        prob['indeps.x'] = 2.
        prob['indeps.z'] = [-1., -1.]

        prob.run_model()

        assert_rel_error(self, (prob['cycle.d1.y1'][0], prob['cycle.d2.y2'][0], prob['obj_cmp.obj'][0], prob['con_cmp1.con1'][0], prob['con_cmp2.con2'][0]),
                         (2.10951651, -0.54758253, 6.8385845, 1.05048349, -24.54758253), 1e-5)


    def test_sellar_mda_promote_connect(self):
        import numpy as np

        from openmdao.api import Problem, Group, IndepVarComp, ExecComp, NonlinearBlockGS
        from openmdao.test_suite.components.sellar import SellarDis1, SellarDis2

        class SellarMDAPromoteConnect(Group):
            """
            Group containing the Sellar MDA. This version uses the disciplines without derivatives.
            """

            def setup(self):
                indeps = self.add_subsystem('indeps', IndepVarComp(), promotes=['*'])
                indeps.add_output('x', 1.0)
                indeps.add_output('z', np.array([5.0, 2.0]))

                cycle = self.add_subsystem('cycle', Group(), promotes=['*'])
                cycle.add_subsystem('d1', SellarDis1())
                cycle.add_subsystem('d2', SellarDis2())
                cycle.connect('d1.y1', 'd2.y1')
                cycle.connect('d2.y2', 'd1.y2')

                # Nonlinear Block Gauss Seidel is a gradient free solver
                cycle.nonlinear_solver = NonlinearBlockGS()

                self.add_subsystem('obj_cmp', ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                       z=np.array([0.0, 0.0]), x=0.0))

                self.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'))
                self.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'))

                self.connect('x', ['d1.x', 'obj_cmp.x'])
                self.connect('z', ['d1.z', 'd2.z', 'obj_cmp.z'])
                self.connect('d1.y1', ['con_cmp1.y1', 'obj_cmp.y1'])
                self.connect('d2.y2', ['con_cmp2.y2', 'obj_cmp.y2'])


        prob = Problem()

        prob.model = SellarMDAPromoteConnect()

        prob.setup()

        prob['x'] = 2.
        prob['z'] = [-1., -1.]

        prob.run_model()

        assert_rel_error(self, (prob['d1.y1'][0], prob['d2.y2'][0], prob['obj_cmp.obj'][0], prob['con_cmp1.con1'][0], prob['con_cmp2.con2'][0]),
                         (2.10951651, -0.54758253, 6.8385845, 1.05048349, -24.54758253), 1e-5)


if __name__ == "__main__":
    unittest.main()
