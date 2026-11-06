import astropy.units as u
import numpy as np
import pytest

import esis_muram_paper


@pytest.mark.parametrize(
    argnames="line,log_temperature",
    argvalues=[
        (esis_muram_paper.O_V, 5.4),
        (esis_muram_paper.Mg_X, 6.1),
    ],
)
class TestLine:
    def test_contribution(self, line: "esis_muram_paper.Line", log_temperature: float):
        """The contribution function peaks at the temperature at which the ion forms."""
        simulation = esis_muram_paper.simulation()
        g = esis_muram_paper.contribution(line)
        assert np.abs(g.inputs - line.wavelength) < 0.01 * u.AA
        index = np.argmax(g.outputs, axis=simulation.axis_temperature)
        peak = np.log10(simulation.temperature[index].ndarray / u.K)
        assert np.isclose(peak, log_temperature)

    def test_bins(self, line: "esis_muram_paper.Line", log_temperature: float):
        """The bins which emit the line hold its peak and leave out the rest."""
        simulation = esis_muram_paper.simulation()
        bins = esis_muram_paper.bins(line)
        temperature = simulation.temperature[{simulation.axis_temperature: bins}]
        log = np.log10(temperature.ndarray / u.K)
        assert log.min() < log_temperature < log.max()
        assert bins.stop - bins.start < simulation.temperature.size
