from WINDOW_openMDAO.src.api import AbstractSupportStructureDesign
from WINDOW_openMDAO.SupportStructure.teamplay_folder.teamplay_file import teamplay
import numpy as np


class TeamPlay(AbstractSupportStructureDesign):

    def support_design_model(self, TI, depth, rotor_radius, rated_wind_speed, \
                             rotor_thrust, rna_mass, \
                             solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                             yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity):
        costs = []
        support_decomm_costs = []
        base_dia = []
        top_dia = []
        tower_length = []
        min_tower_wall_thickness = []
        max_tower_wall_thickness =[]

        tower_costs = []

        results =[]



        #for i in range(len(TI)):
        i =0

        [costs_, support_decomm_costs_,base_dia_, top_dia_, \
             min_tower_wall_thickness_, max_tower_wall_thickness_, tower_costs_] = \
             teamplay(TI[i], depth[i], rotor_radius, rated_wind_speed, \
                                  rotor_thrust, rna_mass, \
                                  solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                  yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)
        for i in range(len(TI)):

            costs.append(costs_)
            support_decomm_costs.append(support_decomm_costs_)
            base_dia.append(base_dia_)
            top_dia.append(top_dia_)
            min_tower_wall_thickness.append(min_tower_wall_thickness_)
            max_tower_wall_thickness.append(max_tower_wall_thickness_)
            tower_costs.append(tower_costs_)


        #TI = np.array(TI)
        #index = np.argmax(TI)

        index = 1
        #print TI, index, base_dia

        base_dia = base_dia[index]
        top_dia = top_dia[index]
        min_tower_wall_thickness = min_tower_wall_thickness[index]
        max_tower_wall_thickness = max_tower_wall_thickness[index]


        '''
            costs.append(teamplay(TI[i], depth[i], rotor_radius, rated_wind_speed, \
                                  rotor_thrust, rna_mass, \
                                  solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                  yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[0])


            
            base_dia.append(teamplay(TI[i], depth[i], rotor_radius, rated_wind_speed, \
                                  rotor_thrust, rna_mass, \
                                  solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                  yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[1])
            
            top_dia.append(teamplay(TI[i], depth[i], rotor_radius, rated_wind_speed, \
                                  rotor_thrust, rna_mass, \
                                  solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                  yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[2])
            tower_length.append(teamplay(TI[i], depth[i], rotor_radius, rated_wind_speed, \
                                  rotor_thrust, rna_mass, \
                                  solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                  yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[3])
            tower_wall_thickness.append(teamplay(TI[i], depth[i], rotor_radius, rated_wind_speed, \
                                  rotor_thrust, rna_mass, \
                                  solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                  yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[4])

        base_dia = teamplay(TI[-1], depth[-1], rotor_radius, rated_wind_speed, \
                                 rotor_thrust, rna_mass, \
                                 solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                 yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[1]

        top_dia = teamplay(TI[-1], depth[-1], rotor_radius, rated_wind_speed, \
                                rotor_thrust, rna_mass, \
                                solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[2]


        min_tower_wall_thickness = teamplay(TI[-1], depth[-1], rotor_radius, rated_wind_speed, \
                                             rotor_thrust, rna_mass, \
                                             solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                             yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[3]

        max_tower_wall_thickness = teamplay(TI[-1], depth[-1], rotor_radius, rated_wind_speed, \
                                             rotor_thrust, rna_mass, \
                                             solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                                             yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)[4]

        #tower_wall_thickness = np.array(tower_wall_thickness)
        #print tower_wall_thickness
        #thickness_max_row=tower_wall_thickness.max(1) #maximum in each row
        #thickness_min_row=tower_wall_thickness.min(1) #minimum in each row

        #thickness_max_row = max(tower_wall_thickness)
        #thickness_min_row = min(tower_wall_thickness)
        #print thickness_max_row'''


        #print base_dia, top_dia, min_tower_wall_thickness, max_tower_wall_thickness
        #print 'Support Done'
        #return np.array(costs), min(np.array(base_dia)), min(np.array(top_dia)), np.array(tower_length), \
               #thickness_min_row[0], thickness_max_row[0]

        return np.array(costs), np.array(support_decomm_costs), base_dia, top_dia, min_tower_wall_thickness,\
        max_tower_wall_thickness, np.array(tower_costs[0])




