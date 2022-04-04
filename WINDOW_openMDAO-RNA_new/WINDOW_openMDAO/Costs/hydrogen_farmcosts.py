from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.input_params import max_n_turbines
from costs.other_costs import other_costs

from WINDOW_openMDAO.input_params import distance_to_grid


class HydrogenFarmCostModel(ExplicitComponent):

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


        self.add_output('investment_costs_h2', val=0.0)
        self.add_output('decommissioning_costs_h2', val=0.0)
        self.add_output('bop_costs_h2', val=0.0)
        self.add_output('pipeline_costs_h2', val=0.0)

        # self.declare_partals(of=['investment_costs', 'decommissioning_costs'], wrt=['n_substations', 'n_turbines', 'length_p_cable_type', 'cost_p_cable_type', 'support_structure_costs', 'depth_central_platform'], method='fd')

    def compute(self, inputs, outputs):
        n_substations = inputs['n_substations']
        n_turbines = inputs['n_turbines']
        length_p_cable_type = inputs['length_p_cable_type']
        cost_p_cable_type = inputs['cost_p_cable_type']
        support_structure_costs = inputs['support_structure_costs']  # this includes tower costs
        support_decomm_costs = inputs['support_decomm_costs']
        depth_central_platform = inputs['depth_central_platform']
        cost_tower = inputs['cost_tower']
        annual_h2 = inputs['annual_h2']

        a = 5*1e5  # the cost in euros/km2 that the developer pays for using ocean area [Hypothetical cost]
        farm_area = inputs['farm_area'] # in km2
        area_use_cost = a*farm_area


        infield_cable_length = sum(length_p_cable_type)



        def pem_decentralized_costs(infield_cable_length , distance_to_grid,annual_h2):
            total_pipeline_length = infield_cable_length + distance_to_grid  # in m

            #pipeline_costfactor = 1.25  # per kW per km (HYGRO estiamtes that matches well with the white paper from Umlat that state roughly 1 euro/kg of H2)

            export_pipeline_costfactor = 0.01 #Euros/kg (Matches HYGRO HKW estimates and also the 2020 European hydrogen backbone paper)
            pipeline_lifetime = 40
            export_pipeline_cost = export_pipeline_costfactor*annual_h2*pipeline_lifetime*(distance_to_grid/1000/60) #Original cost factor of 0.2 euros/kg was adjusted for 60 km length

            #infield_pipeline_cost = pipeline_costfactor* inputs['machine_rating']*(infield_cable_length/1000.0)
            #export_pipeline_cost = pipeline_costfactor * n_turbines * inputs['machine_rating'] * (distance_to_grid / 1000.0)

            #Thermodynamic and Technical Issues of Hydrogen and Methane-Hydrogen Mixtures Pipeline Transmission shows pipeline diameter for different flow rates and pressure
            infield_pipeline_cost = export_pipeline_cost*(1.0/3)*(infield_cable_length/distance_to_grid)  # 1/3rd as infield pipeline diameter would be roughly 1/3rd. Area assumed to be 1/3rd due to small thickness. Length also has to be adjusted for

            pipeline_cost = infield_pipeline_cost + export_pipeline_cost

            print 'infield pipeline cost', infield_pipeline_cost
            print 'export pipeline cost', export_pipeline_cost

            pipeline_installation_cost_perkm = 1e6  # Euros/km (back calculated from BVG for total length of infield (195km) + export (60km)

            pipeline_installation_cost = pipeline_installation_cost_perkm * (total_pipeline_length / 1000.0)

            # print 'pipeline costs', pipeline_cost
            # print 'pipeline installation costs', pipeline_installation_cost

            return pipeline_cost, pipeline_installation_cost

        [pipeline_costs, pipeline_installation_costs] = pem_decentralized_costs(infield_cable_length , distance_to_grid, annual_h2)

        purchase_price_h2 = inputs['purchase_price'] - inputs['machine_rating'] * 40 * 0.88  # cost savings in RNA (converter, transformer, switch gears, etc.). 0.88 for USD to EUR

        turbine_CAPEX_h2 = purchase_price_h2 + cost_tower[0]
        export_cable_h2, electrical_costs_h2, other_investment_h2, decommissioning_costs_h2 = other_costs(depth_central_platform,
                                                                                         n_turbines,
                                                                                         sum(length_p_cable_type),
                                                                                         n_substations, \
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

        farm_CAPEX_h2 = support_structure_investment + other_investment_h2 + pipeline_costs + pipeline_installation_costs
        print 'other investment h2',  other_investment_h2
        print 'pipeline costs', pipeline_costs
        print 'pipeline installation', pipeline_installation_costs

        #### project development and other farm costs based on BVG (https://guidetoanoffshorewindfarm.com/wind-farm-costs) and NREL (https://www.nrel.gov/docs/fy21osti/78471.pdf)
        total_farm_CAPEX = farm_CAPEX_h2 / 0.85  # The other 15 % comes from management, project dev, insurance, contingency, construction management, etc.
        project_dev_management = 0.05*total_farm_CAPEX
        other_farm_costs = 0.1*total_farm_CAPEX #insurance, contingency, construction project management



        outputs['bop_costs_h2'] = support_structure_investment + pipeline_costs - cost_tower[0] * n_turbines  # subtraction as support cost involves tower cost
        outputs['investment_costs_h2'] = total_farm_CAPEX
        outputs['decommissioning_costs_h2'] = decommissioning_costs_h2 + support_decomm_costs
        outputs['pipeline_costs_h2'] = pipeline_costs


        #print 'infield cable costs:', infield_cable_investment


        print 'Total investment costs H2:', outputs['investment_costs_h2']
        print 'project dev and management H2', project_dev_management
        print 'Other farm costs H2 (insurance, contingency)', other_farm_costs
        print 'Decomissioning H2', outputs['decommissioning_costs_h2']
        #print 'Rated power:', inputs['machine_rating']
        #print 'Turbine radius:', inputs['rotor_radius']




        #other_installation_commissioning_costs_h2 = 2.48e8 * (farm_CAPEX_h2 / 2.21978122e+09)

        # print 'other installation commission h2', other_installation_commissioning_costs_h2

