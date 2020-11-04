""" Unit tests for the SqliteCaseReader. """
from __future__ import print_function

import errno
import os
import unittest

from shutil import rmtree
from tempfile import mkdtemp, mkstemp
from collections import OrderedDict

import numpy as np
from six import iteritems, assertRaisesRegex

from openmdao.api import Problem, Group, IndepVarComp, ExecComp, \
    NonlinearRunOnce, NonlinearBlockGS, LinearBlockGS, ScipyOptimizeDriver
from openmdao.recorders.sqlite_recorder import SqliteRecorder, format_version
from openmdao.recorders.case_reader import CaseReader
from openmdao.recorders.sqlite_reader import SqliteCaseReader
from openmdao.core.tests.test_units import SpeedComp
from openmdao.test_suite.components.expl_comp_array import TestExplCompArray
from openmdao.test_suite.components.paraboloid import Paraboloid
from openmdao.test_suite.components.sellar import SellarDerivativesGrouped, \
    SellarDis1withDerivatives, SellarDis2withDerivatives, SellarProblem
from openmdao.utils.assert_utils import assert_rel_error, assert_warning
from openmdao.utils.general_utils import set_pyoptsparse_opt, determine_adder_scaler

from openmdao.solvers.linear.scipy_iter_solver import ScipyKrylov
from openmdao.solvers.nonlinear.newton import NewtonSolver
from openmdao.solvers.linesearch.backtracking import ArmijoGoldsteinLS
from openmdao.test_suite.components.implicit_newton_linesearch import ImplCompTwoStates

# check that pyoptsparse is installed
OPT, OPTIMIZER = set_pyoptsparse_opt('SLSQP')
if OPTIMIZER:
    from openmdao.drivers.pyoptsparse_driver import pyOptSparseDriver


def count_keys(d):
    """
    Count the number of keys in the nested dictionary.

    Parameters
    ----------
    d : nested OrderedDict
        The dictionary of cases to be counted.
    """
    count = 0

    for k in d:
        count += 1
        if isinstance(d[k], OrderedDict):
            count += count_keys(d[k])

    return count


