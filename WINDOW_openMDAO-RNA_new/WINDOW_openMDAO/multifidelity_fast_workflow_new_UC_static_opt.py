# workflow_regular.py only defines the workflow to be built. Class WorkingGroup needs to be imported from another working directory. As an example we provide a working directory in the example folder. Run IEA_borssele_regular.py from the 'example' folder instead


import numpy as np
from openmdao.api import IndepVarComp, Group, ExecComp
from WINDOW_openMDAO.input_params import max_n_turbines, max_n_substations, interest_rate, central_platform, areas, \
    n_quadrilaterals, separation_equation_y, operational_lifetime, number_turbines_per_cable, wind_directions, \
    weibull_shapes, weibull_scales, direction_probabilities, layout, n_turbines, TI_ambient, coll_electrical_efficiency, \
    transm_electrical_efficiency, number_substations
from WINDOW_openMDAO.blade_parameters import blade_span, pegged_chord, pegged_twist
from WINDOW_openMDAO.src.api import AEP, NumberLayout, MinDistance, WithinBoundaries
from WINDOW_openMDAO.WaterDepth.water_depth_models import RoughClosestNode
from WINDOW_openMDAO.Finance.LCOE import LCOE
# from WINDOW_openMDAO.RNA.rna import RNA
from WINDOW_openMDAO.RNA_modified.rna import RNA
from WINDOW_openMDAO.Turbine.single_turbine import single_turbine

from WINDOW_openMDAO.layout_scaling import LayoutScaling
from WINDOW_openMDAO.AEP.farm_AEP import FarmAEP
from WINDOW_openMDAO.Farm_IRR.farm_IRR import FarmIRR

from WINDOW_openMDAO.H2_production.H2_production import H2
from WINDOW_openMDAO.H2_production.LCoH import LCOH


