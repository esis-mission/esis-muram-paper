import aastex
import astropy.units as u
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np

import esis_muram_paper

from ._images import image

__all__ = [
    "fraction_dim",
    "overview",
    "radius_marker",
    "velocity_limit",
]

fraction_dim = 0.3
"""
The fraction of the median radiance below which a pixel is too dim in O V for
its velocity to be drawn.
"""

velocity_limit = 40 * u.km / u.s
"""The velocity at either end of the colormap of the Doppler shifts."""

radius_marker = 6 * u.Mm
"""The radius of the circle drawn around each event."""


def overview() -> aastex.FigureStar:
    """
    The radiance of O V, its Doppler shift, and the radiance of its fast
    plasma, over the whole box of the simulation, with the events circled.
    """
    line = esis_muram_paper.O_V
    total = esis_muram_paper.radiance(line)
    median = np.median(total)
    centroid = esis_muram_paper.centroid(line)
    fast = esis_muram_paper.radiance_blue(line) + esis_muram_paper.radiance_red(line)
    speed = esis_muram_paper.speed_fast.to_value(u.km / u.s)
    limit = velocity_limit.to_value(u.km / u.s)

    fig, axs = plt.subplots(
        ncols=3,
        sharex=True,
        sharey=True,
        figsize=(aastex.text_width_inches, 0.47 * aastex.text_width_inches),
        constrained_layout=True,
    )

    panels = [
        (
            total / median,
            {"cmap": "gray", "norm": matplotlib.colors.LogNorm(0.1, 300)},
            rf"{line.label_plot} radiance over median",
        ),
        (
            np.where(
                total >= fraction_dim * median,
                (centroid / (u.km / u.s)).to(u.dimensionless_unscaled),
                np.nan,
            ),
            {
                "cmap": esis_muram_paper.cmap_doppler,
                "norm": matplotlib.colors.TwoSlopeNorm(0, -limit, limit),
            },
            r"Doppler shift (km\,s$^{-1}$)",
        ),
        (
            fast / median,
            {
                "cmap": esis_muram_paper.cmap_fast,
                "norm": matplotlib.colors.LogNorm(0.03, 30),
            },
            rf"$|v| \geq {speed:.0f}$\,km\,s$^{{-1}}$ over median",
        ),
    ]
    for ax, (a, kwargs, label) in zip(axs, panels):
        mappable = image(ax, a, **kwargs)
        fig.colorbar(mappable, ax=ax, location="bottom", label=label, shrink=0.9)
        ax.set_xlabel("$x$ (Mm)")
        for i, event in enumerate(esis_muram_paper.events()):
            position = event.position
            x = position.x.ndarray.to_value(u.Mm)
            y = position.y.ndarray.to_value(u.Mm)
            radius = radius_marker.to_value(u.Mm)
            # Alternate the labels above and below the circles, so that
            # those of neighboring events do not overlap.
            side = 1 if i % 2 == 0 else -1
            ax.add_patch(
                plt.Circle(
                    (x, y),
                    radius,
                    fill=False,
                    edgecolor=esis_muram_paper.color_red,
                    linewidth=0.8,
                )
            )
            ax.annotate(
                event.name,
                xy=(x + radius, y + side * radius),
                va="bottom" if side > 0 else "top",
                fontsize=7,
                bbox={
                    "boxstyle": "round,pad=0.1",
                    "facecolor": "white",
                    "linewidth": 0,
                },
            )
    axs[0].set_ylabel("$y$ (Mm)")
    for ax in axs:
        ax.set_aspect("equal")

    result = aastex.FigureStar("fig:overview", position="t")
    result.add_fig(fig, width=None)
    result.add_caption(aastex.NoEscape(r"""
The snapshot of the simulation at $t = \simulationTime$, over the whole box of
\simulationWidth\ at its resolution of \simulationPitch, seen from above.
Left: the radiance of \OV\ \SI{630}{\angstrom}, synthesized from the \VDEM, over its median.
Middle: the mean line-of-sight velocity of the plasma, weighted by its radiance in \OV, positive away
from the observer, where the radiance is at least \overviewFractionDim\ of the median.
Right: the radiance of \OV\ from the plasma moving at \speedFast\ or faster either way, over the median
radiance.
The circles mark the \eventsNum\ events brightest in this fast plasma, named in order of its radiance.
"""))
    return result
