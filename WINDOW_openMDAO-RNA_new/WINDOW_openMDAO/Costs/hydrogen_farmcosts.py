from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.input_params import max_n_turbines, distance_to_harbour
from .costs.other_costs import other_costs
import numpy as np
from WINDOW_openMDAO.input_params import distance_to_grid
import csv

class HydrogenFarmCostModel(ExplicitComponent):

    def initialize(self):
        self.options.declare('electrolyser_ratio', desc='Ratio of electroylser rated power to turbine rated power')

    def setup(self):
        self.add_input('n_substations', val=0)
        self.add_input('n_turbines', val=0)
        self.add_input('length_p_cable_type', shape=3)
        self.add_input('cost_p_cable_type', shape=3)
        self.add_input('support_structure_costs', shape=max_n_turbines)
        self.add_input('support_decomm_costs', shape=max_n_turbines)
        self.add_input('depth_central_platform', val=0.0)
        self.add_input('machine_rating', units='W', desc='machine rating', val=10e6)
        self.add_input('rotor_radius', units='m', desc='rotor radius', val=95.4)
        self.add_input('hub_height', units='m', desc='hub height', val=119.0)
        self.add_input('purchase_price', desc='turbine cost in EUR', val=10000000.0)
        self.add_input('warranty_percentage', desc='insurance of the turbines % to its cost price', val=15)
        self.add_input('rna_mass', units='kg', desc='mass of RNA', val=589211.0)
        self.add_input('generator_voltage', units='V', desc='voltage at generator', val=4000.0)
        self.add_input('collection_voltage', units='V', desc='voltage at substation', val=66000.0)
        self.add_input('cost_tower', shape=max_n_turbines)
        self.add_input('farm_area', desc='area of the wind farm in km2')
        self.add_input('annual_h2', desc='annual hydrogen output in kg')
        self.add_input('H2_CAPEX', desc='costs of the elctrolyzer system')


        self.add_output('investment_costs_h2', val=0.0)
        self.add_output('decommissioning_costs_h2', val=0.0)
        self.add_output('bop_costs_h2', val=0.0)
        self.add_output('pipeline_costs_h2', val=0.0)

        # self.declare_partals(of=['investment_costs', 'decommissioning_costs'], wrt=['n_substations', 'n_turbines', 'length_p_cable_type', 'cost_p_cable_type', 'support_structure_costs', 'depth_central_platform'], method='fd')

    def compute(self, inputs, outputs):
        n_substations = inputs['n_substations']
        n_turbines = inputs['n_turbines']
        machine_rating = inputs['machine_rating']
        length_p_cable_type = inputs['length_p_cable_type']
        cost_p_cable_type = inputs['cost_p_cable_type']
        support_structure_costs = inputs['support_structure_costs']  # this includes tower costs
        support_decomm_costs = inputs['support_decomm_costs']
        depth_central_platform = inputs['depth_central_platform']
        cost_tower = inputs['cost_tower']
        annual_h2 = inputs['annual_h2']
        H2_CAPEX = inputs['H2_CAPEX']

        electrolyser_ratio = self.options['electrolyser_ratio']

        a = 5*1e5  # the cost in euros/km2 that the developer pays for using ocean area [Hypothetical cost]
        farm_area = inputs['farm_area'] # in km2
        area_use_cost = a*farm_area


        infield_cable_length = sum(length_p_cable_type)

        #print('Infield length', infield_cable_length)



        def pipeline_costs(infield_cable_length , distance_to_grid, machine_rating, electrolyser_ratio, n_turbines):
            total_pipeline_length = infield_cable_length + distance_to_grid  # in m
            # length_infield_pipeline = infield_cable_length
            length_export_pipeline = distance_to_grid
            #pipeline_costfactor = 1.25  # per kW per km (HYGRO estiamtes that matches well with the white paper from Umlat that state roughly 1 euro/kg of H2)

            export_pipeline_costfactor = 0.01 #Euros/kg (Matches HYGRO HKW estimates and also the 2020 European hydrogen backbone paper)
            pipeline_lifetime = 40
            #export_pipeline_cost = export_pipeline_costfactor*annual_h2*pipeline_lifetime*(distance_to_grid/1000/60) #Original cost factor of 0.2 euros/kg was adjusted for 60 km length


            ''' Different infield pipeline layout compared to cabling layout. Straight feeders running along the column of turbines. 
            Total length mainly depends on the number of columns of turbines. N_T decides number of turbines per column/feeder'''

            p = machine_rating/1000 #in MW

            ## for a wind farm capacity of 800 MW ##
            # power = [10.0, 11.11, 12.12, 12.5, 13.11, 13.56, 14.04, 14.55, 15.09, 16.0, 17.02, 18.18, 19.05, 20.0, 22.22]
            # n_t_feeder = [9,8,8,8,8,8,8,7,7,7,7,7,7,6,6]
            # pipeline_length = [136, 132, 127, 124, 117, 116, 115, 122, 117, 111, 106, 100, 111, 106, 98] #in km

            ## for a wind farm capacity of 1000 MW ##
            power = [10.0, 10.99, 12.05, 12.99, 13.51, 14.08, 14.49, 14.93, 15.62, 16.13, 16.67, 17.24, 18.18, 19.23, 20.0, 22.73]
            n_t_feeder = [10, 10, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7]
            pipeline_length = [150, 137, 139, 131, 126, 135, 131, 128, 124, 120, 117, 113, 122, 115, 111, 100] #in km

            ## for a wind farm capacity of 1200 MW ##
            # power = [10.0, 11.01, 12.0, 13.04, 14.12, 15.0, 15.58, 16.0, 16.67, 17.14, 17.65, 18.18, 18.46, 19.05, 20.0, 22.22]
            # n_t_feeder = [11,10,10,10,9,9,9,9,8,8,8,8,8,8,8,7]
            # pipeline_length = [163,162,150,137,138,136,131,127,132,134,129,127,126,122,117,121] #in km



            arr = np.asarray(power)
            idx = (np.abs(arr - p)).argmin()
            N = n_t_feeder[idx]
            length_infield_pipeline = pipeline_length[idx]*1000



            '''Pipeline cost factors from Markus et al. titled 'Modeling hydrogen networks for future energy systems: A comparison of linear and nonlinear approaches'
            & UC Davis NG pipeline costs from 2004 & Mischner et al. 2013
            Thermodynamic and Technical Issues of Hydrogen and Methane-Hydrogen Mixtures Pipeline Transmission shows pipeline diameter for different flow rates and pressure (D is proportional to M^0.4)
            '''

            if electrolyser_ratio<1:
                flow_rate_infield = machine_rating*electrolyser_ratio * N / 63 / 3600  # calculating mass flow rate at rated power for N turbines in a string. 63 kWh/kg consumption @above rated
                flow_rate_export = machine_rating*electrolyser_ratio * n_turbines/ 63 / 3600
            else:
                flow_rate_infield = machine_rating * N / 57 / 3600  # calculating mass flow rate at rated power for N turbines in a string. 57 kWh/kg consumption @rated power
                flow_rate_export = machine_rating * n_turbines / 57 / 3600

            ref_flow_rate = 0.3 #kg/s
            ref_dia = 90 #mm for a flow rate of 0.3 kg/s close to 80 bar


            dia_infield = ref_dia*(flow_rate_infield /ref_flow_rate)**0.4
            cost_factor_infield = (0.0006*dia_infield**2 + 0.418*dia_infield + 295.62)*1.05 # in Eur/m; data from Markus et al.
            cost_infield_pipeline = cost_factor_infield*1000 * (length_infield_pipeline / 1000)

            dia_export = ref_dia*(flow_rate_export /ref_flow_rate)**0.4
            cost_factor_export= (0.0006*dia_export**2 + 0.418*dia_export + 295.62)*1.05 # in Eur/m; data from Markus et al.
            cost_export_pipeline = cost_factor_export*1000 * (distance_to_grid/1000)  #Export pipeline costs should remain constant for all designs.



            pipeline_cost = cost_infield_pipeline + cost_export_pipeline

            #pipeline_installation_cost_perkm = 1e6  # Euros/km (back calculated from BVG for total length of infield (195km) + export (60km)
            #pipeline_installation_cost = pipeline_installation_cost_perkm * (total_pipeline_length / 1000.0)


            '''Installation costs same as cable installation'''
            # day rates back calculated from BVG burial costs
            installation_rate_infield_pipeline = 0.1  # km/hr for simulatenous lay and burial
            installation_rate_export_pipeline = 0.1  # km/hr for simulatenous lay and burial. Higher for export cable due to lower number of connections to be made
            clv_dayrate = 110000  # cable laying vessel
            cbv_dayrate = 140000  # cable burial vessel
            mobilization_clv = 550000
            mobilization_cbv = 550000

            days_export_pipeline = (length_export_pipeline/1000)/installation_rate_export_pipeline / 24
            days_infield_pipeline = (length_infield_pipeline/1000) /installation_rate_infield_pipeline/ 24

            cost_installation_infield_pipeline = days_infield_pipeline * (clv_dayrate + cbv_dayrate) * 1.5  # for weather delays
            cost_installation_export_pipeline = days_export_pipeline * (clv_dayrate + cbv_dayrate) * 1.5  # for weather delays

            #extra_costs = 20e6  # for cable pull-in, electrical testing and termination, onshore connection

            cost_installation_pipeline = cost_installation_infield_pipeline + cost_installation_export_pipeline + mobilization_cbv * 2 + mobilization_clv * 2  # 1.5 to account for survey, clearance of seabed, etc.

            # cost_perkm_pipeline_installation_infield = 0.45e6  # Euros/km for 150mm pipeline (Outlook for Dutch hydrogen market)
            # cost_perkm_pipeline_installation_export = 0.7e6  # Euros/km for 350 mm pipeline (Outlook for Dutch hydrogen market)
            # cost_installation_pipeline = cost_perkm_pipeline_installation_infield*(length_infield_pipeline/1000) + cost_perkm_pipeline_installation_export*(length_export_pipeline/1000)
            #

            return cost_infield_pipeline, cost_export_pipeline, cost_installation_pipeline

        [infield_pipeline_cost, export_pipeline_cost, pipeline_installation_costs] = pipeline_costs(infield_cable_length, distance_to_grid, machine_rating, electrolyser_ratio, n_turbines)
        pipeline_costs = infield_pipeline_cost + export_pipeline_cost

        purchase_price_h2 = inputs['purchase_price'] - inputs['machine_rating'] * 40 * 0.88  # cost savings in RNA (converter, transformer, switch gears, etc.). 0.88 for USD to EUR

        turbine_CAPEX_h2 = purchase_price_h2 + cost_tower[0]
        export_cable_h2, electrical_costs_h2, other_investment_h2, decommissioning_costs_h2 = other_costs(depth_central_platform,
                                                                                         n_turbines,
                                                                                         sum(length_p_cable_type),
                                                                                         n_substations, distance_to_grid/1000, distance_to_harbour/1000,\
                                                                                         inputs['machine_rating'],
                                                                                         inputs['rotor_radius'],
                                                                                         purchase_price_h2,
                                                                                         inputs['warranty_percentage'], \
                                                                                         inputs['rna_mass'],
                                                                                         inputs['hub_height'],
                                                                                         inputs['generator_voltage'],
                                                                                         inputs['collection_voltage'],
                                                                                         turbine_CAPEX_h2, 2)



        support_structure_investment = sum(support_structure_costs)
        support_decomm_costs = sum(support_decomm_costs)

        farm_CAPEX_h2 = support_structure_investment + other_investment_h2 + pipeline_costs + pipeline_installation_costs + H2_CAPEX
        #print('other investment h2',  other_investment_h2)
        #print('pipeline costs', pipeline_costs)
        #print('pipeline installation', pipeline_installation_costs)

        #### project development and other farm costs based on BVG (https://guidetoanoffshorewindfarm.com/wind-farm-costs) and NREL (https://www.nrel.gov/docs/fy21osti/78471.pdf)
        total_farm_CAPEX = farm_CAPEX_h2 / 0.85  # The other 15 % comes from management, project dev, insurance, contingency, construction management, etc.
        project_dev_management = 0.05*total_farm_CAPEX
        other_farm_costs = 0.1*total_farm_CAPEX #insurance, contingency, construction project management



        outputs['bop_costs_h2'] = support_structure_investment + pipeline_costs - cost_tower[0] * n_turbines  # subtraction as support cost involves tower cost
        outputs['investment_costs_h2'] = total_farm_CAPEX
        outputs['decommissioning_costs_h2'] = decommissioning_costs_h2 + support_decomm_costs
        outputs['pipeline_costs_h2'] = pipeline_costs

        field_names = ['costs_turbine_without_other_H2', 'costs_infield_pipeline', 'costs_export_pipeline', 'costs_installation_pipeline',
                       'costs_bop_H2', 'costs_projectdev_H2', 'costs_farm_other_H2',
                       'costs_totalinvestment_H2', 'costs_decom_H2']
        description = ['Turbine CAPEX without other non-technical costs for hydrogen', 'Costs of infield pipeline for H2', 'Costs of export pipeline for H2','Costs of pipeline installation for H2', 'Balance of plant costs for H2', 'Project development and management costs for H2',
                         'Other farm costs (insurance, contingency, etc. for H2', 'Total farm CAPEX for H2', 'Decommissioning costs for H2']
        data = {field_names[0]: [turbine_CAPEX_h2[0], description[0]],
                field_names[1]: [infield_pipeline_cost[0], description[1]],
                field_names[2]: [export_pipeline_cost[0], description[2]],
                field_names[3]: [pipeline_installation_costs, description[3]],
                field_names[4]: [outputs['bop_costs_h2'][0], description[4]],
                field_names[5]: [project_dev_management[0], description[5]],
                field_names[6]: [other_farm_costs[0], description[6]],
                field_names[7]: [outputs['investment_costs_h2'][0], description[7]],
                field_names[8]: [outputs['decommissioning_costs_h2'][0], description[8]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()



        #print 'infield cable costs:', infield_cable_investment


        # print('Total investment costs H2:', outputs['investment_costs_h2'])
        # print('project dev and management H2', project_dev_management)
        # print('Other farm costs H2 (insurance, contingency)', other_farm_costs)
        # print('Decomissioning H2', outputs['decommissioning_costs_h2'])
        #print 'Rated power:', inputs['machine_rating']
        #print 'Turbine radius:', inputs['rotor_radius']




