import functools

import aastex
import astropy.constants
import astropy.units as u
import fiasco
import matplotlib.pyplot as plt
import named_arrays as na
import numpy as np

import esis_muram_paper

__all__ = [
    "angle",
    "binnings",
    "sigma_observed",
    "sigma_thermal",
    "temperature_peak",
    "width",
    "widths",
    "xi_observed",
]

xi_observed = 30 * u.km / u.s
"""
The nonthermal velocity, as the most probable speed, of the quiet transition
region near :math:`3 \\times 10^5\\,\\mathrm{K}`, the peak of the
nonthermal velocities measured with SUMER by Chae et al. (1998).
"""

binnings = (4, 8)
"""
How many pixels of the simulation wide the blocks are into which its spectra
are binned, about one and two seconds of arc.
"""

_fwhm_per_sigma = 2 * np.sqrt(2 * np.log(2))
"""The full width at half maximum of a Gaussian, over its standard deviation."""


def angle(length: u.Quantity) -> u.Quantity:
    """
    The angle that `length` subtends at the center of the disk, seen from
    one astronomical unit away from the center of the Sun.

    Parameters
    ----------
    length
        A length on the surface of the Sun.
    """
    distance = astropy.constants.au - astropy.constants.R_sun
    return (length / distance).to(u.arcsec, equivalencies=u.dimensionless_angles())


def _mass() -> u.Quantity:
    """The mass of an ion of O V."""
    return fiasco.Ion(esis_muram_paper.O_V.ion, 1e5 * u.K).mass


def temperature_peak() -> u.Quantity:
    """The temperature of the bin of the simulation at which O V is brightest per unit emission measure."""
    simulation = esis_muram_paper.simulation()
    axis = simulation.axis_temperature
    g = esis_muram_paper.contribution(esis_muram_paper.O_V).outputs
    index = np.argmax(g, axis=axis)
    return simulation.temperature[index].ndarray


def sigma_observed() -> u.Quantity:
    """
    The width of O V observed in the quiet Sun, as a standard deviation:
    :data:`xi_observed` over :math:`\\sqrt{2}` added in quadrature to the
    thermal width at :func:`temperature_peak`.
    """
    thermal = astropy.constants.k_B * temperature_peak() / _mass()
    result = np.sqrt(np.square(xi_observed) / 2 + thermal)
    return result.to(u.km / u.s)


@functools.cache
def sigma_thermal() -> u.Quantity:
    """
    The thermal width of O V over the whole box, as a standard deviation:
    the thermal widths of the bins of temperature averaged in quadrature,
    weighted by the radiance of O V from each.
    """
    simulation = esis_muram_paper.simulation()
    line = esis_muram_paper.O_V
    axis = simulation.axis_temperature
    index = {axis: esis_muram_paper.bins(line)}
    others = (simulation.axis_shift, *simulation.axis_xy)
    em = simulation.emission_measure[index].sum(others)
    weight = esis_muram_paper.contribution(line).outputs[index] * em
    thermal = astropy.constants.k_B * simulation.temperature[index] / _mass()
    result = np.sqrt((weight * thermal).sum(axis) / weight.sum(axis))
    return result.ndarray.to(u.km / u.s)


@functools.cache
def width(binning: None | int) -> tuple[na.AbstractScalar, na.AbstractScalar]:
    """
    The width of O V, its full width at half maximum over that of a
    Gaussian of unit standard deviation, and its radiance, in each block of
    `binning` by `binning` pixels of the simulation, with the thermal width
    of each temperature.

    Parameters
    ----------
    binning
        How many pixels wide each block is.
        If :obj:`None`, the spectrum is the mean of the whole box.
    """
    simulation = esis_muram_paper.simulation()
    em = simulation.emission_measure
    axes = simulation.axis_xy
    if binning is None:
        em = em.mean(axes)
    else:
        em = esis_muram_paper.binned(em, binning, axes)
    spectrum = esis_muram_paper.spectrum(esis_muram_paper.O_V, em)
    axis = esis_muram_paper.axis_velocity
    velocity = esis_muram_paper.velocity.cell_centers(axis)
    fwhm = na.pdf.fwhm(velocity, spectrum.outputs, axis=axis)
    return fwhm / _fwhm_per_sigma, spectrum.outputs.sum(axis)


