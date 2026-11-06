import aastex

import esis_muram_paper

__all__ = [
    "events",
]


def events() -> aastex.Section:
    result = aastex.Section("Explosive Events in the Simulation")
    result.append(aastex.NoEscape(r"\label{sec:events}"))
    result.append(esis_muram_paper.figures.event())
    result.append(r"""
\begin{outline}
\item \textbf{Finding them.}
    An event is a connected region of pixels whose plasma moving at \speedFast\ or faster, either way,
    is brighter in \OV\ than \eventsPercentile\ percent of the box and makes up at least
    \eventsFraction\ of the radiance of the pixel.
    The same criteria are applied to the inversions of the \ESIS\ data in
    Section~\ref{sec:observations}, so that both sides of the comparison are found the same way.
    The events are named M1, M2, and so on, in order of the radiance of their fast plasma, so as not to
    be confused with the events of \citet{Parker2022}.
\item \textbf{Event M1} (Figure~\ref{fig:event}), at $(\eventX, \eventY)$.
    A lobe of \eventAreaBlue\ moving toward the observer at \eventSpeedBlue\ on average, with wings
    reaching \eventExtentBlue, and a lobe of \eventAreaRed\ moving away at \eventSpeedRed,
    \eventSeparation\ from it.
    In the \eventsBox\ box around both, about two resolution elements of \ESIS, the width of \OV\ is
    \eventWidthBox.
    The fast plasma of the blue lobe spans the whole \TR, from the coolest bin of the simulation to
    nearly coronal temperatures, and \MgX\ brightens beside it.
\item \textbf{The population.}
    A table of the events: position, area, speeds and extents of each lobe, asymmetry of the wings,
    contrast with the background in \OV\ and \MgX.
\item \textbf{What a snapshot cannot say.}
    Lifetimes, and whether the lobes move apart, need the series of snapshots asked for in
    Section~\ref{sec:simulation}.
\end{outline}
""")
    return result
