import numpy as np
import pandas as pd
from math import pi, radians, sin, cos
import csv
import scipy.io
import os
#import matlab.engine
#eng = matlab.engine.start_matlab()

from WINDOW_openMDAO.src.api import AbsRotorMechanics

        
#############################################################################
########## MODEL 1: Static module based on ReferenceTurbine #################
#############################################################################
class  Analytical(AbsRotorMechanics):
    '''
        this model calculates the stress along the blade section and the tip deflection 
        based on the steady state assumption
    '''
    
    def compute(self, inputs, outputs):
        # metadata        
        num_nodes = self.options['num_nodes']
        E_blade = self.options['E_blade']
        g = self.options['g']
        
        
        # inputs
        shaft_angle = radians(abs(inputs['shaft_angle']))
        span_r = inputs['span_r']
        span_dr = inputs['span_dr']
        span_chord = inputs['span_chord']
        span_thickness = inputs['span_thickness']
        span_mass = inputs['span_mass']
        span_flap_stiff = inputs['span_flap_stiff']
        span_edge_stiff = inputs['span_edge_stiff']
        span_fx = inputs['span_fx']
        span_fy = inputs['span_fy']
        
        # to store information at each blade node 
        zeroes = [0.0] * num_nodes
        nodes = pd.DataFrame(data={ 'r' : span_r, \
                                    'dr' : span_dr, \
                                    'chord' : span_chord, \
                                    'thick': span_thickness, \
                                    'mass' : span_mass, \
                                    'EI_flap' : span_flap_stiff, \
                                    'EI_edge' : span_edge_stiff, \
                                    'I_flap' : [x/E_blade for x in span_flap_stiff], \
                                    'I_edge' : [x/E_blade for x in span_edge_stiff], \
                                    'Fx' : span_fx, \
                                    'Fy' : span_fy, \
                                    'M_flap' : zeroes, \
                                    'M_edge' : zeroes, \
                                    'M_grav' : zeroes, \
                                    'S_flap' : zeroes, \
                                    'S_edge' : zeroes, \
                                    'S_grav' : zeroes, \
                                    'S_max' : zeroes, \
                                    'M_EI' : zeroes, \
                                    'dy_dx': zeroes, \
                                    'y': zeroes
                                } 
                            )
               
        # analytical calculations       
        for i in range(num_nodes): # loop through each i
            for j in range(i, num_nodes): # loop through each node that is beyond i
                nodes.loc[i, 'M_flap'] += (nodes.loc[j, 'Fx'] * nodes.loc[j, 'dr'] + \
                                            nodes.loc[j, 'mass'] * nodes.loc[j, 'dr'] * g * sin(shaft_angle)) * \
                                            (nodes.loc[j, 'r'] - nodes.loc[i, 'r'])
                nodes.loc[i, 'M_edge'] += nodes.loc[j, 'Fy'] * nodes.loc[j, 'dr'] * (nodes.loc[j, 'r'] - nodes.loc[i, 'r'])
                nodes.loc[i, 'M_grav'] += nodes.loc[j, 'mass'] * nodes.loc[j, 'dr'] * g * cos(shaft_angle) * \
                                            (nodes.loc[j, 'r'] - nodes.loc[i, 'r'])                                    
           
            nodes.loc[i, 'S_flap'] = nodes.loc[i, 'M_flap'] * 0.5 * nodes.loc[i, 'thick'] / nodes.loc[i, 'I_flap']
            nodes.loc[i, 'S_edge'] = nodes.loc[i, 'M_edge'] * 0.75 * nodes.loc[i, 'chord'] / nodes.loc[i, 'I_edge']
            nodes.loc[i, 'S_grav'] = nodes.loc[i, 'M_grav'] * 0.75 * nodes.loc[i, 'chord'] / nodes.loc[i, 'I_edge']
            nodes.loc[i, 'S_max'] = nodes.loc[i, 'S_flap'] + nodes.loc[i, 'S_edge'] + nodes.loc[i, 'S_grav']
            nodes.loc[i, 'M_EI']   = nodes.loc[i, 'M_flap'] / nodes.loc[i, 'EI_flap']
            
            if i > 0:
                nodes.loc[i, 'dy_dx'] = nodes.loc[i-1, 'dy_dx'] + \
                                        (nodes.loc[i, 'M_EI'] + nodes.loc[i-1, 'M_EI'])/2.0 * nodes.loc[i, 'dr']
                nodes.loc[i, 'y'] = nodes.loc[i-1, 'y'] + \
                                        (nodes.loc[i, 'dy_dx'] + nodes.loc[i-1, 'dy_dx'])/2.0 * nodes.loc[i, 'dr']          
            
        
        #print nodes

        root_moment_flap = nodes.loc[0, 'M_flap']
        span_moment_flap = np.array(nodes['M_flap'])
        span_moment_edge = np.array(nodes['M_edge'])
        span_moment_gravity = np.array(nodes['M_grav'])
        span_stress_flap = np.array(nodes['S_flap'])
        span_stress_edge = np.array(nodes['S_edge'])
        span_stress_gravity = np.array(nodes['S_grav'])
        span_stress_max = np.array(nodes['S_max']).max()     # np.array(nodes['S_flap']).max()*gamma_ultimate/UTS
        tip_deflection = nodes.loc[num_nodes-1, 'y']


        # scipy.io.savemat('Matlab_scripts\Static_moment.mat',
        #                  dict(MFlap=span_moment_flap, MEdge=span_moment_edge, MGravity=span_moment_gravity,
        #                       ))
        #
        #
        # eng2 = matlab.engine.start_matlab()
        # dir = os.getcwd() + r"\Matlab_scripts"
        # eng2.cd(dir, nargout=0)
        #
        # ret = eng2.Post_processing_static(nargout=0)
        #
        # eng2.quit()
        # results = scipy.io.loadmat('Matlab_scripts\Ultimate_Results_Static.mat')
        # #Root_stress = results['Stress_root_skin'][0]
        # Span_stress = results['Stress_span']
        #
        #
        #
        #
        #
        # ##### 1st row is Flapwise stress in skin along the span #####
        # ##### 2nd row is Flapwise stress in spar along the span #####
        # ##### 3rd row is Edgewise stress in skin along the span #####
        # ##### 4th row is Edgewise stress in Te reinf/ panel along the span #####
        #
        # Stress_flapwise_skin = Span_stress[0,:]
        # Stress_flapwise_spar = Span_stress[1,:]
        # Stress_edgewise_skin = Span_stress[2,:]
        # Stress_edgewise_te_reinf = Span_stress[3,:]
        #
        # Stress_skin = np.concatenate((Stress_flapwise_skin, Stress_edgewise_skin), axis=0)
        #
        # max_stress_skin = max(Stress_skin)
        # max_stress_spar =  max(Stress_flapwise_spar)
        # max_stress_te_reinf = max(Stress_edgewise_te_reinf)
        #
        #
        #
        # #### Extract stresses at given node numbers ###
        # span_node = np.array([7, 15, 24, 37, 47])
        #
        # ## Node 7
        #
        # Stress_flapwise_skin_loc1 = Span_stress[0, span_node[0]-1]
        # Stress_flapwise_spar_loc1 = Span_stress[1, span_node[0]-1]
        #
        # Stress_edgewise_skin_loc1 = Span_stress[2, span_node[0]-1]
        # Stress_edgewise_te_reinf_loc1 = Span_stress[3, span_node[0]-1]
        #
        # ## Node 15
        #
        # Stress_flapwise_skin_loc2 = Span_stress[0, span_node[1]-1]
        # Stress_flapwise_spar_loc2 = Span_stress[1, span_node[1]-1]
        #
        # Stress_edgewise_skin_loc2 = Span_stress[2, span_node[1]-1]
        # Stress_edgewise_te_reinf_loc2 = Span_stress[3, span_node[1]-1]
        #
        # ## Node 24
        #
        # Stress_flapwise_skin_loc3 = Span_stress[0, span_node[2] - 1]
        # Stress_flapwise_spar_loc3 = Span_stress[1, span_node[2] - 1]
        #
        # Stress_edgewise_skin_loc3 = Span_stress[2, span_node[2] - 1]
        # Stress_edgewise_te_reinf_loc3 = Span_stress[3, span_node[2] - 1]
        #
        # ## Node 37
        #
        # Stress_flapwise_skin_loc4 = Span_stress[0, span_node[3] - 1]
        # Stress_flapwise_spar_loc4 = Span_stress[1, span_node[3] - 1]
        #
        # Stress_edgewise_skin_loc4 = Span_stress[2, span_node[3] - 1]
        # Stress_edgewise_te_reinf_loc4 = Span_stress[3, span_node[3] - 1]
        #
        # ## Node 47
        #
        # Stress_flapwise_skin_loc5 = Span_stress[0, span_node[4] - 1]
        # Stress_flapwise_spar_loc5 = Span_stress[1, span_node[4] - 1]
        #
        # Stress_edgewise_skin_loc5 = Span_stress[2, span_node[4] - 1]
        # Stress_edgewise_te_reinf_loc5 = Span_stress[3, span_node[4] - 1]
        #
        # ##### Take the flapwise stresses at skin into one array ####
        #
        # Stress_flapwise_skin = np.array([Stress_flapwise_skin_loc1, Stress_flapwise_skin_loc2, Stress_flapwise_skin_loc3,
        #                                  Stress_flapwise_skin_loc4, Stress_flapwise_skin_loc5])
        #
        # Stress_flapwise_spar = np.array([Stress_flapwise_spar_loc1, Stress_flapwise_spar_loc2, Stress_flapwise_spar_loc3,
        #                                  Stress_flapwise_spar_loc4, Stress_flapwise_spar_loc5])
        #
        # Stress_edgewise_skin = np.array([Stress_edgewise_skin_loc1, Stress_edgewise_skin_loc2, Stress_edgewise_skin_loc3,
        #                                  Stress_edgewise_skin_loc4, Stress_edgewise_skin_loc5])
        #
        # Stress_edgewise_te_reinf = np.array([Stress_edgewise_te_reinf_loc1, Stress_edgewise_te_reinf_loc2, Stress_edgewise_te_reinf_loc3,
        #                                      Stress_edgewise_te_reinf_loc4, Stress_edgewise_te_reinf_loc5])



        safety_factor = 1 #1.5 #Static to Dynamic
        tip_deflection = tip_deflection*safety_factor


        #print 'Tip deflection static : ',tip_deflection
        #print 'Max Stress Spar : ', max_stress_spar
        #print 'Max Stress Skin : ', max_stress_skin
        #print 'Max Stress Te Reinf : ', max_stress_te_reinf

        field_names = ['Tip deflection']
        data = {field_names[0]: tip_deflection}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value])
        csvfile.close()


        # outputs    
        outputs['root_moment_flap'] = nodes.loc[0, 'M_flap']
        outputs['span_moment_flap'] = np.array(nodes['M_flap'])    
        outputs['span_moment_edge'] = np.array(nodes['M_edge'])  
        outputs['span_moment_gravity'] = np.array(nodes['M_grav'])
        outputs['span_stress_flap'] = np.array(nodes['S_flap'])
        outputs['span_stress_edge'] = np.array(nodes['S_edge'])
        outputs['span_stress_gravity'] = np.array(nodes['S_grav'])
        outputs['span_stress_max'] = np.array(nodes['S_max']).max()     # np.array(nodes['S_flap']).max()*gamma_ultimate/UTS
        outputs['tip_deflection'] = tip_deflection
        #outputs['max_stress_skin'] = max_stress_skin
        #outputs['max_stress_spar'] = max_stress_spar
        #outputs['max_stress_te_reinf'] = max_stress_te_reinf
        #outputs['Root_stress'] = Root_stress
        #outputs['Stress_flapwise_skin'] = Stress_flapwise_skin
        #outputs['Stress_flapwise_spar'] = Stress_flapwise_spar
        #outputs['Stress_edgewise_skin'] = Stress_edgewise_skin
        #outputs['Stress_edgewise_te_reinf'] = Stress_edgewise_te_reinf



        
        
        







