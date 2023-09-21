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
        self.add_output('x_coord', shape=(self.n_layout,1))
        self.add_output('y_coord', shape=(self.n_layout,1))
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





        turbine_ref = 120.0 #99.0 # rotor radius of the reference turbine being used
        #scaling_ratio = scaling_factor*(turbine_radius/turbine_ref) # scaling ratio will be equal to scaling_factor*(D_new/D_ref).
        scaling_ratio = scaling_factor    # For fixed area, input files have fixed absolute distance
        scaling_ratio = scaling_ratio[0]

        #print 'scaling_factor:', scaling_factor
        #print 'scaling_ratio:', scaling_ratio


        def centroid(points):
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            _len = len(points)
            centroid_x = sum(x_coords) / _len
            centroid_y = sum(y_coords) / _len

            return centroid_x, centroid_y


        def new_farm():

            [cent_x_ogi, cent_y_ogi] = centroid(orig_layout)

            #print 'ogi centroid x and centroid y',cent_x_ogi,cent_y_ogi

            #multiply coordinates with the scaling ratio
            scaled_layout = [[orig_layout[element][0] * scaling_ratio, orig_layout[element][1] * scaling_ratio] for element in range(len(orig_layout))]

            coord_fixedturb = orig_layout[0] #turbine to the leftmost and bottom which is kept fixed


            dx = scaled_layout[0][0] - coord_fixedturb[0]
            dy = scaled_layout[0][1] - coord_fixedturb[1]





            new_layout = [[element[0]-dx, element[1]-dy] for element in scaled_layout] #shift scaled layout back to the coordinate of fixed turbine
            [cent_x_new, cent_y_new] = centroid(new_layout) # centroid of new layout



            # new_substation_coords = [[element[0]*scaling_ratio-dx, element[1]*scaling_ratio-dy] for element in substation_coords]
            # #new_substation_coords = [cent_x_ogi, cent_y_ogi]

            new_substation_coords = [[cent_x_new, cent_y_new], [cent_x_new + 1000, cent_y_new]]



            x = np.array([new_layout[idx][0] for idx in range(len(new_layout))])
            y = np.array([new_layout[idx][1] for idx in range(len(new_layout))])



            points = np.random.rand(len(x), 2)
            points[:, 0] = x
            points[:, 1] = y
            hull = ConvexHull(points)

            farm_area = hull.volume/1e6 # in km2

            #print(farm_area)
            # x = [item for sublist in x for item in sublist]
            # y = [item for sublist in y for item in sublist]



            # plt.plot(points[:, 0], points[:, 1], 'o')
            # for simplex in hull.simplices:
            #     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
            # plt.show()


            return x,y, new_layout, new_substation_coords, farm_area

        [x_coord, y_coord, new_layout, new_substation_coords, farm_area] = new_farm()


        field_names = ['a_farm']
        description = ['Area of the wind farm']
        data = {field_names[0]: [farm_area, description[0]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in data.items():
                writer.writerow([key, value[0], value[1]])
        csvfile.close()

        #print 'farm_area:', farm_area


        outputs['farm_area'] = farm_area
        outputs['new_layout'] = new_layout
        outputs['x_coord'] = x_coord
        outputs['y_coord'] = y_coord
        outputs['new_substation_coords'] = new_substation_coords
