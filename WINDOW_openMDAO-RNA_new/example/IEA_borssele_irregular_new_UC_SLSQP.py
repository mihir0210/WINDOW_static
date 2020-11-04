# This file must be run from the 'example' folder that has the 'Input' folder.
import numpy as np
import pandas as pd

# Imports OpenMDAO API
from openmdao.api import Problem, ScipyOptimizer, view_model, SimpleGADriver
from openmdao.api import SqliteRecorder, CaseReader



# Imports WINDOW workflow
from WINDOW_openMDAO.multifidelity_fast_workflow_new import WorkingGroup

# Imports models included in WINDOW
# from WINDOW_openMDAO.Turbine.Curves import Curves # Not used in the AEP fast calculator.
from WINDOW_openMDAO.ElectricalCollection.topology_hybrid_optimiser import TopologyHybridHeuristic
from WINDOW_openMDAO.ElectricalCollection.constant_electrical import ConstantElectrical
from WINDOW_openMDAO.ElectricalCollection.POS_optimiser import POSHeuristic
from WINDOW_openMDAO.SupportStructure.teamplay import TeamPlay
from WINDOW_openMDAO.SupportStructure.constant_support import ConstantSupport
from WINDOW_openMDAO.OandM.OandM_models import OM_model1
from WINDOW_openMDAO.AEP.aep_fast_component import AEPFast
from WINDOW_openMDAO.Costs.teamplay_costmodel import TeamPlayCostModel
from WINDOW_openMDAO.AEP.FastAEP.farm_energy.wake_model_mean_new.wake_turbulence_models import frandsen2, \
    danish_recommendation, frandsen, larsen_turbulence, Quarton, constantturbulence
from WINDOW_openMDAO.AEP.FastAEP.farm_energy.wake_model_mean_new.downstream_effects import JensenEffects as Jensen, \
    LarsenEffects as Larsen, Ainslie1DEffects as Ainslie1D, Ainslie2DEffects as Ainslie2D, constantwake
from WINDOW_openMDAO.AEP.FastAEP.farm_energy.wake_model_mean_new.wake_overlap import root_sum_square, maximum, \
    multiplied, summed

# Imports the Options class to instantiate a workflow.
from WINDOW_openMDAO.src.api import WorkflowOptions
#from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC import WorkingGroup
#from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static import WorkingGroup
#from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static_opt import WorkingGroup
from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static_opt_single_turbine import WorkingGroup


import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()


def print_nice(string, value):
    header = '=' * 10 + " " + string + " " + '=' * 10 + '\n'
    header += str(value) + "\n"
    header += "=" * (22 + len(string))
    print header


options = WorkflowOptions()

# Define models to be implemented.
options.models.aep = AEPFast
options.models.wake = Jensen
options.models.merge = root_sum_square
options.models.turbine = None  # Unnecessary for now as long as the power and Ct curves are defined below.
options.models.turbulence = frandsen
options.models.electrical = TopologyHybridHeuristic
options.models.support = TeamPlay
options.models.opex = OM_model1
options.models.apex = TeamPlayCostModel

# Define number of windrose sampling points
options.samples.wind_speeds = 10  #1
options.samples.wind_sectors_angle = 10.0 #30.0

# Define paths to site and turbine defining input files.
options.input.site.windrose_file = "Input/weibull_windrose_12unique.dat"
options.input.site.bathymetry_file = "Input/bathymetry_table.dat"

options.input.turbine.power_file = "Input/power_rna.dat"
options.input.turbine.ct_file = "Input/ct_rna.dat"
options.input.turbine.num_pegged = 3
options.input.turbine.num_airfoils = 8
options.input.turbine.num_nodes = 49
options.input.turbine.num_bins = 31
options.input.turbine.safety_factor = 1.5
options.input.turbine.gearbox_stages = 3
options.input.turbine.gear_configuration = 'eep'
options.input.turbine.mb1_type = 'CARB'
options.input.turbine.mb2_type = 'SRB'
options.input.turbine.drivetrain_design = 'geared'
options.input.turbine.uptower_transformer = True
options.input.turbine.has_crane = True
options.input.turbine.reference_turbine = 'Input/reference_turbine.csv'
options.input.turbine.reference_turbine_cost = 'Input/reference_turbine_cost_mass.csv'

options.input.turbine.wind_speed_file = 'Input/North_sea_2018_100.csv'
options.input.turbine.spot_price_file = 'Input/NL_spot_2018.csv'

