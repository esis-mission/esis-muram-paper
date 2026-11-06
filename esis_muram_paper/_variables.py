import aastex
import astropy.units as u
import named_arrays as na
import numpy as np

import esis_muram_paper

__all__ = [
    "variables",
]


def _pending(name: str) -> aastex.Variable:
    """
    A quantity the analysis has not produced yet, marked where it is cited.

    Every number in this article is computed by the analysis, and these are
    the ones it has no answer for yet. They are written into the text as a
    bold ``XX`` rather than guessed at or left out, so that a draft shows
    plainly what is still owed and no placeholder can be mistaken for a
    measurement. ``??`` is avoided since it is what LaTeX prints for an
    unresolved cross-reference, which the tests look for.
    """
    return aastex.Variable(name=name, value=aastex.NoEscape(r"\textbf{XX}"))


def _simulation() -> list[aastex.Variable]:
    """The numbers describing the snapshot of the simulation."""
    simulation = esis_muram_paper.simulation()
    temperature = simulation.temperature.ndarray
    shift = simulation.shift.ndarray
    return [
        aastex.Variable("simulationTime", np.round(simulation.time)),
        aastex.Variable("simulationWidth", np.round(simulation.width, 1)),
        aastex.Variable("simulationPitch", np.round(simulation.pitch.to(u.km))),
        aastex.Variable(
            "simulationTemperatureMin",
            round(float(np.log10(temperature.min().to_value(u.K))), 1),
        ),
        aastex.Variable(
            "simulationTemperatureMax",
            round(float(np.log10(temperature.max().to_value(u.K))), 1),
        ),
        aastex.Variable("simulationVelocityMin", np.round(shift.min())),
        aastex.Variable("simulationVelocityMax", np.round(shift.max())),
        aastex.Variable("simulationVelocityStep", np.round(simulation.width_shift)),
        aastex.Variable("pressure", esis_muram_paper.pressure),
    ]


def _overview() -> list[aastex.Variable]:
    """The numbers in the caption of :func:`esis_muram_paper.figures.overview`."""
    figure = esis_muram_paper.figures._overview
    return [
        aastex.Variable(
            "overviewFractionDim", round(100 * figure.fraction_dim) * u.percent
        ),
        aastex.Variable("speedFast", esis_muram_paper.speed_fast),
    ]


