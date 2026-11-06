import pathlib

import astropy.units as u
import numpy as np
import pytest

import esis_muram_paper


def test_simulation():
    """
    The snapshot is a box of 1024 pixels of 192 km on a side, seen through 24
    bins of temperature and 49 bins of velocity 10 km/s wide.
    """
    simulation = esis_muram_paper.simulation()
    assert isinstance(simulation, esis_muram_paper.Simulation)
    assert simulation.emission_measure.shape == {
        simulation.axis_temperature: 24,
        simulation.axis_shift: 49,
        simulation.axis_x: 1024,
        simulation.axis_y: 1024,
    }
    assert simulation.emission_measure.unit.is_equivalent(u.cm**-5)
    assert np.isclose(simulation.pitch, 192 * u.km)
    assert np.isclose(simulation.width_shift, 10 * u.km / u.s)
    assert np.all(simulation.emission_measure >= 0)


def test_archive_missing(tmp_path: pathlib.Path):
    """Without the archive, the error says where to put it."""
    with pytest.raises(FileNotFoundError, match="by hand"):
        esis_muram_paper.archive(tmp_path)


def test_archive_checksum(tmp_path: pathlib.Path):
    """An archive which is not the one that was sent is refused."""
    path = tmp_path / esis_muram_paper._muram._name_archive
    path.write_bytes(b"not the archive")
    with pytest.raises(ValueError, match="checksum"):
        esis_muram_paper.archive(tmp_path)
