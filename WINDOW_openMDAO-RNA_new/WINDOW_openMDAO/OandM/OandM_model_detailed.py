
import numpy as np

'''
O&M cost numbers
BVG estimates 89 M/year for a size of roughly 1 GW and 100 turbines

https://www.pbl.nl/sites/default/files/downloads/pbl-2019-costs-of-offshore-wind-energy-2018_3623.pdf
Hollandse Kust Zuid (Total of 700 MW) has O&M of about 41 Euro/kW/year; 
Total of 30 M/year

Hollandse Kust Noord (Total of 759 MW) has O&M of about 41 Euro/kW/year;
Total of 31 M/year

TNWWFS I with roughly 700 MW has O&M cost of about 64 Euro/kW/year; located 56 or 90 km off the coast
Total of 45 M/year
'''

'''
https://www.nrel.gov/docs/fy16osti/66262.pdf
https://journals-sagepub-com.tudelft.idm.oclc.org/doi/pdf/10.1260/0309-524X.39.1.1
Vessel types and rates 
CTV (Crew Transfer Vessel) ---  3000 euros/day based on BVG confirmed with IEA wind task 26 study (https://www.nrel.gov/docs/fy16osti/66262.pdf)
Roughly 22 mins of one-way transfer time to one turbine

jack up WTIV (Wind turbine Installation Vessel) - 225000/day with mobilization time of 60 days and mobilization cost of 500000 
Used for major replacements 

CLV (Cable laying vessel) -- 100000/day with mobilization time of 30 days and mobilization cost of 550000

DSV (Diving support vessel) - 75000/day with a mobilization time of 15 days and mobilization cost of 225000
'''


