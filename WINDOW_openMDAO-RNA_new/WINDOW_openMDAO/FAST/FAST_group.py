from openmdao.api import Group, Problem, IndepVarComp, view_model
import FAST
from WINDOW_openMDAO.RNA.Blade import aerodynamic_design, structural_design, power_curve
import numpy as np


#############################################################################
############################ FAST WORKFLOW #################################
#############################################################################
class FAST_group(Group):
    def initialize(self):
        # fixed parameters
        self.metadata.declare('num_pegged', desc='Number of pegged nodes required to define the chord/twist profile')
        self.metadata.declare('num_airfoils', desc='Number of airfoils along the blade')
        self.metadata.declare('num_nodes', desc='Number of blade sections')
        self.metadata.declare('num_tnodes', desc='Number of tower sections')
        self.metadata.declare('num_bins', desc='Number of wind speed samples')
        self.metadata.declare('reference_turbine', desc='CSV file with the definition of the Reference Turbine')
        self.metadata.declare('rho_air', desc='Density of air [kg/m**3]', default=1.225)
        #self.metadata.declare('E_blade', desc='Youngs modulus of glass fiber [Pa]', default=36.233e9)
        #self.metadata.declare('g', desc='acceleration due to gravity [m/s**2]', default=9.8)
        self.metadata.declare('tower_sm', desc='Tower material Shear modulus', default='80.8*10**9')
        self.metadata.declare('tower_ym', desc='Tower Youngs modulus', default='210*10**9')
        self.metadata.declare('tower_density', desc='Tower material density', default='7850')

    def setup(self):
        # metadata
        num_pegged = self.metadata['num_pegged']
        num_airfoils = self.metadata['num_airfoils']
        num_nodes = self.metadata['num_nodes']
        num_tnodes = self.metadata['num_tnodes']
        num_bins = self.metadata['num_bins']
        reference_turbine = self.metadata['reference_turbine']
        rho_air = self.metadata['rho_air']
        tower_sm = self.metadata['tower_sm']
        tower_ym = self.metadata['tower_ym']
        tower_density = self.metadata['tower_density']
        #E_blade = self.metadata['E_blade']
        #g = self.metadata['g']



        #sub systems

        self.add_subsystem('aero_design', aerodynamic_design.Scaling(num_pegged=num_pegged, num_nodes=num_nodes,
                                                                     num_airfoils=num_airfoils,
                                                                     reference_turbine=reference_turbine))

        self.add_subsystem('struc_design',
                           structural_design.VariableRadius(num_nodes=num_nodes, reference_turbine=reference_turbine))




        self.add_subsystem('FAST', FAST.FAST(num_airfoils=num_airfoils, num_nodes= num_nodes, num_tnodes=num_tnodes,
                                             tower_sm=tower_sm, tower_ym=tower_ym, tower_density=tower_density,
                                             rho_air=rho_air))



        # connections
        self.connect('aero_design.span_r', ['struc_design.span_r', 'FAST.blade_radius'])
        self.connect('aero_design.span_dr', ['struc_design.span_dr'])
        self.connect('aero_design.span_airfoil', ['FAST.blade_nfoil'])
        self.connect('aero_design.span_chord', ['struc_design.span_chord', 'FAST.blade_chord'])
        self.connect('aero_design.span_twist', ['FAST.blade_twist'])



        self.connect('struc_design.span_mass', ['FAST.blade_mass'])
        self.connect('struc_design.span_flap_stiff', ['FAST.blade_ei_flap'])
        self.connect('struc_design.span_edge_stiff', ['FAST.blade_ei_edge'])




    #############################################################################


