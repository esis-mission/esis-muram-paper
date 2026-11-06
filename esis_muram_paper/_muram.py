"""
The MURaM simulation of the quiet Sun whose explosive events this article
studies.
"""

import dataclasses
import functools
import hashlib
import pathlib
import shutil
import tarfile

import astropy.units as u
import named_arrays as na
import numpy as np
import zarr

__all__ = [
    "Simulation",
    "archive",
    "directory_default",
    "simulation",
]

directory_default = pathlib.Path.home() / ".esis_muram_paper"
"""Where the data this article uses is kept."""

_name = "vdem_MURaM_QS_x_120000.zarr"
"""The name of the zarr store of the simulation, as it was sent."""

_name_archive = f"{_name}.tar.gz"
"""The name of the archive the zarr store was sent in."""

_sha256_archive = "9356a2335e49c8a34496281ff193a1c15b5befbd4a4a77c5f85f80f1a372701f"
"""The SHA-256 checksum of the archive :data:`_name_archive`."""


def _sha256(path: pathlib.Path) -> str:
    """The SHA-256 checksum of a file, read a piece at a time."""
    result = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(2**20), b""):
            result.update(chunk)
    return result.hexdigest()


def archive(directory: None | pathlib.Path = None) -> pathlib.Path:
    """
    The zarr store of the velocity differential emission measure (VDEM) of
    the simulation, unpacked from its archive the first time it is needed.

    The archive, :data:`_name_archive`, is the one M. Rempel sent in 2026
    June. It is not published yet, so it has to be put in `directory` by
    hand, or unpacked there already.

    Parameters
    ----------
    directory
        Where the archive, or the store unpacked from it, is kept.
        If :obj:`None` (the default), :data:`directory_default` is used.
    """
    if directory is None:
        directory = directory_default

    result = directory / _name
    if (result / ".zmetadata").exists():
        return result

    path = directory / _name_archive
    if not path.exists():
        raise FileNotFoundError(
            f"Neither {result} nor its archive {path} exists. "
            f"The simulation is not published yet, so put the archive there by hand."
        )

    sha256 = _sha256(path)
    if sha256 != _sha256_archive:
        raise ValueError(f"The checksum of {path} is {sha256}, not {_sha256_archive}.")

    # Unpacked beside the result and moved into place last, so that an
    # unpacking which was interrupted is redone.
    partial = directory / f"{_name}.partial"
    shutil.rmtree(partial, ignore_errors=True)
    partial.mkdir(parents=True)
    with tarfile.open(path) as tar:
        tar.extractall(partial, filter="data")
    (partial / _name).rename(result)
    partial.rmdir()

    return result


@dataclasses.dataclass(frozen=True)
class Simulation:
    """
    The velocity differential emission measure of one snapshot of the
    simulation, along vertical lines of sight through every pixel.
    """

    time: u.Quantity
    """The time of the snapshot, since the simulation began."""

    temperature: na.ScalarArray
    """
    The temperature at the center of each bin of temperature, along
    :attr:`axis_temperature`. The bins are a tenth of a decade wide.
    """

    shift: na.ScalarArray
    """
    The line-of-sight velocity at the center of each bin of velocity, along
    :attr:`axis_shift`.

    The archive does not say which way is positive. This article takes
    positive velocities as away from the observer, which puts the redshift
    of the transition region, averaged over the box, on the red side, as it
    is observed.
    """

    position: na.Cartesian2dVectorArray
    """
    The horizontal position of the center of each pixel, along :attr:`axis_x`
    and :attr:`axis_y`.
    """

    emission_measure: na.ScalarArray
    """
    The emission measure of each pixel in each bin of temperature and of
    velocity, along :attr:`axis_temperature`, :attr:`axis_shift`,
    :attr:`axis_x` and :attr:`axis_y`.
    """

    axis_temperature: str = "temperature"
    """The name of the axis of :attr:`temperature`."""

    axis_shift: str = "shift"
    """The name of the axis of :attr:`shift`."""

    axis_x: str = "x"
    """The name of the axis along which :attr:`position` changes in `x`."""

    axis_y: str = "y"
    """The name of the axis along which :attr:`position` changes in `y`."""

    @property
    def axis_xy(self) -> tuple[str, str]:
        """The names of the two horizontal axes, :attr:`axis_x` and :attr:`axis_y`."""
        return self.axis_x, self.axis_y

    @property
    def width_shift(self) -> u.Quantity:
        """The width of each bin of :attr:`shift`."""
        shift = self.shift
        axis = self.axis_shift
        width = shift[{axis: slice(1, None)}] - shift[{axis: slice(None, -1)}]
        return np.mean(width).ndarray

    @property
    def pitch(self) -> u.Quantity:
        """The width of each pixel."""
        x = self.position.x
        axis = self.axis_x
        width = x[{axis: slice(1, None)}] - x[{axis: slice(None, -1)}]
        return np.mean(width).ndarray

    @property
    def width(self) -> u.Quantity:
        """The width of the box, from the first edge of its pixels to the last."""
        return self.pitch * self.position.x.shape[self.axis_x]


@functools.cache
def simulation(directory: None | pathlib.Path = None) -> Simulation:
    """
    The snapshot of the simulation, read from the store :func:`archive`
    returns.

    The emission measure is kept in single precision, as it is stored, since
    it is several gigabytes.

    Parameters
    ----------
    directory
        Where the archive, or the store unpacked from it, is kept.
        If :obj:`None` (the default), :data:`directory_default` is used.
    """
    store = zarr.open_group(archive(directory), mode="r")
    vdem = store["vdem"]

    dimensions = vdem.attrs["_ARRAY_DIMENSIONS"]
    if dimensions != ["logT", "vdop", "x", "y"]:
        raise ValueError(f"unexpected axes of the emission measure, {dimensions}")
    unit = vdem.attrs["units"]
    if unit != "1e27 / cm5":
        raise ValueError(f"unexpected unit of the emission measure, {unit!r}")

    axis_temperature = Simulation.axis_temperature
    axis_shift = Simulation.axis_shift
    axis_x = Simulation.axis_x
    axis_y = Simulation.axis_y

    # The archive gives the positions from 0 in steps of one pixel, which
    # are taken here as the centers of the pixels.
    return Simulation(
        time=store["Time"][()] * u.s,
        temperature=10 ** na.ScalarArray(store["logT"][:], axes=axis_temperature) * u.K,
        shift=na.ScalarArray(store["vdop"][:] * u.km / u.s, axes=axis_shift),
        position=na.Cartesian2dVectorArray(
            x=na.ScalarArray((store["x"][:] * u.cm).to(u.Mm), axes=axis_x),
            y=na.ScalarArray((store["y"][:] * u.cm).to(u.Mm), axes=axis_y),
        ),
        emission_measure=na.ScalarArray(
            vdem[:] << (1e27 * u.cm**-5),
            axes=(axis_temperature, axis_shift, axis_x, axis_y),
        ),
    )
