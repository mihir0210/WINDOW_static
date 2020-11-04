'''Convert values coming from optimizer to spanwise values '''

from WINDOW_openMDAO.src.AbsPreprocessor.abs_preprocessor import AbsPreprocessor
from WINDOW_openMDAO.FAST.airfoils_coord_integration import airfoils_coord
from WINDOW_openMDAO.Preprocessor.span_layup_integration import span_layup
import numpy as np
import scipy.io
import matlab.engine
import os

eng = matlab.engine.start_matlab()
dir = os.getcwd() + r"\Matlab_scripts"
eng.cd(dir, nargout=0)

class Preprocessor(AbsPreprocessor):

        def compute(self, inputs, outputs):
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
                tau = inputs['tau']
                span_r = inputs['span_r']
                span_dr = inputs['span_dr']
                span_chord = inputs['span_chord']
                span_airfoil = inputs['span_airfoil']

                ##### Addition #####
                scipy.io.savemat('Matlab_scripts\Blade_layup.mat',
                                 dict(Blade_Radius=span_r, Blade_Chord=span_chord, Blade_Nfoil=span_airfoil))

                ####### Define standard layup #######
                web = 54.2 * tau #REMAINS CONSTANT THROUGHTOUT THE SPAN
                skin = 2.82 * tau  #REMAINS CONSTANT THROUGHTOUT THE SPAN
                root = 51.7 * tau #ONLY INITIAL VALUE REQUIRED
                le_core_thicknesses = np.array([20.0, 20.0, 20.0, 20.0]) * tau
                te_core_thicknesses = np.array([90.0, 90.0, 60.0, 20.0]) * tau
                spar_thicknesses = np.array([42.3, 42.3, 36.67, 16.45]) * tau
                te_reinf_thicknesses = np.array([7.05, 7.05, 4.7]) * tau


                #span_radius = np.linspace(1.5, 63, num_nodes)
                span_r = span_r - span_r[0]
                span_radius = np.linspace(span_r[0], span_r[-1], num_nodes)
                span_section = np.divide(span_radius, span_radius[-1]).reshape(1,num_nodes)

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

                properties = scipy.io.loadmat('Matlab_scripts\Preprocessor.mat')

                flapwise_stiffness = properties['EI_flap']
                edgewise_stiffness = properties['EI_edge']
                mass_length = properties['M_L']

                outputs['flapwise_stiffness'] = flapwise_stiffness[0,:]
                outputs['edgewise_stiffness'] = edgewise_stiffness[0,:]
                outputs['mass_length'] = mass_length[0,:]
                outputs['total_blade_mass'] = np.multiply(mass_length, span_dr)


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

        inputs = {'tau': 1}


        outputs = {}

        model = Preprocessor(num_nodes=49)

        model.compute(inputs, outputs)

        ###################################################
        ############### Post Processing ###################
        ###################################################
        beautify_dict(inputs)
        print '-' * 10
        beautify_dict(outputs)



















