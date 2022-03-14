'''
Includes assembly,turbine profit margins, warranty
https://guidetoanoffshorewindfarm.com/wind-farm-costs (BVG)
https://escholarship.org/content/qt4m60d8nt/qt4m60d8nt.pdf (Report by Mark Bolinger)
It is assumed that 70 % of turbine costs come from RNA and tower
while the other 30 % is warranty, assembly, profit margins, etc.
'''

def turbine_other_costs(turbine_CAPEX, n_turbines):
    # cost_BVG = 4e8
    #
    # norm_cost_BVG = cost_BVG/(6224793*100) #normalizing with 10 MW turbine CAPEX and number of turbines (100) in the BVG reference farm
    #
    # turbine_other_costs = norm_cost_BVG*(turbine_CAPEX*n_turbines)

    turbine_other_costs = ((turbine_CAPEX/0.7)*0.3)*n_turbines #RNA and tower costs assumed to be 70 % while 30 % costs of the total share is other costs


    return turbine_other_costs