"""Define the DenseMatrix class."""
from __future__ import division, print_function
import numpy as np
from numpy import ndarray
from six import iteritems

from scipy.sparse import coo_matrix

from openmdao.matrices.coo_matrix import COOMatrix

# NOTE: DenseMatrix is inherited from COOMatrix so that we can easily handle use cases
#       where partials overlap the same matrix entries, as in the case of repeated
#       src_indices entries.  This does require additional memory above storing just
#       the dense matrix, but it's worth it because the code is simpler and more robust.


class DenseMatrix(COOMatrix):
    """
    Dense global matrix.
    """

    def _build(self, num_rows, num_cols, in_ranges, out_ranges):
        """
        Allocate the matrix.

        Parameters
        ----------
        num_rows : int
            number of rows in the matrix.
        num_cols : int
            number of cols in the matrix.
        in_ranges : dict
            Maps input var name to column range.
        out_ranges : dict
            Maps output var name to row range.
        """
        super(DenseMatrix, self)._build(num_rows, num_cols, in_ranges, out_ranges)
        self._coo = self._matrix

    def _prod(self, in_vec, mode, ranges, mask=None):
        """
        Perform a matrix vector product.

        Parameters
        ----------
        in_vec : ndarray[:]
            incoming vector to multiply.
        mode : str
            'fwd' or 'rev'.
        ranges : (int, int, int, int)
            Min row, max row, min col, max col for the current system.
        mask : ndarray of type bool, or None
            Array used to mask out part of the input vector.

        Returns
        -------
        ndarray[:]
            vector resulting from the product.
        """
        # when we have a derivative based solver at a level below the
        # group that owns the AssembledJacobian, we need to use only
        # the part of the matrix that is relevant to the lower level
        # system.
        if ranges is None:
            mat = self._matrix
        else:
            rstart, rend, cstart, cend = ranges
            mat = self._matrix[rstart:rend, cstart:cend]

        if mode == 'fwd':
            if mask is None:
                return mat.dot(in_vec)
            else:
                inputs_masked = np.ma.array(in_vec, mask=mask)

                # Use the special dot product function from masking module so that we
                # ignore masked parts.
                return np.ma.dot(mat, inputs_masked)
        else:  # rev
            if mask is None:
                return mat.T.dot(in_vec)
            else:
                # Mask need to be applied to ext_mtx so that we can ignore multiplication
                # by certain columns.
                mat_T = mat.T
                arrmask = np.zeros(mat_T.shape, dtype=np.bool)
                arrmask[mask, :] = True
                masked_mtx = np.ma.array(mat_T, mask=arrmask, fill_value=0.0)

                masked_product = np.ma.dot(masked_mtx, in_vec).flatten()
                return np.ma.filled(masked_product, fill_value=0.0)

    def _create_mask_cache(self, d_inputs):
        """
        Create masking array for this matrix.

        Note: this only applies when this Matrix is an 'ext_mtx' inside of a
        Jacobian object.

        Parameters
        ----------
        d_inputs : Vector
            The inputs linear vector.

        Returns
        -------
        ndarray or None
            The mask array or None.
        """
        if len(d_inputs._views) > len(d_inputs._names):
            sub = d_inputs._names
            mask = np.ones(len(d_inputs), dtype=np.bool)
            for key, val in iteritems(self._metadata):
                if key[1] in sub:
                    mask[val[1]] = False

            return mask

    def _pre_update(self):
        """
        Do anything that needs to be done at the end of AssembledJacobian._update.
        """
        self._matrix = self._coo

    def _post_update(self):
        """
        Do anything that needs to be done at the end of AssembledJacobian._update.
        """
        # this will add any repeated entries together
        self._matrix = self._coo.toarray()