def _events() -> list[aastex.Variable]:
    """The numbers describing the events of the simulation, and M1 in particular."""
    module = esis_muram_paper._events
    simulation = esis_muram_paper.simulation()
    m1 = esis_muram_paper.events()[0]
    lobes = esis_muram_paper.lobes(m1)
    spectra = esis_muram_paper.figures._event.profiles(lobes)

    def center(mask: na.AbstractScalar) -> na.Cartesian2dVectorArray:
        """The center of the pixels of `mask`."""
        return (simulation.position * mask).sum() / mask.sum()

    def moments(spectrum: na.FunctionArray) -> tuple[u.Quantity, u.Quantity]:
        """The mean velocity and the standard deviation of `spectrum`."""
        axis = esis_muram_paper.axis_velocity
        velocity = esis_muram_paper.velocity.cell_centers(axis)
        radiance = spectrum.outputs
        mean = (velocity * radiance).sum(axis) / radiance.sum(axis)
        variance = (np.square(velocity - mean) * radiance).sum(axis) / radiance.sum(
            axis
        )
        return mean.ndarray.to(u.km / u.s), np.sqrt(variance).ndarray.to(u.km / u.s)

    def extent(spectrum: na.FunctionArray) -> u.Quantity:
        """The fastest velocity toward the observer at which `spectrum` is a hundredth of its peak."""
        axis = esis_muram_paper.axis_velocity
        velocity = esis_muram_paper.velocity.cell_centers(axis)
        radiance = spectrum.outputs
        bright = radiance >= radiance.max() / 100
        return np.where(bright, velocity, np.inf).min().ndarray.to(u.km / u.s)

    blue, red = center(lobes.blue), center(lobes.red)
    separation = np.sqrt(np.square(blue - red).x + np.square(blue - red).y)
    mean_blue, _ = moments(spectra["blue lobe"])
    mean_red, _ = moments(spectra["red lobe"])
    _, sigma_box = moments(spectra["box around both"])
    position = m1.position
    num = module.size_box / simulation.pitch
    num = int(np.round(num.to(u.dimensionless_unscaled)))
    return [
        aastex.Variable("eventsNum", module.num_events),
        aastex.Variable("eventsPercentile", module.percentile_fast),
        aastex.Variable(
            "eventsFraction", round(100 * module.fraction_fast) * u.percent
        ),
        aastex.Variable(
            "eventsFractionLobe", round(100 * module.fraction_lobe) * u.percent
        ),
        aastex.Variable("eventsWindow", module.size_window),
        aastex.Variable("eventsBox", np.round(num * simulation.pitch, 1)),
        aastex.Variable("eventX", np.round(position.x.ndarray, 1)),
        aastex.Variable("eventY", np.round(position.y.ndarray, 1)),
        aastex.Variable(
            "eventAreaBlue", np.round(lobes.blue.sum().ndarray * simulation.pitch**2, 1)
        ),
        aastex.Variable(
            "eventAreaRed", np.round(lobes.red.sum().ndarray * simulation.pitch**2, 2)
        ),
        aastex.Variable("eventSeparation", np.round(separation.ndarray, 1)),
        aastex.Variable("eventSpeedBlue", np.round(np.abs(mean_blue))),
        aastex.Variable("eventSpeedRed", np.round(np.abs(mean_red))),
        aastex.Variable(
            "eventExtentBlue", np.round(np.abs(extent(spectra["blue lobe"])))
        ),
        aastex.Variable("eventWidthBox", np.round(sigma_box)),
    ]


def _widths() -> list[aastex.Variable]:
    """The numbers in the caption of :func:`esis_muram_paper.figures.widths`."""
    figure = esis_muram_paper.figures._widths
    pitch = esis_muram_paper.simulation().pitch
    observed = figure.sigma_observed()

    result = [
        aastex.Variable("widthsXi", figure.xi_observed),
        aastex.Variable("widthsObserved", np.round(observed)),
        aastex.Variable(
            "widthsTemperature", np.round(figure.temperature_peak().to(u.MK), 2)
        ),
        aastex.Variable("widthsThermal", np.round(figure.sigma_thermal())),
        aastex.Variable(
            "widthsBox", np.round(figure.width(None)[0].ndarray.to(u.km / u.s))
        ),
    ]
    for binning, name in zip(figure.binnings, ["Small", "Large"]):
        sigma, radiance = figure.width(binning)
        weight = radiance / radiance.sum()
        median = np.median(sigma).ndarray.to(u.km / u.s)
        fraction = (weight * (sigma >= observed)).sum().ndarray
        result += [
            aastex.Variable(
                f"widthsBlock{name}",
                np.round(figure.angle(binning * pitch), 1),
            ),
            aastex.Variable(f"widthsMedian{name}", np.round(median)),
            aastex.Variable(
                f"widthsFraction{name}",
                np.round(100 * fraction.to(u.dimensionless_unscaled), 1) * u.percent,
            ),
        ]
    return result


def _pendings() -> list[aastex.Variable]:
    """The numbers the analysis of ESIS has not produced yet."""
    return [
        _pending("esisNumEvents"),
        _pending("esisWidth"),
        _pending("comparisonSummary"),
    ]


def variables() -> list[aastex.Variable]:
    """
    The numbers quoted in the article, each as a LaTeX macro.
    """
    return [
        *_simulation(),
        *_overview(),
        *_events(),
        *_widths(),
        *_pendings(),
    ]
