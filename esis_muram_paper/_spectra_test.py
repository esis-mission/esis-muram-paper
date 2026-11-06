import astropy.constants
import astropy.units as u
import named_arrays as na
import numpy as np

import esis_muram_paper


def test_binned():
    """Binning keeps the sum, and leaves out the elements past the last whole block."""
    a = na.ScalarArray(np.arange(30.0).reshape(5, 6), axes=("x", "y"))
    result = esis_muram_paper.binned(a, factor=2, axes=("x", "y"))
    assert result.shape == {"x": 2, "y": 3}
    assert result.sum() == a[{"x": slice(0, 4)}].sum()


def test_radiance():
    """The fast plasma is part of the radiance, and the mean velocities lie within the bins."""
    line = esis_muram_paper.O_V
    total = esis_muram_paper.radiance(line)
    fast = esis_muram_paper.radiance_blue(line) + esis_muram_paper.radiance_red(line)
    assert np.all(fast <= total * (1 + 1e-6))
    assert 0 < (fast.sum() / total.sum()).ndarray < 0.1
    centroid = esis_muram_paper.centroid(line)
    shift = esis_muram_paper.simulation().shift
    assert np.all(np.abs(centroid) <= np.abs(shift).max())


def test_spectrum():
    """The spectrum of the mean of the box, summed over its bins, is the mean radiance of the box."""
    line = esis_muram_paper.O_V
    simulation = esis_muram_paper.simulation()
    em = simulation.emission_measure.mean(simulation.axis_xy)
    spectrum = esis_muram_paper.spectrum(line, em)
    axis = esis_muram_paper.axis_velocity
    velocity = esis_muram_paper.velocity
    width = velocity[{axis: slice(1, None)}] - velocity[{axis: slice(None, -1)}]
    width = (width / astropy.constants.c * line.wavelength).to(u.AA)
    result = (spectrum.outputs * width).sum(axis)
    expected = esis_muram_paper.radiance(line).mean()
    assert np.isclose(result.ndarray, expected.ndarray, rtol=1e-3)
