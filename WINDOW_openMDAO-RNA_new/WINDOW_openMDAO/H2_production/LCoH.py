from openmdao.api import ExplicitComponent
#from time import clock
import numpy as np
import csv

class LCOH(ExplicitComponent):

    def setup(self):

        self.add_input('investment_costs', val=0.0)
        self.add_input('oandm_costs', val=0.0)
        self.add_input('decommissioning_costs', val=0.0)
        self.add_input('annual_H2', val=0.0)
        self.add_input('C_stacks', val=0.0)
        self.add_input('H2_OPEX',val=0.0)
        self.add_input('operational_lifetime', val=0.0)
        self.add_input('interest_rate', val=0.0)
        self.add_input('availability', val=0.0)

        self.add_output('LCoH', val=0.0)



    def compute(self, inputs, outputs):
        investment_costs = inputs['investment_costs']
        oandm_costs = inputs['oandm_costs']
        decommissioning_costs = inputs['decommissioning_costs']
        annual_H2 = inputs['annual_H2']*inputs['availability']
        C_stacks = inputs['C_stacks']
        H2_OPEX = inputs['H2_OPEX']
        operational_lifetime = inputs['operational_lifetime']
        i = inputs['interest_rate']


        total_CAPEX = investment_costs # includes H2_CAPEX
        total_OPEX = oandm_costs + H2_OPEX


        n = list(range(int(operational_lifetime)))
        n.remove(0)
        n.append(int(operational_lifetime))

        a = np.sum((total_OPEX / (1 + i) ** t) for t in n)
        b = np.sum((annual_H2 / (1 + i) ** t) for t in n)
        c = decommissioning_costs/(1+i)**operational_lifetime

        replacement_yr = 10
        #stack_replacement_costs = H2_CAPEX/1.5/(1+i)**replacement_yr #dividing by 1.5 to remove indirect costs and only consider component costs for replacement
        stack_costs = C_stacks*1.3*0.88  #only stack costs $400/kW and not compressor, bop. Multiplied by a factor for installation and usd to eur
        stack_replacement_costs = stack_costs/ (1 + i) ** replacement_yr


        LCoH = (total_CAPEX + a + c + stack_replacement_costs)/b # in Euros/kg

        print('total discounted O&M:', a)
        #print 'WIND CAPEX:', investment_costs
        #print('LCoH:', LCoH)

        #print('discounted H2', b)

        field_names = ['discounted_h2','lcoh']
        description =['Total discounted hydrogen produced over the lifetime', 'Levelized cost of hydrogen']
        data = {field_names[0]: [b[0], description[0]], field_names[1]:[LCoH[0], description[1]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()

        outputs['LCoH'] = LCoH


#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":

    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'investment_costs': 4.72709495e+09, \
              'oandm_costs': 85000000, \
              'decommissioning_costs': 3.73203684e+08, \
              'operational_lifetime': 20.0,\
              'interest_rate': 0.075,\
              'H2_CAPEX': 1.4001e+09,\
              'H2_OPEX': 28002000,\
              'annual_H2': 1.07037509e+08}


    outputs = {}

    model = LCOH()


    model.compute(inputs, outputs)

    print(outputs['LCoH'])
