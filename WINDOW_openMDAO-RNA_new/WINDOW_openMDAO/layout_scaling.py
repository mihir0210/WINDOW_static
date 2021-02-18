from openmdao.api import ExplicitComponent




import numpy as np
from scipy import interpolate
import csv
import pandas as pd
import ast
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull




class LayoutScaling(ExplicitComponent):
    '''
    This class rotates the original layout, scales downwind and crosswind spacing w.r.t the scaling ratio,
    and rotates it back to the given layout orientation.
    '''

    def __init__(self, n_layout,n_substation):
        super(LayoutScaling, self).__init__()
        self.n_layout = n_layout
        self.n_substation = n_substation

    def setup(self):


        self.add_input('orig_layout', shape=(self.n_layout,2))
        self.add_input('substation_coords',shape=(self.n_substation,2))
        self.add_input('turbine_radius')
        self.add_input('scaling_factor')

        self.add_output('new_layout', shape=(self.n_layout,2))
        self.add_output('new_substation_coords',shape=(self.n_substation,2))
        self.add_output('farm_area')

    def compute(self, inputs, outputs):

        orig_layout_ = inputs['orig_layout']
        substation_coords = inputs['substation_coords']
        turbine_radius = inputs['turbine_radius']
        scaling_factor = inputs['scaling_factor']

        orig_layout = []
        for element in range(len(orig_layout_)):
            orig_layout.append([orig_layout_[element][0], orig_layout_[element][1]])





        turbine_ref = 99.0 # rotor radius of the reference turbine being used
        scaling_ratio = scaling_factor*(turbine_radius/turbine_ref) # scaling ratio will be equal to scaling_factor*(D_new/D_ref)

        scaling_ratio = scaling_ratio[0]

        print 'scaling_factor:', scaling_factor
        print 'scaling_ratio:', scaling_ratio


        def centroid(points):
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            _len = len(points)
            centroid_x = sum(x_coords) / _len
            centroid_y = sum(y_coords) / _len

            return centroid_x, centroid_y


        def new_farm():

            [cent_x_ogi, cent_y_ogi] = centroid(orig_layout)



            scaled_layout = [[orig_layout[element][0] * scaling_ratio, orig_layout[element][1] * scaling_ratio] for element in range(len(orig_layout))]


            [cent_x_new, cent_y_new] = centroid(scaled_layout)

            dx = cent_x_new - cent_x_ogi
            dy = cent_y_new - cent_y_ogi



            new_layout = [[element[0]-dx, element[1]-dy] for element in scaled_layout] #shift centroid of scaled layout back to that of original



            new_substation_coords = [[element[0]*scaling_ratio-dx, element[1]*scaling_ratio-dy] for element in substation_coords]

            x = np.array([new_layout[idx][0] for idx in range(len(new_layout))])
            y = np.array([new_layout[idx][1] for idx in range(len(new_layout))])

            #flat_x = [item for sublist in x for item in sublist]
            #flat_y = [item for sublist in y for item in sublist]

            points = np.random.rand(len(x), 2)
            points[:, 0] = x
            points[:, 1] = y
            hull = ConvexHull(points)

            farm_area = hull.volume/1e6 # in

            '''
            plt.plot(points[:, 0], points[:, 1], 'o')
            for simplex in hull.simplices:
                plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
            plt.show()'''


            return new_layout, new_substation_coords, farm_area

        [new_layout, new_substation_coords, farm_area] = new_farm()

        print 'farm_area:', farm_area


        outputs['farm_area'] = farm_area
        outputs['new_layout'] = new_layout
        outputs['new_substation_coords'] = new_substation_coords
