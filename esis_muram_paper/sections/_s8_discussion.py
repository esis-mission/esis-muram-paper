import aastex

__all__ = [
    "discussion",
]


def discussion() -> aastex.Section:
    result = aastex.Section("Discussion")
    result.append(r"""
\begin{outline}
\item What the agreements and disagreements say about reconnection in the quiet \TR, and about the
    simulation: its resolution, the missing nonthermal width, and its magnetic setup.
\item What a series of snapshots would add: lifetimes, and whether the lobes move apart.
\item What the comparison says about \CTIS\ as a way to study \EEs.
\end{outline}
""")
    return result
