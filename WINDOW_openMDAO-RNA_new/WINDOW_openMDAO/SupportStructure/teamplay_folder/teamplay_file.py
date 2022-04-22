from .lib.designers_support.dimension_team_support import DimensionTeamSupport
from .lib.system.properties import RNA
from .lib.environment.physical_environment import Site
from .currency import Cost1


def teamplay(TI, depth, rotor_radius, rated_wind_speed, rotor_thrust, rna_mass, \
             solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
             yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity):

    #print 'RNA mass:', rna_mass
    dimension_team_support = DimensionTeamSupport()
    #dimension_team_support.fsf = TI + 1.4 # 1.4 safety factor to account for wave-induced fatigue and the rest is wind-induced.
    dimension_team_support.fsf = 1
    rna = RNA(rotor_radius, rated_wind_speed, rotor_thrust, rna_mass, \
              solidity_rotor, cd_rotor_idle_vane, cd_nacelle, \
                 yaw_diameter, front_area_nacelle, yaw_to_hub_height, mass_eccentricity)
    site_data = Site()
    site_data.water_depth = depth


    dimension_team_support.run(rna, site_data)

    boat_landing_cost = Cost1(60000.0, 'USD', 2003)  # [$/turbine]
    #Investment costs - Procurement & Installation - Support structure

    min_tower_wall_thickness = min(dimension_team_support.design_variables.support_structure.tower.wall_thickness)
    max_tower_wall_thickness = max(dimension_team_support.design_variables.support_structure.tower.wall_thickness)

    monopile_length = dimension_team_support.design_variables.support_structure.monopile.length

    #print 'monopile length', monopile_length

    return dimension_team_support.total_support_structure_cost + boat_landing_cost, \
            dimension_team_support.cost_analysts.support_team.value.economic.decommissioning.removal.foundations, \
            dimension_team_support.design_variables.support_structure.tower.base_diameter, \
            dimension_team_support.design_variables.support_structure.tower.top_diameter, \
           min_tower_wall_thickness, max_tower_wall_thickness , \
           dimension_team_support.cost_analysts.support_team.value.economic.capex.procurement.support_structures.tower
           #dimension_team_support.design_variables.support_structure.tower.max_wall_thickness
    # dimension_team_support.design_variables.support_structure.tower.length, \




