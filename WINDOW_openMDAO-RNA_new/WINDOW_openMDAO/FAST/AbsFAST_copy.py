from openmdao.api import ExplicitComponent


class AbsFAST(ExplicitComponent):
    def initialize(self):
        self.metadata.declare('num_airfoils', desc='Number of airfoils along the blade')
        self.metadata.declare('num_nodes', desc='Number of blade sections')
        self.metadata.declare('num_tnodes', desc='Number of tower sections')
        self.metadata.declare('tower_sm', desc='Tower material Shear modulus', default='80.8*10**9')
        self.metadata.declare('tower_ym', desc='Tower Youngs modulus', default='210*10**9')
        self.metadata.declare('tower_density', desc='Tower material density', default='7850')
        self.metadata.declare('rho_air', desc='density of air', default='1.225')

    def setup(self):
        # metadata
        num_airfoils = self.metadata['num_airfoils']
        num_nodes = self.metadata['num_nodes']
        num_tnodes=self.metadata['num_tnodes']


        # blade inputs
        self.add_input('blade_mass', desc='Mass of 1 blade', shape=num_nodes)
        self.add_input('blade_ei_flap', desc='Flapwise stiffness', shape=num_nodes)
        self.add_input('blade_ei_edge', desc='Edgewise stiffness', shape=num_nodes)
        self.add_input('blade_radius', units='m', desc='Radius along the blade', shape=num_nodes)
        self.add_input('blade_chord', units='m', desc='Spanwise chord distribution', shape=num_nodes)
        self.add_input('blade_twist', units='deg', desc='Spanwise twist distribution', shape=num_nodes)
        self.add_input('blade_nfoil', desc='Airfoil ID distribution', shape=num_nodes)
        self.add_input('blade_ifoil', desc='Different Blade ID', shape=num_airfoils)
        self.add_input('blade_cone', units='deg', desc='Blade cone angle')
        self.add_input('blade_number', desc='Number of blades')
        self.add_input('pitch', desc='Fine pitch angle')
        self.add_input('design_tsr', desc='Tip speed ratio')
        #self.add_input('tau_root', desc='Thickness factor at root')
        #self.add_input('tau_75', desc='Thickness factor at 75 %')
        self.add_input('tau', desc='Overall Thickness factor')
        self.add_input('rotor_diameter', desc='Rotor Diameter')
        self.add_input('rotor_area', desc='Rotor Area')

        self.add_input('rated_ws', desc='Rated Wind speed')
        self.add_input('blade_mass_total', desc = 'Total blade_mass')
        self.add_input('Cp', desc = 'Co-efficient of Performance')


        #Tower inputs
        self.add_input('tower_hh', units='m', desc='Hub height')
        self.add_input('tower_bthickness', units='m', desc='tower bottom thickness')
        self.add_input('tower_tthickness', units='m', desc='tower top thickness')
        #self.add_input('tower_height', units='m', desc='spanwise tower height', shape=num_tnodes)
        self.add_input('tower_extramass', units='m', desc='spanwise tower extra mass', shape=num_tnodes)
        #self.add_input('tower_diameter', units='m', desc='spanwise tower diameter', shape=num_tnodes)
        self.add_input('tower_top_dia', units='m', desc='Tower top diameter')
        self.add_input('tower_base_dia', units='m', desc='Tower base diameter')

        #DriveTrain and Nacelle inputs
        self.add_input('drivetrain_gen_eff', desc='Drivetrain generator efficiency')
        #self.add_input('drivetrain_gen_hssinertia', desc='Drivetrain generator high speed shaft inertia')
        self.add_input('drivetrain_gear_ratio', desc='Drivetrain gearbox ratio')
        self.add_input('drivetrain_gear_eff', desc='Drivetrain gearbox efficiency')

        self.add_input('nacelle_hub_length', desc='Nacelle hub length')
        self.add_input('nacelle_hub_mass', desc='Nacelle hub mass')
        self.add_input('nacelle_hub_overhang', desc='Nacelle hub overhang')
        self.add_input('nacelle_hub_type', desc='Nacelle hub type')
        self.add_input('nacelle_hub_shafttilt', desc='Nacelle hub shaft tilt')
        self.add_input('nacelle_housing_type', desc='Nacelle housing type')
        self.add_input('nacelle_housing_diameter', desc='Nacelle housing diameter')
        self.add_input('nacelle_housing_length', desc='Nacelle housing length')
        self.add_input('nacelle_housing_mass', desc='Nacelle housing mass')

        #Controls inputs
        self.add_input('rated_power', desc='rated electrical power')

        #other parameters
        #self.add_input('rated_ws', desc='rated wind speed')


        ### Outputs ###
        self.add_output('Tip_Deflection', desc='Tip deflection in m')
        self.add_output('Max_Stress_Skin', desc='Maximum Stress in the skin')
        self.add_output('Max_Stress_Spar', desc='Maximum Stress in the UD-C spar caps')
        self.add_output('Max_Stress_Te_Reinf',desc='Maximum stress in the Trailing edge reinforcement glass fibre')