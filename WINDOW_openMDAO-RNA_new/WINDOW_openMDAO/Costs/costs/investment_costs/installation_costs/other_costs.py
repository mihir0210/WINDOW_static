'''
This includes insurance, contingency (spent) and construction project management
'''


def other_installation_commissioning_costs(NT, P_rated):

    cost_perMW = 2.48e5 #Euros

    other_installation_commissioning_costs = cost_perMW*NT*(P_rated/1000.0)

    return other_installation_commissioning_costs

