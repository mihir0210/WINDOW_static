from openmdao.api import Group, Problem

from WINDOW_openMDAO.H2_production.Alkaline.alkaline import ALKALINE
from WINDOW_openMDAO.H2_production.PEM.pem_decentralized import PEM_DECENTRALIZED


'''
This class determines the hydrogen production and costs given the electrolyser technology
and electrolyser to farm ratio
'''

##### WORKFLOW #####

class H2(Group):

    def initialize(self):
        ### FIXED USER-DEFINED PARAMETERS ###
        self.options.declare('electrolyser_ratio', desc='Ratio of electrolyser capacity to wind farm capacity')
        self.options.declare('time_resolution', desc = 'Number of time points in a year')

    def setup(self):
        electrolyser_ratio = self.options['electrolyser_ratio']
        time_resolution = self.options['time_resolution']


        #Add the two electrolysers

        # self.add_subsystem('Alkaline', ALKALINE(electrolyser_ratio = electrolyser_ratio, time_resolution = time_resolution),
        #                    promotes_inputs=['N_T', 'P_rated', 'farm_power', 'transmission_efficiency'],
        #                    promotes_outputs=['annual_H2', 'H2_CAPEX', 'H2_OPEX', 'H2_produced', 'power_curtailed'])


        self.add_subsystem('PEM', PEM_DECENTRALIZED(time_resolution = time_resolution),
                           promotes_inputs=['N_T', 'P_rated', 'farm_power'],
                           promotes_outputs=['annual_H2', 'H2_CAPEX', 'H2_OPEX', 'H2_produced', 'power_curtailed'])





#############################################################################
##############################  UNIT TESTING ################################

if __name__ == "__main__":
    prob = Problem(H2(electrolyser_ratio = 0.5, time_resolution = 4))

    prob.setup()

    prob['N_T'] = 100
    prob['P_rated'] = 10000.0
    prob['farm_power'] = [1000, 20, 400, 160]
    #prob['transmission_efficiency'] = 0.95

    prob.run_model()

    print((prob['annual_H2']))
    print((prob['H2_CAPEX']))
    print((prob['H2_OPEX']))