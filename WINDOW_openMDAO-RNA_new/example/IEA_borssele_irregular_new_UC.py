
# def run_main_script(value_rad, value_power, N_t):
def run_main_script(value_rad, value_power):
    file = open("Input/power_value.txt", "w")
    file.write(str(value_power))
    file.close()
    print(value_power)

    # file = open("Input/N_t.txt", "w")
    # file.write(str(N_t))
    # file.close()
    # print(N_t)


    # This file must be run from the 'example' folder that has the 'Input' folder.
    import numpy as np
    import pandas as pd
    #from __main__ import value_rad, value_power
    # Imports OpenMDAO API
    from openmdao.api import Problem, ScipyOptimizeDriver     #ScipyOptimizer, view_model, SimpleGADriver
    from openmdao.api import SqliteRecorder, CaseReader
    import csv



    # Imports WINDOW workflow
    from WINDOW_openMDAO.multifidelity_fast_workflow_new import WorkingGroup

    # Imports models included in WINDOW
    # from WINDOW_openMDAO.Turbine.Curves import Curves # Not used in the AEP fast calculator.
    from WINDOW_openMDAO.ElectricalCollection.topology_hybrid_optimiser import TopologyHybridHeuristic
    from WINDOW_openMDAO.ElectricalCollection.constant_electrical import ConstantElectrical
    from WINDOW_openMDAO.ElectricalCollection.POS_optimiser import POSHeuristic
    from WINDOW_openMDAO.SupportStructure.teamplay import TeamPlay
    from WINDOW_openMDAO.SupportStructure.constant_support import ConstantSupport
    from WINDOW_openMDAO.OandM.OandM_models import OM_model1, OM_model2, OM_model3
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

    #from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static_opt_elec_H2 import WorkingGroup
    from WINDOW_openMDAO import multifidelity_fast_workflow_new_UC_static_opt_elec
    #from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static_opt_elec import WorkingGroup
    from WINDOW_openMDAO.multifidelity_fast_workflow_new_UC_static_opt_elec_H2 import WorkingGroup


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
        print(header)


    options = WorkflowOptions()

    # Define models to be implemented.
    options.models.aep = AEPFast
    options.models.wake = Jensen
    options.models.merge = root_sum_square
    options.models.turbine = None  # Unnecessary for now as long as the power and Ct curves are defined below.
    options.models.turbulence = frandsen
    options.models.electrical = TopologyHybridHeuristic
    options.models.support = TeamPlay
    options.models.opex = OM_model3
    options.models.apex = TeamPlayCostModel

    # Define number of windrose sampling points
    options.samples.wind_speeds = 22  # number of wind samples between cut-in and cut-out
    options.samples.wind_sectors_angle = 30.0 # range of one sector for a windrose

    # Define paths to site and turbine defining input files.
    options.input.site.windrose_file = "Input/weibull_windrose_12unique.dat"
    options.input.site.bathymetry_file = "Input/bathymetry_table.dat"


    options.input.turbine.power_file = "Input/power_rna.dat"
    options.input.turbine.ct_file = "Input/ct_rna.dat"
    options.input.turbine.num_pegged = 3
    options.input.turbine.num_airfoils = 50

    options.input.turbine.num_nodes = 50
    options.input.turbine.num_bins = 62 #31
    options.input.turbine.safety_factor = 1.5
    options.input.turbine.gearbox_stages = 3
    options.input.turbine.gear_configuration = 'eep'
    options.input.turbine.mb1_type = 'CARB'
    options.input.turbine.mb2_type = 'SRB'
    options.input.turbine.drivetrain_design = 'geared'
    options.input.turbine.uptower_transformer = True
    options.input.turbine.has_crane = True
    options.input.turbine.reference_turbine = 'Input/Reference_turbine_15MW.csv'
    options.input.turbine.reference_turbine_cost = 'Input/reference_turbine_15MW_cost_mass.csv'
    options.input.turbine.rated_power = value_power/15.0
    options.input.turbine.rotor_radius = value_rad/120.0

    options.input.site.time_resolution = 8760 #52560
    options.input.site.wind_file = 'Input/NorthSea_2019_100m_hourly_ERA5_withdir.csv'



    options.input.market.spot_price_file = 'Input/NL_2019_spot_price_hourly.csv'

    ### H2 addition ###
    options.input.hydrogen.electrolyser_ratio = 1

    ### FAST addition ###

    options.input.turbine.num_tnodes = 11

    field_names = ['p_rated', 'd_rotor']
    description = ['Rated power', 'Rotor diameter']
    data = {field_names[0]: [value_power, description[0]], field_names[1]: [value_rad*2, description[1]]}

    with open('parameters.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in list(data.items()):
            writer.writerow([key, value[0], value[1]])
    csvfile.close()

    import ast
    with open('Input/finance.txt', 'r') as file:
        data = file.read()
        d = ast.literal_eval(data)

    target_IRR = d['target_IRR']
    options.input.market.target_IRR = target_IRR


    # Instantiate OpenMDAO problem class
    problem = Problem()
    problem.model = WorkingGroup(options)
    problem.setup()

    ### Uncomment below to plot N2 diagram in a browser.
    #view_model(problem)
    from time import time

    start = time()

    problem.run_model()


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
    aep = problem['FarmAEP.farm_AEP'][0]
    #subsidy_required = problem['FarmIRR.subsidy_required'][0]

    # lcoh = problem['LCoH.LCoH'][0]

    print_nice("LCOE", lcoe)
    # print_nice("LCoH", lcoh)
    #print_nice("AEP", aep)
    #print_nice("Subsidy required", subsidy_required)

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

    print('Executed in ' + str(round(time() - start, 2)) + ' seconds\n')

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
    return lcoe