def oandm_detailed(rna_costs, array_cable_costs, distance_to_shore, n_t):


    ####### INPUT PARAMS ######

    shift_time = 24 # shift time
    pound_to_euro = 1.17  # to convert BVG estimates to euros
    n_technicians = 50 * (n_t / 100)  # taken from BVG. Scales with Number of turbines
    salary_technician = 1e5  # salary in euros per technician per year

    dayrate_ctv = 3000
    dayrate_wtiv = 4.2e5
    dayrate_jackup = 1.4e5
    dayrate_clv = 100000
    dayrate_dsv = 75000
    dayrate_hlv = 2e5  # https://journals-sagepub-com.tudelft.idm.oclc.org/doi/pdf/10.1260/0309-524X.39.1.1

    mobilization_wtiv = 2e6
    mobilization_jackup = 500000
    mobilization_dsv = 225000
    mobilization_clv = 550000
    mobilization_hlv = 500000

    # speed of different vessels in km/h
    speed_ctv = 40
    speed_hlv = 7
    speed_clv = 6

    # travel time for one round-trip in hours

    traveltime_ctv = 2 * distance_to_shore / speed_ctv
    traveltime_hlv = 2 * distance_to_shore / speed_hlv
    traveltime_clv = 2 * distance_to_shore / speed_clv


    ###### OPERATIONAL COSTS ####
    #fixed_costs = 25e6*pound_to_euro  # insurance, logistics, training, survey, etc. taken from BVG
    operational_costs = 22.5e6 #insurance, logistics, training, survey, etc. (Average of High estimates taken from IEA Task 26 baseline document and BVG)

    #### PREVENTIVE MAINTENANCE AND CORRECTIVE INSPECTION ###

    service_hours_pertub = 50 #services hours per turbine
    service_hours_substation = 30*4 # 30 hours and 4 expected trips
    service_hours_structure = 4 #expected hours for the support structure
    total_service_hours = (service_hours_structure + service_hours_pertub)*n_t + service_hours_substation
    no_ctv = 2
    total_no_trips = 5
    no_days = np.ceil(total_service_hours/no_ctv/shift_time + (traveltime_ctv*no_ctv*total_no_trips/24))

    cost_inspection_preventive = no_days*no_ctv*dayrate_ctv

    rp_preinspection = 7.5
    ene_preinspection = 0.4
    no_ctvs = 1
    total_no_trips = 1
    no_days = np.ceil(ene_preinspection* rp_preinspection*n_t/shift_time/no_ctvs + (traveltime_ctv*no_ctv*total_no_trips/24))

    cost_inspection_corrective = no_days*dayrate_ctv

    cost_inspection = cost_inspection_corrective + cost_inspection_preventive


    ##### TURBINE CORRECTIVE MAINTENANCE ####

    # ene stands for expected number of events/turbine/year
    # rp stands for repair time in hours
    # sp stands for spare part cost (Expressed as a % of RNA costs)


    ene_minor_repair = 3
    rp_minor_repair = 7.5
    sp_minor_repair = 0.001

    no_ctvs = 2
    total_no_trips = 10
    no_days = np.ceil(ene_minor_repair*rp_minor_repair*n_t/shift_time/no_ctvs + traveltime_ctv*no_ctv*total_no_trips/24)
    cost_vessels_minor_repair = no_days*no_ctvs*dayrate_ctv
    cost_sp_minor_repair = sp_minor_repair*rna_costs

    ene_major_repair = 0.3
    rp_major_repair = 22
    sp_major_repair = 0.005

    no_ctvs = 2
    total_no_trips = 1
    no_days = np.ceil(ene_major_repair*rp_major_repair*n_t/shift_time/no_ctvs + traveltime_ctv*no_ctv*total_no_trips/24)
    cost_vessels_major_repair = no_days*no_ctvs*dayrate_ctv
    cost_sp_major_repair = sp_major_repair*rna_costs


    ene_major_replacement = 0.08
    rp_major_replacement = 34
    sp_major_replacement = 0.1


    no_instances = np.ceil(ene_major_replacement*n_t)
    no_mobilizations = np.ceil(no_instances/1)  # depends on the strategy. Assumed that the operator clubs major repairs and calls for a HLV once for x turbine replacements
    no_days = no_instances*(np.ceil(rp_major_replacement/shift_time + traveltime_hlv/24))
    cost_vessels_major_replacement = no_days*dayrate_hlv + mobilization_hlv*2*no_mobilizations
    cost_sp_major_replacement = sp_major_replacement*rna_costs*no_instances

    total_cost_turbine_maintenance = cost_vessels_minor_repair + cost_vessels_major_repair + cost_vessels_major_replacement + cost_sp_minor_repair + cost_sp_major_repair + cost_sp_major_replacement
    total_cost_turbine_maintenance_sp = cost_sp_minor_repair + cost_sp_major_repair + cost_sp_major_replacement

    ##### BOS CORRECTIVE MAINTENANCE ####

    ene_scour_repair = 0.023
    rp_scour_repair = 8

    no_instances = np.ceil(ene_scour_repair*n_t)
    no_days = no_instances*(np.ceil(rp_scour_repair/shift_time + traveltime_clv/24))
    cost_vessels_scour_repair = no_days*dayrate_dsv + mobilization_dsv*2*no_instances

    ene_cable_replacement = 0.0004
    rp_cable_replacement = 32

    no_instances = np.ceil(ene_cable_replacement*n_t)
    no_days = no_instances*(np.ceil(rp_cable_replacement/shift_time))
    cost_vessels_cable_replacement = no_days*dayrate_clv + mobilization_clv*2*no_instances
    cost_sp_cable_replacement = 0.05*array_cable_costs

    total_cost_bos_maintenance = cost_sp_cable_replacement + cost_vessels_cable_replacement + cost_vessels_scour_repair
    total_cost_bos_maintenance_sp = cost_sp_cable_replacement


    vessel_cost = cost_vessels_minor_repair + cost_vessels_major_repair + cost_vessels_major_replacement + cost_vessels_scour_repair + cost_vessels_cable_replacement
    n_tech = np.ceil(n_technicians*(n_t/100)) #number of technicians scale with number of turbines
    costs_om = operational_costs + cost_inspection + vessel_cost + total_cost_turbine_maintenance_sp + total_cost_bos_maintenance_sp  + n_tech*salary_technician

    print('Operational costs:', operational_costs)
    print('Inspection cost:', cost_inspection)
    print('vessel costs:', vessel_cost)
    print('Turbine maintenance spare part:', total_cost_turbine_maintenance_sp)
    print('BoS maintenance spare part:', total_cost_bos_maintenance_sp)
    print('Salary technician:', salary_technician*n_technicians)

    availability = 0.97  # for the same farm

    return costs_om, availability


rna_costs = 6.67e6  # RNA costs of one turbine
ref_cable_costs = 257557706  # array + export cable cost
array_cable_costs = 97852706
distance_to_shore = 60 #in km
n_t = 100


[costs_om, availability] = oandm_detailed(rna_costs, array_cable_costs, distance_to_shore, n_t)

print('Total O&M costs:', costs_om)


