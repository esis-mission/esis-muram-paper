import aastex

__all__ = [
    "introduction",
]


def introduction() -> aastex.Section:
    result = aastex.Section("Introduction")
    result.append(r"""
\begin{outline}
\item \textbf{Explosive events.}
    \EEs\ are brightenings of \TR\ lines such as \CIV, \SiIV, and \OV, about \SI{1.5}{\mega\meter}
    across and a minute long, whose line profiles reach \SI{100}{\kilo\meter\per\second} or more in
    one or both wings \citep{Dere1989,Dere1991}.
    The bidirectional jets seen in rasters across them \citep{Innes1997} made them the canonical
    signature of magnetic reconnection in the \TR, and the profiles seen by \IRIS\ have been read as
    evidence of the plasmoid instability \citep{Innes2015}.
\item \textbf{Why a simulation.}
    A slit spectrograph sees an \EE\ one slit position at a time, so the spatial structure of the
    flows, which distinguishes the models, is mostly inferred.
    Radiative \MHD\ simulations of the quiet Sun now reach the corona \citep{Rempel2017}, and
    form their own \EEs.
    Whether those look like the observed ones, in size, speed, asymmetry, and brightness, is a test of
    the simulation and of the reconnection picture.
\item \textbf{Why \ESIS.}
    \ESIS\ \citep{Parker2022}, a slitless \CTIS\ in the tradition of \citet{Kankelborg2001}, records
    the spectral cube of a wide field at once, so it sees every \EE\ in its field, whole, in each
    exposure, which suits a comparison of populations.
    Its first flight recorded several \EEs\ in \OV\ \citep{Parker2022}.
    But the cube is only recovered by inversion, so the fair comparison is between the observations
    and synthetic \ESIS\ observations of the simulation inverted in the same way.
\item \textbf{This article.}
    Section~\ref{sec:simulation} describes the simulation and its \VDEM, Section~\ref{sec:synthesis}
    the synthesis of its spectra and their widths, Section~\ref{sec:events} its \EEs,
    Section~\ref{sec:forward} the synthetic \ESIS\ observations, Section~\ref{sec:observations} the
    \EEs\ found in the flight data, and Section~\ref{sec:comparison} the comparison.
\end{outline}
""")
    return result
