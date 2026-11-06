import aastex
import astropy.units as u
import matplotlib.axes
import matplotlib.colors
import matplotlib.pyplot as plt
import named_arrays as na
import numpy as np

import esis_muram_paper

from ._images import image

__all__ = [
    "event",
    "profiles",
]


def profiles(
    lobes: "esis_muram_paper.Lobes",
) -> dict[str, na.FunctionArray]:
    """
    The spectra of O V, with their thermal widths, of the blue lobe, the red
    lobe, and the box around both of `lobes`, each summed over its pixels,
    and the spectrum of the whole box of the simulation, averaged over its
    pixels.

    Parameters
    ----------
    lobes
        The lobes of the event.
    """
    line = esis_muram_paper.O_V
    simulation = esis_muram_paper.simulation()
    em = simulation.emission_measure
    axes = simulation.axis_xy
    num = simulation.position.x.shape[simulation.axis_x]
    num *= simulation.position.y.shape[simulation.axis_y]
    return {
        "blue lobe": esis_muram_paper.spectrum(line, (em * lobes.blue).sum(axes)),
        "red lobe": esis_muram_paper.spectrum(line, (em * lobes.red).sum(axes)),
        "box around both": esis_muram_paper.spectrum(line, em[lobes.box].sum(axes)),
        "mean of the whole box": esis_muram_paper.spectrum(line, em.sum(axes) / num),
    }


def _outline(
    ax: "matplotlib.axes.Axes",
    mask: na.AbstractScalar,
    window: dict[str, slice],
    color: str,
) -> None:
    """Outline the pixels of `mask` within `window`."""
    simulation = esis_muram_paper.simulation()
    axis_x, axis_y = simulation.axis_xy
    x = simulation.position.x[{axis_x: window[axis_x]}].ndarray.to_value(u.Mm)
    y = simulation.position.y[{axis_y: window[axis_y]}].ndarray.to_value(u.Mm)
    values = mask[window].explicit.ndarray_aligned((axis_y, axis_x))
    ax.contour(x, y, values.astype(float), levels=[0.5], colors=color, linewidths=0.8)


def _box(ax: "matplotlib.axes.Axes", box: dict[str, slice]) -> None:
    """Draw the edges of the pixels of `box`."""
    simulation = esis_muram_paper.simulation()
    axis_x, axis_y = simulation.axis_xy
    x = simulation.position.x[{axis_x: box[axis_x]}].ndarray.to_value(u.Mm)
    y = simulation.position.y[{axis_y: box[axis_y]}].ndarray.to_value(u.Mm)
    half = simulation.pitch.to_value(u.Mm) / 2
    ax.add_patch(
        plt.Rectangle(
            (x.min() - half, y.min() - half),
            x.max() - x.min() + 2 * half,
            y.max() - y.min() + 2 * half,
            fill=False,
            edgecolor=esis_muram_paper.color_box,
            linewidth=0.8,
        )
    )