##############################  UNIT TESTING ################################
# Activate (Uncomment) the design variables in the Group
#############################################################################
if __name__ == "__main__":
    from time import time
    from WINDOW_openMDAO.src.api import beautify_dict

    start = time()

    # workflow setup
    prob = Problem(FAST_group(num_pegged=3, num_airfoils=8, num_nodes=49, num_bins=30, num_tnodes=11,
                         reference_turbine='Airfoils/reference_turbine.csv',
                         rho_air=1.225, tower_sm=80.8*10**9, tower_ym=210*10**9, tower_density=7850))
    prob.setup()
    # view_model(prob)

    # define inputs
    prob['struc_design.rotor_diameter'] = 126.0
    prob['aero_design.rotor_diameter'] = 126.0
    prob['aero_design.hub_radius'] = 1.5
    prob['aero_design.chord_coefficients'] = [3.38, 3.05, 2.28]
    prob['aero_design.twist_coefficients'] = [13.23, 8.5, 3.23]
    prob['aero_design.span_airfoil_r'] = [01.36, 06.83, 10.25, 14.35, 22.55, 26.65, 34.85, 43.05]
    prob['aero_design.span_airfoil_id'] = [0, 1, 2, 3, 4, 5, 6, 7]
    prob['FAST.blade_ifoil']=[0, 1, 2, 3, 4, 5, 6, 7]
    #prob['pitch'] = 0.0
    prob['struc_design.thickness_factor'] = 1.0
    #prob['shaft_angle'] = -5.0
    prob['FAST.rated_power']=5000000.0
    prob['struc_design.blade_number'] = 3.0
    prob['aero_design.rotor_diameter']=126.0
    prob['struc_design.rotor_diameter']=126.0

    #for blade, tower, nacelle
    prob['FAST.blade_number'] = 3.0
    prob['FAST.blade_cone'] = 2.5
    '''
    prob['blade_ifoil'] = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    
    prob['blade_mass']=np.array([678.9, 639, 423.5, 342.64, 314.66, 260, 208, 154.67, 103.89, 72.67])
    prob['blade_ei_flap']=np.array([1.8 * 10 ** 10, 1.2 * 10 ** 10, 4.407 * 10 ** 9, 2.15 * 10 ** 9, 1.38 * 10 ** 9, 6.37 * 10 ** 8,
                     2.65 * 10 ** 8, 1.07 * 10 ** 8, 5.69 * 10 ** 7, 4.09 * 10 ** 6])
    prob['blade_ei_edge']=np.array([1.8 * 10 ** 10, 1.64 * 10 ** 10, 7.23 * 10 ** 9, 4.63 * 10 ** 9, 3.77 * 10 ** 9, 2.68 * 10 ** 9,
                     1.67 * 10 ** 9, 1.02 * 10 ** 9, 4.92 * 10 ** 8, 8.81 * 10 ** 7])
    prob['blade_radius']=np.array([1.5, 6.62, 13.03, 19.43, 25.85, 32.25, 38.65, 45.06, 51.47, 63])
    prob['blade_chord']=np.array([3.39, 3.97, 4.60, 4.49, 4.15, 3.75, 3.36, 2.98, 2.59, 0.96])
    prob['blade_twist']=np.array([13.23, 13.23, 12.91, 10.24, 8.41, 6.47, 4.62, 2.94, 1.7, 0])
    prob['blade_nfoil']=np.array([0, 0, 2, 3, 4, 5, 6, 7, 7, 7])'''




    prob['FAST.tower_hh'] = 90.0
    prob['FAST.tower_bthickness'] = 0.027
    prob['FAST.tower_tthickness'] = 0.019
    prob['FAST.tower_height'] = np.array([0, 8.76, 17.52, 26.28, 35, 43.8, 52.56, 61.32, 70.08, 78.84, 87.76])
    prob['FAST.tower_extramass'] =np.array([329, 308, 287, 268, 249, 230, 213, 196, 179, 164, 149])
    prob['FAST.tower_diameter'] = np.array([6, 5.78, 5.57, 5.36, 5.15, 4.935, 4.722, 4.509, 4.296, 4.083, 3.87])

    prob['FAST.drivetrain_gen_eff'] = 0.944
    #prob['FAST.drivetrain_gen_hssinertia'] = 534.116
    prob['FAST.drivetrain_gear_ratio'] = 97.0
    prob['FAST.drivetrain_gear_eff'] = 1.0
    prob['FAST.nacelle_hub_length'] = 5.0
    prob['FAST.nacelle_hub_mass'] = 56780.0
    prob['FAST.nacelle_hub_overhang'] = 5.0
    prob['FAST.nacelle_hub_type'] = 1.0
    prob['FAST.nacelle_hub_shafttilt'] = 5.0
    prob['FAST.nacelle_housing_type'] = 1.0
    prob['FAST.nacelle_housing_diameter'] = 5.0
    prob['FAST.nacelle_housing_length'] = 10.0
    prob['FAST.nacelle_housing_mass'] = 240000.0


    prob.run_model()
    print 'Executed in ' + str(round(time() - start, 2)) + ' seconds\n'

    ''''# print outputs
    var_list = ['rotor_torque', 'rotor_thrust', 'rated_wind_speed', 'wind_bin', 'elec_power_bin', \
                'ct_bin', 'root_moment_flap', 'span_stress_max', 'tip_deflection', 'blade_mass', \
                'rotor_cp', 'rotor_ct']
    saved_output = {}
    for v in var_list:
        saved_output[v] = prob[v]

    beautify_dict(saved_output)'''