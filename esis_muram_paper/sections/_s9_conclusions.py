import aastex

__all__ = [
    "conclusions",
]


def conclusions() -> aastex.Section:
    result = aastex.Section("Conclusions")
    result.append(r"""
\begin{outline}
\item The findings, one per item, once the comparison is done.
\end{outline}
""")
    return result
