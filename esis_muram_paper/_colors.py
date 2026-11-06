"""
The colors shared by the figures of the article.
"""

import matplotlib.colors

__all__ = [
    "cmap_doppler",
    "cmap_fast",
    "color_blue",
    "color_box",
    "color_red",
    "color_reference",
]

color_blue = "#2a78d6"
"""The color of plasma moving toward the observer, and of its lobe."""

color_red = "#eb6834"
"""The color of plasma moving away from the observer, and of its lobe."""

color_box = "#1baf7a"
"""The color of the box around both lobes of an event."""

color_reference = "#52514e"
"""The color of a reference, such as an observed value, drawn beside the simulation."""

cmap_fast = matplotlib.colors.LinearSegmentedColormap.from_list(
    "fast",
    ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"],
)
"""The sequential colormap of the radiance of the fast plasma."""

cmap_doppler = matplotlib.colors.LinearSegmentedColormap.from_list(
    "doppler",
    ["#0d366b", "#2a78d6", "#86b6ef", "#f0efec", "#f1a09f", "#e34948", "#8a1f1f"],
)
"""
The diverging colormap of line-of-sight velocity, blue toward the observer
and red away, with a neutral gray at rest.
"""
