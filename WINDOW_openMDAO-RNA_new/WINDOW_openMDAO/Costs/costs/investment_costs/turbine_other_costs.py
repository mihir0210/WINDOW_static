'''
Includes assembly,turbine profit margins
'''

def turbine_other_costs(NT, P_rated):
    cost_perMW = 3e5 #Euros/MW (taken from BVG - warranty - assmebly costs)

    turbine_other_costs = cost_perMW*NT*(P_rated/1000.0)

    return turbine_other_costs