'''
A simple electrical cost model based on BVG estimates
Electrical components include export array cable and offshore and onshore substations
Export cable includes core, sheath, protection layers, joints,etc.
Offshore substation includes electrical system (Transformers, switchgears, etc.) + supporting structure + facilities
'''

def electrical_procurement_costs_BVG(NT, P_rated):
    cable_massperlength_ref = 90.0 #90 kg/m for a 220 kV export cable delivering 1000 MW
    cable_massperlength = cable_massperlength_ref*NT*(P_rated/1000.0)/1000.0 #Scaled mass/m for a different farm power

    cost_kgperm = 1.69e6 #Euros/(kg/m)
    export_cable_cost = cable_massperlength*cost_kgperm

    offshore_substation_fixed = 94e6 #Euros. Includes facilities + support structure with helipad
    offshore_substation_var = 53e6*NT*(P_rated/1000.0)/1000.0  #Euros

    offshore_substation_costs = offshore_substation_fixed + offshore_substation_var

    onshore_substation_costs = 35e6*(NT*P_rated/1000.0)/1000 #Euros

    electrical_total_costs = export_cable_cost + offshore_substation_costs + onshore_substation_costs

    print 'export cable', export_cable_cost
    print 'offshore substation:', offshore_substation_costs
    print 'oshore substation:', onshore_substation_costs

    return electrical_total_costs





