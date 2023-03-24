
'''
Installation cost models for turbine, support structure and electricals (array-cables, export cable, substation)

The foundation is first installed (monopile and transition piece).

Turbine installation phase: Pre-assembly at port depending on installation strategy, followed by transport
to site followed by installation. Pre-assemblies reduce the number of lifts but increases the space occupied on deck,
and hence requires more number of trips.
(Sarker and Faiz: https://www.sciencedirect.com/science/article/pii/S0960148116308035#!)
(Mark and Brian: Green Energy and Technology)

Cable installation depends on km/day rate of the cable laying vessel
'''

########### TURBINE ###########

'''
Number of lifts = 2* Number of turbines * Number of lifts/turbine.....Twice as once during loading at the port and the second time while installing it offshore
Lift height at port is vessel jack up height while lift height during installation is equal to hub height
Lifting time depends on lifting heights and rate of lifting 
Number of assemblies done offshore depends on number of pre-assemblies done onshore 

WTIV vessel day-rate of about 200000 euros/day 
3 lifts with bunny-ear configuration 
jack up speeds of about 1 m/min with capacity of 5 sets of wind turbine components. Transit speed of about 10 km/hr
'''

########### SUPPORT STRUCTURE (MONOPILE + TRANSITION PIECE) ###########

'''
If soil is erodable, scour protection will be required which increases vessel spread and installation time 
Would mainly depend on number of foundations and soil type. 
BVG gives a number of 2-3 days/monopile including mobilization, loading, waiting time for weather (matches with estimates from Green Energy and Technology)
'''

########### CABLES AND SUBSTATION ###########

'''
BVG states day-rates maybe around 210000 euros for substation jack-up vessels and 105000 euros for cable laying vessels; 150000 euros for cable burial vessels (including burial equipment, ROV, plough)
cable pull-in and electrical testing and termination takes 16 million euros extra (According to BVG)
Cable lay-rate of about 1 km/day from 'Offshore installation book' and about 4-5 km/day from NREL paper.
Infield cables have lower lay rate due to more number of connections (0.5 km/day)

substation installation vessel (HLV) day-rate range 200-500 euros/day based on BVG, 500 used by NREL paper
to and fro travel time of about 1 day + installation time of about 1-2 days + mobilization demobilization of 7 days
'''

import numpy as np


def installation_foundation(rotor_diameter, n_t):
    dayrate_wtiv = 200000*(rotor_diameter/200) #scaling up with foundation length/mass?
    day_per_foundation = 2.5
    day_total = np.ceil(day_per_foundation*n_t)*1.5  #for weather delays
    mobilization_wtiv = 500000

    cost_installation_foundation = dayrate_wtiv*day_total + mobilization_wtiv*2

    return cost_installation_foundation

def installation_turbine(rotor_diameter, hub_height, n_t, distance_to_shore):
    dayrate_wtiv = 200000*(rotor_diameter/200) #larger turbines require more deck space, higher lifting capacities, larger vessels
    lifting_rate = 1 #m/min which is the same as 1 min/m
    vessel_capacity = 5 #5 units per trip
    no_lifts_per_turbine = 3  #3 lifts per turbine (tower + bunny configuration nacelle + last blade)
    transit_speed = 10 #km/hr
    mobilization_time = 7 #7 days
    mobilization_wtiv = 500000

    no_trips = n_t/vessel_capacity

    loading_time = 30*lifting_rate*no_lifts_per_turbine*vessel_capacity/60  #where 30 m is the height of the vessel
    travel_time = distance_to_shore*2/transit_speed #a factor of 2 for to and fro
    installation_time_perturb = 60 #60 hours installation time per turbine other than loading and travel time

    installation_time = (hub_height*lifting_rate*no_lifts_per_turbine*vessel_capacity/60) + installation_time_perturb*vessel_capacity

    total_time = (loading_time + travel_time + installation_time)*no_trips
    #day_total = (total_time/24 + mobilization_time*2)*1.5  #for weather delays
    day_total = (total_time / 24) * 1.5  # for weather delays

    cost_installation_turbine = dayrate_wtiv*day_total + mobilization_wtiv*2

    return cost_installation_turbine

def installation_electrical(infield_length, export_length):

    #day rates back calculated from BVG burial costs
    cable_installation_rate_infield = 0.1 #km/hr for simulatenous lay and burial
    cable_installation_rate_export = 0.1 #km/hr for simulatenous lay and burial. Higher for export cable due to lower number of connections to be made
    clv_dayrate = 110000 #cable laying vessel
    cbv_dayrate = 140000 #cable burial vessel
    mobilization_clv = 550000
    mobilization_cbv = 550000

    days_export_cable = export_length/cable_installation_rate_export/24
    days_infield_cable = infield_length/cable_installation_rate_infield/24

    cost_cable_infield = days_infield_cable*(clv_dayrate + cbv_dayrate)*1.5 #for weather delays
    cost_cable_export = days_export_cable*(clv_dayrate + cbv_dayrate)*1.5 #for weather delays

    extra_costs = 20e6 # for cable pull-in, electrical testing and termination, onshore connection

    cost_installation_cables = cost_cable_export + cost_cable_infield + extra_costs + mobilization_cbv*2 + mobilization_clv*2  #1.5 to account for survey, clearance of seabed, etc.
    #print(cost_cable_export + extra_costs)

    hlv_dayrate = 500000
    days_substation = 20 #includes travel, mobilization, installation time
    mobilization_costs = 550000
    onshore_substation_costs = 25e6
    cost_installation_substation = hlv_dayrate*days_substation*1.5 + mobilization_costs*2 + onshore_substation_costs
    cost_installation_electrical = cost_installation_cables + cost_installation_substation


    return cost_installation_electrical


def installation_total(n_t,rotor_diameter, hub_height, distance_to_shore,infield_length, export_length ):
    cost_installation_foundation = installation_foundation(rotor_diameter,n_t)
    cost_installation_turbine = installation_turbine(rotor_diameter, hub_height, n_t, distance_to_shore)
    cost_installation_electrical = installation_electrical(infield_length, export_length)

    total_installation_costs = cost_installation_turbine + cost_installation_foundation + cost_installation_electrical

    return cost_installation_foundation, cost_installation_turbine, cost_installation_electrical, total_installation_costs



