from openmdao.api import ExplicitComponent

class AbsAlkaline(ExplicitComponent):

    def initialize(self):
        self.metadata.declare('electrolyser_ratio', desc='Ratio of electroylser rated power to farm rated power')
        self.metadata.declare('time_resolution', desc = 'Number of time points in a year')

    def setup(self):

        time_points = self.metadata['time_resolution']

        #inputs
        self.add_input('N_T', desc='Number of turbines')
        self.add_input('P_rated', desc='Rated power of the turbine')
        self.add_input('farm_power', desc='hourly wind farm power', shape=time_points)
        self.add_input('transmission_efficiency', desc='Export cable efficiency')

        #outputs
        self.add_output('annual_H2', desc='Annual production of H2 in kg')
        self.add_output('H2_CAPEX', desc='Capital expenditures of H2 facility')
        self.add_output('H2_OPEX', desc='Operational costs of H2 facility')

