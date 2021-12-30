from WINDOW_openMDAO.src.api import AbstractOandM


class OM_model1(AbstractOandM):
    def OandM_model(self, AEP, eff, N_T, P_rated,hub_height_norm,rna_norm,farm_capex_norm, bop_norm):
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
        # print 'farm_capex_norm', farm_capex_norm
        # print 'hub height norm', hub_height_norm
        # print 'rna norm', rna_norm
        # print 'bop norm', bop_norm
        fixed_costs = 21e6 #taken from BVG for a 1000 MW farm
        variable_insurance = 8.2e6*farm_capex_norm

        #maintenance and service
        # assuming 1/3rd of turbine maintenance and service is inspection that scales with hub height,
        # and the rest is replacement (which scales with rna capex)
        #bop maintenance and service scales with bop costs

        variable_turbine_inspection = 13e6*hub_height_norm
        variable_turbine_repair = 26e6*rna_norm

        variable_bop = 21e6*bop_norm

        costs_om = fixed_costs + variable_insurance + variable_turbine_inspection + variable_turbine_repair + variable_bop

        #costs_om = 1.32232705e+08 # if O&M is assumed to be fix

        print 'O&M costs:', costs_om
        return costs_om, availability
