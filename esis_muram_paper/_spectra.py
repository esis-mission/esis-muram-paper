"""
The radiance and the spectra of the lines of ESIS, synthesized from the
velocity differential emission measure of the simulation.
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
    "axis_velocity",
    "binned",
    "centroid",
    "radiance",
    "radiance_blue",
    "radiance_red",
    "radiance_shift",
    "spectrum",
    "speed_fast",
    "velocity",
]

speed_fast = 50 * u.km / u.s
"""
The line-of-sight speed beyond which plasma is counted as fast: the bins of
velocity of the simulation centered this far from rest or farther.
"""

axis_velocity = "velocity"
"""The name of the axis of :data:`velocity`."""

velocity = na.linspace(-300, 300, axis=axis_velocity, num=151) * u.km / u.s
"""
The vertices of the bins of velocity into which the spectra are synthesized,
wide enough to hold the fastest bin of the simulation and its thermal width.
"""

_unit_radiance = u.erg / (u.s * u.cm**2 * u.sr)
"""The unit of the radiance of a line."""

_size_chunk = 2**27
"""
The most elements, a gigabyte in double precision, that :func:`spectrum` puts
into the spectrum of one chunk of pixels before it is summed over the bins of
velocity of the simulation.
"""


def radiance_shift(
    line: "esis_muram_paper.Line",
    emission_measure: na.AbstractScalar,
) -> na.AbstractScalar:
    """
    The radiance of `line` from the plasma in each bin of velocity of the
    simulation, summed over temperature, with no thermal width.

    Parameters
    ----------
    line
        The line to synthesize.
    emission_measure
        The emission measure of the simulation, or a part of it, along the
        axes of temperature and of velocity of the simulation, and any
        others.
    """
    simulation = esis_muram_paper.simulation()
    index = {simulation.axis_temperature: esis_muram_paper.bins(line)}
    g = esis_muram_paper.contribution(line).outputs[index]
    # In single precision, like the emission measure, to keep the product of
    # the two, the largest array along the way, to a few gigabytes.
    g = g.astype(np.float32)
    result = (g * emission_measure[index]).sum(simulation.axis_temperature)
    return (result / (4 * np.pi * u.sr)).to(_unit_radiance)


@functools.cache
def _radiance_shift(line: "esis_muram_paper.Line") -> na.AbstractScalar:
    """:func:`radiance_shift` over the whole box."""
    simulation = esis_muram_paper.simulation()
    return radiance_shift(line, simulation.emission_measure)


@functools.cache
def radiance(line: "esis_muram_paper.Line") -> na.AbstractScalar:
    """
    The radiance of `line` in each pixel of the simulation.

    Parameters
    ----------
    line
        The line to synthesize.
    """
    simulation = esis_muram_paper.simulation()
    return _radiance_shift(line).sum(simulation.axis_shift)


@functools.cache
def radiance_blue(line: "esis_muram_paper.Line") -> na.AbstractScalar:
    """
    The radiance of `line` in each pixel of the simulation from the plasma
    moving toward the observer at :data:`speed_fast` or faster.

    Parameters
    ----------
    line
        The line to synthesize.
    """
    simulation = esis_muram_paper.simulation()
    fast = simulation.shift <= -speed_fast
    return (_radiance_shift(line) * fast).sum(simulation.axis_shift)


@functools.cache
def radiance_red(line: "esis_muram_paper.Line") -> na.AbstractScalar:
    """
    The radiance of `line` in each pixel of the simulation from the plasma
    moving away from the observer at :data:`speed_fast` or faster.

    Parameters
    ----------
    line
        The line to synthesize.
    """
    simulation = esis_muram_paper.simulation()
    fast = simulation.shift >= speed_fast
    return (_radiance_shift(line) * fast).sum(simulation.axis_shift)


@functools.cache
def centroid(line: "esis_muram_paper.Line") -> na.AbstractScalar:
    """
    The mean line-of-sight velocity of the plasma in each pixel of the
    simulation, weighted by its radiance in `line`.

    Parameters
    ----------
    line
        The line to weight the velocity with.
    """
    simulation = esis_muram_paper.simulation()
    weighted = (_radiance_shift(line) * simulation.shift).sum(simulation.axis_shift)
    return weighted / radiance(line)


def binned(
    a: na.AbstractScalar,
    factor: int,
    axes: tuple[str, ...],
) -> na.ScalarArray:
    """
    The sum of `a` over blocks of `factor` elements along each of `axes`.
    The elements past the last whole block are left out.

    Parameters
    ----------
    a
        The array to bin.
    factor
        How many elements of `a` go into each block along each axis.
    axes
        The axes to bin along.
    """
    a = a.explicit
    for axis in axes:
        i = a.axes.index(axis)
        ndarray = a.ndarray
        num = ndarray.shape[i] // factor
        if num * factor != ndarray.shape[i]:
            ndarray = np.take(ndarray, np.arange(num * factor), axis=i)
        shape = ndarray.shape[:i] + (num, factor) + ndarray.shape[i + 1 :]
        a = na.ScalarArray(ndarray.reshape(shape).sum(axis=i + 1), axes=a.axes)
    return a


def spectrum(
    line: "esis_muram_paper.Line",
    emission_measure: na.AbstractScalar,
    width_nonthermal: u.Quantity = 0 * u.km / u.s,
) -> na.FunctionArray:
    """
    The spectral radiance of `line` from `emission_measure`, in the bins of
    :data:`velocity`.

    The plasma in each bin of temperature and of velocity of the simulation
    is given the thermal width of its temperature, and, since its velocity is
    known only to within the bin, the spread of velocity of a bin filled
    evenly, the width of the bin over :math:`\\sqrt{12}`, added in
    quadrature. This is computed with :func:`utu.spectrum.synthesize`.

    Parameters
    ----------
    line
        The line to synthesize.
    emission_measure
        The emission measure of the simulation, or a part of it, along the
        axes of temperature and of velocity of the simulation, and any
        others, which are carried through to the result.
    width_nonthermal
        A nonthermal width added in quadrature to every bin, beyond the
        spread of the bin, as a standard deviation.
    """
    simulation = esis_muram_paper.simulation()
    axis_temperature = simulation.axis_temperature
    axis_shift = simulation.axis_shift
    index = {axis_temperature: esis_muram_paper.bins(line)}

    temperature = simulation.temperature[index]
    mass = fiasco.Ion(line.ion, temperature.ndarray).mass
    width = np.sqrt(
        np.square(simulation.width_shift) / 12 + np.square(width_nonthermal)
    )

    def synthesize(em: na.AbstractScalar) -> na.FunctionArray:
        """The spectrum of `em`, summed over the bins of velocity of the simulation."""
        result = utu.spectrum.synthesize(
            contribution=esis_muram_paper.contribution(line)[index],
            temperature=temperature,
            mass=mass,
            emission_measure=em[index],
            velocity=velocity,
            shift=simulation.shift,
            width_nonthermal=width,
            axis_temperature=axis_temperature,
            axis_velocity=axis_velocity,
        )
        return dataclasses.replace(result, outputs=result.outputs.sum(axis_shift))

    # The spectrum keeps the axis of velocity of the simulation until it is
    # summed over, so it is synthesized a chunk of pixels at a time.
    axis_x = simulation.axis_x
    shape = emission_measure.shape
    if axis_x not in shape:
        return synthesize(emission_measure)
    size_pixel = velocity.size * shape[axis_shift]
    size_pixel *= emission_measure.size // (shape[axis_temperature] * shape[axis_shift])
    size_pixel //= shape[axis_x]
    step = max(1, _size_chunk // size_pixel)
    chunks = [
        synthesize(emission_measure[{axis_x: slice(i, i + step)}])
        for i in range(0, shape[axis_x], step)
    ]
    return dataclasses.replace(
        chunks[0],
        outputs=np.concatenate([c.outputs for c in chunks], axis=axis_x),
    )
