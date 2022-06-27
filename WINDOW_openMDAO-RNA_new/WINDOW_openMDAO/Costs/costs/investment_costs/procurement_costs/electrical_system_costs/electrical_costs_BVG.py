'''
A simple electrical cost model based on BVG estimates
Electrical components include export array cable and offshore and onshore substations
Export cable includes core, sheath, protection layers, joints,etc.
Offshore substation includes electrical system (Transformers, switchgears, etc.) + supporting structure + facilities
'''

import numpy as np


def electrical_procurement_costs_BVG(NT, P_rated, distance_to_grid, config):

    if config == 1:
        cable_massperlength_ref = 90.0 #90 kg/m for a 220 kV export cable delivering 1000 MW
        cable_massperlength = cable_massperlength_ref*NT*(P_rated/1000.0)/1000.0 #Scaled mass/m for a different farm power

        cost_kgperm = 1.69e6 #Euros/(kg/m)
        export_cable_cost = (cable_massperlength*cost_kgperm)*distance_to_grid/60.0  #Normalized with a distance of 60 km distance to shore which was used as a reference

        ##### model 1: number of substations (discrete)

        single_offshore_substation_cap = 500 #one substation can take upto 500 MW
        single_offshore_substation_cost = 70e6 #cost of one substation that includes electricals, facilities and structure

        #substations_required = np.ceil(NT*(P_rated/1000.0)/single_offshore_substation_cap)

        tol = NT*(P_rated/1000.0)/single_offshore_substation_cap - np.round(NT*(P_rated/1000.0)/single_offshore_substation_cap) #check if the value just crosses an integer

        if tol>0 and tol<0.01:
            substations_required = np.round(NT * (P_rated / 1000.0) / single_offshore_substation_cap)

        else:
            substations_required = np.ceil(NT * (P_rated / 1000.0) / single_offshore_substation_cap) #otherwise choose higher number of substations


        #offshore_substation_costs = substations_required*single_offshore_substation_cost

        ##### model 2: fixed and variable component

        offshore_substation_fixed = 94e6 #Euros. Includes facilities + support structure with helipad
        offshore_substation_var = 53e6*NT*(P_rated/1000.0)/1000.0  #Euros

        offshore_substation_costs = offshore_substation_fixed + offshore_substation_var

        ##### model 3: fully variable

        # offshore_substation_costs = 140e6*NT*(P_rated/1000.0)/1000.0 #BVG costs varied with power of the farm

        onshore_substation_costs = 35e6*(NT*P_rated/1000.0)/1000 #Euros

        electrical_total_costs = export_cable_cost + offshore_substation_costs + onshore_substation_costs

        #print 'export cable', export_cable_cost
        #print 'offshore substation:', offshore_substation_costs
        #print 'onshore substation:', onshore_substation_costs

    elif config == 2: #hydrogen
        export_cable_cost = 0 # for HYGRO
        electrical_total_costs = 0 # for HYGRO




    return export_cable_cost, electrical_total_costs





