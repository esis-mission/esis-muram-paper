import aastex

__all__ = [
    "acknowledgments",
]


def acknowledgments() -> aastex.Acknowledgments:
    """
    The acknowledgments of this article.

    The grants are those of the ESIS flight, as the instrument paper and the
    paper on event E acknowledge them. The sentence on CHIANTI is the
    acknowledgment CHIANTI asks of the articles which use it, as the
    contribution functions do.
    """
    result = aastex.Acknowledgments()
    result.append(r"""
We gratefully acknowledge the support of the NASA Heliophysics Low-Cost Access to Space program, grant number
NNX14AK71G, and of the NASA Earth and Space Science Fellowship program, grant number 80NSSC17K0524.
\matthias{The acknowledgment of NSF NCAR, and of the computing time the simulation ran on.}
CHIANTI is a collaborative project involving George Mason University, the University of Michigan (USA), University of
Cambridge (UK) and NASA Goddard Space Flight Center (USA).
This article is an executable paper: every figure, table, and number in it is computed from the
data when the article is built, and the code that builds it is available at
\url{https://github.com/esis-mission/esis-muram-paper}.""")
    return result
