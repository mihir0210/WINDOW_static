from openmdao.api import ExplicitComponent



class AbstractOandM(ExplicitComponent):

    def setup(self):
        self.add_input('AEP', val=0.0)
        self.add_input('array_efficiency', val=0.0)

        self.add_input('N_T', val=0.0)
        self.add_input('P_rated', val=0.0)

        self.add_input('hub_height', val=0.0)
        self.add_input('rna_CAPEX', val=0.0)
        self.add_input('farm_CAPEX', val=0.0)
        self.add_input('bop_costs', val=0.0)

        self.add_output('annual_cost_O&M', val=0.0)
        self.add_output('availability', val=0.0)


    def compute(self, inputs, outputs):
        AEP = inputs['AEP']
        eff = inputs['array_efficiency']

        N_T = inputs['N_T']
        P_rated = inputs['P_rated']

        hub_height = inputs['hub_height']
        rna_CAPEX = inputs['rna_CAPEX']
        farm_CAPEX = inputs['farm_CAPEX']
        bop_costs = inputs['bop_costs']
        outputs['annual_cost_O&M'], outputs['availability'] = self.OandM_model(AEP, eff, N_T, P_rated, hub_height, rna_CAPEX, farm_CAPEX, bop_costs)
