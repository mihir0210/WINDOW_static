from WINDOW_openMDAO.src.api import AbstractOandM
from openmdao.api import ExplicitComponent
import csv

class OM_model1(AbstractOandM):
    def OandM_model(self, AEP, eff, N_T, P_rated, hub_height, rna_capex, farm_capex, bop_costs):
        costs_om = 16.0 * AEP / eff / 1000000.0
        availability = 1 #0.98
        # costs_om = 50000000.
        #costs_om = 85000000 #taken from BVG for a 1000 MW farm

        farm_rated = N_T*P_rated/1000 # FARM rated power in MW

        # total = 85e6 #taken from BVG for a 1000 MW farm
        # fixed = 1
        # variable = 1 - fixed
        # fixed_costs = fixed*total
        # variable_costs = variable*total*(farm_rated/1500)
        #
        # costs_om = fixed_costs + variable_costs
        #print 'farm_capex_norm', farm_capex_norm
        #print 'hub height norm', hub_height_norm
        #print 'rna norm', rna_norm
        #print 'bop norm', bop_norm
        fixed_costs = 29e6 #taken from BVG for a 1000 MW farm. Operations costs are fixed

        #variable_insurance = 8.2e6*farm_capex_norm*(N_T/100) #number of turbine also normalized with BVG farm

        #maintenance and service
        # assuming 1/3rd of turbine maintenance and service is inspection that scales with hub height,
        # and the rest is replacement (which scales with rna capex)
        #bop maintenance and service scales with bop costs

        variable_turbine_inspection = 13e6*(hub_height/116.0)*(N_T/100)
        variable_turbine_repair = 26e6*(rna_capex*N_T/5.17024743e+08)

        variable_bop = 21e6*(bop_costs/9.50483076e+08)

        costs_om = (fixed_costs + variable_turbine_inspection + variable_turbine_repair + variable_bop)

        #costs_om = 1.32232705e+08 # if O&M is assumed to be fix

        print('O&M costs:', costs_om)
        print('O&M costs/MW', costs_om/(N_T*P_rated))
        return costs_om, availability

class OM_model2(ExplicitComponent):
    '''
    This class scales the BVG O&M costs for a given farm based on the cost splits
    (Offshore Wind Innovation Hub Floating wind (major repair strategies)
    (Carroll et. al. on Failure rates)
    '''

    def setup(self):

        self.add_input('RNA_costs', val=0.0)
        self.add_input('cable_costs',val=0.0)
        self.add_input('P_rated', val=0.0)
        #self.add_input('hub_height', val=0.0)
        self.add_input('N_T', val=0.0)

        self.add_output('annual_cost_O&M', val=0.0)
        self.add_output('availability', val=0.0)



    def compute(self, inputs, outputs):

        rna_costs = inputs['RNA_costs']
        N_T = inputs['N_T']
        cable_costs = inputs['cable_costs']

        def oandm():

            ref_rna_costs = 5.531374e+08 #BVG turbine (10 MW - 180 m rotor)
            ref_cable_costs = 274068947 #BVG turbine (10 MW - 180 m rotor; 100 turbines with 7D spacing)
            pound_to_euro = 1.17 #to convert BVG estimates to euros

            fixed_costs = 25e6 #insurance, logistics, training, survey, etc.

            turbine_inspection = 0.25*33e6 #blade and tower inspection
            turbine_repairs = 0.75*33e6 #minor and major repairs and replacements

            turbine_repairs_fixed = 0.65*turbine_repairs*(N_T/100) #cost of (de) mobilization, transit, vessel, etc. dependent on n_t (Same failure rates)
            turbine_repairs_variable = 0.35*turbine_repairs*(rna_costs*N_T/ref_rna_costs)
            updated_turbine_repairs = turbine_repairs_fixed + turbine_repairs_variable

            bos_inspection = 0.5*18e6 #foundation inspection, scour monitoring, cable and substation inspection
            bos_repairs = 0.5*18e6 #repairing of export and inter-array cables

            bos_repairs_fixed = 0.65*bos_repairs*(N_T/100) #vessels and equipment to access the cable
            bos_repairs_variable = 0.35*bos_repairs*(cable_costs/ref_cable_costs) #cost of repairing/replacing the cables
            updated_bos_repairs = bos_repairs_fixed + bos_repairs_variable

            costs_om = (fixed_costs + turbine_inspection + updated_turbine_repairs + bos_inspection + updated_bos_repairs)*pound_to_euro
            availability = 0.97 #for the same farm

            return costs_om, availability

        [costs_om, availability] = oandm()

        #print('O&M', costs_om)

        field_names = ['O&M Costs']
        data = {field_names[0]: costs_om}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value])
        csvfile.close()

        outputs['annual_cost_O&M'] = costs_om
        outputs['availability'] = availability