from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.input_params import max_n_turbines, distance_to_grid, distance_to_harbour
from .costs.other_costs import other_costs
import csv

from WINDOW_openMDAO.input_params import distance_to_grid


class TeamPlayCostModel(ExplicitComponent):

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
        
        self.add_output('investment_costs', val=0.0)
        self.add_output('decommissioning_costs', val=0.0)
        self.add_output('bop_costs', val=0.0)
        self.add_output('cable_costs', val=0.0)
        self.add_output('array_cable_costs', val=0.0)





        #self.declare_partals(of=['investment_costs', 'decommissioning_costs'], wrt=['n_substations', 'n_turbines', 'length_p_cable_type', 'cost_p_cable_type', 'support_structure_costs', 'depth_central_platform'], method='fd')

    def compute(self, inputs, outputs):
        n_substations = inputs['n_substations']
        n_turbines = inputs['n_turbines']
        length_p_cable_type = inputs['length_p_cable_type']
        cost_p_cable_type = inputs['cost_p_cable_type']
        support_structure_costs = inputs['support_structure_costs'] #this includes tower costs
        support_decomm_costs = inputs['support_decomm_costs']
        depth_central_platform = inputs['depth_central_platform']
        cost_tower = inputs['cost_tower']

        a = 5*1e5  # the cost in euros/km2 that the developer pays for using ocean area [Hypothetical cost]
        farm_area = inputs['farm_area'] # in km2
        area_use_cost = a*farm_area

        turbine_CAPEX = inputs['purchase_price'] + cost_tower[0] #RNA + tower cost for one turbine

        export_cable_costs, electrical_costs, other_investment, decommissioning_costs = other_costs(depth_central_platform, n_turbines, sum(length_p_cable_type), n_substations, distance_to_grid/1000, distance_to_harbour/1000, \
                                                                         inputs['machine_rating'], inputs['rotor_radius'], inputs['purchase_price'], inputs['warranty_percentage'], \
                                                                         inputs['rna_mass'], inputs['hub_height'], inputs['generator_voltage'], inputs['collection_voltage'], turbine_CAPEX, 1)

        infield_cable_investment = sum(cost_p_cable_type)
        support_structure_investment = sum(support_structure_costs)
        support_decomm_costs = sum(support_decomm_costs)

        farm_CAPEX = support_structure_investment + infield_cable_investment + other_investment

        #### project development and other farm costs based on BVG (https://guidetoanoffshorewindfarm.com/wind-farm-costs) and NREL (https://www.nrel.gov/docs/fy21osti/78471.pdf)
        total_farm_CAPEX = farm_CAPEX / 0.85  # The other 15 % comes from management, project dev, insurance, contingency, construction management, etc.
        project_dev_management = 0.05*total_farm_CAPEX
        other_farm_costs = 0.1*total_farm_CAPEX #insurance, contingency, construction project management


        outputs['bop_costs'] = support_structure_investment + infield_cable_investment + electrical_costs - cost_tower[0] * n_turbines  # subtraction as support cost involves tower cost
        outputs['investment_costs'] = total_farm_CAPEX # + area_use_cost
        outputs['decommissioning_costs'] = decommissioning_costs + support_decomm_costs
        outputs['cable_costs'] = export_cable_costs + infield_cable_investment
        outputs['array_cable_costs'] = infield_cable_investment


        # print 'Rated power:', inputs['machine_rating']
        # print 'Turbine radius:', inputs['rotor_radius']
        # print 'turbine CAPEX without other costs', turbine_CAPEX
        # print 'infield cable length', sum(length_p_cable_type)
        # print 'infield cable cost:', infield_cable_investment
        # print 'bop_costs', outputs['bop_costs']
        # print 'project dev and management', project_dev_management
        # print 'Other farm costs (insurance, contingency)', other_farm_costs
        # print 'Total investment costs electricity:', outputs['investment_costs']
        # print 'Decomissioning costs', decommissioning_costs + support_decomm_costs

        field_names = ['infield_length', 'costs_turbine_without_other_elec', 'costs_infield_cable',
                       'costs_bop_elec', 'costs_projectdev_elec', 'costs_farm_other_elec',
                       'costs_totalinvestment_elec:', 'costs_decom_elec']
        description = ['Infield array length', 'Turbine CAPEX without other non-technical costs for electricity', 'Costs of infield array for electricity', 'Balance of plant costs for elecricity', 'Project development and management costs for electricity',
                         'Other farm costs (insurance, contingency, etc. for electricity', 'Total farm CAPEX for electricity', 'Decommissioning costs for electricity']
        data = {field_names[0]: [sum(length_p_cable_type), description[0]],
                field_names[1]: [turbine_CAPEX[0],description[1]],
                field_names[2]: [infield_cable_investment,description[2]],
                field_names[3]: [outputs['bop_costs'][0],description[3]],
                field_names[4]: [project_dev_management[0],description[4]],
                field_names[5]: [other_farm_costs[0],description[5]],
                field_names[6]: [outputs['investment_costs'][0],description[6]],
                field_names[7]: [outputs['decommissioning_costs'][0], description[7]],}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()






        # print 'farm CAPEX', farm_CAPEX
        #
        # other_installation_commissioning_costs = 2.48e8*(farm_CAPEX/2.51449632e+09)
        #
        # print 'other installation commission', other_installation_commissioning_costs