### FAST addition ###

options.input.turbine.num_tnodes = 11


# Instantiate OpenMDAO problem class
problem = Problem()
problem.model = WorkingGroup(options)

problem.setup()

problem.driver = ScipyOptimizer()



problem.driver.recording_options['includes'] =[]
problem.driver.recording_options['record_objectives'] = True
problem.driver.recording_options['record_constraints'] = True
problem.driver.recording_options['record_desvars'] = True
recorder = SqliteRecorder("static_SLSQP1redo_final.csv")
problem.driver.add_recorder(recorder)


problem.driver.options['optimizer'] = 'SLSQP'
problem.driver.options['maxiter'] = 50
problem.driver.options['tol'] = 1e-3



problem.driver.options['disp'] = True



'''
# Default input values of NREL5MW / DTU 10 MW Reference Turbine
problem['design_tsr'] = 1.0 #6.5
problem['indep2.blade_number'] = 3
problem['rna.chord_coefficients'] = np.array([1.0, 1.0, 1.0]) # np.array([3.542, 3.01, 2.313])  #* 190.8 / 126.0  #np.array([3.35, 3.5, 2.6])
problem['rna.twist_coefficients'] = np.array([1.0, 1.0, 1.0]) #np.array([13.308, 9.0, 3.125])  #np.array([9.1, 4.3, 1.8])
problem['indep2.span_airfoil_r'] = np.array([01.36, 06.83, 10.25, 14.35, 22.55, 26.65, 34.85, 43.05]) # * 190.8 / 126.0
problem['indep2.span_airfoil_id'] = [0, 1, 2, 3, 4, 5, 6, 7]
problem['pitch'] = 0.0
problem['indep2.thickness_factor'] = 1.0
problem['indep2.shaft_angle'] = -5.0
problem['indep2.cut_in_speed'] = 3.0
problem['indep2.cut_out_speed'] = 25.0
problem['indep2.machine_rating'] = 5000.0
problem['indep2.drive_train_efficiency'] = 0.95
problem['indep2.gear_ratio'] = 96.76
problem['indep2.Np'] = [3, 3, 1]

### Preprocessor ###

problem['rna.tau_root'] = 1
problem['rna.tau_75'] = 1


### FAST ###
problem['indep2.blade_cone'] = 2.5

#problem['indep2.tower_bthickness'] = 0.027
#problem['indep2.tower_tthickness'] = 0.019
#problem['indep2.tower_height'] = np.array([0, 8.76, 17.52, 26.28, 35, 43.8, 52.56, 61.32, 70.08, 78.84, 87.76])
problem['indep2.tower_extramass'] = np.array([329.0, 308.0, 287.0, 268.0, 249.0, 230.0, 213.0, 196.0, 179.0, 164.0, 149.0])
#problem['indep2.tower_diameter'] = np.array([6, 5.78, 5.57, 5.36, 5.15, 4.935, 4.722, 4.509, 4.296, 4.083, 3.87])

problem['indep2.nacelle_hub_length'] = 5.0
problem['indep2.nacelle_hub_mass'] = 56780.0
problem['indep2.nacelle_hub_overhang'] = 5.0
problem['indep2.nacelle_hub_type'] = 1.0
problem['indep2.nacelle_hub_shafttilt'] = 5.0
problem['indep2.nacelle_housing_type'] = 1.0
problem['indep2.nacelle_housing_diameter'] = 5.0
problem['indep2.nacelle_housing_length'] = 10.0
problem['indep2.nacelle_housing_mass'] = 240000.0

problem['indep2.drivetrain_gear_eff'] = 1.0'''


#problem.model.add_design_var('tau_root', lower=0.7, upper=1.3)
#problem.model.add_design_var('tau_75', lower=0.7, upper=1.3)
#problem.model.add_design_var('turbine_radius', lower=50, upper=100)
#problem.model.add_design_var('turbine_rad', lower=0.7, upper=1.3)
problem.model.add_design_var('turbine_rad', lower=0.7, upper=1.3)
problem.model.add_objective('obj.f')  # ref0=-1.5*f_scaler, ref=-0.5*f_scaler)
#problem.model.add_constraint('c2.ramp', upper = 1)  # , ref0=0.25, ref=2.0)



