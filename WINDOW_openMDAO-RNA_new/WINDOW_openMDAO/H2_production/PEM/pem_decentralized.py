from WINDOW_openMDAO.src.AbsH2.pem import AbsPemDecentralized
from WINDOW_openMDAO.H2_production.efficiency import pemdecentralized_efficiency
import csv

class PEM_DECENTRALIZED(AbsPemDecentralized):

    '''
    Returns the annual hydrogen production along with its costs
    '''

    def compute(self, inputs, outputs):

        electrolyser_ratio = self.options['electrolyser_ratio']


        N_T = inputs['N_T']
        P_rated = inputs['P_rated'] #in kW
        farm_power = inputs['farm_power'] #in MW


        electrolyser_rated = P_rated * electrolyser_ratio  # Electrolyser rated power per turbine in kW

        ### Compressor shaft power (Based on shaft power equation from ADAM CHRISTENSEN, International Council on Clean Transportation) ###

        Q = electrolyser_rated*24/57 #maximum H2 flow rate in terms of kg/day. Assuming turbine operates at rated power for 24 hours & 57 kWh/kg electrolyzer consumption
        p_out = 80 #output pressure  Hugo suggests 40-150 bar but most references mention 30-80 bar
        p_in = 30 #input pressure  (https://north-sea-energy.eu/static/7ffd23ec69b9d82a7a982b828be04c50/FINAL-NSE3-D3.1-Final-report-technical-assessment-of-Hydrogen-transport-compression-processing-offshore.pdf)

        P_rated_compressor = (Q*(1/24/3600)*(1.03198*310.95*8.314)*2/(0.00215*0.75*0.4)*((p_out/p_in)**(0.4/2)-1))/1000 #Compressor rated power in kW

        [H2_produced, annual_H2, power_curtailed] = self.production(electrolyser_rated, farm_power, N_T, P_rated_compressor)
        C_stacks, CAPEX = self.CAPEX(electrolyser_rated, P_rated_compressor, N_T)
        OPEX = self.OPEX(CAPEX)



        field_names = ['cost_total_h2system','cost_oandm_h2system', 'annual_h2']
        description =['CAPEX of the H2 system', 'OPEX of the H2 system', 'Annual H2 produced']
        data = {field_names[0]: [CAPEX[0],description[0]], field_names[1]:[OPEX[0], description[1]], field_names[2]:[annual_H2[0], description[2]]}
        # data = {field_names[0]: [CAPEX[0], description[0]], field_names[1]: [OPEX[0], description[1]], field_names[2]: [annual_H2, description[2]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()


        #print 'energy curtailed:', sum(power_curtailed)

        outputs['annual_H2'] = annual_H2
        outputs['C_stacks'] = C_stacks
        outputs['H2_CAPEX'] = CAPEX
        outputs['H2_OPEX'] = OPEX
        outputs['H2_produced'] = H2_produced
        outputs['power_curtailed'] = power_curtailed





    def production(self,electrolyser_rated, farm_power, N_T, P_rated_compressor):

        #### Standard specifications of a PEM Electrolyser ###

        H2 = []
        power_curtailed = []

        for idx in range(len(farm_power)):

            turbine_power = farm_power[idx]*1000/N_T #Average hourly power per turbine in kW

            '''Energy required for desalination is negligible (3.5-7kWh/1000L of seawater: https://hydrogentechworld.com/water-treatment-for-green-hydrogen-what-you-need-to-know)
                '''
            #energy_compression = P_rated_compressor/(electrolyser_rated/65)  #Energy consumed by compressor in kWh/kg calculated at rated conditions
            # P_op_compressor = P_rated_compressor*(turbine_power/electrolyser_rated) #operating power of compressor
            # P_input = turbine_power-P_op_compressor
            P_input = turbine_power #efficiency curve correced to account for all losses (including compression)
            input_load = max(0, min(100, (P_input/electrolyser_rated) * 100.0))

            # E_consumption_kg = pemdecentralized_efficiency(input_load, 'constant')
            # E_consumption_kg_rated = pemdecentralized_efficiency(100, 'constant')

            E_consumption_kg = pemdecentralized_efficiency(input_load, 'variable')
            E_consumption_kg_rated = pemdecentralized_efficiency(100, 'variable')


            if  P_input<electrolyser_rated:
                H2_produced = P_input/E_consumption_kg*N_T
                H2.append(H2_produced)
                power_curtailed.append(0)

            elif P_input>=electrolyser_rated:
                H2_produced = 0.75*electrolyser_rated/E_consumption_kg_rated * N_T + 0.25*P_input/E_consumption_kg*N_T  #can operate at overload for about 15 mins (15/60 hour) and then back to rated for cooling reasons
                #H2_produced = electrolyser_rated/E_consumption_kg*N_T
                H2.append(H2_produced)
                power_curtailed.append((P_input-(0.75*electrolyser_rated + 0.25*P_input))*N_T)

        annual_H2 = sum(H2) #Total hydrogen (in kg) produced in a year

        # print(annual_H2)
        # import pandas as pd
        # df = pd.DataFrame(farm_power)
        # filename = 'farm_power_16_240.csv'
        # # filename = 'farm_power_' + str(round(power[0],2)) + '_' + str(round(rotor_diameter[0],1)) + '_' + str(n_t)  +  '.csv'
        # df.to_csv(filename)
        #
        # df = pd.DataFrame(H2)
        # filename = 'H2_variable_16_240.csv'
        # # filename = 'farm_power_' + str(round(power[0],2)) + '_' + str(round(rotor_diameter[0],1)) + '_' + str(n_t)  +  '.csv'
        # df.to_csv(filename)

        return H2, annual_H2, power_curtailed


    def CAPEX(self, electrolyser_rated,P_rated_compressor, N_T):

        ### Reference costs in dollars per kW ###

        ### Open data estimates ###

        # ref_stacks = 100 #Electrolyser stacks  NREL(https://www.nrel.gov/docs/fy19osti/72740.pdf)
        # ref_bop = 200 #BOP includes deionization, gas separators, gas treatment

        ref_stacks = 400 #IRENA 2020 and also close to ISPT 1GW facility report
        ref_bop = 200 #BOP includes deionization, gas separators, gas treatment. Based on NREL report, ISPT, lower end of IRENA


        water_consumption = (electrolyser_rated/63)*11 #L/h at rated conditions assuming 11 L/kg H2
        ref_desalination = 60000*(water_consumption/2000)  # 60000 euros for a 2000L/h capacity (North Sea Energy deliverable 3.6 page 13)


        C_stacks = ref_stacks*electrolyser_rated*N_T
        C_bop = ref_bop*electrolyser_rated*N_T
        C_compressor = P_rated_compressor*2545*N_T  #Multiplied with cost/kW of compressor from National research council and total number of turbines.
        C_desalination = ref_desalination*N_T
        C_backup = 10e6 #Cost of battery backup. Around 5% of farm power and cost of 150 USD/kWh

        #C_indirect = 0.8 #NREL report page 36 and ISPT 1GW report. Includes installation, margin, indirect costs,  etc.
        C_indirect = 0.6 #NREL report page 36 and ISPT 1GW report. Includes profit margin, indirect costs, contingency etc. Reduced as installation can be performed with the turbine itself

        usd_to_euro = 0.88
        C_total = (usd_to_euro*(C_stacks + C_bop + C_compressor + C_backup) + C_desalination)*(1+C_indirect)
        CAPEX = C_total

        return C_stacks, CAPEX

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






