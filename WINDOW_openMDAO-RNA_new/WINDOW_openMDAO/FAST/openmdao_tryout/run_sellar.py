import numpy as np
from openmdao.api import Problem, Group, NonlinearBlockGS,ScipyOptimizeDriver, ExecComp, IndepVarComp, view_model

from sellar_disciplines import SellarDis1, SellarDis2

class SellarMDAConnect(Group):
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
        self.connect('d1.y1', ['obj_cmp.y1', 'con_cmp1.y1'])
        self.connect('d2.y2', ['obj_cmp.y2', 'con_cmp2.y2'])

prob = Problem()

prob.model = SellarMDAConnect()

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
# prob.driver.options['maxiter'] = 100
prob.driver.options['tol'] = 1e-8

prob.model.add_design_var('x', lower=0, upper=10)
prob.model.add_design_var('z', lower=0, upper=10)
prob.model.add_objective('obj_cmp.obj')
prob.model.add_constraint('con_cmp1.con1', upper=0)
prob.model.add_constraint('con_cmp2.con2', upper=0)

prob.setup()
prob.set_solver_print(level=0)

# Ask OpenMDAO to finite-difference across the model to compute the gradients for the optimizer
prob.model.approx_totals()

prob.run_driver()

print('minimum found at')
print(prob['x'][0])
print(prob['z'])

print('minumum objective')
print(prob['obj_cmp.obj'][0])

