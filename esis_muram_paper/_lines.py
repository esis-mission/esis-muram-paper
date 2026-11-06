"""
The spectral lines of ESIS which this article synthesizes from the simulation.
"""

import dataclasses
import functools

import astropy.units as u
import fiasco
import named_arrays as na
import numpy as np
import utu

import esis_muram_paper

__all__ = [
    "O_V",
    "Line",
    "Mg_X",
    "bins",
    "contribution",
    "pressure",
]

pressure = 1e15 * u.K / u.cm**3
"""
The electron pressure, over Boltzmann's constant, at which the contribution
functions are computed, a typical pressure of the quiet transition region.
"""

fraction_contribution = 1e-3
"""
The fraction of its peak below which the contribution function of a line is
taken as zero, so that only the bins of temperature which emit the line are
synthesized.
"""


@dataclasses.dataclass(frozen=True)
class Line:
    """A spectral line of an ion."""

    ion: str
    """The name of the ion, as :class:`fiasco.Ion` takes it."""

    wavelength: u.Quantity
    """The rest wavelength of the line, to pick its transition with."""

    label: str
    """The name of the line, in LaTeX, using the macros of the preamble."""

    label_plot: str
    """The name of the line, in plain LaTeX, for the labels of the figures."""


O_V = Line(
    ion="O 5",
    wavelength=629.73 * u.AA,
    label=r"\OV\ \SI{630}{\angstrom}",
    label_plot=r"O\,\textsc{v} 630\,\AA{}",
)
"""The line of the transition region that ESIS was designed around."""

Mg_X = Line(
    ion="Mg 10",
    wavelength=624.94 * u.AA,
    label=r"\MgX\ \SI{625}{\angstrom}",
    label_plot=r"Mg\,\textsc{x} 625\,\AA{}",
)
"""The line of the corona closest to :data:`O_V` in the passband of ESIS."""


@functools.cache
def contribution(line: Line) -> na.FunctionArray:
    """
    The contribution function of `line` at the center of each bin of
    temperature of the simulation, at :data:`pressure`.

    Parameters
    ----------
    line
        The line to compute the contribution function of.
    """
    simulation = esis_muram_paper.simulation()
    temperature = simulation.temperature

    ion = fiasco.Ion(line.ion, temperature.ndarray)
    result = utu.spectrum.contribution_function(
        ion=ion,
        density=pressure / temperature,
        axis_temperature=simulation.axis_temperature,
    )

    distance = np.abs(result.inputs - line.wavelength)
    index = np.argmin(distance, axis="line")
    if distance[index] > 0.01 * u.AA:
        raise ValueError(
            f"no transition of {line.ion} within 0.01 A of {line.wavelength}"
        )
    return result[index]


@functools.cache
def bins(line: Line) -> slice:
    """
    The bins of temperature of the simulation which emit `line`: the run of
    bins outside of which its :func:`contribution` is less than
    :data:`fraction_contribution` of its peak.

    Parameters
    ----------
    line
        The line whose bins are wanted.
    """
    g = contribution(line).outputs
    keep = (g >= fraction_contribution * g.max()).ndarray
    first = int(np.argmax(keep))
    last = len(keep) - int(np.argmax(keep[::-1]))
    return slice(first, last)
