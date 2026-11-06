import aastex

import esis_muram_paper

__all__ = [
    "synthesis",
]


def synthesis() -> aastex.Section:
    result = aastex.Section("Synthetic Spectra")
    result.append(aastex.NoEscape(r"\label{sec:synthesis}"))
    result.append(esis_muram_paper.figures.widths())
    result.append(r"""
\begin{outline}
\item \textbf{Contribution functions.}
    The contribution functions of \OV\ \SI{630}{\angstrom} and \MgX\ \SI{625}{\angstrom} from
    CHIANTI \citep{DelZanna2021} at a constant pressure of \pressure, evaluated at the center of each
    bin of temperature, through the \texttt{utu} package.
\item \textbf{Line profiles.}
    The plasma in each bin of temperature and velocity is given its thermal width, and, since its
    velocity is only known to within the bin, the spread of a bin filled evenly, added in quadrature.
\item \textbf{Line widths} (Figure~\ref{fig:widths}).
    In blocks of \widthsBlockSmall\ the median width of \OV\ is \widthsMedianSmall, and in blocks of
    \widthsBlockLarge\ it is \widthsMedianLarge, against \widthsObserved\ observed by \SUMER\
    \citep{Chae1998}.
    Only \widthsFractionSmall\ and \widthsFractionLarge\ of the radiance comes from blocks as wide as
    that, and even the mean spectrum of the whole box, which includes every flow in it, is only
    \widthsBox\ wide.
    Most of the width of the simulation is thermal (\widthsThermal).
\item \textbf{What to do about it.}
    The \ESIS\ observation is simulated both as it is and with a nonthermal width added to every bin
    to match the observed width, which brackets how much the width of the quiet background matters to
    finding \EEs\ in it.
    \matthias{Is the missing nonthermal width expected at this resolution, and is there a run at a
    finer one?}
\end{outline}
""")
    return result
