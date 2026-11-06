from collections.abc import Callable

import aastex
import astropy.units as u
import numpy as np
import pytest

import esis_muram_paper


@pytest.mark.parametrize(
    argnames="factory,kind",
    argvalues=[
        (esis_muram_paper.figures.overview, aastex.FigureStar),
        (esis_muram_paper.figures.event, aastex.FigureStar),
        (esis_muram_paper.figures.widths, aastex.Figure),
    ],
)
def test_figure(factory: Callable[[], aastex.Figure], kind: type):
    """Each figure is drawn, as the kind of figure it is."""
    assert isinstance(factory(), kind)


def test_widths():
    """The simulation is narrower than the observed width, and wider than its thermal width alone."""
    module = esis_muram_paper.figures._widths
    observed = module.sigma_observed()
    assert 20 * u.km / u.s < observed < 30 * u.km / u.s
    for binning in module.binnings:
        sigma, _ = module.width(binning)
        median = np.median(sigma).ndarray
        assert module.sigma_thermal() < median < observed
