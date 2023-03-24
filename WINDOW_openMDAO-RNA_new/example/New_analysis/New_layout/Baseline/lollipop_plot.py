
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

#### Cost comparison of the 10-190 with the 20-270 turbine in an offshore wind farm #####



df = pd.DataFrame()

cost_rotor = 2094120*100*0.88
cost_nacelle = 4051063*100*0.88
cost_tower = 826770*100
other_turbine = 267194235
cost_foundation = (1155582 + 489792)*100
cost_inst_turbine = 85972031
cost_inst_foundation = 71250000
other_costs = 205247775
project_dev = 102623887
oandm =  6.4001e+08
decom =  1.0158e+08
cables = 52118921 + 152100000
substation = 334100000 - 152100000
cost_inst_electrical = 100941774

data_10MW = [cost_rotor, cost_nacelle, cost_tower, other_turbine, cost_foundation, cost_inst_turbine, cost_inst_foundation, other_costs, project_dev, oandm, decom,
        cables, substation, cost_inst_electrical]


perc_share_10MW = [a*100/sum(data_10MW) for a in data_10MW]

df['10MW'] = data_10MW
df['perc_share_10MW'] = perc_share_10MW
#############################

cost_rotor = 5288135*50*0.88
cost_nacelle = 10712847*50*0.88
cost_tower = 2696858.7427*50
other_turbine = 359522642
cost_foundation = (2586339 + 1066062)*50
cost_inst_turbine = 66029765.625
cost_inst_foundation = 50625000
other_costs = 239719855
project_dev = 119859927
oandm = 5.2341e+08
decom =  9.8243e+07
cables = 76590212 + 152100000
substation = 334100000 - 152100000
cost_inst_electrical = 88768587


data_20MW = [cost_rotor, cost_nacelle, cost_tower, other_turbine, cost_foundation, cost_inst_turbine, cost_inst_foundation, other_costs, project_dev, oandm, decom,
        cables, substation, cost_inst_electrical]

perc_share_20MW = [a*100/sum(data_20MW) for a in data_20MW]

df['20MW'] = data_20MW
df['perc_share_20MW'] = perc_share_20MW



##### lollipop plot ##########

fig,ax = plt.subplots(figsize=(12.5,4.5))

spacing = 0.3
y = np.linspace(0,13,14)
ticknames = ['Rotor', 'Nacelle', 'Tower', 'Other turbine', 'Foundation', 'Inst. turbine', 'Inst. foundation', 'Other Inst. Commission', 'Project Dev.', 'O&M', 'Decom.', 'Cables', 'Substation', 'Inst. Electrical']
new_ticknames = list(reversed(ticknames))
plt.hlines(y=y, xmin=0, xmax=df['perc_share_10MW'], color='skyblue')
plt.hlines(y=y+spacing, xmin=0, xmax=df['perc_share_20MW'], color='red')
plt.plot(df['perc_share_10MW'], y, "o", c = 'skyblue', label='10MW')
plt.plot(df['perc_share_20MW'], y+spacing, "o", c = 'red', label='20MW')
plt.yticks(y, ticknames, rotation = 0, fontsize = 12)
plt.xlabel('% Share', fontsize = 16)
plt.legend()
plt.savefig('cost_comparison.png',bbox_inches='tight',dpi=300)
plt.show()
