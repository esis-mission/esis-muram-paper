import aastex

__all__ = [
    "forward",
]


def forward() -> aastex.Section:
    result = aastex.Section("Synthetic ESIS Observations")
    result.append(aastex.NoEscape(r"\label{sec:forward}"))
    result.append(r"""
\begin{outline}
\item \textbf{The scene.}
    The spectral radiance of the simulation in every line in the passband of \ESIS, placed at disk
    center and resampled to the plate scale of \ESIS.
    The box is \simulationWidth\ wide, smaller than the field of \ESIS, so the scene is the box alone,
    or the box tiled.
\item \textbf{The instrument.}
    The model of the first flight of \ESIS\ in the \texttt{esis} package, through the
    \texttt{optika} raytrace, with its point-spread function, vignetting, and the noise of its cameras,
    gives the images of each channel.
\item \textbf{The inversion.}
    The images are inverted with \MART\ \citep{Gordon1970,Okamoto1991} as the flight data are, in the
    \texttt{ctis} package.
    \roy{The Level-4 \MART\ inversions of \texttt{esis} are not merged yet (esis\#70).}
\item \textbf{What survives.}
    The recovered cube against the truth: which events are found, and how their speeds, extents,
    asymmetries, and widths are biased, for the simulation as it is and with the observed width.
\end{outline}
""")
    return result