class TestSqliteCaseReader(unittest.TestCase):

    def setUp(self):
        self.orig_dir = os.getcwd()
        self.temp_dir = mkdtemp()
        os.chdir(self.temp_dir)

        self.filename = os.path.join(self.temp_dir, "sqlite_test")
        self.recorder = SqliteRecorder(self.filename, record_viewer_data=False)

    def tearDown(self):
        os.chdir(self.orig_dir)
        try:
            rmtree(self.temp_dir)
        except OSError as e:
            # If directory already deleted, keep going
            if e.errno not in (errno.ENOENT, errno.EACCES, errno.EPERM):
                raise e

    def test_bad_filetype(self):
        # Pass a plain text file.
        fd, filepath = mkstemp()
        with os.fdopen(fd, 'w') as tmp:
            tmp.write("Lorem ipsum")
            tmp.close()

        with self.assertRaises(IOError) as cm:
            CaseReader(filepath)

        msg = 'File does not contain a valid sqlite database'
        self.assertTrue(str(cm.exception).startswith(msg))

    def test_bad_filename(self):
        # Pass a nonexistent file.
        with self.assertRaises(IOError) as cm:
            CaseReader('junk.sql')

        self.assertTrue(str(cm.exception).startswith('File does not exist'))

    def test_format_version(self):
        prob = SellarProblem()
        prob.model.add_recorder(self.recorder)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)
        self.assertEqual(cr._format_version, format_version,
                         msg='format version not read correctly')

    def test_reader_instantiates(self):
        """ Test that CaseReader returns an SqliteCaseReader. """
        prob = SellarProblem()
        prob.model.add_recorder(self.recorder)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)
        self.assertTrue(isinstance(cr, SqliteCaseReader),
                        msg='CaseReader not returning the correct subclass.')

    def test_invalid_source(self):
        """ Tests that the reader returns params correctly. """
        prob = SellarProblem(SellarDerivativesGrouped)

        driver = prob.driver

        driver.recording_options['record_desvars'] = False
        driver.recording_options['record_responses'] = False
        driver.recording_options['record_objectives'] = False
        driver.recording_options['record_constraints'] = False
        driver.recording_options['record_derivatives'] = False
        driver.add_recorder(self.recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # check that driver is our only source
        self.assertEqual(cr.list_sources(), ['driver'])

        # check source vars
        source_vars = cr.list_source_vars('driver')
        self.assertEqual(sorted(source_vars['inputs']), [])
        self.assertEqual(sorted(source_vars['outputs']), [])

        with assertRaisesRegex(self, RuntimeError, "No cases recorded for problem"):
            cr.list_source_vars('problem')

        with assertRaisesRegex(self, RuntimeError, "Source not found: root"):
            cr.list_source_vars('root')

        with assertRaisesRegex(self, RuntimeError, "Source not found: root.nonlinear_solver"):
            cr.list_source_vars('root.nonlinear_solver')

        # check list cases
        with assertRaisesRegex(self, RuntimeError, "Source not found: foo"):
            cr.list_cases('foo')

        with assertRaisesRegex(self, TypeError, "Source parameter must be a string, 999 is type int"):
            cr.list_cases(999)

    def test_reading_driver_cases(self):
        """ Tests that the reader returns params correctly. """
        prob = SellarProblem(SellarDerivativesGrouped)

        driver = prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)

        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_responses'] = True
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True
        driver.recording_options['record_derivatives'] = True
        driver.add_recorder(self.recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # check that we only have driver cases
        self.assertEqual(cr.list_sources(), ['driver'])

        # check source vars
        source_vars = cr.list_source_vars('driver')
        self.assertEqual(sorted(source_vars['inputs']), [])
        self.assertEqual(sorted(source_vars['outputs']), ['con1', 'con2', 'obj', 'x', 'z'])

        # check that we got the correct number of cases
        driver_cases = cr.list_cases('driver')

        self.assertEqual(driver_cases, [
            'rank0:SLSQP|0', 'rank0:SLSQP|1', 'rank0:SLSQP|2',
            'rank0:SLSQP|3', 'rank0:SLSQP|4', 'rank0:SLSQP|5',
            'rank0:SLSQP|6'
        ])

        # Test to see if the access by case keys works:
        seventh_slsqp_iteration_case = cr.get_case('rank0:SLSQP|6')
        np.testing.assert_almost_equal(seventh_slsqp_iteration_case.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        deriv_case = cr.get_case('rank0:SLSQP|4')
        np.testing.assert_almost_equal(deriv_case.jacobian['obj', 'pz.z'],
                                       [[3.8178954, 1.73971323]], decimal=2)

        # While thinking about derivatives, let's get them all.
        derivs = deriv_case.jacobian

        self.assertEqual(set(derivs.keys()), set([
            ('obj', 'z'), ('con2', 'z'), ('con1', 'x'),
            ('obj', 'x'), ('con2', 'x'), ('con1', 'z')
        ]))

        # Test values from the last case
        last_case = cr.get_case(driver_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['z'], prob['z'])
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # Test to see if the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(driver_cases):
            self.assertEqual(iter_coord, 'rank0:SLSQP|{}'.format(i))

    def test_reading_system_cases(self):
        prob = SellarProblem()
        model = prob.model

        model.recording_options['record_inputs'] = True
        model.recording_options['record_outputs'] = True
        model.recording_options['record_residuals'] = True
        model.recording_options['record_metadata'] = False

        model.add_recorder(self.recorder)

        prob.setup()

        model.nonlinear_solver.options['use_apply_nonlinear'] = True

        model.d1.add_recorder(self.recorder)  # SellarDis1withDerivatives (an ExplicitComp)
        model.obj_cmp.add_recorder(self.recorder)  # an ExecComp

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # check that we only have the three system sources
        self.assertEqual(sorted(cr.list_sources()), ['root', 'root.d1', 'root.obj_cmp'])

        # check source vars
        source_vars = cr.list_source_vars('root')
        self.assertEqual(sorted(source_vars['inputs']), ['x', 'y1', 'y2', 'z'])
        self.assertEqual(sorted(source_vars['outputs']), ['con1', 'con2', 'obj', 'x', 'y1', 'y2', 'z'])

        source_vars = cr.list_source_vars('root.d1')
        self.assertEqual(sorted(source_vars['inputs']), ['x', 'y2', 'z'])
        self.assertEqual(sorted(source_vars['outputs']), ['y1'])

        source_vars = cr.list_source_vars('root.obj_cmp')
        self.assertEqual(sorted(source_vars['inputs']), ['x', 'y1', 'y2', 'z'])
        self.assertEqual(sorted(source_vars['outputs']), ['obj'])

        # Test to see if we got the correct number of cases
        self.assertEqual(len(cr.list_cases('root', recurse=False)), 1)
        self.assertEqual(len(cr.list_cases('root.d1', recurse=False)), 7)
        self.assertEqual(len(cr.list_cases('root.obj_cmp', recurse=False)), 7)

        # Test values from cases
        second_last_case = cr.get_case('rank0:Driver|0|root._solve_nonlinear|0')
        np.testing.assert_almost_equal(second_last_case.inputs['y2'], [12.05848815, ])
        np.testing.assert_almost_equal(second_last_case.outputs['obj'], [28.58830817, ])
        np.testing.assert_almost_equal(second_last_case.residuals['obj'], [0.0, ],)

        # Test to see if the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(cr.list_cases('root.d1', recurse=False)):
            self.assertEqual(iter_coord,
                             'rank0:Driver|0|root._solve_nonlinear|0|NonlinearBlockGS|{iter}|'
                             'd1._solve_nonlinear|{iter}'.format(iter=i))

        for i, iter_coord in enumerate(cr.list_cases('root.obj_cmp', recurse=False)):
            self.assertEqual(iter_coord,
                             'rank0:Driver|0|root._solve_nonlinear|0|NonlinearBlockGS|{iter}|'
                             'obj_cmp._solve_nonlinear|{iter}'.format(iter=i))

    def test_reading_solver_cases(self):
        prob = SellarProblem()
        prob.setup()

        solver = prob.model.nonlinear_solver
        solver.add_recorder(self.recorder)

        solver.recording_options['record_abs_error'] = True
        solver.recording_options['record_rel_error'] = True
        solver.recording_options['record_solver_residuals'] = True

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # check that we only have the one solver source
        self.assertEqual(sorted(cr.list_sources()), ['root.nonlinear_solver'])

        # check source vars
        source_vars = cr.list_source_vars('root.nonlinear_solver')
        self.assertEqual(sorted(source_vars['inputs']), ['x', 'y1', 'y2', 'z'])
        self.assertEqual(sorted(source_vars['outputs']), ['con1', 'con2', 'obj', 'x', 'y1', 'y2', 'z'])

        # Test to see if we got the correct number of cases
        solver_cases = cr.list_cases('root.nonlinear_solver')
        self.assertEqual(len(solver_cases), 7)

        # Test values from cases
        last_case = cr.get_case(solver_cases[-1])
        np.testing.assert_almost_equal(last_case.abs_err, [0.0, ])
        np.testing.assert_almost_equal(last_case.rel_err, [0.0, ])
        np.testing.assert_almost_equal(last_case.outputs['x'], [1.0, ])
        np.testing.assert_almost_equal(last_case.residuals['con2'], [0.0, ])

        # check that the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(solver_cases):
            self.assertEqual(iter_coord,
                             'rank0:Driver|0|root._solve_nonlinear|0|NonlinearBlockGS|%d' % i)

    def test_reading_metadata(self):
        prob = Problem()
        model = prob.model

        # the Sellar problem but with units
        model.add_subsystem('px', IndepVarComp('x', 1.0, units='m', lower=-1000, upper=1000),
                            promotes=['x'])
        model.add_subsystem('pz', IndepVarComp('z', np.array([5.0, 2.0])), promotes=['z'])
        model.add_subsystem('d1', SellarDis1withDerivatives(), promotes=['x', 'z', 'y1', 'y2'])
        model.add_subsystem('d2', SellarDis2withDerivatives(), promotes=['z', 'y1', 'y2'])
        model.add_subsystem('obj_cmp',
                            ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                     z=np.array([0.0, 0.0]),
                                     x={'value': 0.0, 'units': 'm'},
                                     y1={'units': 'm'}, y2={'units': 'cm'}),
                            promotes=['obj', 'x', 'z', 'y1', 'y2'])

        model.add_subsystem('con_cmp1', ExecComp('con1 = 3.16 - y1'), promotes=['con1', 'y1'])
        model.add_subsystem('con_cmp2', ExecComp('con2 = y2 - 24.0'), promotes=['con2', 'y2'])

        model.nonlinear_solver = NonlinearBlockGS(iprint=0)
        model.linear_solver = LinearBlockGS(iprint=0)

        model.add_design_var('z', lower=np.array([-10.0, 0.0]), upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        prob.driver.add_recorder(self.recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        self.assertEqual(cr._output2meta['x']['units'], 'm')
        self.assertEqual(cr._input2meta['obj_cmp.y1']['units'], 'm')
        self.assertEqual(cr._input2meta['obj_cmp.y2']['units'], 'cm')

        self.assertEqual(cr._input2meta['d1.x']['units'], None)
        self.assertEqual(cr._input2meta['d1.y2']['units'], None)
        self.assertEqual(cr._output2meta['d1.y1']['units'], None)

        self.assertEqual(cr._output2meta['x']['explicit'], True)
        self.assertEqual(cr._output2meta['x']['type'], ['output', 'desvar'])

        self.assertEqual(cr._input2meta['obj_cmp.y1']['explicit'], True)
        self.assertEqual(cr._input2meta['obj_cmp.y2']['explicit'], True)

        self.assertEqual(cr._output2meta['x']['lower'], -1000.)
        self.assertEqual(cr._output2meta['x']['upper'], 1000.)
        self.assertEqual(cr._output2meta['y2']['upper'], 1000.)
        self.assertEqual(cr._output2meta['y2']['lower'], 0.1)

    def test_reading_solver_metadata(self):
        prob = SellarProblem(linear_solver=LinearBlockGS())
        prob.setup()

        prob.model.nonlinear_solver.add_recorder(self.recorder)

        d1 = prob.model.d1  # SellarDis1withDerivatives (an ExplicitComponent)
        d1.nonlinear_solver = NonlinearBlockGS(maxiter=5)
        d1.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        metadata = CaseReader(self.filename).solver_metadata

        self.assertEqual(
            sorted(metadata.keys()),
            ['d1.NonlinearBlockGS', 'root.NonlinearBlockGS']
        )
        self.assertEqual(metadata['d1.NonlinearBlockGS']['solver_options']['maxiter'], 5)
        self.assertEqual(metadata['root.NonlinearBlockGS']['solver_options']['maxiter'], 10)

    def test_reading_driver_recording_with_system_vars(self):
        prob = SellarProblem(SellarDerivativesGrouped)

        driver = prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)

        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_responses'] = True
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True
        driver.recording_options['includes'] = ['mda.d2.y2']
        driver.add_recorder(self.recorder)

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # Test values from the last case
        driver_cases = cr.list_cases('driver')
        last_case = cr.get_case(driver_cases[-1])

        np.testing.assert_almost_equal(last_case.outputs['z'], prob['pz.z'])
        np.testing.assert_almost_equal(last_case.outputs['x'], prob['px.x'])
        np.testing.assert_almost_equal(last_case.outputs['y2'], prob['mda.d2.y2'])

    @unittest.skipIf(OPT is None, "pyoptsparse is not installed")
    @unittest.skipIf(OPTIMIZER is None, "pyoptsparse is not providing SNOPT or SLSQP")
    def test_get_child_cases(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)

        driver = prob.driver = pyOptSparseDriver(optimizer='SLSQP', print_results=False)
        prob.driver.opt_settings['ACC'] = 1e-9
        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_responses'] = True
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True
        driver.add_recorder(self.recorder)

        prob.setup()

        model = prob.model
        model.add_recorder(self.recorder)
        model.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # check driver cases
        expected_coords = [
            'rank0:SLSQP|0',
            'rank0:SLSQP|1',
            'rank0:SLSQP|2',
            'rank0:SLSQP|3',
            'rank0:SLSQP|4',
            'rank0:SLSQP|5',
            'rank0:SLSQP|6'
        ]

        last_counter = 0
        for i, c in enumerate(cr.get_cases()):
            self.assertEqual(c.iteration_coordinate, expected_coords[i])
            self.assertTrue(c.counter > last_counter)
            last_counter = c.counter

        self.assertEqual(i+1, len(expected_coords))

        # check driver cases with recursion, flat
        expected_coords = [
            'rank0:SLSQP|0|root._solve_nonlinear|0|NLRunOnce|0',
            'rank0:SLSQP|0|root._solve_nonlinear|0',
            'rank0:SLSQP|0',
            'rank0:SLSQP|1|root._solve_nonlinear|1|NLRunOnce|0',
            'rank0:SLSQP|1|root._solve_nonlinear|1',
            'rank0:SLSQP|1',
            'rank0:SLSQP|2|root._solve_nonlinear|2|NLRunOnce|0',
            'rank0:SLSQP|2|root._solve_nonlinear|2',
            'rank0:SLSQP|2',
            'rank0:SLSQP|3|root._solve_nonlinear|3|NLRunOnce|0',
            'rank0:SLSQP|3|root._solve_nonlinear|3',
            'rank0:SLSQP|3',
            'rank0:SLSQP|4|root._solve_nonlinear|4|NLRunOnce|0',
            'rank0:SLSQP|4|root._solve_nonlinear|4',
            'rank0:SLSQP|4',
            'rank0:SLSQP|5|root._solve_nonlinear|5|NLRunOnce|0',
            'rank0:SLSQP|5|root._solve_nonlinear|5',
            'rank0:SLSQP|5',
            'rank0:SLSQP|6|root._solve_nonlinear|6|NLRunOnce|0',
            'rank0:SLSQP|6|root._solve_nonlinear|6',
            'rank0:SLSQP|6',
        ]

        last_counter = 0
        for i, c in enumerate(cr.get_cases(recurse=True, flat=True)):
            self.assertEqual(c.iteration_coordinate, expected_coords[i])
            if len(c.iteration_coordinate.split('|')) > 2:
                self.assertEqual(c.parent, expected_coords[i+1])
            else:
                self.assertEqual(c.parent, None)
            self.assertTrue(c.counter > last_counter)
            last_counter = c.counter

        self.assertEqual(i+1, len(expected_coords))

        # check child cases with recursion, flat
        expected_coords = [
            'rank0:SLSQP|0|root._solve_nonlinear|0|NLRunOnce|0',
            'rank0:SLSQP|0|root._solve_nonlinear|0',
            'rank0:SLSQP|0',
        ]

        last_counter = 0
        for i, c in enumerate(cr.get_cases('rank0:SLSQP|0', recurse=True, flat=True)):
            self.assertEqual(c.iteration_coordinate, expected_coords[i])
            self.assertTrue(c.counter > last_counter)
            last_counter = c.counter

        self.assertEqual(i+1, len(expected_coords))

        # check child cases with recursion, nested
        expected_coords = {
            'rank0:SLSQP|0': {
                'rank0:SLSQP|0|root._solve_nonlinear|0': {
                    'rank0:SLSQP|0|root._solve_nonlinear|0|NLRunOnce|0': {}
                },
            }
        }

        cases = cr.get_cases('rank0:SLSQP|0', recurse=True, flat=False)

        count = 0
        for case in cases:
            count += 1
            coord = case.iteration_coordinate
            self.assertTrue(coord in list(expected_coords.keys()))
            for child_case in cases[case]:
                count += 1
                child_coord = child_case.iteration_coordinate
                self.assertTrue(child_coord in expected_coords[coord].keys())
                for grandchild_case in cases[case][child_case]:
                    count += 1
                    grandchild_coord = grandchild_case.iteration_coordinate
                    self.assertTrue(grandchild_coord in expected_coords[coord][child_coord].keys())

        self.assertEqual(count, 3)

    def test_get_child_cases_system(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)
        prob.setup()

        model = prob.model
        model.add_recorder(self.recorder)
        model.nonlinear_solver.add_recorder(self.recorder)
        model.mda.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        parent_coord = 'rank0:SLSQP|2|root._solve_nonlinear|2'
        coord = parent_coord + '|NLRunOnce|0'

        # user scenario: given a case (with coord), get all cases with same parent
        case = cr.get_case(coord)
        self.assertEqual(case.parent, parent_coord)

        expected_coords = [
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|0',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|1',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|2',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|3',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|4',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|5',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|6',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|2|NonlinearBlockGS|7',
            parent_coord + '|NLRunOnce|0',
            parent_coord
        ]

        last_counter = 0
        for i, c in enumerate(cr.get_cases(source=case.parent, recurse=True, flat=True)):
            self.assertEqual(c.iteration_coordinate, expected_coords[i])
            self.assertTrue(c.counter > last_counter)
            last_counter = c.counter
            i += 1

        self.assertEqual(i, len(expected_coords))

    def test_list_cases_recurse(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)
        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=True)
        prob.driver.add_recorder(self.recorder)
        prob.setup()

        model = prob.model
        model.add_recorder(self.recorder)
        model.mda.add_recorder(self.recorder)
        model.nonlinear_solver.add_recorder(self.recorder)
        model.mda.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # get total iteration count to check against
        global_iterations = len(cr._global_iterations)

        #
        # get a recursive list of all cases (flat)
        #
        cases = cr.list_cases(recurse=True, flat=True)

        # verify the cases are all there
        self.assertEqual(len(cases), global_iterations)

        # verify the cases are in proper order
        counter = 0
        for i, c in enumerate(cr.get_case(case) for case in cases):
            counter += 1
            self.assertEqual(c.counter, counter)

        #
        # get a recursive dict of all cases (nested)
        #
        cases = cr.list_cases(recurse=True, flat=False)

        num_cases = count_keys(cases)

        self.assertEqual(num_cases, global_iterations)

        #
        # get a recursive list of child cases
        #
        parent_coord = 'rank0:SLSQP|0|root._solve_nonlinear|0'

        expected_coords = [
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|0',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|1',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|2',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|3',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|4',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|5',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|6',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0',
            parent_coord + '|NLRunOnce|0',
            parent_coord
        ]

        cases = cr.list_cases(parent_coord, recurse=True, flat=True)

        # verify the cases are all there and are as expected
        self.assertEqual(len(cases), len(expected_coords))
        for i, c in enumerate(cases):
            self.assertEqual(c, expected_coords[i])

        #
        # get a list of cases for each source
        #
        sources = cr.list_sources()
        self.assertEqual(sorted(sources), [
            'driver', 'root', 'root.mda', 'root.mda.nonlinear_solver', 'root.nonlinear_solver'
        ])

        # verify the coordinates of the returned cases are all there as expected
        expected_coord = {
            'driver':                    r'rank0:SLSQP\|\d',
            'root':                      r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d',
            'root.nonlinear_solver':     r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d\|NLRunOnce\|0',
            'root.mda':                  r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d\|NLRunOnce\|0\|mda._solve_nonlinear\|\d',
            'root.mda.nonlinear_solver': r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d\|NLRunOnce\|0\|mda._solve_nonlinear\|\d\|NonlinearBlockGS\|\d',
        }
        counter = 0
        mda_counter = 0
        root_counter = 0
        for source in sources:
            expected = expected_coord[source]
            cases = cr.list_cases(source, recurse=False)
            for case in cases:
                counter += 1
                if source.startswith('root.mda'):  # count all cases for/under mda system
                    mda_counter += 1
                if source.startswith('root.'):     # count all cases for/under root solver
                    root_counter += 1
                self.assertRegexpMatches(case, expected)

        self.assertEqual(counter, global_iterations)

        #
        # get a recursive list of child cases for the mda system
        #
        counter = 0

        cases = cr.list_cases('root.mda', recurse=True, flat=True)
        for case in cases:
            self.assertTrue(case.index('|mda._solve_nonlinear|') > 0)
            counter += 1

        self.assertEqual(counter, mda_counter)

        #
        # get a recursive list of child cases for the root solver
        #
        counter = 0

        cases = cr.list_cases('root.nonlinear_solver', recurse=True, flat=True)
        for case in cases:
            self.assertTrue(case.index('|NLRunOnce|') > 0)
            counter += 1

        self.assertEqual(counter, root_counter)

    def test_list_cases_nested_model(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=True)
        prob.setup()

        model = prob.model
        model.add_recorder(self.recorder)
        model.mda.add_recorder(self.recorder)
        model.nonlinear_solver.add_recorder(self.recorder)
        model.mda.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # get total iteration count to check against
        global_iterations = len(cr._global_iterations)

        #
        # get a recursive list of all cases (flat)
        #
        cases = cr.list_cases(recurse=True, flat=True)

        # verify the cases are all there
        self.assertEqual(len(cases), global_iterations)

        # verify the cases are in proper order
        counter = 0
        for i, c in enumerate(cr.get_case(case) for case in cases):
            counter += 1
            self.assertEqual(c.counter, counter)

        #
        # get a recursive dict of all cases (nested)
        #
        cases = cr.list_cases(recurse=True, flat=False)

        num_cases = count_keys(cases)

        self.assertEqual(num_cases, global_iterations)

    def test_list_cases_nested_no_source(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=True)
        prob.setup()

        model = prob.model
        model.mda.add_recorder(self.recorder)
        model.nonlinear_solver.add_recorder(self.recorder)
        model.mda.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # get total iteration count to check against
        global_iterations = len(cr._global_iterations)

        #
        # get a recursive list of all cases (flat)
        #
        cases = cr.list_cases(recurse=True, flat=True)

        # verify the cases are all there
        self.assertEqual(len(cases), global_iterations)

        # verify the cases are in proper order
        counter = 0
        for i, c in enumerate(cr.get_case(case) for case in cases):
            counter += 1
            self.assertEqual(c.counter, counter)

        #
        # try to get a recursive dict of all cases (nested), without driver or model
        #
        expected_err = ("A nested dictionary of all cases was requested, but "
                        "neither the driver or the model was recorded. Please "
                        "specify another source (system or solver) for the cases "
                        "you want to see.")

        with self.assertRaises(RuntimeError) as cm:
            cases = cr.list_cases(recurse=True, flat=False)

        self.assertEqual(str(cm.exception), expected_err)

    def test_get_cases_recurse(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)
        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=True)
        prob.driver.opt_settings['ACC'] = 1e-9
        prob.driver.add_recorder(self.recorder)
        prob.setup()

        model = prob.model
        model.add_recorder(self.recorder)
        model.mda.add_recorder(self.recorder)
        model.nonlinear_solver.add_recorder(self.recorder)
        model.mda.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # get total iteration count to check against
        global_iterations = len(cr._global_iterations)

        #
        # get a recursive list of all cases (flat)
        #
        cases = cr.get_cases(recurse=True, flat=True)

        # verify the cases are all there
        self.assertEqual(len(cases), global_iterations)

        # verify the cases are in proper order
        counter = 0
        for i, c in enumerate(cases):
            counter += 1
            self.assertEqual(c.counter, counter)

        #
        # get a recursive dict of all cases (nested)
        #
        cases = cr.get_cases(recurse=True, flat=False)

        num_cases = count_keys(cases)

        self.assertEqual(num_cases, global_iterations)

        #
        # get a recursive list of child cases
        #
        parent_coord = 'rank0:SLSQP|0|root._solve_nonlinear|0'

        expected_coords = [
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|0',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|1',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|2',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|3',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|4',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|5',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0|NonlinearBlockGS|6',
            parent_coord + '|NLRunOnce|0|mda._solve_nonlinear|0',
            parent_coord + '|NLRunOnce|0',
            parent_coord
        ]

        cases = cr.get_cases(parent_coord, recurse=True, flat=True)

        # verify the cases are all there and are as expected
        self.assertEqual(len(cases), len(expected_coords))
        for i, c in enumerate(cases):
            self.assertEqual(c.iteration_coordinate, expected_coords[i])

        #
        # get a list of cases for each source
        #
        sources = cr.list_sources()
        self.assertEqual(sorted(sources), [
            'driver', 'root', 'root.mda', 'root.mda.nonlinear_solver', 'root.nonlinear_solver'
        ])

        # verify the coordinates of the returned cases are as expected and that the cases are all there
        expected_coord = {
            'driver':                    r'rank0:SLSQP\|\d',
            'root':                      r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d',
            'root.nonlinear_solver':     r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d\|NLRunOnce\|0',
            'root.mda':                  r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d\|NLRunOnce\|0\|mda._solve_nonlinear\|\d',
            'root.mda.nonlinear_solver': r'rank0:SLSQP\|\d\|root._solve_nonlinear\|\d\|NLRunOnce\|0\|mda._solve_nonlinear\|\d\|NonlinearBlockGS\|\d',
        }
        counter = 0
        mda_counter = 0
        root_counter = 0
        for source in sources:
            expected = expected_coord[source]
            cases = cr.get_cases(source, recurse=False)
            for case in cases:
                counter += 1
                if source.startswith('root.mda'):  # count all cases for/under mda system
                    mda_counter += 1
                if source.startswith('root.'):     # count all cases for/under root solver
                    root_counter += 1
                self.assertRegexpMatches(case.iteration_coordinate, expected)

        self.assertEqual(counter, global_iterations)

        #
        # get a recursive list of child cases for the mda system
        #
        counter = 0
        cases = cr.get_cases('root.mda', recurse=True, flat=True)
        for case in cases:
            counter += 1

        self.assertEqual(counter, mda_counter)

        #
        # get a recursive list of child cases for the root solver
        #
        counter = 0
        cases = cr.get_cases('root.nonlinear_solver', recurse=True, flat=True)
        for case in cases:
            counter += 1

        self.assertEqual(counter, root_counter)

    def test_list_outputs(self):
        prob = SellarProblem()

        prob.model.add_recorder(self.recorder)
        prob.model.recording_options['record_residuals'] = True

        prob.setup()

        d1 = prob.model.d1  # SellarDis1withDerivatives (an ExplicitComp)
        d1.nonlinear_solver = NonlinearBlockGS(maxiter=5)
        d1.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        # check the system case for 'd1' (there should be only one output, 'd1.y1')
        system_cases = cr.list_cases('root.d1')
        case = cr.get_case(system_cases[1])

        outputs = case.list_outputs(explicit=True, implicit=True, values=True,
                                    residuals=True, residuals_tol=None,
                                    units=True, shape=True, bounds=True,
                                    scaling=True, hierarchical=True, print_arrays=True,
                                    out_stream=None)

        expected_outputs = {
            'd1.y1': {
                'lower': 0.1,
                'upper': 1000.,
                'ref': 1.0,
                'resids': [1.318e-10],
                'shape': (1,),
                'values': [25.5454859]
            }
        }

        self.assertEqual(len(outputs), 1)
        [name, vals] = outputs[0]
        self.assertEqual(name, 'd1.y1')

        expected = expected_outputs[name]
        self.assertEqual(vals['lower'], expected['lower'])
        self.assertEqual(vals['ref'], expected['ref'])
        self.assertEqual(vals['shape'], expected['shape'])
        np.testing.assert_almost_equal(vals['resids'], expected['resids'])
        np.testing.assert_almost_equal(vals['value'], expected['values'])

        # check implicit outputs
        # there should not be any
        impl_outputs_case = case.list_outputs(explicit=False, implicit=True,
                                              out_stream=None)
        self.assertEqual(len(impl_outputs_case), 0)

    def test_list_inputs(self):
        prob = SellarProblem()

        prob.model.add_recorder(self.recorder)
        prob.model.recording_options['record_residuals'] = True

        prob.setup()

        d1 = prob.model.d1  # SellarDis1withDerivatives (an ExplicitComp)
        d1.nonlinear_solver = NonlinearBlockGS(maxiter=5)
        d1.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        expected_inputs_case = {
            'd1.z': {'value': [5., 2.]},
            'd1.x': {'value': [1.]},
            'd1.y2': {'value': [12.27257053]}
        }

        system_cases = cr.list_cases('root.d1')

        case = cr.get_case(system_cases[1])

        inputs_case = case.list_inputs(values=True, units=True, hierarchical=True,
                                       out_stream=None)

        for o in inputs_case:
            vals = o[1]
            name = o[0]
            expected = expected_inputs_case[name]
            np.testing.assert_almost_equal(vals['value'], expected['value'])

    def test_get_vars(self):
        prob = SellarProblem()
        prob.setup()

        prob.model.add_recorder(self.recorder)
        prob.model.recording_options['record_residuals'] = True

        prob.driver.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        driver_cases = cr.list_cases('driver')
        driver_case = cr.get_case(driver_cases[0])

        desvars = driver_case.get_design_vars()
        objectives = driver_case.get_objectives()
        constraints = driver_case.get_constraints()
        responses = driver_case.get_responses()

        expected_desvars = {"x": 1., "z": [5., 2.]}
        expected_objectives = {"obj": 28.58830817, }
        expected_constraints = {"con1": -22.42830237, "con2": -11.94151185}

        expected_responses = expected_objectives.copy()
        expected_responses.update(expected_constraints)

        for expected_set, actual_set in ((expected_desvars, desvars),
                                         (expected_objectives, objectives),
                                         (expected_constraints, constraints),
                                         (expected_responses, responses)):

            self.assertEqual(len(expected_set), len(actual_set))
            for k in expected_set:
                np.testing.assert_almost_equal(expected_set[k], actual_set[k])

    def test_simple_load_system_cases(self):
        prob = SellarProblem()

        model = prob.model
        model.recording_options['record_inputs'] = True
        model.recording_options['record_outputs'] = True
        model.recording_options['record_residuals'] = True
        model.add_recorder(self.recorder)

        prob.setup()

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        system_cases = cr.list_cases('root')
        case = cr.get_case(system_cases[0])

        # Add one to all the inputs and outputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in model._inputs:
            model._inputs[name] += 1.0
        for name in model._outputs:
            model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(case)

        _assert_model_matches_case(case, model)

    def test_load_bad_system_case(self):
        prob = SellarProblem(SellarDerivativesGrouped)

        prob.model.add_recorder(self.recorder)

        driver = prob.driver = ScipyOptimizeDriver()
        driver.options['optimizer'] = 'SLSQP'
        driver.options['tol'] = 1e-9
        driver.options['disp'] = False
        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_responses'] = True
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        system_cases = cr.list_cases('root')
        case = cr.get_case(system_cases[0])

        # try to load it into a completely different model
        prob = SellarProblem()
        prob.setup()

        error_msg = "Input variable, '[^']+', recorded in the case is not found in the model"
        with assertRaisesRegex(self, KeyError, error_msg):
            prob.load_case(case)

    def test_subsystem_load_system_cases(self):
        prob = SellarProblem()
        prob.setup()

        model = prob.model
        model.recording_options['record_inputs'] = True
        model.recording_options['record_outputs'] = True
        model.recording_options['record_residuals'] = True

        # Only record a subsystem
        model.d2.add_recorder(self.recorder)

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(self.filename)

        system_cases = cr.list_cases('root.d2')
        case = cr.get_case(system_cases[0])

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            model._inputs[name] += 1.0
        for name in prob.model._outputs:
            model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(case)

        _assert_model_matches_case(case, model.d2)

    def test_load_system_cases_with_units(self):
        comp = IndepVarComp()
        comp.add_output('distance', val=1., units='m')
        comp.add_output('time', val=1., units='s')

        prob = Problem()
        model = prob.model
        model.add_subsystem('c1', comp)
        model.add_subsystem('c2', SpeedComp())
        model.add_subsystem('c3', ExecComp('f=speed', speed={'units': 'm/s'}, f={'units': 'm/s'}))
        model.connect('c1.distance', 'c2.distance')
        model.connect('c1.time', 'c2.time')
        model.connect('c2.speed', 'c3.speed')

        model.add_recorder(self.recorder)

        prob.setup()
        prob.run_model()

        cr = CaseReader(self.filename)

        system_cases = cr.list_cases('root')
        case = cr.get_case(system_cases[0])

        # Add one to all the inputs just to change the model
        # so we can see if loading the case values really changes the model
        for name in model._inputs:
            model._inputs[name] += 1.0
        for name in model._outputs:
            model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(case)

        _assert_model_matches_case(case, model)

        # make sure it still runs with loaded values
        prob.run_model()

        # make sure the loaded unit strings are compatible with `convert_units`
        from openmdao.utils.units import convert_units
        outputs = case.list_outputs(explicit=True, implicit=True, values=True,
                                    units=True, shape=True, out_stream=None)
        meta = {}
        for name, vals in outputs:
            meta[name] = vals

        from_units = meta['c2.speed']['units']
        to_units = meta['c3.f']['units']

        self.assertEqual(from_units, 'km/h')
        self.assertEqual(to_units, 'm/s')

        self.assertEqual(convert_units(10., from_units, to_units), 10000./3600.)

    def test_optimization_load_system_cases(self):
        prob = SellarProblem(SellarDerivativesGrouped)

        prob.model.add_recorder(self.recorder)

        driver = prob.driver = ScipyOptimizeDriver()
        driver.options['optimizer'] = 'SLSQP'
        driver.options['tol'] = 1e-9
        driver.options['disp'] = False
        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_responses'] = True
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        inputs_before = prob.model.list_inputs(values=True, units=True, out_stream=None)
        outputs_before = prob.model.list_outputs(values=True, units=True, out_stream=None)

        cr = CaseReader(self.filename)

        # get third case
        system_cases = cr.list_cases('root')
        third_case = cr.get_case(system_cases[2])

        iter_count_before = driver.iter_count

        # run the model again with a fresh model
        prob = SellarProblem(SellarDerivativesGrouped)

        driver = prob.driver = ScipyOptimizeDriver()
        driver.options['optimizer'] = 'SLSQP'
        driver.options['tol'] = 1e-9
        driver.options['disp'] = False

        prob.setup()
        prob.load_case(third_case)
        prob.run_driver()
        prob.cleanup()

        inputs_after = prob.model.list_inputs(values=True, units=True, out_stream=None)
        outputs_after = prob.model.list_outputs(values=True, units=True, out_stream=None)

        iter_count_after = driver.iter_count

        for before, after in zip(inputs_before, inputs_after):
            np.testing.assert_almost_equal(before[1]['value'], after[1]['value'])

        for before, after in zip(outputs_before, outputs_after):
            np.testing.assert_almost_equal(before[1]['value'], after[1]['value'])

        # Should take one less iteration since we gave it a head start in the second run
        self.assertEqual(iter_count_before, iter_count_after + 1)

    def test_load_solver_cases(self):
        prob = SellarProblem()
        prob.setup()

        model = prob.model
        model.nonlinear_solver.add_recorder(self.recorder)

        fail = prob.run_driver()
        prob.cleanup()

        self.assertFalse(fail, 'Problem failed to converge')

        cr = CaseReader(self.filename)

        solver_cases = cr.list_cases('root.nonlinear_solver')
        case = cr.get_case(solver_cases[0])

        # Add one to all the inputs just to change the model
        # so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            model._inputs[name] += 1.0
        for name in prob.model._outputs:
            model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(case)

        _assert_model_matches_case(case, model)

    def test_load_driver_cases(self):
        prob = Problem()
        model = prob.model

        model.add_subsystem('p1', IndepVarComp('x', 50.0), promotes=['*'])
        model.add_subsystem('p2', IndepVarComp('y', 50.0), promotes=['*'])
        model.add_subsystem('comp', Paraboloid(), promotes=['*'])
        model.add_subsystem('con', ExecComp('c = x - y'), promotes=['*'])

        model.add_design_var('x', lower=-50.0, upper=50.0)
        model.add_design_var('y', lower=-50.0, upper=50.0)

        model.add_objective('f_xy')
        model.add_constraint('c', lower=15.0)

        prob.driver.add_recorder(self.recorder)
        prob.driver.recording_options['includes'] = ['*']

        prob.set_solver_print(0)

        prob.setup()
        fail = prob.run_driver()
        prob.cleanup()

        self.assertFalse(fail, 'Problem failed to converge')

        cr = CaseReader(self.filename)

        driver_cases = cr.list_cases('driver')
        case = cr.get_case(driver_cases[0])

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            prob.model._inputs[name] += 1.0
        for name in prob.model._outputs:
            prob.model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(case)

        _assert_model_matches_case(case, model)

    def test_system_options_pickle_fail(self):
        # simple paraboloid model
        model = Group()
        ivc = IndepVarComp()
        ivc.add_output('x', 3.0)
        model.add_subsystem('subs', ivc)
        subs = model.subs

        # declare two options
        subs.options.declare('options value 1', 1)
        # Given object which can't be pickled
        subs.options.declare('options value to fail', (i for i in []))
        subs.add_recorder(self.recorder)

        prob = Problem(model)
        prob.setup()

        msg = "Trying to record options which cannot be pickled on system with name: subs. " \
              "Use the 'options_excludes' recording option on system objects to avoid " \
              "attempting to record options which cannot be pickled. Skipping recording " \
              "options for this system."
        with assert_warning(RuntimeWarning, msg):
            prob.run_model()

        prob.cleanup()
        cr = CaseReader(self.filename)
        subs_options = cr.system_metadata['subs']['component_options']

        # no options should have been recorded for d1
        self.assertEqual(len(subs_options._dict), 0)

    def test_pre_load(self):
        prob = SellarProblem()
        prob.setup()

        recorder = SqliteRecorder(self.filename)

        prob.add_recorder(recorder)
        prob.driver.add_recorder(recorder)
        prob.model.add_recorder(recorder)
        prob.model.nonlinear_solver.add_recorder(recorder)

        prob.run_driver()
        prob.record_iteration('c_1')
        prob.record_iteration('c_2')
        prob.cleanup()

        # without pre_load, we should get format_version and metadata but no cases
        cr = CaseReader(self.filename, pre_load=False)

        num_driver_cases = len(cr.list_cases('driver', recurse=False))
        num_system_cases = len(cr.list_cases('root', recurse=False))
        num_solver_cases = len(cr.list_cases('root.nonlinear_solver', recurse=False))
        num_problem_cases = len(cr.list_cases('problem'))

        self.assertEqual(num_driver_cases, 1)
        self.assertEqual(num_system_cases, 1)
        self.assertEqual(num_solver_cases, 7)
        self.assertEqual(num_problem_cases, 2)

        self.assertEqual(cr._format_version, format_version)

        self.assertEqual(set(cr.system_metadata.keys()),
                         set(['root'] + [sys.name for sys in prob.model._subsystems_allprocs]))

        self.assertEqual(sorted(cr.problem_metadata.keys()),
                         ['abs2prom', 'connections_list', 'tree', 'variables'])

        self.assertEqual(len(cr._driver_cases._cases), 0)
        self.assertEqual(len(cr._system_cases._cases), 0)
        self.assertEqual(len(cr._solver_cases._cases), 0)
        self.assertEqual(len(cr._problem_cases._cases), 0)

        # with pre_load, we should get format_version, metadata and all cases
        cr = CaseReader(self.filename, pre_load=True)

        num_driver_cases = len(cr.list_cases('driver', recurse=False))
        num_system_cases = len(cr.list_cases('root', recurse=False))
        num_solver_cases = len(cr.list_cases('root.nonlinear_solver', recurse=False))
        num_problem_cases = len(cr.list_cases('problem'))

        self.assertEqual(num_driver_cases, 1)
        self.assertEqual(num_system_cases, 1)
        self.assertEqual(num_solver_cases, 7)
        self.assertEqual(num_problem_cases, 2)

        self.assertEqual(cr._format_version, format_version)

        self.assertEqual(set(cr.system_metadata.keys()),
                         set(['root'] + [sys.name for sys in prob.model._subsystems_allprocs]))

        self.assertEqual(set(cr.problem_metadata.keys()),
                         set(['abs2prom', 'connections_list', 'tree', 'variables']))

        self.assertEqual(len(cr._driver_cases._cases), num_driver_cases)
        self.assertEqual(len(cr._system_cases._cases), num_system_cases)
        self.assertEqual(len(cr._solver_cases._cases), num_solver_cases)
        self.assertEqual(len(cr._problem_cases._cases), num_problem_cases)

        for case_type in (cr._driver_cases, cr._solver_cases,
                          cr._system_cases, cr._problem_cases):
            for key in case_type.list_cases():
                self.assertTrue(key in case_type._cases)
                self.assertEqual(key, case_type._cases[key].iteration_coordinate)

    def test_caching_cases(self):
        prob = SellarProblem()
        prob.setup()

        prob.add_recorder(self.recorder)
        prob.driver.add_recorder(self.recorder)
        prob.model.add_recorder(self.recorder)
        prob.model.nonlinear_solver.add_recorder(self.recorder)

        prob.run_driver()
        prob.record_iteration('c_1')
        prob.record_iteration('c_2')
        prob.cleanup()

        cr = CaseReader(self.filename, pre_load=False)

        self.assertEqual(len(cr._driver_cases._cases), 0)
        self.assertEqual(len(cr._system_cases._cases), 0)
        self.assertEqual(len(cr._solver_cases._cases), 0)
        self.assertEqual(len(cr._problem_cases._cases), 0)

        # get cases without caching them
        for case_type in (cr._driver_cases, cr._solver_cases,
                          cr._system_cases, cr._problem_cases):
            for key in case_type.list_cases():
                case_type.get_case(key)

        self.assertEqual(len(cr._driver_cases._cases), 0)
        self.assertEqual(len(cr._system_cases._cases), 0)
        self.assertEqual(len(cr._solver_cases._cases), 0)
        self.assertEqual(len(cr._problem_cases._cases), 0)

        # get cases and cache them
        for case_type in (cr._driver_cases, cr._solver_cases,
                          cr._system_cases, cr._problem_cases):
            for key in case_type.list_cases():
                case_type.get_case(key, cache=True)

        # assert that we have now stored each of the cases
        self.assertEqual(len(cr._driver_cases._cases), 1)
        self.assertEqual(len(cr._system_cases._cases), 1)
        self.assertEqual(len(cr._solver_cases._cases), 7)
        self.assertEqual(len(cr._problem_cases._cases), 2)

        for case_type in (cr._driver_cases, cr._solver_cases,
                          cr._system_cases, cr._problem_cases):
            for key in case_type.list_cases():
                self.assertTrue(key in case_type._cases)
                self.assertEqual(key, case_type._cases[key].iteration_coordinate)

    def test_reading_driver_cases_with_indices(self):
        # note: size must be an even number
        SIZE = 10
        prob = Problem()

        driver = prob.driver = ScipyOptimizeDriver()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['disp'] = False

        prob.driver.add_recorder(self.recorder)
        driver.recording_options['includes'] = ['*']

        model = prob.model
        indeps = model.add_subsystem('indeps', IndepVarComp(), promotes_outputs=['*'])

        # the following were randomly generated using np.random.random(10)*2-1 to randomly
        # disperse them within a unit circle centered at the origin.
        # Also converted this array to > 1D array to test that capability of case recording
        x_vals = np.array([
            0.55994437, -0.95923447, 0.21798656, -0.02158783, 0.62183717,
            0.04007379, 0.46044942, -0.10129622, 0.27720413, -0.37107886
        ]).reshape((-1, 1))

        indeps.add_output('x', x_vals)
        indeps.add_output('y', np.array([
            0.52577864, 0.30894559, 0.8420792, 0.35039912, -0.67290778,
            -0.86236787, -0.97500023, 0.47739414, 0.51174103, 0.10052582
        ]))
        indeps.add_output('r', .7)

        model.add_subsystem('circle', ExecComp('area = pi * r**2'))

        model.add_subsystem('r_con', ExecComp('g = x**2 + y**2 - r**2',
                                              g=np.ones(SIZE), x=np.ones(SIZE), y=np.ones(SIZE)))

        thetas = np.linspace(0, np.pi/4, SIZE)

        model.add_subsystem('theta_con', ExecComp('g=arctan(y/x) - theta',
                                                  g=np.ones(SIZE), x=np.ones(SIZE),
                                                  y=np.ones(SIZE), theta=thetas))
        model.add_subsystem('delta_theta_con', ExecComp('g = arctan(y/x)[::2]-arctan(y/x)[1::2]',
                                                        g=np.ones(SIZE//2), x=np.ones(SIZE),
                                                        y=np.ones(SIZE)))

        model.add_subsystem('l_conx', ExecComp('g=x-1', g=np.ones(SIZE), x=np.ones(SIZE)))

        model.connect('r', ('circle.r', 'r_con.r'))
        model.connect('x', ['r_con.x', 'theta_con.x', 'delta_theta_con.x'])
        model.connect('x', 'l_conx.x')
        model.connect('y', ['r_con.y', 'theta_con.y', 'delta_theta_con.y'])

        model.add_design_var('x', indices=[0, 3])
        model.add_design_var('y')
        model.add_design_var('r', lower=.5, upper=10)

        # nonlinear constraints
        model.add_constraint('r_con.g', equals=0)

        IND = np.arange(SIZE, dtype=int)
        EVEN_IND = IND[0::2]  # all even indices
        model.add_constraint('theta_con.g', lower=-1e-5, upper=1e-5, indices=EVEN_IND)
        model.add_constraint('delta_theta_con.g', lower=-1e-5, upper=1e-5)

        # this constrains x[0] to be 1 (see definition of l_conx)
        model.add_constraint('l_conx.g', equals=0, linear=False, indices=[0, ])

        # linear constraint
        model.add_constraint('y', equals=0, indices=[0], linear=True)

        model.add_objective('circle.area', ref=-1)

        prob.setup(mode='fwd')
        prob.run_driver()
        prob.cleanup()

        # get the case we recorded
        cr = CaseReader(self.filename)
        case = cr.get_case(0)

        # check 'use_indices' option, default is to use indices
        dvs = case.get_design_vars()
        assert_rel_error(self, dvs['x'], x_vals[[0, 3]], 1e-12)

        dvs = case.get_design_vars(use_indices=False)
        assert_rel_error(self, dvs['x'], x_vals, 1e-12)

        cons = case.get_constraints()
        self.assertEqual(len(cons['theta_con.g']), len(EVEN_IND))

        cons = case.get_constraints(use_indices=False)
        self.assertEqual(len(cons['theta_con.g']), SIZE)

        # add one to all the inputs just to change the model, so we
        # can see if loading the case values really changes the model
        for name in prob.model._inputs:
            model._inputs[name] += 1.0
        for name in prob.model._outputs:
            model._outputs[name] += 1.0

        # load in the case we recorded and check that the model then matches
        prob.load_case(case)
        _assert_model_matches_case(case, model)

    def test_multidimensional_arrays(self):
        prob = Problem()
        model = prob.model

        comp = TestExplCompArray(thickness=1.)  # has 2D arrays as inputs and outputs
        model.add_subsystem('comp', comp, promotes=['*'])
        # just to add a connection, otherwise an exception is thrown in recording viewer data.
        # must be a bug
        model.add_subsystem('double_area',
                            ExecComp('double_area = 2 * areas',
                                     areas=np.zeros((2, 2)),
                                     double_area=np.zeros((2, 2))),
                            promotes=['*'])

        prob.driver.add_recorder(self.recorder)
        prob.driver.recording_options['includes'] = ['*']

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            model._inputs[name] += 1.0
        for name in prob.model._outputs:
            model._outputs[name] += 1.0

        # Now load in the case we recorded
        cr = CaseReader(self.filename)

        driver_cases = cr.list_cases('driver')
        case = cr.get_case(driver_cases[0])

        prob.load_case(case)

        _assert_model_matches_case(case, model)

    def test_simple_paraboloid_scaled_desvars(self):

        prob = Problem()
        model = prob.model = Group()

        model.add_subsystem('p1', IndepVarComp('x', 50.0), promotes=['*'])
        model.add_subsystem('p2', IndepVarComp('y', 50.0), promotes=['*'])
        model.add_subsystem('comp', Paraboloid(), promotes=['*'])
        model.add_subsystem('con', ExecComp('c = x - y'), promotes=['*'])

        prob.set_solver_print(level=0)

        prob.driver = ScipyOptimizeDriver()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['tol'] = 1e-9
        prob.driver.options['disp'] = False

        prob.driver.recording_options['record_desvars'] = True
        prob.driver.recording_options['record_responses'] = True
        prob.driver.recording_options['record_objectives'] = True
        prob.driver.recording_options['record_constraints'] = True
        recorder = SqliteRecorder("cases.sql")
        prob.driver.add_recorder(recorder)

        ref = 5.0
        ref0 = -5.0
        model.add_design_var('x', lower=-50.0, upper=50.0, ref=ref, ref0=ref0)
        model.add_design_var('y', lower=-50.0, upper=50.0, ref=ref, ref0=ref0)
        model.add_objective('f_xy')
        model.add_constraint('c', lower=10.0, upper=11.0)

        prob.setup(check=False, mode='fwd')

        prob.run_driver()
        prob.cleanup()

        cr = CaseReader("cases.sql")

        # Test values from the last case
        driver_cases = cr.list_cases('driver')
        last_case = cr.get_case(driver_cases[-1])

        dvs = last_case.get_design_vars(scaled=False)
        unscaled_x = dvs['x'][0]
        unscaled_y = dvs['y'][0]

        dvs = last_case.get_design_vars(scaled=True)
        scaled_x = dvs['x'][0]
        scaled_y = dvs['y'][0]

        adder, scaler = determine_adder_scaler(ref0, ref, None, None)
        self.assertAlmostEqual((unscaled_x + adder) * scaler, scaled_x, places=12)
        self.assertAlmostEqual((unscaled_y + adder) * scaler, scaled_y, places=12)

    def test_reading_all_case_types(self):
        prob = SellarProblem(SellarDerivativesGrouped, nonlinear_solver=NonlinearRunOnce)
        prob.setup(mode='rev')

        driver = prob.driver = ScipyOptimizeDriver(disp=False, tol=1e-9)

        #
        # Add recorders
        #

        # driver
        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_responses'] = True
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True
        driver.add_recorder(self.recorder)

        # root solver
        nl = prob.model.nonlinear_solver
        nl.recording_options['record_metadata'] = True
        nl.recording_options['record_abs_error'] = True
        nl.recording_options['record_rel_error'] = True
        nl.recording_options['record_solver_residuals'] = True
        nl.add_recorder(self.recorder)

        # system
        pz = prob.model.pz  # IndepVarComp which is an ExplicitComponent
        pz.recording_options['record_metadata'] = True
        pz.recording_options['record_inputs'] = True
        pz.recording_options['record_outputs'] = True
        pz.recording_options['record_residuals'] = True
        pz.add_recorder(self.recorder)

        # mda solver
        nl = prob.model.mda.nonlinear_solver = NonlinearBlockGS()
        nl.recording_options['record_metadata'] = True
        nl.recording_options['record_abs_error'] = True
        nl.recording_options['record_rel_error'] = True
        nl.recording_options['record_solver_residuals'] = True
        nl.add_recorder(self.recorder)

        # problem
        prob.recording_options['includes'] = []
        prob.recording_options['record_objectives'] = True
        prob.recording_options['record_constraints'] = True
        prob.recording_options['record_desvars'] = True
        prob.add_recorder(self.recorder)

        fail = prob.run_driver()

        prob.record_iteration('final')
        prob.cleanup()

        self.assertFalse(fail, 'Problem optimization failed.')

        cr = CaseReader(self.filename)

        #
        # check sources
        #

        self.assertEqual(sorted(cr.list_sources()), [
            'driver', 'problem', 'root.mda.nonlinear_solver', 'root.nonlinear_solver', 'root.pz'
        ])

        #
        # check system cases
        #

        system_cases = cr.list_cases('root.pz', recurse=False)
        expected_cases = [
            'rank0:SLSQP|0|root._solve_nonlinear|0|NLRunOnce|0|pz._solve_nonlinear|0',
            'rank0:SLSQP|1|root._solve_nonlinear|1|NLRunOnce|0|pz._solve_nonlinear|1',
            'rank0:SLSQP|2|root._solve_nonlinear|2|NLRunOnce|0|pz._solve_nonlinear|2',
            'rank0:SLSQP|3|root._solve_nonlinear|3|NLRunOnce|0|pz._solve_nonlinear|3',
            'rank0:SLSQP|4|root._solve_nonlinear|4|NLRunOnce|0|pz._solve_nonlinear|4',
            'rank0:SLSQP|5|root._solve_nonlinear|5|NLRunOnce|0|pz._solve_nonlinear|5',
            'rank0:SLSQP|6|root._solve_nonlinear|6|NLRunOnce|0|pz._solve_nonlinear|6'
        ]
        self.assertEqual(len(system_cases), len(expected_cases))
        for i, coord in enumerate(system_cases):
            self.assertEqual(coord, expected_cases[i])

        # check inputs, outputs and residuals for last case
        case = cr.get_case(system_cases[-1])

        self.assertEqual(case.inputs, None)

        self.assertEqual(list(case.outputs.keys()), ['z'])
        self.assertEqual(case.outputs['z'][0], prob['z'][0])
        self.assertEqual(case.outputs['z'][1], prob['z'][1])

        self.assertEqual(list(case.residuals.keys()), ['z'])
        self.assertEqual(case.residuals['z'][0], 0.)
        self.assertEqual(case.residuals['z'][1], 0.)

        #
        # check solver cases
        #

        root_solver_cases = cr.list_cases('root.nonlinear_solver', recurse=False)
        expected_cases = [
            'rank0:SLSQP|0|root._solve_nonlinear|0|NLRunOnce|0',
            'rank0:SLSQP|1|root._solve_nonlinear|1|NLRunOnce|0',
            'rank0:SLSQP|2|root._solve_nonlinear|2|NLRunOnce|0',
            'rank0:SLSQP|3|root._solve_nonlinear|3|NLRunOnce|0',
            'rank0:SLSQP|4|root._solve_nonlinear|4|NLRunOnce|0',
            'rank0:SLSQP|5|root._solve_nonlinear|5|NLRunOnce|0',
            'rank0:SLSQP|6|root._solve_nonlinear|6|NLRunOnce|0'
        ]
        self.assertEqual(len(root_solver_cases), len(expected_cases))
        for i, coord in enumerate(root_solver_cases):
            self.assertEqual(coord, expected_cases[i])

        case = cr.get_case(root_solver_cases[-1])

        expected_inputs = ['x', 'y1', 'y2', 'z']
        expected_outputs = ['con1', 'con2', 'obj', 'x', 'y1', 'y2', 'z']

        self.assertEqual(sorted(case.inputs.keys()), expected_inputs)
        self.assertEqual(sorted(case.outputs.keys()), expected_outputs)
        self.assertEqual(sorted(case.residuals.keys()), expected_outputs)

        for key in expected_inputs:
            np.testing.assert_almost_equal(case.inputs[key], prob[key])

        for key in expected_outputs:
            np.testing.assert_almost_equal(case.outputs[key], prob[key])

        np.testing.assert_almost_equal(case.abs_err, 0, decimal=6)
        np.testing.assert_almost_equal(case.rel_err, 0, decimal=6)

        #
        # check mda solver cases
        #

        # check that there are multiple iterations and mda solver is part of the coordinate
        mda_solver_cases = cr.list_cases('root.mda.nonlinear_solver', recurse=False)
        self.assertTrue(len(mda_solver_cases) > 1)
        for coord in mda_solver_cases:
            self.assertTrue('mda._solve_nonlinear' in coord)

        case = cr.get_case(mda_solver_cases[-1])

        expected_inputs = ['x', 'y1', 'y2', 'z']
        expected_outputs = ['y1', 'y2']

        self.assertEqual(sorted(case.inputs.keys()), expected_inputs)
        self.assertEqual(sorted(case.outputs.keys()), expected_outputs)
        self.assertEqual(sorted(case.residuals.keys()), expected_outputs)

        for key in expected_inputs:
            np.testing.assert_almost_equal(case.inputs[key], prob[key])

        for key in expected_outputs:
            np.testing.assert_almost_equal(case.outputs[key], prob[key])

        np.testing.assert_almost_equal(case.abs_err, 0, decimal=6)
        np.testing.assert_almost_equal(case.rel_err, 0, decimal=6)

        # check that the recurse option returns root and mda solver cases plus child system cases
        all_solver_cases = cr.list_cases('root.nonlinear_solver', recurse=True, flat=True)
        self.assertEqual(len(all_solver_cases),
                         len(root_solver_cases) + len(mda_solver_cases) + len(system_cases))

        #
        # check driver cases
        #

        driver_cases = cr.list_cases('driver', recurse=False)
        expected_cases = [
            'rank0:SLSQP|0',
            'rank0:SLSQP|1',
            'rank0:SLSQP|2',
            'rank0:SLSQP|3',
            'rank0:SLSQP|4',
            'rank0:SLSQP|5',
            'rank0:SLSQP|6'
        ]
        # check that there are multiple iterations and they have the expected coordinates
        self.assertTrue(len(driver_cases), len(expected_cases))
        for i, coord in enumerate(driver_cases):
            self.assertEqual(coord, expected_cases[i])

        # check VOI values from last driver iteration
        case = cr.get_case(driver_cases[-1])

        expected_dvs = {
            "z": prob['pz.z'],
            "x": prob['px.x']
        }
        expected_obj = {
            "obj": prob['obj_cmp.obj']
        }
        expected_con = {
            "con1": prob['con_cmp1.con1'],
            "con2": prob['con_cmp2.con2']
        }

        dvs = case.get_design_vars()
        obj = case.get_objectives()
        con = case.get_constraints()

        self.assertEqual(dvs.keys(), expected_dvs.keys())
        for key in expected_dvs:
            np.testing.assert_almost_equal(dvs[key], expected_dvs[key])

        self.assertEqual(obj.keys(), expected_obj.keys())
        for key in expected_obj:
            np.testing.assert_almost_equal(obj[key], expected_obj[key])

        self.assertEqual(con.keys(), expected_con.keys())
        for key in expected_con:
            np.testing.assert_almost_equal(con[key], expected_con[key])

        # check accessing values via outputs attribute
        expected_outputs = expected_dvs
        expected_outputs.update(expected_obj)
        expected_outputs.update(expected_con)

        self.assertEqual(set(case.outputs.keys()), set(expected_outputs.keys()))
        for key in expected_outputs:
            np.testing.assert_almost_equal(case.outputs[key], expected_outputs[key])

        # check that the recurse option also returns system and solver cases (all_solver_cases)
        all_driver_cases = cr.list_cases('driver', recurse=True, flat=True)

        expected_cases = driver_cases + \
            [c for c in all_solver_cases if c.startswith('rank0:SLSQP')]

        self.assertEqual(len(all_driver_cases), len(expected_cases))
        for case in expected_cases:
            self.assertTrue(case in all_driver_cases)

    def test_linesearch(self):
        prob = Problem()

        model = prob.model

        model.add_subsystem('px', IndepVarComp('x', 1.0))
        model.add_subsystem('comp', ImplCompTwoStates())
        model.connect('px.x', 'comp.x')

        model.nonlinear_solver = NewtonSolver()
        model.nonlinear_solver.options['maxiter'] = 3
        # model.nonlinear_solver.options['solve_subsystems'] = True
        model.nonlinear_solver.options['iprint'] = 2
        model.linear_solver = ScipyKrylov()

        ls = model.nonlinear_solver.linesearch = ArmijoGoldsteinLS(bound_enforcement='vector')
        ls.options['maxiter'] = 3
        ls.options['alpha'] = 1.0

        # add recorder to nonlinear solver, linesearch solver and model
        model.nonlinear_solver.add_recorder(self.recorder)
        model.nonlinear_solver.linesearch.add_recorder(self.recorder)
        model.comp.add_recorder(self.recorder)
        model.add_recorder(self.recorder)

        prob.setup(check=False)

        prob['px.x'] = 2.0
        prob['comp.y'] = 0.0
        prob['comp.z'] = 1.6
        prob.run_model()
        prob.cleanup()

        expected = [
            'rank0:root._solve_nonlinear|0|Newton_subsolve|0',
            'rank0:root._solve_nonlinear|0|NewtonSolver|0',
            'rank0:root._solve_nonlinear|0|NewtonSolver|1|ArmijoGoldsteinLS|0',
            'rank0:root._solve_nonlinear|0|NewtonSolver|1|ArmijoGoldsteinLS|1',
            'rank0:root._solve_nonlinear|0|NewtonSolver|1|ArmijoGoldsteinLS|2',
            'rank0:root._solve_nonlinear|0|NewtonSolver|1',
            'rank0:root._solve_nonlinear|0|NewtonSolver|2|ArmijoGoldsteinLS|0',
            'rank0:root._solve_nonlinear|0|NewtonSolver|2|ArmijoGoldsteinLS|1',
            'rank0:root._solve_nonlinear|0|NewtonSolver|2|ArmijoGoldsteinLS|2',
            'rank0:root._solve_nonlinear|0|NewtonSolver|2',
            'rank0:root._solve_nonlinear|0'
        ]

        cr = CaseReader(self.filename)

        for i, c in enumerate(cr.list_cases()):
            case = cr.get_case(c)


            coord = case.iteration_coordinate
            self.assertEqual(coord, expected[i])

            # check the source
            if 'ArmijoGoldsteinLS' in coord:
                self.assertEqual(case.source, 'root.nonlinear_solver.linesearch')
            elif 'Newton' in coord:
                self.assertEqual(case.source, 'root.nonlinear_solver')
            else:
                self.assertEqual(case.source, 'root')


class TestFeatureSqliteReader(unittest.TestCase):

    def setUp(self):
        self.orig_dir = os.getcwd()
        self.temp_dir = mkdtemp()
        os.chdir(self.temp_dir)

    def tearDown(self):
        os.chdir(self.orig_dir)
        try:
            rmtree(self.temp_dir)
        except OSError as e:
            # If directory already deleted, keep going
            if e.errno not in (errno.ENOENT, errno.EACCES, errno.EPERM):
                raise e

    def test_feature_list_cases(self):
        from openmdao.api import Problem, ScipyOptimizeDriver, SqliteRecorder
        from openmdao.test_suite.components.sellar_feature import SellarMDA

        import numpy as np

        prob = Problem(model=SellarMDA())

        model = prob.model
        model.add_design_var('z', lower=np.array([-10.0, 0.0]),
                                  upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        driver = prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9)

        driver.add_recorder(SqliteRecorder('cases.sql'))

        prob.setup()
        prob.set_solver_print(0)
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader('cases.sql')

        case_ids = cr.list_cases()

        self.assertEqual(len(case_ids), driver.iter_count)
        self.assertEqual(case_ids, ['rank0:SLSQP|%d' % i for i in range(driver.iter_count)])
        self.assertEqual('', '')

        for case_id in case_ids:
            case = cr.get_case(case_id)
            self.assertEqual(case, case)

    def test_feature_get_cases(self):
        from openmdao.api import Problem, ScipyOptimizeDriver, SqliteRecorder
        from openmdao.test_suite.components.sellar_feature import SellarMDA

        import numpy as np

        prob = Problem(model=SellarMDA())

        model = prob.model
        model.add_design_var('z', lower=np.array([-10.0, 0.0]),
                                  upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        driver = prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9)
        driver.add_recorder(SqliteRecorder('cases.sql'))

        prob.setup()
        prob.set_solver_print(0)
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader('cases.sql')

        cases = cr.get_cases()

        self.assertEqual(len(cases), driver.iter_count)

        for case in cases:
            self.assertEqual(case, case)

    def test_feature_get_cases_nested(self):
        from openmdao.api import Problem, ScipyOptimizeDriver, SqliteRecorder
        from openmdao.test_suite.components.sellar_feature import SellarMDA

        import numpy as np

        # define Sellar MDA problem
        prob = Problem(model=SellarMDA())

        model = prob.model
        model.add_design_var('z', lower=np.array([-10.0, 0.0]),
                                  upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=False)

        # add recorder to the driver, model and solver
        recorder = SqliteRecorder('cases.sql')

        prob.driver.add_recorder(recorder)
        model.add_recorder(recorder)
        model.nonlinear_solver.add_recorder(recorder)

        # run the problem
        prob.setup()
        prob.set_solver_print(0)
        prob.run_driver()
        prob.cleanup()

        # get the last driver case
        cr = CaseReader('cases.sql')

        driver_cases = cr.list_cases('driver')
        last_driver_case = driver_cases[-1]

        # get a recursive dict of all child cases of the last driver case
        cases = cr.get_cases(last_driver_case, recurse=True, flat=False)

        # access the last driver case and it's children
        for case in cases:
            self.assertEqual(case, case)
            for child_case in cases[case]:
                self.assertEqual(child_case, child_case)
                for grandchild in cases[case][child_case]:
                    self.assertEqual(grandchild, grandchild)

    def test_feature_list_sources(self):
        from openmdao.api import Problem, ScipyOptimizeDriver, SqliteRecorder
        from openmdao.test_suite.components.sellar_feature import SellarMDA

        import numpy as np

        # define Sellar MDA problem
        prob = Problem(model=SellarMDA())

        model = prob.model
        model.add_design_var('z', lower=np.array([-10.0, 0.0]),
                                  upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=False)

        # add recorder to the driver, model and solver
        recorder = SqliteRecorder('cases.sql')

        prob.driver.add_recorder(recorder)
        model.add_recorder(recorder)
        model.nonlinear_solver.add_recorder(recorder)

        # run the problem
        prob.setup()
        prob.set_solver_print(0)
        prob.run_driver()
        prob.cleanup()

        # examine cases to see what was recorded
        cr = CaseReader('cases.sql')

        self.assertEqual(sorted(cr.list_sources()), ['driver', 'root', 'root.nonlinear_solver'])

        driver_vars = cr.list_source_vars('driver')
        self.assertEqual(('inputs:', sorted(driver_vars['inputs']), 'outputs:', sorted(driver_vars['outputs'])),
                         ('inputs:', [], 'outputs:', ['con1', 'con2', 'obj', 'x', 'z']))

        model_vars = cr.list_source_vars('root')
        self.assertEqual(('inputs:', sorted(model_vars['inputs']), 'outputs:', sorted(model_vars['outputs'])),
                         ('inputs:', ['x', 'y1', 'y2', 'z'], 'outputs:', ['con1', 'con2', 'obj', 'x', 'y1', 'y2', 'z']))

        solver_vars = cr.list_source_vars('root')
        self.assertEqual(('inputs:', sorted(solver_vars['inputs']), 'outputs:', sorted(solver_vars['outputs'])),
                         ('inputs:', ['x', 'y1', 'y2', 'z'], 'outputs:', ['con1', 'con2', 'obj', 'x', 'y1', 'y2', 'z']))

    def test_feature_reading_derivatives(self):
        from openmdao.api import Problem, ScipyOptimizeDriver, SqliteRecorder
        from openmdao.test_suite.components.sellar_feature import SellarMDA

        import numpy as np

        prob = Problem(model=SellarMDA())

        model = prob.model
        model.add_design_var('z', lower=np.array([-10.0, 0.0]),
                                  upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        driver = prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=False)
        driver.recording_options['record_derivatives'] = True

        driver.add_recorder(SqliteRecorder('cases.sql'))

        prob.setup()
        prob.set_solver_print(0)
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader('cases.sql')

        # Get derivatives associated with the last iteration.
        derivs = cr.get_case(-1).jacobian

        # check that derivatives have been recorded.
        self.assertEqual(set(derivs.keys()), set([
            ('obj', 'z'), ('con2', 'z'), ('con1', 'x'),
            ('obj', 'x'), ('con2', 'x'), ('con1', 'z')
        ]))

        # Get specific derivative.
        assert_rel_error(self, derivs['obj', 'z'], derivs['obj', 'z'])

    def test_feature_recording_option_precedence(self):
        from openmdao.api import Problem, IndepVarComp, ExecComp, ScipyOptimizeDriver, \
            SqliteRecorder
        from openmdao.recorders.case_reader import CaseReader
        from openmdao.test_suite.components.paraboloid import Paraboloid

        prob = Problem()
        model = prob.model
        model.add_subsystem('p1', IndepVarComp('x', 50.0), promotes=['*'])
        model.add_subsystem('p2', IndepVarComp('y', 50.0), promotes=['*'])
        model.add_subsystem('comp', Paraboloid(), promotes=['*'])
        model.add_subsystem('con', ExecComp('c = x - y'), promotes=['*'])

        prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=False)

        model.add_design_var('x', lower=-50.0, upper=50.0)
        model.add_design_var('y', lower=-50.0, upper=50.0)
        model.add_objective('f_xy')
        model.add_constraint('c', lower=15.0)

        filename = "cases.sql"
        recorder = SqliteRecorder(filename)

        prob.driver.add_recorder(recorder)
        prob.driver.recording_options['record_desvars'] = True
        prob.driver.recording_options['includes'] = []
        prob.driver.recording_options['excludes'] = ['p2.y']

        prob.set_solver_print(0)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        # First case with record_desvars = True and includes = []
        cr = CaseReader(filename)
        case = cr.get_case(-1)

        self.assertEqual(sorted(case.outputs.keys()), ['c', 'f_xy', 'x'])

        # Second case with record_desvars = False and includes = []
        recorder = SqliteRecorder(filename)
        prob.driver.add_recorder(recorder)
        prob.driver.recording_options['record_desvars'] = False
        prob.driver.recording_options['includes'] = []

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(filename)
        case = cr.get_case(0)

        self.assertEqual(sorted(case.outputs.keys()), ['c', 'f_xy'])

        # Third case with record_desvars = True and includes = ['*']
        recorder = SqliteRecorder(filename)
        prob.driver.add_recorder(recorder)
        prob.driver.recording_options['record_desvars'] = True
        prob.driver.recording_options['includes'] = ['*']

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(filename)
        case = cr.get_case(0)

        self.assertEqual(sorted(case.outputs.keys()), ['c', 'f_xy', 'x'])

        # Fourth case with record_desvars = False and includes = ['*']
        recorder = SqliteRecorder(filename)
        prob.driver.add_recorder(recorder)
        prob.driver.recording_options['record_desvars'] = False
        prob.driver.recording_options['includes'] = ['*']

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader(filename)
        case = cr.get_case(0)

        self.assertEqual(sorted(case.outputs.keys()), ['c', 'f_xy'])

    def test_feature_driver_options_with_values(self):
        from openmdao.api import Problem, ScipyOptimizeDriver, SqliteRecorder, CaseReader
        from openmdao.test_suite.components.sellar import SellarDerivatives

        import numpy as np

        prob = Problem(model=SellarDerivatives())

        model = prob.model
        model.add_design_var('z', lower=np.array([-10.0, 0.0]),
                                  upper=np.array([10.0, 10.0]))
        model.add_design_var('x', lower=0.0, upper=10.0)
        model.add_objective('obj')
        model.add_constraint('con1', upper=0.0)
        model.add_constraint('con2', upper=0.0)

        driver = prob.driver = ScipyOptimizeDriver(optimizer='SLSQP', tol=1e-9, disp=False)

        driver.add_recorder(SqliteRecorder("cases.sql"))

        driver.recording_options['includes'] = []
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True
        driver.recording_options['record_desvars'] = True

        prob.setup()
        prob.set_solver_print(0)
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader("cases.sql")

        driver_cases = cr.list_cases('driver')
        case = cr.get_case(driver_cases[0])

        self.assertEqual(sorted(case.outputs.keys()), ['con1', 'con2', 'obj', 'x', 'z'])

        objs = case.get_objectives()
        cons = case.get_constraints()
        dvs = case.get_design_vars()

        # keys() will give you the promoted variable names
        self.assertEqual((sorted(objs.keys()), sorted(cons.keys()), sorted(dvs.keys())),
                         (['obj'], ['con1', 'con2'], ['x', 'z']))

        # alternatively, you can get the absolute names
        self.assertEqual((sorted(objs.absolute_names()), sorted(cons.absolute_names()), sorted(dvs.absolute_names())),
                         (['obj_cmp.obj'], ['con_cmp1.con1', 'con_cmp2.con2'], ['px.x', 'pz.z']))

        # you can access variable values using either the promoted or the absolute name
        self.assertEqual((objs['obj'], objs['obj_cmp.obj']), (objs['obj_cmp.obj'], objs['obj']))
        self.assertEqual((dvs['x'], dvs['px.x']), (dvs['px.x'], dvs['x']))