#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":
    from time import time
    import matplotlib.pyplot as plt    
    from WINDOW_openMDAO.src.api import beautify_dict
    
    ###################################################
    ############### Model Execution ###################
    ################################################### 
    shaft_angle = -5.0
    span_r = [3.0375, 6.1125, 9.1875, 12.2625, 15.3375, 18.4125, 21.4875, 24.5625, 27.6375, 30.7125, 33.7875, 36.8625, 39.9375, 43.0125, 46.0875, 49.1625, 52.2375, 55.3125, 58.3875, 61.4625]
    span_dr = [3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075]
    span_chord = [3.5615, 3.9127, 4.2766, 4.5753, 4.6484, 4.5489, 4.3819, 4.2206, 4.0382, 3.8449, 3.6549, 3.4713, 3.2868, 3.1022, 2.9178, 2.7332, 2.5487, 2.3691, 2.1346, 1.4683]
    span_thickness = [3.5614, 3.3798, 2.7023, 2.1252, 1.7103, 1.5501, 1.414, 1.2486, 1.0955, 0.9645, 0.8542, 0.767, 0.664, 0.6017, 0.5409, 0.4944, 0.4608, 0.42, 0.3861, 0.2655]
    span_mass = [697.7655, 679.6009, 413.8751, 410.6307, 384.1854, 346.2471, 333.3628, 320.0997, 298.2267, 275.5935, 252.3555, 227.5372, 193.881, 166.5232, 146.1523, 126.5607, 100.8119, 85.5755, 62.0602, 17.4553]
    span_flap_stiff = [1.8371E+10, 1.3871E+10, 5.9623E+09, 4.7197E+09, 3.0085E+09, 2.2642E+09, 1.9079E+09, 1.5313E+09, 1.1402E+09, 7.8028E+08, 5.2445E+08, 3.4265E+08, 2.1866E+08, 1.3169E+08, 9.8637E+07, 7.4358E+07, 5.2445E+07, 3.6103E+07, 2.0647E+07, 1.5998E+06]
    span_edge_stiff = [1.8403E+10, 1.7684E+10, 8.7006E+09, 7.1049E+09, 6.3176E+09, 4.7961E+09, 4.3343E+09, 3.9345E+09, 3.4919E+09, 2.9340E+09, 2.5390E+09, 1.9896E+09, 1.5029E+09, 1.1941E+09, 8.9622E+08, 6.8351E+08, 4.6979E+08, 3.6768E+08, 2.1335E+08, 2.0813E+07]
    span_fx = [0.0, 152.8413, 692.3132, 1231.7851, 1771.257, 2077.937, 2385.88, 2693.823, 3167.965, 3613.9953, 4060.0257, 4506.056, 4882.4425, 5258.829, 5635.2155, 6011.602, 5169.536, 4327.47, 3485.404, 2222.305]
    span_fy = [-3.5, -103.8047, 162.8256, 429.456, 696.0863, 702.4778, 701.8906, 701.3033, 720.8832, 725.5557, 730.2281, 734.9006, 732.7446, 730.5885, 728.4325, 726.2764, 558.9978, 391.7192, 224.4406, -26.4774]

    inputs={'shaft_angle' : shaft_angle, \
            'span_r' : span_r, \
            'span_dr' : span_dr, \
            'span_chord' : span_chord, \
            'span_thickness' : span_thickness, \
            'span_mass' : span_mass, \
            'span_flap_stiff' : span_flap_stiff, \
            'span_edge_stiff' : span_edge_stiff, \
            'span_fx' : span_fx, \
            'span_fy' : span_fy}
    outputs={}
    
    model = Analytical(num_nodes=20, E_blade=36.233e9, g=9.8)      
    model.compute(inputs, outputs)  
    
    
    ###################################################
    ############### Post Processing ###################
    ################################################### 
    beautify_dict(inputs) 
    print(('-'*10))
    beautify_dict(outputs)     

    plt.plot(inputs['span_r'], outputs['span_stress_gravity'])
    plt.show()
 

        
    
    
    
    
            