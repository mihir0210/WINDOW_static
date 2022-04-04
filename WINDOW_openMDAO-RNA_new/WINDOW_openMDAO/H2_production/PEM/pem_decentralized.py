from WINDOW_openMDAO.src.AbsH2.pem import AbsPemDecentralized
from WINDOW_openMDAO.H2_production.efficiency import pemdecentralized_efficiency


class PEM_DECENTRALIZED(AbsPemDecentralized):

    '''
    Returns the annual hydrogen production along with its costs
    '''

    def compute(self, inputs, outputs):

        #electrolyser_ratio = self.metadata['electrolyser_ratio']


        N_T = inputs['N_T']
        P_rated = inputs['P_rated'] #in kW
        farm_power = inputs['farm_power'] #in MW
        #transmission_eff = inputs['transmission_efficiency']

        P_rated = P_rated / 1000  # in MW

        #farm_power = [P*transmission_eff for P in farm_power] #Multiplying farm power with elec cable efficiency

        farm_rated = N_T*P_rated    #Wind farm rated power in MW

        #electrolyser_rated = farm_rated*electrolyser_ratio #Electrolyser rated power in MW
        sizing_ratio = 1
        electrolyser_rated = farm_rated*sizing_ratio  # Electrolyser rated power in MW
        stack_size = 2.5 #2.5 #MW; Can also choose 10 MW

        [H2_produced, annual_H2, power_curtailed] = self.production(electrolyser_rated, farm_power, stack_size)



        CAPEX = self.CAPEX(electrolyser_rated, annual_H2, stack_size)

        OPEX = self.OPEX(CAPEX)

        print 'Annual H2:', annual_H2
        print 'H2 CAPEX:', CAPEX
        print 'H2 OPEX', OPEX

        #print 'energy curtailed:', sum(power_curtailed)

        outputs['annual_H2'] = annual_H2
        outputs['H2_CAPEX'] = CAPEX
        outputs['H2_OPEX'] = OPEX
        outputs['H2_produced'] = H2_produced
        outputs['power_curtailed'] = power_curtailed






    def production(self,electrolyser_rated, farm_power, stack_size):


        print 'Electrolyzer rated', electrolyser_rated
        #### Standard specifications of a PEM Electrolyser ###

        H2 = []
        power_curtailed = []
        compression_eff = 0.97 # 3% losses to compress from 30 bar to 100 bar (IRENA)

        for idx in range(len(farm_power)):

            input_load = max(0,min(100, (farm_power[idx]*compression_eff/electrolyser_rated)*100.0))

            E_consumption_kg = pemdecentralized_efficiency(input_load, 'variable', stack_size)

            #print 'farm power ', farm_power[idx]
            #print 'Energy consumed', E_consumption_kg

            # if farm_power[idx]<base_load*electrolyser_rated:
            #     H2.append(0) #eletrolyser shut down
            #     power_curtailed.append(0) #for hydrogen only
            #     #power_curtailed.append(farm_power[idx]) #for both hydrogen and elec
            #     c1 = c1+1

            if  farm_power[idx]<electrolyser_rated:
                H2_produced = farm_power[idx]*1000/E_consumption_kg
                H2.append(H2_produced)
                power_curtailed.append(0)

            elif farm_power[idx]>electrolyser_rated or farm_power[idx] == electrolyser_rated:
                H2_produced = electrolyser_rated*1000/E_consumption_kg
                H2.append(H2_produced)
                power_curtailed.append(0)
                #power_curtailed.append(farm_power[idx]-electrolyser_rated)

            #elec_comp = ((286.76*H2_produced*285.15/100)/(0.5*0.0696*3.6e9))*(1.41/0.41)*((70/30)**(0.41/1.41) - 1)

            #print elec_comp


        annual_H2 = sum(H2) #Total hydrogen (in kg) produced in a year


        return H2, annual_H2, power_curtailed


    def CAPEX(self, electrolyser_rated, annual_H2, stack_size):

        ### Reference costs in dollars per kW ###


        ### Open data estimates ###

        ref_stacks = 100 #Electrolyser stacks  NREL(https://www.nrel.gov/docs/fy19osti/72740.pdf) and IRENA
        ref_bop = 200 #BOP includes power supply, deionization, gas separators, compressors, gas treatment

        #ref_compressor = 50 #IRENA page 39

        electrolyser_rated = electrolyser_rated*1000 #Converting to kW

        C_stacks = ref_stacks*electrolyser_rated
        C_bop = ref_bop*electrolyser_rated

        ### Compressor costs can be expressed in $/kg of hydrogen produced

        ref_compressor = 0.05 #$/kg (HYGRO HKW estimates, IRENA, ADAM CHRISTENSEN, International Council on Clean Transportation)

        C_compressor = ref_compressor*annual_H2

        C_indirect = 0.5 #NREL report. Includes installation, margin, indirect costs, etc.

        usd_to_euro = 0.88
        C_total = (C_stacks + C_bop + C_compressor)*(1+C_indirect)*usd_to_euro

        if stack_size==2.5:
            CAPEX = C_total
        elif stack_size==10:
            CAPEX = C_total*0.8 #20 % cost reduction based on IRENA figure 26

        return CAPEX

    def OPEX(self, CAPEX):

        OPEX = 0.02*CAPEX #icct2020 says 1-3%

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

    model = PEM_DECENTRALIZED(time_resolution = 4)


    model.compute(inputs, outputs)

    #print outputs['annual_H2']
    #print outputs['H2_CAPEX']
    #print outputs['H2_OPEX']
    #print outputs['H2_produced']






