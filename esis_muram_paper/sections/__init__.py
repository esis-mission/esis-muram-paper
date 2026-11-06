"""
The sections of this article, each a factory function returning an
:class:`aastex.Section`.
"""

from ._s0_abstract import abstract
from ._s1_introduction import introduction
from ._s2_simulation import simulation
from ._s3_synthesis import synthesis
from ._s4_events import events
from ._s5_forward import forward
from ._s6_observations import observations
from ._s7_comparison import comparison
from ._s8_discussion import discussion
from ._s9_conclusions import conclusions

__all__ = [
    "abstract",
    "comparison",
    "conclusions",
    "discussion",
    "events",
    "forward",
    "introduction",
    "observations",
    "simulation",
    "synthesis",
]
