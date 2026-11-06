"""
Create the figures and compile the LaTeX files for this article.
"""

from . import figures, sections, tables
from ._acknowledgments import acknowledgments
from ._acronyms import acronyms
from ._authors import authors
from ._colors import (
    cmap_doppler,
    cmap_fast,
    color_blue,
    color_box,
    color_red,
    color_reference,
)
from ._document import document, pdf
from ._events import Event, Lobes, events, lobes
from ._keywords import keywords
from ._lines import O_V, Line, Mg_X, bins, contribution, pressure
from ._muram import Simulation, archive, directory_default, simulation
from ._preamble import preamble
from ._spectra import (
    axis_velocity,
    binned,
    centroid,
    radiance,
    radiance_blue,
    radiance_red,
    radiance_shift,
    spectrum,
    speed_fast,
    velocity,
)
from ._style import rc
from ._url import url
from ._variables import variables

__all__ = [
    "O_V",
    "Event",
    "Line",
    "Lobes",
    "Mg_X",
    "Simulation",
    "acknowledgments",
    "acronyms",
    "archive",
    "authors",
    "axis_velocity",
    "binned",
    "bins",
    "centroid",
    "cmap_doppler",
    "cmap_fast",
    "color_blue",
    "color_box",
    "color_red",
    "color_reference",
    "contribution",
    "directory_default",
    "document",
    "events",
    "figures",
    "keywords",
    "lobes",
    "pdf",
    "preamble",
    "pressure",
    "radiance",
    "radiance_blue",
    "radiance_red",
    "radiance_shift",
    "rc",
    "sections",
    "simulation",
    "spectrum",
    "speed_fast",
    "tables",
    "url",
    "variables",
    "velocity",
]
