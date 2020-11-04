.. _feature_MetaModelStructuredComp:

***********************
MetaModelStructuredComp
***********************

`MetaModelStructuredComp` is a smooth interpolation Component for data that exists on a regular, structured, grid.
This differs from :ref:`MetaModelUnStructured <feature_MetaModelUnStructuredComp>` which accepts unstructured data as collections of points.

`MetaModelStructuredComp` produces smooth fits through provided training data using polynomial
splines of order 1 (linear), 3 (cubic), or 5 (quintic). Analytic
derivatives are automatically computed.

Note that `MetaModelStructuredComp` only accepts scaler inputs and outputs. If you have a multivariable function, each
input variable needs its own named OpenMDAO input.

For multi-dimensional data, fits are computed
on a separable per-axis basis. If a particular dimension does not have
enough training data points to support a selected spline order (e.g. 3
sample points, but an order 5 quintic spline is specified), the order of the
fitted spline will be automatically reduced for that dimension alone.

Extrapolation is supported, but disabled by default. It can be enabled
via the :code:`extrapolate` option (see below).

MetaModelStructuredComp Options
-------------------------------

.. embed-options::
    openmdao.components.meta_model_structured_comp
    MetaModelStructuredComp
    options

MetaModelStructuredComp Examples
--------------------------------

A simple quick-start example is fitting the exclusive-or ("XOR") operator between
two inputs, `x` and `y`:

.. embed-code::
    openmdao.components.tests.test_meta_model_structured_comp.TestMetaModelStructuredCompMapFeature.test_xor
    :layout: code, output


An important consideration for multi-dimensional input is that the order in which
the input variables are added sets the expected dimension of the output
training data. For example, if inputs `x`, `y` and `z` are added to the component
with training data array lengths of 5, 12, and 20 respectively, and are added
in `x`, `y`, and `z` order, than the output training data must be an ndarray
with shape (5, 12, 20).

This is illustrated by the example:

.. embed-code::
    openmdao.components.tests.test_meta_model_structured_comp.TestMetaModelStructuredCompMapFeature.test_shape
    :layout: code, output

You can also predict multiple independent output points by setting the `vec_size` argument to be equal to the number of
points you want to predict. Here, we set it to 2 and predict 2 points with `MetaModelStructuredComp`:

.. embed-code::
    openmdao.components.tests.test_meta_model_structured_comp.TestMetaModelStructuredCompMapFeature.test_vectorized
    :layout: code, output


Finally, it is possible to compute gradients with respect to the given
output training data. These gradients are not computed by default, but
can be enabled by setting the option `training_data_gradients` to `True`.
When this is done, for each output that is added to the component, a
corresponding input is added to the component with the same name but with an
`_train` suffix. This allows you to connect in the training data as an input
array, if desired.

The following example shows the use of training data gradients. This is the
same example problem as above, but note `training_data_gradients` has been set
to `True`. This automatically creates an input named `f_train` when the output
`f` was added. The gradient of `f` with respect to `f_train` is also seen to
match the finite difference estimate in the `check_partials` output.

.. embed-code::
    openmdao.components.tests.test_meta_model_structured_comp.TestMetaModelStructuredCompMapFeature.test_training_derivatives
    :layout: code, output

.. tags:: MetaModelStructuredComp, Component
