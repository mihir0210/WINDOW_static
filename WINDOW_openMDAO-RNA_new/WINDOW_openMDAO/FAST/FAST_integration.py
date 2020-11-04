import numpy as np
import scipy.io
import pandas as pd
import math
import os
import time


### Start Matlab engine and add the path of Matlab_scripts and Subfunctions ###
import matlab.engine

'''
eng2 = matlab.engine.start_matlab()
dir = os.getcwd() + r"\Matlab_scripts"
eng2.cd(dir, nargout=0)
dir2 = dir + r"\subfunctions"
eng2.addpath(dir2, nargout=0)'''


from scipy.interpolate import pchip
from WINDOW_openMDAO.FAST.AbsFAST_copy import AbsFAST
from WINDOW_openMDAO.FAST.airfoils_coord_integration import airfoils_coord
from WINDOW_openMDAO.RNA.Blade.airfoils import ReadAirfoil
from WINDOW_openMDAO.FAST.load_case_selector_integration import load_case_selector
from WINDOW_openMDAO.FAST.post_processor_integration import post_processor


class FAST(AbsFAST):
    '''
    Creates all .mat files required to run the FAST simulink block and post process data
        '''


    def compute(self, inputs, outputs):




        t_start = time.time()
        num_airfoils = self.metadata['num_airfoils']
        num_nodes = self.metadata['num_nodes']
        num_tnodes = self.metadata['num_tnodes']
        tower_sm = self.metadata['tower_sm']
        tower_ym = self.metadata['tower_ym']
        tower_density = self.metadata['tower_density']
        rho_air = self.metadata['rho_air']

        # blade inputs
        blade_mass = inputs['blade_mass']
        blade_ei_flap = inputs['blade_ei_flap']
        blade_ei_edge = inputs['blade_ei_edge']
        blade_radius = inputs['blade_radius']
        blade_chord = inputs['blade_chord']
        blade_twist = inputs['blade_twist']
        blade_nfoil = inputs['blade_nfoil']
        blade_ifoil = inputs['blade_ifoil']
        blade_cone = inputs['blade_cone']
        blade_number = inputs['blade_number']
        pitch = inputs['pitch']
        design_tsr = inputs['design_tsr']
        #tau_root = inputs['tau_root']
        #tau_75 = inputs['tau_75']
        tf = inputs['tau']
        rotor_diameter = inputs['rotor_diameter']
        rotor_area = inputs['rotor_area']
        #rated_ws = inputs['rated_ws']
        blade_mass_total = inputs['blade_mass_total']


        #print rated_ws
        tau_root = tf
        tau_75 = tf

        ### Convert to absolute values for optimization###
        tsr_ref = 7.6
        design_tsr = tsr_ref * design_tsr
        pitch_ref = 3.5
        pitch = pitch_ref*pitch


        # convert to np array to make it compatible with other np functions

        blade_mass = np.array(blade_mass).reshape(num_nodes, 1)
        blade_ei_flap = np.array(blade_ei_flap).reshape(num_nodes, 1)
        blade_ei_edge = np.array(blade_ei_edge).reshape(num_nodes, 1)
        blade_radius = np.array(blade_radius).reshape(num_nodes, 1)
        blade_chord = np.array(blade_chord).reshape(num_nodes, 1)
        blade_twist = np.array(blade_twist).reshape(num_nodes, 1)
        blade_nfoil = np.array(blade_nfoil).reshape(num_nodes, 1)
        blade_ifoil = np.array(blade_ifoil).reshape(num_airfoils, 1)

        n_sections = num_nodes - 1
        section_length = blade_radius[-1] / n_sections
        #blade_mass_total = np.sum(blade_mass * section_length)

        #rotor_diameter = blade_radius[-1] * 2
        rotor_diameter = np.asscalar(np.array(rotor_diameter))
        #rotor_area = math.pi * (rotor_diameter ** 2) / 4

        t = np.zeros(num_nodes)
        for i in range(num_nodes):
            type = blade_nfoil[i, 0]
            airfoil_geometry = airfoils_coord(type)
            t_u = max(airfoil_geometry[1, 0:200] * blade_chord[i, 0])
            t_l = min(airfoil_geometry[1, 199:-1] * blade_chord[i, 0])
            t[i] = t_u - t_l

        t = t.reshape(num_nodes, 1)
        blade_thickness = t
        s = int(2 * round((num_nodes / 5 + 1) / 2) - 1)
        t = np.convolve(t[:, 0], np.ones((s, 1))[:, 0] / np.sum(s), mode='same') / t[:, 0]
        t[0:((s - 1) / 2 - 1)] = 1
        t[(len(t) - 1) - (s - 1) / 2:-1] = 1
        t = t.reshape(num_nodes, 1)
        blade_thickness = np.multiply(blade_thickness, t)

        # offsets
        i = np.array(np.where(blade_nfoil > 1))
        i = i[0, :]
        x = np.array([blade_radius[0, 0], blade_radius[i[0], 0], blade_radius[-1, 0]])
        cg = np.array([0, 0.2, 0.2])
        sc = np.array([0, -0.03, 0.1])
        blade_cg = np.multiply(np.interp(blade_radius[:, 0], x, cg), blade_chord[:, 0])
        blade_sc = np.multiply(np.interp(blade_radius[:, 0], x, sc), blade_chord[:, 0])
        blade_cg = blade_cg.reshape(num_nodes, 1)
        blade_sc = blade_sc.reshape(num_nodes, 1)

        # Factors for inertia and torsional stiffness per airfoil
        tref = np.array([1.000, 0.700, 0.405, 0.350, 0.300, 0.250, 0.210, 0.180])
        cflap = np.array([0.446, 0.260, 0.147, 0.035, 0.027, 0.014, 0.010, 0.004])
        cedge = np.array([0.034, 0.028, 0.022, 0.019, 0.017, 0.014, 0.015, 0.018])
        ctor = np.array([0.170, 0.136, 0.094, 0.020, 0.021, 0.025, 0.025, 0.022])
        ccgo = np.array([0.010, 0.018, 0.030, 0.060, 0.047, 0.037, 0.045, 0.060])
        pitch_axis = np.array([0.5, 0.45, 0.40, 0.375, 0.375, 0.375, 0.375, 0.375])
        blade_ac = np.nan * np.zeros(num_nodes)
        blade_ac[blade_nfoil[:, 0] == 0] = 0.25
        blade_ac[np.divide(blade_thickness[:, 0], blade_chord[:, 0]) < 0.35] = 0.125
        blade_ac[np.where(np.isnan(blade_ac))] = np.interp(blade_radius[np.where(np.isnan(blade_ac))][:, 0],
                                                           blade_radius[np.where(~np.isnan(blade_ac))][:, 0],
                                                           blade_ac[np.where(~np.isnan(blade_ac))])
        blade_ac = blade_ac.reshape(num_nodes,1)

        tref_new = tref[::-1]
        cflap_new = cflap[::-1]
        cedge_new = cedge[::-1]
        ctor_new = ctor[::-1]
        ccgo_new = ccgo[::-1]
        pitch_axis_new = pitch_axis[::-1]
        ratio = blade_thickness[:, 0] / blade_chord[:, 0]

        a = pchip(tref_new, ccgo_new)(ratio[::-1])
        b = pchip(tref_new, cflap_new)(ratio[::-1])
        c = pchip(tref_new, cedge_new)(ratio[::-1])
        d = pchip(tref_new, ctor_new)(ratio[::-1])
        e = pchip(tref_new, pitch_axis_new)(ratio[::-1])
        a = a[::-1]
        b = b[::-1]
        c = c[::-1]
        d = d[::-1]
        e = e[::-1]
        a = a.reshape(num_nodes, 1)
        b = b.reshape(num_nodes, 1)
        c = c.reshape(num_nodes, 1)
        d = d.reshape(num_nodes, 1)
        e = e.reshape(num_nodes, 1)
        blade_eo = a * blade_chord
        blade_flap_iner = b * blade_mass * blade_thickness ** 2
        # blade_edge_iner=c*blade_mass*blade_chord[:,0] ** 2
        blade_edge_iner = c * blade_mass * blade_chord ** 2
        blade_GJ = d * (blade_ei_flap + blade_ei_edge)
        blade_pitch_axis = e

        # Blade structural properties estimated from thickness
        # blade_flap_iner = np.multiply(np.interp(ratio,tref, cflap),blade_mass[:,0], blade_thickness[:,0]**2)
        # blade_edge_iner = np.multiply(np.interp(ratio, tref, cedge), blade_mass[:,0], blade_chord[:,0] ** 2)
        # blade_GJ = np.multiply(np.interp(ratio, tref, ctor), (blade_ei_flap+ blade_ei_edge))
        blade_EA = 1.3 * 10 ** 7 * blade_mass
        # blade_pitch_axis = np.interp(blade_thickness[:,0]/blade_chord[:,0],tref, pitch_axis)

        # Find fine pitch angle and then subtract that from blade twist angle to get the first point to zero
        #fine_pitch = blade_twist[-1]
        #blade_twist = blade_twist - fine_pitch
        #fine_pitch = np.asscalar(np.array(fine_pitch))  # convert to scalar
        pitch = np.asscalar(np.array(pitch))  # convert to scalar

        '''
        scipy.io.savemat('Matlab_scripts\main_variables.mat', dict(Blade_Chord=blade_chord,
                                                                   Blade_Twist=blade_twist))
        scipy.io.savemat('Matlab_scripts\other_variables.mat', dict(design_tsr=design_tsr,
                                                                    pitch=pitch, tau_root=tau_root,
                                                                    tau_75=tau_75))'''



        '''
        Check if new values are different from previous function call values.
        If yes, only then proceed with linearization and FAST call : only for SLSQP
        

        other_variables = scipy.io.loadmat('Matlab_scripts\other_variables.mat')
        tsr_pre = other_variables['design_tsr']
        pitch_pre = other_variables['pitch']
        tau_root_pre = other_variables['tau_root']
        tau_75_pre = other_variables['tau_75']

        main_variables = scipy.io.loadmat('Matlab_scripts\main_variables.mat')
        Blade_pre_chord = main_variables['Blade_Chord']
        Blade_pre_twist = main_variables['Blade_Twist']

        diff_chord = np.subtract(blade_chord,Blade_pre_chord)
        diff_twist = np.subtract(blade_twist, Blade_pre_twist)
        diff_tsr = abs(design_tsr - tsr_pre)
        diff_pitch = abs(pitch - pitch_pre)
        diff_tau_root = abs(tau_root - tau_root_pre)
        diff_tau_75 = abs(tau_75 - tau_75_pre)

        diff_chord = max(abs(diff_chord))
        diff_twist = max(abs(diff_twist))

        diff = [diff_chord, diff_twist, diff_tsr, diff_pitch, diff_tau_root, diff_tau_75]

        scipy.io.savemat('Matlab_scripts\main_variables.mat', dict(Blade_Chord=blade_chord,
                                                                   Blade_Twist=blade_twist))
        scipy.io.savemat('Matlab_scripts\other_variables.mat', dict(design_tsr=design_tsr,
                                                                    pitch=pitch, tau_root=tau_root,
                                                                    tau_75=tau_75))
        max_diff = max(diff)
        print 'Maximum difference:',max_diff

 

        if max_diff > 1e-6:'''





        eng2 = matlab.engine.start_matlab("-desktop")
        dir = os.getcwd() + r"\Matlab_scripts"
        eng2.cd(dir, nargout=0)
        dir2 = dir + r"\subfunctions"
        eng2.addpath(dir2, nargout=0)


        scipy.io.savemat('Matlab_scripts\Blade.mat',
                         dict(Blade_Mass=blade_mass, Blade_EIflap=blade_ei_flap, Blade_EIedge=blade_ei_edge,
                              Blade_Radius=blade_radius, Blade_Chord=blade_chord, Blade_Twist=blade_twist,
                              Blade_PitchAxis=blade_pitch_axis, Blade_NFoil=blade_nfoil, Blade_IFoil=blade_ifoil,
                              Blade_Cone=blade_cone, Blade_Number=blade_number, Blade_Thickness=blade_thickness,
                              Blade_cg=blade_cg, Blade_sc=blade_sc, Blade_ac=blade_ac, Blade_eo=blade_eo,
                              Blade_FlapIner=blade_flap_iner, Blade_EdgeIner=blade_edge_iner,
                              Blade_GJ=blade_GJ, Blade_EA=blade_EA))

        # Generate Airfoil.mat

        # airfoil_name = np.array(['Cylinder 1', 'Cylinder 2', 'DU 99-W-405', 'DU 99-W-350', 'DU 97-W-300', 'DU 91-W2-250', 'DU 93-W-210', 'NACA 64-618'])
        # airfoil_name = ('Cylinder 1', 'Cylinder 2', 'DU 99-W-405', 'DU 99-W-350', 'DU 97-W-300', 'DU 91-W2-250', 'DU 93-W-210', 'NACA 64-618')
        # airfoil_name.shape = (8, 1)
        # names used in the MATLAB script

        # get geometry
        airfoil_geometry_cyl1 = airfoils_coord(0)
        airfoil_geometry_cyl2 = airfoils_coord(1)
        airfoil_geometry_du405 = airfoils_coord(2)
        airfoil_geometry_du350 = airfoils_coord(3)
        airfoil_geometry_du300 = airfoils_coord(4)
        airfoil_geometry_du250 = airfoils_coord(5)
        airfoil_geometry_du210 = airfoils_coord(6)
        airfoil_geometry_naca = airfoils_coord(7)

        # get alpha,cl,cd and cm

        airfoil_cyl1 = ReadAirfoil(0)
        airfoil_cyl2 = ReadAirfoil(1)
        airfoil_du405 = ReadAirfoil(2)
        airfoil_du350 = ReadAirfoil(3)
        airfoil_du300 = ReadAirfoil(4)
        airfoil_du250 = ReadAirfoil(5)
        airfoil_du210 = ReadAirfoil(6)
        airfoil_naca = ReadAirfoil(7)

        len_cyl1 = len(airfoil_cyl1['Cl'])
        len_cyl2 = len(airfoil_cyl2['Cl'])
        len_du405 = len(airfoil_du405['Cl'])
        len_du350 = len(airfoil_du350['Cl'])
        len_du300 = len(airfoil_du300['Cl'])
        len_du250 = len(airfoil_du250['Cl'])
        len_du210 = len(airfoil_du210['Cl'])
        len_naca = len(airfoil_naca['Cl'])

        cyl1_alpha = np.array(airfoil_cyl1['Alpha']).reshape(len_cyl1, 1)
        cyl2_alpha = np.array(airfoil_cyl2['Alpha']).reshape(len_cyl2, 1)
        du405_alpha = np.array(airfoil_du405['Alpha']).reshape(len_du405, 1)
        du350_alpha = np.array(airfoil_du350['Alpha']).reshape(len_du350, 1)
        du300_alpha = np.array(airfoil_du300['Alpha']).reshape(len_du300, 1)
        du250_alpha = np.array(airfoil_du250['Alpha']).reshape(len_du250, 1)
        du210_alpha = np.array(airfoil_du210['Alpha']).reshape(len_du210, 1)
        naca_alpha = np.array(airfoil_naca['Alpha']).reshape(len_naca, 1)

        cyl1_cl = np.array(airfoil_cyl1['Cl']).reshape(len_cyl1, 1)
        cyl2_cl = np.array(airfoil_cyl2['Cl']).reshape(len_cyl2, 1)
        du405_cl = np.array(airfoil_du405['Cl']).reshape(len_du405, 1)
        du350_cl = np.array(airfoil_du350['Cl']).reshape(len_du350, 1)
        du300_cl = np.array(airfoil_du300['Cl']).reshape(len_du300, 1)
        du250_cl = np.array(airfoil_du250['Cl']).reshape(len_du250, 1)
        du210_cl = np.array(airfoil_du210['Cl']).reshape(len_du210, 1)
        naca_cl = np.array(airfoil_naca['Cl']).reshape(len_naca, 1)

        cyl1_cd = np.array(airfoil_cyl1['Cd']).reshape(len_cyl1, 1)
        cyl2_cd = np.array(airfoil_cyl2['Cd']).reshape(len_cyl2, 1)
        du405_cd = np.array(airfoil_du405['Cd']).reshape(len_du405, 1)
        du350_cd = np.array(airfoil_du350['Cd']).reshape(len_du350, 1)
        du300_cd = np.array(airfoil_du300['Cd']).reshape(len_du300, 1)
        du250_cd = np.array(airfoil_du250['Cd']).reshape(len_du250, 1)
        du210_cd = np.array(airfoil_du210['Cd']).reshape(len_du210, 1)
        naca_cd = np.array(airfoil_naca['Cd']).reshape(len_naca, 1)

        cyl1_cm = np.array(airfoil_cyl1['Cm']).reshape(len_cyl1, 1)
        cyl2_cm = np.array(airfoil_cyl2['Cm']).reshape(len_cyl2, 1)
        du405_cm = np.array(airfoil_du405['Cm']).reshape(len_du405, 1)
        du350_cm = np.array(airfoil_du350['Cm']).reshape(len_du350, 1)
        du300_cm = np.array(airfoil_du300['Cm']).reshape(len_du300, 1)
        du250_cm = np.array(airfoil_du250['Cm']).reshape(len_du250, 1)
        du210_cm = np.array(airfoil_du210['Cm']).reshape(len_du210, 1)
        naca_cm = np.array(airfoil_naca['Cm']).reshape(len_naca, 1)

        # CnSlope, stall angles and critCn

        airfoil_cnslope = np.array([0, 0, 7.48880, 7.18380, 7.33260, 6.44620, 6.20470, 6.00310]).reshape(num_airfoils,
                                                                                                         1)
        airfoil_stallang1 = np.array([0, 0, 9, 11.50, 9, 8.50, 8, 9]).reshape(num_airfoils, 1)
        airfoil_stallang2 = np.array([0, 0, -9, -11.50, -9, -8.50, -8, -9]).reshape(num_airfoils, 1)
        airfoil_critcn1 = np.array([0, 0, 1.3519, 1.6717, 1.4490, 1.4336, 1.4144, 1.4073]).reshape(num_airfoils, 1)
        airfoil_critcn2 = np.array([0, 0, -0.3226, -0.3075, -0.6138, -0.6873, -0.5324, -0.7945]).reshape(num_airfoils,
                                                                                                         1)

        scipy.io.savemat('Matlab_scripts\Airfoil.mat', dict(Airfoil_Geometry1=airfoil_geometry_cyl1,
                                             Airfoil_Geometry2=airfoil_geometry_cyl2,
                                             Airfoil_Geometry3=airfoil_geometry_du405,
                                             Airfoil_Geometry4=airfoil_geometry_du350,
                                             Airfoil_Geometry5=airfoil_geometry_du300,
                                             Airfoil_Geometry6=airfoil_geometry_du250,
                                             Airfoil_Geometry7=airfoil_geometry_du210,
                                             Airfoil_Geometry8=airfoil_geometry_naca, Airfoil_Alpha1=cyl1_alpha,
                                             Airfoil_Alpha2=cyl2_alpha,
                                             Airfoil_Alpha3=du405_alpha, Airfoil_Alpha4=du350_alpha,
                                             Airfoil_Alpha5=du300_alpha,
                                             Airfoil_Alpha6=du250_alpha, Airfoil_Alpha7=du210_alpha,
                                             Airfoil_Alpha8=naca_alpha,
                                             Airfoil_Cl1=cyl1_cl, Airfoil_Cl2=cyl2_cl, Airfoil_Cl3=du405_cl,
                                             Airfoil_Cl4=du350_cl,
                                             Airfoil_Cl5=du300_cl, Airfoil_Cl6=du250_cl, Airfoil_Cl7=du210_cl,
                                             Airfoil_Cl8=naca_cl,
                                             Airfoil_Cd1=cyl1_cd, Airfoil_Cd2=cyl2_cd, Airfoil_Cd3=du405_cd,
                                             Airfoil_Cd4=du350_cd,
                                             Airfoil_Cd5=du300_cd, Airfoil_Cd6=du250_cd, Airfoil_Cd7=du210_cd,
                                             Airfoil_Cd8=naca_cd,
                                             Airfoil_Cm1=cyl1_cm, Airfoil_Cm2=cyl2_cm, Airfoil_Cm3=du405_cm,
                                             Airfoil_Cm4=du350_cm,
                                             Airfoil_Cm5=du300_cm, Airfoil_Cm6=du250_cm, Airfoil_Cm7=du210_cm,
                                             Airfoil_Cm8=naca_cm,
                                             Airfoil_CnSlope=airfoil_cnslope, Airfoil_StallAngle1=airfoil_stallang1,
                                             Airfoil_StallAngle2=airfoil_stallang2,
                                             Airfoil_CritCn1=airfoil_critcn1, Airfoil_CritCn2=airfoil_critcn2))

        # tower inputs
        tower_hh = inputs['tower_hh']
        tower_bthickness = inputs['tower_bthickness']
        tower_tthickness = inputs['tower_tthickness']
        tower_height = np.zeros(num_tnodes)
        #tower_height = np.array(inputs['tower_height']).reshape(num_tnodes, 1)
        n_sections_tower = num_tnodes-1
        length_tower_segment = tower_hh/n_sections_tower
        for i in range(1,num_tnodes):
            tower_height[i] = tower_height[i-1] + length_tower_segment

        tower_height = np.array(tower_height).reshape(num_tnodes, 1)
        tower_extramass = np.array(inputs['tower_extramass']).reshape(num_tnodes, 1)

        tower_top_dia = inputs['tower_top_dia']
        tower_base_dia = inputs['tower_base_dia']
        tower_diameter = np.array([np.linspace(tower_base_dia, tower_top_dia, len(tower_height))]).reshape(
            num_tnodes, 1)
        #tower_diameter = np.array(inputs['tower_diameter']).reshape(num_tnodes, 1)
        tower_wallthickness = np.array([np.linspace(tower_bthickness, tower_tthickness, len(tower_height))]).reshape(
            num_tnodes, 1)  # transpose
        tower_mass = tower_density * math.pi * (
                    tower_diameter ** 2 - (tower_diameter - 2 * tower_wallthickness) ** 2) / 4 + tower_extramass
        tower_ei = tower_ym * math.pi / 64 * (tower_diameter ** 4 - (tower_diameter - 2 * tower_wallthickness) ** 4)
        tower_gj = tower_sm * math.pi / 32 * (tower_diameter ** 4 - (tower_diameter - 2 * tower_wallthickness) ** 4)
        tower_ea = tower_ym * math.pi * tower_diameter * tower_wallthickness
        tower_iner = 0.5 * tower_mass * (tower_diameter / 2 - tower_wallthickness) ** 2

        scipy.io.savemat('Matlab_scripts\Tower.mat', dict(Tower_HubHeight=tower_hh, Tower_BottomThickness=tower_bthickness,
                                           Tower_TopThickness=tower_tthickness,
                                           Tower_Height=tower_height, Tower_ExtraMass=tower_extramass,
                                           Tower_Diameter=tower_diameter,
                                           Tower_WallThickness=tower_wallthickness, Tower_Mass=tower_mass,
                                           Tower_EI=tower_ei,
                                           Tower_GJ=tower_gj, Tower_EA=tower_ea, Tower_Iner=tower_iner))

        # Nacelle inputs

        nacelle_hub_length = inputs['nacelle_hub_length']
        nacelle_hub_mass = inputs['nacelle_hub_mass']
        nacelle_hub_overhang = inputs['nacelle_hub_overhang']
        nacelle_hub_type = inputs['nacelle_hub_type']
        nacelle_hub_shafttilt = inputs['nacelle_hub_shafttilt']
        nacelle_housing_type = inputs['nacelle_housing_type']
        nacelle_housing_diameter = inputs['nacelle_housing_diameter']
        nacelle_housing_length = inputs['nacelle_housing_length']
        nacelle_housing_mass = inputs['nacelle_housing_mass']

        scipy.io.savemat('Matlab_scripts\Nacelle.mat', dict(Nacelle_Hub_Length=nacelle_hub_length, Nacelle_Hub_Mass=nacelle_hub_mass,
                                             Nacelle_Hub_Overhang=nacelle_hub_overhang,
                                             Nacelle_Hub_Type=nacelle_hub_type,
                                             Nacelle_Hub_ShaftTilt=nacelle_hub_shafttilt,
                                             Nacelle_Housing_Type=nacelle_housing_type,
                                             Nacelle_Housing_Diameter=nacelle_housing_diameter,
                                             Nacelle_Housing_Length=nacelle_housing_length,
                                             Nacelle_Housing_Mass=nacelle_housing_mass))

        # DriveTrain and Controls inputs
        rated_power = inputs['rated_power']  # in KW
        rated_power = np.asscalar(np.array(rated_power))

        # drivetrain_gen_hssinertia=inputs['drivetrain_gss_hssinertia']
        drivetrain_gen_eff = inputs['drivetrain_gen_eff']
        drivetrain_gear_ratio = inputs['drivetrain_gear_ratio']
        drivetrain_gear_eff = inputs['drivetrain_gear_eff']

        # get Cp, tsr by generating steady state curve at fine pitch angle


        #output = eng2.GenerateSteadyOp(fine_pitch, nargout=2)
        #Cp = output[0]
        #tsr = output[1]



        #design_tsr = np.asscalar(np.array(design_tsr))  # convert to scalar
        #output = eng2.GenerateSteadyOp_Cp(pitch, design_tsr, nargout=1)
        #Cp = output

        Cp = inputs['Cp']




        rated_ws = (2 * rated_power*1000/drivetrain_gen_eff/ (Cp * rho_air * rotor_area)) ** (1.0 / 3.0)
        rated_ws = np.asscalar(np.array(rated_ws))  # convert to scalar


        print 'Cp:',Cp
        print 'TSR:',design_tsr
        print 'Rated wind speed:',rated_ws
        print 'Pitch:', pitch


        control_windspeed_cutin = 4.0
        control_windspeed_cutout = 25.0

        cutin_omega_lss = design_tsr * control_windspeed_cutin / blade_radius[-1]  # in radian/s

        # get cut in rpm from frequency analysis

        #control_dt = 0.008
        control_dt = 0.0125
        control_lpfcutoff = 3.0
        control_brake_deploytime = 0.6
        control_brake_torque = 28116
        control_brake_delay = 1.5

        control_foreaft_gain = 0.1
        control_foreaft_maxpitchamplitude = 5.0

        ##### Design methodology and rpm range assumed to be same as NREL ####

        rated_omega_lss = design_tsr * rated_ws / blade_radius[-1]  # in radian/s
        rated_omega_lss_rpm = rated_omega_lss * 60 / (2 * math.pi)  # in rpm
        rated_omega_lss_rpm = np.asscalar(np.array(rated_omega_lss_rpm))
        rated_genspeed = rated_omega_lss_rpm * drivetrain_gear_ratio  # in rpm
        control_omega_c = rated_genspeed * 0.9276

        opt_mode_gain = 0.5 * 1.225 * Cp * math.pi * drivetrain_gear_eff * blade_radius[-1] ** 5 / (design_tsr ** 3) / (
                    drivetrain_gear_ratio ** 3)
        opt_mode_gain_rpm = opt_mode_gain * 4 * math.pi ** 2 / 60 / 60  # converting to /rpm2
        mech_power = rated_power*1000 / drivetrain_gen_eff  # in W
        control_demanded_gen_torque = mech_power / (2 * math.pi * control_omega_c / 60)

        gen_slip = 0.1  # generator slip expressed in percentage
        omega_b3 = control_omega_c * (1 - gen_slip)  # point at which the line passing through c and b2 meets x axis
        slope = control_demanded_gen_torque / (control_omega_c - omega_b3)
        constant = -slope * omega_b3

        # Equating y=k*omega^2 and Y=mx+c gives a quadratic equation that needs to be solved
        # Coefficients a,b and c are given

        a = opt_mode_gain_rpm
        b = -slope
        c = -constant
        d = math.sqrt(b ** 2 - 4 * a * c)
        root1 = (-b + d) / 2 / a
        root2 = (-b - d) / 2 / a
        control_omega_b2 = root2
        control_omega_b = 0.75 * control_omega_b2  # range taken from NREL 5 MW turbine, check for resonance later
        control_omega_a = 0.77 * control_omega_b  # range taken from NREL 5 MW turbine, check for resonance later

        # control_omega_a=cutin_omega_lss*60*drivetrain_gear_ratio/(2*math.pi) #all in rpm
        # control_omega_b=1.3*control_omega_a  #30% higher

        # control_omega_b2=0.99*control_omega_c

        control_torque_limit = 1.1 * control_demanded_gen_torque
        control_torque_slew = 20000.0
        control_torque_min = 200.0
        control_torque_scheduled = 0.0
        control_torque_kp = -3500 * np.ones(12)
        control_torque_kp = control_torque_kp.reshape(1, 12)
        control_torque_ti = 0.25 * np.ones(12)
        control_torque_ti = control_torque_ti.reshape(1, 12)

        control_pitch_fine = pitch
        control_pitch_min = -2.0
        control_pitch_max = 90.0
        control_pitch_minrate = -8.0
        control_pitch_maxrate = 8.0
        control_pitch_scheduled = 1.0
        control_pitch_startuppitch = 45.0
        control_pitch_startuppitchrate = 1.0
        control_pitch_startupspeed = 0.25
        control_pitch_kp = -0.003
        control_pitch_ki = -0.001

        # Scaling HSS inertia from the reference turbine
        drivetrain_gen_hssinertia = 534.116 * (rated_power*1000 / (5 * 10 ** 6)) ** (5 / 3) * (
                    12.1 * 97 / control_omega_c) ** 2
        drivetrain_lssinertia = drivetrain_gen_hssinertia * drivetrain_gear_ratio ** 2

        scipy.io.savemat('Matlab_scripts\Drivetrain.mat', dict(Drivetrain_Generator_Efficiency=drivetrain_gen_eff,
                                                Drivetrain_Generator_HSSInertia=drivetrain_gen_hssinertia,
                                                Drivetrain_Gearbox_Ratio=drivetrain_gear_ratio,
                                                Drivetrain_Gearbox_eff=drivetrain_gear_eff,
                                                Drivetrain_LSSInertia=drivetrain_lssinertia))

        scipy.io.savemat('Matlab_scripts\Control.mat', dict(Control_WindSpeed_Cutin=control_windspeed_cutin,
                                             Control_WindSpeed_Cutout=control_windspeed_cutout,
                                             Control_DT=control_dt, Control_LPFCutOff=control_lpfcutoff,
                                             Control_Brake_Deploytime=control_brake_deploytime,
                                             Control_Brake_Torque=control_brake_torque,
                                             Control_Brake_Delay=control_brake_delay,
                                             Control_ForeAft_Gain=control_foreaft_gain,
                                             Control_ForeAft_MaxPitchAmplitude=control_foreaft_maxpitchamplitude,
                                             Control_Torque_Demanded=control_demanded_gen_torque,
                                             Control_Torque_Limit=control_torque_limit,
                                             Control_Torque_Slewrate=control_torque_slew,
                                             Control_Torque_OptGain=opt_mode_gain,
                                             Control_Torque_SpeedA=control_omega_a,
                                             Control_Torque_SpeedB=control_omega_b,
                                             Control_Torque_SpeedB2=control_omega_b2,
                                             Control_Torque_SpeedC=control_omega_c,
                                             Control_Torque_Min=control_torque_min,
                                             Control_Torque_Scheduled=control_torque_scheduled,
                                             Control_Torque_Kp=control_torque_kp,
                                             Control_Torque_Ti=control_torque_ti,
                                             Control_Pitch_Fine=control_pitch_fine,
                                             Control_Pitch_Min=control_pitch_min,
                                             Control_Pitch_Max=control_pitch_max,
                                             Control_Pitch_Minrate=control_pitch_minrate,
                                             Control_Pitch_Maxrate=control_pitch_maxrate,
                                             Control_Pitch_StartupPitch=control_pitch_startuppitch,
                                             Control_Pitch_StartupPitchRate=control_pitch_startuppitchrate,
                                             Control_Pitch_StartupSpeed=control_pitch_startupspeed,
                                             Control_Pitch_Scheduled=control_pitch_scheduled,
                                             Control_Pitch_Kp=control_pitch_kp,
                                             Control_Pitch_Ki=control_pitch_ki))



        # linearize and find out scheduled pitch angles
        # this script performs the linearization from rated uptil cutoff wind speed and
        # determines gain scheduled kp and ki analytically
        gains = eng2.Control_gains_new(rated_ws, rated_omega_lss_rpm, nargout=2)

        Linearization_end=time.time()-t_start
        print 'FAST run time before Load cases (s):', Linearization_end
        '''
        #Certification settings: User decides the load case

        dlc_type='ultimate' #use either 'fatigue'or 'ultimate'
        wind_type='NTM' #use 'steady', 'stepped', 'NWP', 'NTM', 'EWM1, 'EWM50', 'EWS', 'ETM', 'EOG', 'EDC', 'ECG'
        operating_mode='normal' #use 'normal', 'grid loss', 'startup', 'normal shutdown', 'emergency shutdown', 'idling', 'parked'

        load_case(dlc_type, wind_type, operating_mode, rated_ws)



        Load case selector creates the certification mat file for a particular critical load case that was predetermined
        Load cases that were selected:
        Based on max Tip Deflection 
            -DLC 1.3 at 11.4 m/s

        Based on max Oop moment
            -DLC 1.3 at 11.4 m/s

        Based on max Ip moment
            -DLC 3.3 at 4m/s

        Based on max Flapwise moment
            -DLC 3.3 at 4m/s

        Based on max Edgewise moment
            -DLC 2.1 at 11.4 m/s

        DLC 1.2 for FATIGUE: 4-26 m/s
        
        '''

        '''
        rotor_diameter = 126
        rated_ws = 11.4'''

        # run load case 1.3
        load_case_selector(1.3, rotor_diameter, rated_ws)

        ret = eng2.Certification(nargout=0)




        '''
        #run load case 2.1
        load_case_selector(2.1,rotor_diameter, rated_ws)
        ret= eng2.Certification(nargout=0)
        ret = eng2.Post_processing(nargout=0)
        results = scipy.io.loadmat('Matlab_scripts\Ultimate_Results.mat')
        deflection_21 = results['Deflection']
        Stress_root = results['Stress_root']
        Stress_span = np.array(results['Stress_span']).reshape(5,4)

        Stress_flapwise_skin_loc1 = Stress_span[0,0]
        Stress_flapwise_skin_loc2 = Stress_span[1,0]
        Stress_flapwise_skin_loc3 = Stress_span[2,0]
        Stress_flapwise_skin_loc4 = Stress_span[3,0]
        Stress_flapwise_skin_loc5 = Stress_span[4,0]

        Stress_flapwise_skin = np.array([Stress_flapwise_skin_loc1, Stress_flapwise_skin_loc2, Stress_flapwise_skin_loc3,
                                         Stress_flapwise_skin_loc4, Stress_flapwise_skin_loc5])


        
        #Stresses in Pa and Tip deflection (m)
        print 'DLC 2.1, Root stress in MPa:', Stress_root
        print 'DLC 2.1, Deflection in m:', deflection_21
        print 'DLC 2.1, Flapwise stresses in the skin in MPa:', Stress_flapwise_skin


        #run load case 3.3
        load_case_selector(3.3,rotor_diameter, rated_ws)
        ret= eng2.Certification(nargout=0)
        ret=eng2.Post_processing(nargout=0)
        results = scipy.io.loadmat('Matlab_scripts\Ultimate_Results.mat')
        deflection_33 = results['Deflection']
        Stress_root = results['Stress_root']
        Stress_span = np.array(results['Stress_span']).reshape(5,4)

        Stress_flapwise_skin_loc1 = Stress_span[0,0]
        Stress_flapwise_skin_loc2 = Stress_span[1,0]
        Stress_flapwise_skin_loc3 = Stress_span[2,0]
        Stress_flapwise_skin_loc4 = Stress_span[3,0]
        Stress_flapwise_skin_loc5 = Stress_span[4,0]

        Stress_flapwise_skin = np.array([Stress_flapwise_skin_loc1, Stress_flapwise_skin_loc2, Stress_flapwise_skin_loc3,
                                         Stress_flapwise_skin_loc4, Stress_flapwise_skin_loc5])


        #Stresses in Pa and Tip deflection (m)
        print 'DLC 3.3, Root stress in m:', Stress_root
        print 'DLC 3.3, Deflection in MPa:', deflection_33
        print 'DLC 3.3, Flapwise stresses in the skin in MPa:', Stress_flapwise_skin'''

        ret = eng2.Post_processing_60(nargout=0)

        eng2.quit()


        results = scipy.io.loadmat('Matlab_scripts\Ultimate_Results.mat')
        deflection_13 = np.asscalar(results['Deflection'])
        Stress_root = np.asscalar(results['Stress_root'])
        Stress_span = np.array(results['Stress_span']).reshape(5,4)

        Stress_flapwise_skin_loc1 = Stress_span[0,0]
        Stress_flapwise_skin_loc2 = Stress_span[1,0]
        Stress_flapwise_skin_loc3 = Stress_span[2,0]
        Stress_flapwise_skin_loc4 = Stress_span[3,0]
        Stress_flapwise_skin_loc5 = Stress_span[4,0]

        Stress_flapwise_skin = np.array([Stress_flapwise_skin_loc1, Stress_flapwise_skin_loc2, Stress_flapwise_skin_loc3,
                                         Stress_flapwise_skin_loc4, Stress_flapwise_skin_loc5])


        Stress_flapwise_spar_loc1 = Stress_span[0,1]
        Stress_flapwise_spar_loc2 = Stress_span[1,1]
        Stress_flapwise_spar_loc3 = Stress_span[2,1]
        Stress_flapwise_spar_loc4 = Stress_span[3,1]
        Stress_flapwise_spar_loc5 = Stress_span[4,1]

        Stress_flapwise_spar = np.array([Stress_flapwise_spar_loc1, Stress_flapwise_spar_loc2, Stress_flapwise_spar_loc3,
                                         Stress_flapwise_spar_loc4, Stress_flapwise_spar_loc5])


        Stress_edgewise_skin_loc1 = Stress_span[0,2]
        Stress_edgewise_skin_loc2 = Stress_span[1,2]
        Stress_edgewise_skin_loc3 = Stress_span[2,2]
        Stress_edgewise_skin_loc4 = Stress_span[3,2]
        Stress_edgewise_skin_loc5 = Stress_span[4,2]

        Stress_edgewise_skin = np.array([Stress_edgewise_skin_loc1, Stress_edgewise_skin_loc2, Stress_edgewise_skin_loc3,
                                         Stress_edgewise_skin_loc4, Stress_edgewise_skin_loc5])

        Stress_edgewise_te_reinf_loc1 = Stress_span[0, 3]
        Stress_edgewise_te_reinf_loc2 = Stress_span[1, 3]
        Stress_edgewise_te_reinf_loc3 = Stress_span[2, 3]
        Stress_edgewise_te_reinf_loc4 = Stress_span[3, 3]
        Stress_edgewise_te_reinf_loc5 = Stress_span[4, 3]

        Stress_edgewise_te_reinf = np.array([Stress_edgewise_te_reinf_loc1, Stress_edgewise_te_reinf_loc2, Stress_edgewise_te_reinf_loc3,
                                             Stress_edgewise_te_reinf_loc4, Stress_edgewise_te_reinf_loc5])

        max_flapwise_skin = max(Stress_flapwise_skin)
        max_flapwise_spar = max(Stress_flapwise_spar)
        max_edgewise_skin = max(Stress_edgewise_skin)
        max_edgewise_te_reinf = max(Stress_edgewise_te_reinf)

        max_stress_skin = max(max_edgewise_skin, max_flapwise_skin, Stress_root)
        max_stress_te_reinf = max_edgewise_te_reinf
        max_stress_spar = max_flapwise_spar

        '''
        if blade_mass_total < 9000.0:
            deflection_13 = 15.0
            max_stress_spar = 1200.0
            max_stress_skin = 800.0
            max_stress_te_reinf = 1100.0

        
        if blade_mass_total < 10500.0:
            deflection_13 = 15.0
            max_stress_spar = 1500.0
            max_stress_skin = 1000.0
            max_stress_te_reinf = 1400.0'''




        # Stresses in Pa and Tip deflection (m)
        #print 'DLC 1.3, Root stress in MPa:', Stress_root
        print 'DLC 1.3, Deflection in m:', deflection_13
        print 'DLC 1.3, Skin sress (MPa):', max_stress_skin
        print 'DLC 1.3, Spar stress(MPa):', max_stress_spar
        print 'DLC 1.3, Te_Reinf stress (MPa):', max_stress_te_reinf

        #print 'DLC 1.3, Edgewise stresses in the skin (MPa):', Stress_edgewise_skin
        #print 'DLC 1.3, Edgewise stresses in the TE Reinf (MPa):', Stress_edgewise_te_reinf




        #### Run FATIGUE analysis and obtain Fatigue damage and damage equivalent load###
        '''
        load_case_selector('Fatigue',rotor_diameter, rated_ws)
        ret= eng2.Certification(nargout=0)'''

        elapsed_run=time.time()-t_start
        print 'FAST run time elapsed (s):',elapsed_run


        '''
        #variables_1 = scipy.io.loadmat('Matlab_scripts\DLC_U=6.00.mat')
        #ret = eng2.Post_processing(nargout=0)
        Stress_ts_6 = scipy.io.loadmat('Matlab_scripts\Fatigue_6.mat')


        #variables_2 = scipy.io.loadmat('Matlab_scripts\DLC_U=8.00.mat')
        #ret = eng2.Post_processing(nargout=0)
        Stress_ts_8 = scipy.io.loadmat('Matlab_scripts\Fatigue_8.mat')


        #variables_3 = scipy.io.loadmat('Matlab_scripts\DLC_U=12.00.mat')
        #ret = eng2.Post_processing(nargout=0)
        Stress_ts_12 = scipy.io.loadmat('Matlab_scripts\Fatigue_12.mat')


        #variables_4 = scipy.io.loadmat('Matlab_scripts\DLC_U=16.00.mat')
        #ret = eng2.Post_processing(nargout=0)
        Stress_ts_16 = scipy.io.loadmat('Matlab_scripts\Fatigue_16.mat')


        #variables_5 = scipy.io.loadmat('Matlab_scripts\DLC_U=20.00.mat')
        #ret = eng2.Post_processing(nargout=0)
        Stress_ts_20 = scipy.io.loadmat('Matlab_scripts\Fatigue_20.mat')


        #variables_6 = scipy.io.loadmat('Matlab_scripts\DLC_U=23.50.mat')
        #ret = eng2.Post_processing(nargout=0)
        Stress_ts_23_5 = scipy.io.loadmat('Matlab_scripts\Fatigue_23.50.mat')






        Stress_ts=np.vstack([Stress_ts_6, Stress_ts_8, Stress_ts_12, Stress_ts_16, Stress_ts_20, Stress_ts_23_5])
        scipy.io.savemat('Matlab_scripts\Stress.mat', dict(Stress_ts=Stress_ts))
        Results = eng2.Fatigue_calculator(nargout=2)
        Fatigue=Results[0]
        DEL=Results[1] #Damage equivalent load
        print Fatigue
        elapsed=time.time()-t_start
        print 'FAST time elapsed (s):',elapsed'''

        outputs['Tip_Deflection'] = deflection_13
        #outputs['Flapwise_Stress_Skin'] = max_flapwise_skin
        outputs['Max_Stress_Spar'] = max_stress_spar
        outputs['Max_Stress_Skin'] = max_stress_skin
        outputs['Max_Stress_Te_Reinf'] = max_stress_te_reinf
        #outputs['Stress_Root'] = Stress_root


