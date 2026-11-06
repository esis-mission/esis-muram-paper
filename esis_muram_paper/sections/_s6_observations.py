import aastex

__all__ = [
    "observations",
]


def observations() -> aastex.Section:
    result = aastex.Section("Explosive Events Observed by ESIS")
    result.append(aastex.NoEscape(r"\label{sec:observations}"))
    result.append(r"""
\begin{outline}
\item \textbf{The data.}
    The \OV\ exposures of the first flight of \ESIS, on 2019 September 30 \citep{Parker2022}, inverted
    with \MART.
\item \textbf{The search.}
    The criteria of Section~\ref{sec:events} applied to every inverted exposure, which finds
    \esisNumEvents\ events.
    The width of \OV\ observed by \ESIS\ in the quiet background is \esisWidth, beside the
    \widthsObserved\ of \SUMER.
\item \textbf{Against the events of \citet{Parker2022}.}
    Which of the events they reported the search finds, and which it finds that they did not.
\end{outline}
""")
    return result
