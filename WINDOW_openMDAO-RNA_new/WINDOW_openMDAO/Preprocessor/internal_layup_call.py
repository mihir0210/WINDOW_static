'''Convert values coming from optimizer to spanwise values '''

from WINDOW_openMDAO.src.AbsRNA.Blade.AbsPreprocessor.abs_preprocessor import AbsPreprocessor
from WINDOW_openMDAO.FAST.airfoils_coord import airfoils_coord
from WINDOW_openMDAO.Preprocessor.span_layup import span_layup
import numpy as np
import scipy.io
import matlab.engine
import os

eng = matlab.engine.start_matlab()


class Preprocessor(AbsPreprocessor):

        def compute(self, inputs, outputs):
                #metadata

                num_nodes = self.options['num_nodes']

                airfoil_geometry_cyl1 = airfoils_coord(0)
                airfoil_geometry_cyl2 = airfoils_coord(1)
                airfoil_geometry_du405 = airfoils_coord(2)
                airfoil_geometry_du350 = airfoils_coord(3)
                airfoil_geometry_du300 = airfoils_coord(4)
                airfoil_geometry_du250 = airfoils_coord(5)
                airfoil_geometry_du210 = airfoils_coord(6)
                airfoil_geometry_naca = airfoils_coord(7)

                scipy.io.savemat('Airfoil_layup.mat', dict(Airfoil_Geometry1=airfoil_geometry_cyl1,
                                                                    Airfoil_Geometry2=airfoil_geometry_cyl2,
                                                                    Airfoil_Geometry3=airfoil_geometry_du405,
                                                                    Airfoil_Geometry4=airfoil_geometry_du350,
                                                                    Airfoil_Geometry5=airfoil_geometry_du300,
                                                                    Airfoil_Geometry6=airfoil_geometry_du250,
                                                                    Airfoil_Geometry7=airfoil_geometry_du210,
                                                                    Airfoil_Geometry8=airfoil_geometry_naca))

                # Design variables, all values are in mm (0.15, 0.3, 0.5 and 0.75 span)


                #inputs
                #### Thickness factor inputs at the root and 0.75 section
                #### Interpolate values of thickness factor for sections 0.11, 0.3 and 0.5
                tf_root = inputs['tau'][0]
                tf_75 = inputs['tau'][1]


                tf_section = np.array([0, 0.75])
                tf = np.array([tf_root, tf_75])

                tf_section_required = np.array([0, 0.11, 0.3, 0.5, 0.75])
                tf_span = np.interp(tf_section_required, tf_section, tf)

                tf_11 = tf_span[1]
                tf_30 = tf_span[2]
                tf_50 = tf_span[3]

                ####### Define standard layup #######
                web = 54.2 * tf_root #REMAINS CONSTANT THROUGHTOUT THE SPAN
                skin = 2.82 * tf_root  #REMAINS CONSTANT THROUGHTOUT THE SPAN
                root = np.array([51.7, 35]) * tf_root #ONLY INITIAL VALUE REQUIRED

                ### Defined at sections 0.11, 0.3, 0.5, 0.75, TE REINF IS 0 AT 0.75
                le_core_thicknesses = np.array([20.0*tf_11, 20.0*tf_30, 20.0*tf_50, 20.0*tf_75])
                te_core_thicknesses = np.array([90.0*tf_11, 90.0*tf_30, 60.0*tf_50, 20.0*tf_75])
                spar_thicknesses = np.array([42.3*tf_11, 42.3*tf_30, 36.67*tf_50, 16.45*tf_75])
                te_reinf_thicknesses = np.array([7.05*tf_11, 7.05*tf_30, 4.7*tf_50])



                #span_radius = np.linspace(1.5, 63, num_nodes)
                span_radius = np.linspace(0, 61.5, num_nodes)
                span_section = np.divide(span_radius, span_radius[-1]).reshape(1, num_nodes)

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

                span_layup(span_radius, span_section, web, skin, root, le_core1, spar1, te_core1, te_reinf1, le_core2, spar2, te_core2, te_reinf2,
                               le_core3, spar3, te_core3, te_reinf3, le_core4, spar4, te_core4)

                ret = eng.extract_properties_parameterized(nargout=0)

                properties = scipy.io.loadmat('Preprocessor.mat')

                flapwise_stiffness = properties['EI_flap']
                edgewise_stiffness = properties['EI_edge']
                mass_length = properties['M_L']

                outputs['flapwise_stiffness'] = flapwise_stiffness
                outputs['edgewise_stiffness'] = edgewise_stiffness
                outputs['mass_length'] = mass_length


if __name__ == "__main__":
        from WINDOW_openMDAO.src.Utils.print_utilities import beautify_dict
        import matplotlib.pyplot as plt
###################################################
############### Model Execution ###################
###################################################
        '''inputs = {'web': 54.2, 'skin': 2.82, 'root': 51.7,
                'le_core_thicknesses': np.array([20.0, 20.0, 20.0, 20.0]),
                'te_core_thicknesses': np.array([90.0, 90.0, 60.0, 20.0]),
                'spar_thicknesses': np.array([42.3, 42.3, 36.67, 16.45]),
                'te_reinf_thicknesses': np.array([7.05, 7.05, 4.7])}'''

        inputs = {'tau' : [1.0, 1.0]}

        outputs = {}

        model = Preprocessor(num_nodes=49)

        model.compute(inputs, outputs)

        ###################################################
        ############### Post Processing ###################
        ###################################################
        beautify_dict(inputs)
        print '-' * 10
        beautify_dict(outputs)



