class TestPromotedToAbsoluteMap(unittest.TestCase):
    def setUp(self):
        self.dir = mkdtemp()
        self.original_path = os.getcwd()
        os.chdir(self.dir)

    def tearDown(self):
        os.chdir(self.original_path)
        try:
            rmtree(self.dir)
        except OSError as e:
            # If directory already deleted, keep going
            if e.errno not in (errno.ENOENT, errno.EACCES, errno.EPERM):
                raise e

    def test_dict_functionality(self):
        prob = SellarProblem(SellarDerivativesGrouped)
        driver = prob.driver = ScipyOptimizeDriver()

        recorder = SqliteRecorder("cases.sql")

        driver.add_recorder(recorder)
        driver.recording_options['includes'] = []
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_constraints'] = True
        driver.recording_options['record_desvars'] = True
        driver.recording_options['record_derivatives'] = True

        prob.setup()
        prob.run_driver()
        prob.cleanup()

        cr = CaseReader("cases.sql")

        driver_cases = cr.list_cases('driver')
        driver_case = cr.get_case(driver_cases[-1])

        dvs = driver_case.get_design_vars()
        derivs = driver_case.jacobian

        # verify that map looks and acts like a regular dict
        self.assertTrue(isinstance(dvs, dict))
        self.assertEqual(sorted(dvs.keys()), ['x', 'z'])
        self.assertEqual(sorted(dvs.items()), [('x', dvs['x']), ('z', dvs['z'])])

        # verify that using absolute names works the same as using promoted names
        self.assertEqual(sorted(dvs.absolute_names()), ['px.x', 'pz.z'])
        self.assertEqual(dvs['px.x'], dvs['x'])
        self.assertEqual(dvs['pz.z'][0], dvs['z'][0])
        self.assertEqual(dvs['pz.z'][1], dvs['z'][1])

        # verify we can set the value using either promoted or absolute name as key
        # (although users wouldn't normally do this, it's used when copying or scaling)
        dvs['x'] = 111.
        self.assertEqual(dvs['x'], 111.)
        self.assertEqual(dvs['px.x'], 111.)

        dvs['px.x'] = 222.
        self.assertEqual(dvs['x'], 222.)
        self.assertEqual(dvs['px.x'], 222.)

        # verify deriv keys are tuples as expected, both promoted and absolute
        self.assertEqual(set(derivs.keys()), set([
            ('obj', 'z'), ('con2', 'z'), ('con1', 'x'),
            ('obj', 'x'), ('con2', 'x'), ('con1', 'z')
        ]))
        self.assertEqual(set(derivs.absolute_names()), set([
            ('obj_cmp.obj', 'pz.z'), ('con_cmp2.con2', 'pz.z'), ('con_cmp1.con1', 'px.x'),
            ('obj_cmp.obj', 'px.x'), ('con_cmp2.con2', 'px.x'), ('con_cmp1.con1', 'pz.z')
        ]))

        # verify we can access derivs via tuple or string, with promoted or absolute names
        J = prob.compute_totals(of=['obj'], wrt=['x'])
        expected = J[('obj', 'x')]
        np.testing.assert_almost_equal(derivs[('obj', 'x')], expected, decimal=6)
        np.testing.assert_almost_equal(derivs[('obj', 'px.x')], expected, decimal=6)
        np.testing.assert_almost_equal(derivs[('obj_cmp.obj', 'px.x')], expected, decimal=6)
        np.testing.assert_almost_equal(derivs['obj,x'], expected, decimal=6)
        np.testing.assert_almost_equal(derivs['obj,px.x'], expected, decimal=6)
        np.testing.assert_almost_equal(derivs['obj_cmp.obj,x'], expected, decimal=6)

        # verify we can set derivs via tuple or string, with promoted or absolute names
        # (although users wouldn't normally do this, it's used when copying)
        for key, value in [(('obj', 'x'), 111.), (('obj', 'px.x'), 222.),
                           ('obj_cmp.obj,x', 333.), ('obj_cmp.obj,px.x', 444.)]:
            derivs[key] = value
            self.assertEqual(derivs[('obj', 'x')], value)
            self.assertEqual(derivs[('obj', 'px.x')], value)
            self.assertEqual(derivs[('obj_cmp.obj', 'px.x')], value)
            self.assertEqual(derivs['obj,x'], value)
            self.assertEqual(derivs['obj,px.x'], value)
            self.assertEqual(derivs['obj_cmp.obj,x'], value)

        # verify that we didn't mess up deriv keys by setting values
        self.assertEqual(set(derivs.keys()), set([
            ('obj', 'z'), ('con2', 'z'), ('con1', 'x'),
            ('obj', 'x'), ('con2', 'x'), ('con1', 'z')
        ]))
        self.assertEqual(set(derivs.absolute_names()), set([
            ('obj_cmp.obj', 'pz.z'), ('con_cmp2.con2', 'pz.z'), ('con_cmp1.con1', 'px.x'),
            ('obj_cmp.obj', 'px.x'), ('con_cmp2.con2', 'px.x'), ('con_cmp1.con1', 'pz.z')
        ]))


