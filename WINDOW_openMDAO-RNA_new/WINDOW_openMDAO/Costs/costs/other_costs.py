import csv

def other_costs(depth_central_platform, n_turbines, infield_length, n_substations, distance_to_grid, distance_to_harbour,\
                turbine_rated_power, rotor_radius, purchase_price, warranty_percentage, \
                rna_mass, hub_height, generator_voltage, collection_voltage, turbine_CAPEX, config):

    from .investment_costs.project_development_cost import project_development_cost
    from .investment_costs.management_cost import management_costs
    from .investment_costs.procurement_costs.auxiliary_costs.auxiliary_costs import auxiliary_procurement
    from .investment_costs.procurement_costs.electrical_system_costs.electrical_costs import electrical_procurement_costs
    from .investment_costs.procurement_costs.RNA_costs.RNA_costs import rna_costs
    from .investment_costs.installation_costs.auxiliary_installation_costs import auxiliary_installation_costs
    from .investment_costs.installation_costs.electrical_installation_costs import electrical_installation_costs
    from .investment_costs.installation_costs.RNA_installation_costs import rna_installation_costs
    from .decommissioning_costs.decommissioning_costs import decommissioning_costs

    from .investment_costs.procurement_costs.electrical_system_costs.electrical_costs_BVG import electrical_procurement_costs_BVG
    from .investment_costs.installation_costs.electrical_installation_costs_BVG import electrical_installation_costs_BVG
    from .investment_costs.installation_costs.other_costs import other_installation_commissioning_costs
    from .investment_costs.turbine_other_costs import turbine_other_costs
    from .investment_costs.installation_costs.installation_model import installation_total

    #project_development = project_development_cost(n_turbines, turbine_rated_power)

    #procurement_auxiliary = auxiliary_procurement(depth_central_platform, n_substations, n_turbines, turbine_rated_power)

    procurement_rna = rna_costs(n_turbines, purchase_price, warranty_percentage)

    turbine_other_costs = turbine_other_costs(turbine_CAPEX, n_turbines)

    [export_cable, procurement_electrical] = electrical_procurement_costs_BVG(n_turbines, turbine_rated_power, distance_to_grid, config)
    #procurement_electrical = 0.0 #for a case in NL where TenneT pays
    #export_cable = 0.0#for a case in NL where TenneT pays

    #installation_electrical = electrical_installation_costs_BVG(config, infield_length)


    #procurement_electrical = electrical_procurement_costs(n_turbines, turbine_rated_power, generator_voltage, collection_voltage)

    #installation_auxiliary = auxiliary_installation_costs(n_turbines, turbine_rated_power)

    #installation_electrical = electrical_installation_costs()

    #installation_rna = rna_installation_costs(n_turbines, rotor_radius, hub_height)

    [installation_foundation, installation_turbine, installation_electrical, total_installation_costs] = installation_total(n_turbines,2*rotor_radius, hub_height, distance_to_harbour,infield_length/1000, distance_to_grid )

    decommissioning = decommissioning_costs(infield_length, n_turbines, rna_mass, hub_height,config)


    if config==1:

        field_names = ['costs_exportcable', 'costs_total_electrical', 'costs_installation_electrical', 'costs_RNA_elec', 'costs_installation_turbine', 'costs_other_turbine_elec', 'installation_foundation']
        description = ['Export cable costs', 'Total electrical procurement costs including substations', 'Total electrical installation costs', 'Total RNA procurement costs in euros for electricity', 'Total turbine installation costs', 'Other turbine costs (profits, assembly, etc. for electricity', 'Foudnation installation costs']
        data = {field_names[0]: [export_cable[0], description[0]],
                field_names[1]: [procurement_electrical[0], description[1]],
                field_names[2]: [installation_electrical, description[2]],
                field_names[3]: [procurement_rna[0], description[3]],
                field_names[4]: [installation_turbine[0], description[4]],
                field_names[5]: [turbine_other_costs[0], description[5]],
                field_names[6]: [installation_foundation[0], description[6]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()

    elif config==2:
        field_names = ['costs_RNA_H2', 'costs_other_turbine_H2']
        description = ['Total RNA procurement costs in euros for H2', 'Other turbine costs (profits, assembly, etc. for H2']
        data = {field_names[0]: [procurement_rna[0], description[0]],
                field_names[1]: [turbine_other_costs[0], description[1]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()


    #investment_costs = project_development + procurement_auxiliary + procurement_rna + procurement_electrical + installation_auxiliary + installation_electrical + installation_rna
    #investment_costs = procurement_rna + turbine_other_costs + procurement_electrical + installation_electrical + installation_rna
    #investment_costs = project_development + procurement_rna + turbine_other_costs + installation_rna + other_installation_commissioning_costs
    investment_costs = procurement_rna + turbine_other_costs + procurement_electrical + total_installation_costs
    # print "project_development ", project_development
    # print "procurement_auxiliary", procurement_auxiliary 
    # print "procurement_rna" ,procurement_rna 
    # print "procurement_electrical" ,procurement_electrical 
    # print "installation_auxiliary" ,installation_auxiliary 
    # print "installation_electrical", installation_electrical
    # print  "installation_rna", installation_rna
    # print "installation + procurement turbines"
    # print procurement_rna + installation_rna
    #
    # print "installation + procurement electrical"
    # print installation_electrical + procurement_electrical
    #
    # print "project development"
    # print project_development
    #
    # print "auxiliary costs"
    # print procurement_auxiliary + installation_auxiliary
    #
    # print "decommissioning costs"
    # print decommissioning

    #management_investment = management_costs(investment_costs)

    # print 'project development:', project_development
    # print 'management costs:', management_investment

    # print "investment costs"
    # print investment_costs + management_investment
    electrical_costs = procurement_electrical
    return export_cable, electrical_costs, investment_costs, decommissioning


if __name__ == '__main__':
    print((total_costs(20.0, 5, 230000)))
