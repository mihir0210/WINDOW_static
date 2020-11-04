'''Convert values coming from optimizer to spanwise values '''

from WINDOW_openMDAO.src.AbsRNA.Blade.AbsPreprocessor.abs_preprocessor import AbsPreprocessor
from WINDOW_openMDAO.FAST.airfoils_coord_integration import airfoils_coord
from WINDOW_openMDAO.RNA_modified.Blade.Preprocessor.span_layup_integration import span_layup
import numpy as np
import scipy.io
import matlab.engine
import os

'''
eng1 = matlab.engine.start_matlab()

dir = os.getcwd() + r"\Matlab_scripts"
eng1.cd(dir, nargout=0)'''



class Preprocessor(AbsPreprocessor):


        def compute(self, inputs, outputs):
                #eng1 = matlab.engine.start_matlab("-desktop") ### Run in desktop mode only when using FAST
                eng1 = matlab.engine.start_matlab()

                dir = os.getcwd() + r"\Matlab_scripts"
                eng1.cd(dir, nargout=0)

            #metadata
                #num_stations = self.metadata['num_stations']
                num_nodes = self.metadata['num_nodes']

                airfoil_geometry_cyl1 = airfoils_coord(0)
                airfoil_geometry_cyl2 = airfoils_coord(1)
                airfoil_geometry_du405 = airfoils_coord(2)
                airfoil_geometry_du350 = airfoils_coord(3)
                airfoil_geometry_du300 = airfoils_coord(4)
                airfoil_geometry_du250 = airfoils_coord(5)
                airfoil_geometry_du210 = airfoils_coord(6)
                airfoil_geometry_naca = airfoils_coord(7)

                scipy.io.savemat('Matlab_scripts\Airfoil_layup.mat', dict(Airfoil_Geometry1=airfoil_geometry_cyl1,
                                                                    Airfoil_Geometry2=airfoil_geometry_cyl2,
                                                                    Airfoil_Geometry3=airfoil_geometry_du405,
                                                                    Airfoil_Geometry4=airfoil_geometry_du350,
                                                                    Airfoil_Geometry5=airfoil_geometry_du300,
                                                                    Airfoil_Geometry6=airfoil_geometry_du250,
                                                                    Airfoil_Geometry7=airfoil_geometry_du210,
                                                                    Airfoil_Geometry8=airfoil_geometry_naca))

                # Design variables, all values are in mm (0.15, 0.3, 0.5 and 0.75 span)


                #inputs
                #tau = np.array(inputs['tau'])
                #### Thickness factor inputs at the root and 0.75 section
                tf = inputs['tau']

                #print 'Thickness factor:',tf


                #tf_root = inputs['tau_root']
                #tf_75 = inputs['tau_75']
                span_r = np.array(inputs['span_r'])
                span_dr = np.array(inputs['span_dr'])
                span_chord = np.array(inputs['span_chord'])
                span_airfoil = np.array(inputs['span_airfoil'])

                #print 'span_r:', span_r

                ##### Addition #####
                scipy.io.savemat('Matlab_scripts\Blade_layup.mat',
                                 dict(Blade_Radius=span_r, Blade_Chord=span_chord, Blade_Nfoil=span_airfoil))


                tf_root = tf
                tf_75 = tf

                #### Interpolate values of thickness factor for sections 0.11, 0.3 and 0.5

                tf_section = np.array([0, 0.75]).reshape(1,2).astype(float)
                tf = np.array([tf_root, tf_75]).reshape(1,2).astype(float)

                tf_section_required = np.array([0, 0.11, 0.3, 0.5, 0.75]).reshape(1,5).astype(float)
                tf_span = np.interp(tf_section_required[0,:], tf_section[0,:], tf[0,:])

                tf_11 = tf_span[1]
                tf_30 = tf_span[2]
                tf_50 = tf_span[3]

                #print tf_root, tf_75

                ####### Define standard layup #######
                web = 54.2 * tf_root #REMAINS CONSTANT THROUGHTOUT THE SPAN
                skin = 2.82 * tf_root  #REMAINS CONSTANT THROUGHTOUT THE SPAN
                root = np.array([51.7, 35]) * tf_root #ONLY INITIAL VALUE REQUIRED

                ### Defined at sections 0.11, 0.3, 0.5, 0.75, TE REINF IS 0 AT 0.75
                le_core_thicknesses = np.array([20.0*tf_11, 20.0*tf_30, 20.0*tf_50, 20.0*tf_75])
                te_core_thicknesses = np.array([90.0*tf_11, 90.0*tf_30, 60.0*tf_50, 20.0*tf_75])
                spar_thicknesses = np.array([42.3*tf_11, 42.3*tf_30, 36.67*tf_50, 16.45*tf_75])
                te_reinf_thicknesses = np.array([7.05*tf_11, 7.05*tf_30, 4.7*tf_50])



                #span_r = span_r - span_r[0]
                #span_section = np.divide(span_r, span_r[-1]).reshape(1, num_nodes)

                ##### Change values 1.5 and 61.5 to hub radius and blade length - hub radius

                #results = scipy.io.loadmat('Matlab_scripts\NREL5MW_blade.mat')
                #span_r = np.array(results['a']).reshape(1,num_nodes)


                span_r = span_r - 1.5  # need to change when hub radius changes
                #span_section = np.divide(span_r, 61.5).reshape(1, num_nodes) # need to change to blade radius last point
                #span_section = np.divide(span_r, 100).reshape(1, num_nodes)  # need to change to blade radius last point

                span_section = np.divide(span_r, span_r[-1]).reshape(1, num_nodes)
                #print 'span_r:', span_r
                #print 'span_section:', span_section


                root1 = root[0] # Root thickness at 0
                root2 = root[1] # Root thickness at 0.02

                le_core1 = le_core_thicknesses[0] # Leading edge core material thickness at station 1
                le_core2 = le_core_thicknesses[1] # Leading edge core material thickness at station 2
                le_core3 = le_core_thicknesses[2] # Leading edge core material thickness at station 3
                le_core4 = le_core_thicknesses[3] # Leading edge core material thickness at station 4

                te_core1 = te_core_thicknesses[0] #Trailing edge core material thickness at station 1
                te_core2 = te_core_thicknesses[1] #Trailing edge core material thickness at station 2
                te_core3 = te_core_thicknesses[2] #Trailing edge core material thickness at station 3
                te_core4 = te_core_thicknesses[3] #Trailing edge core material thickness at station 4

                spar1 = spar_thicknesses[0] # Spar cap UD Carbon material thickness at station 1
                spar2 = spar_thicknesses[1] # Spar cap UD Carbon material thickness at station 2
                spar3 = spar_thicknesses[2] # Spar cap UD Carbon material thickness at station 3
                spar4 = spar_thicknesses[3] # Spar cap UD Carbon material thickness at station 4

                te_reinf1 = te_reinf_thicknesses[0] #Trailing edge re-inforcement UD glass material thickness at station 1
                te_reinf2 = te_reinf_thicknesses[1] #Trailing edge re-inforcement UD glass material thickness at station 2
                te_reinf3 = te_reinf_thicknesses[2] #Trailing edge re-inforcement UD glass material thickness at station 3

                span_layup(span_r, span_section, web, skin, root1, root2, le_core1, spar1, te_core1, te_reinf1, le_core2, spar2,
               te_core2, te_reinf2, le_core3, spar3, te_core3, te_reinf3, le_core4, spar4, te_core4)

                ret = eng1.extract_properties_parameterized_latest(nargout=0)

                eng1.quit()


                properties = scipy.io.loadmat('Matlab_scripts\Preprocessor.mat')

                flapwise_stiffness = properties['EI_flap']
                edgewise_stiffness = properties['EI_edge']
                mass_length = properties['M_L']
                total_blade_mass = np.sum(np.multiply(mass_length, span_dr))
                outputs['flapwise_stiffness'] = flapwise_stiffness[0,:]
                outputs['edgewise_stiffness'] = edgewise_stiffness[0,:]
                outputs['mass_length'] = mass_length[0,:]
                outputs['total_blade_mass'] = total_blade_mass

                # Blade mass
                print 'Blade mass:', total_blade_mass

