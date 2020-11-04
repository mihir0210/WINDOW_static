'''
Read outputs and convert them into values that can be used as constraints
'''

import numpy as np
import pandas as pd
import math
import os

def post_processor(t_bt, t_d, b_ei_flap, b_c,b_m,b_r, a_g, type, moment):
    Time=[]
    RootMEdg1=[]
    RootMEdg2=[]
    RootMEdg3=[]
    RootMFlp1=[]
    RootMFlp2=[]
    RootMFlp3=[]
    RootMOoP1=[]
    RootMOoP2=[]
    RootMOoP3=[]
    RootMIP1=[]
    RootMIP2=[]
    RootMIP3=[]
    OoPDefl1=[]
    OoPDefl2=[]
    OoPDefl3=[]
    TwrBsMxt=[]
    TwrBsMyt=[]
    TwrBsMzt=[]
    RotSpeed=[]


    if type==1 and moment==0:

        dir=os.getcwd()
        relative_name = dir + '\Matlab_scripts\subfunctions\inputfiles\FAST.SFunc.out'
        dataframe = pd.read_csv(relative_name, sep='\t', index_col=False, header=None,
                            names=['Time', 'OoPDefl1', 'OoPDefl2', 'OoPDefl3', 'RootMOoP1', 'RootMOoP2', 'RootMOoP3',
                                   'RootMIP1', 'RootMIP2', 'RootMIP3', 'RootMFlp1', 'RootMFlp2', 'RootMFlp3',
                                   'RootMEdg1', 'RootMEdg2', 'RootMEdg3', 'TwrBsMxt', 'TwrBsMyt', 'TwrBsMzt',
                                'RotSpeed'],
                            usecols=[0, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,36], skiprows=8)

        Time = np.array(dataframe['Time'])
        RootMEdg1 = np.array(dataframe['RootMEdg1'])
        RootMEdg2 = np.array(dataframe['RootMEdg2'])
        RootMEdg3 = np.array(dataframe['RootMEdg3'])
        RootMFlp1 = np.array(dataframe['RootMFlp1'])
        RootMFlp2 = np.array(dataframe['RootMFlp2'])
        RootMFlp3 = np.array(dataframe['RootMFlp3'])
        RootMIP1 = np.array(dataframe['RootMIP1'])
        RootMIP2 = np.array(dataframe['RootMIP2'])
        RootMIP3 = np.array(dataframe['RootMIP3'])
        RootMOoP1 = np.array(dataframe['RootMOoP1'])
        RootMOoP2 = np.array(dataframe['RootMOoP2'])
        RootMOoP3 = np.array(dataframe['RootMOoP3'])
        OoPDefl1 = np.array(dataframe['OoPDefl1'])
        OoPDefl2 = np.array(dataframe['OoPDefl2'])
        OoPDefl3 = np.array(dataframe['OoPDefl3'])
        TwrBsMxt = np.array(dataframe['TwrBsMxt'])  # xt axis along the wind. Side-Side motion
        TwrBsMyt = np.array(dataframe['TwrBsMyt'])  # yt axis perpendicular to wind. Fore-Aft motion
        TwrBsMzt = np.array(dataframe['TwrBsMzt'])  # zt axis along the tower axis
        RotSpeed = np.array(dataframe['RotSpeed'])

        rows = len(RootMEdg1)

        Time = Time.reshape(rows, 1)
        RootMEdg1 = RootMEdg1.reshape(rows, 1)
        RootMEdg2 = RootMEdg2.reshape(rows, 1)
        RootMEdg3 = RootMEdg3.reshape(rows, 1)
        RootMFlp1 = RootMFlp1.reshape(rows, 1)
        RootMFlp2 = RootMFlp2.reshape(rows, 1)
        RootMFlp3 = RootMFlp3.reshape(rows, 1)
        RootMIP1 = RootMIP1.reshape(rows, 1)
        RootMIP2 = RootMIP2.reshape(rows, 1)
        RootMIP3 = RootMIP3.reshape(rows, 1)
        RootMOoP1 = RootMOoP1.reshape(rows, 1)
        RootMOoP2 = RootMOoP2.reshape(rows, 1)
        RootMOoP3 = RootMOoP3.reshape(rows, 1)
        OoPDefl1 = OoPDefl1.reshape(rows, 1)
        OoPDefl2 = OoPDefl2.reshape(rows, 1)
        OoPDefl3 = OoPDefl3.reshape(rows, 1)
        TwrBsMxt = TwrBsMxt.reshape(rows, 1)  # xt axis along the wind. Side-Side motion
        TwrBsMyt = TwrBsMyt.reshape(rows, 1)  # yt axis perpendicular to wind. Fore-Aft motion
        TwrBsMzt = TwrBsMzt.reshape(rows, 1)  # zt axis along the tower axis
        RotSpeed = RotSpeed.reshape(rows,1)

    elif type==2:
        Time = moment['Time']
        RootMEdg1 = moment['RootMEdg1']
        RootMEdg2 = moment['RootMEdg2']
        RootMEdg3 = moment['RootMEdg3']
        RootMFlp1 = moment['RootMFlp1']
        RootMFlp2 = moment['RootMFlp2']
        RootMFlp3 = moment['RootMFlp3']
        RootMIP1 = moment['RootMIP1']
        RootMIP2 = moment['RootMIP2']
        RootMIP3 = moment['RootMIP3']
        RootMOoP1 = moment['RootMOoP1']
        RootMOoP2 = moment['RootMOoP2']
        RootMOoP3 = moment['RootMOoP3']
        OoPDefl1 = moment['OoPDefl1']
        OoPDefl2 = moment['OoPDefl2']
        OoPDefl3 = moment['OoPDefl3']
        TwrBsMxt = moment['TwrBsMxt']  # xt axis along the wind. Side-Side motion
        TwrBsMyt = moment['TwrBsMyt']  # yt axis perpendicular to wind. Fore-Aft motion
        TwrBsMzt = moment['TwrBsMzt']  # zt axis along the tower axis
        RotSpeed = moment['RotSpeed']

    # remove first 60 seconds of the simulation
    t_remove = 60.0
    sampling_time = 0.008

    remove = int(t_remove / sampling_time) - 1

    # Start these arrays from the 7500th element

    Time = Time[remove:]
    RootMEdg1 = RootMEdg1[remove:]
    RootMEdg2 = RootMEdg2[remove:]
    RootMEdg3 = RootMEdg3[remove:]
    RootMFlp1 = RootMFlp1[remove:]
    RootMFlp2 = RootMFlp2[remove:]
    RootMFlp3 = RootMFlp3[remove:]
    RootMIP1 = RootMIP1[remove:]
    RootMIP2 = RootMIP2[remove:]
    RootMIP3 = RootMIP3[remove:]
    RootMOoP1 = RootMOoP1[remove:]
    RootMOoP2 = RootMOoP2[remove:]
    RootMOoP3 = RootMOoP3[remove:]
    OoPDefl1 = OoPDefl1[remove:]
    OoPDefl2 = OoPDefl2[remove:]
    OoPDefl3 = OoPDefl3[remove:]
    TwrBsMxt = TwrBsMxt[remove:]  # axis along the wind. Side-Side motion
    TwrBsMyt = TwrBsMyt[remove:]  # yt axis perpendiculat to wind. Fore-Aft motion
    TwrBsMzt = TwrBsMzt[remove:]  # zt axis along the tower axis
    RotSpeed = RotSpeed[remove:]



    '''Blades : Stiffness properties and calculting stresses at the root'''
    RootMEdg = np.concatenate([RootMEdg1, RootMEdg2, RootMEdg3])
    RootMFlp = np.concatenate([RootMFlp1, RootMFlp2, RootMFlp3])
    RootMIP = np.concatenate([RootMIP1, RootMIP2, RootMIP3])
    RootMOoP = np.concatenate([RootMOoP1, RootMOoP2, RootMOoP3])
    OoPDefl = np.concatenate([OoPDefl1, OoPDefl2, OoPDefl3])
    RotSpeed = np.concatenate([RotSpeed, RotSpeed, RotSpeed])

    # Resultant moments at the root

    resultant_moment_flap_edge = np.sqrt(RootMEdg ** 2 + RootMFlp ** 2)
    resultant_moment_out_in = np.sqrt(RootMOoP ** 2 + RootMIP ** 2)


    max_moment_flap_edge = max(resultant_moment_flap_edge) #in KNm
    max_moment_out_in = max(resultant_moment_out_in) #in KNm

    i=np.argmax(resultant_moment_flap_edge) # Take index of max resultant moment
    i=np.asscalar(i)

    # Max stresses and tip deflection
    root_stiffness = b_ei_flap[0]
    root_chord=b_c[0]
    root_thick2chord=max(a_g[1,:]) # thickness to chord ratio
    y_blade=root_chord*root_thick2chord #max distance from neutral axis
    glass_fibre_Emodulus=7.5e10 #Glass fibre modulus of elasticity
    ### 3.623e10 in Tanuj's report ###
    root_Iarea=root_stiffness/glass_fibre_Emodulus #Area moment of inertia at root using Stifness=EI

    Stress_flap_edge=max_moment_flap_edge*y_blade*1000/root_Iarea/1e6
    Stress_out_in=max_moment_out_in*y_blade*1000/root_Iarea/1e6
    Root_stress=np.double(max([Stress_flap_edge,Stress_out_in])) # Max stress at the root
    Deflection=np.double(max(OoPDefl))

    ### Calculate Bolt stresses ###
    ### 48 bolts with a nominal radius of 36 mm (M36) ###

    bolt_r = 0.036 # bolt radius in m
    n_bolts= 48
    '''
    https://pdfs.semanticscholar.org/e8f0/f5dfe6e0d75de62f1469e38ae180478331ec.pdf pretension of 35 KN
    https://link.springer.com/article/10.1007/s11668-013-9675-4  preload of 265 KN
    '''
    A_bolt = math.pi*bolt_r**2
    F_preload= 265e3# preloading of bolt, in N
    omega=2*math.pi*RotSpeed[i]/60
    F_centrifugal=b_m*b_r*omega**2/48  #per bolt

    Axial_stress_bolt = (F_preload+F_centrifugal/n_bolts)/ A_bolt

    delta=n_bolts*A_bolt/math.pi/root_chord #Assuming thin cylinder approximation n*A=pi*D*delta
    Section_modulus=(math.pi*root_chord**3/32)*(1-((root_chord-2*delta)/root_chord)**4)
    Bending_stress_bolt=max_moment_flap_edge*1000/Section_modulus
    Tensile_stress_bolt = Axial_stress_bolt + Bending_stress_bolt


    # Only for fatigue
    Stress_timeseries = resultant_moment_flap_edge * y_blade * 1000 / root_Iarea / 1e6
    Stress_timeseries = Stress_timeseries.reshape(1,len(Stress_timeseries))

    '''Tower Base stress'''
    tower_base_Iarea=(math.pi/64)*(t_d[0]**4-(t_d[0]-2*t_bt)**4)
    tower_base_Ipolar=2*tower_base_Iarea
    y_tower=t_d[0]/2

    TwrBsM=np.sqrt(TwrBsMxt ** 2 + TwrBsMyt ** 2)
    max_tower_moment=max(TwrBsM) #in KNm
    max_tower_moment_torsion=max(TwrBsMzt) #in KNm

    Stress_tower_base=np.double(max_tower_moment*y_tower*1000/tower_base_Iarea/1e6)
    Stress_tower_base_shear=np.double(max_tower_moment_torsion*y_tower*1000/tower_base_Ipolar/1e6)

    return Root_stress, Deflection, Stress_tower_base, Stress_tower_base_shear, Stress_timeseries, Tensile_stress_bolt















