from WINDOW_openMDAO.src.AbsH2.alkaline import AbsAlkaline
from WINDOW_openMDAO.H2_production.efficiency import alkaline_efficiency

class ALKALINE(AbsAlkaline):

    '''
    Returns the annual hydrogen production along with its costs
    '''

    def compute(self, inputs, outputs):

        electrolyser_ratio = self.metadata['electrolyser_ratio']


        N_T = inputs['N_T']
        P_rated = inputs['P_rated'] #in kW
        farm_power = inputs['farm_power'] #in MW
        transmission_eff = inputs['transmission_efficiency']

        P_rated = P_rated / 1000  # in MW

        farm_power = [P*transmission_eff for P in farm_power] #Multiplying farm power with elec cable efficiency

        farm_rated = N_T*P_rated    #Wind farm rated power in MW



        electrolyser_rated = farm_rated*electrolyser_ratio #Electrolyser rated power in MW



        [H2_produced, annual_H2, power_curtailed] = self.production(electrolyser_rated, farm_power)

        CAPEX = self.CAPEX(electrolyser_rated)

        OPEX = self.OPEX(CAPEX)

        print 'Annual H2:', annual_H2
        print 'H2 CAPEX:', CAPEX
        print 'H2 OPEX', OPEX




        print 'energy curtailed:', sum(power_curtailed)



        outputs['annual_H2'] = annual_H2
        outputs['H2_CAPEX'] = CAPEX
        outputs['H2_OPEX'] = OPEX
        outputs['H2_produced'] = H2_produced
        outputs['power_curtailed'] = power_curtailed






    def production(self,electrolyser_rated, farm_power):



        #### Standard specifications of an Alkaline Electrolyser ###

        base_load = 0 #Need to maintain it at a minimum of 15 % input load (Shut down otherwise)


        H2 = []
        power_curtailed = []

        for idx in range(len(farm_power)):



            input_load = min(100, (farm_power[idx]/electrolyser_rated)*100.0)

            E_consumption_kg = alkaline_efficiency(input_load, 'variable')

            if base_load>0:

                if farm_power[idx]<base_load*electrolyser_rated:
                    H2.append(0) #eletrolyser shut down
                    #power_curtailed.append(0) #for hydrogen only
                    power_curtailed.append(farm_power[idx]) #for both hydrogen and elec

                elif farm_power[idx]>base_load*electrolyser_rated and farm_power[idx]<electrolyser_rated:
                    H2_produced = farm_power[idx]*1000/E_consumption_kg
                    H2.append(H2_produced[0])
                    power_curtailed.append(0)
                elif farm_power[idx]>electrolyser_rated or farm_power[idx] == electrolyser_rated:
                    H2_produced = electrolyser_rated*1000/E_consumption_kg
                    H2.append(H2_produced[0])
                    power_curtailed.append(farm_power[idx]-electrolyser_rated)

            else:
                if  farm_power[idx]<electrolyser_rated:
                    H2_produced = farm_power[idx]*1000/E_consumption_kg
                    H2.append(H2_produced[0])
                    power_curtailed.append(0)
                elif farm_power[idx]>electrolyser_rated or farm_power[idx] == electrolyser_rated:
                    H2_produced = electrolyser_rated*1000/E_consumption_kg
                    H2.append(H2_produced[0])
                    #power_curtailed.append(farm_power[idx]-electrolyser_rated)
                    power_curtailed.append(0)






        annual_H2 = sum(H2) #Total hydrogen (in kg) produced in a year

        return H2, annual_H2, power_curtailed


    def CAPEX(self, electrolyser_rated):

        ### Reference costs in Euros per kW ###

        ref_stacks = 182 #Electrolyser stacks
        ref_bop = 205 #BOP includes gas separators, compressors, gas treatment
        ref_pe = 194 #Power electronics includes step down transformers and rectifiers
        ref_utilities =120 #Water plant, cooling towers, etc.
        ref_civil = 78

        #ref_indirect = 210 #engineering, project management, commissioning
        #ref_owner = 88 #Site supervisory teams, insurance, land lease
        #ref_contingency = 0.3 #30 % extra for future risks

        ref_indirect = 0 #0.2 # 20 % extra  for engineering, project management, commissioning, Site supervisory teams, insurance, land lease, contingency

        electrolyser_rated = electrolyser_rated*1000 #Converting to kW

        C_stacks = ref_stacks*electrolyser_rated
        C_bop = ref_bop*electrolyser_rated
        C_pe = ref_pe*electrolyser_rated
        C_utilities = ref_utilities*electrolyser_rated
        C_civil = ref_civil*electrolyser_rated

        C_indirect = ref_indirect*electrolyser_rated
        #C_owner = ref_owner*electrolyser_rated

        C_total = C_stacks + C_bop + C_pe + C_utilities + C_civil # + C_indirect + C_owner
        C_indirect = ref_indirect*C_total

        #C_contingency = ref_contingency*C_total
        CAPEX = C_total + C_indirect

        #CAPEX = C_total + C_contingency

        return CAPEX

    def OPEX(self, CAPEX):

        OPEX = 0.02*CAPEX

        return OPEX


#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":

    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'N_T': 100.0, \
              'P_rated': 10000.0, \
              'farm_power': [1000, 20, 400, 160], \
              'transmission_efficiency': 0.95}
    outputs = {}

    model = ALKALINE(electrolyser_ratio = 0.5, time_resolution = 4)


    model.compute(inputs, outputs)

    #print outputs['annual_H2']
    #print outputs['H2_CAPEX']
    #print outputs['H2_OPEX']






