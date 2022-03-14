# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 14:58:16 2015

@author: Αλβέρτος
"""


class cost1:
    def __init__(self, value, currency, year):
        value_year = 2016
        # Inflation and exchange rate {'Currency Code': [Average inflation rate, Exchange rate to Euro]}
        self.conversion = {'USD': [2.57, 0.89],
                           'GBP': [2.55, 1.27],
                           'DKK': [1.84, 0.13],
                           'SEK': [2.03, 0.11],
                           'NOK': [1.95, 0.11],
                           'Euro': [2.16, 1.0]}

        inflation_rate = self.conversion[currency][0]
        exchange_rate = self.conversion[currency][1]

        self.ref_value = value
        self.currency = currency
        self.ref_year = year
        self.value = value * ((1.0 + (inflation_rate / 100.0)) ** (value_year - year)) * exchange_rate
        #self.value = 1.32 #Back calculated from BVG 10 MW report


class CostAnalysts:

    def __init__(self, support_team):
        self.support_team = support_team
        self.number_of_turbines = 1
        #self.tower_price = cost1(2.04, 'USD', 2002)  # [$/kg]
        self.tower_price = cost1(1.02, 'USD', 2002)  # [$/kg] #Recalibrated overall costs based on BVG reports
        #self.transition_piece_price = cost1(3.75, 'Euro', 2007)  # [euro/kg]
        self.transition_piece_price = cost1(1.95, 'Euro', 2007)  # [euro/kg] #Recalibrated based on BVG reports
        self.grout_price = cost1(0.1, 'Euro', 2003)  # [euro/kg] (This value is not supported by literature/data and based on some information on the web about concrete
        #self.monopile_price = cost1(2.25, 'Euro', 2007)  # [euro/kg]
        self.monopile_price = cost1(2, 'Euro', 2007)  # [euro/kg] #BVG highly overestimates mass (recheck)
        self.scour_protection_per_volume = cost1(211.0, 'Euro', 2003)  # [euro/m^3]
        self.foundation_installation_per_mass = cost1(1.4, 'USD', 2010)  # [$/kg]
        self.scour_protection_removal_per_volume = cost1(33.0, 'USD', 2010)  # [$/m^3]

    def initialyse(self):
        self.set_support_structure_costs()

    def set_support_structure_costs(self):
        self.support_team.value.economic.capex.procurement.support_structures.tower = self.number_of_turbines * self.tower_price.value * self.support_team.properties.support_structure.tower_mass

        self.support_team.value.economic.capex.procurement.support_structures.transition_piece = self.number_of_turbines * self.transition_piece_price.value * self.support_team.properties.support_structure.transition_piece_mass

        self.support_team.value.economic.capex.procurement.support_structures.grout = self.number_of_turbines * self.grout_price.value * self.support_team.properties.support_structure.grout_mass

        self.support_team.value.economic.capex.procurement.support_structures.monopile = self.number_of_turbines * self.monopile_price.value * self.support_team.properties.support_structure.pile_mass

        self.support_team.value.economic.capex.procurement.support_structures.scour_protection = self.number_of_turbines * self.scour_protection_per_volume.value * self.support_team.properties.support_structure.scour_protection_volume
        # print self.support_team.value.economic.capex.procurement.support_structures.scour_protection + self.support_team.value.economic.capex.procurement.support_structures.monopile + self.support_team.value.economic.capex.procurement.support_structures.grout + self.support_team.value.economic.capex.procurement.support_structures.transition_piece + self.support_team.value.economic.capex.procurement.support_structures.tower
        self.support_team.value.economic.capex.installation.foundations = self.number_of_turbines * self.foundation_installation_per_mass.value * self.support_team.properties.support_structure.pile_mass
        # print self.support_team.value.economic.capex.installation.foundations
        #self.support_team.value.economic.decommissioning.removal.foundations = self.support_team.value.economic.capex.installation.foundations

        self.support_team.value.economic.decommissioning.removal.scour_protection = self.number_of_turbines * self.scour_protection_removal_per_volume.value * self.support_team.properties.support_structure.scour_protection_volume
        # print self.support_team.value.economic.decommissioning.removal.scour_protection + self.support_team.value.economic.decommissioning.removal.foundations
        self.support_team.total_support_structure_cost = self.support_team.value.economic.capex.procurement.support_structures.tower + self.support_team.value.economic.capex.procurement.support_structures.transition_piece + self.support_team.value.economic.capex.procurement.support_structures.grout + self.support_team.value.economic.capex.procurement.support_structures.monopile + self.support_team.value.economic.capex.procurement.support_structures.scour_protection + self.support_team.value.economic.capex.installation.foundations

        self.support_team.value.economic.decommissioning.removal.foundations = self.support_team.value.economic.capex.installation.foundations + self.support_team.value.economic.decommissioning.removal.scour_protection

        print 'tower mass:', self.support_team.properties.support_structure.tower_mass
        print 'monopile mass:', self.support_team.properties.support_structure.pile_mass
        print 'transition piece mass:', self.support_team.properties.support_structure.transition_piece_mass
        print 'tower costs:', self.support_team.value.economic.capex.procurement.support_structures.tower
        print 'monopile costs:', self.support_team.value.economic.capex.procurement.support_structures.monopile
        print 'transition piece costs:', self.support_team.value.economic.capex.procurement.support_structures.transition_piece
        print 'foundation installation costs:',  self.support_team.value.economic.capex.installation.foundations
        print 'foundation decommisioning:', self.support_team.value.economic.decommissioning.removal.foundations
        #print 'real support struc cost:',  self.support_team.value.economic.capex.procurement.support_structures.transition_piece + self.support_team.value.economic.capex.procurement.support_structures.grout + self.support_team.value.economic.capex.procurement.support_structures.monopile + self.support_team.value.economic.capex.procurement.support_structures.scour_protection