def widths() -> aastex.Figure:
    """
    The widths of O V synthesized from the simulation, with their thermal
    widths, against the width observed in the quiet Sun.
    """
    observed = sigma_observed().to_value(u.km / u.s)
    thermal = sigma_thermal().to_value(u.km / u.s)
    pitch = esis_muram_paper.simulation().pitch

    fig, axs = plt.subplots(
        nrows=2,
        figsize=(aastex.column_width_inches, 1.3 * aastex.column_width_inches),
        constrained_layout=True,
    )

    ax = axs[0]
    bins = np.arange(8, 40.5, 0.5)
    colors = [esis_muram_paper.color_blue, esis_muram_paper.color_red]
    for binning, color in zip(binnings, colors):
        sigma, radiance = width(binning)
        radiance = radiance.ndarray.value.ravel()
        size = angle(binning * pitch).to_value(u.arcsec)
        ax.hist(
            sigma.ndarray.to_value(u.km / u.s).ravel(),
            bins=bins,
            weights=radiance / radiance.sum(),
            histtype="step",
            color=color,
            label=rf"${size:.1f}''$ blocks",
        )
    ax.axvline(observed, color="black", linestyle="--", linewidth=0.8)
    ax.annotate(
        "observed",
        xy=(observed, 0.95),
        xycoords=("data", "axes fraction"),
        xytext=(3, 0),
        textcoords="offset points",
        va="top",
        fontsize=7,
    )
    ax.axvline(thermal, color="0.5", linestyle=":", linewidth=0.8)
    ax.annotate(
        "thermal",
        xy=(thermal, 0.95),
        xycoords=("data", "axes fraction"),
        xytext=(-3, 0),
        textcoords="offset points",
        va="top",
        ha="right",
        fontsize=7,
    )
    ax.set_xlabel(r"width, FWHM$/2.355$ (km\,s$^{-1}$)")
    ax.set_ylabel("fraction of the radiance")
    ax.legend(frameon=False, fontsize=7, loc="center right")

    ax = axs[1]
    axis = esis_muram_paper.axis_velocity
    simulation = esis_muram_paper.simulation()
    em = simulation.emission_measure.mean(simulation.axis_xy)
    spectrum = esis_muram_paper.spectrum(esis_muram_paper.O_V, em).outputs
    velocity = esis_muram_paper.velocity.cell_centers(axis)
    v = velocity.ndarray.to_value(u.km / u.s)
    profile = (spectrum / spectrum.max()).ndarray.to_value(u.dimensionless_unscaled)
    mean = (velocity * spectrum).sum(axis) / spectrum.sum(axis)
    mean = mean.ndarray.to_value(u.km / u.s)
    ax.plot(
        v,
        profile,
        color=esis_muram_paper.color_blue,
        label="simulation",
    )
    ax.plot(
        v,
        np.exp(-np.square((v - mean) / observed) / 2),
        color="black",
        linestyle="--",
        linewidth=0.8,
        label="observed width",
    )
    ax.set_xlim(-120, 120)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"line-of-sight velocity (km\,s$^{-1}$)")
    ax.set_ylabel(r"O\,\textsc{v} spectrum over its peak")
    ax.legend(frameon=False, fontsize=7, loc="upper left")

    result = aastex.Figure("fig:widths", position="t")
    result.add_fig(fig, width=None)
    result.add_caption(aastex.NoEscape(r"""
Top: the widths of \OV\ \SI{630}{\angstrom} synthesized from the simulation, each the full width at half
maximum over that of a Gaussian of unit standard deviation, in blocks of \widthsBlockSmall\ and
\widthsBlockLarge, weighted by their radiance.
The dashed line is the width observed in the quiet Sun, \widthsObserved, the nonthermal velocity of
\citet{Chae1998}, \widthsXi, over $\sqrt{2}$ added in quadrature to the thermal width at
\widthsTemperature, and the dotted line is the thermal width of the simulation alone,
\widthsThermal.
Bottom: the mean spectrum of \OV\ over the whole box, whose width is \widthsBox, against a Gaussian of
the observed width.
"""))
    return result