def _assert_model_matches_case(case, system):
    '''
    Check to see if the values in the case match those in the model.

    Parameters
    ----------
    case : Case object
        Case to be used for the comparison.
    system : System object
        System to be used for the comparison.
    '''
    case_inputs = case.inputs
    model_inputs = system._inputs
    for name, model_input in iteritems(model_inputs._views):
        np.testing.assert_almost_equal(case_inputs[name], model_input)

    case_outputs = case.outputs
    model_outputs = system._outputs
    for name, model_output in iteritems(model_outputs._views):
        np.testing.assert_almost_equal(case_outputs[name], model_output)


class TestSqliteCaseReaderLegacy(unittest.TestCase):

    legacy_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'legacy_sql')

    def setUp(self):
        self.orig_dir = os.getcwd()
        self.temp_dir = mkdtemp()
        os.chdir(self.temp_dir)

    def tearDown(self):
        os.chdir(self.orig_dir)
        try:
            rmtree(self.temp_dir)
        except OSError as e:
            # If directory already deleted, keep going
            if e.errno not in (errno.ENOENT, errno.EACCES, errno.EPERM):
                raise e

    def test_database_v4(self):
        # the change between v4 and v5 was the addition of the 'source' information
        # this tests the proper determination of the case source without that data
        #
        # the legacy database was created with the same setup as the above test named
        # "test_reading_all_case_types" so this is a slimmed down version of that test
        #
        # NOTE: ScipyOptimizeDriver did not record its initial run under its own
        #       recording context prior to V5, so the initial case does not reflect
        #       the driver as the source

        filename = os.path.join(self.legacy_dir, 'case_database_v4.sql')

        cr = CaseReader(filename)

        #
        # check sources
        #

        self.assertEqual(sorted(cr.list_sources()), [
            'driver', 'problem', 'root.mda.nonlinear_solver', 'root.nonlinear_solver', 'root.pz'
        ])

        driver_vars = cr.list_source_vars('driver')
        self.assertEqual(('inputs:', sorted(driver_vars['inputs']), 'outputs:', sorted(driver_vars['outputs'])),
                         ('inputs:', [], 'outputs:', ['con1', 'con2', 'obj', 'x', 'z']))

        model_vars = cr.list_source_vars('root.pz')
        self.assertEqual(('inputs:', sorted(model_vars['inputs']), 'outputs:', sorted(model_vars['outputs'])),
                         ('inputs:', [], 'outputs:', ['z']))

        solver_vars = cr.list_source_vars('root.mda.nonlinear_solver')
        self.assertEqual(('inputs:', sorted(solver_vars['inputs']), 'outputs:', sorted(solver_vars['outputs'])),
                         ('inputs:', ['x', 'y1', 'y2', 'z'], 'outputs:', ['y1', 'y2']))

        #
        # check system cases
        #

        system_cases = cr.list_cases('root.pz', recurse=False)
        expected_cases = [
            'rank0:root._solve_nonlinear|0|NLRunOnce|0|pz._solve_nonlinear|0',
            'rank0:SLSQP|0|root._solve_nonlinear|1|NLRunOnce|0|pz._solve_nonlinear|1',
            'rank0:SLSQP|1|root._solve_nonlinear|2|NLRunOnce|0|pz._solve_nonlinear|2',
            'rank0:SLSQP|2|root._solve_nonlinear|3|NLRunOnce|0|pz._solve_nonlinear|3',
            'rank0:SLSQP|3|root._solve_nonlinear|4|NLRunOnce|0|pz._solve_nonlinear|4',
            'rank0:SLSQP|4|root._solve_nonlinear|5|NLRunOnce|0|pz._solve_nonlinear|5',
            'rank0:SLSQP|5|root._solve_nonlinear|6|NLRunOnce|0|pz._solve_nonlinear|6',
        ]
        self.assertEqual(len(system_cases), len(expected_cases))
        for i, coord in enumerate(system_cases):
            self.assertEqual(coord, expected_cases[i])

        #
        # check solver cases
        #

        root_solver_cases = cr.list_cases('root.nonlinear_solver', recurse=False)
        expected_cases = [
            'rank0:root._solve_nonlinear|0|NLRunOnce|0',
            'rank0:SLSQP|0|root._solve_nonlinear|1|NLRunOnce|0',
            'rank0:SLSQP|1|root._solve_nonlinear|2|NLRunOnce|0',
            'rank0:SLSQP|2|root._solve_nonlinear|3|NLRunOnce|0',
            'rank0:SLSQP|3|root._solve_nonlinear|4|NLRunOnce|0',
            'rank0:SLSQP|4|root._solve_nonlinear|5|NLRunOnce|0',
            'rank0:SLSQP|5|root._solve_nonlinear|6|NLRunOnce|0'
        ]
        self.assertEqual(len(root_solver_cases), len(expected_cases))
        for i, coord in enumerate(root_solver_cases):
            self.assertEqual(coord, expected_cases[i])

        case = cr.get_case(root_solver_cases[-1])

        expected_inputs = ['x', 'y1', 'y2', 'z']
        expected_outputs = ['con1', 'con2', 'obj', 'x', 'y1', 'y2', 'z']

        self.assertEqual(sorted(case.inputs.keys()), expected_inputs)
        self.assertEqual(sorted(case.outputs.keys()), expected_outputs)
        self.assertEqual(sorted(case.residuals.keys()), expected_outputs)

        #
        # check mda solver cases
        #

        # check that there are multiple iterations and mda solver is part of the coordinate
        mda_solver_cases = cr.list_cases('root.mda.nonlinear_solver', recurse=False)
        self.assertTrue(len(mda_solver_cases) > 1)
        for coord in mda_solver_cases:
            self.assertTrue('mda._solve_nonlinear' in coord)

        case = cr.get_case(mda_solver_cases[-1])

        expected_inputs = ['x', 'y1', 'y2', 'z']
        expected_outputs = ['y1', 'y2']

        self.assertEqual(sorted(case.inputs.keys()), expected_inputs)
        self.assertEqual(sorted(case.outputs.keys()), expected_outputs)
        self.assertEqual(sorted(case.residuals.keys()), expected_outputs)

        np.testing.assert_almost_equal(case.abs_err, 0, decimal=6)
        np.testing.assert_almost_equal(case.rel_err, 0, decimal=6)

        # check that the recurse option returns root and mda solver cases plus child system cases
        all_solver_cases = cr.list_cases('root.nonlinear_solver', recurse=True, flat=True)
        self.assertEqual(len(all_solver_cases),
                         len(root_solver_cases) + len(mda_solver_cases) + len(system_cases))

        #
        # check driver cases
        #

        driver_cases = cr.list_cases('driver', recurse=False)
        expected_cases = [
            'rank0:SLSQP|0',
            'rank0:SLSQP|1',
            'rank0:SLSQP|2',
            'rank0:SLSQP|3',
            'rank0:SLSQP|4',
            'rank0:SLSQP|5',
        ]
        # check that there are multiple iterations and they have the expected coordinates
        self.assertTrue(len(driver_cases), len(expected_cases))
        for i, coord in enumerate(driver_cases):
            self.assertEqual(coord, expected_cases[i])

    def test_driver_v3(self):
        """
        Backwards compatibility version 3.
        Legacy case recording file generated using code from test_record_driver_system_solver
        test in test_sqlite_recorder.py
        """
        prob = SellarProblem(SellarDerivativesGrouped)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        filename = os.path.join(self.legacy_dir, 'case_driver_solver_system_03.sql')

        cr = CaseReader(filename)

        # list just the driver cases
        driver_cases = cr.list_cases('driver', recurse=False)

        # check that we got the correct number of cases
        self.assertEqual(len(driver_cases), 6)

        # check that the access by case keys works:
        seventh_slsqp_iteration_case = cr.get_case('rank0:SLSQP|5')
        np.testing.assert_almost_equal(seventh_slsqp_iteration_case.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        # Test values from the last case
        last_case = cr.get_case(driver_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['z'], prob['z'])
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # check that the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(driver_cases):
            self.assertEqual(iter_coord, 'rank0:SLSQP|{}'.format(i))

        # Test problem metadata
        self.assertIsNotNone(cr.problem_metadata)
        self.assertTrue('connections_list' in cr.problem_metadata)
        self.assertTrue('tree' in cr.problem_metadata)
        self.assertTrue('variables' in cr.problem_metadata)

        # While we are here, make sure we can load this case.

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            prob.model._inputs[name] += 1.0
        for name in prob.model._outputs:
            prob.model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(seventh_slsqp_iteration_case)

        _assert_model_matches_case(seventh_slsqp_iteration_case, prob.model)

    def test_driver_v2(self):
        """ Backwards compatibility version 2. """
        prob = SellarProblem(SellarDerivativesGrouped)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        filename = os.path.join(self.legacy_dir, 'case_driver_solver_system_02.sql')

        cr = CaseReader(filename)

        # list just the driver cases
        driver_cases = cr.list_cases('driver', recurse=False)

        # check that we got the correct number of cases
        self.assertEqual(len(driver_cases), 7)

        # check that the access by case keys works:
        seventh_slsqp_iteration_case = cr.get_case('rank0:SLSQP|5')
        np.testing.assert_almost_equal(seventh_slsqp_iteration_case.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        # Test values from the last case
        last_case = cr.get_case(driver_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['z'], prob['z'])
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # check that the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(driver_cases):
            self.assertEqual(iter_coord, 'rank0:SLSQP|{}'.format(i))

        # Test driver metadata
        self.assertIsNotNone(cr.problem_metadata)
        self.assertTrue('connections_list' in cr.problem_metadata)
        self.assertTrue('tree' in cr.problem_metadata)
        self.assertTrue('variables' in cr.problem_metadata)

        # While we are here, make sure we can load this case.

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            prob.model._inputs[name] += 1.0
        for name in prob.model._outputs:
            prob.model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(seventh_slsqp_iteration_case)

        _assert_model_matches_case(seventh_slsqp_iteration_case, prob.model)

    def test_solver_v2(self):
        """ Backwards compatibility version 2. """
        filename = os.path.join(self.legacy_dir, 'case_driver_solver_system_02.sql')

        cases = CaseReader(filename)

        # list just the solver cases
        solver_cases = cases.list_cases('root.nonlinear_solver', recurse=False)

        # check that we got the correct number of cases
        self.assertEqual(len(solver_cases), 7)

        # check that the access by case keys works:
        sixth_solver_case_id = solver_cases[5]
        self.assertEqual(sixth_solver_case_id, 'rank0:SLSQP|5|root._solve_nonlinear|5|NLRunOnce|0')

        sixth_solver_iteration = cases.get_case(sixth_solver_case_id)

        np.testing.assert_almost_equal(sixth_solver_iteration.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        # Test values from the last case
        last_case = cases.get_case(solver_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # check that the case keys (iteration coords) come back correctly
        coord = 'rank0:SLSQP|{}|root._solve_nonlinear|{}|NLRunOnce|0'
        for i, iter_coord in enumerate(solver_cases):
            self.assertEqual(iter_coord, coord.format(i, i))

    def test_system_v2(self):
        """ Backwards compatibility version 2. """
        filename = os.path.join(self.legacy_dir, 'case_driver_solver_system_02.sql')

        cr = CaseReader(filename)

        # list just the system cases
        system_cases = cr.list_cases('root', recurse=False)

        # check that we got the correct number of cases
        self.assertEqual(len(system_cases), 7)

        # check that the access by case keys works:
        sixth_system_case_id = system_cases[5]
        self.assertEqual(sixth_system_case_id, 'rank0:SLSQP|5|root._solve_nonlinear|5')

        sixth_system_case = cr.get_case(system_cases[5])

        np.testing.assert_almost_equal(sixth_system_case.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        last_case = cr.get_case(system_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # check that the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(system_cases):
            self.assertEqual(iter_coord, 'rank0:SLSQP|{}|root._solve_nonlinear|{}'.format(i, i))

        # Test metadata read correctly
        self.assertEqual(cr._output2meta['mda.d2.y2']['type'], {'output'})
        self.assertEqual(cr._output2meta['mda.d2.y2']['size'], 1)
        self.assertTrue(cr._output2meta['mda.d2.y2']['explicit'], {'output'})
        self.assertEqual(cr._input2meta['mda.d1.z']['type'], {'input'})
        self.assertEqual(cr._input2meta['mda.d1.z']['size'], 2)
        self.assertIsNone(cr._input2meta['mda.d1.z']['units'])
        self.assertTrue(cr._output2meta['mda.d2.y2']['explicit'], {'output'})

    def test_driver_v1(self):
        """ Backwards compatibility oldest version. """
        prob = SellarProblem(SellarDerivativesGrouped)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        filename = os.path.join(self.legacy_dir, 'case_driver_01.sql')

        cr = CaseReader(filename)

        # recorded data from driver only
        self.assertEqual(cr.list_sources(), ['driver'])

        # check that we got the correct number of cases
        driver_cases = cr.list_cases('driver')
        self.assertEqual(len(driver_cases), 7)

        # check that the access by case keys works:
        seventh_slsqp_iteration_case = cr.get_case('rank0:SLSQP|5')
        np.testing.assert_almost_equal(seventh_slsqp_iteration_case.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        # Test values from the last case
        last_case = cr.get_case(driver_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['z'], prob['z'],)
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # check that the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(driver_cases):
            self.assertEqual(iter_coord, 'rank0:SLSQP|{}'.format(i))

        # While we are here, make sure we can load this case.

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            prob.model._inputs[name] += 1.0
        for name in prob.model._outputs:
            prob.model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(seventh_slsqp_iteration_case)

        _assert_model_matches_case(seventh_slsqp_iteration_case, prob.model)

    def test_driver_v1_pre_problem(self):
        """ Backwards compatibility oldest version. """
        prob = SellarProblem(SellarDerivativesGrouped)
        prob.driver = ScipyOptimizeDriver(tol=1e-9, disp=False)
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        filename = os.path.join(self.legacy_dir, 'case_driver_pre01.sql')

        cr = CaseReader(filename)

        # recorded data from driver only
        self.assertEqual(cr.list_sources(), ['driver'])

        # check that we got the correct number of cases
        driver_cases = cr.list_cases('driver')
        self.assertEqual(len(driver_cases), 7)

        # check that the access by case keys works:
        seventh_slsqp_iteration_case = cr.get_case('rank0:SLSQP|5')
        np.testing.assert_almost_equal(seventh_slsqp_iteration_case.outputs['z'],
                                       [1.97846296, -2.21388305e-13], decimal=2)

        # Test values from the last case
        last_case = cr.get_case(driver_cases[-1])
        np.testing.assert_almost_equal(last_case.outputs['z'], prob['z'])
        np.testing.assert_almost_equal(last_case.outputs['x'], [-0.00309521], decimal=2)

        # check that the case keys (iteration coords) come back correctly
        for i, iter_coord in enumerate(driver_cases):
            self.assertEqual(iter_coord, 'rank0:SLSQP|{}'.format(i))

        # While we are here, make sure we can load this case.

        # Add one to all the inputs just to change the model
        #   so we can see if loading the case values really changes the model
        for name in prob.model._inputs:
            prob.model._inputs[name] += 1.0
        for name in prob.model._outputs:
            prob.model._outputs[name] += 1.0

        # Now load in the case we recorded
        prob.load_case(seventh_slsqp_iteration_case)

        _assert_model_matches_case(seventh_slsqp_iteration_case, prob.model)


if __name__ == "__main__":
    unittest.main()
