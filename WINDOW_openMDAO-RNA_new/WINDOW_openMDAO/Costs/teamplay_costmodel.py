from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.input_params import max_n_turbines
from costs.other_costs import other_costs

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
        self.add_output('investment_costs_h2', val=0.0)
        self.add_output('decommissioning_costs', val=0.0)
        self.add_output('decommissioning_costs_h2', val=0.0)

        self.add_output('bop_costs', val=0.0)
        self.add_output('bop_costs_h2', val=0.0)




        #self.declare_partals(of=['investment_costs', 'decommissioning_costs'], wrt=['n_substations', 'n_turbines', 'length_p_cable_type', 'cost_p_cable_type', 'support_structure_costs', 'depth_central_platform'], method='fd')

    def compute(self, inputs, outputs):
        n_substations = inputs['n_substations']
        n_turbines = inputs['n_turbines']
        length_p_cable_type = inputs['length_p_cable_type']
        cost_p_cable_type = inputs['cost_p_cable_type']
        support_structure_costs = inputs['support_structure_costs']
        support_decomm_costs = inputs['support_decomm_costs']
        depth_central_platform = inputs['depth_central_platform']
        cost_tower = inputs['cost_tower']

        turbine_CAPEX = inputs['purchase_price'] + cost_tower[0]

        #print 'turbine capex', turbine_CAPEX

        electrical_costs, other_investment, decommissioning_costs = other_costs(depth_central_platform, n_turbines, sum(length_p_cable_type), n_substations, \
                                                                         inputs['machine_rating'], inputs['rotor_radius'], inputs['purchase_price'], inputs['warranty_percentage'], \
                                                                         inputs['rna_mass'], inputs['hub_height'], inputs['generator_voltage'], inputs['collection_voltage'], turbine_CAPEX, 1)
        # other_investment = 0.0
        infield_cable_investment = sum(cost_p_cable_type)
        # infield_cable_investment = 7973617.59755
        support_structure_investment = sum(support_structure_costs)
        support_decomm_costs = sum(support_decomm_costs)

        outputs['bop_costs'] = support_structure_investment + infield_cable_investment + electrical_costs
        print 'bop_costs', outputs['bop_costs']
        outputs['decommissioning_costs'] = decommissioning_costs + support_decomm_costs
        # support_structure_investment = 91955760.7762

        a = 5*1e5  # the cost in euros/km2 that the developer pays for using ocean area [Hypothetical cost]
        farm_area = inputs['farm_area'] # in km2
        area_use_cost = a*farm_area

        #print 'Farm area and area use cost', farm_area, area_use_cost

        #print 'infield cable cost:', infield_cable_investment
        farm_CAPEX = support_structure_investment + infield_cable_investment + other_investment
        #print 'farm CAPEX', farm_CAPEX

        other_installation_commissioning_costs = 2.48e8*(farm_CAPEX/2.6490261e+09)

        print 'other installation commission', other_installation_commissioning_costs


        outputs['investment_costs'] = support_structure_investment + infield_cable_investment + other_investment + other_installation_commissioning_costs#+ area_use_cost  # TODO Apply management percentage also to electrical and support structure costs.
        # print support_structure_investment ,infield_cable_investment ,other_investment, outputs['decommissioning_costs']

        def pem_decentralized_costs():
            total_pipeline_length = distance_to_grid  # in m
            pipeline_costfactor = 1.25  # per kW per km

            pipeline_cost = pipeline_costfactor * n_turbines * inputs['machine_rating'] * (
                        total_pipeline_length / 1000.0) #+ 40e6


            pipeline_installation_cost_perkm = 4e6  # Euros

            pipeline_installation_cost = pipeline_installation_cost_perkm * (total_pipeline_length / 1000.0)

            print 'pipeline costs', pipeline_cost
            print 'pipeline installation costs', pipeline_installation_cost

            return pipeline_cost, pipeline_installation_cost

        [pipeline_costs, pipeline_installation_costs] = pem_decentralized_costs()

        purchase_price_h2 = inputs['purchase_price'] - inputs['machine_rating']*40*0.88 # cost savings in RNA (converter, transformer, switch gears, etc.). 0.88 for USD to EUR

        turbine_CAPEX_h2 = purchase_price_h2 + cost_tower[0]
        electrical_costs_h2, other_investment_h2, decommissioning_costs_h2 = other_costs(depth_central_platform, n_turbines, sum(length_p_cable_type), n_substations, \
                                                                         inputs['machine_rating'], inputs['rotor_radius'], purchase_price_h2, inputs['warranty_percentage'], \
                                                                         inputs['rna_mass'], inputs['hub_height'], inputs['generator_voltage'], inputs['collection_voltage'], turbine_CAPEX_h2, 2)

        farm_CAPEX_h2 = support_structure_investment + infield_cable_investment + other_investment_h2 + pipeline_costs + pipeline_installation_costs
        #print 'farm CAPEX h2', farm_CAPEX_h2

        other_installation_commissioning_costs_h2 = 2.48e8*(farm_CAPEX_h2/2.21978122e+09)

        print 'other installation commission h2', other_installation_commissioning_costs_h2

        outputs['bop_costs_h2'] = support_structure_investment + infield_cable_investment + pipeline_costs
        print 'bop_costs_h2', outputs['bop_costs_h2']

        outputs['investment_costs_h2'] = support_structure_investment + other_investment_h2 + pipeline_costs + pipeline_installation_costs + infield_cable_investment +\
        other_installation_commissioning_costs_h2 #+ area_use_cost
        outputs['decommissioning_costs_h2'] = decommissioning_costs_h2 + support_decomm_costs
        #print 'purchase price:', inputs['purchase_price']

        print 'infield cable cots:', infield_cable_investment
        print 'Support costs:', support_structure_investment
        print 'Total investment costs electricity:', outputs['investment_costs']
        print 'Total investment costs H2:', outputs['investment_costs_h2']
        print 'Decomissioning H2', outputs['decommissioning_costs_h2']
        print 'Rated power:', inputs['machine_rating']
        print 'Turbine radius:', inputs['rotor_radius']






