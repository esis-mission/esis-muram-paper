"""
Drawing maps of the simulation, shared by the figures.
"""

import astropy.units as u
import matplotlib.axes
import matplotlib.image
import named_arrays as na
import numpy as np

import esis_muram_paper

__all__ = [
    "image",
]


def image(
    ax: matplotlib.axes.Axes,
    a: na.AbstractScalar,
    window: None | dict[str, slice] = None,
    **kwargs,
) -> matplotlib.image.AxesImage:
    """
    Draw a map of the simulation at its full resolution, with `x` across and
    `y` up, in megameters.

    The pixels are embedded as they are, not resampled, so that a printed
    figure keeps the resolution of the simulation.

    Parameters
    ----------
    ax
        The axes to draw on.
    a
        The map, along the horizontal axes of the simulation. If it carries
        a unit, it must be dimensionless.
    window
        The part of the simulation to draw, as slices along its horizontal
        axes. If :obj:`None` (the default), the whole box is drawn.
    kwargs
        Passed on to :meth:`matplotlib.axes.Axes.imshow`.
    """
    simulation = esis_muram_paper.simulation()
    axis_x, axis_y = simulation.axis_xy
    if window is None:
        window = {axis_x: slice(None), axis_y: slice(None)}

    x = simulation.position.x[{axis_x: window[axis_x]}].ndarray.to_value(u.Mm)
    y = simulation.position.y[{axis_y: window[axis_y]}].ndarray.to_value(u.Mm)
    half = simulation.pitch.to_value(u.Mm) / 2

    a = a[window].explicit
    values = a.ndarray_aligned((axis_y, axis_x))
    values = u.Quantity(values).to_value(u.dimensionless_unscaled)

    return ax.imshow(
        np.asarray(values, dtype=float),
        origin="lower",
        interpolation="none",
        extent=(x.min() - half, x.max() + half, y.min() - half, y.max() + half),
        **kwargs,
    )
