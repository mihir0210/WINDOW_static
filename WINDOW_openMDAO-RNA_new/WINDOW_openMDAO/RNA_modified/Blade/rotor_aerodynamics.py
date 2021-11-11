from math import pi

from WINDOW_openMDAO.src.api import AbsRotorAerodynamics
from bem import bem_rotor
import matlab.engine
import os
import numpy as np
import scipy.io




#############################################################################
##############################  MODEL 1: BEM ################################
#############################################################################
class BEM(AbsRotorAerodynamics):
    '''
        implements a BEM code written by Tanuj 
    '''
    
    def compute(self, inputs, outputs): 
        # metadata
        rho_air = self.metadata['rho_air']
          
        # inputs     
        design_tsr = inputs['design_tsr']
        wind_speed = inputs['wind_speed'] 
        blade_number = inputs['blade_number']
        rotor_diameter = inputs['rotor_diameter']
        hub_radius = inputs['hub_radius']
        span_r = inputs['span_r']
        span_dr = inputs['span_dr']
        span_chord = inputs['span_chord']
        span_twist = inputs['span_twist']
        span_airfoil = inputs['span_airfoil']
        span_airfoil_id = inputs['span_airfoil_id']
        pitch = inputs['pitch']


        ### Convert to absolute values for optimization###
        #tsr_ref = 7.6
        #design_tsr = tsr_ref*design_tsr

        #pitch_ref = 3.5
        #pitch = pitch_ref*pitch


        #print 'Pitch:', pitch



        
        rotor_radius = rotor_diameter/2.0
        rotor_speed = (design_tsr*wind_speed/rotor_radius) * (30/pi) # rpm
        
        # Execute the BEM code. Check bem.py
        [spanwise, rotor] = bem_rotor(wind_speed, rho_air, \
                                      blade_number, rotor_radius, hub_radius, design_tsr, pitch, \
                                      span_r, span_dr, span_chord, span_twist, span_airfoil, \
                                      is_prandtl=1, is_glauert=1)


        '''
        Uses scripts from WIND TURBINE DESIGN COURSE
        ## Find Cp using a different method

        #eng3 = matlab.engine.start_matlab("-desktop")  ###Only when using FAST
        eng3 = matlab.engine.start_matlab()
        dir = os.getcwd() + r"\Matlab_scripts"
        eng3.cd(dir, nargout=0)
        
        scipy.io.savemat('Matlab_scripts\Blade_Cp.mat',
                 dict(Blade_Radius=span_r, Blade_Chord=span_chord, Blade_Twist=span_twist,
                      Blade_NFoil=span_airfoil, Blade_IFoil=span_airfoil_id,
                      Blade_Number=blade_number))
        
        

        pitch = np.asscalar(np.array(pitch))  # convert to scalar
        design_tsr = np.asscalar(np.array(design_tsr))  # convert to scalar
        Cp = eng3.GenerateSteadyOp_Cp(pitch, design_tsr, nargout=1)

        # tsr = output[1]


        eng3.quit()'''


        print 'rotor speed', rotor_speed

        
        # outputs
        outputs['rotor_speed'] = rotor_speed
        outputs['swept_area'] = rotor['swept_area']
        outputs['rotor_cp'] = rotor['cp']
        #outputs['rotor_cp'] = Cp
        outputs['rotor_cq'] = rotor['cq']
        outputs['rotor_ct'] = rotor['ct']
        outputs['rotor_power'] = rotor['power']
        outputs['rotor_torque'] = rotor['torque']
        outputs['rotor_thrust'] = rotor['thrust']
        outputs['span_fx'] = spanwise['fx']
        outputs['span_fy'] = spanwise['fy']
        
        
        

        
        
        
        
           
        





#############################################################################
##############################  UNIT TESTING ################################
#############################################################################         
if __name__ == "__main__":
    from time import time
    from WINDOW_openMDAO.src.api import beautify_dict
    
    ###################################################
    ############### Model Execution ###################
    ################################################### 
    span_r = [3.0375, 6.1125, 9.1875, 12.2625, 15.3375, 18.4125, 21.4875, 24.5625, 27.6375, 30.7125, 33.7875, 36.8625, 39.9375, 43.0125, 46.0875, 49.1625, 52.2375, 55.3125, 58.3875, 61.4625]
    span_dr = [3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075]
    span_airfoil = [0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 4.0, 5.0, 5.0, 5.0, 6.0, 6.0, 6.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]
    span_chord = [3.5615, 3.9127, 4.2766, 4.5753, 4.6484, 4.5489, 4.3819, 4.2206, 4.0382, 3.8449, 3.6549, 3.4713, 3.2868, 3.1022, 2.9178, 2.7332, 2.5487, 2.3691, 2.1346, 1.4683]
    span_twist = [13.235, 13.235, 13.235, 13.1066, 11.6516, 10.5523, 9.6506, 8.7896, 7.876, 6.937, 6.0226, 5.1396, 4.2562, 3.428, 2.735, 2.1466, 1.5521, 0.9525, 0.3813, 0.0477]

    inputs={'design_tsr' : 7.0, \
            'wind_speed' : 12.2, \
            'blade_number' : 3, \
            'rotor_diameter' : 126.0, \
            'hub_radius' : 1.5, \
            'span_r' : span_r, \
            'span_dr' : span_dr, \
            'span_chord' :  span_chord, \
            'span_twist' : span_twist, \
            'span_airfoil' : span_airfoil,\
            'pitch': 0}
    outputs={}
    
    model = BEM(num_nodes=20, rho_air=1.225)
    
    start = time()  
    model.compute(inputs, outputs)  
    print 'Executed in ' + str(round(time() - start, 2)) + ' seconds'
    
    
    ###################################################
    ############### Post Processing ###################
    ################################################### 
    beautify_dict(inputs) 
    print '-'*10
    beautify_dict(outputs)  
    
    
    
  
        
     
    


 