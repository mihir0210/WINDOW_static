"""
Simple B-spline component for interpolation.
"""
from six import string_types

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix

from openmdao.core.explicitcomponent import ExplicitComponent
from openmdao.utils.array_utils import tile_sparse_jac

CITATIONS = """
@conference {Hwang2012c,
        title = {GeoMACH: Geometry-Centric MDAO of Aircraft Configurations with High Fidelity},
        booktitle = {Proceedings of the 14th AIAA/ISSMO Multidisciplinary Analysis Optimization
                     Conference},
        year = {2012},
        note = {<p>AIAA 2012-5605</p>},
        month = {September},
        address = {Indianapolis, IN},
        author = {John T. Hwang and Joaquim R. R. A. Martins}
}
"""


def get_bspline_mtx(num_cp, num_pt, order=4, distribution='sine'):
    """
    Compute matrix of B-spline coefficients.

    Parameters
    ----------
    num_cp : int
        Number of control points.
    num_pt : int
        Number of interpolated points.
    order : int(4)
        B-spline order.
    distribution : str
        Choice of spatial distribution to use for placing the control points. It can be 'sine' or
        'uniform'.

    Returns
    -------
    csr_matrix
        Sparse matrix of B-spline coefficients.
    """
    knots = np.zeros(num_cp + order)
    knots[order - 1:num_cp + 1] = np.linspace(0, 1, num_cp - order + 2)
    knots[num_cp + 1:] = 1.0

    t_vec = np.linspace(0, 1, num_pt)
    if distribution == 'uniform':
        pass
    elif distribution == 'sine':
        t_vec = 0.5 * (1.0 + np.sin(-0.5 * np.pi + t_vec * np.pi))

    basis = np.zeros(order)
    arange = np.arange(order)
    data = np.zeros((num_pt, order))
    rows = np.zeros((num_pt, order), int)
    cols = np.zeros((num_pt, order), int)

    for ipt in range(num_pt):
        t = t_vec[ipt]

        i0 = -1
        for ind in range(order, num_cp + 1):
            if (knots[ind - 1] <= t) and (t < knots[ind]):
                i0 = ind - order
        if t == knots[-1]:
            i0 = num_cp - order

        basis[:] = 0.
        basis[-1] = 1.

        for i in range(2, order + 1):
            ll = i - 1
            j1 = order - ll
            j2 = order
            n = i0 + j1
            if knots[n + ll] != knots[n]:
                basis[j1 - 1] = (knots[n + ll] - t) / (knots[n + ll] - knots[n]) * basis[j1]
            else:
                basis[j1 - 1] = 0.
            for j in range(j1 + 1, j2):
                n = i0 + j
                if knots[n + ll - 1] != knots[n - 1]:
                    basis[j - 1] = (t - knots[n - 1]) / \
                        (knots[n + ll - 1] - knots[n - 1]) * basis[j - 1]
                else:
                    basis[j - 1] = 0.
                if knots[n + ll] != knots[n]:
                    basis[j - 1] += (knots[n + ll] - t) / (knots[n + ll] - knots[n]) * basis[j]
            n = i0 + j2
            if knots[n + ll - 1] != knots[n - 1]:
                basis[j2 - 1] = (t - knots[n - 1]) / \
                    (knots[n + ll - 1] - knots[n - 1]) * basis[j2 - 1]
            else:
                basis[j2 - 1] = 0.

        data[ipt, :] = basis
        rows[ipt, :] = ipt
        cols[ipt, :] = i0 + arange

    data, rows, cols = data.flatten(), rows.flatten(), cols.flatten()

    return csr_matrix((data, (rows, cols)), shape=(num_pt, num_cp))


class BsplinesComp(ExplicitComponent):
    """
    Simple B-spline component for interpolation.

    Attributes
    ----------
    cite : str
        Listing of relevant citations that should be referenced when publishing
        work that uses this class.
    """

    def __init__(self, **kwargs):
        """
        Initialize the BsplinesComp.

        Parameters
        ----------
        **kwargs : dict of keyword arguments
            Keyword arguments that will be mapped into the Component options.
        """
        super(BsplinesComp, self).__init__(**kwargs)

        self.cite = CITATIONS

    def initialize(self):
        """
        Declare options.
        """
        self.options.declare('num_control_points', types=int, default=10,
                             desc="Number of control points.")
        self.options.declare('num_points', types=int, default=20,
                             desc="Number of interpolated points.")
        self.options.declare('vec_size', types=int, default=1,
                             desc='The number of independent rows to interpolate.')
        self.options.declare('bspline_order', 4, types=int, desc="B-spline order.")
        self.options.declare('in_name', types=str, default='h_cp',
                             desc="Name to use for the input variable (control points).")
        self.options.declare('out_name', types=str, default='h',
                             desc="Name to use for the output variable (interpolated points).")
        self.options.declare('units', types=string_types, default=None, allow_none=True,
                             desc="Units to use for the input and output variables.")
        self.options.declare('distribution', default='sine', values=['uniform', 'sine'],
                             desc="Choice of spatial distribution to use for placing the control "
                                  "points. It can be 'sine' or 'uniform'.")

    def setup(self):
        """
        Set up the B-spline component.
        """
        opts = self.options
        num_control_points = opts['num_control_points']
        num_points = opts['num_points']
        vec_size = opts['vec_size']
        in_name = opts['in_name']
        out_name = opts['out_name']
        units = opts['units']

        self.add_input(in_name, val=np.random.rand(vec_size, num_control_points), units=units)
        self.add_output(out_name, val=np.random.rand(vec_size, num_points), units=units)

        jac = get_bspline_mtx(num_control_points, num_points,
                              order=opts['bspline_order'],
                              distribution=opts['distribution']).tocoo()

        data, rows, cols = tile_sparse_jac(jac.data, jac.row, jac.col,
                                           num_points, num_control_points, vec_size)

        self.jac = csc_matrix((data, (rows, cols)),
                              shape=(vec_size * num_points, vec_size * num_control_points))

        self.declare_partials(of=out_name, wrt=in_name, val=data, rows=rows, cols=cols)

        self.set_check_partial_options('*', method='cs')

    def compute(self, inputs, outputs):
        """
        Compute values at the B-spline interpolation points.

        Parameters
        ----------
        inputs : `Vector`
            `Vector` containing inputs.
        outputs : `Vector`
            `Vector` containing outputs.
        """
        opts = self.options
        num_control_points = opts['num_control_points']
        num_points = opts['num_points']
        vec_size = opts['vec_size']

        out_shape = (vec_size, num_points)
        in_shape = (vec_size, num_control_points)

        out = self.jac * inputs[opts['in_name']].reshape(np.prod(in_shape))
        outputs[opts['out_name']] = out.reshape(out_shape)