def event() -> aastex.FigureStar:
    """
    The brightest event of the simulation, M1: maps of its radiance in O V
    and Mg X and of the radiance of its fast plasma, its spectra in O V, and
    the emission measure of its lobes in temperature and velocity.
    """
    simulation = esis_muram_paper.simulation()
    line = esis_muram_paper.O_V
    m1 = esis_muram_paper.events()[0]
    lobes = esis_muram_paper.lobes(m1)
    window = lobes.window

    total = esis_muram_paper.radiance(line)
    median = np.median(total)
    mg_x = esis_muram_paper.radiance(esis_muram_paper.Mg_X)
    speed = esis_muram_paper.speed_fast.to_value(u.km / u.s)

    fig = plt.figure(
        figsize=(aastex.text_width_inches, 0.62 * aastex.text_width_inches),
        constrained_layout=True,
    )
    grid = fig.add_gridspec(nrows=2, ncols=4, height_ratios=[1, 0.95])
    maps = [fig.add_subplot(grid[0, 0])]
    maps += [
        fig.add_subplot(grid[0, i], sharex=maps[0], sharey=maps[0]) for i in (1, 2, 3)
    ]

    norm_fast = matplotlib.colors.LogNorm(0.1, 300)
    panels = [
        (
            total / median,
            {"cmap": "gray", "norm": matplotlib.colors.LogNorm(0.3, 1000)},
            rf"{line.label_plot} over median",
        ),
        (
            esis_muram_paper.radiance_blue(line) / median,
            {"cmap": esis_muram_paper.cmap_fast, "norm": norm_fast},
            rf"$v \leq -{speed:.0f}$\,km\,s$^{{-1}}$ over median",
        ),
        (
            esis_muram_paper.radiance_red(line) / median,
            {"cmap": esis_muram_paper.cmap_fast, "norm": norm_fast},
            rf"$v \geq {speed:.0f}$\,km\,s$^{{-1}}$ over median",
        ),
        (
            mg_x / np.median(mg_x),
            {"cmap": "gray", "norm": matplotlib.colors.LogNorm(0.3, 30)},
            rf"{esis_muram_paper.Mg_X.label_plot} over median",
        ),
    ]
    for ax, (a, kwargs, label) in zip(maps, panels):
        mappable = image(ax, a, window=window, **kwargs)
        fig.colorbar(mappable, ax=ax, location="bottom", label=label, shrink=0.9)
        _outline(ax, lobes.blue, window, esis_muram_paper.color_blue)
        _outline(ax, lobes.red, window, esis_muram_paper.color_red)
        _box(ax, lobes.box)
        ax.set_xlabel("$x$ (Mm)")
        ax.set_aspect("equal")
    maps[0].set_ylabel("$y$ (Mm)")
    for ax in maps[1:]:
        ax.tick_params(labelleft=False)

    ax = fig.add_subplot(grid[1, :2])
    colors = [
        esis_muram_paper.color_blue,
        esis_muram_paper.color_red,
        esis_muram_paper.color_box,
        esis_muram_paper.color_reference,
    ]
    for (name, spectrum), color in zip(profiles(lobes).items(), colors):
        radiance = spectrum.outputs
        ax.stairs(
            (radiance / radiance.max()).ndarray.to_value(u.dimensionless_unscaled),
            esis_muram_paper.velocity.ndarray.to_value(u.km / u.s),
            color=color,
            linestyle="--" if name.startswith("mean") else "-",
            label=name,
        )
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1.5)
    ax.set_xlim(-250, 250)
    for v in (-100, -speed, speed, 100):
        ax.axvline(v, color="0.85", linewidth=0.5, zorder=0)
    ax.set_xlabel(r"line-of-sight velocity (km\,s$^{-1}$)")
    ax.set_ylabel("spectrum over its peak")
    ax.legend(frameon=False, fontsize=7, loc="lower right")

    g = esis_muram_paper.contribution(line).outputs
    g = (g / g.max()).ndarray.to_value(u.dimensionless_unscaled)
    log_temperature = np.log10(simulation.temperature.ndarray.to_value(u.K))
    shift = simulation.shift.ndarray.to_value(u.km / u.s)
    width = simulation.width_shift.to_value(u.km / u.s)
    axes = simulation.axis_xy
    for i, (name, mask) in enumerate(
        [("blue lobe", lobes.blue), ("red lobe", lobes.red)]
    ):
        ax = fig.add_subplot(grid[1, 2 + i])
        em = (simulation.emission_measure * mask).sum(axes)
        em = em.ndarray_aligned((simulation.axis_temperature, simulation.axis_shift))
        em = em.to_value(u.cm**-5)
        mappable = ax.imshow(
            em,
            origin="lower",
            aspect="auto",
            interpolation="none",
            cmap=esis_muram_paper.cmap_fast,
            norm=matplotlib.colors.LogNorm(em.max() * 1e-4, em.max()),
            extent=(
                shift.min() - width / 2,
                shift.max() + width / 2,
                log_temperature.min() - 0.05,
                log_temperature.max() + 0.05,
            ),
        )
        fig.colorbar(
            mappable,
            ax=ax,
            location="bottom",
            label=r"emission measure (cm$^{-5}$)",
            shrink=0.9,
        )
        ax.plot(shift.min() + 60 * g, log_temperature, color="black", linewidth=0.8)
        ax.axvline(0, color="0.5", linewidth=0.5)
        ax.set_title(name, fontsize=8)
        ax.set_xlabel(r"velocity (km\,s$^{-1}$)")
        if i == 0:
            ax.set_ylabel(r"$\log_{10} T$ (K)")
        else:
            ax.tick_params(labelleft=False)

    result = aastex.FigureStar("fig:event", position="t")
    result.add_fig(fig, width=None)
    result.add_caption(aastex.NoEscape(r"""
Event M1, the brightest event of the simulation in fast plasma, within \eventsWindow\ of its center.
Top, from left: the radiance of \OV\ \SI{630}{\angstrom}, of the \OV\ plasma moving toward the
observer at \speedFast\ or faster, of that moving away from the observer at \speedFast\ or faster,
each over the median radiance of \OV\ over the box, and the radiance of \MgX\ \SI{625}{\angstrom}
over its own median.
The blue and orange outlines are the lobes of the event, which make up \eventsFractionLobe\ or more of
the radiance of their pixels, and the green square is the \eventsBox\ box around both.
Bottom left: the spectra of \OV\ of the two lobes and of the box, each summed over its pixels, and
the mean spectrum of the whole box (dashed), each over its peak, with the thermal width of each
temperature.
Bottom right: the emission measure of each lobe in temperature and line-of-sight velocity, with the
contribution function of \OV\ (black) for reference.
"""))
    return result
