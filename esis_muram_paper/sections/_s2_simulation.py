import aastex

import esis_muram_paper

__all__ = [
    "simulation",
]


def simulation() -> aastex.Section:
    result = aastex.Section("The Simulation")
    result.append(aastex.NoEscape(r"\label{sec:simulation}"))
    result.append(esis_muram_paper.figures.overview())
    result.append(r"""
\begin{outline}
\item \textbf{The run.}
    A simulation of the quiet Sun with \MURaM\ \citep{Vogler2005,Rempel2017}, in a box
    \simulationWidth\ wide with pixels of \simulationPitch, from the convection zone into the corona.
    \matthias{The depth of the box, the vertical resolution, the magnetic setup (mean flux, dynamo or
    imposed field), how long the run has gone, and the paper to cite for this run.}
\item \textbf{The \VDEM.}
    For each pixel, the emission measure of the plasma along a vertical line of sight, binned in
    $\log_{10} T$ from \simulationTemperatureMin\ to \simulationTemperatureMax\ and in line-of-sight
    velocity from \simulationVelocityMin\ to \simulationVelocityMax\ in steps of
    \simulationVelocityStep, the format used for \MUSE.
    \matthias{Whether the emission measure is that of $n_e^2$ or of $n_e n_H$, which way the velocity is
    positive, and the paper to cite for the format.}
    We take positive velocities as away from the observer, which puts the redshift of the \TR, averaged
    over the box, on the red side, as it is observed.
\item \textbf{The snapshot.}
    One snapshot, at $t = \simulationTime$ (Figure~\ref{fig:overview}).
    The lifetime of an \EE\ is about a minute and the cadence of \ESIS\ is several seconds, so a
    comparison of their evolution needs a series of snapshots.
    \matthias{Could the \VDEM\ be computed for a series of snapshots around this one, every
    \SI{10}{\second} or so, covering a few minutes?}
\end{outline}
""")
    return result
