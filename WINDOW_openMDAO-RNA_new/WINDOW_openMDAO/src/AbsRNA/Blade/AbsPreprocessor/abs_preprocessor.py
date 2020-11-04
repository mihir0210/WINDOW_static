from openmdao.api import ExplicitComponent

class AbsPreprocessor(ExplicitComponent):
    def initialize(self):
        self.metadata.declare('num_stations', desc='Number of stations along the blade')
        self.metadata.declare('num_nodes', desc='Number of nodes along the blade')


    def setup(self):
        # metadata

        #num_stations = self.metadata['num_stations']
        num_nodes = self.metadata['num_nodes']




        # Internal layup inputs
        '''self.add_input('web', desc='web thickness')
        self.add_input('skin', desc='skin triax thickness')
        self.add_input('root', desc='root triax thickness')
        self.add_input('le_core_thicknesses', units='mm', desc='Leading edge core thicknesses along the blade',
                       shape=num_stations)
        self.add_input('te_core_thicknesses', units='mm', desc='Trailing edge core thicknesses along the blade',
                       shape=num_stations)
        self.add_input('spar_thicknesses', units='mm', desc='Spar UD thicknesses along the blade',
                       shape=num_stations)

        self.add_input('te_reinf_thicknesses', units='mm', desc='Trailing edge UD thicknesses along the blade',
                   shape=num_stations-1)'''
        #self.add_input('tau_root', desc='Thickness factor at root')
        #self.add_input('tau_75', desc='Thickness factor at 75 % span')

        self.add_input('tau', desc='Overall Thickness factor')


        self.add_input('span_r', desc='Absolute value of Span radius', shape=num_nodes)
        self.add_input('span_dr', desc='Absolute value of Span element lengths', shape=num_nodes)
        self.add_input('span_chord', desc='Absolute value of Span chord', shape=num_nodes)
        self.add_input('span_airfoil', desc='Absolute value of Span airfoil', shape=num_nodes)

        # Internal layup outputs
        self.add_output('flapwise_stiffness', desc='Spanwise flapwise stiffness', shape=num_nodes)
        self.add_output('edgewise_stiffness', desc='Spanwise edgewise stiffness', shape=num_nodes)
        self.add_output('mass_length', desc='Spanwise mass per unit length', shape=num_nodes)
        self.add_output('total_blade_mass', desc='Total mass of the blade')