class WorkingGroup(Group):
    def __init__(self, options):
        super(WorkingGroup, self).__init__()
        self.aep_model = options.models.aep
        self.wake_model = options.models.wake
        self.merge_model = options.models.merge
        self.turbine_model = options.models.turbine
        self.turbulence_model = options.models.turbulence
        self.electrical_model = options.models.electrical
        self.support_model = options.models.support
        self.opex_model = options.models.opex
        self.apex_model = options.models.apex
        self.windspeed_sampling_points = options.samples.wind_speeds
        self.direction_sampling_angle = options.samples.wind_sectors_angle
        # self.n_cases = int((360.0 / self.direction_sampling_angle) * (self.windspeed_sampling_points + 1.0))
        self.windrose_file = options.input.site.windrose_file
        self.bathymetry_file = options.input.site.bathymetry_file

        self.power_curve_file = options.input.turbine.power_file
        self.ct_curve_file = options.input.turbine.ct_file
        self.num_pegged = options.input.turbine.num_pegged
        self.num_airfoils = options.input.turbine.num_airfoils
        self.num_nodes = options.input.turbine.num_nodes
        self.num_bins = options.input.turbine.num_bins
        self.safety_factor = options.input.turbine.safety_factor
        self.gearbox_stages = options.input.turbine.gearbox_stages
        self.gear_configuration = options.input.turbine.gear_configuration
        self.mb1_type = options.input.turbine.mb1_type
        self.mb2_type = options.input.turbine.mb2_type
        self.drivetrain_design = options.input.turbine.drivetrain_design
        self.uptower_transformer = options.input.turbine.uptower_transformer
        self.has_crane = options.input.turbine.has_crane
        self.reference_turbine = options.input.turbine.reference_turbine
        self.reference_turbine_cost = options.input.turbine.reference_turbine_cost

        self.time_resolution = options.input.site.time_resolution
        self.wind_file = options.input.site.wind_file
        #self.wind_speed_file = options.input.site.wind_speed_file
        self.spot_price_file = options.input.market.spot_price_file

        self.electrolyser_ratio = options.input.hydrogen.electrolyser_ratio
        ### FAST addition ###
        self.num_tnodes = options.input.turbine.num_tnodes

    def setup(self):
        indep2 = self.add_subsystem('indep2', IndepVarComp(),
                                    promotes_outputs=['turbine_rad', 'rated_power', 'scaling_factor'])
        #                                    promotes_outputs=['design_tsr', 'chord_coefficients', 'twist_coefficients',
        #                                                     'pitch', 'tau'])

        indep2.add_output("areas", val=areas)
        indep2.add_output('layout', val=layout)
        indep2.add_output('turbine_rad', val=240/240.0)
        indep2.add_output('rated_power', val=15/15.0)
        indep2.add_output('scaling_factor', val=1)
        # indep2.add_output('turbine_radius', val=63.0)
        # indep2.add_output('turbine_radius', val=120.0)d
        # indep2.add_output('machine_rating', val = 5000.0)

        indep2.add_output('n_turbines', val=n_turbines)
        indep2.add_output('n_turbines_p_cable_type',
                          val=number_turbines_per_cable)  # In ascending order, but 0 always at the end. 0 is used for requesting only two or one cable type.
        indep2.add_output('substation_coords', val=central_platform)
        indep2.add_output('n_substations', val=number_substations)
        indep2.add_output('coll_electrical_efficiency', val=coll_electrical_efficiency)
        indep2.add_output('transm_electrical_efficiency', val=transm_electrical_efficiency)
        indep2.add_output('operational_lifetime', val=operational_lifetime)
        indep2.add_output('interest_rate', val=interest_rate)
        indep2.add_output('availability', val=0.97)



        indep2.add_output('design_tsr', desc='design tip speed ratio', val=9) #9 for the 10 MW; 8.5-9 for the 15 MW
        indep2.add_output('chord_coefficients', units='m', desc='coefficients of polynomial chord profile',
                          val=np.array(pegged_chord))
        indep2.add_output('twist_coefficients', units='deg', desc='coefficients of polynomial twist profile',
                          val=np.array(pegged_twist))
        indep2.add_output('pitch', units='deg', desc='pitch angle', val=0.0)
        indep2.add_output('tau', val=1)
        # indep2.add_output('tau_root')
        # indep2.add_output('tau_75')

        indep2.add_output('blade_number', desc='number of blades', val=3)
        indep2.add_output('span_airfoil_r', units='m',
                          desc='list of blade node radial location at which the airfoils are specified',
                          val=np.array(blade_span))
        indep2.add_output('span_airfoil_id', desc='list of blade node Airfoil ID', val=range(50))
        indep2.add_output('thickness_factor', desc='scaling factor for laminate thickness', val=1.0)
        indep2.add_output('shaft_angle', units='deg',
                          desc='angle of the LSS inclindation with respect to the horizontal', val=-6.0)
        indep2.add_output('cut_in_speed', units='m/s', desc='cut-in wind speed', val=4.0)
        indep2.add_output('cut_out_speed', units='m/s', desc='cut-out wind speed', val=25.0)
        # indep2.add_output('machine_rating', units='kW', desc='machine rating', val=5000.0)
        indep2.add_output('drive_train_efficiency', desc='efficiency of aerodynamic to electrical conversion',
                          val=0.944)
        indep2.add_output('gear_ratio', desc='overall gearbox ratio', val= 40) #check; 40 in BVG; 97 for the 5 MW
        indep2.add_output('Np', desc='number of planets in each stage', val=[3, 3, 1]) #3,3,1 default

        indep2.add_output('weibull_scale', desc='weibull scale parameter', val=8.469)
        indep2.add_output('weibull_shape', desc='weibull shape parameter', val=2.345)




        ## Design variables ##
        ## Use this format when optimizing ##
        '''

        indep2.add_output('chord_coefficients', units='m', desc='coefficients of polynomial chord profile',
                          val = np.array([1, 1,  1]))
        indep2.add_output('twist_coefficients', units='deg', desc='coefficients of polynomial twist profile',
                          val= np.array([1, 1, 1]))
        indep2.add_output('pitch', units='deg', desc='pitch angle', val=0.028)
        #indep2.add_output('tau_root', val=0.8)
        #indep2.add_output('tau_75', val=0.8)
        indep2.add_output('design_tsr', desc='design tip speed ratio', val=1)
        indep2.add_output('tau', val=1)'''

        self.add_subsystem('rad_scaling', ExecComp('turbine_radius = turbine_rad*120'))
        self.add_subsystem('power_scaling', ExecComp('machine_rating = rated_power*15000.0'))

        self.add_subsystem('rad2dia', ExecComp('rotor_diameter = turbine_radius*2.0', \
                                               rotor_diameter={'units': 'm'}))

        self.add_subsystem('rna', RNA(num_pegged=self.num_pegged, \
                                      num_airfoils=self.num_airfoils, \
                                      num_nodes=self.num_nodes, \
                                      num_bins=self.num_bins, \
                                      safety_factor=self.safety_factor, \
                                      gearbox_stages=self.gearbox_stages, \
                                      gear_configuration=self.gear_configuration, \
                                      mb1_type=self.mb1_type, \
                                      mb2_type=self.mb2_type, \
                                      drivetrain_design=self.drivetrain_design, \
                                      uptower_transformer=self.uptower_transformer, \
                                      has_crane=self.has_crane, \
                                      reference_turbine=self.reference_turbine, \
                                      reference_turbine_cost=self.reference_turbine_cost, \
                                      power_file=self.power_curve_file, \
                                      ct_file=self.ct_curve_file))
                         #promotes_inputs=['design_tsr', 'pitch', 'chord_coefficients', 'twist_coefficients',
                                     #    'tau'])

        ##### Add Preprocessor ####
        # self.add_subsystem('Preprocessor', Preprocessor(num_nodes=self.num_nodes, num_stations=self.num_stations))

        self.add_subsystem('usd2eur', ExecComp('cost_rna_eur = cost_rna_usd * 0.88'))

        self.add_subsystem('layout_scaling', LayoutScaling(max_n_turbines,max_n_substations))

        self.add_subsystem('numbersubstation', NumberLayout(max_n_substations))
        self.add_subsystem('numberlayout', NumberLayout(max_n_turbines))
        self.add_subsystem('depths', RoughClosestNode(max_n_turbines, self.bathymetry_file))
        self.add_subsystem('platform_depth', RoughClosestNode(max_n_substations, self.bathymetry_file))

        self.add_subsystem('AeroAEP', self.aep_model(self.wake_model, self.turbulence_model, self.merge_model,
                                                     self.direction_sampling_angle, self.windspeed_sampling_points,
                                                     self.windrose_file, self.power_curve_file, self.ct_curve_file))

        ## Add farm AEP module
        self.add_subsystem('FarmAEP', FarmAEP(wind_file=self.wind_file,
                                              direction_sampling_angle = self.direction_sampling_angle,
                                              time_resolution = self.time_resolution))

        self.add_subsystem('electrical', self.electrical_model())

        self.add_subsystem('support', self.support_model())

        self.add_subsystem('Costs', self.apex_model())





        self.add_subsystem('OandM', self.opex_model())
        self.add_subsystem('AEP', AEP())

        self.add_subsystem('lcoe', LCOE())
        self.add_subsystem('constraint_distance', MinDistance())
        self.add_subsystem('constraint_boundary', WithinBoundaries())

        self.add_subsystem('H2', H2(electrolyser_ratio = self.electrolyser_ratio,
                                    time_resolution = self.time_resolution))

        self.add_subsystem('LCoH', LCOH())



        ## Add farm IRR module
        self.add_subsystem('FarmIRR', FarmIRR(wind_file=self.wind_file,
                                              spot_price_file=self.spot_price_file,
                                              time_resolution = self.time_resolution))











        ## Different connects

        # self.connect('indep2.turbine_radius', 'rad2dia.turbine_radius')
        self.connect('turbine_rad', 'rad_scaling.turbine_rad')
        self.connect('rated_power', 'power_scaling.rated_power')

        self.connect('rad_scaling.turbine_radius', 'rad2dia.turbine_radius')
        self.connect('rad2dia.rotor_diameter', 'rna.rotor_diameter')
        self.connect('indep2.design_tsr', 'rna.design_tsr')
        self.connect('indep2.blade_number', 'rna.blade_number')
        self.connect('indep2.chord_coefficients', 'rna.chord_coefficients')
        self.connect('indep2.twist_coefficients', 'rna.twist_coefficients')
        self.connect('indep2.span_airfoil_r', 'rna.span_airfoil_r')
        self.connect('indep2.span_airfoil_id', 'rna.span_airfoil_id')
        self.connect('indep2.pitch', 'rna.pitch')
        # self.connect('indep2.thickness_factor', 'rna.thickness_factor')
        self.connect('indep2.shaft_angle', 'rna.shaft_angle')
        self.connect('indep2.cut_in_speed', 'rna.cut_in_speed')
        self.connect('indep2.cut_out_speed', 'rna.cut_out_speed')
        # self.connect('indep2.machine_rating', 'rna.machine_rating')
        self.connect('power_scaling.machine_rating', 'rna.machine_rating')
        self.connect('indep2.drive_train_efficiency', 'rna.drive_train_efficiency')
        self.connect('indep2.gear_ratio', 'rna.gear_ratio')
        self.connect('indep2.Np', 'rna.Np')
        self.connect('rna.cost_rna', 'usd2eur.cost_rna_usd')

        # self.connect('indep2.turbine_radius', 'AeroAEP.turbine_radius')
        self.connect('rad_scaling.turbine_radius', 'AeroAEP.turbine_radius')
        self.connect('indep2.cut_in_speed', 'AeroAEP.cut_in_speed')
        self.connect('indep2.cut_out_speed', 'AeroAEP.cut_out_speed')
        # self.connect('indep2.machine_rating', 'AeroAEP.machine_rating')
        self.connect('power_scaling.machine_rating', 'AeroAEP.machine_rating')
        self.connect('rna.rated_wind_speed', 'AeroAEP.rated_wind_speed')

        ###### Layout scaling connects ######

        self.connect('indep2.layout', 'layout_scaling.orig_layout')
        self.connect('indep2.substation_coords', 'layout_scaling.substation_coords')
        self.connect('rad_scaling.turbine_radius', 'layout_scaling.turbine_radius')
        self.connect('scaling_factor', 'layout_scaling.scaling_factor')

        self.connect("layout_scaling.new_layout", ["numberlayout.orig_layout", "AeroAEP.layout", "constraint_distance.orig_layout",
                                       "constraint_boundary.layout"])
        self.connect("layout_scaling.new_substation_coords", "numbersubstation.orig_layout")

        self.connect('layout_scaling.farm_area', 'Costs.farm_area')
        #self.connect("indep2.layout", ["numberlayout.orig_layout", "AeroAEP.layout", "constraint_distance.orig_layout",
                                       #"constraint_boundary.layout"])
        #self.connect("indep2.substation_coords", "numbersubstation.orig_layout")



        # self.connect("indep2.turbine_radius", "constraint_distance.turbine_radius")
        self.connect("rad_scaling.turbine_radius", "constraint_distance.turbine_radius")
        self.connect("indep2.areas", "constraint_boundary.areas")

        self.connect('numberlayout.number_layout', 'depths.layout')

        self.connect('indep2.n_turbines',
                     ['AeroAEP.n_turbines', 'electrical.n_turbines', 'support.n_turbines', 'Costs.n_turbines'])

        self.connect('numberlayout.number_layout', 'electrical.layout')
        self.connect('indep2.n_turbines_p_cable_type', 'electrical.n_turbines_p_cable_type')
        self.connect('indep2.substation_coords', 'electrical.substation_coords')
        self.connect('indep2.n_substations', 'electrical.n_substations')
        self.connect('rna.turbine_rated_current', 'electrical.turbine_rated_current')

        self.connect('depths.water_depths', 'support.depth')
        self.connect('AeroAEP.max_TI', 'support.max_TI')
        # self.connect('indep2.turbine_radius', 'support.rotor_radius')
        self.connect('rad_scaling.turbine_radius', 'support.rotor_radius')
        self.connect('rna.rated_wind_speed', 'support.rated_wind_speed')
        self.connect('rna.rotor_thrust', 'support.rotor_thrust')
        self.connect('rna.rna_mass', 'support.rna_mass')
        self.connect('rna.solidity_rotor', 'support.solidity_rotor')
        self.connect('rna.cd_rotor_idle_vane', 'support.cd_rotor_idle_vane')
        self.connect('rna.cd_nacelle', 'support.cd_nacelle')
        self.connect('rna.tower_top_diameter', 'support.yaw_diameter')
        self.connect('rna.front_area_nacelle', 'support.front_area_nacelle')
        self.connect('rna.yaw_to_hub_height', 'support.yaw_to_hub_height')
        self.connect('rna.mass_eccentricity', 'support.mass_eccentricity')



        #self.connect('indep2.tau', 'rna.tau')  #### uniform Thickness factor

        self.connect('AeroAEP.efficiency', 'OandM.array_efficiency')
        #self.connect('AeroAEP.AEP', ['AEP.aeroAEP', 'OandM.AEP'])
        self.connect('FarmAEP.farm_AEP', ['AEP.aeroAEP', 'OandM.AEP'])
        self.connect('rna.hub_height', 'FarmAEP.hub_height')

        self.connect('indep2.n_turbines', 'OandM.N_T')
        self.connect('power_scaling.machine_rating', 'OandM.P_rated')



        self.connect('OandM.availability', 'AEP.availability')
        self.connect('indep2.coll_electrical_efficiency', 'AEP.electrical_efficiency')

        self.connect('numbersubstation.number_layout', 'platform_depth.layout')
        self.connect('platform_depth.water_depths', 'Costs.depth_central_platform', src_indices=[0])

        self.connect('indep2.n_substations', 'Costs.n_substations')
        self.connect('electrical.length_p_cable_type', 'Costs.length_p_cable_type')
        self.connect('electrical.cost_p_cable_type', 'Costs.cost_p_cable_type')
        self.connect('support.cost_support', 'Costs.support_structure_costs')
        self.connect('support.support_decomm_costs', 'Costs.support_decomm_costs')
        # self.connect('indep2.machine_rating', 'Costs.machine_rating')
        self.connect('power_scaling.machine_rating', 'Costs.machine_rating')
        # self.connect('indep2.turbine_radius', 'Costs.rotor_radius')
        self.connect('rad_scaling.turbine_radius', 'Costs.rotor_radius')
        self.connect('rna.hub_height', 'Costs.hub_height')
        self.connect('usd2eur.cost_rna_eur', 'Costs.purchase_price')
        self.connect('rna.warranty_percentage', 'Costs.warranty_percentage')
        self.connect('rna.rna_mass', 'Costs.rna_mass')
        self.connect('rna.generator_voltage', 'Costs.generator_voltage')
        self.connect('rna.collection_voltage', 'Costs.collection_voltage')



        self.connect('Costs.investment_costs', 'lcoe.investment_costs')
        self.connect('OandM.annual_cost_O&M', 'lcoe.oandm_costs')
        self.connect('Costs.decommissioning_costs', 'lcoe.decommissioning_costs')
        self.connect('FarmAEP.farm_AEP', 'lcoe.AEP')
        self.connect('indep2.transm_electrical_efficiency', 'lcoe.transm_electrical_efficiency')
        self.connect('indep2.operational_lifetime', 'lcoe.operational_lifetime')
        self.connect('indep2.interest_rate', 'lcoe.interest_rate')
        self.connect('indep2.availability', 'lcoe.availability')



        # farm IRR connects

        self.connect('FarmAEP.farm_power', 'FarmIRR.farm_power')
        self.connect('indep2.operational_lifetime', 'FarmIRR.operational_lifetime')
        self.connect('indep2.transm_electrical_efficiency', 'FarmIRR.transm_electrical_efficiency')
        self.connect('Costs.investment_costs_h2', 'FarmIRR.investment_costs')
        self.connect('OandM.annual_cost_O&M', 'FarmIRR.oandm_costs')
        self.connect('Costs.decommissioning_costs', 'FarmIRR.decommissioning_costs')

        self.connect('H2.H2_produced', 'FarmIRR.H2_produced')
        self.connect('H2.H2_CAPEX', 'FarmIRR.H2_CAPEX')
        self.connect('H2.H2_OPEX', 'FarmIRR.H2_OPEX')
        self.connect('H2.power_curtailed', 'FarmIRR.power_curtailed')


        # H2 connects

        self.connect('indep2.n_turbines', 'H2.N_T')
        self.connect('power_scaling.machine_rating', 'H2.P_rated')
        self.connect('FarmAEP.farm_power', 'H2.farm_power')
        #self.connect('indep2.transm_electrical_efficiency', 'H2.transmission_efficiency')

        self.connect('H2.annual_H2', 'LCoH.annual_H2')
        self.connect('H2.H2_CAPEX', 'LCoH.H2_CAPEX')
        self.connect('H2.H2_OPEX', 'LCoH.H2_OPEX')
        self.connect('indep2.interest_rate', 'LCoH.interest_rate')
        self.connect('indep2.operational_lifetime', 'LCoH.operational_lifetime')
        self.connect('Costs.investment_costs_h2', 'LCoH.investment_costs')
        self.connect('OandM.annual_cost_O&M', 'LCoH.oandm_costs')
        self.connect('Costs.decommissioning_costs_h2', 'LCoH.decommissioning_costs')
        self.connect('indep2.availability', 'LCoH.availability')






        ## Subsystem and Connections for Objective and Constraints ##
        #self.add_subsystem('obj', ExecComp('f=lcoe'))  # Reference value
        #self.connect('lcoe.LCOE', 'obj.lcoe')

        self.add_subsystem('obj', ExecComp('f=-1*IRR'))  # Reference value
        self.connect('FarmIRR.IRR', 'obj.IRR')

        ### For SLSQP ###

        #self.add_subsystem('c1', ExecComp('tip_deflection = deflection*63.0/turbine_radius/7.07'))  # Reference value
        #self.connect('rna.tip_deflection', 'c1.deflection')
        #self.connect('rad_scaling.turbine_radius', 'c1.turbine_radius')

        #self.add_subsystem('c2', ExecComp('ramp = ramp_90/15.0'))  # Reference value
        #self.connect('single_turbine.ramp_90', 'c2.ramp_90')




        '''
        self.add_subsystem('c1', ExecComp('tip_deflection=deflection/7.07'))  # Reference value
        self.connect('rna.tip_deflection', 'c1.deflection')

        self.add_subsystem('c2', ExecComp('Spar_stress=max_stress_spar/1047'))  # Reference value
        self.connect('rna.max_stress_spar', 'c2.max_stress_spar')

        self.add_subsystem('c3', ExecComp('Skin_stress=max_stress_skin/700'))  # Reference value
        self.connect('rna.max_stress_skin', 'c3.max_stress_skin')

        self.add_subsystem('c4', ExecComp('Te_Reinf_stress=max_stress_te_reinf/702'))  # Reference value
        self.connect('rna.max_stress_te_reinf', 'c4.max_stress_te_reinf')'''

        ### For GA ###
        '''

        self.add_subsystem('c1', ExecComp('tip_deflection=deflection'))  # Reference value
        self.connect('rna.tip_deflection', 'c1.deflection')

        self.add_subsystem('c2', ExecComp('Spar_stress=max_stress_spar'))  # Reference value
        self.connect('rna.max_stress_spar', 'c2.max_stress_spar')

        self.add_subsystem('c3', ExecComp('Skin_stress=max_stress_skin'))  # Reference value
        self.connect('rna.max_stress_skin', 'c3.max_stress_skin')

        self.add_subsystem('c4', ExecComp('Te_Reinf_stress=max_stress_te_reinf'))  # Reference value
        self.connect('rna.max_stress_te_reinf', 'c4.max_stress_te_reinf')'''





