from openmdao.api import Group, Problem

from WINDOW_openMDAO.H2_production.Alkaline.alkaline import Alkaline


'''
This class determines the hydrogen production and costs given the electrolyser technology
and electrolyser to farm ratio
'''

##### WORKFLOW #####

class H2(Group):

    def initialize(self):
        ### FIXED USER-DEFINED PARAMETERS ###
        self.metadata.declare('electrolyser_ratio', desc='Ratio of electrolyser capacity to wind farm capacity')
        self.metadata.declare('time_resolution', desc = 'Number of time points in a year')

    def setup(self):
        electrolyser_ratio = self.metadata['electrolyser_ratio']
        time_resolution = self.metadata['time_resolution']


        #Add the two electrolyser

        self.add_subsystem('Alkaline', Alkaline(electrolyser_ratio = electrolyser_ratio, time_resolution = time_resolution),
                           promotes_inputs=['N_T', 'P_rated', 'farm_power', 'transmission_efficiency'],
                           promotes_outputs=['annual_H2', 'H2_CAPEX', 'H2_OPEX'])


        #self.add_subsystem('PEM', PEM())




#############################################################################
##############################  UNIT TESTING ################################

if __name__ == "__main__":
    prob = Problem(H2(electrolyser_ratio = 0.5, time_resolution = 4))

    prob.setup()

    prob['N_T'] = 100
    prob['P_rated'] = 10000.0
    prob['farm_power'] = [1000, 20, 400, 160]
    prob['transmission_efficiency'] = 0.95

    prob.run_model()

    print prob['annual_H2']
    print prob['H2_CAPEX']
    print prob['H2_OPEX']