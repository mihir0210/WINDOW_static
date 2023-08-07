from openmdao.api import ExplicitComponent

class AbsPemDecentralized(ExplicitComponent):

    def initialize(self):
        #self.options.declare('electrolyser_ratio', desc='Ratio of electroylser rated power to farm rated power')
        self.options.declare('time_resolution', desc = 'Number of time points in a year')

    def setup(self):

        time_points = self.options['time_resolution']

        #inputs
        self.add_input('N_T', desc='Number of turbines')
        self.add_input('P_rated', desc='Rated power of the turbine')
        self.add_input('farm_power', desc='hourly wind farm power', shape=time_points)

        #outputs
        self.add_output('annual_H2', desc='Annual production of H2 in kg')
        self.add_output('C_stacks', desc='Capital expenditures of electrolyzer stacks')
        self.add_output('H2_CAPEX', desc='Capital expenditures of H2 facility')
        self.add_output('H2_OPEX', desc='Operational costs of H2 facility')
        self.add_output('H2_produced', desc='hourly hydrogen production', shape=time_points)
        self.add_output('power_curtailed', desc='hourly farm power curtailed', shape=time_points)

