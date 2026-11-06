import aastex

__all__ = [
    "comparison",
]


def comparison() -> aastex.Section:
    result = aastex.Section("Simulated and Observed Explosive Events")
    result.append(aastex.NoEscape(r"\label{sec:comparison}"))
    result.append(r"""
\begin{outline}
\item \textbf{Populations.}
    The distributions of area, speed and extent of each lobe, asymmetry of the wings, and contrast with
    the background, for the events of the synthetic observations and of the flight data, found the same
    way.
\item \textbf{Rates.}
    The number of events per unit area of the quiet Sun in each.
\item \textbf{Event M1 as \ESIS\ would see it,} against the most similar observed event.
\end{outline}
""")
    return result