#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":
    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'blade_number': 3.0, 'blade_ifoil': [0, 1, 2, 3, 4, 5, 6, 7], 'blade_cone': 2.5,
              'blade_mass': [678.9, 639, 423.5, 342.64, 314.66, 260, 208, 154.67, 103.89, 72.67],
              'blade_ei_flap': [1.8 * 10 ** 10, 1.2 * 10 ** 10, 4.407 * 10 ** 9, 2.15 * 10 ** 9, 1.38 * 10 ** 9,
                                6.37 * 10 ** 8, 2.65 * 10 ** 8,
                                1.07 * 10 ** 8, 5.69 * 10 ** 7, 4.09 * 10 ** 6],
              'blade_ei_edge': [1.8 * 10 ** 10, 1.64 * 10 ** 10, 7.23 * 10 ** 9, 4.63 * 10 ** 9, 3.77 * 10 ** 9,
                                2.68 * 10 ** 9,
                                1.67 * 10 ** 9, 1.02 * 10 ** 9, 4.92 * 10 ** 8, 8.81 * 10 ** 7],
              'blade_radius': [1.5, 6.62, 13.03, 19.43, 25.85, 32.25, 38.65, 45.06, 51.47, 63],
              'blade_chord': [3.39, 3.97, 4.60, 4.49, 4.15, 3.75, 3.36, 2.98, 2.59, 0.96],
              'blade_twist': [13.23, 13.23, 12.91, 10.24, 8.41, 6.47, 4.62, 2.94, 1.7, 0],
              'blade_nfoil': [0, 0, 2, 3, 4, 5, 6, 7, 7, 7],

              'tower_hh': 90.0,
              'tower_bthickness': 0.027,
              'tower_tthickness': 0.019,
              'tower_height': [0, 8.76, 17.52, 26.28, 35, 43.8, 52.56, 61.32, 70.08, 78.84, 87.76],
              'tower_extramass': [329.0, 308.0, 287.0, 268.0, 249.0, 230.0, 213.0, 196.0, 179.0, 164.0, 149.0],
              'tower_diameter': [6, 5.78, 5.57, 5.36, 5.15, 4.935, 4.722, 4.509, 4.296, 4.083, 3.87],

              'drivetrain_gen_eff': 0.944,
              'drivetrain_gen_hssinertia': 534.116,
              'drivetrain_gear_ratio': 97.0,
              'drivetrain_gear_eff': 1.0,
              'nacelle_hub_length': 5.0,
              'nacelle_hub_mass': 56780.0,
              'nacelle_hub_overhang': 5.0,
              'nacelle_hub_type': 1.0,
              'nacelle_hub_shafttilt': 5.0,
              'nacelle_housing_type': 1.0,
              'nacelle_housing_diameter': 5.0,
              'nacelle_housing_length': 10.0,
              'nacelle_housing_mass': 240000.0,
              'rated_ws': 11.4,
              'rated_power': 5.0 * 10 ** 6}
    outputs = {}

    model = FAST(num_nodes=10, num_airfoils=8, num_tnodes=11, tower_sm=80.8 * 10 ** 9, tower_ym=210 * 10 ** 9,
                 tower_density=7850, rho_air=1.225)

    model.compute(inputs, outputs)



