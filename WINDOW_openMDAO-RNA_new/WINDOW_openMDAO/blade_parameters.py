'''
Reads the OpenFast AeroDyn-blade file for the IEA 10 MW turbine and returns blade spans,
blade chord and twist at pegged nodes
'''

import pandas as pd
abs_path = 'Input//'
file = 'IEA-10.0-198-RWT_AeroDyn15_blade.dat'

filename = abs_path + file

df = pd.read_csv(filename, delim_whitespace=True,skiprows=6, index_col=False,
                 names=['span', 'curve', 'sweep', 'curveangle', 'Twist', 'Chord', 'Airfoil_id'])


blade_span = []

for idx in range(30):
    blade_span.append(df['span'][idx])

blade_section = [r/blade_span[-1] for r in blade_span] #blade sections

nodes_chord = [0, 0.7, 0.9]
nodes_twist = [0, 0.4, 0.7]

pegged_chord = []
pegged_twist = []

for idx in range(len(nodes_chord)):
    diff = [sec - nodes_chord[idx] for sec in blade_section ]
    diff = [abs(diff) for diff in diff]
    index = diff.index(min(diff))
    pegged_chord.append(df['Chord'][index])

for idx in range(len(nodes_twist)):
    diff = [sec - nodes_twist[idx] for sec in blade_section]
    diff = [abs(diff) for diff in diff]
    index = diff.index(min(diff))
    pegged_twist.append(df['Twist'][index])