if __name__ == "__main__":
        from WINDOW_openMDAO.src.Utils.print_utilities import beautify_dict
        import matplotlib.pyplot as plt
###################################################
############### Model Execution ###################
###################################################
        '''inputs = {'web': 54.2, 'skin': 2.82, 'root': 51.7,
                'le_core_thicknesses': [20.0, 20.0, 20.0, 20.0],
                'te_core_thicknesses': [90.0, 90.0, 60.0, 20.0],
                'spar_thicknesses': [42.3, 42.3, 36.67, 16.45],
                'te_reinf_thicknesses': [7.05, 7.05, 4.7]}'''

        span_r = [3.0375, 6.1125, 9.1875, 12.2625, 15.3375, 18.4125, 21.4875, 24.5625, 27.6375, 30.7125,
                    33.7875, 36.8625, 39.9375, 43.0125, 46.0875, 49.1625, 52.2375, 55.3125, 58.3875, 61.4625],
        span_dr = [3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075, 3.075,
                     3.075, 3.075, 3.075, 3.075, 3.075, 3.075],
        span_chord = [3.5615, 3.9127, 4.2766, 4.5753, 4.6484, 4.5489, 4.3819, 4.2206, 4.0382, 3.8449, 3.6549, 3.4713,
                        3.2868, 3.1022, 2.9178, 2.7332, 2.5487, 2.3691, 2.1346, 1.4683]

        inputs = {'tau': 1, 'span_r': span_r, 'span_dr' : span_dr, 'span_chord' : span_chord}




        outputs = {}

        model = Preprocessor(num_nodes=20)

        model.compute(inputs, outputs)

        ###################################################
        ############### Post Processing ###################
        ###################################################
        beautify_dict(inputs)
        print '-' * 10
        beautify_dict(outputs)



















