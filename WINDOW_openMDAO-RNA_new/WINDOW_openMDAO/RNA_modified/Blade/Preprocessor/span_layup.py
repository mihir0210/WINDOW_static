'''
Define function to convert from variables to mat file with interpolated values of thicknesses
along the span
'''

import numpy as np
import scipy.io

def span_layup(span_radius, span_section, web, skin, root, le_core1, spar1, te_core1, te_reinf1, le_core2, spar2,
               te_core2, te_reinf2,
               le_core3, spar3, te_core3, te_reinf3, le_core4, spar4, te_core4):
    section = np.array([0, 0.025, 0.11, 0.3, 0.5, 0.75, 0.95, 1]).reshape(1, 8).astype(float)

    #### Root ends at 0.15 ####
    #### TE reinf ends at 0.75 ####
    #### Spar caps, le core and te core end at 0.95 ####
    #### Skin goes throughout the blade ####

    le_core = np.array([0, 0, le_core1, le_core2, le_core3, le_core4, 0, 0]).reshape(1, 8).astype(float)
    te_core = np.array([0, 0, te_core1, te_core2, te_core3, te_core4, 0, 0]).reshape(1, 8).astype(float)
    spar = np.array([0, 0, spar1, spar2, spar3, spar4, 0, 0]).reshape(1, 8).astype(float)
    te_reinf = np.array([0, 0, te_reinf1, te_reinf2, te_reinf3, 0, 0, 0]).reshape(1, 8).astype(float)
    skin = np.array([skin, skin, skin, skin, skin, skin, skin, skin]).reshape(1, 8).astype(float)

    root_section = np.array([0, 0.022, 0.025, 0.15, 0.3, 0.5, 0.75, 0.95, 1]).reshape(1, 9).astype(float)
    root = np.array([root[0], root[0], root[1], 0, 0, 0, 0, 0, 0]).reshape(1, 9).astype(float)

    web_section = np.array([0.05, 0.1, 0.3, 0.5, 0.8, 0.95, 1]).reshape(1, 7).astype(float)
    web = np.array([1, web, web, web, web, web, 1]).reshape(1, 7).astype(float)

    skin_span = np.interp(span_section[0, :], section[0, :], skin[0, :])
    root_span = np.interp(span_section[0, :], root_section[0, :], root[0, :])
    web_span = np.interp(span_section[0, :], web_section[0, :], web[0, :])
    le_core_span = np.interp(span_section[0, :], section[0, :], le_core[0, :])
    spar_span = np.interp(span_section[0, :], section[0, :], spar[0, :])
    te_core_span = np.interp(span_section[0, :], section[0, :], te_core[0, :])
    te_reinf_span = np.interp(span_section[0, :], section[0, :], te_reinf[0, :])

    scipy.io.savemat('Internal_layup.mat', dict(skin_span=skin_span, root_span=root_span,
                                                web_span=web_span, le_core_span=le_core_span,
                                                spar_span=spar_span, te_core_span=te_core_span,
                                                te_reinf_span=te_reinf_span, span_radius=span_radius))