'''
problem.model.add_constraint('design_tsr', lower=0.9, upper=1.05)
problem.model.add_constraint('chord_coefficients', lower=[0.9, 0.9, 0.9], upper=[1.2, 1.2, 1.2])
problem.model.add_constraint('twist_coefficients', lower=0.8*np.ones(3), upper=1.2*np.ones(3))
problem.model.add_constraint('pitch', lower=-0.286, upper=1)
problem.model.add_constraint('tau_root',lower=0.8, upper=1.2)
problem.model.add_constraint('tau_75',lower=0.8, upper=1.2)'''



# prob.model.add_constraint('rna.blade.pc.rated_tip_speed', upper=80.0, scaler=80.0) #, ref0=0.25, ref=2.0)
#problem.model.add_constraint('rna.rna.span_stress_max', upper=1.0)  # , ref0=0.25, ref=2.0)

problem.setup()

### Uncomment below to plot N2 diagram in a browser.
#view_model(problem)
from time import time

start = time()

#problem.run_model()
problem.model.approx_totals('fd')
problem.run_driver()

#############################
######## PARAMS #############
#############################
'''
farm_params = ['lcoe.LCOE', 'AeroAEP.AEP', \
               'AeroAEP.efficiency', 'AEP.electrical_efficiency',
               'Costs.support_structure_investment']

# Save variables
result = {'tsr': problem['design_tsr'],
          'chord': problem['chord_coefficients'],
          'twist': problem['twist_coefficients'],
          'pitch': problem['pitch'],
          'tf_root': problem['tau_root'],
          'tf_75' : problem['tau_75']
          }

# Save Farm parameters
for p in farm_params:
    result[p] = problem[p][0]

    # Save in file
    result = pd.DataFrame(result)
    pd.DataFrame(result).to_csv('static_GA.csv')'''



lcoe = problem['lcoe.LCOE'][0]
aep = problem['AeroAEP.AEP'][0]
base_dia = problem['support.base_dia']
top_dia = problem['support.top_dia']
turbine_radius = problem['rad_scaling.turbine_radius']
rated_power = problem['power_scaling.machine_rating']



print_nice("LCOE", lcoe)
print_nice("AEP", aep)
print_nice("Turbine radius", turbine_radius)
print_nice("Rated power", rated_power)

'''
### Setup Optimization ####
problem.driver = ScipyOptimizer()
problem.driver.options['optimizer'] = 'SLSQP'
problem.driver.options['tol'] = 1.0e-3
problem.driver.options['disp'] = True
problem.driver.options['maxiter'] = 1

problem.model.add_design_var('indep2.tau_root', lower= 0.6, upper=1.1)
problem.model.add_design_var('indep2.tau_75', lower=0.6, upper=1.1)
problem.model.add_design_var('indep2.chord_coefficients', lower=[3, 2,1 ], upper=[5, 4, 3])
problem.model.add_design_var('indep2.twist_coefficients', lower=[9, 6, 1], upper=[16, 12, 6])




problem.model.add_constraint('Tip_Deflection', upper=7)
problem.model.add_constraint('Flapwise_Stress_Skin', upper=700)
problem.model.add_constraint('Flapwise_Stress_Spar', upper=1047)
problem.model.add_constraint('Stress_Root',  upper=700)


# Ask OpenMDAO to finite-difference across the model to compute the gradients for the optimizer
problem.model.approx_totals()

problem['indep2.chord_coefficients'] = np.array([3.542, 3.01, 2.313])  #* 190.8 / 126.0
problem['indep2.twist_coefficients'] = [13.308, 9.0, 3.125]

### Preprocessor ###
problem['indep2.tau_root'] = 1.0
problem['indep2.tau_75'] = 1.0

problem.model.add_objective('LCOE')


problem.run_driver()'''

print 'Executed in ' + str(round(time() - start, 2)) + ' seconds\n'

# print outputs
from WINDOW_openMDAO.src.api import beautify_dict

'''
var_list = ['rotor_mass', 'nacelle_mass', 'rna_mass','cost_rna', 'tip_deflection', 'Root_stress', \
            'Stress_flapwise_skin', 'Stress_flapwise_spar', 'Stress_edgewise_skin', 'Stress_edgewise_te_reinf',
            'rotor_cp', 'rotor_ct', 'rotor_torque', 'rotor_thrust', \
            'rated_wind_speed', 'wind_bin', 'elec_power_bin', 'ct_bin', \
            'scale.hub_height', 'scale.turbine_rated_current', 'scale.solidity_rotor']

saved_output = {}
for v in var_list:
    saved_output[v] = problem['rna.' + v]
beautify_dict(saved_output)'''

