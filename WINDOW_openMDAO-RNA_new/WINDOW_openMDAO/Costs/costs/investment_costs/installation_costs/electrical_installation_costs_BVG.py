'''
Export cable installation includes cable burial, pull-in, cable-laying vessels, etc.
Offshore and onshore substation installation is taken as it is from BVG
'''


from WINDOW_openMDAO.input_params import distance_to_grid


def electrical_installation_costs_BVG(config, infield_length):

    if config == 1:

        cable_installation_cost_perkm = 1e6 #1.25e6 #Euros/km  (back calculated from BVG for total length of infield (195km) + export (60km)

        array_cable_installation_cost = cable_installation_cost_perkm*(infield_length/1000.0)

        export_cable_installation_cost = cable_installation_cost_perkm*(distance_to_grid/1000.0)

        cable_installation_total = array_cable_installation_cost + export_cable_installation_cost

        offshore_substation_installation = 4.1e7 #Euros
        onshore_substation_installation = 2.9e7 #Euros

        electrical_installation_total = cable_installation_total + offshore_substation_installation + onshore_substation_installation

        #print 'array cable installation', array_cable_installation_cost
        #print 'export cable installation', export_cable_installation_cost
        #print 'cable installation:', cable_installation_total
        #print 'offshore sub and onshore substation installation', offshore_substation_installation, onshore_substation_installation

    elif config == 2:
        electrical_installation_total = 0 #for HYGRO

    return electrical_installation_total